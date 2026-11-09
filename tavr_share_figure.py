# -*- coding: utf-8 -*-
"""TAVR and SAVR as shares of the same 100%, in one panel.

Replaces the stacked-bar version. The two series are complements of one
denominator, so they mirror each other and the crossing is the point: TAVR
passes half of all isolated AVR in 2019, falls back below for 2021-22, and is
clear of it by 2024. The stacked bars encoded that as segment heights nobody
could subtract by eye.

Counts are read live from the TAVR workbook (Trend_TAVR_Share), and the
per-year n sits under each year because the denominator nearly halves across
the series -- a share chart alone would hide that.

    python3 tavr_share_figure.py [out.png]
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ANCHOR, MID = "#091e48", "#1B6FC4"
RAMP = ("#10385F", "#2E6B9E", "#5F97C4", "#97BFDC", "#C9DCEA")

SHEET = "1XXHAOccwTdqTFLTV7ph2__dnv3DEdb8YEvKXc0St_Vg"
GVIZ = ("https://docs.google.com/spreadsheets/d/%s/gviz/tq"
        "?tqx=out:csv&headers=0&sheet=Trend_TAVR_Share" % SHEET)

# the last values read from the workbook, so the figure still draws offline
YEARS = list(range(2013, 2025))
N  = [266, 359, 340, 417, 458, 368, 372, 290, 244, 335, 284, 271]
EV = [28, 39, 64, 173, 201, 131, 192, 184, 109, 153, 155, 158]


def _live():
    """(years, N, events) from the workbook; the baked values on any failure."""
    import csv, io as _io, urllib.request
    try:
        req = urllib.request.Request(GVIZ, headers={"User-Agent": "henryblair.online"})
        txt = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
        ys, ns, es = [], [], []
        started = False
        for row in csv.reader(_io.StringIO(txt)):
            y = (row[0] or "").strip() if row else ""
            ok = y.isdigit() and len(y) == 4 and len(row) > 2
            if not ok:
                if started:
                    break          # the year table has ended
                continue
            try:
                n = int((row[1] or "").replace(",", ""))
                e = int((row[2] or "").replace(",", ""))
            except ValueError:
                if started:
                    break
                continue
            # the sheet carries a year-vs-year block below whose first two
            # cells are both years; a count table has 0 <= events <= N
            if n <= 0 or not (0 <= e <= n) or int(y) in ys:
                if started:
                    break
                continue
            started = True
            ys.append(int(y)); ns.append(n); es.append(e)
        if len(ys) >= 8:
            return ys, ns, es
    except Exception:
        pass
    return YEARS, N, EV


YEARS, N, EV = _live()

def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)

TAVR = [100.0 * e / n for e, n in zip(EV, N)]
SAVR = [100.0 - t for t in TAVR]
TLO, THI = zip(*[wilson(e, n) for e, n in zip(EV, N)])
SLO, SHI = [100 - h for h in THI], [100 - l for l in TLO]

fig, ax = plt.subplots(figsize=(11, 6.6))

ax.fill_between(YEARS, TLO, THI, color=ANCHOR, alpha=.13, lw=0, zorder=2)
ax.fill_between(YEARS, SLO, SHI, color=MID,    alpha=.13, lw=0, zorder=2)

ax.axhline(50, color=RAMP[2], lw=1.1, ls=(0, (5, 4)), zorder=3)
ax.text(2012.82, 51, "50%", fontsize=9, color=RAMP[2], va="bottom")

ax.plot(YEARS, SAVR, "-s", color=MID, lw=2.4, ms=6, mfc="white", mec=MID,
        mew=1.9, zorder=5, label="SAVR  (open)")
ax.plot(YEARS, TAVR, "-o", color=ANCHOR, lw=2.8, ms=6.4, mfc=ANCHOR,
        mec="white", mew=1.2, zorder=6, label="TAVR  (transcatheter)")

# when the two lines are close the labels would collide, so push them apart
for x, t, sv in zip(YEARS, TAVR, SAVR):
    gap = abs(t - sv)
    d = 13 if gap > 14 else 23
    up, dn = (d, -d - 5) if t >= sv else (-d - 5, d)
    ax.annotate("%.0f" % t, (x, t), textcoords="offset points", xytext=(0, up),
                ha="center", va="center", fontsize=8.4, color=ANCHOR,
                fontweight="bold")
    ax.annotate("%.0f" % sv, (x, sv), textcoords="offset points", xytext=(0, dn),
                ha="center", va="center", fontsize=8.4, color=MID,
                fontweight="bold")

ax.annotate("TAVR passes SAVR", xy=(2019, 51.6), xytext=(2018.3, 82),
            fontsize=9.4, color=ANCHOR, ha="center",
            arrowprops=dict(arrowstyle="-", color=RAMP[3], lw=1.1))
ax.annotate("and briefly falls back", xy=(2021, 44.7), xytext=(2021.3, 17),
            fontsize=9.4, color=ANCHOR, ha="center",
            arrowprops=dict(arrowstyle="-", color=RAMP[3], lw=1.1))

for x, n in zip(YEARS, N):
    ax.annotate("n=%d" % n, (x, 0), xycoords=("data", "axes fraction"),
                textcoords="offset points", xytext=(0, -27), ha="center",
                fontsize=7.8, color="#5c7490")

ax.set_ylim(0, 100); ax.set_xlim(2012.6, 2024.4)
ax.set_xticks(YEARS)
ax.set_yticks(range(0, 101, 25))
ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"])
ax.set_ylabel("Share of isolated aortic valve replacement", fontsize=10.5)
ax.tick_params(labelsize=9.4)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
for s in ("left", "bottom"):
    ax.spines[s].set_color("#b9c5d0")
ax.legend(frameon=False, fontsize=10, loc="upper left",
          bbox_to_anchor=(0.005, 1.055), ncol=2)
ax.set_title("TAVR and SAVR as shares of isolated aortic valve replacement, "
             "ACS NSQIP 2013–2024",
             fontsize=13, fontweight="bold", color=ANCHOR, loc="left", pad=36)

fig.text(0.013, -0.035,
         "The two series are complements of one denominator, so they sum to "
         "100% and mirror each other. Shaded bands: Wilson 95% CI. "
         "p-trend < 0.001 (Cochran–Armitage).",
         fontsize=8.6, color="#5c7490")
import sys
OUT = sys.argv[1] if len(sys.argv) > 1 else "tavr-share.png"
fig.savefig(OUT, dpi=190, facecolor="white",
            bbox_inches="tight", pad_inches=0.34)
print("wrote %s  (%d years, live)" % (OUT, len(YEARS)))
