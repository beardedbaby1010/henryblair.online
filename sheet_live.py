# -*- coding: utf-8 -*-
"""One live link for every project whose workbook uses the FLAGGING layout.

pca_figure.py and ve_figure.py each own a diagram as well as their numbers, so
they stay separate. Everything else — the six NSQIP workbooks, the ADI and
urogyn-survey workbooks — shares one table shape, so it shares one module:

    Key | Variable | Level | N1 | n1 (%1) [Wilson] | N2 | n2 (%2) [Wilson]
        | RR [Katz] | OR [Woolf] | RD [Wald], [Newcombe] | ...

A row is addressed by its Variable text, which is unique within a tab and reads
like English in the config below, so a page hook says what it means. A column is
addressed by its header, never by position, so inserting a column in the
spreadsheet cannot silently shift every number on the site.

Nothing here computes a statistic. Every value is the spreadsheet's own; the
only transformation is pulling one field out of a composite cell such as
"1,243 (1.1%) [1.0%-1.2%]" and printing the brackets the way the page does.

The build bakes current values into the HTML, and assets/live.js re-reads the
same tabs in the browser, so a page is right before any JavaScript runs and
right again a minute after the spreadsheet changes.
"""
import html, json, os, re, urllib.request

GVIZ = ("https://docs.google.com/spreadsheets/d/%s/gviz/tq"
        "?tqx=out:csv&headers=0&sheet=%s")

