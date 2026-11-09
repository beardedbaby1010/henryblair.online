# -*- coding: utf-8 -*-
"""Live numbers for the PVR self-estimation page.

The PVR master workbook carries a reconciliation sheet — tab "1", "every
reported value vs live" — whose column A is the name of a statistic, column B
its value recomputed from the Source rows, and column E its 95% interval. That
is exactly the contract pca_figure.py has with the QM sheet, so this page gets
the same treatment: the build bakes the current values into the HTML and
assets/pvr-live.js re-reads the same tab in the browser.

Nothing here computes a statistic. Every number is the spreadsheet's own.
"""
import html, re

SHEET_ID = "1lnQ7RmxJbf1sU62X5P9kFJViR0yCRTeMl4sRNJV3zaM"
# headers=0 matters: without it gviz folds the sheet's merged title rows into a
# single cell and the first nine statistics vanish. gviz also drops a cell whose
# type disagrees with its column, so the four median rows and the "85 (85.0%)"
# strings never arrive — those stay baked, and only the numeric rows are live.
GVIZ = ("https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&headers=0&sheet=1"
        % SHEET_ID)

# page key -> (row label in column A, how to render column B)
#   n0/n1/n2  a number to that many decimals
#   pct0/pct1 a percentage to that many decimals
#   med       the sheet's own "68.00 (55.25 - 76.00)" string, tidied
FIELDS = {
    # Table 3 Panel A - estimation accuracy
    "est_within":   ("Estimates within 30% of measured (%)", "pct0"),
    "mean_meas":    ("Mean measured PVR (mL)", "n1"),
    "mean_est":     ("Mean estimated PVR (mL)", "n1"),
    "mean_diff":    ("Mean difference (mL)", "n1"),
    "r2":           ("Regression R\u00b2 (est. vs measured)", "n3"),
    "reg_p":        ("Regression p", "p"),
    # Table 3 Panel B - concordance
    "correct_tot":  ("Figure 3 - total % correct", "pct1"),
    "meas_normal":  ("Figure 2 - measured Normal / AccElev / IncompEmpty / Retention", "n0"),
    "est_normal":   ("Figure 2 - estimated categories", "n0"),
    # Table 2 - study characteristics
    "freq":         ("Urinary frequency (presenting complaint) (%)", "pct0"),
    "incomplete":   ("Incomplete emptying (%)", "pct0"),
    "hesitancy":    ("Urinary hesitancy (%)", "pct0"),
    "incont":       ("Urinary incontinence (%)", "pct0"),
    "anxiety":      ("Anxiety (%)", "pct0"),
    "depression":   ("Depression (%)", "pct0"),
    "radiation":    ("Pelvic radiation (%)", "pct0"),
    "diabetes":     ("Type 2 diabetes mellitus (%)", "pct0"),
    "diuretic":     ("Use of diuretic (%)", "pct0"),
    "urge_inc":     ("Urgency incontinence (leaking with urgency) (%)", "pct0"),
    "stress_inc":   ("Stress incontinence (leaking with valsalva) (%)", "pct0"),
    "urgency":      ("Urgency without incontinence (urgent rushing) (%)", "pct0"),
    "freq_check":   ("Urinary frequency (symptom checklist) (%)", "pct0"),
    "nocturia":     ("Nocturia (%)", "pct0"),
    # Figures and regressions
    "fig1_p":       ("Figure 1 - Welch t-test p (inter-void by frequency)", "p"),
    "r2_single":    ("Single-predictor R\u00b2 (frequency ~ inter-void)", "n3"),
    "r2_multi":     ("Multivariable R\u00b2 (6 predictors)", "n3"),
    # Table 4 - the smallest Mann-Whitney p on the page is the one the text quotes
    "mwu_min":      ("Urinary incontinence", "n3"),
}

def esc(s): return html.escape(str(s), quote=True)

def _num(s):
    try:
        return float(re.sub(r"[^0-9eE.+-]", "", str(s).split("(")[0]) or "nan")
    except ValueError:
        return None

def render(raw, how):
    """The spreadsheet's value, in the form the page prints it."""
    if raw is None or str(raw).strip() == "":
        return None
    s = str(raw).strip()
    if how == "raw":
        return s
    if how == "med":                       # "68.00 (55.25 - 76.00)" -> "68 (55.3-76.0)"
        m = re.match(r"\s*([\d.]+)\s*\(\s*([\d.]+)\s*-\s*([\d.]+)\s*\)", s)
        if not m:
            return s
        a, b, c = (float(x) for x in m.groups())
        trim = lambda v: ("%g" % round(v, 1))
        return "%s (%s–%s)" % (trim(a), trim(b), trim(c))
    v = _num(s)
    if v is None:
        return s
    if how == "p":
        return "&lt; 0.001" if v < 0.001 else ("%.3f" % v).rstrip("0").rstrip(".")
    if how.startswith("pct"):
        return "%.*f%%" % (int(how[3:]), v)
    return "%.*f" % (int(how[1:]), v)


