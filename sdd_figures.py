# -*- coding: utf-8 -*-
"""The two figures for the same-day-discharge project, drawn from its workbook.

The two that were on the page came from an early pipeline test run -- the
project's own guide says "there is no workbook or saved answers for this
project" -- which is why one was a forest plot with a single row and the other
labelled twenty zeros. These are drawn instead from the Google workbook that
does hold the analysis, live:

    Trend_SDD           same-day discharge share, by year
    Trend_Readmission   30-day readmission by year, split by discharge timing

    python3 sdd_figures.py [outdir]
"""
import csv, io as _io, math, os, sys, urllib.parse, urllib.request

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ANCHOR, MID = "#091e48", "#1B6FC4"
RAMP = ("#10385F", "#2E6B9E", "#5F97C4", "#97BFDC", "#C9DCEA")
INK, MUT, LINE = "#132742", "#5c7490", "#b9c5d0"

SHEET = "1ESAUzokZpr5G3zCwJRQcMYPvFmNTOQEqxPUvyahWqo8"
GVIZ = ("https://docs.google.com/spreadsheets/d/%s/gviz/tq"
        "?tqx=out:csv&headers=0&sheet=%s")


def rows(tab):
    u = GVIZ % (SHEET, urllib.parse.quote(tab))
    req = urllib.request.Request(u, headers={"User-Agent": "henryblair.online"})
    txt = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    return list(csv.reader(_io.StringIO(txt)))


def years(tab, cols):
    """Rows whose first cell is a 4-digit year, until the table ends."""
    out, started = [], False
    for r in rows(tab):
        y = (r[0] or "").strip() if r else ""
        if not (y.isdigit() and len(y) == 4 and len(r) > max(cols)):
            if started:
                break
            continue
        try:
            vals = [int(str(r[c]).replace(",", "")) for c in cols]
        except ValueError:
            if started:
                break
            continue
        if any(v < 0 for v in vals) or int(y) in [o[0] for o in out]:
            if started:
                break
            continue
        started = True
        out.append((int(y),) + tuple(vals))
    return out


def wilson(k, n, z=1.96):
    if not n:
        return 0.0, 0.0
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * max(c - h, 0), 100 * min(c + h, 1)