# ---------------------------------------------------------------- the projects
# slug -> sheet id, tab, and {page key: (Variable text, column, format)}
#
# formats
#   n      the count            "1,243 (1.1%) [1.0%-1.2%]" -> "1,243"
#   pct    the percentage                                  -> "1.1%"
#   pct2   that percentage recomputed from n/N, two decimals -> "0.25%"
#          (the workbook prints one; the abstracts print two)
#   ci     percentage with its Wilson interval              -> "1.1% (1.0-1.2)"
#   n_of_N count over its denominator                       -> "1,243 / 112,132"
#   N      the denominator alone                            -> "112,132"
#   ratio  a ratio cell         "0.15 [0.09-0.27]"          -> "0.15 (0.09-0.27)"
#   ratio0 the point estimate alone                         -> "0.15"
#   raw    the cell, untouched
SHEETS = {
    "oab-adi": {
        "id": "1nVRKNIr4aPuSjBQUDhQfK3-7XajJ-Ni0irVtXjmSG1U",
        "tab": "1",
        "fields": {
            # the workbook writes both arms into one cell; adv_/dis_ pull one out
            "time_adv":    ("Trip duration (min), median (IQR)", "Group Values", "adv_n"),
            "time_dis":    ("Trip duration (min), median (IQR)", "Group Values", "dis_n"),
            "time_p":      ("Trip duration (min), median (IQR)", "p-value", "p"),
            "cost_adv":    ("Cost ($), median (IQR)", "Group Values", "adv_n"),
            "cost_dis":    ("Cost ($), median (IQR)", "Group Values", "dis_n"),
            "cost_p":      ("Cost ($), median (IQR)", "p-value", "p"),
            "urge_adv":    ("Urinary urge frequency", "Group Values", "adv_pct"),
            "urge_dis":    ("Urinary urge frequency", "Group Values", "dis_pct"),
            "urge_p":      ("Urinary urge frequency", "p-value", "p"),
            "transit_adv": ("Public transit", "Group Values", "adv_pct"),
            "transit_dis": ("Public transit", "Group Values", "dis_pct"),
            "transit_p":   ("Public transit", "p-value", "p"),
            "accomp_adv":  ("Accompanied to visit", "Group Values", "adv_pct"),
            "accomp_dis":  ("Accompanied to visit", "Group Values", "dis_pct"),
            "accomp_p":    ("Accompanied to visit", "p-value", "p"),
            "video_adv":   ("Willing to do a video visit", "Group Values", "adv_pct"),
            "video_dis":   ("Willing to do a video visit", "Group Values", "dis_pct"),
        },
    },
    "urogyn-perceptions": {
        "id": "16xPztZ5epiIFnTUqqXLcgzYIFHapAgoi_4Qu9n-iddw",
        "tab": "Tables",
        "fields": {
            "any_interest":   ("Any fellowship interest", "n (%) [Wilson CI]", "pct"),
            "any_interest_ci":("Any fellowship interest", "n (%) [Wilson CI]", "ci"),
            "has_mentor":     ("Has a URPS mentor", "n (%) [Wilson CI]", "pct"),
            "role_in_uro":    ("URPS has a defined role in urology (agree)", "n (%) [Wilson CI]", "pct"),
            "not_obgyn":      ("URPS should be primarily OBGYN (disagree)", "n (%) [Wilson CI]", "pct"),
            "exposure_pgy3":  ("First meaningful exposure by PGY-3", "n (%) [Wilson CI]", "pct"),
            "no_exposure":    ("No meaningful exposure (never)", "n (%) [Wilson CI]", "pct"),
            "faculty_yes":    ("URPS fellowship-trained faculty: yes", "n (%) [Wilson CI]", "pct"),
            "inst_fellowship":("Institutional URPS fellowship: yes", "n (%) [Wilson CI]", "pct"),
            "barrier_other":  ("Barrier: prefers another subspecialty", "n (%) [Wilson CI]", "pct"),
            "barrier_scope":  ("Barrier: narrowed scope of practice", "n (%) [Wilson CI]", "pct"),
            "barrier_exposure":("Barrier: limited exposure", "n (%) [Wilson CI]", "pct"),
        },
    },
    "nsqip-same-day-discharge": {
        "id": "1ESAUzokZpr5G3zCwJRQcMYPvFmNTOQEqxPUvyahWqo8",
        "tab": "SDD_vs_Overnight",
        "fields": {
            "n_overnight":    ("Transfusion \u226472 h", "N1", "N"),
            "n_sdd":          ("Transfusion \u226472 h", "N2", "N"),
            "readmit_on":     ("30-day readmission", "n1 (%1) [Wilson]", "pct"),
            "readmit_sdd":    ("30-day readmission", "n2 (%2) [Wilson]", "pct"),
            "readmit_rr":     ("30-day readmission", "RR [Katz]", "ratio"),
            "readmit_rr0":    ("30-day readmission", "RR [Katz]", "ratio0"),
            "unpl_rr":        ("Unplanned readmission", "RR [Katz]", "ratio"),
            "serious_on":     ("Serious complication", "n1 (%1) [Wilson]", "pct"),
            "serious_sdd":    ("Serious complication", "n2 (%2) [Wilson]", "pct"),
            "serious_rr":     ("Serious complication", "RR [Katz]", "ratio"),
            "anycomp_on":     ("Any complication", "n1 (%1) [Wilson]", "pct"),
            "anycomp_sdd":    ("Any complication", "n2 (%2) [Wilson]", "pct"),
            "anycomp_rr":     ("Any complication", "RR [Katz]", "ratio"),
            "reop_on":        ("Reoperation", "n1 (%1) [Wilson]", "pct"),
            "reop_sdd":       ("Reoperation", "n2 (%2) [Wilson]", "pct"),
            "reop_rr":        ("Reoperation", "RR [Katz]", "ratio"),
            "death_rr":       ("30-day mortality", "RR [Katz]", "ratio"),
            "nonhome_rr":     ("Non-home discharge", "RR [Katz]", "ratio"),
            "transfusion_rr": ("Transfusion \u226472 h", "RR [Katz]", "ratio"),
        },
    },
    "nsqip-bph-bleeding": {
        "id": "1RzIoYqAdbkHdEBsBve9sheStWZ5sB3joBsC49ArK3lU",
        "tab": "PVP_vs_TURP",
        "fields": {
            "pvp_transf":     ("Transfusion \u226472 h", "n2 (%2) [Wilson]", "pct2"),
            "turp_transf":    ("Transfusion \u226472 h", "n1 (%1) [Wilson]", "pct2"),
            "pvp_transf_rr":  ("Transfusion \u226472 h", "RR [Katz]", "ratio"),
            "pvp_transf_rr0": ("Transfusion \u226472 h", "RR [Katz]", "ratio0"),
            "pvp_bleed":      ("Bleeding composite", "n2 (%2) [Wilson]", "pct"),
            "turp_bleed":     ("Bleeding composite", "n1 (%1) [Wilson]", "pct"),
            "holep_bleed":    ("Bleeding composite", "n2 (%2) [Wilson]", "pct", "HoLEP_vs_TURP"),
            "holep_serious":  ("Serious complication", "n2 (%2) [Wilson]", "pct", "HoLEP_vs_TURP"),
            "turp_serious":   ("Serious complication", "n1 (%1) [Wilson]", "pct", "HoLEP_vs_TURP"),
            "holep_readmit":  ("30-day readmission", "n2 (%2) [Wilson]", "pct", "HoLEP_vs_TURP"),
            "turp_readmit":   ("30-day readmission", "n1 (%1) [Wilson]", "pct", "HoLEP_vs_TURP"),
        },
    },
    "nsqip-opioids": {
        "id": "11U1zAc3idXhyFsKEhSYhCVYEVfrj3EkYGlaqC_1DrfA",
        "tab": "Rx_vs_NoRx",
        "fields": {
            "readmit_rx":     ("30-day readmission", "n2 (%2) [Wilson]", "pct"),
            "readmit_norx":   ("30-day readmission", "n1 (%1) [Wilson]", "pct"),
            "readmit_rr":     ("30-day readmission", "RR [Katz]", "ratio"),
        },
    },
    "nsqip-rasp-elderly": {
        "id": "1Ky767miyoMNHrKN37X4s-ZuYM6zLomAwvLAr_ogQ6OQ",
        "tab": "Age75_vs_younger",
        "fields": {
            "old_anycomp":    ("Any complication", "n2 (%2) [Wilson]", "pct"),
            "young_anycomp":  ("Any complication", "n1 (%1) [Wilson]", "pct"),
            "old_anycomp_rr": ("Any complication", "RR [Katz]", "ratio"),
            "old_transf":     ("Transfusion \u226472 h", "n2 (%2) [Wilson]", "pct"),
            "young_transf":   ("Transfusion \u226472 h", "n1 (%1) [Wilson]", "pct"),
            "old_nonhome":    ("Non-home discharge", "n2 (%2) [Wilson]", "pct"),
            "young_nonhome":  ("Non-home discharge", "n1 (%1) [Wilson]", "pct"),
            "old_serious":    ("Serious complication", "n2 (%2) [Wilson]", "pct"),
            "young_serious":  ("Serious complication", "n1 (%1) [Wilson]", "pct"),
        },
    },
    "nsqip-rasp-vs-osp": {
        "id": "1KdrNMDgCVsNVSlupcDrVzQEY-_1IARLjbSbE2roaLFw",
        "tab": "RASP_vs_OSP",
        "fields": {
            "rasp_transf":    ("Transfusion \u226472 h", "n2 (%2) [Wilson]", "pct"),
            "osp_transf":     ("Transfusion \u226472 h", "n1 (%1) [Wilson]", "pct"),
            "transf_rr":      ("Transfusion \u226472 h", "RR [Katz]", "ratio"),
            "transf_rr0":     ("Transfusion \u226472 h", "RR [Katz]", "ratio0"),
            "rasp_anycomp":   ("Any complication", "n2 (%2) [Wilson]", "pct"),
            "osp_anycomp":    ("Any complication", "n1 (%1) [Wilson]", "pct"),
            "rasp_readmit":   ("30-day readmission", "n2 (%2) [Wilson]", "pct"),
            "osp_readmit":    ("30-day readmission", "n1 (%1) [Wilson]", "pct"),
            "rasp_reop":      ("Reoperation", "n2 (%2) [Wilson]", "pct"),
            "osp_reop":       ("Reoperation", "n1 (%1) [Wilson]", "pct"),
        },
    },
    "nsqip-colpopexy": {
        "id": "1Re7gvVzqrXyWpZoKJgVTM_uNLtR5ZTXY9_ajyErSQaM",
        "tab": "Robotic_SCP_vs_SSLF",
        "fields": {
            "scp_uti":        ("30-day UTI (primary outcome)", "n2 (%2) [Wilson]", "pct"),
            "sslf_uti":       ("30-day UTI (primary outcome)", "n1 (%1) [Wilson]", "pct"),
            "uti_rr":         ("30-day UTI (primary outcome)", "RR [Katz]", "ratio"),
            "uti_rr0":        ("30-day UTI (primary outcome)", "RR [Katz]", "ratio0"),
            "scp_anycomp":    ("Any complication", "n2 (%2) [Wilson]", "pct"),
            "sslf_anycomp":   ("Any complication", "n1 (%1) [Wilson]", "pct"),
            "scp_reop":       ("Reoperation", "n2 (%2) [Wilson]", "pct"),
            "sslf_reop":      ("Reoperation", "n1 (%1) [Wilson]", "pct"),
            "scp_serious":    ("Serious complication", "n2 (%2) [Wilson]", "pct"),
            "sslf_serious":   ("Serious complication", "n1 (%1) [Wilson]", "pct"),
            "scp_los":        ("LOS >1 day", "n2 (%2) [Wilson]", "pct"),
            "sslf_los":       ("LOS >1 day", "n1 (%1) [Wilson]", "pct"),
        },
    },
}

