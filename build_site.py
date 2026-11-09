#!/usr/bin/env python3
"""
build_site.py — turn projects.py into the site.

  python3 build_site.py          build everything
  ./publish "message"            build, check, commit, push

What it writes
  index.html                       project cards, in the order given in projects.py
  projects/<slug>/index.html       generated hubs (manuscript section stripped) and
                                   the tab bar for hand-written ones
  projects/<slug>/paper/index.html a passphrase-gated manuscript (AES-256-CBC,
                                   PBKDF2-SHA256, HMAC-SHA256; decrypted in the browser)
  the tab bar in every hand-written page

Nothing here is a source of truth. Copy lives in projects.py; passphrases live in
_secrets/passwords.json; manuscripts live wherever projects.py points. All three
are outside the commit except projects.py.
"""
import io
import os
import re, sys, json, base64, hashlib, hmac, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import projects as CFG

SECRETS = os.path.join(ROOT, "_secrets", "passwords.json")
GATECACHE = os.path.join(ROOT, "_secrets", ".gatecache.json")
PBKDF2_ITERATIONS = 250_000
MASTER_KEY_ID = "masterkey"

def expand(p):
    """Resolve a path from projects.py.

    Absolute or ~-prefixed paths are used as given. Anything else is looked for
    first inside the repo, then under each SOURCE_ROOTS entry in order; the first
    hit wins. That way one machine's ~/Documents and another's mount point both
    resolve the same config."""
    if p.startswith("~") or os.path.isabs(p):
        return os.path.expanduser(p)
    local = os.path.normpath(os.path.join(ROOT, p))
    if os.path.exists(local):
        return local
    for r in getattr(CFG, "SOURCE_ROOTS", []):
        cand = os.path.join(os.path.expanduser(r), p)
        if os.path.exists(cand):
            return cand
    return local

def warn(msg):   print("  !! " + msg)
def note(msg):   print("     " + msg)

# ------------------------------------------------------------------ head + chrome

HEAD_TAGS = """
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="48x48" href="/assets/favicon-48.png">
<link rel="icon" type="image/png" sizes="96x96" href="/assets/favicon-96.png">
<link rel="icon" type="image/png" sizes="192x192" href="/assets/favicon-192.png">
<link rel="icon" type="image/png" sizes="512x512" href="/assets/favicon-512.png">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#111111">
<meta property="og:site_name" content="Henry M. Blair">
<meta property="og:image" content="https://henryblair.online/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
"""

SITEBAR_CSS = """
<style id="site-nav-css">
:root{--sitebar:34px;--badge:160px}
.sb-badge{position:fixed;top:0;left:0;width:var(--badge);height:var(--badge);z-index:120;background:#111;
  display:flex;align-items:center;justify-content:center;border-right:1px solid #333;
  border-bottom:1px solid #333;border-radius:0;text-decoration:none}
.sb-badge img{width:76%;height:76%;border-radius:50%;display:block;
  transition:transform .15s ease,box-shadow .15s ease}
.sb-badge:hover img{transform:scale(1.05);box-shadow:0 0 0 2px #f4f4f2}
.sb-badge:focus-visible img{outline:2px solid #fff;outline-offset:2px}
.sitebar{position:fixed;top:0;left:var(--badge);right:0;height:34px;z-index:100;
  display:flex;align-items:stretch;background:#111;color:#fff;
  font-family:ui-sans-serif,-apple-system,"Segoe UI",Inter,"Helvetica Neue",Arial,sans-serif;
  font-size:12px;overflow-x:auto;scrollbar-width:none}
.sitebar::-webkit-scrollbar{display:none}
.sitebar .sb-brand{display:flex;align-items:center;padding:0 14px;font-weight:800;
  letter-spacing:.12em;text-transform:uppercase;color:#fff;text-decoration:none;
  border:0;border-right:1px solid #333;white-space:nowrap}
.sitebar .sb-tabs{display:flex;align-items:stretch}
.sitebar .sb-tabs a{display:flex;align-items:center;padding:0 14px;color:#b9bcbf;
  text-decoration:none;border:0;border-right:1px solid #333;white-space:nowrap;font-weight:600}
.sitebar .sb-tabs a:hover{color:#fff;background:#1c1c1c}
.sitebar .sb-tabs a[aria-current="page"]{color:#111;background:#f4f4f2}
.sb-fade{position:fixed;top:0;right:0;width:46px;height:34px;z-index:101;pointer-events:none;
  background:linear-gradient(to right,rgba(17,17,17,0),#111 70%)}
/* The generated hubs carry their own copy of the bar, so the menu and the
   right-hand group have to be repeated here or they only work on the
   hand-written pages. Keep in step with the same rules in site.css. */
.sitebar .sb-tabs.sb-right{margin-left:auto}
.sitebar .sb-tabs.sb-right > :first-child{border-left:1px solid #333}
.sb-menu{position:relative;display:inline-flex;align-items:stretch;border-right:1px solid #333}
.sb-menubtn{display:inline-flex;align-items:center;gap:5px;height:100%;
  padding:0 14px;border:0;background:none;color:#b9bcbf;cursor:pointer;
  font:inherit;letter-spacing:inherit;white-space:nowrap;font-weight:600}
.sb-menubtn:hover{color:#fff;background:#1c1c1c}
.sb-menu.on .sb-menubtn{color:#fff;background:#1c1c1c}
.sb-caret{width:0;height:0;border-left:3.5px solid transparent;
  border-right:3.5px solid transparent;border-top:4px solid currentColor;
  transition:transform .12s ease}
.sb-menu.on .sb-caret{transform:rotate(180deg)}
.sitebar .sb-menupanel{position:fixed;z-index:60;margin-top:0;
  min-width:216px;max-height:min(70vh,420px);overflow-y:auto;
  background:#111;border:1px solid #333;border-top:0;border-radius:0;
  box-shadow:0 12px 26px rgba(0,0,0,.45);padding:0}
.sitebar .sb-menupanel a{display:block;height:34px;line-height:34px;
  padding:0 14px;border-radius:0;border:0;border-bottom:1px solid #262626;
  font-size:12px;font-weight:600;color:#fff;text-decoration:none;white-space:nowrap}
.sitebar .sb-menupanel a:last-child{border-bottom:0}
.sitebar .sb-menupanel a:hover{background:#1c1c1c;color:#fff}
.sitebar .sb-menupanel a[aria-current="page"]{background:#f4f4f2;color:#111;font-weight:700}
.topbar{top:34px;left:var(--badge)}
.hubbar{left:var(--badge)}
#side{top:max(calc(var(--top) + 34px),calc(var(--badge) + 14px))}
main{padding-top:calc(var(--top) + 34px + 22px)}
.sec{scroll-margin-top:calc(var(--top) + 34px + 8px)}
@media(max-width:640px){
  :root{--badge:52px}
  .topbar{left:0}
  .topbar .brand span{display:none}
  .topbar .brand{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
  .topbar #q{width:120px}
}
@media print{.sitebar{display:none}.topbar{top:0}main{padding-top:0}}
</style>
"""

# With this many tabs the bar always overflows, so the open one can sit off-screen
# when a page loads. Centre it on load, without smooth-scrolling (which would look
# like the page moving under the reader).
# The Projects menu. Keyboard and pointer both, closes on Escape, on a click
# outside, and on scrolling the bar — a panel left hanging over the page while
# the bar moves underneath it reads as a bug.
MENU_JS = ("(function(){var m=document.querySelector('.sb-menu');if(!m)return;"
           "var b=m.querySelector('.sb-menubtn'),p=m.querySelector('.sb-menupanel');"
           "if(!b||!p)return;"
           "function place(){var r=b.getBoundingClientRect();"
           "p.style.top=(r.bottom+2)+'px';"
           "var w=p.offsetWidth||220,l=Math.min(r.left,window.innerWidth-w-8);"
           "p.style.left=Math.max(8,l)+'px';}"
           "function open(){p.hidden=false;b.setAttribute('aria-expanded','true');"
           "m.classList.add('on');place();"
           "var a=p.querySelector('[aria-current=\\'page\\']');"
           "if(a&&a.scrollIntoView)a.scrollIntoView({block:'nearest'});}"
           "function shut(){p.hidden=true;b.setAttribute('aria-expanded','false');"
           "m.classList.remove('on');}"
           "b.addEventListener('click',function(e){e.stopPropagation();"
           "p.hidden?open():shut();});"
           "document.addEventListener('click',function(e){if(!m.contains(e.target))shut();});"
           "document.addEventListener('keydown',function(e){if(e.key==='Escape')shut();});"
           "var bar=document.querySelector('.sitebar');"
           "if(bar)bar.addEventListener('scroll',shut,{passive:true});"
           "window.addEventListener('resize',function(){if(!p.hidden)place();});"
           "p.addEventListener('click',function(e){if(e.target.tagName==='A')shut();});"
           "})();")

