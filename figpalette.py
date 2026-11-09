# -*- coding: utf-8 -*-
"""The one place the site's figure colours are defined.

Chosen 9 Nov 2026 from a side-by-side test of four blue palettes on the two
jobs these figures actually do: telling two series apart, and naming five
groups. The pair and the ramp were picked separately, which is why they are
separate here --- a two-series chart needs contrast, a five-bar chart needs a
sequence, and one list cannot be good at both.

    SERIES   two lines that must not be confused with each other
    RAMP     an ordered set of categories, dark to pale
    P        the named roles the cohort-derivation diagrams draw with
    TINT     the pale wash behind each family's boxes

Greyscale was part of the test: RAMP's five steps stay evenly spaced when a
journal prints it in black and white.
"""

# two series, maximum separation, navy first
SERIES = ("#091e48", "#1B6FC4")

# five ordered categories, dark to pale
RAMP = ("#10385F", "#2E6B9E", "#5F97C4", "#97BFDC", "#C9DCEA")

ANCHOR = SERIES[0]

# roles for the cohort-derivation SVGs (pca_figure.py, ve_figure.py)
P = {
    "ink":    "#132742",   # text and rules
    "mut":    "#5c7490",   # secondary text
    "line":   "#bccbd9",   # hairlines
    "arrow":  "#8aa6c2",   # connectors
    "black":  ANCHOR,      # the cohort itself
    "teal":   RAMP[1],     # first query family
    "plum":   RAMP[2],     # second query family
    "slate":  RAMP[3],     # comparison arms
    "band":   "#eef3f9",   # band background
    "bandbd": "#cfdceb",   # band border
}

# the pale wash behind each family
TINT = {
    "teal":  "#e6eef6",
    "plum":  "#eef4fa",
    "slate": "#f3f8fc",
    "black": "#e8ecf3",
}


def matplotlib(plt):
    """Apply the palette to a matplotlib session, for the generator scripts."""
    plt.rcParams.update({
        "axes.prop_cycle": plt.cycler(color=list(RAMP)),
        "axes.edgecolor": P["line"],
        "axes.labelcolor": P["ink"],
        "text.color": P["ink"],
        "xtick.color": P["mut"],
        "ytick.color": P["mut"],
        "axes.titlecolor": P["ink"],
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 10,
    })


def on(fill, light="#ffffff", dark=None):
    """Readable text colour for a given fill.

    The ramp runs from near-black navy to a very pale blue, so "solid box =
    white text" stops being true halfway down it. This picks by relative
    luminance instead, which is what the contrast guidelines measure.
    """
    dark = dark or P["ink"]
    h = str(fill).lstrip("#")
    if len(h) != 6:
        return light
    def lin(c):
        c = int(h[c:c + 2], 16) / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    L = 0.2126 * lin(0) + 0.7152 * lin(2) + 0.0722 * lin(4)
    # contrast against white vs against the ink, whichever is better
    cw = 1.05 / (L + 0.05)
    hd = str(dark).lstrip("#")
    def lin2(c):
        c = int(hd[c:c + 2], 16) / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    Ld = 0.2126 * lin2(0) + 0.7152 * lin2(2) + 0.0722 * lin2(4)
    cd = (max(L, Ld) + 0.05) / (min(L, Ld) + 0.05)
    return light if cw >= cd else dark
