# -*- coding: utf-8 -*-
"""Cohort-derivation figure for the vaginal-estrogen project page.

Built in the same idiom as pca_figure.py, and by the same rules: every count in
the spine is addressed by its query name in the VE master workbook's QM sheet,
never typed in here, so the figure cannot drift from the data. The build bakes
the answer into the SVG and assets/ve-live.js re-reads the same sheet in the
browser, so the page is right before any JavaScript runs and right again a
minute after the spreadsheet changes.

Three abstracts come out of one query tree, so the figure is one spine and three
panels: the trend and the formulations, the breast-cancer strata, and who the
rise reached.
"""
import html

# ---------------------------------------------------------------- the numbers
# key -> QM query name, or ("-", a, b) for a difference
SOURCES = {
    # the spine, post-announcement window
    "incare":    "Unstrat_denom_25",
    "incare24":  "Unstrat_denom_24",
    "inc":       "Unstrat_num_25",
    "inc24":     "Unstrat_num_24",
    "prev":      "Unstrat_prev_num_25",
    "prevden":   "Unstrat_prev_denom_25",
    # breast cancer strata, post window
    "hx":        "Hx_num_25",
    "hxden":     "Hx_denom_25",
    "ha":        "HA_num_25",
    "haden":     "HA_denom_25",
    "nh":        "NH_num_25",
    "nhden":     "NH_denom_25",
    "nha":       "NHA_num_25",
    "nhaden":    "NHA_denom_25",
    # receptor strata, pre window (the vintage the receptor block was run at)
    "erp":       "HA_ERP_num_24",
    "erpden":    "HA_ERP_denom_24",
    "ern":       "HA_ERN_num_24",
    "ernden":    "HA_ERN_denom_24",
    # non-estrogen alternatives
    "cp":        "CP_Unstrat_num_25",
    "cpha":      "CP_HA_num_25",
    # formulation, Jan-Mar 2026
    "ring":      "26Jan_VAG_RING_num",
    "tab":       "26Jan_VAG_TAB_num",
    "cream":     "26Jan_VAG_CREAM_num",
}

def resolve(qm):
    """qm: {query name: count} -> {key: int}. Differences resolved after names."""
    out, pending = {}, []
    for k, src in SOURCES.items():
        if isinstance(src, tuple):
            pending.append((k, src))
        else:
            out[k] = qm.get(src)
    for k, (_, a, b) in pending:
        out[k] = None if out.get(a) is None or out.get(b) is None else out[a] - out[b]
    return out

# ------------------------------------------------------------------- palette
# One vibrant blue family: the cohort is the deepest, each abstract takes a tone,
# and comparison arms recede. Matches assets/site.css and the figure PNGs.
P = {
    "ink":   "#1b2a3c",
    "mut":   "#5c7083",
    "line":  "#b9c5d0",
    "arrow": "#8fa2b5",
    "black": "#24374f",   # the cohort itself - deep navy
    "teal":  "#3e5773",   # first family
    "plum":  "#5a7694",   # second family
    "slate": "#9bacbd",   # comparison arms
    "band":  "#eef1f4",
    "bandbd": "#cfd8e1",
}
TINT = {"teal": "#e8edf3", "plum": "#edf1f5", "slate": "#f3f5f8", "black": "#e9ecef"}
SERIF = "Iowan Old Style,Palatino Linotype,Palatino,Georgia,serif"
SANS = "-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif"

def esc(s): return html.escape(str(s), quote=True)

def fmt(v):
    return "—" if v is None else format(int(v), ",")

# --------------------------------------------------------------- the panels
# Schematic, like the ADT figure: the workbook holds one query per stratum per
# cohort, not a count for every cell of the cross, so drawing numbers inside the
# panels would either invent them or imply the single pair that exists applies
# to every branch. Structure only; the counts live in the spine.

BW, TG, RG = 244, 66, 17

SUB_MAX = 46          # characters that fit the 244px box at 11.5px

class Bx(object):
    def __init__(s, label, tone, sub=None, solid=True):
        if sub and len(sub) > SUB_MAX:
            raise ValueError("sub line too long for the box: %r" % sub)
        s.label, s.tone, s.sub, s.solid = label, tone, sub, solid
        s.h = 70 if sub else 50
        s.x = s.y = 0.0

