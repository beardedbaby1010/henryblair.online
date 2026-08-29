#!/usr/bin/env python3
"""
Build henryblair.online.

Each project is authored elsewhere as one self-contained HTML file (the PCa
project hub, for example). This script reads that file, adds the site tab bar,
and writes the result into projects/<slug>/. The source file is never modified.

Two variants are produced per project:

  PUBLIC  projects/<slug>/index.html
          The hub with the full-manuscript section removed. This is what the
          world sees. Safe to publish in a public repository.

  FULL    projects/<slug>/<full_path>/index.html
          The complete hub, manuscript included, at an unguessable URL and
          marked noindex so search engines never list it.

          Only built when PUBLISH_FULL = True below, and you should only set
          that to True once this repository is PRIVATE (GitHub Pro). In a
          public repo anyone can read the folder names here, so an unguessable
          URL protects nothing.

Sources live in _source/ , which is gitignored -- the manuscript never enters
a commit.

Add a project:  add to PROJECTS, add a card to index.html, run this, push.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

# Set True ONLY when this repository is private (requires GitHub Pro).
PUBLISH_FULL = False

CONTACT = "henrymblair@gmail.com"

PROJECTS = [
    {
        "slug":   "adt-initiation",
        "tab":    "ADT Initiation",
        "source": "_source/pca_project_hub_standalone.html",
        # remove the <section id="paper"> block from the public build
        "strip_paper": True,
        # where the complete version lives when PUBLISH_FULL is on
        "full_path": "full-2f4cdd679f40",
    },
    {
        "slug":   "ve-boxed-warning",
        "tab":    "Vaginal Estrogen",
        # hand-written page (projects/<slug>/index.html); the build only refreshes its tab bar
        "static": True,
    },
    # {"slug": "next-project", "tab": "Next Project", "source": "_source/hub.html"},
]

# Hand-written pages, in tab order. Each file must contain the
# <!--SITENAV--> ... <!--/SITENAV--> markers; the tab bar is written into them.
PAGES = [
    {"key": "about",   "tab": "About Me",           "href": "/about/",   "file": "about/index.html"},
    {"key": "contact", "tab": "Contact Me",         "href": "/contact/", "file": "contact/index.html"},
    {"key": "resume",  "tab": "Resume",             "href": "/resume/",  "file": "resume/index.html"},
    {"key": "home",    "tab": "Research Portfolio", "href": "/",         "file": "index.html"},
]

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
.sitebar .sb-private{margin-left:auto;display:flex;align-items:center;padding:0 14px;
  color:#e0b874;border-left:1px solid #333;letter-spacing:.09em;text-transform:uppercase;
  font-size:10.5px;font-weight:700;white-space:nowrap}
/* push the project's own chrome down by the height of the site bar */
.topbar{top:34px}
#side{top:calc(var(--top) + 34px)}
main{padding-top:calc(var(--top) + 34px + 22px)}
.sec{scroll-margin-top:calc(var(--top) + 34px + 8px)}
@media(max-width:640px){
  .topbar .brand span{display:none}
  .topbar .brand{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
  .topbar #q{width:120px}
  .sitebar .sb-private{display:none}
}
@media print{.sitebar{display:none}.topbar{top:0}main{padding-top:0}}
</style>
"""

PAPER_CARD = ('<a class="navcard" href="#paper"><h3>Read the paper →</h3>'
              '<p>The full manuscript as a navigable page, every table and figure inline.</p></a>')
PAPER_CARD_PUBLIC = ('<a class="navcard" href="mailto:%s?subject=Request%%20for%%20the%%20ADT%%20initiation%%20manuscript">'
                     '<h3>The paper — on request →</h3>'
                     '<p>The manuscript is not posted publicly while the work is under review. '
                     'Email me and I will send it.</p></a>') % CONTACT
PAPER_LINK = '<a href="#paper" data-sec="paper">The paper</a>'


def nav_html(active=None, private=False):
    """active is a PAGES key or a project slug."""
    tabs = []
    for pg in PAGES:
        cur = ' aria-current="page"' if pg["key"] == active else ''
        tabs.append('<a href="%s"%s>%s</a>' % (pg["href"], cur, pg["tab"]))
    for pr in PROJECTS:
        cur = ' aria-current="page"' if pr["slug"] == active else ''
        tabs.append('<a href="/projects/%s/"%s>%s</a>' % (pr["slug"], cur, pr["tab"]))
    badge = '<span class="sb-private">Private link · full manuscript</span>' if private else ''
    return ('<div class="sitebar">\n'
            '  <a class="sb-brand" href="/">Henry M. Blair</a>\n'
            '  <nav class="sb-tabs">' + "".join(tabs) + '</nav>\n'
            '  ' + badge + '\n'
            '</div>')