def esc(s): return html.escape(str(s), quote=True)

# ------------------------------------------------------------------- rendering
_DASH = "–"

def _first_num(s):
    m = re.match(r"\s*([\d,]+(?:\.\d+)?)", str(s))
    return m.group(1) if m else None

def _paren_pct(s):
    m = re.search(r"\(([^)]*?%)\)", str(s))
    return m.group(1) if m else None

def _bracket(s):
    m = re.search(r"\[([^\]]*)\]", str(s))
    return m.group(1) if m else None

def _arm(s, which):
    """The ADI tab writes both arms into one cell:
         "Adv: 44/57 (77.2%)\nDis:  54/59 (91.5%)"
    Return one arm's text, so a page can address 'the disadvantaged group'."""
    for line in str(s).splitlines():
        t = line.strip()
        if t.lower().startswith(which):
            return t.split(":", 1)[1].strip()
    return None


def pick(row, col):
    """row[col], or the first header that starts with col. Some headers carry a
    multi-line explanation ("Group Values\nAdvantaged group = ..."), and the
    config should not have to repeat it."""
    if col in row:
        return row[col]
    for k in row:
        if k and k.startswith(col):
            return row[k]
    return None


def render(cell, fmt, row=None, col=None):
    """One cell, in the form the page prints it. None when the cell is empty."""
    if cell is None or not str(cell).strip():
        return None
    s = str(cell).strip()
    if fmt == "raw":
        return s
    if fmt.startswith("adv") or fmt.startswith("dis"):
        arm = _arm(s, "adv" if fmt.startswith("adv") else "dis")
        if arm is None:
            return None
        rest = fmt[3:]
        if rest == "_pct":
            return _paren_pct(arm)
        if rest == "_n":
            return _first_num(arm)
        return arm
    if fmt == "p":
        try:
            v = float(re.sub(r"[^0-9.eE+-]", "", s))
        except ValueError:
            return s
        return "&lt; 0.001" if v < 0.001 else ("%.3f" % v).rstrip("0").rstrip(".")
    if fmt in ("n", "N"):
        return _first_num(s)
    if fmt == "pct":
        return _paren_pct(s)
    if fmt == "pct2":
        n = _first_num(s)
        N = _first_num(row.get("N1" if col == "n1 (%1) [Wilson]" else "N2", "")) if row else None
        if not n or not N:
            return _paren_pct(s)
        try:
            return "%.2f%%" % (100.0 * float(n.replace(",", "")) / float(N.replace(",", "")))
        except (ValueError, ZeroDivisionError):
            return _paren_pct(s)
    if fmt == "ci":
        p, b = _paren_pct(s), _bracket(s)
        return p if not b else "%s (%s)" % (p, b.replace("%", ""))
    if fmt == "n_of_N":
        n = _first_num(s)
        N = _first_num(row.get("N1" if col == "n1 (%1) [Wilson]" else "N2", "")) if row else None
        return n if not N else "%s / %s" % (n, N)
    if fmt in ("ratio", "ratio0"):
        pt, b = _first_num(s), _bracket(s)
        if fmt == "ratio0" or not b:
            return pt
        return "%s (%s)" % (pt, b)
    return s

