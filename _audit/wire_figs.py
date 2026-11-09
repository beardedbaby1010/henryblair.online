# -*- coding: utf-8 -*-
"""Put every pipeline figure on its project page, with the title it draws."""
import io, re

FIGS = {
 "nsqip-opioids": [
  ("Figure_1.png", "Opioid prescription at discharge by procedure category.", None),
  ("Figure_1_horizontal.png", "The same comparison, drawn horizontally so the longer "
   "procedure labels sit in full.", "layout variant"),
  ("Figure_1b.png", "Prescription and prescription size together: <b>A</b> the share "
   "discharged with an opioid, <b>B</b> the size of that prescription in oral morphine "
   "milligram equivalents, by procedure category.", None),
  ("Figure_1c.png", "Opioid prescription at discharge by procedure category.",
   "layout variant"),
  ("Figure_1d.png", "Prescription and prescription size by procedure category.",
   "layout variant"),
  ("Figure_2.png", "Opioid prescription at discharge by surgical approach — "
   "endoscopic, open, minimally invasive.", None),
  ("Figure_3.png", "Opioid prescription at discharge by patient subgroup.", None),
  ("Figure_3_horizontal.png", "The same subgroups, drawn horizontally.", "layout variant"),
  ("Figure_4.png", "Prescriptions above 200 oral morphine milligram equivalents, by "
   "patient subgroup — the secondary outcome.", None),
 ],
 "nsqip-bph-bleeding": [
  ("Figure_1.png", "Transfusion within 72 hours after BPH surgery, by year and procedure.", None),
  ("Figure_1b.png", "The same series, 2019–2024.", "layout variant"),
  ("Figure_2.png", "Share of BPH procedures by year and procedure type — how the "
   "mix moved over thirteen years.", None),
  ("Figure_3.png", "Thirty-day outcomes after HoLEP and PVP compared with TURP. "
   "<b>A</b> HoLEP vs TURP, <b>B</b> PVP vs TURP.", None),
  ("Figure_3_before_footnote.png", "The same forest plot carrying each arm's rates "
   "beside the risk ratio.", "layout variant"),
  ("Figure_3b.png", "Thirty-day complications after HoLEP and PVP compared with TURP, "
   "complication by complication.", None),
  ("Figure_4.png", "Transfusion within 72 hours, 2019–2024 against 2012–2018, "
   "by procedure — the era comparison behind the trend.", None),
 ],
 "nsqip-same-day-discharge": [
  ("Figure_1_forest.png", "Thirty-day outcomes, same-day discharge against overnight "
   "stay.", None),
  ("Figure_2_rates.png", "Overlap-weighted 30-day outcome rates, which hold the "
   "measured case mix fixed between the two groups.", None),
 ],
 "nsqip-rasp-vs-osp": [
  ("Figure_1.png", "Robot-assisted share of simple prostatectomy by year "
   "(Cochran–Armitage trend z = 9.83, p &lt; 0.001).", None),
  ("Figure_2.png", "Transfusion within 72 hours after simple prostatectomy, by year "
   "and approach.", None),
  ("Figure_3.png", "Thirty-day outcomes after simple prostatectomy, RASP against OSP.", None),
  ("Figure_4.png", "The same outcomes within each subgroup — anaesthesia risk "
   "class, frailty, age, obesity, anaemia.", None),
  ("Figure_5.png", "Thirty-day complications after simple prostatectomy, complication "
   "by complication.", None),
 ],
 "nsqip-rasp-elderly": [
  ("Figure_1.png", "The cohort by age and frailty: <b>A</b> the four groups, <b>B</b> "
   "the age distribution within each frailty stratum.", None),
  ("Figure_2.png", "Thirty-day complications, age 75 and over against under 75.", None),
  ("Figure_3.png", "Thirty-day complications, frail (mFI-5 ≥ 2) against not frail.", None),
  ("Figure_4.png", "Thirty-day complications, men who are both old and frail against "
   "men who are neither.", None),
  ("Figure_5.png", "Prostatectomy-specific complications by age, among cases in the "
   "procedure-targeted file.", None),
  ("Figure_6.png", "Prostatectomy-specific complications by frailty.", None),
  ("Figure_7.png", "Prostatectomy-specific complications, both against neither.", None),
  ("Figure_8.png", "Thirty-day outcomes by age and frailty, as one forest plot.", None),
  ("Figure_9.png", "Complications and resource use across the four age-and-frailty "
   "groups.", None),
  ("Figure_10.png", "Serious complications, infection, readmission and reoperation "
   "across the same four groups.", None),
  ("Figure_11.png", "Prostatectomy-specific complications across the four groups.", None),
  ("Figure_12.png", "Thirty-day outcomes by frailty score, mFI-5 from 0 to 3 or more "
   "— frailty as a gradient rather than a threshold.", None),
 ],
 "nsqip-colpopexy": [
  ("Figure_1.png", "Sacrocolpopexy and sacrospinous ligament fixation cases by year, "
   "with the robotic share of SCP.", None),
  ("Figure_2.png", "Thirty-day urinary tract infection by year and procedure.", None),
  ("Figure_3.png", "Thirty-day outcomes, robotic sacrocolpopexy against sacrospinous "
   "ligament fixation.", None),
  ("Figure_4.png", "The same outcomes by subgroup — isolated procedures against "
   "those with any concurrent procedure, which is where the UTI difference is "
   "interrogated.", None),
  ("Figure_5.png", "Individual 30-day complications, robotic SCP against SSLF.", None),
  ("Figure_6.png", "Thirty-day outcomes under each cohort definition — how much "
   "the result depends on who is counted.", None),
  ("Figure_7.png", "Thirty-day urinary tract infection by subgroup.", None),
 ],
}