TAB_SCROLL = ("(function(){function c(){"
              "var b=document.querySelector('.sitebar');if(!b)return;"
              "var f=document.querySelector('.sb-fade');"
              "var over=b.scrollWidth>b.clientWidth+1;"
              "if(f)f.style.display=over?'':'none';"
              "var a=b.querySelector('[aria-current=\\'page\\']');"
              "if(!a||!over)return;"
              "var x=a.offsetLeft-(b.clientWidth-a.offsetWidth)/2;"
              "b.scrollLeft=Math.max(0,Math.min(x,b.scrollWidth-b.clientWidth));}"
              "c();if(document.readyState!=='complete'){window.addEventListener('load',c);}"
              "window.addEventListener('resize',c);})();")


# Every project used to get its own tab, which pushed the bar to twenty-two items
# and made the thing it was meant to help — finding a project — worse. They now
# live in one "Projects" menu, placed in the bar wherever PAGES puts the entry
# whose key is "projects".
PROJECTS_KEY = "projects"

def projects_menu(active=None):
    items, here = [], False
    for pr in CFG.PROJECTS:
        if not pr.get("tab"):
            continue
        cur = pr["slug"] == active
        here = here or cur
        items.append('<a role="menuitem" href="/projects/%s/"%s>%s</a>'
                     % (pr["slug"], ' aria-current="page"' if cur else '', pr["tab"]))
    if not items:
        return ''
    return ('<div class="sb-menu">'
            '<button type="button" class="sb-menubtn" aria-expanded="false" '
            'aria-haspopup="true"%s>Projects<span class="sb-caret" aria-hidden="true"></span></button>'
            '<div class="sb-menupanel" role="menu" hidden>%s</div></div>'
            % (' aria-current="page"' if here else '', "".join(items)))

# A hand-written count beside a hand-written grid goes stale the first time a
# card is added. Recount from the cards themselves on every build.
GRID_PAGES = {"abstracts/index.html": ("abs", "abstract"),
              "earlier/index.html":   ("ew",  "project"),
              "other/index.html":     ("ew",  "project")}

def sync_counts():
    for rel, (cls, noun) in GRID_PAGES.items():
        path = os.path.join(ROOT, rel)
        if not os.path.exists(path):
            continue
        raw = read_file(path, "grid page")
        if raw is None:          # unreadable source: leave the count alone
            continue
        html = raw.decode("utf-8")
        n = len(re.findall(r'<a class="%s"' % cls, html))
        if not n:
            continue
        word = noun if n == 1 else noun + "s"
        new = re.sub(r'(<p class="affil[^"]*">)\d+\s+\w+',
                     lambda m: "%s%d %s" % (m.group(1), n, word), html)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            note("%s - count set to %d %s" % (rel, n, word))

def nav_html(active=None):
    """Two groups: the reading tabs at the left, Projects and In Preparation
    pushed to the right edge. An entry opts into the right group with
    "right": True in PAGES; order within each group follows PAGES."""
    left, right = [], []
    for pg in CFG.PAGES:
        if pg["key"] == PROJECTS_KEY:
            markup = projects_menu(active)
        else:
            cur = ' aria-current="page"' if pg["key"] == active else ''
            markup = '<a href="%s"%s>%s</a>' % (pg["href"], cur, pg["tab"])
        (right if pg.get("right") else left).append(markup)
    if not any(pg["key"] == PROJECTS_KEY for pg in CFG.PAGES):
        right.append(projects_menu(active))     # never lose the projects entirely
    navs = '  <nav class="sb-tabs">' + "".join(left) + '</nav>\n'
    if right:
        navs += '  <nav class="sb-tabs sb-right">' + "".join(right) + '</nav>\n'
    return ('<a class="sb-badge" href="/" aria-label="Henry M. Blair — home">'
            '<img src="/assets/headshot-badge.png" alt="" width="320" height="320"></a>\n'
            '<div class="sitebar">\n'
            '  <a class="sb-brand" href="/">Henry M. Blair</a>\n'
            + navs +
            '</div>\n<span class="sb-fade" aria-hidden="true"></span>\n'
            '<script>' + TAB_SCROLL + '</script>\n'
            '<script>' + MENU_JS + '</script>')

def set_nav(path, active):
    if not os.path.exists(path):
        warn("missing page: %s" % os.path.relpath(path, ROOT)); return False
    html = open(path, encoding="utf-8").read()
    if "<!--SITENAV-->" not in html:
        warn("no SITENAV markers in %s" % os.path.relpath(path, ROOT)); return False
    new = re.sub(r"<!--SITENAV-->.*?<!--/SITENAV-->",
                 "<!--SITENAV-->\n" + nav_html(active) + "\n<!--/SITENAV-->", html, flags=re.S)
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
    return True

# ------------------------------------------------------------------ generated hubs

PAPER_LINK = '<a href="#paper" data-sec="paper">The paper</a>'
PAPER_CARD = ('<a class="navcard" href="#paper"><h3>Read the paper →</h3>'
              '<p>The full manuscript as a navigable page, every table and figure inline.</p></a>')

def paper_card(slug, gated):
    if gated:
        return ('<a class="navcard" href="/projects/%s/paper/"><h3>The manuscript →</h3>'
                '<p>Behind a passphrase while the work is unpublished. If I sent you one, it opens here.</p></a>'
                % slug)
    return ('<a class="navcard" href="mailto:henrymblair@gmail.com"><h3>The paper — on request →</h3>'
            '<p>The manuscript is not posted publicly. Email me and I will send it.</p></a>')

def strip_paper(html, slug, gated):
    start = html.find('<section id="paper" class="sec">')
    if start == -1:
        note("no paper section found, nothing stripped"); return html
    end = html.find('</section>', start)
    removed = (end + len('</section>')) - start
    html = html[:start] + html[end + len('</section>'):]
    html = html.replace(PAPER_LINK, '')
    if PAPER_CARD in html:
        html = html.replace(PAPER_CARD, paper_card(slug, gated))
    else:
        note("paper nav card not found; check the source markup")
    note("stripped manuscript section (%.1f MB)" % (removed / 1e6))
    return html

def wrap(html, slug):
    html = re.sub(r'<style id="site-nav-css">.*?</style>', '', html, flags=re.S)
    html = html.replace("</head>", HEAD_TAGS + SITEBAR_CSS + "</head>", 1)
    m = re.search(r"<body[^>]*>", html)
    i = m.end()
    return html[:i] + "\n" + nav_html(slug) + "\n" + html[i:]

def build_project_page(p):
    page = p.get("page")
    if not page:
        return True
    out = os.path.join(ROOT, "projects", p["slug"], "index.html")
    if page["kind"] == "auto":
        return build_auto_hub(p)
    if page["kind"] == "static":
        ok = set_nav(out, p["slug"])
        note("%s — hand-written page, tab bar refreshed" % p["slug"])
        return ok
    src = expand(page["source"])
    if not os.path.exists(src):
        warn("%s: source not found: %s" % (p["slug"], src))
        warn("   fix the path in projects.py and re-run; the card still renders meanwhile")
        return False
    raw = open(src, encoding="utf-8", errors="replace").read()
    html = strip_paper(raw, p["slug"], bool(p.get("paper"))) if page.get("strip_paper") else raw
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(wrap(html, p["slug"]))
    note("-> projects/%s/index.html  (%.1f MB)" % (p["slug"], os.path.getsize(out) / 1e6))
    return True

# ------------------------------------------------------------------ passphrase gate

SECRETS_TXT = os.path.join(ROOT, "_secrets", "passwords.txt")

def load_secrets():
    """Read _secrets/passwords.txt — one `id = passphrase` per line, # for comments.

    Falls back to the older passwords.json if the text file is not there. Ids are
    project slugs (for manuscripts) and file names (for gated downloads)."""
    out = {}
    if os.path.exists(SECRETS_TXT):
        try:
            lines = open(SECRETS_TXT, encoding="utf-8").readlines()
        except OSError as e:
            # Errno 35 here means the file is in iCloud and not on this disk. Say so
            # plainly instead of dying with a traceback about deadlocks.
            warn("cannot read _secrets/passwords.txt (%s)" % e)
            warn("   if it lives in iCloud, right-click the folder in Finder and choose")
            warn("   \"Keep Downloaded\", then re-run. Nothing gated was published.")
            return out
        for n, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                warn("passwords.txt line %d is not `id = passphrase`: %s" % (n, line[:40]))
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip()
            if k and v:
                out[k] = v
    elif os.path.exists(SECRETS):
        out = json.load(open(SECRETS))
    return out

