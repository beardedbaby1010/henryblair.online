# -*- coding: utf-8 -*-
"""Check each project page against the numbers in its submitted abstract.

MOST_ABSTRACTS.txt is the authoritative source: these are the strings the
abstracts actually print. For each page we ask only "does the page contain
this number anywhere" -- a miss is something to look at by hand, not
necessarily an error, because a page may legitimately not mention a stat.
"""
import html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# slug -> list of (what it is, the string the abstract prints)
CHECKS = {
 "nsqip-opioids": [
   ("cohort", "59,773"), ("with opioid n", "33,110"), ("with opioid %", "55.4"),
   ("TURBT low", "26.0"), ("kidney high", "79.1"),
   ("endoscopic", "26.9"), ("open", "65.7"), ("MIS", "75.1"),
   ("age>=70", "45.3"), ("age<70", "62.2"),
   ("women", "62.4"), ("men", "53.8"),
   ("inpatient", "61.3"), ("outpatient", "51.5"),
   ("readmit opioid", "5.8"), ("readmit none", "6.2"),
   ("TURBT readmit", "5.7"), ("RP readmit", "4.1"),
 ],
 "nsqip-same-day-discharge": [
   ("cohort", "119,220"), ("sdd n", "7,088"), ("sdd %", "5.9"),
   ("2019", "1.9"), ("2024", "15.6"), ("elderly from", "0.6"), ("elderly to", "8.2"),
   ("readmit sdd", "3.3"), ("readmit overnight", "4.2"), ("RR", "0.78"),
   ("RR lo", "0.69"), ("RR hi", "0.89"),
   ("compl sdd", "5.0"), ("compl overnight", "6.4"),
   ("reop sdd", "0.5"), ("reop overnight", "1.1"),
   ("era RR", "1.02"), ("era lo", "0.97"), ("era hi", "1.08"),
 ],
 "nsqip-bph-bleeding": [
   ("cohort", "123,020"), ("TURP", "82,020"), ("PVP", "31,087"), ("HoLEP", "9,913"),
   ("HoLEP share from", "5.8"), ("HoLEP share to", "14.8"),
   ("PVP transfusion", "0.25"), ("TURP transfusion", "0.90"),
   ("PVP RR", "0.28"), ("PVP lo", "0.22"), ("PVP hi", "0.35"),
   ("PVP composite", "1.4"), ("TURP composite", "2.6"),
   ("HoLEP bleed", "2.5"), ("HoLEP serious", "1.4"), ("TURP serious", "1.7"),
   ("HoLEP readmit", "4.1"), ("TURP readmit", "5.3"),
   ("TURP trend from", "1.7"), ("TURP trend to", "0.6"),
   ("HoLEP trend p", "0.049"),
 ],
 "nsqip-colpopexy": [
   ("cohort", "12,623"), ("SCP", "7,589"), ("SSLF", "5,034"),
   ("concomitant SCP", "89"), ("concomitant SSLF", "94"),
   ("compl SCP", "6.6"), ("compl SSLF", "8.8"),
   ("reop SCP", "0.9"), ("reop SSLF", "1.5"),
   ("stay SCP", "5.4"), ("stay SSLF", "14.0"),
   ("serious SCP", "1.4"), ("serious SSLF", "1.3"), ("readmit", "1.9"),
   ("UTI SCP", "3.6"), ("UTI SSLF", "5.1"),
   ("UTI RR", "0.70"), ("UTI lo", "0.60"), ("UTI hi", "0.83"),
   ("sub RR", "0.56"), ("sub lo", "0.41"), ("sub hi", "0.77"),
 ],
 "nsqip-rasp-vs-osp": [
   ("cohort", "3,033"), ("RASP n", "2,580"), ("RASP %", "85.1"),
   ("2022", "73.2"), ("2024", "91.2"),
   ("transfusion RASP", "1.8"), ("transfusion OSP", "18.3"),
   ("RR", "0.10"), ("RR lo", "0.07"), ("RR hi", "0.14"),
   ("compl RASP", "11.2"), ("compl OSP", "28.0"),
   ("readmit RASP", "5.5"), ("readmit OSP", "8.2"),
   ("reop RASP", "1.6"), ("reop OSP", "4.2"),
   ("wound RASP", "0.9"), ("wound OSP", "2.6"),
   ("AKI RASP", "0.7"),
 ],
 "nsqip-rasp-elderly": [
   ("cohort", "2,580"), ("elderly n", "691"), ("elderly %", "26.8"),
   ("frail n", "519"), ("frail %", "20.5"), ("both n", "182"), ("both %", "7.2"),
   ("compl old", "13.5"), ("compl young", "10.3"), ("RR", "1.3"),
   ("RR lo", "1.03"), ("RR hi", "1.64"),
   ("transfusion old", "3.2"), ("transfusion young", "1.3"),
   ("nonhome old", "2.0"), ("nonhome young", "0.6"),
   ("stay old", "32.9"), ("stay young", "25.8"),
   ("serious old", "3.8"), ("serious young", "3.4"),
   ("readmit old", "5.6"), ("readmit young", "5.5"),
   ("frail stay", "36.0"), ("nonfrail stay", "25.6"), ("mortality", "0.1"),
 ],
 "urogyn-perceptions": [
   ("respondents", "115"),
   ("exposure OR", "1.96"), ("exposure p", "0.018"),
   ("formal yes", "77.4"), ("formal no", "58.1"), ("formal p", "0.028"),
   ("formal adj OR", "6.07"), ("formal adj p", "0.020"),
   ("level OR", "0.62"), ("level p", "0.003"),
   ("satisfaction OR", "3.55"), 
   ("exposure by yr3", "73"), ("no exposure", "17"),
   ("URPS faculty", "77"), ("institutional fellowship", "37"),
   ("defined role", "90"),
   ("mid-residency OR", "23.26"), ("undecided OR", "57.45"),
   ("mentorship p", "0.071"),
   ("other subspecialty", "65"), ("narrowed scope", "33"), ("limited exposure", "30"),
   ("freetext n", "58"), ("theme exposure", "40"), ("theme structure", "21"),
   ("theme scope", "19"), ("theme nonmod", "17"),
   ("no-faculty OR", "3.53"), ("no-faculty p", "0.011"),
   ("mentorship OR", "5.40"), ("mentorship OR p", "0.004"),
 ],
 "ketamine-cystitis": [
   ("admissions", "4,020"), ("rise", "140"),
   ("2016 rate", "1.22"), ("2021 rate", "2.92"),
   ("mean age", "41.5"), ("male", "66.5"), ("medicaid", "52.2"),
   ("urban teaching", "80.3"), ("DEA reports", "11,329"),
   ("retail increase", "350"), ("clinics", "300"),
 ],
 "adt-initiation": [
   ("TriNetX patients", "67.2"), ("ADT starters", "28,524"), ("mCSPC", "5,998"),
   ("intensified", "45.0"), ("ARPI only", "36.1"), ("docetaxel only", "6.4"),
   ("both", "2.5"),
   ("2017", "33.9"), ("2023", "52.4"), ("RR", "1.55"), ("RR lo", "1.36"), ("RR hi", "1.76"),
   ("ARPI from", "21.7"), ("ARPI to", "48.1"), ("ARPI RR", "2.21"),
   ("docetaxel from", "12.9"), ("docetaxel to", "9.4"), ("docetaxel RR", "0.73"),
   ("era RR", "1.28"), ("era lo", "1.19"), ("era hi", "1.39"),
   ("triplet from", "0.7"), ("triplet to", "5.1"),
   ("abiraterone 2017", "78.4"), ("abiraterone 2023", "55.7"),
   ("visceral", "45.4"), ("nonvisceral", "44.9"), ("visceral RR", "1.01"),
   ("sustained ADT", "25,640"), ("DXA 1yr", "13.1"), ("unscreened 5yr", "70.1"),
   ("osteoporosis PR", "3.58"), ("osteo lo", "3.12"), ("osteo hi", "4.11"),
   ("prior screening PR", "6.34"),
   ("bone disease screened", "23.5"), ("no bone disease", "12.4"), ("bone RR", "1.89"),
   ("antiresorptive RR", "2.69"), ("fracture RR", "2.28"),
   ("yr1 fracture prompt", "3.4"), ("yr1 fracture never", "1.3"), ("yr1 RR", "2.52"),
   ("matched RR", "1.03"), ("matched lo", "0.85"), ("matched hi", "1.26"),
 ],
 "ve-boxed-warning": [
   ("new starts from", "16.7"), ("new starts to", "39.0"),
   ("pre-trend", "25.8"), ("pre lo", "23.1"), ("pre hi", "28.6"),
   ("level", "0.5"), ("level p", "0.92"),
   ("slope", "54.5"), ("slope p", "0.010"),
   ("prevalent", "46.7"), ("prevalent p", "0.002"),
   ("calibrated", "43.8"), ("cal lo", "0.7"), ("cal hi", "105.2"),
   ("initiation after", "48"), ("initiation before", "21"),
   ("ring from", "12.0"), ("ring to", "8.0"), ("ring RR", "0.67"), ("cream", "49.8"),
   ("bc frequency", "34.4"), ("nobc frequency", "21.0"), ("freq PR", "1.64"),
   ("bc UTI", "47.5"), ("nobc UTI", "35.5"), ("UTI PR", "1.34"),
   ("bc dyspareunia", "12.6"), ("nobc dyspareunia", "8.6"), ("dysp PR", "1.47"),
   ("bc atrophic", "44.7"), ("nobc atrophic", "36.3"), ("atrophic PR", "1.23"),
   ("bc RR before", "0.72"), ("bc RR after", "0.77"),
   ("ER RR before", "0.94"), ("ER RR after", "0.98"),
   ("white before", "74.3"), ("white after", "109.5"),
   ("black before", "34.6"), ("black after", "53.2"),
   ("bw RR before", "0.46"), ("bw lo", "0.45"), ("bw hi", "0.48"),
   ("bw RR after", "0.49"), ("bw after lo", "0.47"), ("bw after hi", "0.50"),
   ("asian before", "0.69"), ("asian after", "0.65"),
   ("aian before", "0.83"), ("aian after", "0.79"),
   ("hispanic before", "0.87"), ("hispanic after", "0.98"),
   ("gap before", "39.8"), ("gap after", "56.4"), ("gap widening", "42"),
 ],
}

def text_of(path):
    s = open(path, encoding="utf-8").read()
    s = re.sub(r"<script.*?</script>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<style.*?</style>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s)

total = miss = 0
for slug, items in sorted(CHECKS.items()):
    p = os.path.join(ROOT, "projects", slug, "index.html")
    if not os.path.exists(p):
        print("MISSING PAGE %s" % slug); continue
    body = text_of(p)
    gone = [(w, v) for w, v in items if v not in body]
    total += len(items); miss += len(gone)
    print("%-26s %2d/%2d present" % (slug, len(items) - len(gone), len(items)))
    for w, v in gone:
        print("      absent: %-24s %s" % (w, v))
print("\n%d/%d abstract values found on their pages (%d to look at)"
      % (total - miss, total, miss))
