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
TAB_SCROLL = ("(function(){function c(){var b=document.querySelector('.sitebar');"
              "if(!b)return;var a=b.querySelector('[aria-current=\\'page\\']');if(!a)return;"
              "var x=a.offsetLeft-(b.clientWidth-a.offsetWidth)/2;"
              "b.scrollLeft=Math.max(0,Math.min(x,b.scrollWidth-b.clientWidth));}"
              "c();if(document.readyState!=='complete'){window.addEventListener('load',c);}"
              "window.addEventListener('resize',c);})();")


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
    return ('<a class="sb-badge" href="/" aria-label="Henry M. Blair — home">'
            '<img src="/assets/headshot-badge.png" alt="" width="320" height="320"></a>\n'
            '<div class="sitebar">\n'
            '  <a class="sb-brand" href="/">Henry M. Blair</a>\n'
            '  <nav class="sb-tabs">' + "".join(tabs) + '</nav>\n'
            '</div>\n<span class="sb-fade" aria-hidden="true"></span>\n'
            '<script>' + TAB_SCROLL + '</script>')

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
        for n, line in enumerate(open(SECRETS_TXT, encoding="utf-8"), 1):
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
    <div class="r"><a id="dl" download="%(filename)s">Download</a> · <a href="%(back_url)s">%(back_label)s</a></div>
  </div>
  <iframe id="frame" title="%(title)s"></iframe>
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


# ------------------------------------------------------------------ downloads

BUILT_GATES = set()   # gate pages this build produced (anything else is retired)
ALIAS_URLS = {}       # alias file name -> the URL that actually serves it
GATED_ALIASES = {}    # gated source file -> stable alias stem to publish the gate under

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

    published = {}
    for name in sorted(os.listdir(src)):
        if name.startswith(".") or not os.path.isfile(os.path.join(src, name)):
            continue
        s_path = os.path.join(src, name)
        published[name] = s_path
        if name in gates:
            continue                       # gated: never published in the clear
        d_path = os.path.join(out, name)
        if not os.path.exists(d_path) or os.path.getsize(d_path) != os.path.getsize(s_path):
            open(d_path, "wb").write(open(s_path, "rb").read())

    import fnmatch
    for pattern, alias in getattr(CFG, "DOWNLOAD_ALIASES", {}).items():
        matches = [n for n in published if fnmatch.fnmatch(n, pattern)]
        if not matches:
            warn("nothing in _downloadable/ matches %s (alias %s not published)" % (pattern, alias))
            continue
        newest = max(matches, key=lambda n: os.path.getmtime(published[n]))
        if len(matches) > 1:
            note("%s → %d matches, serving the newest: %s" % (pattern, len(matches), newest))
        if newest in gates:
            # gated: the stable URL is the passphrase page, not a file
            ALIAS_URLS[alias] = "/downloads/%s/" % slugify(os.path.splitext(alias)[0])
            GATED_ALIASES[newest] = os.path.splitext(alias)[0]
            note("%s  →  %s  (passphrase required)" % (newest, ALIAS_URLS[alias]))
        else:
            open(os.path.join(out, alias), "wb").write(open(published[newest], "rb").read())
            ALIAS_URLS[alias] = "/downloads/%s" % alias
            note("%s  →  /downloads/%s" % (newest, alias))

    note("published %d file(s) to downloads/" % len([n for n in published if n not in gates]))
    ok = build_download_gates(published)
    prune_downloads(published, gates)
    fix_cv_link()
    return ok


def prune_downloads(published, gates):
    """Remove anything in downloads/ that this build did not just publish.

    This is the safety net that matters: when a file becomes gated, the copy
    published earlier in the clear must stop being served. Leaving it would put an
    unprotected URL right beside the passphrase page. Anything unexpected is
    removed (or, if it cannot be deleted, moved out of the site and reported)."""
    out = os.path.join(ROOT, "downloads")
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
        sec("about", "About & provenance",
            '  <h2>About &amp; provenance</h2>\n  <div class="keybox">%s</div>\n'
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

def prune_gates():
    """Retire gate pages this build did not produce.

    Commenting out a passphrase does not publish the item — it stops being published
    at all. Without this, the previously built page would linger and keep opening
    with the old passphrase, which is the opposite of what removing a line means."""
    import shutil
    roots = [os.path.join(ROOT, "projects"), os.path.join(ROOT, "downloads")]
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            if "index.html" not in filenames:
                continue
            is_gate = '<script id="payload"' in open(os.path.join(dirpath, "index.html"),
                                                     encoding="utf-8", errors="replace").read(400000)
            if not is_gate:
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


# ------------------------------------------------------------------ cache-bust
VERSIONED = ["assets/site.css", "assets/project.css", "assets/headshot-badge.png"]

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
    ok &= build_downloads()
    prune_gates()
    ok &= build_home()
    ok &= version_assets()
    print("Done." if ok else "Done, with problems (see above).")
    sys.exit(0 if ok else 1)