def tidy(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(LINE)
    ax.tick_params(labelsize=9, colors=MUT)
    ax.yaxis.label.set_color(INK); ax.xaxis.label.set_color(INK)


def fig_uptake(out):
    d = years("Trend_SDD", [1, 2])                 # year, N, events
    ys = [r[0] for r in d]; N = [r[1] for r in d]; E = [r[2] for r in d]
    pct = [100.0 * e / n for e, n in zip(E, N)]
    lo, hi = zip(*[wilson(e, n) for e, n in zip(E, N)])

    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    ax.axvspan(2011.4, 2018.5, color=RAMP[4], alpha=.38, lw=0)
    ax.text(2015, 14.2, "Laparoscopic prostatectomy on Medicare's\nInpatient-Only List",
            ha="center", fontsize=8.6, color=MUT, linespacing=1.35)
    ax.annotate("removed, January 2018", xy=(2018, 0.9), xytext=(2018.25, 4.4),
                fontsize=9, color=ANCHOR,
                arrowprops=dict(arrowstyle="-", color=RAMP[2], lw=1.1))
    ax.fill_between(ys, lo, hi, color=ANCHOR, alpha=.14, lw=0)
    ax.plot(ys, pct, "-o", color=ANCHOR, lw=2.6, ms=6, mfc=ANCHOR,
            mec="white", mew=1.2, zorder=4)
    for x, y, e in zip(ys, pct, E):
        if y > 1.2 or x in (ys[0], ys[-1]):
            ax.annotate("%.1f%%" % y, (x, y), textcoords="offset points",
                        xytext=(0, 12), ha="center", fontsize=8.4,
                        color=ANCHOR, fontweight="bold")
    for x, n in zip(ys, N):
        ax.annotate("%s" % format(n, ","), (x, 0), xycoords=("data", "axes fraction"),
                    textcoords="offset points", xytext=(0, -42), ha="center",
                    fontsize=7.2, color=MUT)
    ax.set_xticks(ys); ax.set_ylim(0, 18); ax.set_xlim(2011.4, 2024.6)
    ax.set_ylabel("Discharged the same day (%)", fontsize=10.5)
    ax.set_title("Same-day discharge after robot-assisted radical prostatectomy, "
                 "ACS NSQIP 2012–2024", fontsize=12.5, fontweight="bold",
                 color=ANCHOR, loc="left", pad=12)
    tidy(ax)
    fig.text(0.012, -0.045,
             "Shaded band: Wilson 95%% CI. Cases per year printed under each point "
             "(%s in all). Read live from Trend_SDD." % format(sum(N), ","),
             fontsize=8.4, color=MUT)
    fig.savefig(out, dpi=190, facecolor="white", bbox_inches="tight", pad_inches=0.33)
    plt.close(fig)
    return len(ys), sum(N), sum(E)


def fig_readmission(out):
    d = years("Trend_Readmission", [1, 2, 4, 5])   # year, Nover, Eover, Nsdd, Esdd
    ys = [r[0] for r in d]
    ov = [100.0 * r[2] / r[1] if r[1] else None for r in d]
    sd = [100.0 * r[4] / r[3] if r[3] else None for r in d]
    sdn = [r[3] for r in d]

    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    ax.plot(ys, ov, "-s", color=MID, lw=2.3, ms=6, mfc="white", mec=MID, mew=1.9,
            label="Overnight stay", zorder=3)
    thin = [y for y, n in zip(ys, sdn) if n < 100]
    ax.plot(ys, sd, "-o", color=ANCHOR, lw=2.6, ms=6, mfc=ANCHOR, mec="white",
            mew=1.2, label="Same-day discharge", zorder=4)
    for x, y, n in zip(ys, sd, sdn):
        if n < 100:
            off = 14 if y < 2.0 else -17
            ax.annotate("n=%d" % n, (x, y), textcoords="offset points",
                        xytext=(0, off), ha="center", fontsize=7.2, color=MUT)
    if thin:
        ax.axvspan(min(thin) - .5, max(thin) + .5, color=RAMP[4], alpha=.34, lw=0)
        ax.text((min(thin) + max(thin)) / 2.0, 7.4,
                "fewer than 100 same-day cases a year\n— these points are noise",
                ha="center", fontsize=8.4, color=MUT, linespacing=1.35)
    ax.set_xticks(ys); ax.set_ylim(0, 8); ax.set_xlim(2011.5, 2024.5)
    ax.set_ylabel("Readmitted within 30 days (%)", fontsize=10.5)
    ax.set_title("Thirty-day readmission did not rise as same-day discharge scaled",
                 fontsize=12.5, fontweight="bold", color=ANCHOR, loc="left", pad=12)
    ax.legend(frameon=False, fontsize=9.6, loc="upper right")
    tidy(ax)
    fig.text(0.012, -0.03,
             "Crude rates by year and discharge timing. Same-day discharge is scarce "
             "before 2019, so those points move on a handful of events. Read live "
             "from Trend_Readmission.", fontsize=8.4, color=MUT)
    fig.savefig(out, dpi=190, facecolor="white", bbox_inches="tight", pad_inches=0.33)
    plt.close(fig)
    return len(ys)


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(d, exist_ok=True)
    a = fig_uptake(os.path.join(d, "Figure_1_uptake.png"))
    b = fig_readmission(os.path.join(d, "Figure_2_readmission.png"))
    print("uptake: %d years, %s cases, %s same-day" % (a[0], format(a[1], ","), format(a[2], ",")))
    print("readmission: %d years" % b)