def strip_paper(html):
    """Remove the full-manuscript section, its sidebar link, and its nav card."""
    start = html.find('<section id="paper" class="sec">')
    if start == -1:
        print("     note: no paper section found, nothing stripped")
        return html
    end = html.find('</section>', start)
    removed = (end + len('</section>')) - start
    html = html[:start] + html[end + len('</section>'):]
    html = html.replace(PAPER_LINK, '')
    if PAPER_CARD in html:
        html = html.replace(PAPER_CARD, PAPER_CARD_PUBLIC)
    else:
        print("     note: paper nav card not found; check the source markup")
    print("     stripped manuscript section (%.1f MB)" % (removed / 1e6))
    return html


def wrap(html, slug, private):
    html = re.sub(r'<style id="site-nav-css">.*?</style>', '', html, flags=re.S)
    html = html.replace("</head>", SITEBAR_CSS + "</head>", 1)
    if private:
        html = html.replace('<meta charset="utf-8">',
                            '<meta charset="utf-8">\n<meta name="robots" content="noindex,nofollow">', 1)
    m = re.search(r"<body[^>]*>", html)
    i = m.end()
    return html[:i] + "\n" + nav_html(slug, private) + "\n" + html[i:]


def write(path, html):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8").write(html)
    print("     -> %s  (%.1f MB)" % (os.path.relpath(path, ROOT), os.path.getsize(path) / 1e6))


def build_project(p):
    if p.get("static"):
        path = os.path.join(ROOT, "projects", p["slug"], "index.html")
        if not os.path.exists(path):
            print("  !! %s is marked static but %s is missing" % (p["slug"], path)); return False
        html = open(path, encoding="utf-8").read()
        if "<!--SITENAV-->" not in html:
            print("  !! no SITENAV markers in %s" % path); return False
        new = re.sub(r"<!--SITENAV-->.*?<!--/SITENAV-->",
                     "<!--SITENAV-->\n" + nav_html(p["slug"]) + "\n<!--/SITENAV-->", html, flags=re.S)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
        print("  %s (hand-written) — tab bar refreshed" % p["slug"])
        return True
    src = os.path.normpath(os.path.join(ROOT, p["source"]))
    if not os.path.exists(src):
        print("  !! source not found: %s" % src)
        return False
    print("  %s" % p["slug"])
    raw = open(src, encoding="utf-8", errors="replace").read()

    pub = strip_paper(raw) if p.get("strip_paper") else raw
    write(os.path.join(ROOT, "projects", p["slug"], "index.html"), wrap(pub, p["slug"], False))

    full_dir = os.path.join(ROOT, "projects", p["slug"], p.get("full_path", "full"))
    if PUBLISH_FULL:
        write(os.path.join(full_dir, "index.html"), wrap(raw, p["slug"], True))
    elif os.path.exists(os.path.join(full_dir, "index.html")):
        print("     PUBLISH_FULL is off but %s exists -- delete that folder before pushing"
              % os.path.relpath(full_dir, ROOT))
    return True


def update_pages():
    """Write the current tab bar into every hand-written page."""
    for pg in PAGES:
        path = os.path.join(ROOT, pg["file"])
        if not os.path.exists(path):
            print("  !! missing page: %s" % pg["file"]); continue
        html = open(path, encoding="utf-8").read()
        if "<!--SITENAV-->" not in html:
            print("  !! no SITENAV markers in %s" % pg["file"]); continue
        new = re.sub(r"<!--SITENAV-->.*?<!--/SITENAV-->",
                     "<!--SITENAV-->\n" + nav_html(pg["key"]) + "\n<!--/SITENAV-->",
                     html, flags=re.S)
        if new != html:
            open(path, "w", encoding="utf-8").write(new)
            print("  tab bar -> %s" % pg["file"])


if __name__ == "__main__":
    print("Building site in %s" % ROOT)
    print("PUBLISH_FULL = %s" % PUBLISH_FULL)
    ok = all([build_project(p) for p in PROJECTS])
    update_pages()
    print("Done." if ok else "Done, with problems (see above).")
    sys.exit(0 if ok else 1)
