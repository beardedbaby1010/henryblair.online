# -*- coding: utf-8 -*-
"""Canonical VE query spec, derived from 310 verified dumps (not hand-written)."""
import re, json

COH = ["No_HA","No_C50","No_Hx","HA","C50","Hx","Unstrat"]
STR = ["ERPos","ERNeg","ERAmbig","ERUnrec","ERP_Old","ERN_Old"]
MARK = [("ICD","Diagnoses: ICD-10"),("CPT","CPT 1013626"),("VAG","estradiol"),
        ("C50","ICD-10-CM C50"),("Z85","Z85.3"),("Z170","Z17.0"),("Z171","Z17.1"),
        ("ET","tamoxifen")]
FP = {  # title -> must/cannot/operator fingerprint
 "In_Care":"11000000/00000000/OR", "VE_Denom":"11000000/00000000/OR",
 "WASHOUT_VE":"00000000/00100000/-", "VE_Num":"00100000/00000000/-",
 "HA":"00011000/00000000/OR", "C50":"00010000/00000000/-", "Hx":"00001000/00000000/-",
 "No_HA":"00000000/00011000/OR", "No_C50":"00000000/00010000/-", "No_Hx":"00000000/00001000/-",
 "ERPos":"00000101/00000010/OR", "ERNeg":"00000010/00000101/OR",
 "ERAmbig":"00000110/00000000/AND","ERUnrec":"00000000/00000110/OR",
 "ERP_Old":"00000100/00000010/-", "ERN_Old":"00000010/00000100/-"}
HUMAN = {
 "In_Care":"must: ICD-10 dx OR CPT 1013626 office visit",
 "VE_Denom":"must: ICD-10 dx OR CPT 1013626 office visit",
 "WASHOUT_VE":"cannot: estradiol [Vaginal Product]",
 "VE_Num":"must: estradiol [Vaginal Product]",
 "HA":"must: C50 OR Z85.3", "C50":"must: C50", "Hx":"must: Z85.3",
 "No_HA":"cannot: C50 OR Z85.3","No_C50":"cannot: C50","No_Hx":"cannot: Z85.3",
 "ERPos":"must: Z17.0 OR tamoxifen OR anastrozole OR letrozole OR exemestane; cannot: Z17.1",
 "ERNeg":"must: Z17.1; cannot: Z17.0 OR the four endocrine agents",
 "ERAmbig":"must: Z17.1 AND Z17.0","ERUnrec":"cannot: Z17.1 OR Z17.0",
 "ERP_Old":"must: Z17.0; cannot: Z17.1","ERN_Old":"must: Z17.1; cannot: Z17.0"}

def parse_name(n):
    m = re.match(r'^BCa-('+"|".join(COH)+r')_∩_(?:('+"|".join(STR)+r')_)?((?:prev_)?(?:num|denom))_(2[45])_(Nov|Jun)$', n)
    if not m: return None
    co, st, met, yy, mo = m.groups()
    return {"cohort":co, "stratum":st or "", "metric":met, "yy":yy, "mon":mo}

def windows(yy, mon):
    y = int(yy)
    if mon == "Nov":
        idx = "between Nov 01, 20%d and Mar 31, 20%d" % (y, y+1)
        care= "between Nov 01, 20%d and Mar 31, 20%d" % (y-1, y)
        cut = "on or before Oct 31, 20%d" % y
    else:
        idx = "between Jun 01, 20%d and Oct 31, 20%d" % (y, y)
        care= "between Jun 01, 20%d and Oct 31, 20%d" % (y-1, y-1)
        cut = "on or before May 31, 20%d" % y
    return idx, care, cut

