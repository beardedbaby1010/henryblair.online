# -*- coding: utf-8 -*-
"""Read a pipeline All_Figures.html and return what it says about each figure.

The pipeline already writes, for every figure it draws, a title, a one-line
description of what it shows, and the workbook tab its numbers come from.
That is exactly the caption a project page wants, so take it from there
rather than writing it again by hand.
"""
import html as H
import os
import re


def read(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    body = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S | re.I)

    out = []
    # each entry names its PNG; the text after it is the description and tab
    for m in re.finditer(r'>([A-Za-z0-9_]+\.png)\s*&#8599;|>([A-Za-z0-9_]+\.png)\s*↗', body):
        png = m.group(1) or m.group(2)
        tail = body[m.end():m.end() + 1200]
        tail = re.sub(r"<[^>]+>", "\n", tail)
        tail = H.unescape(tail)
        lines = [l.strip() for l in tail.splitlines() if l.strip()]
        desc, tab = "", ""
        for i, l in enumerate(lines):
            if l.startswith("Shows "):
                desc = l
            if l.startswith("Numbers:"):
                for nxt in lines[i + 1:i + 3]:
                    if nxt and not nxt.startswith("tab of"):
                        tab = nxt
                        break
                break
            if desc and i > 4:
                break
        num = re.match(r"Figure_(S?\d+)_?(.*)", os.path.splitext(png)[0])
        label = ("Figure %s" % num.group(1)) if num else os.path.splitext(png)[0]
        name = (num.group(2).replace("_", " ").strip().capitalize()
                if num and num.group(2) else "")
        out.append({"png": png, "label": label, "name": name,
                    "desc": desc[6:].strip().rstrip(".") if desc else "",
                    "tab": tab})
    return out


if __name__ == "__main__":
    import sys
    for f in sys.argv[1:]:
        print("###", os.path.basename(f))
        for e in read(f):
            print("  %-34s %-13s %-22s %s" % (e["png"], e["label"], e["tab"], e["desc"][:64]))
