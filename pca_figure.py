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

# ------------------------------------------------------------------- palette
P = {
    "ink":    "#16202b",
    "mut":    "#5e6b78",
    "line":   "#c3ccd4",
    "navy":   "#13335a",   # the anchor cohort
    "blue":   "#2a6f97",   # key cohort
    "teal":   "#1b7f79",   # bone branch
    "amber":  "#a85d00",   # metastatic branch
    "plum":   "#7a4a8f",   # intensification
    "slate":  "#64748b",   # comparison / "not" arms
    "bandA":  "#eaf3f4",
    "bandB":  "#fbf0e4",
}
TINT = {"teal": "#e4f1f0", "amber": "#fbeada", "plum": "#f0e8f4",
        "blue": "#e3eef5", "slate": "#eceff2"}

# --------------------------------------------------------------- tree layout
class N:
    def __init__(self, key, label, tone="blue", solid=False, denom=None, kids=None):
        self.key, self.label, self.tone, self.solid = key, label, tone, solid
        self.denom = denom
        self.kids = kids or []
        self.w = 0; self.x = 0.0; self.y = 0

BOX_H, V_GAP, H_GAP = 62, 72, 14

def measure(n, chw):
    """Width of a node's subtree in layout units."""
    if not n.kids:
        n.span = chw
        return n.span
    n.span = sum(measure(k, chw) for k in n.kids) + H_GAP * (len(n.kids) - 1)
    n.span = max(n.span, chw)
    return n.span

def place(n, left, top, chw):
    n.y = top
    if not n.kids:
        n.x = left + (n.span - chw) / 2.0
        n.w = chw
        return
    cur = left
    for k in n.kids:
        place(k, cur, top + BOX_H + V_GAP, chw)
        cur += k.span + H_GAP
    first, last = n.kids[0], n.kids[-1]
    centre = (first.x + first.w / 2.0 + last.x + last.w / 2.0) / 2.0
    n.w = chw
    n.x = centre - chw / 2.0

def walk(n):
    yield n
    for k in n.kids:
        yield from walk(k)

# ------------------------------------------------------------------ the tree
def trees():
    bone = [
        N("cx1", "Central DXA ≤1 y", "teal", True, kids=[
            N("rx2a", "Antiresorptive initiator ≤5 y", "teal", denom="rx2aden"),
            N("fx2a", "Fragility fracture ≤5 y", "teal", denom="fx2aden"),
        ]),
        N("nocx1", "No central DXA ≤1 y", "slate"),
        N("cxnever", "Never central DXA", "slate"),
        N("siadt", "Sustained-ADT cohort", "teal", True, kids=[
            N("sep", "Pre-existing bone disease", "teal"),
            N("sem", "No pre-existing bone disease", "slate"),
            N("scx1", "Central DXA ≤1 y", "teal"),
            N("snocx1", "No central DXA ≤1 y", "slate"),
            N("scxnever", "Never central DXA", "slate"),
        ]),
    ]
    mets = [
        N("notmets", "Not metastatic ≤1 mo", "slate"),
        N("mets", "Metastatic", "amber", True, kids=[
            N("visc", "Visceral", "amber", kids=[
                N("iv", "Intensified", "plum"),
                N("nv", "Not intensified", "slate"),
            ]),
            N("notvisc", "Not visceral", "amber", kids=[
                N("inv", "Intensified", "plum"),
                N("nnv", "Not intensified", "slate"),
            ]),
            N("inten", "Intensified", "plum", True, kids=[
                N("arpi", "ARPI", "plum", kids=[
                    N("abi", "Abiraterone", "plum"),
                    N("daro", "Darolutamide", "plum"),
                    N("enza", "Enzalutamide", "plum"),
                    N("apa", "Apalutamide", "plum"),
                ]),
                N("doce", "Docetaxel", "plum"),
                N("trip", "Triple therapy", "plum"),
            ]),
            N("notinten", "Not intensified", "slate"),
        ]),
    ]
    return bone, mets

# -------------------------------------------------------------------- render
def esc(s): return html.escape(str(s), quote=True)

def fmt(v):
    return "—" if v is None else format(int(v), ",")

