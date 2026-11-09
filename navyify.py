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