def section(slug):
    blocks = []
    for src, cap, note in FIGS[slug]:
        n = int(re.search(r"(\d+)", src).group(1))
        label = src.replace("Figure_", "Figure ").replace(".png", "").replace("_", " ")
        caption = "<b>%s.</b> %s%s" % (
            label, cap,
            (" <i>(%s)</i>" % note) if note else "")
        blocks.append({"figure": {"src": src, "alt": cap[:110], "caption": caption}})
    return {"id": "figures", "title": "Figures", "nav": "Figures",
            "tag": "%d" % len(FIGS[slug]),
            "intro": "Produced by the "
                     "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a> from this "
                     "project's workbook, and recoloured onto the site's palette. Every "
                     "value drawn here is a cell in that workbook.",
            "blocks": blocks}


def insert(src_text, slug):
    """Add the figures section to this project's hub dict."""
    i = src_text.find('"slug": "%s"' % slug)
    if i < 0:
        return src_text, "NOT FOUND"
    h = src_text.find('"hub": {', i)
    nxt = src_text.find('"slug": "', i + 20)
    if h < 0 or (nxt > 0 and h > nxt):
        return src_text, "no hub"
    if '"id": "figures"' in src_text[i:(nxt if nxt > 0 else len(src_text))]:
        return src_text, "already"
    at = h + len('"hub": {')
    body = "\n            \"sections\": [\n                %r,\n            ]," % (section(slug),)
    return src_text[:at] + body + src_text[at:], "inserted %d figure(s)" % len(FIGS[slug])


if __name__ == "__main__":
    p = "projects.py"
    s = io.open(p, encoding="utf-8").read()
    for slug in FIGS:
        s, msg = insert(s, slug)
        print("  %-26s %s" % (slug, msg))
    # the nocturia abstract was submitted, not merely prepared
    s = s.replace("abstract prepared for the 2027 AUA Annual Meeting",
                  "abstract submitted to the 2027 AUA Annual Meeting")
    io.open(p, "w", encoding="utf-8").write(s)
    import py_compile
    py_compile.compile(p, doraise=True)
    print("\nprojects.py compiles.")