# --------------------------------------------------------------------- reading
# A tab announces a new table with one of these in column A. Everything after
# it is that table's rows until the next such line.
HEADERS = ("Key", "Comparison", "Proportion", "Variable", "Abstract")

def parse(csv_text, headers=HEADERS, label="Variable"):
    """A tab -> {row label: {column header: cell}}.

    Every header line restarts the columns, because one tab holds several
    tables. The row is keyed by its 'label' column when the table has one and
    by column A otherwise, and the first occurrence wins, so an addressed row
    cannot change meaning when a later table repeats the label."""
    import csv, io as _io
    out, hdr = {}, None
    for row in csv.reader(_io.StringIO(csv_text)):
        if not row:
            continue
        first = (row[0] or "").strip()
        if first in headers:
            hdr = [(c or "").strip() for c in row]
            continue
        if not hdr or not first:
            continue
        d = dict(zip(hdr, row))
        key = (d.get(label) or "").strip() or first
        if key not in out:
            out[key] = d
    return out


def _popts(cfg):
    """parse() options a project overrides; most use the defaults."""
    o = {}
    if cfg.get("headers"):
        o["headers"] = tuple(cfg["headers"])
    if cfg.get("label"):
        o["label"] = cfg["label"]
    return o


def fetch(sheet_id, tab, timeout=25):
    req = urllib.request.Request(GVIZ % (sheet_id, tab),
                                 headers={"User-Agent": "henryblair.online build"})
    return urllib.request.urlopen(req, timeout=timeout).read().decode("utf-8", "replace")


