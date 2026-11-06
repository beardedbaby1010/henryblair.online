# Handoff: building beardedbaby1010.com

A guide to standing up a second site with the same interface as henryblair.online,
but **behind a password at the front door** — nothing readable until someone
authenticates, at any URL on the domain.

You have built one static site before. This one differs in exactly one important
way, and that difference changes the hosting. Read Part 1 before doing anything
else; it is the part that will save you from building the wrong thing.

---

## Contents

- [Part 1 — The one hard problem, and the honest answer](#part-1--the-one-hard-problem-and-the-honest-answer)
- [Part 2 — Choose an architecture](#part-2--choose-an-architecture)
- [Part 3 — Set it up, step by step](#part-3--set-it-up-step-by-step)
- [Part 4 — What to copy from henryblair.online](#part-4--what-to-copy-from-henryblaironline)
- [Part 5 — Making it your own](#part-5--making-it-your-own)
- [Part 6 — Publishing](#part-6--publishing)
- [Part 7 — Things that will bite you](#part-7--things-that-will-bite-you)
- [Part 8 — Checklist](#part-8--checklist)

---

## Part 1 — The one hard problem, and the honest answer

### GitHub Pages cannot password-protect anything

This is the single most important fact in this document, and it is not obvious.

GitHub Pages is a **dumb file server**. It hands any file to anyone who asks for
it. There is no login, no session, no "who are you" step — those need a server
that runs code on each request, and Pages does not run code.

Three things follow, and each one catches people out:

**A private repository does not make a private site.** These are separate
settings. A private repo hides your *source* from other GitHub users. The
*published site* stays wide open to the entire internet. (On the free plan a
public repo is required for Pages at all; even on paid plans, making the repo
private does not gate the site.)

**A JavaScript password prompt is theatre.** You can write a page that asks for a
password and reveals content when it matches. This stops nobody. The content is
already in the file that was sent to the browser — "View Source" shows it, and
`curl` shows it without ever running your JavaScript. If a page can display it
after a password, it already had it before the password.

**An unguessable URL is not protection either.** `/secret-a83bf/` is one leaked
link, one browser-history export, or one shared screenshot away from public.
Search engines find these more often than people expect.

### What actually works — and what henryblair.online already does

There are only two real mechanisms:

**1. Encrypt the content.** The file on the server is ciphertext. Without the
passphrase there is nothing to read, even for someone who downloads the raw file.
This is what the manuscript gates on henryblair.online do, and it is genuinely
secure — but it protects *files one at a time*, and the page structure, URLs and
file names all stay public. Wrong tool for "gate the whole site".

**2. Put a real server in front.** Something that checks who you are on every
request and refuses to serve the file otherwise. This is what you want here, and
it means **not using GitHub Pages as the host.**

You keep GitHub as the place your code lives. You just stop using GitHub as the
web server.

---

## Part 2 — Choose an architecture

| Option | Real protection? | Cost | Private repo OK? | Effort |
|---|---|---|---|---|
| **Cloudflare Pages + Cloudflare Access** ⭐ | Yes — auth at the edge, whole domain | Free tier | **Yes** | Moderate, one-time |
| Cloudflare Pages + a Worker doing Basic Auth | Yes — one shared password | Free tier | **Yes** | Moderate, one-time |
| GitHub Pages + encrypt every page | Partial — URLs and structure stay public | Free | No (public repo) | High, ongoing friction |
| Netlify password protection | Yes | Paid feature | Yes | Low |
| GitHub Pages + JS password | **No. Do not do this.** | Free | No | Low |

### Recommendation: Cloudflare Pages + Cloudflare Access

Why this one:

- **It is the same workflow you already have.** Cloudflare Pages deploys from a
  GitHub repo on every push. You keep `git push` (or `./publish`) as the ritual.
- **It supports private repositories** — so the source is hidden *and* the site is
  gated. GitHub Pages cannot give you both without paying.
- **Access sits in front of the whole domain,** including every path and every
  file. There is no "I forgot to protect that page" failure mode.
- **The free Zero Trust tier covers a small number of users.** (It has
  historically been 50 seats; confirm the current limit when you sign up — these
  numbers move.) For a personal site with a handful of people, free.

Login is by **one-time PIN**: a visitor enters their email, Cloudflare emails
them a code, they enter it, and they get a session cookie for however long you
set. You control the allow-list — specific email addresses, or a whole domain
like `@downstate.edu`.

### If you want a literal shared password instead

Access does email codes, not a single shared password. If you would rather hand
one password to everybody, use **Cloudflare Pages + a Worker doing HTTP Basic
Auth** instead. It is about fifteen lines of JavaScript running in front of the
site, and the browser shows the classic username/password box.

Trade-offs, honestly: a shared password cannot be revoked for one person without
changing it for everyone, you get no record of who visited, and the browser
caches the credentials aggressively. Access is better in every way except the
mental model. But if "one password, tell it to whoever" is the actual
requirement, Basic Auth is the honest fit and there is no shame in it.

---

## Part 3 — Set it up, step by step

Do these in order. Steps 1–3 give you a working public site; step 4 is what locks
it. **Do not put real content in until step 4 is done and tested.**

### Step 1 — The repository

1. Create a new repo on GitHub: `beardedbaby1010.com`.
2. Make it **private**. (With Cloudflare Pages this costs nothing and hides
   your source. This is the option GitHub Pages could not give you.)
3. Clone it to `~/Documents/beardedbaby1010.com/`.

**Do not enable GitHub Pages on this repo.** If you do, you will have a
completely unprotected copy of the site living at
`beardedbaby1010.github.io` while you think it is gated. Leave Pages off.

### Step 2 — Move DNS to Cloudflare

Cloudflare can only guard traffic that goes through Cloudflare, so the domain's
nameservers have to point there. You keep owning the domain at GoDaddy; you are
only changing who answers DNS queries.

1. Sign up at cloudflare.com (free).
2. **Add a site** → `beardedbaby1010.com`. Choose the Free plan.
3. Cloudflare scans your existing DNS records and shows you two nameservers,
   something like `xxx.ns.cloudflare.com`.
4. In **GoDaddy** → your domain → **Nameservers** → **Change** → **I'll use my own
   nameservers** → paste both Cloudflare nameservers → save.
5. Wait. Propagation is usually minutes but can take a few hours. Cloudflare
   emails you when the domain is active.

This is different from what you did for henryblair.online, where you left DNS at
GoDaddy and just pointed A records at GitHub. Here Cloudflare has to be in the
request path.

### Step 3 — Cloudflare Pages

1. Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** →
   **Connect to Git**.
2. Authorize GitHub, pick the `beardedbaby1010.com` repo.
3. Build settings, for a plain static site:
   - **Framework preset:** None
   - **Build command:** *leave blank*
   - **Build output directory:** `/`
   (You generate the HTML on your Mac and commit it, exactly like henryblair.online.
   Cloudflare just serves what is in the repo.)
4. **Save and Deploy.** You get a URL like `beardedbaby1010.pages.dev`.
5. **Custom domains** → add `beardedbaby1010.com` and `www.beardedbaby1010.com`.
   Since DNS is already at Cloudflare, it wires the records up itself.

No `CNAME` file, no `.nojekyll` — those are GitHub Pages things. HTTPS is
automatic.

### Step 4 — Lock the front door with Access

1. Cloudflare dashboard → **Zero Trust** (it may ask you to pick a team name and
   choose a plan — choose **Free**; a payment method may be requested but the free
   plan is not charged).
2. **Access** → **Applications** → **Add an application** → **Self-hosted**.
3. Configure:
   - **Application name:** beardedbaby1010
   - **Session duration:** how long a login lasts — 1 week is a sane start
   - **Domain:** `beardedbaby1010.com`, **path left empty**

   Leaving the path empty is what makes this cover *every* URL on the domain.
   A path of `/private` would protect only that subtree.
4. Add a second domain entry for `www.beardedbaby1010.com` so both spellings are
   covered.
5. **Add a policy:**
   - **Name:** Allowed people
   - **Action:** Allow
   - **Rule:** `Emails` → list the exact addresses, **or** `Emails ending in` →
     `@downstate.edu` to let a whole institution in.
6. **Login methods:** enable **One-time PIN**. That is the email-a-code flow and
   needs no other identity provider.
7. Save.

### Step 5 — Test it properly

Do not skip this, and do not test in your normal browser window — you may already
hold a session cookie and conclude it is broken when it is working.

1. Open a **private/incognito window**.
2. Visit `https://beardedbaby1010.com` → you should get the Cloudflare login page.
3. Enter an allowed email → check for the code → enter it → the site loads.
4. In another incognito window, try a **deep URL** that exists, e.g.
   `https://beardedbaby1010.com/assets/site.css`. **It must also prompt for
   login.** If a raw asset loads without auth, your application's domain or path
   is wrong — fix it before adding content.
5. Try an email that is *not* on the allow-list. It should be refused.

### Step 6 — Close the side doors

Two ways in that bypass your front door if you forget them:

- **The `*.pages.dev` URL.** `beardedbaby1010.pages.dev` serves the same site and
  is not covered by an Access policy scoped to your custom domain. Either add a
  second Access application for `beardedbaby1010.pages.dev`, or disable the
  pages.dev access in the project settings.
- **Preview deployments.** Every branch gets its own preview URL. In the Pages
  project → **Settings** → enable Access protection for preview deployments (or
  only ever push to the production branch).

---

## Part 4 — What to copy from henryblair.online

The generator is not research-specific. Copy these into the new repo:

```
build_site.py        the generator — the tab bar, the badge, the gates,
                     the cache-busting, the date and toolchain passes
publish              rebuild → safety checks → commit → push
assets/site.css      all the shared styling
assets/project.css   the inner-page chrome (sidebar, tables, figures)
.gitignore           keeps _source/, _secrets/, _downloadable/ out of git
```

Then create a fresh `projects.py`. **Do not copy the old one** — it is 82 KB of
urology content. Copy only its *shape*: the `SOURCE_ROOTS`, `PAGES`,
`DOWNLOAD_ALIASES` and `PROJECTS` structures, with your own entries.

What you get for free by copying, without writing any of it again:

- the scrolling tab bar that auto-centres the open tab
- the floating headshot/logo badge on every page
- three page kinds — `auto` (written entirely in the config), `generated` (from a
  standalone HTML export), `static` (hand-written)
- passphrase gates for individual files, and the `EMBED_GATES` mechanism for
  videos hosted elsewhere
- `?v=<hash>` cache-busting on shared assets
- the house-style passes: dates normalised to `Month Dayth, Year`, toolchain
  names stripped from published pages
- the fail-closed rule: a gated item with no passphrase is not published at all

### Do you still need the per-file gates?

Behind Access, mostly no — everything is already private. Keep them for one case:
something you want to share with *one specific person* without giving them a
login to the whole site. Send them the encrypted file's URL and its passphrase;
Access still fronts the domain, so they need both. Belt and braces.

---

## Part 5 — Making it your own

### The look lives in four CSS variables

At the top of `assets/site.css`:

```css
:root{
  --ink:#111;        /* body text */
  --ink2:#33383c;    /* secondary text */
  --mut:#6b6f73;     /* captions, metadata */
  --line:#d9dbdd;    /* rules and borders */
  --bg:#f4f4f2;      /* page background */
  --surf:#fff;       /* cards */
  --accent:#1c4f7c;  /* links — the one colour that carries identity */
  --sitebar:34px;    /* tab bar height */
  --badge:160px;     /* the top-left square */
  --sans: …;         /* UI font stack */
  --serif: …;        /* headline font stack */
}
```

Change `--accent`, `--bg` and `--serif` and it stops looking like the research
portfolio while keeping the layout that works. Everything else follows from these.

### The badge

`assets/headshot-badge.png`, a 512×512 square. Any logo or image works. Keep it
square — it is displayed as a circle inside a dark tile, so anything important
must sit inside the inscribed circle, away from the corners.

### The structure

`PAGES` in `projects.py` holds the hand-written tabs (About, Contact, and so on).
`PROJECTS` holds everything generated. The tab bar is built from both, in order.
Rename the concept freely — the code does not care whether an entry is a research
project, a recipe, a chapter or a client.

---

## Part 6 — Publishing

Identical to henryblair.online, with one difference in what happens after the push:

```bash
cd ~/Documents/beardedbaby1010.com
./publish "what changed"
```

`publish` rebuilds every page, runs its safety checks, commits, and pushes.
**Cloudflare Pages picks up the push and redeploys automatically** — usually
faster than GitHub Pages did, under a minute. You can watch each deployment in
the Pages dashboard, which is a real improvement: GitHub Pages fails silently,
Cloudflare shows you a build log.

Preview locally exactly as before:

```bash
python3 build_site.py
python3 -m http.server 8000
```

Use the server, not a `file://` preview — the gate pages need WebCrypto, which
only works over https or on localhost.

---

## Part 7 — Things that will bite you

These are all learned the hard way on henryblair.online. Every one cost real time.

### Never hand-edit a generated file

Anything under `projects/` or `downloads/` is rewritten on every build. Editing
it works, looks right, and is silently destroyed on the next `./publish`. Change
the config instead. If you find yourself editing generated HTML, that is a signal
the generator needs a new option.

### Cache-busting is not optional

Hosts tell browsers to cache `/assets/*` for a long time. Change your CSS and a
returning visitor gets **new HTML against the old stylesheet** — which renders as
a broken-looking page for them and a fine page for you, the worst kind of bug.
The `?v=<content-hash>` stamp in `build_site.py` fixes this permanently. It is
already in the code you are copying; do not remove it.

### iCloud will eat your repository

If the folder lives in `~/Documents` with iCloud Drive and "Optimize Mac Storage"
on, macOS silently evicts files to the cloud — including `.git` internals. The
symptom is `OSError: [Errno 35] Resource deadlock avoided`, or git dying with a
bus error, or git returning nothing at all.

**Fix it before you start:** right-click the project folder in Finder → **Keep
Downloaded**. Do it for every folder the build reads from, not just the repo.

### Git repositories full of large generated files get fat

henryblair.online's `.git` is over 100 MB, because a 4.4 MB page is rewritten in
most commits and git keeps every version forever. Nothing breaks, but clones are
slow and it cannot be undone without rewriting history.

For the new site: keep large binaries out of the repo where you can, and if a
generated page is going to be multi-megabyte and change often, consider whether
it needs to be committed at all.

### The 100 MB file limit

GitHub rejects any single file over 100 MB (and warns above 50 MB). Video is the
usual casualty. Host video elsewhere — Vimeo, YouTube unlisted, Descript — and
embed it. Behind Access the embed is as private as the rest of the site anyway.

### Fail closed, always

The gate code refuses to publish a protected item whose passphrase is missing,
rather than publishing it unprotected. Keep that behaviour. The failure mode it
prevents — silently publishing something you believed was private — is the one
that actually matters.

### Test privacy from outside

After any change to Access policies, test in an incognito window with an email
that should *not* work. It is very easy to convince yourself a site is protected
when you are simply carrying a valid session cookie.

### Nothing shared can be unshared

If someone has downloaded a file or been told a link, no later change takes it
back. Rotating a passphrase or removing an email from the allow-list stops
*future* access only. Decide what to publish on that basis.

---

## Part 8 — Checklist

**Setup**

- [ ] Private GitHub repo created, cloned to `~/Documents/beardedbaby1010.com/`
- [ ] GitHub Pages **not** enabled on it
- [ ] Finder → **Keep Downloaded** on the folder
- [ ] Domain added to Cloudflare, nameservers changed at GoDaddy, domain active
- [ ] Cloudflare Pages project connected to the repo, build command blank,
      output directory `/`
- [ ] Custom domain added — both apex and `www`
- [ ] Zero Trust Access application created: domain set, **path empty**
- [ ] Policy added with the allow-list; One-time PIN login enabled

**Verify before adding content**

- [ ] Incognito → homepage prompts for login
- [ ] Incognito → a deep asset URL also prompts for login
- [ ] A non-allow-listed email is refused
- [ ] `*.pages.dev` is protected or disabled
- [ ] Preview deployments are protected

**Then build**

- [ ] `build_site.py`, `publish`, `assets/*.css`, `.gitignore` copied over
- [ ] Fresh `projects.py` with your own content
- [ ] `--accent`, `--bg`, fonts and badge changed
- [ ] `./publish` runs clean and Cloudflare redeploys
- [ ] A real page loads correctly after logging in

---

## If you get stuck

The failure is almost always one of these:

| Symptom | Cause |
|---|---|
| Site loads without asking for a login | Access application domain or path is wrong, or you are testing with a live session cookie |
| Login page never appears, DNS errors | Nameservers not yet switched, or not yet propagated |
| Changes do not appear | Check the Pages deployment log — the build may have failed, or the push may not have landed |
| Page looks unstyled after a CSS change | Cached stylesheet; the version stamp is missing or you did not re-run the build |
| Anything "Resource deadlock avoided" | iCloud evicted the file — Keep Downloaded |
| Git bus errors or silent failures | Same cause — iCloud eviction inside `.git` |
