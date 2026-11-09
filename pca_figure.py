# -*- coding: utf-8 -*-
"""Cohort-derivation figure for the ADT project page.

Every count is addressed by its query name in the PCa master workbook's QM
sheet, never typed in here, so the figure cannot drift from the data. Four
nodes are differences rather than named queries; they are written as
expressions and evaluated the same way.
"""
import html

# ---------------------------------------------------------------- the numbers
# key -> QM query name, or ("-", a, b) for a difference
SOURCES = {
    "iadt":        "PCa ∩ ADT Union 2x ∩ Washout ∩ ADT Washout_new (IADT)",
    "cx1":         "Cx-01y_new",
    "cxnever":     "Cx-Never_new",
    "nocx1":       ("-", "iadt", "cx1"),
    "rx2a":        "Rx-2a-05y_new",
    "rx2aden":     "Rx-2a-denom_new",
    "fx2a":        "Fx-2a-05y_new",
    "fx2aden":     "Fx-2a-denom_new",
    "siadt":       "v1_SIADT_new",
    "sep":         "v1 ∩ E+_new",
    "sem":         "v1 ∩ E-_new",
    "scx1":        "v1 ∩ Cx-01y_new",
    "scxnever":    "v1 ∩ Cx-Never_new",
    "snocx1":      ("-", "siadt", "scx1"),
    "mets":        "2017-23: Mets_new",
    "notmets":     ("-", "iadt", "mets"),
    "visc":        "2017-23: Visceral_new",
    "notvisc":     "2017-23: Not Visceral_new",
    "iv":          "2017-23: Intensified ∩ Visceral_new",
    "inv":         "2017-23: Intensified ∩ Not Visceral_new",
    "nv":          ("-", "visc", "iv"),
    "nnv":         ("-", "notvisc", "inv"),
    "inten":       "2017-23: Intensified_new",
    "notinten":    "2017-23: Not Intensified_new",
    "arpi":        "2017-23: ARPI_new",
    "doce":        "2017-23: Docetaxel_new",
    "trip":        "2017-23: Triple Therapy_new",
    "abi":         "2017-23: Abiraterone_new",
    "daro":        "2017-23: Darolutamide_new",
    "enza":        "2017-23: Enzalutamide_new",
    "apa":         "2017-23: Apalutamide_new",
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

SPINE_SOURCES = {
    "pca":      "PCa_new",
    "adt1":     "PCa ∩ ADT Union ∩ No Washout_new",
    "adt1wo":   "PCa ∩ ADT Union ∩ Washout_new",
    "adt1awo":  "PCa ∩ ADT Union ∩ Washout ∩ ADT Washout_new",
    "adt2":     "PCa ∩ ADT Union 2x ∩ No Washout_new",
    "adt2wo":   "PCa ∩ ADT Union 2x ∩ Washout_new (IADT_old)",
    "dx70v1":   "PCa_Dx_at_70_v1_new2",
    "dx70v2":   "PCa_Dx_at_70_v2_new2",
    "dx70v3":   "PCa_Dx_at_70_v3_new2",
    "dx70v4":   "PCa_Dx_at_70_v4_new2",
    "siadt2":   "v2_SIADT_new",
    "a2_1523":  "supp_2015-23: ADT Union 2x ∩ No Washout_new",
    "a2_1623":  "supp_2016-23: ADT Union 2x ∩ No Washout_new",
    "a2_1823":  "supp_2018-23: ADT Union 2x ∩ No Washout_new",
    "a2_1824":  "supp_2018-24: ADT Union 2x ∩ No Washout_new",
    "a2_1925":  "supp_2019-25: ADT Union 2x ∩ No Washout_new",
    "aw_1523":  "supp_2015-23: ADT Union 2x ∩ Washout_new",
    "aw_1623":  "supp_2016-23: ADT Union 2x ∩ Washout_new",
    "aw_1823":  "supp_2018-23: ADT Union 2x ∩ Washout_new",
    "aw_1824":  "supp_2018-24: ADT Union 2x ∩ Washout_new",
    "aw_1925":  "supp_2019-25: ADT Union 2x ∩ Washout_new",
    "ia_1523":  "supp_2015-23: ADT Union 2x ∩ Washout ∩ ADT Washout_new",
    "ia_1623":  "supp_2016-23: ADT Union 2x ∩ ADT Washout ∩ Washout_new",
    "ia_1823":  "supp_2018-23: ADT Union 2x ∩ ADT Washout ∩ Washout_new",
    "ia_1824":  "supp_2018-24: ADT Union 2x ∩ ADT Washout ∩ Washout_new",
    "ia_1925":  "supp_2019-25: ADT Union 2x ∩ ADT Washout ∩ Washout_new",
}
SOURCES.update(SPINE_SOURCES)

# ------------------------------------------------------------------- palette
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
# The spine carries the counts. The two panels are deliberately schematic: the
# workbook holds one query per stratum per cohort, not a count for every cell of
# the cross, so drawing numbers here would either invent them or imply that the
# single pair that does exist applies to every branch. Structure only.

BW, TG, RG = 244, 66, 17

class Bx(object):
    def __init__(s, label, tone, sub=None, solid=True):
        s.label, s.tone, s.sub, s.solid = label, tone, sub, solid
        s.h = 70 if sub else 50
        s.x = s.y = 0.0

def draw_bx(b, out):
    fill = P[b.tone] if b.solid else TINT[b.tone]
    tc = "#ffffff" if b.solid else P["ink"]
    sc = "rgba(255,255,255,.78)" if b.solid else P["mut"]
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
    bone = [
        [Bx("Incident ADT", "black"), Bx("Sustained ADT", "black"),
         Bx("In-care", "black"), Bx("Sustained ADT and in-care", "black")],
        [Bx("Promptly screened", "teal", "central DXA ≤1 y"),
         Bx("Not promptly screened", "slate"),
         Bx("Never screened", "slate"),
         Bx("Pre-existing bone disease", "teal"),
         Bx("No pre-existing bone disease", "slate")],
        [Bx("Antiresorptive initiator", "teal", "≤5 y · no prior Rx or bone mets", solid=False),
         Bx("Fragility fracture", "teal", "≤5 y · no prior fracture or bone mets", solid=False)],
    ]
    mets = [
        [Bx("Metastatic", "black"), Bx("Not metastatic", "slate")],
        [Bx("Visceral", "plum"), Bx("Not visceral", "plum")],
        [Bx("Intensified", "plum"), Bx("Not intensified", "slate")],
        [Bx("ARPI", "plum", "abiraterone · apalutamide", solid=False),
         Bx("Docetaxel", "plum", solid=False),
         Bx("Triple therapy", "plum", solid=False)],
    ]
    return bone, mets

# ------------------------------------------------- the derivation spine
def _win(keys):
    labels = ["2015–23", "2019–25"]
    return list(zip(labels, keys))

SPINE = [
    {"key": None, "label": "TriNetX US Collaborative Network", "network": True},
    {"key": "pca", "label": "Prostate cancer",
     "crit": "ICD-10 C61, age ≥70, ≥2 instances",
     "sens": ("AGE-AT-DIAGNOSIS DEFINITION",
              [("v1", "dx70v1"), ("v2", "dx70v2"), ("v3", "dx70v3"), ("v4", "dx70v4")])},
    {"key": "adt1", "label": "+ ADT", "crit": "ADT Union, Jan 2017 – Dec 2023",
     "sens": ("ADT 2× APPLIED HERE · INDEX WINDOW", _win(["a2_1523", "a2_1925"]))},
    {"key": "adt1wo", "label": "+ washout", "crit": "no ADT on or before Dec 31, 2016",
     "sens": ("ADT 2× APPLIED HERE · INDEX WINDOW", _win(["aw_1523", "aw_1925"]))},
    {"key": "adt1awo", "label": "+ ADT washout", "crit": "69_ADT_Wash"},
    {"key": "iadt", "label": "Incident ADT — + ADT 2×", "anchor": True,
     "crit": "ADT Union carries ≥2 instances",
     "sens": ("INDEX WINDOW", _win(["ia_1523", "ia_1925"]))},
    {"key": "siadt", "label": "Sustained ADT", "crit": "v1_SIADT", "anchor": True},
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

def build(vals, network=None, hcos=None, snapshot=None):
    bone, mets = panels()
    C1X = PAD
    C2X = C1X + CW + 28
    C3X = C2X + SPW + 70
    HEAD, BANDH = 142, 36

    aTop = HEAD + BANDH + 18
    hA = _lay(bone, C3X, aTop)
    bTop = aTop + hA + 52
    hB = _lay(mets, C3X, bTop + BANDH + 18)

    spineH = len(SPINE) * (SPH + SPG) - SPG
    pBot = bTop + BANDH + 18 + hB
    spineTop = max(HEAD, HEAD + (pBot - HEAD - spineH) / 2.0)
    bottom = max(pBot, spineTop + spineH)
    width = C3X + 4 * (BW + TG) - TG + PAD
    height = bottom + 104

    out = []; A = out.append
    A('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" class="pcafig" '
      'font-family="%s" role="img" aria-label="Cohort derivation">' % (width, height, SANS))
    A('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
      'markerHeight="7" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 z" fill="%s"/>'
      '</marker></defs>' % P["arrow"])
    A('<rect width="100%" height="100%" fill="#ffffff"/>')
    A('<text x="%d" y="54" font-family="%s" font-size="28" font-weight="800" fill="%s">'
      'Cohort derivation</text>' % (PAD, SERIF, P["ink"]))
    A('<text x="%d" y="78" font-size="12.5" fill="%s">Men ≥70 initiating ADT for prostate '
      'cancer · TriNetX US Collaborative Network%s</text>'
      % (PAD, P["mut"], (" · %s health-care organisations" % esc(hcos)) if hcos else ""))
    A('<text x="%d" y="97" font-size="11" fill="%s">%s; sensitivity windows at left. The two '
      'panels are schematic: every cohort is carried through every stratum.</text>'
      % (PAD, P["mut"], esc(snapshot or "Index window Jan 2017 – Dec 2023")))
    for x, t in ((C1X, "SENSITIVITIES"), (C2X, "COHORT CONSTRUCTION")):
        A('<text x="%d" y="%d" font-size="9.5" font-weight="700" fill="%s" '
          'letter-spacing=".10em">%s</text>' % (x, HEAD - 10, P["mut"], t))

    bw = width - C3X - PAD
    for top, title in ((HEAD, "Bone-density screening &amp; bone health"),
                       (bTop, "Metastatic disease &amp; treatment intensification")):
        A('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s"/>'
          % (C3X, top, bw, BANDH, P["band"], P["bandbd"]))
        A('<text x="%.1f" y="%d" text-anchor="middle" font-family="%s" font-size="15" '
          'font-weight="700" fill="%s">%s</text>'
          % (C3X + bw / 2.0, top + 23, SERIF, P["ink"], title))

    rows = []; y = spineTop
    for i, st in enumerate(SPINE):
        solid = st.get("anchor") or st.get("network")
        fill = P["black"] if solid else "#ffffff"
        tc = "#ffffff" if solid else P["ink"]
        sub = "rgba(255,255,255,.90)" if solid else P["ink"]
        bd = "" if solid else ' stroke="%s" stroke-width="1.3"' % P["ink"]
        A('<rect x="%d" y="%.1f" width="%d" height="%d" rx="6" fill="%s"%s/>'
          % (C2X, y, SPW, SPH, fill, bd))
        cx = C2X + SPW / 2.0
        A('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="%s" font-size="14" '
          'font-weight="700" fill="%s">%s</text>' % (cx, y + 24, SERIF, tc, esc(st["label"])))
        if st.get("crit"):
            cc = "rgba(255,255,255,.66)" if solid else P["mut"]
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
        two = len(pairs) == 4
        rn = (len(pairs) + 1) // 2 if two else len(pairs)
        gh = 19 + rn * CH + (rn - 1) * CG
        gy = ry + SPH / 2.0 - gh / 2.0
        A('<text x="%.1f" y="%.1f" font-size="9" font-weight="700" fill="%s" text-anchor="end" '
          'letter-spacing=".07em">%s</text>' % (C1X + CW, gy + 8, P["mut"], esc(title)))

        def chip(cx, cy, cw, lab, k):
            A('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="4" fill="#f3f5f8" '
              'stroke="#dbe2ea"/>' % (cx, cy, cw, CH))
            A('<text x="%.1f" y="%.1f" font-size="10.5" fill="%s">%s</text>'
              % (cx + 8, cy + 15, P["mut"], esc(lab)))
            A('<text x="%.1f" y="%.1f" font-size="10.5" font-weight="700" fill="%s" '
              'text-anchor="end" data-q="%s">%s</text>'
              % (cx + cw - 8, cy + 15, P["ink"], esc(k), fmt(vals.get(k))))

        cy = gy + 19
        if two:
            gap = CW - 2 * COL2
            for i in range(0, len(pairs), 2):
                for j, (lab, k) in enumerate(pairs[i:i + 2]):
                    chip(C1X + j * (COL2 + gap), cy, COL2, lab, k)
                cy += CH + CG
        else:
            for lab, k in pairs:
                chip(C1X, cy, CW, lab, k); cy += CH + CG
        A('<path d="M%d %.1f H%d" fill="none" stroke="%s" stroke-width="1.1" '
          'stroke-dasharray="3 3"/>' % (C1X + CW + 8, ry + SPH / 2.0, C2X - 5, P["line"]))

    sy = [ry for st, ry in rows if st["key"] == "iadt"][0] + SPH / 2.0
    for tiers in (bone, mets):
        ys = [b.y + b.h / 2.0 for b in tiers[0]]
        rail = C2X + SPW + 26
        A('<path d="M%d %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.6"/>'
          % (C2X + SPW, sy, rail, P["arrow"]))
        A('<path d="M%.1f %.1f V%.1f" fill="none" stroke="%s" stroke-width="1.6"/>'
          % (rail, min(min(ys), sy), max(max(ys), sy), P["arrow"]))
        for b in tiers[0]:
            A('<path d="M%.1f %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.5" '
              'marker-end="url(#ah)"/>' % (rail, b.y + b.h / 2.0, b.x - 9, P["arrow"]))

    # bone health is a full cross; panel B is not — only metastatic men are split
    # by site, and only intensified men receive a drug.
    bus(bone[0], bone[1], out); bus(bone[1], bone[2], out)
    bus(mets[0][:1], mets[1], out); bus(mets[1], mets[2], out); bus(mets[2][:1], mets[3], out)
    for tiers in (bone, mets):
        for t in tiers:
            for b in t:
                draw_bx(b, out)

    ky = bottom + 44
    A('<path d="M%d %.1f H%d" fill="none" stroke="%s" stroke-width="1"/>'
      % (PAD, ky - 20, width - PAD, P["line"]))
    kx = PAD
    for tone, lab in (("black", "Whole cohort"), ("teal", "Bone health"),
                      ("plum", "Treatment intensification"), ("slate", "Comparison arm")):
        A('<rect x="%.1f" y="%.1f" width="13" height="13" rx="3" fill="%s"/>'
          % (kx, ky - 10, P[tone]))
        A('<text x="%.1f" y="%.1f" font-size="10.5" fill="%s">%s</text>'
          % (kx + 19, ky, P["mut"], esc(lab)))
        kx += 26 + len(lab) * 6.0 + 26
    A('<text x="%d" y="%.1f" text-anchor="end" font-size="10" fill="%s">Counts from the PCa '
      'master workbook (QM sheet); each stratum is estimated propensity-matched.</text>'
      % (width - PAD, ky, P["mut"]))
    A('</svg>')
    return "".join(out)


# ------------------------------------------------------- reading the workbook
# The PCa master sheet answers this endpoint without sign-in, which is what lets
# the page refresh itself in the browser. The build reads the same endpoint and
# bakes the answer in, so the page is correct before a single byte of JS runs —
# and still correct if Google is unreachable, or if the sheet is locked down
# later. A cache on disk means a failed fetch degrades to the last known-good
# numbers instead of publishing blanks.
SHEET_ID = "1r61VFTZoFx6jRbCFqB17m_67dbgG_cAGG5uO6r1OQIA"
GVIZ = ("https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=QM"
        % SHEET_ID)

def parse_qm(csv_text):
    """QM is Query Name | Query Count | HCO Count | Network Patients."""
    import csv, io as _io
    qm, network, hcos = {}, None, None
    for i, row in enumerate(csv.reader(_io.StringIO(csv_text))):
        if len(row) < 2:
            continue
        name = (row[0] or "").strip()
        raw  = (row[1] or "").replace(",", "").strip()
        try:
            n = int(float(raw))
        except ValueError:
            n = None
        if name and n is not None and name not in qm:
            qm[name] = n
        # The header rows carry the network size and HCO total. Merged cells make
        # the CSV columns differ from what a spreadsheet reader shows, so take
        # them from the first data row that actually has both.
        if network is None and len(row) > 3:
            net = (row[3] or "").replace(",", "").strip()
            try: network = int(float(net))
            except ValueError: pass
        if hcos is None and len(row) > 4 and " of " in (row[4] or ""):
            hcos = row[4].strip()
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
            if not qm.get(SOURCES["iadt"]):
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
    return """/* Refreshes the cohort figure from the PCa master sheet.
   Generated by pca_figure.py — do not edit by hand. */
(function () {
  "use strict";
  var MAP = %s;
  var URL_ = %s;
  if (!document.querySelector('[data-q]')) return;

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
        if (network === null && f.length > 3) { var v = num(f[3]); if (v) network = v; }
        if (hcos === null && f.length > 4 && f[4].indexOf(" of ") > -1) hcos = f[4].trim();
      });
      if (qm[MAP.iadt] == null) return;        // not the sheet we expect; keep baked values

      var vals = {}, k, src;
      for (k in MAP) { src = MAP[k]; if (typeof src === "string") vals[k] = qm[src]; }
      for (k in MAP) {
        src = MAP[k];
        if (src instanceof Array) {
          var a = vals[src[1]], b = vals[src[2]];
          vals[k] = (a == null || b == null) ? null : a - b;
        }
      }

      var changed = 0;
      document.querySelectorAll("[data-q]").forEach(function (el) {
        var key = el.getAttribute("data-q");
        if (key === "_network") {
          if (network) {
            var sN = "n = " + network.toLocaleString("en-US");
            if (sN !== el.textContent) { el.textContent = sN; changed++; }
          }
          return;
        }
        if (key === "_meta") {
          var bits = [];
          if (network) bits.push(network.toLocaleString("en-US") + " patients");
          if (hcos) bits.push(hcos + " healthcare organisations");
          bits.push("index 2017\\u20132023");
          var s = bits.join(" \\u00b7 ");
          if (s !== el.textContent) { el.textContent = s; changed++; }
          return;
        }
        var v = vals[key];
        if (v == null) return;
        var denom = el.getAttribute("data-denom");
        var s2 = "n = " + v.toLocaleString("en-US");
        if (denom && vals[denom] != null) s2 += " of " + vals[denom].toLocaleString("en-US");
        if (s2 !== el.textContent) { el.textContent = s2; changed++; }
      });
    })
    .catch(function () { /* keep the baked numbers */ });
})();
""" % (json.dumps(mapping, ensure_ascii=False, sort_keys=True), json.dumps(GVIZ))


MARK_A, MARK_B = "<!--PCAFIG-->", "<!--/PCAFIG-->"

def block(vals, network=None, hcos=None, snapshot="index 2017–2023", source="sheet"):
    """The whole figure section: intro sentence, the diagram, and a provenance line."""
    closes = ("Each panel is schematic: it shows which strata the cohort is carried "
              "through, not a count per branch.")
    where = {"sheet": "read from the master workbook at build time",
             "cache": "last known-good values — the workbook was unreachable at build time",
             }.get(source, "")
    return "".join([
        MARK_A,
        '\n   <p class="secintro">The cohort is reached from the network one criterion '
        'at a time. %s</p>\n   ' % closes,
        '<div class="diagramwrap">', build(vals, network, hcos, snapshot), '</div>\n   ',
        '<p id="pcafig-note" class="fignote">Every count in the spine is addressed by its '
        'query name in the PCa master workbook, never typed in — %s.</p>\n   ' % where,
        '<script src="/assets/pca-live.js" defer></script>\n   ',
        MARK_B,
    ])