def draw_bx(b, out):
    fill = P[b.tone] if b.solid else TINT[b.tone]
    tc = "#ffffff" if b.solid else P["ink"]
    sc = "rgba(255,255,255,.80)" if b.solid else P["mut"]
    bd = "" if b.solid else ' stroke="%s" stroke-width="1.1"' % P[b.tone]
    out.append('<rect x="%.1f" y="%.1f" width="%d" height="%.1f" rx="6" fill="%s"%s/>'
               % (b.x, b.y, BW, b.h, fill, bd))
    cx = b.x + BW / 2.0
    out.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="%s" font-size="15" '
               'font-weight="700" fill="%s">%s</text>'
               % (cx, b.y + (26 if b.sub else 31), SERIF, tc, esc(b.label)))
    if b.sub:
        out.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="%s" font-size="11.5" '
                   'fill="%s">%s</text>' % (cx, b.y + 48, SANS, sc, esc(b.sub)))

def bus(srcs, tgts, out):
    """One rail between two tiers: each source joins it, each target leaves it."""
    rail = srcs[0].x + BW + TG / 2.0
    ys = [b.y + b.h / 2.0 for b in srcs + tgts]
    out.append('<path d="M%.1f %.1f V%.1f" fill="none" stroke="%s" stroke-width="1.4"/>'
               % (rail, min(ys), max(ys), P["arrow"]))
    for b in srcs:
        out.append('<path d="M%.1f %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.4"/>'
                   % (b.x + BW, b.y + b.h / 2.0, rail, P["arrow"]))
    for b in tgts:
        out.append('<path d="M%.1f %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.4" '
                   'marker-end="url(#ah)"/>' % (rail, b.y + b.h / 2.0, b.x - 9, P["arrow"]))

def panels():
    trend = [
        [Bx("Incident use", "black", "no prior vaginal estrogen"),
         Bx("Prevalent use", "black", "washout omitted")],
        [Bx("Monthly rate per 10,000", "teal", "39 months, Jan 2023 – Mar 2026"),
         Bx("Control drugs", "teal", "one positive, three negative"),
         Bx("Formulation", "slate", "ring · tablet/insert · cream")],
        [Bx("Level and slope at Nov 2025", "teal", "segmented, one harmonic", solid=False),
         Bx("Calibrated slope change", "teal", "against the three controls", solid=False),
         Bx("Share of classified starts", "slate", "ring is the only relabeled product", solid=False)],
    ]
    breast = [
        [Bx("Breast-cancer history", "black", "Z85.3"),
         Bx("History or active disease", "black", "Z85.3 or C50"),
         Bx("No breast-cancer code", "slate")],
        [Bx("ER-positive", "plum", "Z17.0"),
         Bx("ER-negative", "plum", "Z17.1"),
         Bx("Receptor not coded", "slate")],
        [Bx("Initiation rate and rate ratio", "plum", solid=False),
         Bx("Coded symptom burden", "plum", "prevalence ratio among initiators", solid=False),
         Bx("Prasterone or ospemifene", "slate", "non-estrogen alternative", solid=False)],
    ]
    reach = [
        [Bx("Women starting in each window", "black")],
        [Bx("Recorded race", "teal", "applied to the cohort's patient count"),
         Bx("Recorded ethnicity", "teal", "a separate axis")],
        [Bx("Rate per 10,000 within each group", "teal", solid=False),
         Bx("Rate ratio vs White women", "slate", "Hispanic vs non-Hispanic", solid=False),
         Bx("Absolute difference per 10,000", "teal", "the measure that moved", solid=False)],
    ]
    return trend, breast, reach