def expected(name):
    """-> ordered [(title, fingerprint, window, human)] or None if the name is unparseable."""
    p = parse_name(name)
    if not p: return None
    idx, care, cut = windows(p["yy"], p["mon"])
    is_prev = p["metric"].startswith("prev_")
    is_num  = p["metric"].endswith("num")
    out = [("In_Care", care)]
    if not is_prev: out.append(("WASHOUT_VE", cut))
    out.append(("VE_Denom", idx))
    if p["cohort"] != "Unstrat": out.append((p["cohort"], cut))
    if is_num: out.append(("VE_Num", idx))
    if p["stratum"]: out.append((p["stratum"], cut))
    return [(t, FP[t], w, HUMAN[t]) for t, w in out]

# ---------- reading an actual dump row ----------
def _clean(s):
    """Accept either the displayed cell text or the ="..."&CHAR(10)&"..." formula."""
    s = str(s)
    if not s.startswith("="):
        return s
    s = re.sub(r'^=', '', s).strip('"')
    s = s.replace('"&CHAR(10)&"', '\n').replace('&CHAR(10)&', '\n')
    # Some tabs hold rows whose CHAR(10)s were lost on paste, leaving bare
    # &"-concatenation. That join is the line break too.
    s = s.replace('"&"', '\n')
    return s.replace('""', '"')

def fingerprint(cell):
    must = re.search(r'Must have:([\s\S]*?)(?:Cannot have:|$)', cell)
    cant = re.search(r'Cannot have:([\s\S]*)', cell)
    def bits(b):
        b = b.group(1) if b else ""
        return "".join("1" if m[1] in b else "0" for m in MARK)
    op = "AND" if re.search(r'(?m)^AND ', cell) else ("OR" if re.search(r'(?m)^OR ', cell) else "-")
    return bits(must) + "/" + bits(cant) + "/" + op

TITLES = set(FP)

def actual(row):
    """dump row -> [(title, fingerprint, window)].

    Column layout is NOT fixed: tabs differ in whether the =$A$n helper columns
    are present, so a fixed stride silently reads the date cell as a group. Find
    the cells by what they contain instead — a group cell's first line is a known
    group title; a window is the next 'occurred ...' cell after it."""
    cells = [_clean(c).strip() for c in row]
    groups = []
    for i, cell in enumerate(cells):
        if not cell or cell in ("–", "-"): continue
        title = cell.split("\n")[0].strip().strip('"')
        if title not in TITLES: continue
        if "Must have" not in cell and "Cannot have" not in cell: continue
        win = ""
        for j in range(i+1, min(i+4, len(cells))):
            m = re.search(r'occurred ([^\n]+)', cells[j])
            if m: win = m.group(1).strip(); break
        groups.append((title, fingerprint(cell), win))
    return groups

def check(row):
    """-> (ok, [problems])"""
    name = _clean(row[0]).strip()
    exp = expected(name)
    if exp is None: return (None, ["name does not match the BCa grammar"])
    act = actual(row)
    probs = []
    if len(act) != len(exp):
        probs.append("%d groups, expected %d (%s)" % (len(act), len(exp), " → ".join(t for t,_,_,_ in exp)))
    for i in range(max(len(act), len(exp))):
        e = exp[i] if i < len(exp) else None
        a = act[i] if i < len(act) else None
        if e and not a: probs.append("group %d missing: %s" % (i+1, e[0])); continue
        if a and not e: probs.append("group %d unexpected: %s" % (i+1, a[0])); continue
        if a[0] != e[0]: probs.append("group %d titled %s, expected %s" % (i+1, a[0], e[0])); continue
        if a[1] != e[1]:
            why = []
            if a[1].split("/")[0] != e[1].split("/")[0]: why.append("must-have terms")
            if a[1].split("/")[1] != e[1].split("/")[1]: why.append("cannot-have terms")
            if a[1].split("/")[2] != e[1].split("/")[2]: why.append("AND/OR (%s not %s)" % (a[1].split("/")[2], e[1].split("/")[2]))
            probs.append("%s: wrong %s" % (e[0], " and ".join(why)))
        if a[2] != e[2]: probs.append("%s: window %r, expected %r" % (e[0], a[2], e[2]))
    return (len(probs) == 0, probs)