def parse(csv_text):
    """tab '1' -> {row label: column B}. First occurrence of a label wins."""
    import csv, io as _io
    out = {}
    for row in csv.reader(_io.StringIO(csv_text)):
        if len(row) < 2:
            continue
        k = (row[0] or "").strip()
        if k and k not in out and (row[1] or "").strip():
            out[k] = row[1].strip()
    return out


def load(cache_path, fetch=True, timeout=20):
    """({page key: rendered string}, source). Never raises; falls back to cache."""
    import json, os, urllib.request
    rows = None
    source = "cache"
    if fetch:
        try:
            req = urllib.request.Request(GVIZ, headers={"User-Agent": "henryblair.online build"})
            txt = urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")
            rows = parse(txt)
            if FIELDS["mean_meas"][0] not in rows:
                rows = None                # got something, but not the sheet we expect
            else:
                source = "sheet"
        except Exception:
            rows = None
    if rows is None and os.path.exists(cache_path):
        rows = json.load(open(cache_path, encoding="utf-8")).get("rows", {})
    if not rows:
        return None, "unavailable"
    if source == "sheet":
        keep = {lab for lab, _ in FIELDS.values()}
        slim = {k: v for k, v in rows.items() if k in keep}
        d = os.path.dirname(cache_path)
        if d:
            os.makedirs(d, exist_ok=True)
        tmp = cache_path + ".tmp"
        json.dump({"rows": slim}, open(tmp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(tmp, cache_path)
    return {k: render(rows.get(lab), how) for k, (lab, how) in FIELDS.items()}, source


def bake(html_text, vals):
    """Rewrite the text of every <span data-q="key"> the page carries."""
    def sub(m):
        key = m.group(1)
        v = vals.get(key)
        return m.group(0) if v is None else '<span data-q="%s">%s</span>' % (esc(key), v)
    return re.sub(r'<span data-q="([a-z0-9_]+)">.*?</span>', sub, html_text, flags=re.S)


def live_js():
    """Browser-side refresh, same contract as the build: labels come from FIELDS
    here, so the page and the build cannot disagree about what a number means."""
    import json
    return """/* Refreshes the PVR page from tab "1" of the PVR master sheet.
   Generated by pvr_live.py — do not edit by hand. */
(function () {
  "use strict";
  var FIELDS = %s;
  var URL_ = %s;
  if (!document.querySelector("[data-q]")) return;

  function cells(line) {
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
    var n = parseFloat(String(s == null ? "" : s).split("(")[0].replace(/[^0-9eE.+-]/g, ""));
    return isFinite(n) ? n : null;
  }
  function render(raw, how) {
    if (raw == null || !String(raw).trim()) return null;
    var s = String(raw).trim(), m, v;
    if (how === "raw") return s;
    if (how === "med") {
      m = s.match(/\\s*([\\d.]+)\\s*\\(\\s*([\\d.]+)\\s*-\\s*([\\d.]+)\\s*\\)/);
      if (!m) return s;
      var t = function (x) { return String(Math.round(parseFloat(x) * 10) / 10); };
      return t(m[1]) + " (" + t(m[2]) + "\\u2013" + t(m[3]) + ")";
    }
    v = num(s);
    if (v === null) return s;
    if (how === "p") return v < 0.001 ? "< 0.001"
        : String(parseFloat(v.toFixed(3)));
    if (how.indexOf("pct") === 0) return v.toFixed(+how.slice(3)) + "%%";
    return v.toFixed(+how.slice(1));
  }

  fetch(URL_, { credentials: "omit" })
    .then(function (r) { if (!r.ok) throw 0; return r.text(); })
    .then(function (txt) {
      var rows = {};
      txt.split(/\\r?\\n/).forEach(function (line) {
        if (!line) return;
        var f = cells(line), k = (f[0] || "").trim();
        if (k && !(k in rows) && (f[1] || "").trim()) rows[k] = f[1].trim();
      });
      if (!(FIELDS.mean_meas[0] in rows)) return;   // not the sheet we expect
      document.querySelectorAll("[data-q]").forEach(function (el) {
        var spec = FIELDS[el.getAttribute("data-q")];
        if (!spec) return;
        var out = render(rows[spec[0]], spec[1]);
        if (out !== null && out !== el.textContent) el.textContent = out;
      });
    })
    .catch(function () { /* keep the baked numbers */ });
})();
""" % (json.dumps({k: [lab, how] for k, (lab, how) in FIELDS.items()},
                  ensure_ascii=False, sort_keys=True), json.dumps(GVIZ))