def box(n, vals):
    """One node. The number carries data-q so the page can refresh it live."""
    tone = n.tone
    fill = P[tone] if n.solid else TINT[tone]
    txt  = "#ffffff" if n.solid else P["ink"]
    sub  = "rgba(255,255,255,.80)" if n.solid else P["mut"]
    stroke = P[tone] if not n.solid else "none"
    sw = "" if n.solid else ' stroke="%s" stroke-width="1.2"' % stroke
    v = fmt(vals.get(n.key))
    if n.denom:
        v = "%s of %s" % (v, fmt(vals.get(n.denom)))
    cx = n.x + n.w / 2.0
    label = esc(n.label)
    # wrap long labels onto two lines at a sensible break
    words, lines, cur = label.split(" "), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > 25 and cur:
            lines.append(cur); cur = w
        else:
            cur = trial
    lines.append(cur)
    lines = lines[:2]
    ly = n.y + (23 if len(lines) == 1 else 18)
    out = ['<g class="nd">']
    out.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" rx="7" fill="%s"%s/>'
               % (n.x, n.y, n.w, BOX_H, fill, sw))
    for i, ln in enumerate(lines):
        out.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="12.5" '
                   'font-weight="700" fill="%s">%s</text>' % (cx, ly + i * 15, txt, ln))
    dn = ' data-denom="%s"' % esc(n.denom) if n.denom else ''
    out.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="14" '
               'font-weight="700" fill="%s" data-q="%s"%s>n = %s</text>'
               % (cx, n.y + BOX_H - 13, sub if n.solid else P[tone], esc(n.key), dn, esc(v)))
    out.append('</g>')
    return "".join(out)

def connect(parent_cx, parent_bottom, kids):
    """Orthogonal connectors: down, across the spine, down into each child."""
    if not kids:
        return ""
    mid = parent_bottom + V_GAP / 2
    xs = [k.x + k.w / 2.0 for k in kids]
    d = ['<path d="M%.1f %d V%.1f" fill="none" stroke="%s" stroke-width="1.3"/>'
         % (parent_cx, parent_bottom, mid, P["line"])]
    if len(kids) > 1:
        d.append('<path d="M%.1f %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.3"/>'
                 % (min(xs), mid, max(xs), P["line"]))
    for k in kids:
        d.append('<path d="M%.1f %.1f V%d" fill="none" stroke="%s" stroke-width="1.3"/>'
                 % (k.x + k.w / 2.0, mid, k.y, P["line"]))
    return "".join(d)

CHW, PAD = 168, 44

