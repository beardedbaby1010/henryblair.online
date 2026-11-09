# -*- coding: utf-8 -*-
"""Corrections found by auditing every project page against MOST_ABSTRACTS.txt.

Run from the repo root. Idempotent -- each edit reports applied / already done
/ not found, and a file is only rewritten when something in it changed. No
number here is invented: every replacement is the value the submitted abstract
prints.
"""
import io, os, sys

REPORT = []
TOUCHED = set()


def patch(candidates, old, new, what):
    """Apply one edit to whichever candidate file carries `old`."""
    for path in candidates:
        if not os.path.exists(path):
            continue
        s = io.open(path, encoding="utf-8").read()
        if old in s:
            if s.count(old) > 1:
                REPORT.append(("AMBIGUOUS x%d" % s.count(old), what, path))
                return
            io.open(path, "w", encoding="utf-8").write(s.replace(old, new, 1))
            TOUCHED.add(path)
            REPORT.append(("applied", what, path))
            return
    for path in candidates:
        if os.path.exists(path) and new in io.open(path, encoding="utf-8").read():
            REPORT.append(("already", what, path))
            return
    REPORT.append(("NOT FOUND", what, candidates[0]))


def patch_any(candidates, alternatives, what):
    """One edit, several possible spellings of the anchor. Applies the first
    that matches anywhere, so an em dash written as an entity in one file and
    as a character in another is the same edit, reported once."""
    for old, new in alternatives:
        for path in candidates:
            if os.path.exists(path) and old in io.open(path, encoding="utf-8").read():
                patch(candidates, old, new, what)
                return
    for old, new in alternatives:
        for path in candidates:
            if os.path.exists(path) and new in io.open(path, encoding="utf-8").read():
                REPORT.append(("already", what, path)); return
    REPORT.append(("NOT FOUND", what, candidates[0]))


PROJ = ["projects.py"]
PCA = ["_source/pca_project_hub_standalone.html", "projects/adt-initiation/index.html"]

# ---------------------------------------------------------------------------
# 1. Four bare "<" in prose. They render, because HTML treats "<" before a
#    digit as text, but they are not valid markup and they defeat any tool
#    that strips tags with a regex -- which is how the audit first lost the
#    HoLEP trend clause and the same-day-discharge elderly figures.
for old, new, what in [
    ("PVP 0.5% to 0.0% (both p<0.001), HoLEP",
     "PVP 0.5% to 0.0% (both p&lt;0.001), HoLEP",
     "bph-bleeding: escape p<0.001"),
    ("inpatients (61.3% vs 51.5%; all p<0.001)",
     "inpatients (61.3% vs 51.5%; all p&lt;0.001)",
     "opioids: escape p<0.001"),
    ("91.2% in 2024 (p-trend<0.001)",
     "91.2% in 2024 (p-trend&lt;0.001)",
     "rasp-vs-osp: escape p-trend<0.001"),
    ("15.6% in 2024 (p<0.001 for trend)",
     "15.6% in 2024 (p&lt;0.001 for trend)",
     "same-day-discharge: escape p<0.001"),
]:
    patch(PROJ, old, new, what)

# ---------------------------------------------------------------------------
# 2. The ADT page said docetaxel "stayed flat". The submitted abstract reports
#    it falling, 12.9% to 9.4% (RR 0.73): ARPIs both displaced it and widened
#    the treated group, which is a stronger claim than flat. And the
#    visceral-vs-not rate ratio is 1.01 (0.95-1.08), not 1.00.
# "then plateaued" is not in the abstract either -- intensification rose to
# 52.4% in 2023, the last year, and the page's own year table shows 44.4% then
# 52.4%. That is a rise, not a plateau, so the clause goes.
patch_any(PCA, [
    ("docetaxel stayed flat &mdash; then plateaued.",
     "docetaxel use <em>fell</em> (12.9% &rarr; 9.4%) &mdash; so ARPIs both displaced the older "
     "agent and widened the treated group."),
    ("docetaxel stayed flat \u2014 then plateaued.",
     "docetaxel use <em>fell</em> (12.9% \u2192 9.4%) \u2014 so ARPIs both displaced the older "
     "agent and widened the treated group."),
    ("docetaxel stayed flat",
     "docetaxel use <em>fell</em> (12.9% to 9.4%)"),
], "adt: docetaxel fell, not flat")