def _aes(key: bytes, iv: bytes, data: bytes, decrypt=False):
    cmd = ["openssl", "enc", "-aes-256-cbc", "-K", key.hex(), "-iv", iv.hex()]
    if decrypt: cmd.insert(2, "-d")
    r = subprocess.run(cmd, input=data, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("openssl: " + r.stderr.decode()[:200])
    return r.stdout


def read_file(path, what):
    """Read a source file, saying something useful when it cannot be read.

    A file stored in iCloud but not downloaded locally raises EDEADLK here rather
    than a missing-file error, which is confusing the first time you meet it."""
    try:
        return open(path, "rb").read()
    except OSError as e:
        warn("could not read %s: %s" % (path, e))
        warn("   if it lives in iCloud, open it once in Finder to download it, then re-run")
        UNREADABLE.add(os.path.abspath(path))
        return None


def passphrases_for(item_id, secrets):
    """The keyslots for one protected item: its own passphrase, plus the master.

    MASTER_KEY_ID is not itself a protected item — it is a passphrase that opens
    everything. An item with only a master passphrase and none of its own is still
    protected; an item with neither is not published at all."""
    keys = []
    own = secrets.get(item_id)
    if own:
        keys.append((item_id, own))
    master = secrets.get(MASTER_KEY_ID)
    if master and master != own:
        keys.append((MASTER_KEY_ID, master))
    return keys


def encrypt(data: bytes, passwords):
    """Encrypt once, unlock with any of several passphrases.

    The file is encrypted under a random 64-byte content key (32 for AES, 32 for the
    HMAC). That content key is then wrapped separately under each passphrase — the
    same keyslot idea disk encryption uses. Adding a master passphrase therefore does
    not weaken the per-item ones and does not mean encrypting the file twice; each
    slot is an independent envelope around the same key.

    `passwords` is a list of (label, passphrase). Order is irrelevant — the page tries
    every slot and uses whichever one the entered passphrase opens."""
    b64 = lambda x: base64.b64encode(x).decode()
    ck = os.urandom(64)
    ck_enc, ck_mac = ck[:32], ck[32:]
    iv = os.urandom(16)
    ct = _aes(ck_enc, iv, data)
    mac = hmac.new(ck_mac, iv + ct, hashlib.sha256).digest()

    slots = []
    for label, pw in passwords:
        salt = os.urandom(16)
        dk = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt, PBKDF2_ITERATIONS, 64)
        kek, kmac = dk[:32], dk[32:]
        wiv = os.urandom(16)
        wct = _aes(kek, wiv, ck)
        slots.append({"label": label, "salt": b64(salt), "iv": b64(wiv), "ct": b64(wct),
                      "mac": b64(hmac.new(kmac, wiv + wct, hashlib.sha256).digest())})

    return {"v": 2, "kdf": "PBKDF2-SHA256", "it": PBKDF2_ITERATIONS, "cipher": "AES-256-CBC",
            "iv": b64(iv), "ct": b64(ct), "mac": b64(mac), "slots": slots}


GATE_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s — passphrase required</title>
<meta name="robots" content="noindex,nofollow">
<link rel="stylesheet" href="/assets/site.css">
%(head)s
<style>
.gatewrap{max-width:560px;margin:0 auto;padding:64px clamp(18px,5vw,40px) 80px}
.lock{background:var(--surf);border:1px solid var(--line);border-top:3px solid #111;padding:28px 30px}
.lock h1{font-family:var(--serif);font-size:27px;margin:0 0 6px;letter-spacing:-.01em}
.lock .sub{color:var(--mut);font-size:14px;margin:0 0 20px}
.lock label{display:block;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--mut);font-weight:700;margin-bottom:7px}
.lock input{width:100%%;padding:11px 13px;border:1px solid #bbb;background:#fafafa;font-size:15px;
  font-family:inherit;border-radius:2px}
