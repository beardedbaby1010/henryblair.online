# henryblair.online

Research portfolio for Henry M. Blair. Static site, hosted on GitHub Pages.

```
index.html                    Research Portfolio tab (the landing page)
about/index.html              About Me tab
contact/index.html            Contact Me tab
resume/index.html             Resume tab
resume/Henry-Blair-CV.pdf     the downloadable CV
assets/site.css               shared styles for all four pages above
projects/<slug>/index.html    one page per project  -- GENERATED, don't hand-edit
build_site.py                 the generator
_source/                      the standalone project HTML files  -- GITIGNORED
CNAME  .nojekyll  404.html
```

## The tab bar

Tab order and labels live in one place: `PAGES` (hand-written pages) and
`PROJECTS` (generated ones) at the top of `build_site.py`. Running the script
rewrites the bar into every page between the `<!--SITENAV-->` markers, so a
label change or a new tab is one edit plus one run -- never five files by hand.

The CV PDF is printed from `resume/index.html` (the print stylesheet in
`site.css` drops the tab bar, the download button and the footer). To
regenerate it after editing the resume page:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --no-pdf-header-footer \
  --print-to-pdf="resume/Henry-Blair-CV.pdf" \
  "https://henryblair.online/resume/"
```

## What is public and what is not

`build_site.py` produces the public page for each project by taking the
standalone hub and **removing the full-manuscript section** (`<section id="paper">`).
What stays public: the question, cohort derivation, every query builder, the
data tables, all figures, methods, limitations, references, provenance. What
goes: the manuscript text itself, replaced by an "on request" card that mails
henrymblair@gmail.com.

The manuscript source lives in `_source/`, which is gitignored, so it never
enters a commit and never reaches GitHub.

### Publishing the full version later

`PUBLISH_FULL = True` in `build_site.py` also writes the complete hub to
`projects/<slug>/full-<random>/`, marked `noindex` so search engines skip it —
a link-only page you can hand to a co-author or program director.

**Only turn that on once this repository is private.** Pages from a private
repo requires GitHub Pro (~$4/month). In a public repo anyone can read the
folder names and open the file directly, so the unguessable URL protects
nothing.

## Adding a project

1. Drop the standalone HTML into `_source/`.
2. Add an entry to `PROJECTS` in `build_site.py`:

   ```python
   {"slug": "my-project", "tab": "My Project", "source": "_source/hub.html"},
   ```

   Add `"strip_paper": True` if it has a `<section id="paper">` to hold back.
3. Copy the existing `<a class="proj">` card in `index.html` and edit it.
4. Publish:

   ```bash
   python3 build_site.py
   git add -A && git commit -m "Add my-project" && git push
   ```

## Updating a project

Re-export the standalone HTML over the file in `_source/`, then run the same
two commands. The build is idempotent — running it twice gives the same output.

## Notes

- Project pages are a few MB because fonts and figures are embedded in the
  standalone export. Fine for Pages (100 MB/file limit), just a slower first
  load on a phone.
- `.trash/` holds superseded files and is gitignored.
- Everything committed here is public. No PHI, no raw data.