patch(PCA, "intensified <b>no more often</b> (RR 1.00)",
      "intensified <b>no more often</b> (RR 1.01, 0.95&ndash;1.08)",
      "adt: visceral RR 1.00 -> 1.01")
patch(PCA, "Rates are identical (RR 1.00).",
      "Rates are the same within noise (45.4% vs 44.9%; RR 1.01, 0.95&ndash;1.08).",
      "adt: Figure 11 caption")

# ---------------------------------------------------------------------------
# 3. The ketamine-cystitis page still said "Early stage -- cohort definition in
#    progress", but the abstract is written and submitted with full results.
#    Replace the placeholder hub with what the abstract reports.
KETAMINE_NEW = '''    {
        "slug": "ketamine-cystitis", "tab": None, "group": "current",
        "title": "Ketamine cystitis in the United States",
        "kicker": "National Inpatient Sample \\u00b7 2016\\u20132021",
        "status": "Abstract submitted \\u2014 2027 AUA Annual Meeting",
        "summary": "Ketamine reaches patients two ways now \\u2014 illicitly, and by prescription for "
                   "depression and chronic pain \\u2014 and admissions for its bladder toxicity rose 140% "
                   "in six years. Where those admissions happened only partly matches where the drug "
                   "is seized, which points at medical access as an under-recognized contributor.",
        "stats": [("+140%", "rise in admissions, 2016\\u20132021"),
                  ("4,020", "estimated admissions"),
                  ("41.5", "mean age, years"),
                  ("52.2%", "insured by Medicaid")],
        "tags": ["Ketamine cystitis", "Epidemiology", "Substance use", "National Inpatient Sample",
                 "Real-world data"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Marc Ganz, MD", "Michael West", "Yitzchak Katlowitz", "Henry M. Blair",
                       "Gina DeMeo", "Christopher Edwards, MD", "Arshia Sandozi, DO",
                       "Ariel Schulman, MD"],
            "lede": "Ketamine use has moved in a decade from club drug to prescribed treatment for "
                    "depression and chronic pain. Its bladder toxicity is well described in case "
                    "series and poorly described at national scale \\u2014 which is a problem if "
                    "prescribing keeps rising.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting.",
            "question": "How common is ketamine-associated cystitis in the United States, who "
                        "develops it, and does its geography follow illicit supply or medical access?",
            "approach": [
                "We analysed the 2016\\u20132021 National Inpatient Sample. Suspected ketamine cystitis "
                "was defined by concurrent ICD-10-CM diagnoses of a hallucinogen-related disorder and "
                "lower urinary tract symptoms.",
                "NIS weights gave annual rates per 100,000 admissions and variation across Census "
                "divisions.",
                "Drug Enforcement Administration Forensic Laboratory Information System ketamine "
                "reports were mapped by division and standardised to Census populations \\u2014 a "
                "proxy for illicit supply.",
                "Published retail-dispensing data and national ketamine-clinic counts were reviewed "
                "to put medical access beside it.",
            ],
            "findings": [
                "An estimated 4,020 admissions were identified. Rates rose 140%, from 1.22 per "
                "100,000 admissions in 2016 to 2.92 in 2021.",
                "Mean age was 41.5 years; 66.5% were male, 52.2% had Medicaid, and 80.3% were "
                "treated at urban teaching hospitals.",
                "Geographic admission patterns only partially overlapped those of 11,329 DEA "
                "ketamine reports from the same years.",
                "Over the same period published retail data showed a 350% increase in patients "
                "dispensed ketamine from 2018\\u20132023, and over 300 ketamine-focused clinics were "
                "listed nationally.",
            ],
            "findings_note": "Admissions rose 140% with only partial geographic overlap with illicit "
                             "ketamine reports. Against rapidly expanding retail dispensing and clinic "
                             "access, illicit use alone may not explain the growing burden; medical "
                             "exposure may be an under-recognised contributor and warrants direct "
                             "investigation.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-ketamine-cystitis/"}],
            "sidefoot": "Marc Ganz, MD \\u00b7 Henry M. Blair<br>Department of Urology, "
                        "Maimonides Medical Center",
        },
    },
'''