# ------------------------------------------------- the derivation spine
SPINE = [
    {"key": None, "label": "TriNetX US Collaborative Network", "network": True},
    {"key": "incare", "label": "Women aged 40–90 in active care",
     "crit": "diagnosis or outpatient E&M code in the same months a year earlier",
     "sens": ("COMPARISON WINDOW", [("Nov 24 – Mar 25", "incare24"),
                                    ("Nov 25 – Mar 26", "incare")])},
    {"key": "inc", "label": "Started vaginal estrogen", "anchor": True,
     "crit": "RxNorm 4083 vaginal, none on or before the preceding 31 Oct",
     "sens": ("COMPARISON WINDOW", [("Nov 24 – Mar 25", "inc24"),
                                    ("Nov 25 – Mar 26", "inc")])},
    {"key": "prev", "label": "Continued vaginal estrogen", "anchor": True,
     "crit": "washout omitted — any record in the window",
     "sens": ("DENOMINATOR", [("Women in care", "prevden")])},
]
SPW, SPH, SPG = 338, 78, 30
CH, CG, CW, COL2 = 22, 7, 190, 91
PAD = 44

def _lay(tiers, x0, top):
    hs = [sum(b.h for b in t) + RG * (len(t) - 1) for t in tiers]
    H = max(hs)
    for i, t in enumerate(tiers):
        y = top + (H - hs[i]) / 2.0
        for b in t:
            b.x = x0 + i * (BW + TG); b.y = y; y += b.h + RG
    return H

BANDS = [("A.  Prescribing trend, control drugs and formulation", "trend"),
         ("B.  Breast cancer, receptor status, and what is prescribed instead", "breast"),
         ("C.  Who the post-announcement rise reached", "reach")]