def build(vals, network=None, hcos=None, snapshot=None):
    bone, mets = trees()
    # lay each band out independently, then centre the two under one anchor
    def layout(roots, top):
        for r in roots: measure(r, CHW)
        cur = PAD
        for r in roots:
            place(r, cur, top, CHW)
            cur += r.span + H_GAP * 2
        return cur - H_GAP * 2

    bandA_top = 300
    wA = layout(bone, bandA_top + 56)
    depthA = max(n.y for r in bone for n in walk(r)) + BOX_H
    bandB_top = depthA + 64
    wB = layout(mets, bandB_top + 56)
    depthB = max(n.y for r in mets for n in walk(r)) + BOX_H

    width = max(wA, wB) + PAD
    # centre the narrower band
    for roots, w in ((bone, wA), (mets, wB)):
        shift = (width - PAD - w) / 2.0
        if shift > 0:
            for r in roots:
                for n in walk(r): n.x += shift

    anchor_w, anchor_h = 240, 66
    ax = (width - anchor_w) / 2.0
    ay = 196
    out = []
    A = out.append
    key_top = depthB + 52
    height = key_top + 86

    A('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" '
      'class="pcafig" role="img" aria-label="Cohort and query derivation">'
      % (int(width), int(height)))
    A('<rect width="100%" height="100%" fill="#ffffff"/>')
    A('<text x="%d" y="62" font-size="27" font-weight="800" fill="%s" '
      'font-family="Iowan Old Style,Palatino,Georgia,serif">Cohort &amp; query derivation</text>'
      % (PAD, P["navy"]))
    sub1 = "Men ≥70 initiating ADT for prostate cancer · TriNetX US Collaborative Network"
    A('<text x="%d" y="90" font-size="13" fill="%s">%s</text>' % (PAD, P["mut"], esc(sub1)))
    bits = []
    if network: bits.append("%s patients" % format(int(network), ","))
    if hcos:    bits.append("%s healthcare organisations" % hcos)
    if snapshot: bits.append(esc(snapshot))
    if bits:
        A('<text x="%d" y="110" font-size="13" fill="%s" data-q="_meta">%s</text>'
          % (PAD, P["mut"], " · ".join(bits)))

    # anchor cohort
    A('<rect x="%.1f" y="%d" width="%d" height="%d" rx="8" fill="%s"/>'
      % (ax, ay, anchor_w, anchor_h, P["navy"]))
    A('<text x="%.1f" y="%d" text-anchor="middle" font-size="13" font-weight="700" '
      'fill="#fff">Incident-ADT cohort</text>' % (ax + anchor_w / 2.0, ay + 25))
    A('<text x="%.1f" y="%d" text-anchor="middle" font-size="16" font-weight="800" '
      'fill="rgba(255,255,255,.88)" data-q="iadt">n = %s</text>'
      % (ax + anchor_w / 2.0, ay + 48, fmt(vals.get("iadt"))))

    for roots, top, w, title, tone in (
            (bone, bandA_top, wA, "Bone-density screening &amp; bone health", "teal"),
            (mets, bandB_top, wB, "Metastatic disease &amp; treatment intensification", "amber")):
        A('<rect x="%d" y="%d" width="%.1f" height="34" rx="6" fill="%s"/>'
          % (PAD - 10, top, width - 2 * PAD + 20, P["bandA"] if tone == "teal" else P["bandB"]))
        A('<text x="%.1f" y="%d" text-anchor="middle" font-size="13.5" font-weight="800" '
          'fill="%s">%s</text>' % (width / 2.0, top + 23, P[tone], title))
        # spine from the anchor down into the band
        A('<path d="M%.1f %d V%d" fill="none" stroke="%s" stroke-width="1.3"/>'
          % (width / 2.0, ay + anchor_h if tone == "teal" else top - 26, top, P["line"]))
        tops = [r for r in roots]
        xs = [r.x + r.w / 2.0 for r in tops]
        mid = top + 34 + 22
        A('<path d="M%.1f %d V%.1f" fill="none" stroke="%s" stroke-width="1.3"/>'
          % (width / 2.0, top + 34, mid, P["line"]))
        A('<path d="M%.1f %.1f H%.1f" fill="none" stroke="%s" stroke-width="1.3"/>'
          % (min(xs), mid, max(xs), P["line"]))
        for r in tops:
            A('<path d="M%.1f %.1f V%d" fill="none" stroke="%s" stroke-width="1.3"/>'
              % (r.x + r.w / 2.0, mid, r.y, P["line"]))
        for r in roots:
            for n in walk(r):
                if n.kids:
                    A(connect(n.x + n.w / 2.0, n.y + BOX_H, n.kids))
        for r in roots:
            for n in walk(r):
                A(box(n, vals))

    # key
    A('<text x="%d" y="%d" font-size="12" font-weight="800" fill="%s" '
      'letter-spacing="1.4">KEY</text>' % (PAD, key_top, P["mut"]))
    kx = PAD + 46
    for tone, lab in (("teal", "Bone-density branch"), ("amber", "Metastatic branch"),
                      ("plum", "Intensification"), ("slate", "Comparison arm")):
        A('<rect x="%d" y="%d" width="15" height="15" rx="3" fill="%s"/>'
          % (kx, key_top - 12, P[tone]))
        A('<text x="%d" y="%d" font-size="12" fill="%s">%s</text>'
          % (kx + 22, key_top, P["mut"], lab))
        kx += 30 + len(lab) * 6.6 + 34
    A('<text x="%d" y="%d" font-size="11.5" fill="%s">Incident-ADT cohort: men ≥70 with '
      'prostate cancer starting ADT for the first time (ADT prescribed ≥2 times) while ≥70, '
      '2017–2023, after a washout.</text>' % (PAD, key_top + 28, P["mut"]))
    A('<text x="%d" y="%d" font-size="11.5" fill="%s">Rx/Fx ≤5 y: n with the outcome of n at '
      'risk — screened men without the outcome before ADT. Triple therapy is counted in both '
      'ARPI and docetaxel.</text>' % (PAD, key_top + 46, P["mut"]))
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
      if (changed) {
        var note = document.getElementById("pcafig-note");
        if (note) note.textContent = "Refreshed from the master workbook just now.";
      }
    })
    .catch(function () { /* keep the baked numbers */ });
})();
""" % (json.dumps(mapping, ensure_ascii=False, sort_keys=True), json.dumps(GVIZ))


MARK_A, MARK_B = "<!--PCAFIG-->", "<!--/PCAFIG-->"

def block(vals, network=None, hcos=None, snapshot="index 2017–2023", source="sheet"):
    """The whole figure section: intro sentence, the diagram, and a provenance
    line. The intro states a partition that must close, computed from the same
    numbers, so a sentence can never quietly contradict the picture above it."""
    mets, inten, notinten = vals.get("mets"), vals.get("inten"), vals.get("notinten")
    if None not in (mets, inten, notinten) and inten + notinten == mets:
        closes = ("The metastatic partition closes exactly (%s + %s = %s)."
                  % (fmt(inten), fmt(notinten), fmt(mets)))
    else:
        closes = ""
    where = {"sheet": "read from the master workbook at build time",
             "cache": "last known-good values — the workbook was unreachable at build time",
             }.get(source, "")
    return "".join([
        MARK_A,
        '\n   <p class="secintro">Each cohort was carved by ANDing one criterion at a '
        'time onto its parent, anchored to the first incident ADT term. %s</p>\n   ' % closes,
        '<div class="diagramwrap">', build(vals, network, hcos, snapshot), '</div>\n   ',
        '<p id="pcafig-note" class="fignote">Every count above is addressed by its query '
        'name in the PCa master workbook, never typed in — %s.</p>\n   ' % where,
        '<script src="/assets/pca-live.js" defer></script>\n   ',
        MARK_B,
    ])