def swap_ketamine():
    path = "projects.py"
    s = io.open(path, encoding="utf-8").read()
    if '"Abstract submitted \\u2014 2027 AUA Annual Meeting",\n        "summary": "Ketamine' in s \
       or '"stats": [("+140%", "rise in admissions' in s:
        REPORT.append(("already", "ketamine: hub rewritten from the abstract", path)); return
    key = '"slug": "ketamine-cystitis"'
    i = s.find(key)
    if i < 0:
        REPORT.append(("NOT FOUND", "ketamine: hub rewritten from the abstract", path)); return
    start = s.rfind("    {\n", 0, i)
    nxt = s.find('"slug": "', i + len(key))
    end = s.rfind("    {\n", 0, nxt) if nxt > 0 else -1
    if start < 0 or end <= start:
        REPORT.append(("NOT FOUND (bounds)", "ketamine hub", path)); return
    io.open(path, "w", encoding="utf-8").write(s[:start] + KETAMINE_NEW + "\n" + s[end:])
    TOUCHED.add(path)
    REPORT.append(("applied", "ketamine: hub rewritten from the abstract", path))


# ---------------------------------------------------------------------------
# 4. The bleeding abstract prints transfusion as 0.25% vs 0.90%; the workbook
#    formats the same counts to one decimal, so the page read 0.3% vs 0.9%.
#    The counts agree exactly (78/31,087 and 742/82,020), so recompute the
#    percentage from n/N at two decimals rather than ask the spreadsheet to
#    change its number format. A new "pct2" format, in the build and in the
#    browser refresh, so the two cannot disagree.
SL = ["sheet_live.py"]

patch(SL, '#   pct    the percentage                                  -> "1.1%"',
      '#   pct    the percentage                                  -> "1.1%"\n'
      '#   pct2   that percentage recomputed from n/N, two decimals -> "0.25%"\n'
      '#          (the workbook prints one; the abstracts print two)',
      "sheet_live: document pct2")

patch(SL, '''    if fmt == "pct":
        return _paren_pct(s)''',
      '''    if fmt == "pct":
        return _paren_pct(s)
    if fmt == "pct2":
        n = _first_num(s)
        N = _first_num(row.get("N1" if col == "n1 (%1) [Wilson]" else "N2", "")) if row else None
        if not n or not N:
            return _paren_pct(s)
        try:
            return "%.2f%%" % (100.0 * float(n.replace(",", "")) / float(N.replace(",", "")))
        except (ValueError, ZeroDivisionError):
            return _paren_pct(s)''',
      "sheet_live: pct2 in the build")

patch(SL, '    if (fmt === "pct") return parenPct(s);',
      '''    if (fmt === "pct") return parenPct(s);
    if (fmt === "pct2") {
      var p2n = firstNum(s),
          p2N = row ? firstNum(row[col === "n1 (%%1) [Wilson]" ? "N1" : "N2"] || "") : null;
      if (!p2n || !p2N) return parenPct(s);
      var p2v = parseFloat(p2n.replace(/,/g, "")) / parseFloat(p2N.replace(/,/g, ""));
      return isFinite(p2v) ? (100 * p2v).toFixed(2) + "%%" : parenPct(s);
    }''',
      "sheet_live: pct2 in the browser")