def build(vals, network=None, hcos=None, snapshot=None):
    trend, breast, reach = panels()
    tiersets = [trend, breast, reach]
    C1X = PAD
    C2X = C1X + CW + 28
    C3X = C2X + SPW + 70
    HEAD, BANDH = 142, 36

    tops, heights = [], []
    y = HEAD
    for ts in tiersets:
        tops.append(y)
        h = _lay(ts, C3X, y + BANDH + 18)
        heights.append(h)
        y += BANDH + 18 + h + 52
    pBot = y - 52

    spineH = len(SPINE) * (SPH + SPG) - SPG
    spineTop = max(HEAD, HEAD + (pBot - HEAD - spineH) / 2.0)
    bottom = max(pBot, spineTop + spineH)
    width = C3X + 3 * (BW + TG) - TG + PAD
    height = bottom + 104

    out = []; A = out.append
    A('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" class="pcafig" '
      'font-family="%s" role="img" aria-label="Cohort and query derivation">' % (width, height, SANS))
    A('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
      'markerHeight="7" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="%s"/>'
      '</marker></defs>' % P["arrow"])
    A('<rect width="100%" height="100%" fill="#ffffff"/>')
    A('<text x="%d" y="54" font-family="%s" font-size="28" font-weight="800" fill="%s">'
      'Cohort and query derivation</text>' % (PAD, SERIF, P["ink"]))
    A('<text x="%d" y="78" font-size="12.5" fill="%s">Women aged 40–90 in active care · '
      'TriNetX US Collaborative Network%s</text>'
      % (PAD, P["mut"], (" · %s health-care organisations" % esc(hcos)) if hcos else ""))
    A('<text x="%d" y="97" font-size="11" fill="%s">%s; the window the spine counts is shown '
      'at left. Each panel is schematic: it shows which strata the cohort is carried through, '
      'not a count per branch.</text>'
      % (PAD, P["mut"], esc(snapshot or "Windows Nov 2024 – Mar 2025 and Nov 2025 – Mar 2026")))
    for x, t in ((C1X, "WINDOWS"), (C2X, "COHORT CONSTRUCTION")):
        A('<text x="%d" y="%d" font-size="9.5" font-weight="700" fill="%s" '
          'letter-spacing=".10em">%s</text>' % (x, HEAD - 10, P["mut"], t))

    bw = width - C3X - PAD
    for (title, _), top in zip(BANDS, tops):
        A('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s"/>'
          % (C3X, top, bw, BANDH, P["band"], P["bandbd"]))
        A('<text x="%.1f" y="%d" text-anchor="middle" font-family="%s" font-size="15" '
          'font-weight="700" fill="%s">%s</text>'
          % (C3X + bw / 2.0, top + 23, SERIF, P["ink"], esc(title)))

    rows = []; y = spineTop
    for i, st in enumerate(SPINE):
        solid = st.get("anchor") or st.get("network")
        fill = P["black"] if solid else "#ffffff"
        tc = "#ffffff" if solid else P["ink"]
        sub = "rgba(255,255,255,.92)" if solid else P["ink"]
        bd = "" if solid else ' stroke="%s" stroke-width="1.3"' % P["ink"]
        A('<rect x="%d" y="%.1f" width="%d" height="%d" rx="6" fill="%s"%s/>'
          % (C2X, y, SPW, SPH, fill, bd))
        cx = C2X + SPW / 2.0
        A('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="%s" font-size="14" '
          'font-weight="700" fill="%s">%s</text>' % (cx, y + 24, SERIF, tc, esc(st["label"])))
        if st.get("crit"):
            cc = "rgba(255,255,255,.70)" if solid else P["mut"]
            A('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" fill="%s">%s</text>'
              % (cx, y + 41, cc, esc(st["crit"])))
        val = fmt(network) if st.get("network") else fmt(vals.get(st["key"]))
        qk = "_network" if st.get("network") else st["key"]
        A('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="16" font-weight="800" '
          'fill="%s" data-q="%s">n = %s</text>' % (cx, y + 64, sub, esc(qk), val))
        if i < len(SPINE) - 1:
            A('<path d="M%.1f %.1f V%.1f" fill="none" stroke="%s" stroke-width="1.6" '
              'marker-end="url(#ah)"/>' % (cx, y + SPH, y + SPH + SPG - 2, P["arrow"]))
        rows.append((st, y)); y += SPH + SPG

    for st, ry in rows:
        s = st.get("sens")
        if not s:
            continue
        title, pairs = s
        gh = 19 + len(pairs) * CH + (len(pairs) - 1) * CG
        gy = ry + SPH / 2.0 - gh / 2.0
        A('<text x="%.1f" y="%.1f" font-size="9" font-weight="700" fill="%s" text-anchor="end" '
          'letter-spacing=".07em">%s</text>' % (C1X + CW, gy + 8, P["mut"], esc(title)))
        cy = gy + 19
        for lab, k in pairs:
            A('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="4" fill="#f3f5f8" '
              'stroke="#dbe2ea"/>' % (C1X, cy, CW, CH))
            A('<text x="%.1f" y="%.1f" font-size="10.5" fill="%s">%s</text>'
              % (C1X + 8, cy + 15, P["mut"], esc(lab)))
            A('<text x="%.1f" y="%.1f" font-size="10.5" font-weight="700" fill="%s" '
              'text-anchor="end" data-q="%s">%s</text>'
              % (C1X + CW - 8, cy + 15, P["ink"], esc(k), fmt(vals.get(k))))
            cy += CH + CG
        A('<path d="M%d %.1f H%d" fill="none" stroke="%s" stroke-width="1.1" '
          'stroke-dasharray="3 3"/>' % (C1X + CW + 8, ry + SPH / 2.0, C2X - 5, P["line"]))

    sy = [ry for st, ry in rows if st["key"] == "inc"][0] + SPH / 2.0
    for ts in tiersets:
        ys = [b.y + b.h / 2.0 for b in ts[0]]
        rail = C2X + SPW + 26
        A('<path d="M%d %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.6"/>'
          % (C2X + SPW, sy, rail, P["arrow"]))
        A('<path d="M%.1f %.1f V%.1f" fill="none" stroke="%s" stroke-width="1.6"/>'
          % (rail, min(min(ys), sy), max(max(ys), sy), P["arrow"]))
        for b in ts[0]:
            A('<path d="M%.1f %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.5" '
              'marker-end="url(#ah)"/>' % (rail, b.y + b.h / 2.0, b.x - 9, P["arrow"]))

    # A and C are full crosses; in B only women with a breast-cancer code are
    # split by receptor status, so the second rail starts from those two boxes.
    bus(trend[0], trend[1], out);   bus(trend[1], trend[2], out)
    bus(breast[0][:2], breast[1], out); bus(breast[1], breast[2], out)
    bus(reach[0], reach[1], out);   bus(reach[1], reach[2], out)
    for ts in tiersets:
        for t in ts:
            for b in t:
                draw_bx(b, out)

    ky = bottom + 44
    A('<path d="M%d %.1f H%d" fill="none" stroke="%s" stroke-width="1"/>'
      % (PAD, ky - 20, width - PAD, P["line"]))
    kx = PAD
    for tone, lab in (("black", "Whole cohort"), ("teal", "Trend and reach"),
                      ("plum", "Breast cancer"), ("slate", "Comparison arm")):
        A('<rect x="%.1f" y="%.1f" width="13" height="13" rx="3" fill="%s"/>'
          % (kx, ky - 10, P[tone]))
        A('<text x="%.1f" y="%.1f" font-size="10.5" fill="%s">%s</text>'
          % (kx + 19, ky, P["mut"], esc(lab)))
        kx += 26 + len(lab) * 6.0 + 26
    A('<text x="%d" y="%.1f" text-anchor="end" font-size="10" fill="%s">Counts from the VE '
      'master workbook (QM sheet); every rate on this page shares this denominator.</text>'
      % (width - PAD, ky, P["mut"]))
    A('</svg>')
    return "".join(out)


