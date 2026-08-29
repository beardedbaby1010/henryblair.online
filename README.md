# henryblair.online

Research portfolio for Henry M. Blair. A static site, generated from one config
file, hosted free on GitHub Pages at a custom domain.

This README is written to be followed literally. If you have forgotten
everything about how the site works, start at **[The 60-second version](#the-60-second-version)**,
then jump to the tab you want to change.

---

## Contents

- [The 60-second version](#the-60-second-version)
- [How the pieces fit](#how-the-pieces-fit)
- [File layout](#file-layout)
- [Publishing](#publishing)
- [Updating each tab](#updating-each-tab) ← the part you will use most
- [When a project folder outside this repo changes](#when-a-project-folder-outside-this-repo-changes)
- [Adding a brand-new project](#adding-a-brand-new-project)
- [Passphrase gates](#passphrase-gates)
- [Downloads](#downloads)
- [Figures](#figures)
- [The chrome every page shares](#the-chrome-every-page-shares)
- [Troubleshooting](#troubleshooting)
- [Rules that keep the site safe](#rules-that-keep-the-site-safe)

---

## The 60-second version

Almost every change is the same three steps:

```bash
cd ~/Documents/henryblair.online
# 1. edit projects.py  (or one of the four hand-written pages)
./publish "what I changed"
# 2. wait ~60 seconds
# 3. reload henryblair.online
```

That's it. `./publish` rebuilds every page, runs safety checks, commits and
pushes. GitHub redeploys on its own.

**The one rule:** never hand-edit a file inside `projects/` or `downloads/`
unless this README explicitly says that page is hand-written. Those are
generated, and your edit will be wiped out on the next build without warning.

---

## How the pieces fit

```
   projects.py            build_site.py               the website
 ┌──────────────┐        ┌──────────────┐        ┌──────────────────┐
 │ every project│  ───▶  │  reads it,   │  ───▶  │ index.html       │
 │ every tab    │        │  writes the  │        │ projects/…/      │
 │ every gate   │        │  whole site  │        │ downloads/…/     │
 └──────────────┘        └──────────────┘        └──────────────────┘
        ▲                        ▲
        │                        │
  you edit this        pulls manuscripts, PDFs and
                       hubs from folders OUTSIDE this
                       repo (Maimo_Work, _source, …)
```

Three ideas hold it together:

1. **`projects.py` is the single source of truth.** A project's copy, card
   numbers, tab label, page content and gated manuscript are all one entry
   there.
2. **Source material lives outside the repo.** Manuscripts stay in
   `~/Documents/Maimo_Work/…`; `projects.py` points at them. Nothing is copied
   in by hand.
3. **The repo is public, some content is not.** Manuscripts and the CV are
   encrypted at build time and only ever committed as ciphertext.

---

## File layout

```
projects.py                   THE CONFIG — every project, every tab, every gate
build_site.py                 the generator (rarely needs editing)
publish                       rebuild → safety checks → commit → push

index.html                    Research Portfolio tab   ← hand-written header,
                                                          project cards generated
about/index.html              About Me tab             ← hand-written
contact/index.html            Contact Me tab           ← hand-written
resume/index.html             Resume tab               ← hand-written

assets/site.css               styles for the four pages above
assets/project.css            styles for project hubs (sidebar, tables, figures)
assets/                       favicons, share image, contact icons, badge photo

projects/<slug>/index.html    a project page                    ← GENERATED
projects/<slug>/figures/      that project's images             ← you put them here
projects/<slug>/paper/        the passphrase gate               ← GENERATED
downloads/                    public downloads + download gates ← GENERATED

_source/                      standalone hubs, headshot original   ← GITIGNORED
_secrets/passwords.txt        all passphrases                      ← GITIGNORED
_downloadable/                the real PDFs (CV, posters)          ← GITIGNORED

CNAME  .nojekyll  404.html  favicon.ico  site.webmanifest
```

**GENERATED** = rewritten on every build. Don't edit by hand.
**GITIGNORED** = never leaves your Mac, never reaches GitHub.

---

## Publishing

```bash
cd ~/Documents/henryblair.online
./publish "what changed"        # rebuild → commit → push
./publish                       # message defaults to "Update site — <date>"
./publish --no-push "wip"       # build and commit only, don't push yet
```

Make it two words from anywhere:

```bash
echo "alias pub='~/Documents/henryblair.online/publish'" >> ~/.zshrc
```

### To preview before pushing

```bash
python3 build_site.py
python3 -m http.server 8000     # open http://localhost:8000
```

Use the server, **not** a `file://` preview — the passphrase gates need
WebCrypto, which only works over https or on localhost.

### What publish protects you from

Before committing, it refuses if manuscript markup (`class="manuscript"`) has
leaked into a public page, or if `_source/` has somehow become tracked by git.
It also clears stale `.git/*.lock` files first, so a killed git run can't wedge
the repo.

---

## Updating each tab

The site has 4 fixed tabs and 18 project tabs. Every one of them is covered
below. Tab **order** is the order of `PAGES` then `PROJECTS` in `projects.py`.

### About Me

Hand-written page. Edit the prose directly:

```bash
open -a TextEdit about/index.html      # or your editor of choice
```

Edit only the text between `<main>` and `</main>`. Leave the `<head>` and the
`<!--SITENAV-->` markers alone — the build rewrites the nav between them.
Then `./publish "About page"`.

### Contact Me

Hand-written page: `contact/index.html`.

Email addresses and the phone number are **deliberately not written as plain
text** anywhere in the HTML — they're assembled in JavaScript from split-up
`data-` attributes so scrapers don't harvest them:

```html
<a class="mail" data-u="henry.blair" data-d="downstate.edu"></a>
<a class="tel"  data-a="914" data-b="708" data-c="9909"></a>
```

To change an address, edit `data-u` (the part before the @) and `data-d` (the
domain). Never type a full address as visible text — that defeats the point.

The icon row at the bottom (LinkedIn, ORCID, Instagram, Outlook) uses images
from `assets/icons/`. To add another, copy a 96px+ PNG into that folder and
duplicate an existing `<a class="soc">` block.

Then `./publish "Contact page"`.

### Resume

Two separate things, and it matters which one you mean:

| What | Where | How |
|---|---|---|
| The résumé **shown on the site** | `resume/index.html` | edit the HTML, `./publish` |
| The résumé **people download** | `_downloadable/Henry_Blair_CV_*.pdf` | drop in a new file, `./publish` |

For the download: name the new file with a new date, e.g.
`Henry_Blair_CV_2026_Dec.pdf`, and drop it in `_downloadable/` **next to** the
old one. The build always serves the newest match and prints which one it
picked. The public link never changes, so a CV link you emailed months ago
starts serving the new file automatically.

The CV is passphrase-gated. If you rename it, update the matching line in
`_secrets/passwords.txt` and the key in `DOWNLOAD_GATES` in `projects.py` — the
id is the **file name**. If you forget, the build refuses to publish it and
tells you so.

### Research Portfolio (the landing page)

The header (name, tagline, affiliation, intro paragraph) is hand-written in
`index.html`. Everything below `PROJECTS` — every card, in both the current and
earlier groups — is generated from `projects.py`. Editing a card by hand does
nothing; the next build overwrites it.

| To change | Edit |
|---|---|
| Name, tagline, affiliation, intro | `index.html` |
| A card's title, blurb, numbers, tags | that project's entry in `projects.py` |
| Which group a card is in | `"group": "current"` or `"earlier"` |
| Card order | move the entry up or down in `PROJECTS` |

### The 18 project tabs

Every project tab is one entry in the `PROJECTS` list in `projects.py`. To find
the one you want, search the file for its tab label.

**These fields control the card and the tab:**

```python
"slug":   "oab-pvr",                 # the URL: /projects/oab-pvr/  (don't change casually)
"tab":    "PVR Self-Estimation",     # the tab label
"group":  "current",                 # "current" or "earlier" on the home page
"title":  "…",                       # headline on the card and the page
"kicker": "…",                       # the small grey line above the title
"status": "…",                       # e.g. "Submitted — Family Practice"
"summary": "…",                      # the paragraph on the card
"stats":  [("100", "women enrolled")],   # the big numbers on the card
"tags":   ["Telemedicine"],          # the little boxes
```

**These control the page itself:**

```python
"page":  {"kind": "auto"},           # where the page HTML comes from — see below
"paper": {"pdf": "Maimo_Work/…/manuscript.pdf",   # the gated manuscript
          "label": "Manuscript V7", "note": "…"},
"hub":   { … },                      # the page's sections and prose
```

#### The three kinds of page

| `page["kind"]` | The page comes from | How you edit it |
|---|---|---|
| `auto` (16 projects) | The `hub` block in `projects.py` | edit `projects.py` |
| `generated` (ADT Initiation) | A standalone HTML export in `_source/` | re-export upstream, copy into `_source/` |
| `static` (Vaginal Estrogen) | `projects/ve-boxed-warning/index.html`, hand-written | edit that file directly |

#### Editing an `auto` page

The `hub` block's keys become the page, in this fixed order. Note which keys
take a **string**, which take a **list of strings**, and which take **blocks**:

| Key | Type | Becomes |
|---|---|---|
| `people` | list of strings | the byline under the title |
| `lede` | string | the paragraph under the byline (defaults to `summary`) |
| `status_detail` | string | the "Status." callout (defaults to `status`) |
| `in_progress` | `True` | the amber "this hub is still being built" notice |
| `sections` | list of sections | your own named sections — see below |
| `question` | string | section "The question" |
| `approach` | list of strings | section "How it is done" (a bullet list) |
| `findings` | list of strings | section "What it shows" (a bullet list) |
| `findings_note` | string | a callout at the end of that section |
| `videos` | list | section "The videos" |
| `materials` | list of `{"label":…, "url":…}` | section "Materials" |
| `next` | string | section "What comes next" |
| `about` | list of strings | section "About & provenance" |
| `sidefoot` | string | the credit line in the left sidebar (`<br>` allowed) |

Everything above takes plain text. HTML like `<i>italics</i>` is allowed inside
a string.

#### Custom sections, for anything richer

Tables, figures and big numbers live in a **custom section**, which is the only
place block syntax applies:

```python
"sections": [
    {"id": "cohort",                       # becomes the #anchor
     "title": "How the cohort was built",  # the <h2>
     "nav": "Cohort",                      # the sidebar label (defaults to title)
     "intro": "One optional sentence.",
     "blocks": [
         {"h3": "Who was included"},
         {"prose": "A paragraph. <i>Italics</i> and links are fine."},
         {"bullets": ["first point", "second point"]},
         {"callout": "A boxed aside."},
         {"stats": [("69.3%", "never screened"),
                    ("3.6×", "risk ratio", "optional small print")]},
         {"figure": {"src": "fig1.jpg", "caption": "…", "alt": "…"}},
         {"table": {"head": ["Group", "n", "p"],
                    "rows": [["Quartile 1", "50", "0.04"]]}},
     ]},
],
```

`figure.src` is a bare filename; the file must exist in
`projects/<slug>/figures/`. In a table, the first cell of each row is left-
aligned and the rest are treated as numbers.

A project with nothing written yet still gets a tab and a page — set
`"in_progress": True` and it says so rather than 404ing.

#### The per-project cheat sheet

| Tab | Kind | Page content lives in | External source it pulls from |
|---|---|---|---|
| ADT Initiation | generated | `_source/pca_project_hub_standalone.html` | `Maimo_Work/PCa/` (`build_hub.py`), manuscript V7 |
| Vaginal Estrogen | static | `projects/ve-boxed-warning/index.html` | `Maimo_Work/VE/` manuscript V3 |
| PVR Self-Estimation | auto | `projects.py` | `Maimo_Work/old_OAB Proj/PVR/` manuscript V7 |
| Deprivation & Access | auto | `projects.py` | `_source/manuscripts/ADI-and-Travel-Time-V3.pdf` |
| Nocturia Goals | auto | `projects.py` | `Maimo_Work/Oliver Menken/` manuscript V3 |
| Retzius-Sparing RARP | auto | `projects.py` | — (no manuscript yet) |
| Focal Therapy | auto | `projects.py` | — |
| Ketamine Cystitis | auto | `projects.py` | — |
| Urogyn Survey | auto | `projects.py` | — |
| AUA Core Videos | auto | `projects.py` | — |
| MAUDE Device Safety | auto | `projects.py` | poster in `_downloadable/` (gated) |
| Med-Ed AI | auto | `projects.py` | — |
| Honors Thesis | auto | `projects.py` | thesis PDF in `_downloadable/` |
| EP2 & Status Epilepticus | auto | `projects.py` | published paper (DOI link) |
| Monocyte Engraftment | auto | `projects.py` | — |
| 5xFAD Inflammation | auto | `projects.py` | — |
| TBI & Stress | auto | `projects.py` | poster in `_downloadable/` |
| Estrogen & Dentate Gyrus | auto | `projects.py` | paper + poster in `_downloadable/` |

### Changing tab order or renaming a tab

Both live in `projects.py`. Rename by editing `"tab"`. Reorder by moving the
whole entry up or down in the `PROJECTS` list. Never rename a `"slug"` unless
you accept that the old URL breaks — anyone who bookmarked it gets a 404.

### Removing a tab

Delete (or comment out) its entry in `PROJECTS`, then run `./publish`. The tab
and its card disappear. The old page folder under `projects/` is left behind —
delete it manually and publish again if you want it gone from the site.

---

## When a project folder outside this repo changes

This is the case the site is built for: you did more work in
`~/Documents/Maimo_Work/<project>/`, and now the site should reflect it.
**You do not copy anything into this repo.** `projects.py` points at those
folders; you re-point it or just re-publish.

### Step 0 — always

```bash
cd ~/Documents/henryblair.online
```

### Case A — a new version of the manuscript

Say `Henry Edits V7 …pdf` became `Henry Edits V8 …pdf`.

1. Open `projects.py`, find the project, update the path:

   ```python
   "paper": {"pdf": "Maimo_Work/old_OAB Proj/PVR/Henry Edits V8 PVR Manuscript.pdf",
             "label": "Manuscript V8", "note": "Submitted to Family Practice."},
   ```

2. `./publish "PVR manuscript V8"`

The build re-encrypts it because the file changed. The passphrase is unchanged,
so anyone you already gave it to keeps access — they just get the new version.

**Paths are relative to `SOURCE_ROOTS`** at the top of `projects.py`
(`~/Documents`, then `~/mnt`). So write `Maimo_Work/PVR/file.pdf`, not the full
`/Users/henryblair/Documents/…` path. The first root that has the file wins,
which is why the same config works on the Mac and in a sandbox.

### Case B — you renamed or moved the project folder

This is the most common way to break the site, and it fails loudly:

```
!! oab-pvr: manuscript not found: …/Maimo_Work/OAB Proj/PVR/…
   fix the path in projects.py and re-run
```

Fix the path in `projects.py` and re-publish. Nothing else breaks — the card
still renders while the path is wrong, it just loses its manuscript link.

Note the fail-safe: while the file is missing, the **gate is retired** rather
than left serving a stale copy. The manuscript is never accidentally exposed.

### Case C — new results, new numbers, new figures

1. **Numbers on the card** → `"stats"` in `projects.py`.
2. **Prose, tables, findings** → the `hub` block for that project.
3. **Figures** → export them as `.jpg`/`.png`, copy into
   `projects/<slug>/figures/`, then add a `figure` block inside one of that
   project's custom `sections`:

   ```python
   {"figure": {"src": "fig4.jpg", "caption": "Travel time by ADI quartile."}}
   ```

   Figures are the one kind of file you do copy into the repo, because they get
   published. Keep them under ~500 KB each.
4. `./publish "PVR: updated results"`

### Case D — the ADT project (the `generated` one)

Its page is not written in `projects.py` — it's a full standalone HTML export
produced by `build_hub.py` in the PCa folder. After changing the data or the
hub upstream:

```bash
cd ~/Documents/Maimo_Work/PCa
python3 build_hub.py                     # re-export the standalone hub
cp <the standalone html> ~/Documents/henryblair.online/_source/pca_project_hub_standalone.html
cd ~/Documents/henryblair.online
./publish "ADT hub refresh"
```

The build strips the `<section id="paper">` manuscript block out of that export
before publishing it, so the public page carries the derivation, queries,
tables, figures, methods and references — but not the manuscript text.

If you want to change wording that appears in the ADT page, edit it in
`build_hub.py` upstream, not in `_source/` — otherwise the next export
overwrites you.

### Case E — a new poster, slide deck or PDF to hand out

1. Put the file in `_downloadable/`.
2. Reference it from the project's `materials` list as
   `/downloads/<filename>`.
3. If it should require a passphrase, add it to `DOWNLOAD_GATES` in
   `projects.py` **and** give it a passphrase in `_secrets/passwords.txt`.
4. `./publish`

### After any of the above

Check the build output. It names every file it read, every gate it built, and
every path it could not find. A build that says `Done.` with no `!!` lines did
exactly what you meant.

---

## Adding a brand-new project

Add one entry to `PROJECTS` in `projects.py`. That is the whole job — the tab,
the home-page card, the page and the gate all follow from it.

```python
{
    "slug": "my-project", "tab": "My Project", "group": "current",
    "title": "The question in one line",
    "kicker": "Retrospective cohort study · Maimonides Medical Center",
    "status": "Data collection underway",
    "summary": "The paragraph that appears on the home-page card.",
    "stats": [("120", "patients"), ("2", "sites")],
    "tags": ["Urology", "Access to care"],

    "page": {"kind": "auto"},
    "hub": {
        "people": ["Henry M. Blair", "Someone Else, MD"],
        "lede": "One or two sentences under the title.",
        "in_progress": True,               # remove once there is real content
        "question": "What are we actually asking, in one or two sentences?",
        "approach": ["how the cohort is built", "what is measured"],
        "sidefoot": "Henry M. Blair<br>Department of Urology, Maimonides",
    },
},
```

Then `./publish "Add my-project"`.

To gate a manuscript for it, add a `paper` block **and** a line in
`_secrets/passwords.txt` keyed by the slug. Without the passphrase the build
refuses to publish the manuscript at all — it never guesses.

---

## Passphrase gates

Unpublished manuscripts and the CV are AES-256-CBC encrypted at build time and
decrypted in the reader's browser. The published page contains **ciphertext
only** — there is nothing to read in the page source or in the repository.

The scheme uses **keyslots**, the same idea as disk encryption: one random key
encrypts the file, and that key is wrapped separately under each passphrase. So
every item opens with either its own passphrase or the **masterkey**, and adding
the master weakens nothing — a slot only opens if its HMAC verifies. Key
derivation is PBKDF2-SHA256 at 250,000 iterations, with an HMAC-SHA256 checked
before decryption, so a wrong passphrase fails cleanly instead of producing
garbage.

### The passwords file

`_secrets/passwords.txt`, one `id = passphrase` per line:

```
masterkey                    = …        # opens everything
adt-initiation               = …        # id = project slug → that manuscript
2024-maude-msre-poster.pdf   = …        # id = file name    → that download
```

Gitignored. Never committed. Losing it means picking new passphrases and
rebuilding — nothing worse.

### It fails closed

- A gated item with **no passphrase is not published at all.** The build says so
  and skips it.
- **Comment out a line** and the next build retires that gate and prunes any
  stale unprotected copy.
- The one combination that *opens something up* is removing a file from
  `DOWNLOAD_GATES` **as well** — then it becomes a free public download.

### Things worth knowing

- Encryption only re-runs when the file, its passphrases, or the gate template
  change, so committed ciphertext stays stable across publishes (cache:
  `_secrets/.gatecache.json`).
- **A decrypted copy cannot be recalled.** Rotating a passphrase stops future
  access, not a PDF someone already saved.
- Uses the `openssl` that ships with macOS plus the Python standard library.
  Nothing to install.

---

## Downloads

Anything people should be able to download goes in `_downloadable/`. Each build
copies it to `downloads/`, which is what the site serves. `_downloadable/` is
gitignored; the published copies are what get committed.

Versioned files get a permanent public URL through `DOWNLOAD_ALIASES`:

```python
DOWNLOAD_ALIASES = {"Henry_Blair_CV_*.pdf": "Henry-Blair-CV.pdf"}
```

The newest match wins, so a link already emailed or printed keeps working and
quietly starts serving the new file.

---

## Figures

Figures are the one kind of file you copy into the repo by hand:

```
projects/<slug>/figures/fig1.jpg
```

Reference them by bare filename in a `figure` block. They are published as-is,
so export them at a sensible size — a 4 MB figure makes the page slow on a
phone for no visible benefit.

---

## The chrome every page shares

Every page — hand-written, generated hub, gate page — gets three things from
`nav_html()` in `build_site.py`:

- the **headshot badge**, a fixed square top-left that links home;
- the **tab bar**, which scrolls sideways rather than squeezing tabs, and
  auto-centres whichever tab is open;
- a **version stamp** on the shared assets (`site.css?v=<hash>`, and likewise
  `project.css`, the badge photo and the share image).

That last one matters more than it looks. GitHub Pages tells browsers to cache
`/assets/*`, so without it a returning visitor keeps the old stylesheet against
the new HTML — which is exactly how a restyled element ends up rendering
unstyled. The hash changes only when the file does, so changes land immediately
and unchanged assets stay cached.

To change the badge photo, replace `assets/headshot-badge.png` (square, 512px)
and publish. To change the link-preview card, replace `assets/og-image.png`
(1200×630) — the version stamp forces Slack, LinkedIn and iMessage to re-fetch
it instead of showing the old one for days.

---

## Troubleshooting

**A change doesn't show up on the live site.**
Wait a full minute — GitHub Pages redeploys on its own schedule. Then hard-reload
(⌘⇧R). If it still doesn't show, run `git status`; an unpushed commit means the
push failed.

**The page looks unstyled, or an element renders wrong after a CSS change.**
Cached stylesheet. The version stamp normally prevents this; if you edited CSS
without running `build_site.py`, the stamp is stale. Just `./publish`.

**`fatal: Unable to create '.git/index.lock': File exists`**
A previous git run was killed. `./publish` clears these automatically now; if
you hit it running git by hand, `rm -f .git/index.lock`.

**`!! <slug>: manuscript not found`**
You moved or renamed the source folder. Fix the path in `projects.py`.

**`!! no passphrase for <thing> — NOT published`**
Add a line for it in `_secrets/passwords.txt`. This is the fail-closed behaviour
working correctly: it would rather publish nothing than publish it unprotected.

**A gate page says the passphrase is wrong when it isn't.**
You're previewing over `file://`. WebCrypto needs https or localhost — use
`python3 -m http.server 8000`.

**I edited a project page and my change vanished.**
It was a generated page. Find that project in `projects.py` and make the change
there instead.

---

## Rules that keep the site safe

1. **Everything committed here is public.** No PHI, no raw data, no patient
   identifiers — not in a figure, not in a table, not in a filename.
2. **Never commit `_source/`, `_secrets/` or `_downloadable/`.** They're
   gitignored; leave it that way. `publish` checks `_source/` on every run.
3. **Never hand-edit generated files.** Anything under `projects/` (except the
   two hand-written pages named above), all of `downloads/`, and every gate page.
4. **Never share the masterkey.** Give people the specific item's passphrase.
5. **Assume anything you've shared is permanent.** Rotating a passphrase stops
   future access, not a copy already downloaded.