patch(SL, '"pvp_transf":     ("Transfusion \\u226472 h", "n2 (%2) [Wilson]", "pct"),',
      '"pvp_transf":     ("Transfusion \\u226472 h", "n2 (%2) [Wilson]", "pct2"),',
      "sheet_live: pvp_transf -> pct2")
patch(SL, '"turp_transf":    ("Transfusion \\u226472 h", "n1 (%1) [Wilson]", "pct"),',
      '"turp_transf":    ("Transfusion \\u226472 h", "n1 (%1) [Wilson]", "pct2"),',
      "sheet_live: turp_transf -> pct2")

# and the page's own baked text, so it is right before any JavaScript runs
patch(PROJ, '<span data-q=\\"pvp_transf\\">0.3%</span> vs <span data-q=\\"turp_transf\\">0.9%</span>',
      '<span data-q=\\"pvp_transf\\">0.25%</span> vs <span data-q=\\"turp_transf\\">0.90%</span>',
      "bph-bleeding: baked transfusion to two decimals")


# ---------------------------------------------------------------------------
# 5. The In Preparation page gains a "Regenerate figures from the live sheet"
#    section: one row per generator, with the command that rebuilds it from
#    the live workbook. A static page cannot run Python, so the button copies
#    the command rather than pretending to execute it.
INPREP = "_source/in-preparation.html"


def add_inprep_section(fragment):
    if not os.path.exists(INPREP):
        REPORT.append(("NOT FOUND", "in-preparation: figures section", INPREP)); return
    if not os.path.exists(fragment):
        REPORT.append(("NO FRAGMENT", "in-preparation: figures section", fragment)); return
    s = io.open(INPREP, encoding="utf-8").read()
    if "<!--REGENFIGS-->" in s:
        REPORT.append(("already", "in-preparation: figures section", INPREP)); return
    frag = io.open(fragment, encoding="utf-8").read().rstrip() + "\n"
    for anchor in ("</main>", "<!--/BODY-->", "</body>"):
        i = s.rfind(anchor)
        if i >= 0:
            io.open(INPREP, "w", encoding="utf-8").write(s[:i] + frag + s[i:])
            TOUCHED.add(INPREP)
            REPORT.append(("applied before %s" % anchor,
                           "in-preparation: figures section", INPREP))
            return
    io.open(INPREP, "a", encoding="utf-8").write("\n" + frag)
    TOUCHED.add(INPREP)
    REPORT.append(("appended at end", "in-preparation: figures section", INPREP))


# ---------------------------------------------------------------------------
# 6. The VE page's Table 2 shows no interval for the pre-announcement trend.
#    Abstract A reports it: +25.8%/yr, 95% CI 23.1-28.6. The estimate on the
#    page and in the abstract agree exactly, so the interval belongs with it.
#    (The cell is a plain <td>, not a data-q span, so this one is safe to
#    write -- nothing refetches it.)
VE = ["_source/ve-boxed-warning.html", "projects/ve-boxed-warning/index.html"]

patch(VE,
      '<tr><td>Pre-announcement trend, incident use</td><td class="n">+25.8%/yr</td>'
      '<td class="n">&mdash;</td><td class="n">&lt;0.001</td></tr>',
      '<tr><td>Pre-announcement trend, incident use</td><td class="n">+25.8%/yr</td>'
      '<td class="n">+23.1 to +28.6</td><td class="n">&lt;0.001</td></tr>',
      "ve: pre-trend CI from abstract A")


if __name__ == "__main__":
    for f in ("projects.py", "sheet_live.py", "build_site.py"):
        if not os.path.exists(f):
            sys.exit("run this from the repo root (%s not found)" % f)
    swap_ketamine()
    add_inprep_section(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "inprep_figures_section.html"))
    print("files touched: %s\n" % (", ".join(sorted(TOUCHED)) or "none"))
    for status, what, path in REPORT:
        print("  %-18s %-46s %s" % (status, what, path))
    import py_compile
    for f in ("projects.py", "sheet_live.py"):
        py_compile.compile(f, doraise=True)
    print("\nprojects.py and sheet_live.py compile.")