# ------------------------------------------------------- reading the workbook
# The VE master sheet answers this endpoint without sign-in, which is what lets
# the page refresh itself in the browser. The build reads the same endpoint and
# bakes the answer in, so the page is correct before a single byte of JS runs —
# and still correct if Google is unreachable. A cache on disk means a failed
# fetch degrades to the last known-good numbers instead of publishing blanks.
SHEET_ID = "1Cy64AGkUWwHMHl3a-F2AhOxZOmTl-iOJMsmy5FA85L8"
GVIZ = ("https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=QM"
        % SHEET_ID)

def parse_qm(csv_text):
    """QM is Query Name | Count | HCOs for that query | . | Network Patients | 'n of m'."""
    import csv, io as _io
    qm, network, hcos = {}, None, None
    for row in csv.reader(_io.StringIO(csv_text)):
        if len(row) < 2:
            continue
        name = (row[0] or "").strip()
        raw = (row[1] or "").replace(",", "").strip()
        try:
            n = int(float(raw))
        except ValueError:
            n = None
        if name and n is not None and name not in qm:
            qm[name] = n
        # The network size and HCO total repeat on every row; take the first that
        # carries both, and never let a later blank overwrite them.
        if network is None and len(row) > 4:
            net = (row[4] or "").replace(",", "").strip()
            try: network = int(float(net))
            except ValueError: pass
        if hcos is None and len(row) > 5 and " of " in (row[5] or ""):
            hcos = row[5].strip()
    return qm, network, hcos