.lock input:focus{outline:none;border-color:#111;background:#fff}
.lock button{margin-top:14px;background:#111;color:#fff;border:1px solid #111;padding:11px 20px;
  font-size:13.5px;font-weight:700;letter-spacing:.03em;cursor:pointer;font-family:inherit}
.lock button:hover{background:var(--accent);border-color:var(--accent)}
.lock button[disabled]{opacity:.55;cursor:default}
.msg{margin-top:14px;font-size:13.5px;min-height:20px}
.msg.err{color:#a2372c}
.meta{margin-top:22px;padding-top:16px;border-top:1px solid var(--line);font-size:12.5px;color:var(--mut)}
.reader{display:none;max-width:1100px;margin:0 auto;padding:22px clamp(14px,4vw,30px) 40px}
.reader.on{display:block}
.readerbar{display:flex;flex-wrap:wrap;gap:12px;align-items:baseline;justify-content:space-between;
  padding-bottom:12px;border-bottom:2px solid #111;margin-bottom:14px}
.readerbar h1{font-family:var(--serif);font-size:22px;margin:0}
.readerbar .r{font-size:13px;color:var(--mut)}
iframe{width:100%%;height:82vh;border:1px solid var(--line);background:#fff}
</style>
</head>
<body>

%(nav)s

<div class="gatewrap" id="gate">
  <div class="lock">
    <h1>%(title)s</h1>
    <p class="sub">%(subtitle)s</p>
    <form id="f">
      <label for="pw">Passphrase</label>
      <input id="pw" type="password" autocomplete="off" autocapitalize="off" spellcheck="false"
             placeholder="the passphrase I sent you">
      <button id="go" type="submit">Unlock</button>
    </form>
    <div class="msg" id="msg"></div>
    <div class="meta">The file on this page is encrypted (AES-256-CBC, PBKDF2-SHA256, %(iters)s iterations).
      It is decrypted in your browser and never leaves it. Without the passphrase there is nothing to read —
      not in the page source, not in the repository.<br><br>
      %(note)s<a href="%(back_url)s">← %(back_label)s</a></div>
  </div>
</div>

<div class="reader" id="reader">
  <div class="readerbar">
    <h1>%(title)s</h1>
    <div class="r"><span id="dlwrap"><a id="dl" download="%(filename)s">Download</a> · </span><a href="%(back_url)s">%(back_label)s</a></div>
  </div>
  <iframe id="frame" title="%(title)s" allowfullscreen></iframe>
</div>

<script id="payload" type="application/json">%(payload)s</script>
<script>
(function(){
  var blob = JSON.parse(document.getElementById('payload').textContent);
  var f = document.getElementById('f'), msg = document.getElementById('msg'), go = document.getElementById('go');
  var b64 = function(s){ return Uint8Array.from(atob(s), function(c){ return c.charCodeAt(0); }); };
  var cat = function(a,b){ var o=new Uint8Array(a.length+b.length); o.set(a); o.set(b,a.length); return o; };

  f.addEventListener('submit', function(e){
    e.preventDefault();
    var pw = document.getElementById('pw').value;
    if(!pw){ return; }
    if(!(window.crypto && crypto.subtle)){
      msg.className='msg err';
      msg.textContent='This browser will only decrypt over https. Open the page at https://henryblair.online.';
      return;
    }
    go.disabled = true; msg.className='msg'; msg.textContent='Checking…';
    setTimeout(function(){ unlock(pw); }, 20);
  });

  // Try each keyslot in turn. A slot opens only if its HMAC verifies, so a wrong
  // passphrase is rejected rather than producing garbage — and whichever slot the
  // passphrase belongs to (its own, or the master) yields the same content key.
  function openSlot(pw, i){
    if(i >= blob.slots.length){ return Promise.reject(new Error('no slot')); }
    var slot = blob.slots[i], enc = new TextEncoder();
    return crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveBits'])
      .then(function(base){
        return crypto.subtle.deriveBits(
          {name:'PBKDF2', salt:b64(slot.salt), iterations:blob.it, hash:'SHA-256'}, base, 512);
      })
      .then(function(bits){
        var kek = new Uint8Array(bits,0,32), kmac = new Uint8Array(bits,32,32);
        var wiv = b64(slot.iv), wct = b64(slot.ct);
        return crypto.subtle.importKey('raw', kmac, {name:'HMAC',hash:'SHA-256'}, false, ['verify'])
          .then(function(k){ return crypto.subtle.verify('HMAC', k, b64(slot.mac), cat(wiv,wct)); })
          .then(function(ok){
            if(!ok){ return openSlot(pw, i+1); }          // not this slot — try the next
            return crypto.subtle.importKey('raw', kek, {name:'AES-CBC'}, false, ['decrypt'])
              .then(function(k){ return crypto.subtle.decrypt({name:'AES-CBC', iv:wiv}, k, wct); })
              .then(function(ck){ return new Uint8Array(ck); });
          });
      });
  }

  function unlock(pw){
    openSlot(pw, 0)
      .then(function(ck){
        msg.textContent = 'Decrypting…';
        var ckEnc = ck.slice(0,32), ckMac = ck.slice(32,64);
        var iv = b64(blob.iv), ct = b64(blob.ct);
        return crypto.subtle.importKey('raw', ckMac, {name:'HMAC',hash:'SHA-256'}, false, ['verify'])
          .then(function(k){ return crypto.subtle.verify('HMAC', k, b64(blob.mac), cat(iv,ct)); })
          .then(function(ok){
            if(!ok){ throw new Error('content failed integrity check'); }
            return crypto.subtle.importKey('raw', ckEnc, {name:'AES-CBC'}, false, ['decrypt']);
          })
          .then(function(k){ return crypto.subtle.decrypt({name:'AES-CBC', iv:iv}, k, ct); });
      })
      .then(function(pt){
        // The plaintext is either a document or the address of one. A URL means the
        // address itself was the secret: nothing to download, just somewhere to look.
        var head = String.fromCharCode.apply(null, new Uint8Array(pt.slice(0, 9))).toLowerCase();
        if(head.indexOf('<!doctype') === 0 || head.indexOf('<html') === 0){
          var h = URL.createObjectURL(new Blob([pt], {type:'text/html'}));
          document.getElementById('frame').src = h;
          document.getElementById('dlwrap').style.display = 'none';
        } else if(head.indexOf('http') === 0){
          document.getElementById('frame').src = new TextDecoder().decode(pt).trim();
          document.getElementById('dlwrap').style.display = 'none';
        } else {
          var url = URL.createObjectURL(new Blob([pt], {type:'application/pdf'}));
          document.getElementById('frame').src = url;
          document.getElementById('dl').href = url;
        }
        document.getElementById('gate').style.display = 'none';
        document.getElementById('reader').className = 'reader on';
      })
      .catch(function(){
        go.disabled = false;
        msg.className = 'msg err';
        msg.textContent = 'That passphrase did not work.';
      });
  }
})();
</script>
</body>
</html>
"""

def write_gate(out, title, subtitle, blurb, back_url, back_label, filename, data, passwords, cache_key):
    """Encrypt `data` under `password` and write a passphrase page to `out`.
    Skips the work when neither the file nor the passphrase has changed."""
    keymat = "".join("%s:%s" % (l, pw) for l, pw in sorted(passwords))
    # The page template and the shared nav are part of what gets written, so a change
    # to either has to invalidate the cache — otherwise a gate keeps serving the old
    # chrome long after the rest of the site has moved on.
    template = (GATE_PAGE + nav_html(None) + HEAD_TAGS).encode()
    fingerprint = hashlib.sha256(data + keymat.encode() + str(PBKDF2_ITERATIONS).encode()
                                 + hashlib.sha256(template).digest()).hexdigest()
    cache = json.load(open(GATECACHE)) if os.path.exists(GATECACHE) else {}
    BUILT_GATES.add(os.path.abspath(out))
    if cache.get(cache_key) == fingerprint and os.path.exists(out):
        note("%s — gate unchanged (%d passphrase%s)" % (cache_key, len(passwords), "" if len(passwords)==1 else "s"))
        return True
    payload = encrypt(data, passwords)
    html = GATE_PAGE % {
        "title": title, "subtitle": subtitle, "note": blurb,
        "back_url": back_url, "back_label": back_label,
        "iters": "{:,}".format(PBKDF2_ITERATIONS),
        "filename": filename, "head": HEAD_TAGS, "nav": nav_html(None),
        "payload": json.dumps(payload),
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    cache[cache_key] = fingerprint
    os.makedirs(os.path.dirname(GATECACHE), exist_ok=True)
    json.dump(cache, open(GATECACHE, "w"), indent=1)
    note("-> %s  (%.1f MB encrypted, %d keyslot%s: %s)"
         % (os.path.relpath(out, ROOT), os.path.getsize(out) / 1e6, len(passwords),
            "" if len(passwords)==1 else "s", ", ".join(l for l, _ in passwords)))
    return True


def build_gate(p):
    paper = p.get("paper")
    if not paper:
        return True
    slug = p["slug"]
    src = expand(paper["pdf"])
    if not os.path.exists(src):
        warn("%s: manuscript not found: %s" % (slug, src))
        warn("   fix the path in projects.py and re-run")
        return False
    secrets = load_secrets()
    keys = passphrases_for(slug, secrets)
    if not keys:
        warn("%s: no passphrase in _secrets/passwords.txt — gate not built" % slug)
        return False

    data = read_file(src, "manuscript")
    if data is None:
        return False
    return write_gate(
        out=os.path.join(ROOT, "projects", slug, "paper", "index.html"),
        title=esc(p["title"]),
        subtitle="%s · %s" % (esc(paper.get("label", "Manuscript")), esc(paper.get("note", "Unpublished."))),
        blurb="",
        back_url="/projects/%s/" % slug, back_label="back to the project",
        filename=os.path.basename(src),
        data=data, passwords=keys, cache_key="project:" + slug)


# ------------------------------------------------------------------ gated downloads

def build_download_gates(published):
    """Files listed in DOWNLOAD_GATES are published only as passphrase pages.

    The raw file is never copied into downloads/, so there is no unprotected URL to
    find. A gated file with no passphrase is NOT published at all — failing closed is
    the only safe direction here."""
    gates = getattr(CFG, "DOWNLOAD_GATES", {})
    if not gates:
        return True
    secrets = load_secrets()
    ok = True
    sync_counts()
    for name, meta in gates.items():
        src = published.get(name)
        if not src:
            warn("DOWNLOAD_GATES lists %s but it is not in _downloadable/" % name); ok = False; continue
        keys = passphrases_for(name, secrets)
        if not keys:
            warn("no passphrase for %s in _secrets/passwords.txt — NOT published" % name); ok = False; continue
        data = read_file(src, "download")
        if data is None:
            ok = False; continue
        slug = slugify(GATED_ALIASES.get(name, os.path.splitext(name)[0]))
        ok &= write_gate(
            out=os.path.join(ROOT, "downloads", slug, "index.html"),
            title=esc(meta.get("title", name)),
            subtitle=esc(meta.get("subtitle", "")),
            blurb=esc(meta.get("note", "")),
            back_url=meta.get("back_url", "/"), back_label=meta.get("back_label", "back to the portfolio"),
            filename=name, data=data, passwords=keys, cache_key="download:" + name)
    return ok


def build_page_gates():
    """Pages that are private in full: the file published is ciphertext.

    Used for working notes that belong to me rather than to a reader. The page
    is written in _source/ (gitignored), encrypted at build time, and rendered
    in place once a passphrase opens it."""
    gates = getattr(CFG, "PAGE_GATES", {})
    if not gates:
        return True
    secrets = load_secrets()
    ok = True
    for key, meta in gates.items():
        keys = passphrases_for(key, secrets)
        if not keys:
            warn("no passphrase for %s in _secrets/passwords.txt — NOT published" % key)
            ok = False
            continue
        src = expand(meta["source"])
        data = read_file(src, "page")
        if data is None:
            ok = False
            continue
        ok &= write_gate(
            out=os.path.join(ROOT, meta["dir"], "index.html"),
            title=esc(meta.get("title", key)),
            subtitle=esc(meta.get("subtitle", "")),
            blurb=esc(meta.get("note", "")),
            back_url=meta.get("back_url", "/"),
            back_label=meta.get("back_label", "back to the portfolio"),
            filename="", data=data, passwords=keys, cache_key="page:" + key)
    return ok


def build_embed_gates():
    """Anything hosted elsewhere — a video, a slide deck — gated by its address.

    The file itself is too large to live in the repository, so what gets encrypted
    is the embed URL. Until someone enters a passphrase the address is not in the
    page source, and afterwards it plays in place. Worth being clear-eyed: this
    protects who *finds* the link, not who can watch it once they have it — the
    host's own sharing settings decide that."""
    gates = getattr(CFG, "EMBED_GATES", {})
    if not gates:
        return True
    secrets = load_secrets()
    ok = True
    for key, meta in gates.items():
        keys = passphrases_for(key, secrets)
        if not keys:
            warn("no passphrase for %s in _secrets/passwords.txt — NOT published" % key)
            ok = False
            continue
        ok &= write_gate(
            out=os.path.join(ROOT, "watch", key, "index.html"),
            title=esc(meta.get("title", key)),
            subtitle=esc(meta.get("subtitle", "")),
            blurb=esc(meta.get("note", "")),
            back_url=meta.get("back_url", "/"),
            back_label=meta.get("back_label", "back to the project"),
            filename="", data=meta["url"].encode("utf-8"),
            passwords=keys, cache_key="embed:" + key)
    return ok


# ------------------------------------------------------------------ downloads

BUILT_GATES = set()   # gate pages this build produced (anything else is retired)
ALIAS_URLS = {}       # alias file name -> the URL that actually serves it
GATED_ALIASES = {}    # gated source file -> stable alias stem to publish the gate under

# Sources this build could not read. A file evicted to iCloud raises EDEADLK, which
# is indistinguishable from "deleted" to anything that only asks whether it opened.
# That is not a distinction the pruners may guess at: deleting a published gate
# because its source was merely offline takes a document off the site and is not
# noticed until someone follows a dead link. While this set is non-empty the build
# refuses to delete anything.
UNREADABLE = set()

def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def build_downloads():
    """Copy _downloadable/ into downloads/, and give versioned files a stable public name.

    Drop a file in _downloadable/ and it is published. Files matching a pattern in
    DOWNLOAD_ALIASES are additionally published under a fixed URL, so a link already
    emailed or printed keeps working when a new version lands: the newest match wins.
    Files listed in DOWNLOAD_GATES are published only behind a passphrase."""
    src = os.path.join(ROOT, "_downloadable")
    out = os.path.join(ROOT, "downloads")
    if not os.path.isdir(src):
        warn("no _downloadable/ folder — nothing to publish as a download"); return True
    os.makedirs(out, exist_ok=True)
    gates = getattr(CFG, "DOWNLOAD_GATES", {})

    import fnmatch
    names = [n for n in sorted(os.listdir(src))
             if not n.startswith(".") and os.path.isfile(os.path.join(src, n))]

    # A versioned family (Henry_Blair_CV_*.pdf) shares one public URL, so it has to
    # share one access decision. If any member is gated, every member is: otherwise
    # moving the gate to a new version silently starts serving the old one in the
    # clear, right beside the passphrase page. This is how the August CV came back.
    blocked = set(gates)
    for pattern in getattr(CFG, "DOWNLOAD_ALIASES", {}):
        family = [n for n in names if fnmatch.fnmatch(n, pattern)]
        if any(n in gates for n in family):
            for n in family:
                if n not in gates:
                    note("%s — gated with the rest of %s" % (n, pattern))
            blocked |= set(family)

    published = {}
    for name in names:
        s_path = os.path.join(src, name)
        published[name] = s_path
        if name in blocked:
            continue                       # gated: never published in the clear
        d_path = os.path.join(out, name)
        if not os.path.exists(d_path) or os.path.getsize(d_path) != os.path.getsize(s_path):
            open(d_path, "wb").write(open(s_path, "rb").read())

    for pattern, alias in getattr(CFG, "DOWNLOAD_ALIASES", {}).items():
        matches = [n for n in published if fnmatch.fnmatch(n, pattern)]
        if not matches:
            warn("nothing in _downloadable/ matches %s (alias %s not published)" % (pattern, alias))
            continue
        newest = max(matches, key=lambda n: os.path.getmtime(published[n]))
        if len(matches) > 1:
            note("%s → %d matches, serving the newest: %s" % (pattern, len(matches), newest))
        if newest in blocked:
            # gated: the stable URL is the passphrase page, not a file
            ALIAS_URLS[alias] = "/downloads/%s/" % slugify(os.path.splitext(alias)[0])
            GATED_ALIASES[newest] = os.path.splitext(alias)[0]
            note("%s  →  %s  (passphrase required)" % (newest, ALIAS_URLS[alias]))
        else:
            open(os.path.join(out, alias), "wb").write(open(published[newest], "rb").read())
            ALIAS_URLS[alias] = "/downloads/%s" % alias
            note("%s  →  /downloads/%s" % (newest, alias))

    note("published %d file(s) to downloads/" % len([n for n in published if n not in blocked]))
    ok = build_download_gates(published)
    prune_downloads(published, blocked)
    fix_cv_link()
    return ok


def prune_downloads(published, gates):
    """Remove anything in downloads/ that this build did not just publish.

    This is the safety net that matters: when a file becomes gated, the copy
    published earlier in the clear must stop being served. Leaving it would put an
    unprotected URL right beside the passphrase page. Anything unexpected is
    removed (or, if it cannot be deleted, moved out of the site and reported)."""
    out = os.path.join(ROOT, "downloads")
    if UNREADABLE:
        warn("not pruning downloads/: %d source(s) could not be read this build"
             % len(UNREADABLE))
        return
    expected = {n for n in published if n not in gates}
    expected |= {os.path.basename(u.rstrip("/")) for u in ALIAS_URLS.values()}
    expected |= {slugify(GATED_ALIASES.get(n, os.path.splitext(n)[0])) for n in gates if n in published}
    for name in sorted(os.listdir(out)):
        if name.startswith(".") or name in expected:
            continue
        path = os.path.join(out, name)
        why = "now behind a passphrase" if name in gates else "no longer in _downloadable/"
        try:
            if os.path.isdir(path):
                import shutil; shutil.rmtree(path)
            else:
                os.remove(path)
            note("removed downloads/%s (%s)" % (name, why))
        except OSError:
            quarantine = os.path.join(ROOT, ".trash", "stale-downloads")
            os.makedirs(quarantine, exist_ok=True)
            os.rename(path, os.path.join(quarantine, name))
            warn("downloads/%s (%s) could not be deleted — moved to .trash/stale-downloads/" % (name, why))


def fix_cv_link():
    """Keep the resume page's Download button pointing at wherever the CV really is.

    Gating the CV moves it from /downloads/Henry-Blair-CV.pdf to a passphrase page,
    and ungating it moves it back. The button follows automatically rather than
    quietly 404-ing."""
    url = ALIAS_URLS.get("Henry-Blair-CV.pdf")
    if not url:
        return
    path = os.path.join(ROOT, "resume", "index.html")
    html = open(path, encoding="utf-8").read()
    new = re.sub(r'(<a class="btn" href=")[^"]*(")', lambda m: m.group(1) + url + m.group(2), html, count=1)
    if url.endswith("/"):
        new = new.replace('download="Henry-Blair-CV.pdf">Download PDF<', '>Download CV (passphrase)<')
    else:
        new = new.replace('>Download CV (passphrase)<', ' download="Henry-Blair-CV.pdf">Download PDF<')
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
        note("resume download button → %s" % url)


# ------------------------------------------------------------------ generated hubs (from config)

AUTO_HUB = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s — project</title>
<meta name="description" content="%(desc)s">
<link rel="stylesheet" href="/assets/site.css">
<link rel="stylesheet" href="/assets/project.css">
%(head)s
</head>
<body>

<!--SITENAV-->%(nav)s<!--/SITENAV-->

<header class="hubbar">
  <div class="ht">%(title)s <span>· %(kicker)s</span></div>
</header>

<nav class="hubside">
%(sidenav)s
  <div class="sidefoot">%(sidefoot)s</div>
</nav>

<main class="hub">
%(sections)s
  <div class="pgfoot">%(footnote)s</div>
</main>
</body>
</html>
"""

def material_url(url, label):
    """Point a materials link at the gate when its file is gated.

    Lets projects.py keep naming the file — /downloads/poster.pdf — while the build
    decides whether that resolves to the file or to its passphrase page, so gating
    something later never leaves a dead link behind."""
    gates = getattr(CFG, "DOWNLOAD_GATES", {})
    if url.startswith("/downloads/"):
        name = url[len("/downloads/"):]
        if name in gates:
            stem = GATED_ALIASES.get(name, os.path.splitext(name)[0])
            return "/downloads/%s/" % slugify(stem), label + " — passphrase"
    return url, label


def render_blocks(items, slug):
    """Render an ordered list of content blocks inside a hub section.

    Block kinds: h3, prose, bullets, callout, figure, table, stats. A section is
    just a list of these, so a hub can be as thorough as its material allows
    without needing its own hand-written page."""
    out = []
    for b in items:
        if "h3" in b:
            out.append('  <h3>%s</h3>' % b["h3"])
        if "prose" in b:
            for para in ([b["prose"]] if isinstance(b["prose"], str) else b["prose"]):
                out.append('  <p>%s</p>' % para)
        if "bullets" in b:
            out.append('  <ul class="pitfalls">' +
                       "".join('<li>%s</li>' % x for x in b["bullets"]) + '</ul>')
        if "callout" in b:
            out.append('  <div class="callout">%s</div>' % b["callout"])
        if "stats" in b:
            out.append('  <div class="statrow">' + "".join(
                '<div class="stat"><div class="statv">%s</div><div class="statl">%s</div>'
                '%s</div>' % (esc(v), esc(l), ('<div class="stats">%s</div>' % esc(sub)) if sub else "")
                for v, l, sub in [(x[0], x[1], x[2] if len(x) > 2 else "") for x in b["stats"]]) + '</div>')
        if "figure" in b:
            f = b["figure"]
            out.append('  <figure><img src="figures/%s" alt="%s">\n'
                       '  <figcaption>%s</figcaption></figure>'
                       % (f["src"], esc(f.get("alt", f.get("caption", "")))[:120], f.get("caption", "")))
        if "table" in b:
            t = b["table"]
            head = "".join('<th>%s</th>' % h for h in t["head"])
            rows = ""
            for r in t["rows"]:
                cls = ""
                if isinstance(r, dict):
                    cls, r = ' class="%s"' % r.get("cls", ""), r["cells"]
                cells = "".join('<td%s>%s</td>' % (' class="n"' if i else "", c)
                                for i, c in enumerate(r))
                rows += "<tr%s>%s</tr>" % (cls, cells)
            out.append('  <div class="tblwrap"><table><thead><tr>%s</tr></thead>'
                       '<tbody>%s</tbody></table></div>' % (head, rows))
            if t.get("note"):
                out.append('  <p class="tblnote">%s</p>' % t["note"])
    return "\n".join(out) + "\n"


def auto_sections(p):
    h = p.get("hub", {})
    out, nav = [], []

    def sec(sid, label, inner):
        nav.append('  <a href="#%s">%s</a>' % (sid, label))
        out.append('<section id="%s" class="sec">\n%s</section>' % (sid, inner))

    stats = "".join('<div class="stat"><div class="statv">%s</div><div class="statl">%s</div></div>'
                    % (esc(v), esc(l)) for v, l in p.get("stats", []))
    o  = '  <div class="masthead2">\n'
    o += '    <div class="tag">%s</div>\n' % esc(p["kicker"])
    o += '    <h1>%s</h1>\n' % esc(p["title"])
    if h.get("people"):
        o += '    <p class="authors">%s</p>\n' % esc(" · ".join(h["people"]))
    o += '    <p class="lede">%s</p>\n' % h.get("lede", esc(p["summary"]))
    o += '  </div>\n'
    if stats:
        o += '  <div class="statrow">%s</div>\n' % stats
    o += '  <div class="callout"><b>Status.</b> %s</div>\n' % h.get("status_detail", esc(p.get("status", "")))
    if h.get("in_progress"):
        o += ('  <div class="wip"><b>This hub is still being built.</b> '
              'The analysis is underway; the derivation, tables and figures will be posted here as they '
              'are finished, the way the completed projects on this site are. What is below is the design '
              'and the current state, written up as it stands.</div>\n')
    sec("overview", "Overview", o)

    for cs in h.get("sections", []):
        body = '  <h2>%s%s</h2>\n' % (esc(cs["title"]),
                                     (' <span class="snap">%s</span>' % esc(cs["tag"])) if cs.get("tag") else "")
        if cs.get("intro"):
            body += '  <p class="secintro">%s</p>\n' % cs["intro"]
        body += render_blocks(cs.get("blocks", []), p["slug"])
        sec(cs["id"], cs.get("nav", cs["title"]), body)

    if h.get("question"):
        sec("question", "The question", '  <h2>The question</h2>\n  <p>%s</p>\n' % h["question"])

    if h.get("approach"):
        body = '  <h2>How it is being done</h2>\n  <ul class="pitfalls">\n'
        body += "".join('    <li>%s</li>\n' % a for a in h["approach"]) + '  </ul>\n'
        sec("approach", "How it is done", body)

    if h.get("findings"):
        body = '  <h2>What it shows so far</h2>\n  <ul class="pitfalls">\n'
        body += "".join('    <li>%s</li>\n' % f for f in h["findings"]) + '  </ul>\n'
        if h.get("findings_note"):
            body += '  <div class="callout">%s</div>\n' % h["findings_note"]
        sec("findings", "What it shows", body)

    if h.get("videos"):
        body = '  <h2>The videos</h2>\n'
        for v in h["videos"]:
            if v.get("src"):
                body += ('  <figure><video controls preload="metadata" %s src="%s"></video>\n'
                         '  <figcaption><b>%s.</b> %s</figcaption></figure>\n'
                         % (('poster="%s"' % v["poster"]) if v.get("poster") else "",
                            v["src"], esc(v["title"]), v.get("caption", "")))
            else:
                body += ('  <div class="gate"><h3>%s</h3><p>%s</p></div>\n'
                         % (esc(v["title"]), v.get("caption", "Not yet posted.")))
        sec("videos", "The videos", body)

    if h.get("materials"):
        body = '  <h2>Materials</h2>\n  <div class="dls">'
        for m in h["materials"]:
            u, lab = material_url(m["url"], m["label"])
            body += '<a class="dl" href="%s">%s</a>' % (u, esc(lab))
        body += '</div>\n'
        sec("materials", "Materials", body)

    if p.get("paper"):
        body = ('  <h2>The manuscript</h2>\n'
                '  <div class="gate"><h3>%s</h3><p>%s Behind a passphrase while the work is unpublished — '
                '<a href="/projects/%s/paper/">open it here</a> if I sent you one, or '
                '<a href="mailto:henrymblair@gmail.com">email me</a>.</p></div>\n'
                % (esc(p["paper"].get("label", "Manuscript")), esc(p["paper"].get("note", "")), p["slug"]))
        sec("paper", "The manuscript", body)

    if h.get("next"):
        sec("next", "What comes next", '  <h2>What comes next</h2>\n  <p>%s</p>\n' % h["next"])

    if h.get("about"):
        sec("about", "About the study",
            '  <h2>About the study</h2>\n  <div class="keybox">%s</div>\n'
            % "".join('<p>%s</p>' % x for x in h["about"]))

    return "\n\n".join(out), "\n".join(nav)


def build_auto_hub(p):
    sections, sidenav = auto_sections(p)
    h = p.get("hub", {})
    html = AUTO_HUB % {
        "title": esc(p["title"]), "kicker": esc(p["kicker"]),
        "desc": esc(p["summary"][:180]), "head": HEAD_TAGS, "nav": nav_html(p["slug"]),
        "sidenav": sidenav, "sidefoot": h.get("sidefoot", "Henry M. Blair"),
        "sections": sections,
        "footnote": h.get("footnote", "This page grows as the work does."),
    }
    out = os.path.join(ROOT, "projects", p["slug"], "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    note("-> projects/%s/index.html  (generated hub)" % p["slug"])
    return True


# ------------------------------------------------------------------ landing page

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def card(p):
    linked = bool(p.get("page"))
    stats = "".join('<div class="stat"><div class="v">%s</div><div class="l">%s</div></div>'
                    % (esc(v), esc(l)) for v, l in p.get("stats", []))
    tags = "".join('<span class="tag">%s</span>' % esc(t) for t in p.get("tags", []))
    inner = (
        '  <div class="kicker">%s</div>\n'
        '  <h3>%s</h3>\n'
        '  <p>%s</p>\n' % (esc(p["kicker"]), esc(p["title"]), esc(p["summary"]))
    )
    if stats:
        inner += '  <div class="stats">%s</div>\n' % stats
    if tags:
        inner += '  <div class="tags">%s</div>\n' % tags
    inner += ('  <div class="open">Open the project hub &rarr;</div>\n' if linked
              else '  <div class="statusline">%s</div>\n' % esc(p["status"]))
    if linked:
        return '<a class="proj" href="/projects/%s/">\n%s</a>' % (p["slug"], inner)
    return '<div class="proj flat">\n%s</div>' % inner

def build_home():
    path = os.path.join(ROOT, "index.html")
    html = open(path, encoding="utf-8").read()
    if "<!--PROJECTS-->" not in html:
        warn("index.html has no <!--PROJECTS--> markers; cards not written"); return False

    current = [p for p in CFG.PROJECTS if p.get("group", "current") == "current"]
    earlier = [p for p in CFG.PROJECTS if p.get("group") == "earlier"]

    body = "\n\n".join(card(p) for p in current)
    if earlier:
        body += ('\n\n<h2 class="sect">Earlier work</h2>\n'
                 '<p class="sectnote">Where the method came from: imaging and bench work at Emory and '
                 'New York Medical College, beginning in high school through the STAR program.</p>\n\n'
                 + "\n\n".join(card(p) for p in earlier))
    new = re.sub(r"<!--PROJECTS-->.*?<!--/PROJECTS-->",
                 "<!--PROJECTS-->\n" + body + "\n<!--/PROJECTS-->", html, flags=re.S)
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
    note("-> index.html  (%d projects, %d earlier)" % (len(current), len(earlier)))
    return True


def earlier_card(e):
    thumb = ('<img class="pth" src="%s" alt="">' % e["thumb"]) if e.get("thumb") else ""
    links = "".join('<a class="dl" href="%s">%s</a>' % (l["url"], esc(l["label"]))
                    for l in e.get("links", []))
    meta = " · ".join(x for x in [esc(e.get("kicker", "")), esc(str(e.get("year", "")))] if x)
    return ('<div class="proj flat earlier">\n'
            '%s  <div class="kicker">%s</div>\n'
            '  <h3>%s</h3>\n'
            '  <p>%s</p>\n'
            '%s'
            '</div>' % (thumb, meta, esc(e["title"]), esc(e["summary"]),
                        ('  <div class="dls">%s</div>\n' % links) if links else ""))


# ------------------------------------------------------------------ main

def prune_gates():
    """Retire gate pages this build did not produce.

    Commenting out a passphrase does not publish the item — it stops being published
    at all. Without this, the previously built page would linger and keep opening
    with the old passphrase, which is the opposite of what removing a line means."""
    import shutil
    roots = [os.path.join(ROOT, "projects"), os.path.join(ROOT, "downloads"),
             os.path.join(ROOT, "watch"),
             os.path.join(ROOT, "in-preparation")]
    if UNREADABLE:
        warn("not retiring any gate: %d source(s) could not be read this build"
             % len(UNREADABLE))
        return
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if "index.html" not in filenames:
                continue
            try:
                head = open(os.path.join(dirpath, "index.html"),
                            encoding="utf-8", errors="replace").read(400000)
            except OSError as e:
                warn("could not read %s (%s) — leaving it alone"
                     % (os.path.relpath(dirpath, ROOT), e))
                UNREADABLE.add(os.path.abspath(os.path.join(dirpath, "index.html")))
                continue
            if '<script id="payload"' not in head:
                continue
            if os.path.abspath(os.path.join(dirpath, "index.html")) in BUILT_GATES:
                continue
            try:
                shutil.rmtree(dirpath)
                warn("retired %s — no passphrase for it any more" % os.path.relpath(dirpath, ROOT))
            except OSError:
                q = os.path.join(ROOT, ".trash", "retired-gates")
                os.makedirs(q, exist_ok=True)
                os.rename(dirpath, os.path.join(q, os.path.basename(dirpath) + "-" + str(int(os.path.getmtime(dirpath)))))
                warn("retired %s (moved to .trash/retired-gates/)" % os.path.relpath(dirpath, ROOT))


# -------------------------------------------------------------------- polish
# The published pages should read as finished work, not as the output of a
# toolchain. These run over every page the build writes, so a re-exported hub
# cannot quietly reintroduce a filename.

# Cloudflare Web Analytics. Paste the site token from the Cloudflare dashboard
# between the quotes and re-publish. Empty means no analytics script is emitted
# anywhere — nothing is loaded, nothing is tracked.
ANALYTICS_TOKEN = ""

BEACON = ('<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
          'data-cf-beacon=\'{"token": "%s"}\'></script>')
BEACON_RE = re.compile(r'\s*<script[^>]*cloudflareinsights[^>]*></script>')

def set_analytics(html):
    """One beacon per page, or none. Removing the token removes the script."""
    html = BEACON_RE.sub("", html)
    if ANALYTICS_TOKEN and "</body>" in html:
        html = html.replace("</body>", "\n" + (BEACON % ANALYTICS_TOKEN) + "\n</body>", 1)
    return html


SCRUB = [
    # "provenance" is jargon; the section is simply about the study
    ('<h2>About &amp; data provenance</h2>', '<h2>About the study</h2>'),
    ('<h2>About &amp; provenance</h2>', '<h2>About the study</h2>'),
    ('data-sec="about">About &amp; provenance</a>', 'data-sec="about">About the study</a>'),

    # ADT hub — source notes written for the author, not the reader
    ('<b>One snapshot, sourced from this folder.</b> Every number is read from\n'
     '   <em>Henry - PCa Data Master.xlsx</em> and every figure from <em>pca_figures/</em> '
     '(produced by <em>pca_figures.py</em>);\n   the page regenerates with <em>build_hub.py</em>. '
     'All counts are the Aug 19, 2026 extraction',
     '<b>One snapshot.</b> Every number and every figure on this page comes from a single '
     'extraction — the Aug 19, 2026 pull'),
    ('<h2>Figures <span class="snap">pca_figures.py</span></h2>', '<h2>Figures</h2>'),
    ('The manuscript figures, produced by <em>pca_figures.py</em> from the same workbook '
     'and referenced live — re-run it to update them here.',
     'The manuscript figures, drawn from the same workbook as every number above.'),
    ('<p><b>Self-sourcing.</b> This page is generated by <em>build_hub.py</em> from '
     '<em>Henry - PCa Data Master.xlsx</em> (numbers) and <em>pca_figures/</em> '
     '(figures, from <em>pca_figures.py</em>). Change the spreadsheet or re-run the figures, '
     're-run build_hub.py, and the page updates.</p>\n     ', ''),
    ('<footer class="pgfoot">Generated by build_hub.py from Henry - PCa Data Master.xlsx '
     'and pca_figures/ · snapshot Aug 19, 2026 · counts as-queried, never rescaled.</footer>',
     '<footer class="pgfoot">Snapshot Aug 19, 2026 · counts as queried, never rescaled.</footer>'),
]

MONTHS = {"jan": "January", "feb": "February", "mar": "March", "apr": "April",
          "may": "May", "jun": "June", "jul": "July", "aug": "August",
          "sep": "September", "sept": "September", "oct": "October",
          "nov": "November", "dec": "December"}

def _ordinal(n):
    n = int(n)
    if 11 <= n % 100 <= 13:
        return "%dth" % n
    return "%d%s" % (n, {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th"))

_MDY = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec)[a-z]*\.?\s+"
                  r"(\d{1,2})(?:st|nd|rd|th)?,?\s+(\d{4})\b")
_DMY = re.compile(r"\b(\d{1,2})(?:st|nd|rd|th)?\s+"
                  r"(January|February|March|April|May|June|July|August|September|October|"
                  r"November|December)\s+(\d{4})\b")
_SPLIT = re.compile(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", re.S)

def _dates_in_text(t):
    t = _MDY.sub(lambda m: "%s %s, %s" % (MONTHS[m.group(1).lower()],
                                          _ordinal(m.group(2)), m.group(3)), t)
    t = _DMY.sub(lambda m: "%s %s, %s" % (m.group(2), _ordinal(m.group(1)), m.group(3)), t)
    return t

def normalize_dates(html):
    """Write every date as Month Dayth, Year — and only in visible text, never
    inside a tag, a script or a stylesheet."""
    return "".join(part if (i % 2) else _dates_in_text(part)
                   for i, part in enumerate(_SPLIT.split(html)))

def polish_pages():
    changed = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", ".locktrash", ".trash", "_source", "_secrets",
                                    "_downloadable", "__pycache__", "_to_delete")]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            f = os.path.join(dirpath, name)
            try:
                html = open(f, encoding="utf-8", errors="replace").read()
            except OSError as e:
                warn("could not polish %s (%s)" % (os.path.relpath(f, ROOT), e))
                continue
            out = html
            for a, b in SCRUB:
                out = out.replace(a, b)
            out = normalize_dates(out)
            out = set_analytics(out)
            if out != html:
                open(f, "w", encoding="utf-8").write(out)
                changed += 1
    note("polished %d page(s) — dates normalised, toolchain names removed%s"
         % (changed, ", analytics beacon set" if ANALYTICS_TOKEN else ""))
    return True


# ------------------------------------------------------------------ cache-bust
VERSIONED = ["assets/site.css", "assets/project.css", "assets/headshot-badge.png",
              "assets/og-image.png"]

AN_A, AN_B = "<!--ANALYTICS-->", "<!--/ANALYTICS-->"

def analytics_tag():
    """The counter snippet, or "" when no site code is configured."""
    cfg = getattr(CFG, "ANALYTICS", None) or {}
    code = (cfg.get("goatcounter") or "").strip()
    if not code:
        return ""
    return ('%s<script data-goatcounter="https://%s.goatcounter.com/count" '
            'async src="//gc.zgo.at/count.js"></script>%s'
            % (AN_A, esc(code), AN_B))

def stamp_analytics():
    """Put the counter on every published page, or take it off every page.

    Written as a stamp over the built output rather than into each template,
    because the pages come from four different places -- hand-written files,
    generated project hubs, gate pages and the home page -- and a counter that
    is missing from a quarter of the site measures nothing useful. Clearing the
    site code removes it again on the next build, so switching it off is one
    edit and not a hunt."""
    cfg = getattr(CFG, "ANALYTICS", None) or {}
    skip = tuple(cfg.get("skip") or ())
    tag = analytics_tag()
    pat = re.compile(re.escape(AN_A) + r".*?" + re.escape(AN_B), re.S)
    on = off = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", ".trash", ".locktrash", "_source", "_secrets",
                                    "_downloadable", "__pycache__")]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            f = os.path.join(dirpath, name)
            rel = os.path.relpath(f, ROOT).replace(os.sep, "/")
            want = "" if (not tag or rel.startswith(skip)) else tag
            raw = read_file(f, "page")
            if raw is None:
                continue
            html = raw.decode("utf-8", "replace")
            new = pat.sub("", html)
            if want:
                if "</body>" not in new:
                    continue
                new = new.replace("</body>", want + "\n</body>", 1)
            if new != html:
                open(f, "w", encoding="utf-8").write(new)
                on += 1 if want else 0
                off += 0 if want else 1
    if tag:
        note("analytics: counter on %d page(s)%s"
             % (on, (" - %s skipped" % ", ".join(skip)) if skip else ""))
    elif off:
        note("analytics: counter removed from %d page(s)" % off)
    return True

def version_assets():
    """Stamp ?v=<content hash> onto the shared assets in every published page.

    GitHub Pages tells browsers to cache /assets/* for a while, so a visitor who
    saw the site before a CSS change keeps the old stylesheet against the new
    HTML — which is how a restyled element ends up rendering unstyled. A hash in
    the query string makes each new version a different URL, so the change lands
    immediately and unchanged assets stay cached."""
    import re
    stamps = {}
    for rel in VERSIONED:
        f = os.path.join(ROOT, rel)
        if os.path.exists(f):
            stamps[rel] = hashlib.sha256(open(f, "rb").read()).hexdigest()[:10]
    if not stamps:
        return True
    pat = re.compile(r'/(' + "|".join(re.escape(r) for r in stamps) + r')(\?v=[0-9a-f]+)?')
    touched = 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", ".trash", "_source", "_secrets", "_downloadable", "__pycache__")]
        for name in filenames:
            if not name.endswith(".html"):
                continue
            f = os.path.join(dirpath, name)
            try:
                html = open(f, encoding="utf-8", errors="replace").read()
            except OSError as e:
                warn("could not version %s (%s)" % (os.path.relpath(f, ROOT), e))
                continue
            new = pat.sub(lambda m: "/" + m.group(1) + "?v=" + stamps[m.group(1)], html)
            if new != html:
                open(f, "w", encoding="utf-8").write(new)
                touched += 1
    note("stamped %d page(s) with asset versions (%s)"
         % (touched, ", ".join(sorted(v for v in stamps.values()))))
    return True


# ------------------------------------------------- byte-exact static payloads
# Files that are served verbatim and whose bytes are part of a contract with
# something outside this site. install.sh is piped straight into zsh by anyone
# running the one-liner, so a stray edit here is executed on their machine: a
# CRLF, a BOM, or a well-meant "polish" pass would break it in confusing ways,
# or worse, run. The hash is checked after every build so a change is loud and
# deliberate rather than silent. Update the hash only when the script itself
# is meant to change.
VERBATIM = {
    "nsqip/install.sh":
        "9f2f12458e4955a8937b2f57104ed21e9730c50f89d40fa0460aab033bac25cd",
}

KIT_ZIP = "nsqip/NSQIP_ZIP.zip"

def check_kit_zip():
    """The kit is replaced from time to time, so its bytes are not pinned — but
    its shape is. install.sh refuses anything that does not unpack to
    NSQIP_ZIP/run_this_first.zsh, so a zip built one folder too deep would be
    downloaded by everyone and then rejected on their machine. Check it here
    instead, where it is cheap to notice."""
    import zipfile
    f = os.path.join(ROOT, KIT_ZIP)
    if not os.path.exists(f):
        warn("%s is missing — the one-liner will download nothing" % KIT_ZIP)
        return False
    try:
        z = zipfile.ZipFile(f)
        if z.testzip() is not None:
            warn("%s is a corrupt zip" % KIT_ZIP); return False
        names = z.namelist()
    except Exception as e:
        warn("%s is not a readable zip (%s)" % (KIT_ZIP, e)); return False
    if "NSQIP_ZIP/run_this_first.zsh" not in names:
        tops = sorted({n.split("/")[0] for n in names})
        warn("%s does not contain NSQIP_ZIP/run_this_first.zsh — install.sh will"
             " refuse it (top-level: %s)" % (KIT_ZIP, ", ".join(tops) or "none"))
        return False
    note("%s ok, %d entries, %.0f KB" % (KIT_ZIP, len(names), os.path.getsize(f) / 1024.0))
    return True


def check_verbatim():
    ok = True
    for rel, want in VERBATIM.items():
        f = os.path.join(ROOT, rel)
        if not os.path.exists(f):
            warn("%s is missing — the one-liner that pipes it into zsh will 404" % rel)
            ok = False; continue
        raw = open(f, "rb").read()
        got = hashlib.sha256(raw).hexdigest()
        if got != want:
            warn("%s changed: expected sha256 %s, found %s" % (rel, want[:12], got[:12]))
            warn("   if that was deliberate, update VERBATIM in this file")
            ok = False; continue
        if b"\r\n" in raw:
            warn("%s has CRLF line endings; it must be LF only" % rel); ok = False
        elif raw.startswith(b"\xef\xbb\xbf"):
            warn("%s starts with a byte-order mark; it must not" % rel); ok = False
        else:
            note("%s verbatim, sha256 %s" % (rel, got[:12]))
    return ok


# ------------------------------------------------- live numbers from the sheet
# The ADT figure's counts live in the PCa master workbook, not in this repo.
# The build reads them and bakes them into the page, so the page is correct
# before any JavaScript runs and stays correct if the workbook is unreachable
# or later locked down; a small script then refreshes them in the browser.
PCA_HUB = os.path.join(ROOT, "_source", "pca_project_hub_standalone.html")
PCA_CACHE = os.path.join(ROOT, "_source", "pca_qm_cache.json")

def build_pca_figure():
    try:
        import pca_figure as PF
    except ImportError:
        warn("pca_figure.py is missing — the ADT cohort figure cannot be built")
        return False
    if not os.path.exists(PCA_HUB):
        warn("%s is missing" % os.path.relpath(PCA_HUB, ROOT)); return False
    vals, network, hcos, source = PF.load(PCA_CACHE)
    if vals is None:
        warn("could not read the PCa workbook and no cache exists — "
             "leaving the ADT figure as it is")
        return False
    missing = sorted(k for k, v in vals.items() if v is None)
    if missing:
        warn("workbook is missing %d value(s): %s" % (len(missing), ", ".join(missing)))
        return False
    html = io.open(PCA_HUB, encoding="utf-8", errors="replace").read()
    a, b = html.find(PF.MARK_A), html.find(PF.MARK_B)
    if a < 0 or b < a:
        warn("PCAFIG markers not found in the hub source"); return False
    new = html[:a] + PF.block(vals, network, hcos, source=source) + html[b + len(PF.MARK_B):]
    if new != html:
        io.open(PCA_HUB, "w", encoding="utf-8").write(new)
    js = os.path.join(ROOT, "assets", "pca-live.js")
    io.open(js, "w", encoding="utf-8").write(PF.live_js())
    note("ADT cohort figure: %d counts %s (IADT %s, network %s)"
         % (len(vals), "from the workbook" if source == "sheet" else "from cache",
            format(vals["iadt"], ","), format(network, ",") if network else "?"))
    return True


if __name__ == "__main__":
    print("Building %s" % ROOT)
    ok = True
    ok &= build_pca_figure()
    for p in CFG.PROJECTS:
        if p.get("page") or p.get("paper"):
            print("  %s" % p["slug"])
        ok &= build_project_page(p)
        ok &= build_gate(p)
    for pg in CFG.PAGES:
        if pg.get("gate"):      # a gate page is written whole, bar included
            continue
        if pg.get("menu") or not pg.get("file"):   # a menu entry has no page of its own
            continue
        set_nav(os.path.join(ROOT, pg["file"]), pg["key"])
    ok &= build_downloads()
    ok &= build_embed_gates()
    ok &= build_page_gates()
    prune_gates()
    ok &= build_home()
    ok &= polish_pages()
    ok &= version_assets()
    ok &= stamp_analytics()
    if UNREADABLE:
        warn("%d source file(s) could not be read; nothing was deleted and the "
             "published site may be incomplete" % len(UNREADABLE))
        for f in sorted(UNREADABLE):
            warn("   %s" % os.path.relpath(f, ROOT))
        ok = False
    ok &= check_verbatim()
    ok &= check_kit_zip()
    print("Done." if ok else "Done, with problems (see above).")
    sys.exit(0 if ok else 1)
