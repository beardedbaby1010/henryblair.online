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
import os, re, sys, json, base64, hashlib, hmac, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
import projects as CFG

SECRETS = os.path.join(ROOT, "_secrets", "passwords.json")
GATECACHE = os.path.join(ROOT, "_secrets", ".gatecache.json")
PBKDF2_ITERATIONS = 250_000

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
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/assets/favicon-16.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<meta property="og:site_name" content="Henry M. Blair">
<meta property="og:image" content="https://henryblair.online/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
"""

SITEBAR_CSS = """
<style id="site-nav-css">
:root{--sitebar:34px}
.sitebar{position:fixed;top:0;left:0;right:0;height:34px;z-index:100;
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
.topbar{top:34px}
#side{top:calc(var(--top) + 34px)}
main{padding-top:calc(var(--top) + 34px + 22px)}
.sec{scroll-margin-top:calc(var(--top) + 34px + 8px)}
@media(max-width:640px){
  .topbar .brand span{display:none}
  .topbar .brand{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
  .topbar #q{width:120px}
}
@media print{.sitebar{display:none}.topbar{top:0}main{padding-top:0}}
</style>
"""

def nav_html(active=None):
    tabs = []
    for pg in CFG.PAGES:
        cur = ' aria-current="page"' if pg["key"] == active else ''
        tabs.append('<a href="%s"%s>%s</a>' % (pg["href"], cur, pg["tab"]))
    for pr in CFG.PROJECTS:
        if not pr.get("tab"):
            continue
        cur = ' aria-current="page"' if pr["slug"] == active else ''
        tabs.append('<a href="/projects/%s/"%s>%s</a>' % (pr["slug"], cur, pr["tab"]))
    return ('<div class="sitebar">\n'
            '  <a class="sb-brand" href="/">Henry M. Blair</a>\n'
            '  <nav class="sb-tabs">' + "".join(tabs) + '</nav>\n'
            '</div>\n<span class="sb-fade" aria-hidden="true"></span>')

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

def load_secrets():
    if not os.path.exists(SECRETS):
        return {}
    return json.load(open(SECRETS))

def encrypt(data: bytes, password: str):
    """PBKDF2-SHA256 → 32-byte AES key + 32-byte MAC key. AES-256-CBC, then HMAC over iv|ct.
    Uses only the standard library plus the openssl binary that ships with macOS."""
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, PBKDF2_ITERATIONS, 64)
    ek, mk = dk[:32], dk[32:]
    iv = os.urandom(16)
    r = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-K", ek.hex(), "-iv", iv.hex()],
                       input=data, capture_output=True)
    if r.returncode != 0:
        raise RuntimeError("openssl: " + r.stderr.decode()[:200])
    ct = r.stdout
    mac = hmac.new(mk, iv + ct, hashlib.sha256).digest()
    b64 = lambda b: base64.b64encode(b).decode()
    return {"v": 1, "kdf": "PBKDF2-SHA256", "it": PBKDF2_ITERATIONS, "cipher": "AES-256-CBC",
            "salt": b64(salt), "iv": b64(iv), "mac": b64(mac), "ct": b64(ct)}

GATE_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s — manuscript</title>
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
    <p class="sub">%(label)s · %(note)s</p>
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
      <a href="/projects/%(slug)s/">← back to the project</a></div>
  </div>
</div>

<div class="reader" id="reader">
  <div class="readerbar">
    <h1>%(title)s</h1>
    <div class="r"><a id="dl" download="%(filename)s">Download PDF</a> · <a href="/projects/%(slug)s/">back to the project</a></div>
  </div>
  <iframe id="frame" title="%(title)s"></iframe>
</div>

<script id="payload" type="application/json">%(payload)s</script>
<script>
(function(){
  var blob = JSON.parse(document.getElementById('payload').textContent);
  var f = document.getElementById('f'), msg = document.getElementById('msg'), go = document.getElementById('go');
  var b64 = function(s){ return Uint8Array.from(atob(s), function(c){ return c.charCodeAt(0); }); };

  f.addEventListener('submit', function(e){
    e.preventDefault();
    var pw = document.getElementById('pw').value;
    if(!pw){ return; }
    if(!(window.crypto && crypto.subtle)){
      msg.className='msg err';
      msg.textContent='This browser will only decrypt over https. Open the page at https://henryblair.online.';
      return;
    }
    go.disabled = true; msg.className='msg'; msg.textContent='Deriving key…';
    setTimeout(function(){ unlock(pw); }, 20);
  });

  function unlock(pw){
    var enc = new TextEncoder();
    crypto.subtle.importKey('raw', enc.encode(pw), 'PBKDF2', false, ['deriveBits'])
      .then(function(base){
        return crypto.subtle.deriveBits(
          {name:'PBKDF2', salt:b64(blob.salt), iterations:blob.it, hash:'SHA-256'}, base, 512);
      })
      .then(function(bits){
        var ek = new Uint8Array(bits, 0, 32), mk = new Uint8Array(bits, 32, 32);
        var iv = b64(blob.iv), ct = b64(blob.ct), mac = b64(blob.mac);
        var signed = new Uint8Array(iv.length + ct.length);
        signed.set(iv); signed.set(ct, iv.length);
        return crypto.subtle.importKey('raw', mk, {name:'HMAC', hash:'SHA-256'}, false, ['verify'])
          .then(function(mkey){ return crypto.subtle.verify('HMAC', mkey, mac, signed); })
          .then(function(ok){
            if(!ok){ throw new Error('bad passphrase'); }
            return crypto.subtle.importKey('raw', ek, {name:'AES-CBC'}, false, ['decrypt']);
          })
          .then(function(key){ return crypto.subtle.decrypt({name:'AES-CBC', iv:iv}, key, ct); });
      })
      .then(function(pt){
        var url = URL.createObjectURL(new Blob([pt], {type:'application/pdf'}));
        document.getElementById('frame').src = url;
        document.getElementById('dl').href = url;
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
    pw = secrets.get(slug)
    if not pw:
        warn("%s: no passphrase in _secrets/passwords.json — gate not built" % slug)
        return False

    data = open(src, "rb").read()
    fingerprint = hashlib.sha256(data + pw.encode() + str(PBKDF2_ITERATIONS).encode()).hexdigest()
    cache = json.load(open(GATECACHE)) if os.path.exists(GATECACHE) else {}
    out = os.path.join(ROOT, "projects", slug, "paper", "index.html")

    if cache.get(slug) == fingerprint and os.path.exists(out):
        note("%s — gate unchanged" % slug)
        return True

    payload = encrypt(data, pw)
    html = GATE_PAGE % {
        "title": p["title"], "slug": slug, "head": HEAD_TAGS,
        "label": paper.get("label", "Manuscript"),
        "note": paper.get("note", "Unpublished."),
        "iters": "{:,}".format(PBKDF2_ITERATIONS),
        "filename": os.path.basename(src),
        "nav": nav_html(slug),
        "payload": json.dumps(payload),
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    cache[slug] = fingerprint
    os.makedirs(os.path.dirname(GATECACHE), exist_ok=True)
    json.dump(cache, open(GATECACHE, "w"), indent=1)
    note("-> projects/%s/paper/index.html  (%.1f MB encrypted)" % (slug, os.path.getsize(out) / 1e6))
    return True

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

def _p(text):
    return '<p>%s</p>' % text

def auto_sections(p):
    h = p.get("hub", {})
    out, nav = [], []

    def sec(sid, label, inner):
        nav.append('  <a href="#%s">%s</a>' % (sid, label))
        out.append('<section id="%s" class="sec">\n%s</section>' % (sid, inner))

    # overview
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
    o += ('  <div class="callout"><b>Status.</b> %s</div>\n'
          % h.get("status_detail", esc(p.get("status", ""))))
    if h.get("in_progress"):
        o += ('  <div class="wip"><b>This hub is still being built.</b> '
              'The analysis is underway; the derivation, tables and figures will be posted here as '
              'they are finished, the way the completed projects on this site are. What is below is '
              'the design and the current state, written up as it stands.</div>\n')
    sec("overview", "Overview", o)

    if h.get("question"):
        sec("question", "The question", '  <h2>The question</h2>\n  %s\n' % _p(h["question"]))

    if h.get("approach"):
        body = '  <h2>How it is being done</h2>\n  <ul class="pitfalls">\n'
        body += "".join('    <li>%s</li>\n' % a for a in h["approach"])
        body += '  </ul>\n'
        sec("approach", "How it is done", body)

    if h.get("findings"):
        body = '  <h2>What it shows so far</h2>\n  <ul class="pitfalls">\n'
        body += "".join('    <li>%s</li>\n' % f for f in h["findings"])
        body += '  </ul>\n'
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
        body += "".join('<a class="dl" href="%s">%s</a>' % (m["url"], esc(m["label"])) for m in h["materials"])
        body += '</div>\n'
        sec("materials", "Materials", body)

    if p.get("paper"):
        body = ('  <h2>The manuscript</h2>\n'
                '  <div class="gate"><h3>%s</h3><p>%s Behind a passphrase while the work is '
                'unpublished — <a href="/projects/%s/paper/">open it here</a> if I sent you one, or '
                '<a href="mailto:henrymblair@gmail.com">email me</a>.</p></div>\n'
                % (esc(p["paper"].get("label", "Manuscript")),
                   esc(p["paper"].get("note", "")), p["slug"]))
        sec("paper", "The manuscript", body)

    if h.get("next"):
        sec("next", "What comes next", '  <h2>What comes next</h2>\n  %s\n' % _p(h["next"]))

    if h.get("about"):
        sec("about", "About & provenance",
            '  <h2>About &amp; provenance</h2>\n  <div class="keybox">%s</div>\n'
            % "".join(_p(x) for x in h["about"]))

    return "\n\n".join(out), "\n".join(nav)

def build_auto_hub(p):
    sections, sidenav = auto_sections(p)
    h = p.get("hub", {})
    html = AUTO_HUB % {
        "title": esc(p["title"]), "kicker": esc(p["kicker"]),
        "desc": esc(p["summary"][:180]), "head": HEAD_TAGS, "nav": nav_html(p["slug"]),
        "sidenav": sidenav,
        "sidefoot": h.get("sidefoot", "Henry M. Blair"),
        "sections": sections,
        "footnote": h.get("footnote", "This page is generated from projects.py — it grows as the work does."),
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

if __name__ == "__main__":
    print("Building %s" % ROOT)
    ok = True
    for p in CFG.PROJECTS:
        if p.get("page") or p.get("paper"):
            print("  %s" % p["slug"])
        ok &= build_project_page(p)
        ok &= build_gate(p)
    for pg in CFG.PAGES:
        set_nav(os.path.join(ROOT, pg["file"]), pg["key"])
    ok &= build_home()
    print("Done." if ok else "Done, with problems (see above).")
    sys.exit(0 if ok else 1)