def load(cache_path, fetch=True, timeout=20):
    """(values, network, hcos, source). Never raises; falls back to the cache."""
    import json, os, urllib.request
    qm = network = hcos = None
    source = "cache"
    if fetch:
        try:
            req = urllib.request.Request(GVIZ, headers={"User-Agent": "henryblair.online build"})
            txt = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")
            qm, network, hcos = parse_qm(txt)
            if not qm.get(SOURCES["inc"]):
                qm = None               # got something, but not the sheet we expect
            else:
                source = "sheet"
        except Exception:
            qm = None
    if qm is None and os.path.exists(cache_path):
        c = json.load(open(cache_path, encoding="utf-8"))
        qm, network, hcos = c.get("qm", {}), c.get("network"), c.get("hcos")
    if qm is None:
        return None, None, None, "unavailable"
    if source == "sheet":
        keep = {v for v in SOURCES.values() if isinstance(v, str)}
        slim = {k: v for k, v in qm.items() if k in keep}
        tmp = cache_path + ".tmp"
        d = os.path.dirname(cache_path)
        if d:
            os.makedirs(d, exist_ok=True)
        json.dump({"qm": slim, "network": network, "hcos": hcos},
                  open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(tmp, cache_path)
    return resolve(qm), network, hcos, source


def live_js():
    """Browser-side refresh. The key->query map is written from SOURCES here, so
    the page and the build can never disagree about what a number means.

    Baked values are already correct when this runs; it only overwrites a number
    when it parses cleanly and actually differs, so a failed or partial fetch
    leaves the figure exactly as it shipped."""
    import json
    mapping = {k: (list(v) if isinstance(v, tuple) else v) for k, v in SOURCES.items()}
    return """/* Refreshes the VE cohort figure from the VE master sheet.
   Generated by ve_figure.py — do not edit by hand. */
(function () {
  "use strict";
  var MAP = %s;
  var URL_ = %s;
  var root = document.getElementById("vefig");
  if (!root || !root.querySelector("[data-q]")) return;

  function cells(line) {                       // one CSV row -> array of fields
    var out = [], cur = "", q = false, i, c;
    for (i = 0; i < line.length; i++) {
      c = line[i];
      if (q) {
        if (c === '"') { if (line[i + 1] === '"') { cur += '"'; i++; } else q = false; }
        else cur += c;
      } else if (c === '"') q = true;
      else if (c === ",") { out.push(cur); cur = ""; }
      else cur += c;
    }
    out.push(cur);
    return out;
  }

  function num(s) {
    var n = parseFloat(String(s == null ? "" : s).replace(/,/g, "").trim());
    return isFinite(n) ? Math.round(n) : null;
  }

  fetch(URL_, { credentials: "omit" })
    .then(function (r) { if (!r.ok) throw 0; return r.text(); })
    .then(function (txt) {
      var qm = {}, network = null, hcos = null;
      txt.split(/\\r?\\n/).forEach(function (line) {
        if (!line) return;
        var f = cells(line), name = (f[0] || "").trim(), n = num(f[1]);
        if (name && n !== null && !(name in qm)) qm[name] = n;
        if (network === null && f.length > 4) { var v = num(f[4]); if (v) network = v; }
        if (hcos === null && f.length > 5 && f[5].indexOf(" of ") > -1) hcos = f[5].trim();
      });
      if (qm[MAP.inc] == null) return;         // not the sheet we expect; keep baked values

      var vals = {}, k, src;
      for (k in MAP) { src = MAP[k]; if (typeof src === "string") vals[k] = qm[src]; }
      for (k in MAP) {
        src = MAP[k];
        if (src instanceof Array) {
          var a = vals[src[1]], b = vals[src[2]];
          vals[k] = (a == null || b == null) ? null : a - b;
        }
      }

      root.querySelectorAll("[data-q]").forEach(function (el) {
        var key = el.getAttribute("data-q");
        if (key === "_network") {
          if (network) {
            var sN = "n = " + network.toLocaleString("en-US");
            if (sN !== el.textContent) el.textContent = sN;
          }
          return;
        }
        var v = vals[key];
        if (v == null) return;
        var s2 = (el.getAttribute("data-bare") === "1" ? "" : "n = ")
                 + v.toLocaleString("en-US");
        if (s2 !== el.textContent) el.textContent = s2;
      });
    })
    .catch(function () { /* keep the baked numbers */ });
})();
""" % (json.dumps(mapping, ensure_ascii=False, sort_keys=True), json.dumps(GVIZ))


MARK_A, MARK_B = "<!--VEFIG-->", "<!--/VEFIG-->"

def block(vals, network=None, hcos=None, snapshot=None, source="sheet"):
    """The whole figure section: intro sentence, the diagram, and a provenance line."""
    where = {"sheet": "read from the master workbook at build time, and re-read in your "
                      "browser when this page loads",
             "cache": "last known-good values — the workbook was unreachable at build time",
             }.get(source, "")
    return "".join([
        MARK_A,
        '\n  <p class="secintro">Three abstracts come out of one query tree. The cohort is '
        'reached from the network one criterion at a time, and each band below is one of the '
        'three: how the trend was measured, how the breast-cancer strata were built, and how '
        'the composition of the rise was recovered.</p>\n  ',
        '<div class="diagramwrap" id="vefig">', build(vals, network, hcos, snapshot),
        '</div>\n  ',
        '<p class="tblnote"><b>Figure 1.</b> Cohort and query derivation. Every count in the '
        'spine is addressed by its query name in the VE master workbook, never typed in — %s. '
        'Dark boxes are cohorts, solid colour marks the query families run against them, and '
        'outlined boxes are the quantities each family produces.</p>\n  ' % where,
        '<script src="/assets/ve-live.js" defer></script>\n  ',
        MARK_B,
    ])
