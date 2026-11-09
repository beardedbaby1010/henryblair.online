# -*- coding: utf-8 -*-
"""Is every live-linked page still reading its workbook?

A page that loses its sheet does not break -- it falls back to the cache and
keeps showing the last good numbers, which is the right behaviour and also
means a renamed tab can go unnoticed for months. This asks all eleven sources
the same question and prints one line each: where the numbers came from, how
many fields resolved, and which did not.

    python3 _audit/live_check.py          every source
    python3 _audit/live_check.py --cache  use the cache, do not touch the network

Exit status is 1 if anything came from the cache or left a field empty.
"""
import os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

import sheet_live, pvr_live, pca_figure, ve_figure           # noqa: E402

CACHE = os.path.join(tempfile.gettempdir(), "henryblair-live-check")


def line(name, vals, source):
    empty = sorted(k for k, v in (vals or {}).items() if v is None)
    n = len(vals or {})
    print("  %-26s %-12s %2d/%2d fields%s"
          % (name, source, n - len(empty), n,
             ("   empty: " + ", ".join(empty[:8])) if empty else ""))
    return source == "sheet" and n and not empty


def main():
    fetch = "--cache" not in sys.argv
    os.makedirs(CACHE, exist_ok=True)
    ok = True

    print("Workbook-backed pages (sheet_live.py)")
    for slug in sorted(sheet_live.SHEETS):
        try:
            vals, src = sheet_live.load(slug, CACHE, do_fetch=fetch)
        except Exception as e:
            print("  %-26s EXCEPTION   %s" % (slug, e)); ok = False; continue
        ok &= line(slug, vals, src)

    print("\nPages with their own module")
    vals, src = pvr_live.load(os.path.join(CACHE, "pvr.json"), fetch=fetch)
    ok &= line("oab-pvr", vals, src)

    for mod, name in ((pca_figure, "adt-initiation"), (ve_figure, "ve-boxed-warning")):
        r = mod.load(os.path.join(CACHE, name + ".json"), fetch=fetch)
        vals, src = r[0], r[-1]
        ok &= line(name, vals, src)
        try:
            svg = mod.build(*r[:-1])
            print("  %-26s derivation figure: %d bytes, %d labels"
                  % ("", len(svg), svg.count("<text")))
        except Exception as e:
            print("  %-26s FIGURE FAILED: %s: %s" % ("", type(e).__name__, e))
            ok = False

    print("\n%s" % ("all sources live and complete" if ok
                    else "something fell back to cache or left a field empty"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
