# -*- coding: utf-8 -*-
"""Recolour a greyscale figure onto the site's blue ramp.

The NSQIP pipeline draws in black and white. Rather than re-run six
generators to change their colours, this maps each pixel's lightness onto
figpalette.RAMP: black becomes the anchor navy, mid-greys become the ramp's
middle steps, white stays white. Ordering is preserved, so a chart that was
readable in greyscale stays readable, and it is still readable if someone
prints it back to greyscale.

Pixels that already carry colour are left alone, so running it twice does
nothing the second time.

    python3 navyify.py in.png out.png [--width 1600]
"""
import sys
from PIL import Image

from figpalette import RAMP, SERIES

def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

# lightness -> colour. Anchored on the palette, ending at white.
STOPS = [(0.00, _rgb(SERIES[0])),
         (0.16, _rgb(RAMP[0])),
         (0.36, _rgb(RAMP[1])),
         (0.57, _rgb(RAMP[2])),
         (0.75, _rgb(RAMP[3])),
         (0.89, _rgb(RAMP[4])),
         (1.00, (255, 255, 255))]


def lut():
    out = []
    for i in range(256):
        t = i / 255.0
        for j in range(len(STOPS) - 1):
            a, b = STOPS[j], STOPS[j + 1]
            if a[0] <= t <= b[0]:
                f = 0 if b[0] == a[0] else (t - a[0]) / (b[0] - a[0])
                out.append(tuple(int(round(a[1][k] + f * (b[1][k] - a[1][k])))
                                 for k in range(3)))
                break
        else:
            out.append(STOPS[-1][1])
    return out


def convert(src, dst, width=None, sat_tol=18):
    im = Image.open(src).convert("RGB")
    if width and im.width > width:
        im = im.resize((width, max(1, round(im.height * width / im.width))),
                       Image.LANCZOS)
    L = lut()
    px = im.load()
    W, H = im.size
    for y in range(H):
        for x in range(W):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > sat_tol:
                continue                      # already coloured; leave it
            px[x, y] = L[(r * 299 + g * 587 + b * 114) // 1000]
    im.save(dst, optimize=True)
    return im.size


if __name__ == "__main__":
    a = sys.argv[1:]
    w = None
    if "--width" in a:
        i = a.index("--width"); w = int(a[i + 1]); a = a[:i] + a[i + 2:]
    print(convert(a[0], a[1], w))


# ---------------------------------------------------------------- bar gradient
def bars(src, dst, width=None, min_frac=0.0008):
    """Recolour, then paint each bar its own step of the ramp.

    A bar chart whose bars all share one grey comes out of the lightness map
    with all its bars one blue, which is what the eye reads as "no
    information here". The bars are large connected regions of a single fill,
    so they can be found and coloured by position instead -- left to right
    across the ramp, which is also the order the chart is already sorted in.

    Everything that is not a bar (text, axes, error bars) goes through the
    ordinary lightness map.
    """
    import numpy as np
    from scipy import ndimage
    from PIL import Image

    im = Image.open(src).convert("RGB")
    if width and im.width > width:
        im = im.resize((width, max(1, round(im.height * width / im.width))),
                       Image.LANCZOS)
    # int32, not int16: 255*587 overflows a signed 16-bit accumulator and
    # the whole background comes back inverted
    a = np.asarray(im).astype(np.int32)
    g = (a[:, :, 0] * 299 + a[:, :, 1] * 587 + a[:, :, 2] * 114) // 1000
    flat = (a.max(2) - a.min(2)) <= 18                 # grey pixels only

    # candidate fills: greys that cover a meaningful area and are not paper
    vals, counts = np.unique(g[flat], return_counts=True)
    area = g.size
    # Anti-aliasing smears one fill across several adjacent greys, and
    # scanning each separately finds every bar once per grey. Cluster first.
    cand = [(int(v), int(c)) for v, c in zip(vals, counts)
            if c / area >= min_frac and 18 < v < 246]
    fills, groups = [], []
    for v, c in sorted(cand):
        if groups and v - groups[-1][-1][0] <= 6:
            groups[-1].append((v, c))
        else:
            groups.append([(v, c)])
    for grp in groups:
        tot = sum(c for _, c in grp)
        fills.append(int(round(sum(v * c for v, c in grp) / float(tot))))

    L = lut()
    out = np.zeros(a.shape, dtype=np.uint8)
    for i in range(256):
        out[g == i] = L[i]
    out[~flat] = a[~flat].astype(np.uint8)             # keep existing colour

    boxes = []
    for v in fills:
        m = flat & (np.abs(g - v) <= 6)
        lab, n = ndimage.label(m)
        if not n:
            continue
        for sl, idx in zip(ndimage.find_objects(lab), range(1, n + 1)):
            h, w = sl[0].stop - sl[0].start, sl[1].stop - sl[1].start
            comp = (lab[sl] == idx)
            if comp.sum() < area * min_frac:
                continue
            if comp.sum() / float(h * w) < 0.80:       # bars are solid blocks
                continue
            if h < 8 or w < 8:
                continue
            boxes.append((sl[1].start + w / 2.0, sl, idx, lab))

    # Glyphs and legend swatches are solid blocks too. Bars share a bottom
    # edge and are a large fraction of the biggest block; keep those.
    if boxes:
        areas = [(b[1][0].stop - b[1][0].start) * (b[1][1].stop - b[1][1].start)
                 for b in boxes]
        big = max(areas)
        bottoms = [b[1][0].stop for b in boxes]
        from collections import Counter
        base, _ = Counter(bottoms).most_common(1)[0]
        boxes = [b for b, ar in zip(boxes, areas)
                 if ar >= big * 0.04 and abs(b[1][0].stop - base) <= 3]

    if len(boxes) >= 3:
        boxes.sort(key=lambda b: b[0])
        n = len(boxes)
        stops = [_rgb(c) for c in (SERIES[0],) + tuple(RAMP)]
        for k, (_, sl, idx, lab) in enumerate(boxes):
            t = k / float(n - 1)
            pos = t * (len(stops) - 1)
            lo = min(int(pos), len(stops) - 2)
            f = pos - lo
            col = tuple(int(round(stops[lo][j] + f * (stops[lo + 1][j] - stops[lo][j])))
                        for j in range(3))
            region = out[sl]
            region[lab[sl] == idx] = col
            out[sl] = region

    Image.fromarray(out).save(dst, optimize=True)
    return len(boxes)
