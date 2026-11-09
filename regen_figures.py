#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate a project's figures from its live Google Sheet.

The figure generators already take their workbook from an environment
variable -- ADI_XLSX, PVR_XLSX, VE_XLSX, URPS_XLSX -- and their output
directory from a matching *_FIGDIR. So nothing in them has to change for them
to read live data: download the sheet as .xlsx, point the variable at the
download, run the script untouched.

That is all this does. It is deliberately not a rewrite of the generators:
they are the analysis, they are long, and they are already correct. This is
the one piece that was missing, which is a reliable way to say "use what is in
the spreadsheet right now".

    python3 regen_figures.py                 what it knows how to build
    python3 regen_figures.py adi             fetch the live sheet, run adi_figs.py
    python3 regen_figures.py adi pvr         several
    python3 regen_figures.py all             everything mapped
    python3 regen_figures.py adi --local     use the workbook already on disk
    python3 regen_figures.py adi --keep      leave the download in place
    python3 regen_figures.py adi --dry-run   say what it would do

Exit status is 0 only if every requested project succeeded.
"""
from __future__ import print_function

import argparse
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
MAIMO = os.environ.get("MAIMO_ROOT") or os.path.expanduser("~/Documents/Maimo_Work")
if not os.path.isdir(MAIMO):
    alt = os.path.join(HERE, "!Maimo_Work_alias")
    if os.path.isdir(alt):
        MAIMO = alt

CACHE = os.environ.get("LIVE_WORKBOOK_DIR") or os.path.expanduser(
    "~/Library/Caches/henryblair.online/live-workbooks")

EXPORT = "https://docs.google.com/spreadsheets/d/%s/export?format=xlsx"

# ---------------------------------------------------------------------------
# name -> what it takes to rebuild that project's figures
#
#   sheet     the Google Sheet the analysis lives in
#   script    the generator, relative to Maimo_Work
#   env_xlsx  the variable it reads its workbook path from
#   env_figdir the variable it reads its output directory from (None: it has
#             no such variable and writes beside itself)
#   figdir    where the figures land, relative to the script's own directory
#   slug      the project on the site, for --publish
PROJECTS = {
    "adi": {
        "title": "Deprivation & access (OAB)",
        "sheet": "1nVRKNIr4aPuSjBQUDhQfK3-7XajJ-Ni0irVtXjmSG1U",
        "script": "!Todays_Tasks/ADI_Project/adi_figs.py",
        "env_xlsx": "ADI_XLSX", "env_figdir": "ADI_FIGDIR",
        "figdir": "Figures", "slug": "oab-adi",
    },
    "adi-all": {
        "title": "Deprivation & access — every variable",
        "sheet": "1nVRKNIr4aPuSjBQUDhQfK3-7XajJ-Ni0irVtXjmSG1U",
        "script": "!Todays_Tasks/ADI_Project/adi_all_variable_figs.py",
        "env_xlsx": "ADI_XLSX", "env_figdir": "ADI_FIGDIR",
        "figdir": "Figures", "slug": None,
    },
    "pvr": {
        "title": "PVR self-estimation",
        "sheet": "1lnQ7RmxJbf1sU62X5P9kFJViR0yCRTeMl4sRNJV3zaM",
        "script": "!Todays_Tasks/PVR_Project/pvr_figs.py",
        "env_xlsx": "PVR_XLSX", "env_figdir": "PVR_FIGDIR",
        "figdir": "Figures", "slug": "oab-pvr",
    },
    "pvr-all": {
        "title": "PVR self-estimation — every variable",
        "sheet": "1lnQ7RmxJbf1sU62X5P9kFJViR0yCRTeMl4sRNJV3zaM",
        "script": "!Todays_Tasks/PVR_Project/pvr_all_variable_figs.py",
        "env_xlsx": "PVR_XLSX", "env_figdir": "PVR_FIGDIR",
        "figdir": "Figures", "slug": None,
    },
    "ve": {
        "title": "Vaginal estrogen after the boxed warning",
        "sheet": "1Cy64AGkUWwHMHl3a-F2AhOxZOmTl-iOJMsmy5FA85L8",
        "script": "!Todays_Tasks/VE_project/ve_figures.py",
        "env_xlsx": "VE_XLSX", "env_figdir": "VE_FIGDIR",
        "figdir": "Figures", "slug": "ve-boxed-warning",
    },
    "urps": {
        "title": "Urogynecology resident survey",
        "sheet": "16xPztZ5epiIFnTUqqXLcgzYIFHapAgoi_4Qu9n-iddw",
        "script": "!Todays_Tasks/Urogyne_project/urps_figs.py",
        "env_xlsx": "URPS_XLSX", "env_figdir": "URPS_FIGDIR",
        "figdir": "urps_figures", "slug": "urogyn-perceptions",
    },
    "pca": {
        "title": "ADT initiation (prostate cancer)",
        "sheet": "1r61VFTZoFx6jRbCFqB17m_67dbgG_cAGG5uO6r1OQIA",
        "script": "5_PCa_x_ADT/Scripts/pca_figures.py",
        "env_xlsx": "PCA_XLSX", "env_figdir": "PCA_FIGDIR",
        # the script defaults OUTPUT_DIR to a relative "Figures", which would
        # land wherever it is run from; naming it absolutely avoids that
        "figdir": "../Figures", "slug": "adt-initiation",
    },
}

IMAGES = (".png", ".jpg", ".jpeg", ".svg", ".pdf", ".webp")


def say(*a):
    try:
        print(*a)
        sys.stdout.flush()
    except BrokenPipeError:      # piped into head, which is fine
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)


def fetch(sheet, dest, timeout=180):
    """The sheet, as .xlsx. Raises if what comes back is not a workbook --
    a sign-in page is served with status 200 and would otherwise be handed to
    openpyxl as if it were data."""
    import urllib.request
    req = urllib.request.Request(EXPORT % sheet,
                                 headers={"User-Agent": "regen_figures.py"})
    tmp = dest + ".part"
    with urllib.request.urlopen(req, timeout=timeout) as r, open(tmp, "wb") as f:
        head = r.read(4)
        if head[:2] != b"PK":
            raise IOError("that link did not return a workbook (got %r...). "
                          "Is the sheet shared with anyone who has the link?"
                          % head)
        f.write(head)
        while True:
            chunk = r.read(1 << 20)
            if not chunk:
                break
            f.write(chunk)
    os.replace(tmp, dest)
    return os.path.getsize(dest)


def snapshot(d):
    """{path: mtime} for the images in a directory, before we touch it."""
    out = {}
    if not os.path.isdir(d):
        return out
    for n in os.listdir(d):
        if n.lower().endswith(IMAGES):
            p = os.path.join(d, n)
            try:
                out[p] = os.path.getmtime(p)
            except OSError:
                pass
    return out


def run(name, cfg, args):
    say("\n" + "=" * 72)
    say("%s  --  %s" % (name, cfg["title"]))
    say("=" * 72)

    if cfg.get("unmapped"):
        say("  SKIPPED: %s" % cfg["unmapped"])
        return None

    script = os.path.join(MAIMO, cfg["script"])
    if not os.path.exists(script):
        say("  script not found: %s" % script)
        return False
    sdir = os.path.dirname(script)
    figdir = os.path.abspath(os.path.join(sdir, cfg["figdir"]))

    env = dict(os.environ)
    book = None
    if args.local:
        say("  --local: leaving the workbook the script finds on its own")
    else:
        os.makedirs(CACHE, exist_ok=True)
        book = os.path.join(CACHE, "%s.xlsx" % name)
        say("  sheet   %s" % cfg["sheet"])
        if args.dry_run:
            say("  would download to %s" % book)
        else:
            t0 = time.time()
            try:
                n = fetch(cfg["sheet"], book)
            except Exception as e:
                say("  download failed: %s" % e)
                return False
            say("  got     %.1f MB in %.1fs" % (n / 1048576.0, time.time() - t0))
        env[cfg["env_xlsx"]] = book
    if cfg["env_figdir"]:
        env[cfg["env_figdir"]] = figdir

    say("  script  %s" % script)
    say("  figures %s" % figdir)
    if args.dry_run:
        say("  would run: %s %s" % (os.path.basename(sys.executable),
                                    os.path.basename(script)))
        return None

    before = snapshot(figdir)
    t0 = time.time()
    p = subprocess.run([sys.executable, script], cwd=sdir, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.decode("utf-8", "replace")
    took = time.time() - t0

    if p.returncode != 0:
        say("  FAILED after %.1fs (exit %d). Last of its output:" % (took, p.returncode))
        for line in out.strip().splitlines()[-25:]:
            say("    | %s" % line)
        return False

    after = snapshot(figdir)
    new = sorted(k for k in after if k not in before)
    upd = sorted(k for k in after if k in before and after[k] > before[k])
    say("  done in %.1fs: %d figure(s) written, %d new"
        % (took, len(new) + len(upd), len(new)))
    for p_ in new:
        say("    + %s" % os.path.basename(p_))
    for p_ in upd:
        say("    ~ %s" % os.path.basename(p_))
    if not new and not upd:
        say("    (nothing changed on disk -- check the script's own output:)")
        for line in out.strip().splitlines()[-15:]:
            say("    | %s" % line)
    if not args.keep and book and os.path.exists(book):
        os.remove(book)
    return True


def listing():
    say("Projects this can rebuild from their live sheet:\n")
    for name in sorted(PROJECTS):
        c = PROJECTS[name]
        flag = "  [not mapped yet]" if c.get("unmapped") else ""
        say("  %-9s %s%s" % (name, c["title"], flag))
        say("            %s" % c["script"])
    say("\n  python3 regen_figures.py <name> [<name>...]   or   all")
    say("  workbooks are downloaded to %s" % CACHE)


def main():
    ap = argparse.ArgumentParser(add_help=True, description=__doc__.splitlines()[0])
    ap.add_argument("names", nargs="*")
    ap.add_argument("--local", action="store_true",
                    help="do not download; let the script find its own workbook")
    ap.add_argument("--keep", action="store_true",
                    help="keep the downloaded workbook after the run")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    if not args.names:
        listing()
        return 0
    names = sorted(PROJECTS) if args.names == ["all"] else args.names
    bad = [n for n in names if n not in PROJECTS]
    if bad:
        say("unknown: %s" % ", ".join(bad)); listing(); return 2

    results = {n: run(n, PROJECTS[n], args) for n in names}
    say("\n" + "-" * 72)
    for n in names:
        r = results[n]
        say("  %-9s %s" % (n, "ok" if r else ("skipped" if r is None else "FAILED")))
    return 0 if all(r is not False for r in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