def tabs_used(cfg):
    """Every tab this project's fields read, the default one first."""
    out = [cfg["tab"]]
    for spec in cfg["fields"].values():
        t = spec[3] if len(spec) > 3 else cfg["tab"]
        if t not in out:
            out.append(t)
    return out


def load(slug, cache_dir, do_fetch=True):
    """({page key: rendered string}, source). Never raises; falls back to cache."""
    cfg = SHEETS[slug]
    cache_path = os.path.join(cache_dir, "%s_cache.json" % slug)
    rows, source = None, "cache"
    if do_fetch:
        try:
            got = {}
            for t in tabs_used(cfg):
                got[t] = parse(fetch(cfg["id"], t), **_popts(cfg))
            if not any(got.values()):
                rows = None
            else:
                rows, source = got, "sheet"
        except Exception:
            rows = None
    if rows is None and os.path.exists(cache_path):
        rows = json.load(open(cache_path, encoding="utf-8")).get("rows")
    if not rows:
        return None, "unavailable"
    if source == "sheet":
        wanted = {}
        for spec in cfg["fields"].values():
            wanted.setdefault(spec[3] if len(spec) > 3 else cfg["tab"], set()).add(spec[0])
        slim = {t: {k: v for k, v in (rows.get(t) or {}).items() if k in names}
                for t, names in wanted.items()}
        os.makedirs(cache_dir, exist_ok=True)
        tmp = cache_path + ".tmp"
        json.dump({"rows": slim}, open(tmp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1, sort_keys=True)
        os.replace(tmp, cache_path)
    vals = {}
    for key, spec in cfg["fields"].items():
        var, col, fmt = spec[0], spec[1], spec[2]
        tab = spec[3] if len(spec) > 3 else cfg["tab"]
        row = (rows.get(tab) or {}).get(var)
        vals[key] = None if row is None else render(pick(row, col), fmt, row, col)
    return vals, source


def bake(html_text, vals):
    """Rewrite the text of every <span data-q="key"> the page carries."""
    def sub(m):
        v = vals.get(m.group(1))
        return m.group(0) if v is None else '<span data-q="%s">%s</span>' % (esc(m.group(1)), v)
    return re.sub(r'<span data-q="([a-zA-Z0-9_]+)">.*?</span>', sub, html_text, flags=re.S)


# ------------------------------------------------------------------ browser side
def live_js(slug):
    """Browser-side refresh for one project. The field map is written from
    SHEETS here, so the page and the build cannot disagree about a number."""
    cfg = SHEETS[slug]
    fields = {k: [v[0], v[1], v[2], (v[3] if len(v) > 3 else cfg["tab"])]
              for k, v in cfg["fields"].items()}
    urls = {t: GVIZ % (cfg["id"], t) for t in tabs_used(cfg)}
    return """/* Refreshes %s from its live workbook (%s).
   Generated by sheet_live.py - do not edit by hand. */
(function () {
  "use strict";
  var FIELDS = %s;
  var URLS = %s;
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
  function firstNum(s) { var m = String(s).match(/^\\s*([\\d,]+(?:\\.\\d+)?)/); return m ? m[1] : null; }
  function parenPct(s) { var m = String(s).match(/\\(([^)]*?%%)\\)/); return m ? m[1] : null; }
  function bracket(s) { var m = String(s).match(/\\[([^\\]]*)\\]/); return m ? m[1] : null; }
  function arm(s, which) {
    var lines = String(s).split(/\\n/), i, t;
    for (i = 0; i < lines.length; i++) {
      t = lines[i].trim();
      if (t.toLowerCase().indexOf(which) === 0) return t.split(":").slice(1).join(":").trim();
    }
    return null;
  }
  function render(cell, fmt, row, col) {
    if (cell == null || !String(cell).trim()) return null;
    var s = String(cell).trim(), p, b, n, N, a;
    if (fmt === "raw") return s;
    if (fmt.indexOf("adv") === 0 || fmt.indexOf("dis") === 0) {
      a = arm(s, fmt.indexOf("adv") === 0 ? "adv" : "dis");
      if (a === null) return null;
      if (fmt.slice(3) === "_pct") return parenPct(a);
      if (fmt.slice(3) === "_n") return firstNum(a);
      return a;
    }
    if (fmt === "p") {
      var v = parseFloat(s.replace(/[^0-9.eE+-]/g, ""));
      if (!isFinite(v)) return s;
      return v < 0.001 ? "< 0.001" : String(parseFloat(v.toFixed(3)));
    }
    if (fmt === "n" || fmt === "N") return firstNum(s);
    if (fmt === "pct") return parenPct(s);
    if (fmt === "pct2") {
      var p2n = firstNum(s),
          p2N = row ? firstNum(row[col === "n1 (%%1) [Wilson]" ? "N1" : "N2"] || "") : null;
      if (!p2n || !p2N) return parenPct(s);
      var p2v = parseFloat(p2n.replace(/,/g, "")) / parseFloat(p2N.replace(/,/g, ""));
      return isFinite(p2v) ? (100 * p2v).toFixed(2) + "%%" : parenPct(s);
    }
    if (fmt === "ci") { p = parenPct(s); b = bracket(s);
      return b ? p + " (" + b.replace(/%%/g, "") + ")" : p; }
    if (fmt === "n_of_N") { n = firstNum(s);
      N = firstNum(row[col === "n1 (%%1) [Wilson]" ? "N1" : "N2"] || "");
      return N ? n + " / " + N : n; }
    if (fmt === "ratio" || fmt === "ratio0") { p = firstNum(s); b = bracket(s);
      return (fmt === "ratio0" || !b) ? p : p + " (" + b + ")"; }
    return s;
  }

  function readTab(txt) {
      var rows = {}, hdr = null;
      txt.split(/\\r?\\n/).forEach(function (line) {
        if (!line) return;
        var f = cells(line), first = (f[0] || "").trim(), d = {}, i;
        if (first === "Key") { hdr = f.map(function (c) { return (c || "").trim(); }); return; }
        if (!hdr || !first) return;
        for (i = 0; i < hdr.length; i++) d[hdr[i]] = f[i];
        var v = (d.Variable || "").trim();
        if (v && !(v in rows)) rows[v] = d;
      });
      return rows;
  }

  var names = Object.keys(URLS);
  Promise.all(names.map(function (t) {
    return fetch(URLS[t], { credentials: "omit" })
      .then(function (r) { if (!r.ok) throw 0; return r.text(); })
      .then(readTab)
      .catch(function () { return null; });
  })).then(function (results) {
      var byTab = {};
      names.forEach(function (t, i) { byTab[t] = results[i]; });
      document.querySelectorAll("[data-q]").forEach(function (el) {
        var spec = FIELDS[el.getAttribute("data-q")];
        if (!spec) return;
        var rows = byTab[spec[3]];
        if (!rows) return;
        var row = rows[spec[0]];
        if (!row) return;
        var cell = row[spec[1]];
        if (cell === undefined) {
          for (var k in row) { if (k && k.indexOf(spec[1]) === 0) { cell = row[k]; break; } }
        }
        var out = render(cell, spec[2], row, spec[1]);
        if (out !== null && out !== el.textContent) el.textContent = out;
      });
  }).catch(function () { /* keep the baked numbers */ });
})();
""" % (slug, cfg["tab"],
       json.dumps(fields, ensure_ascii=False, sort_keys=True),
       json.dumps(urls, ensure_ascii=False, sort_keys=True))
