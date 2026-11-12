#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check every BCa query row in a Google Sheet tab against the canonical group spec.

    python3 check_sheet.py <sheet url or key> <tab name> [--write] [--col H]

Reads the tab live, predicts from each query NAME what groups/terms/operators/
windows it must have, compares against the dump cells, and prints ✓/✗ per row.
With --write it inserts a column (default H) holding "✓" or "✗ <reason>".

Needs: pip3 install gspread  ·  creds at ~/mnt/Google_APIs_Creds_Tokens/credentials.json
(override with  TNX_CREDS=/path/to/credentials.json)
"""
import sys, os, re, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spec import check, expected, _clean          # the derived spec

DEFAULT_CREDS = os.path.expanduser("~/mnt/Google_APIs_Creds_Tokens/credentials.json")
if not os.path.exists(DEFAULT_CREDS):
    DEFAULT_CREDS = os.path.expanduser(
        "/Library/Informatics/Google_APIs_Creds_Tokens/credentials.json")

def key_of(s):
    m = re.search(r'/spreadsheets/d/([A-Za-z0-9_-]+)', s)
    return m.group(1) if m else s.strip()

def col_to_idx(c):
    n = 0
    for ch in c.upper(): n = n*26 + (ord(ch)-64)
    return n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet"); ap.add_argument("tab")
    ap.add_argument("--write", action="store_true",
                    help="insert the verdict column into the sheet")
    ap.add_argument("--col", default="H",
                    help="column to insert the verdict at (default H)")
    ap.add_argument("--creds", default=os.environ.get("TNX_CREDS", DEFAULT_CREDS))
    a = ap.parse_args()

    import gspread
    gc = gspread.service_account(filename=a.creds)
    ws = gc.open_by_key(key_of(a.sheet)).worksheet(a.tab)
    # FORMULA, not the displayed text: the API returns formatted cells with the
    # newlines stripped, which collapses every group into one unsplittable line.
    rows = ws.get("A1:AC%d" % ws.row_count, value_render_option="FORMULA")
    rows = [r for r in rows if r and str(r[0]).strip()]

    verdicts, ok, bad, skip = [], 0, 0, 0
    for r in rows:
        name = _clean(r[0]).strip()
        good, probs = check(r)
        if good is None:
            skip += 1; verdicts.append(["—"])
            print("  —  %-46s name not in the BCa grammar" % name[:46])
        elif good:
            ok += 1; verdicts.append(["✓"])
        else:
            bad += 1; verdicts.append(["✗ " + "; ".join(probs)])
            print("  ✗  %-46s %s" % (name[:46], "; ".join(probs)))

    print("\n%s · %s" % (a.tab, key_of(a.sheet)))
    print("rows %d  |  ✓ %d  |  ✗ %d  |  name not in grammar %d"
          % (len(rows), ok, bad, skip))

    if a.write:
        ws.insert_cols([[]], col_to_idx(a.col))
        ws.update(range_name="%s1:%s%d" % (a.col, a.col, len(verdicts)),
                  values=verdicts, value_input_option="RAW")
        print("wrote %d verdicts into column %s (everything shifted right one)"
              % (len(verdicts), a.col))
    else:
        print("read-only; add --write to insert the column")

if __name__ == "__main__":
    main()
