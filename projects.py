#!/usr/bin/env python3
"""
projects.py — the single source of truth for henryblair.online.

Everything the site shows about a project lives here: the copy, the numbers on
its card, where its page comes from, and which manuscript sits behind the
passphrase gate. build_site.py reads this file and writes the site.

Re-pointing a project at a new file is a one-line edit here plus `./publish`.
Paths starting with ~ are expanded; paths outside the repo are fine (the build
copies or encrypts what it needs and never commits the source).

If a path is missing, the build says so and keeps going — the card still
renders, it just loses the link. Nothing silently half-builds.
"""

# ---------------------------------------------------------------- where source folders live
# Project sources (manuscripts, hubs, figures) are named relative to these roots;
# the first root that contains the file wins. Move Maimo_Work somewhere else and
# you change one line here, not ten paths below.
SOURCE_ROOTS = [
    "~/Documents",
    "~/mnt",          # the folder mounts used when Claude builds the site
]

# ---------------------------------------------------------------- downloads
# Anything dropped in _downloadable/ is published at /downloads/<same name>.
# These patterns additionally publish the NEWEST match under a fixed URL, so links
# that are already out in the world keep working when a new version lands.
DOWNLOAD_ALIASES = {
    "Henry_Blair_CV_*.pdf": "Henry-Blair-CV.pdf",
}

# Downloads that require a passphrase. A file listed here is published ONLY as a
# passphrase page at /downloads/<name>/ — the raw file is never copied into the
# site, so there is no unprotected URL. Give each one a passphrase in
# _secrets/passwords.txt, keyed by the same file name.
# ------------------------------------------------------- fully private pages
# A page whose whole content is encrypted. The published file is ciphertext, so
# the working notes below are not readable by anyone without a passphrase. The
# source lives in _source/ and is never committed.
PAGE_GATES = {
    "in-preparation": {
        "source": "_source/in-preparation.html",
        "dir": "in-preparation",
        "title": "In preparation",
        "subtitle": "Working notes \u2014 what needs doing to reach submission",
        "note": "These are my own notes rather than a public page. ",
        "back_url": "/", "back_label": "back to the portfolio",
    },
}

# ------------------------------------------------------- passphrase-gated embeds
# Video and other media that is too large to live in this repository. What gets
# encrypted is the embed address itself, so it is not in the page source until
# someone enters a passphrase; then it plays in place at /watch/<key>/.
# Give each key a passphrase in _secrets/passwords.txt (the masterkey always works).
EMBED_GATES = {
    "aua-snm-video": {
        "url": "https://share.descript.com/embed/MudR8c10Jra",
        "title": "Sacral Neuromodulation Placement",
        "subtitle": "AUA Core Curriculum teaching video · 7:58 · submitted August 31st, 2026",
        "note": "Under review by the AUA. ",
        "back_url": "/projects/aua-core-videos/", "back_label": "back to the project",
    },
    "aua-pessary-video": {
        "url": "https://share.descript.com/embed/t1mErexxxMb",
        "title": "Vaginal Pessaries: Types and Fitting",
        "subtitle": "AUA Core Curriculum teaching video · 7:09 · submitted August 31st, 2026",
        "note": "Under review by the AUA. ",
        "back_url": "/projects/aua-core-videos/", "back_label": "back to the project",
    },
}

DOWNLOAD_GATES = {
    "urps-exposure-manuscript.pdf": {
        "title": "Exposure Isn\u2019t Everything: What Drives Urology Resident Interest in URPS?",
        "subtitle": "Manuscript \u00b7 national survey of US urology residents",
        "back_url": "/projects/urogyn-perceptions/", "back_label": "back to the project"},
    "urps-who-owns-manuscript.pdf": {
        "title": "Who Owns Urogynecology and Reconstructive Pelvic Surgery, and Can We All Get Along?",
        "subtitle": "Manuscript \u00b7 national survey of US urology residents",
        "back_url": "/projects/urogyn-perceptions/", "back_label": "back to the project"},
    "urps-why-not-manuscript.pdf": {
        "title": "Why Not URPS? Barriers and Facilitators to Fellowship Interest",
        "subtitle": "Manuscript \u00b7 national survey of US urology residents",
        "back_url": "/projects/urogyn-perceptions/", "back_label": "back to the project"},
    "abstract-nocturia-patient-goals.pdf": {
        "title": "What Do Patients with Nocturia Want Treated? Patient-Defined Goals and Tolerance Beyond Void Count",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Urodynamics/Lower Urinary Tract Dysfunction/Female Pelvic Medicine",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-adt-bone-density-screening.pdf": {
        "title": "Bone-density screening is triggered by prior bone disease rather than androgen-deprivation therapy itself",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Health Services Research: Quality Improvement & Patient Safety",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-adt-intensification-trends.pdf": {
        "title": "Trends in treatment intensification for metastatic castration-sensitive prostate cancer in men aged 70 or older, 2017-2023",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Prostate Cancer: Advanced (including drug therapy)",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-ketamine-cystitis.pdf": {
        "title": "Tracing the Ketamine: Illicit Supply, Medical Access, and the Epidemiology of Ketamine Cystitis",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Infections/Inflammation/Cystic Disease of the Genitourinary Tract: Kidney & Bladder",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-nsqip-bph-bleeding.pdf": {
        "title": "National Trends in Bleeding and Perioperative Outcomes After TURP, Photoselective Vaporization, and HoLEP: An ACS NSQIP Analysis, 2012–2024",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Benign Prostatic Hyperplasia: Surgical Therapy & New Technology",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-nsqip-colpopexy.pdf": {
        "title": "Robotic Sacrocolpopexy Versus Transvaginal Sacrospinous Ligament Fixation, Comparison of Urinary Tract Infections and Perioperative Complications: An ACS NSQIP Analysis, 2022–2024",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Urodynamics/Lower Urinary Tract Dysfunction/Female Pelvic Medicine: Female Pelvic Organ Prolapse and Reconstructive Surgery (including non-trauma related fistula and urethral diverticulum)",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-nsqip-opioids-at-discharge.pdf": {
        "title": "Half Leave With Opioids: Is Urologic Surgery Overprescribing Pain Medication? An ACS NSQIP Analysis of 2024 Data",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Health Services Research: Quality Improvement & Patient Safety",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-nsqip-rasp-elderly-frail.pdf": {
        "title": "Too Old or Too Frail for Robot-Assisted Enucleation Prostatectomy? An ACS NSQIP Analysis, 2022–2024",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Health Services Research: Quality Improvement & Patient Safety",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-nsqip-rasp-vs-osp.pdf": {
        "title": "The Rapid Rise of Robot-Assisted Simple Prostatectomy, Less Blood, Fewer Complications: National Utilization Trends and Perioperative Outcomes, 2022-2024",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Benign Prostatic Hyperplasia: Surgical Therapy & New Technology",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-nsqip-same-day-discharge.pdf": {
        "title": "Home the Same Day, No Harm Done? The National Shift Toward Same-Day Discharge After Robotic Prostatectomy: An ACS NSQIP Analysis, 2012–2024",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Health Services Research: Quality Improvement & Patient Safety",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-pediatric-ebike-gu-trauma.pdf": {
        "title": "National Trends in Pediatric Bicycle-Associated Genitourinary Trauma Amid the Rise of E-Bikes",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Pediatrics: Tumors, Trauma & Transplantation",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-urps-exposure.pdf": {
        "title": "Exposure isn't everything: What drives urology resident interest in Urogynecology and Reconstructive Pelvic Surgery",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Education Research",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-urps-who-owns.pdf": {
        "title": "Who owns Urogynecology and Reconstructive Pelvic Surgery, and can we all get along?",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Urodynamics/Lower Urinary Tract Dysfunction/Female Pelvic Medicine: Female Pelvic Organ Prolapse and Reconstructive Surgery (including non-trauma related fistula and urethral diverticulum)",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-urps-why-not.pdf": {
        "title": "Why not Urogynecology and Reconstructive Pelvic Surgery? Barriers and facilitators to fellowship interest among current United States urology residents",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Expanding the Urology Workforce",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-ve-breast-cancer-undertreatment.pdf": {
        "title": "Overburdened and undertreated: Breast cancer patients carry the highest genitourinary symptom burden but the lowest vaginal estrogen use.",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Sexual Function/Dysfunction: Medical, Hormonal & Non-surgical Therapy",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-ve-fda-announcement.pdf": {
        "title": "Vaginal estrogen prescribing accelerated after the Food and Drug Administration boxed-warning announcement, independent of formulation labeling",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Health Policy Research",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-ve-racial-treatment-gap.pdf": {
        "title": "Rise in vaginal estrogen use after the FDA announcement widened the absolute racial treatment gap",
        "subtitle": "Abstract · 2027 AUA Annual Meeting · Improving Access and Outcomes Across All Populations",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-sufu-ve-fda-announcement.pdf": {
        "title": "Vaginal estrogen prescribing before and after the FDA announcement on removing boxed warnings",
        "subtitle": "Abstract \u00b7 2027 SUFU Winter Meeting",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-sufu-ve-breast-cancer-burden.pdf": {
        "title": "Breast cancer: overburdened and undertreated \u2014 highest genitourinary symptom burden and lowest vaginal estrogen use",
        "subtitle": "Abstract \u00b7 2027 SUFU Winter Meeting",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-sufu-ve-receptor-status.pdf": {
        "title": "Vaginal estrogen underuse after breast cancer is independent of receptor status",
        "subtitle": "Abstract \u00b7 2027 SUFU Winter Meeting",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "abstract-sufu-ve-formulation.pdf": {
        "title": "Announcement, not label: vaginal estrogen prescribing after recent FDA actions is not formulation-specific",
        "subtitle": "Abstract \u00b7 2027 SUFU Winter Meeting",
        "back_url": "/abstracts/", "back_label": "back to the abstracts"},
    "2024-maude-msre-poster.pdf": {
        "title": "Analysis of adverse events, robotic urological surgeries",
        "subtitle": "Conference poster · Society of Urologic Robotic Surgeons Focal Therapy, 2024",
        "back_url": "/projects/maude-sealing-devices/", "back_label": "back to the project",
    },
    "Henry_Blair_CV_2026_Nov.pdf": {
        "title": "Curriculum vitae — Henry M. Blair",
        "subtitle": "Updated November 2026",
        "back_url": "/resume/", "back_label": "back to the resume",
    },
}

# ---------------------------------------------------------------- hand-written pages
PAGES = [
    {"key": "about",   "tab": "About Me",           "href": "/about/",   "file": "about/index.html"},
    {"key": "contact", "tab": "Contact Me",         "href": "/contact/", "file": "contact/index.html"},
    {"key": "resume",  "tab": "Resume",             "href": "/resume/",  "file": "resume/index.html"},
    {"key": "home",    "tab": "Research Portfolio", "href": "/",         "file": "index.html"},
    {"key": "abstracts", "tab": "Abstracts",     "href": "/abstracts/", "file": "abstracts/index.html"},
    {"key": "earlier",   "tab": "Earlier Work",  "href": "/earlier/",   "file": "earlier/index.html"},
    {"key": "in-preparation", "tab": "In Preparation", "href": "/in-preparation/",
     "file": "in-preparation/index.html", "gate": True},
]

# ---------------------------------------------------------------- projects
# "page"  : how the project page is produced
#           {"kind": "generated", "source": ..., "strip_paper": True}  built from a self-contained hub
#           {"kind": "static"}                                          hand-written at projects/<slug>/index.html
#           None                                                        card only, no page and no tab
# "paper" : the manuscript to put behind a passphrase (per-project passphrase
#           in _secrets/passwords.json, which git ignores). Omit for none.

PROJECTS = [

    # ============================================================ current work

    {
        "slug": "adt-initiation", "tab": "ADT Initiation", "group": "current",
        "title": "The Missed Moment of ADT Initiation",
        "kicker": "Retrospective aggregate cohort study · TriNetX US Collaborative Network",
        "status": "Manuscript V7 · in preparation",
        "summary": "When an older man starts androgen-deprivation therapy for prostate cancer, one moment "
                   "carries two guideline duties: monitor his bones, and—if the cancer is already "
                   "metastatic—intensify treatment. Examined together in one population, both duties fail "
                   "at the same moment.",
        "stats": [("69.3%", "never receive a central bone scan"),
                  ("41.1%", "intensified when metastatic"),
                  ("3.6×",  "screening tracks prior bone disease"),
                  ("35,851","men on ADT")],
        "tags": ["Prostate cancer", "ADT", "Bone health", "Treatment intensification", "TriNetX"],
        "page": {"kind": "generated", "source": "_source/pca_project_hub_standalone.html", "strip_paper": True},
        "paper": {"pdf": "Maimo_Work/5_PCa_x_ADT/Old/Henry - PCa Manuscript V7.pdf",
                  "label": "Manuscript V7", "note": "In preparation."},
    },

    {
        "slug": "ve-boxed-warning", "tab": "Vaginal Estrogen", "group": "current",
        "title": "Prescribing After the Warning Disappeared",
        "kicker": "Retrospective cohort study · TriNetX Global Collaborative Network",
        "status": "Manuscript V3",
        "summary": "For twenty-two years low-dose vaginal estrogen carried the same boxed warning as "
                   "high-dose systemic hormone therapy. The FDA removed it on 11 November 2025. Nine months "
                   "on either side of that date, prescribing rose — and it rose most in the women the "
                   "warning had most deterred.",
        "stats": [("+14.3%", "use per woman seen"),
                  ("1.29",   "rate ratio in breast-cancer survivors"),
                  ("1.47 / 0.88", "positive vs negative controls"),
                  ("192,157","women on vaginal estrogen")],
        "tags": ["Menopause", "GSM", "FDA labeling", "Pharmacoepidemiology", "Breast cancer", "TriNetX"],
        "page": {"kind": "static"},
        "paper": {"pdf": "Maimo_Work/3_VE/Old/Old_Manuscripts/Henry - VE Manuscript V3.pdf",
                  "label": "Manuscript V3", "note": "Co-authored with Dr. Arshia Sandozi."},
    },

    {
        "slug": "oab-pvr", "tab": "PVR Self-Estimation", "group": "current",
        "title": "Can women self-estimate their post-void residual?",
        "kicker": "Cross-sectional study · Department of Urogynecology, Maimonides Medical Center",
        "status": "Submitted — Family Practice (Oxford University Press)",
        "summary": "AUA guidelines require a post-void residual measurement to diagnose overactive bladder — "
                   "which needs an in-office ultrasound, at odds with the telemedicine pathway the same "
                   "guidelines endorse. One hundred women estimated their own residual before it was measured.",
        "stats": [("100", "women enrolled"), ("22%", "estimated within 30%"),
                  ("95%", "had a normal residual"), ("0", "met retention criteria")],
        "tags": ["Overactive bladder", "Telemedicine", "Guidelines", "Access to care", "Primary care"],
        "page": {"kind": "auto"},
        "paper": {"pdf": "Maimo_Work/1_PVR_Self-Estimation/old_PVR/Henry Edits V7 PVR Manuscript Family Practice.pdf",
                  "label": "Manuscript V7", "note": "Submitted to Family Practice (OUP)."},
        "hub": {
            "people": ["Colby Rondeau, MD", "Henry M. Blair", "Sumyia Razzak",
                                    "Sarah Chaudhary", "Trashana Smith", "Michael Silver",
                                    "Allison Polland, MD"],
            "lede": "A guideline can contradict itself. AUA and SUFU guidance endorses telemedicine for the "
                    "initial evaluation of overactive bladder, and separately requires a post-void residual "
                    "measurement to exclude retention — which requires the in-office bladder ultrasound that "
                    "telemedicine was meant to avoid, and that most primary-care offices do not own. The "
                    "practical question for a family physician is not whether PVR <i>can</i> be measured, but "
                    "whether it <i>must</i> be, before treatment can safely begin.",
            "status_detail": "Submitted to <i>Family Practice</i> (Oxford University Press). Approved by the "
                             "Maimonides Medical Center IRB. I am corresponding author.",
            "sections": [
                {
                    "id": "design", "title": "How the study was built", "nav": "How it was built",
                    "intro": "Single-centre cross-sectional study at a urogynecology practice in Brooklyn — "
                             "a dense urban setting — designed so that a negative result would still answer "
                             "the clinical question.",
                    "blocks": [
                        {"h3": "Who was included"},
                        {"prose": "English-speaking women aged 18–85 presenting with bladder complaints — "
                                  "urgency, frequency, sensation of incomplete emptying, hesitancy or "
                                  "incontinence. Women over 85 were excluded to preserve deidentification "
                                  "given how few there were."},
                        {"h3": "Who was excluded, and why it matters"},
                        {"prose": "Anyone with a documented history of catheterization or incomplete "
                                  "emptying. That exclusion is the study's most consequential design "
                                  "decision and its main limitation: it removes precisely the women most "
                                  "likely to have an elevated residual, which is why the retention rate here "
                                  "is not a population baseline."},
                        {"h3": "How the estimate was elicited"},
                        {"prose": "Participants were told that normal bladder capacity is 300–500 mL and a "
                                  "normal residual under 50–100 mL, then shown pre-filled reference balloons "
                                  "at 5, 10, 100 and 200 mL — anchoring the estimate to something physical "
                                  "rather than a number in the abstract. Immediately after voiding they gave "
                                  "an estimate, and ultrasound measurement followed."},
                        {"h3": "What counted as accurate"},
                        {"prose": "Pre-specified as within 30% of the measured value — equivalently, an "
                                  "estimated-to-measured ratio between 0.7 and 1.3 — following Drangsholt et "
                                  "al., in which women estimated <i>voided</i> volumes to that margin. "
                                  "Analysis was by Mann-Whitney U for predictors of accuracy and linear "
                                  "regression of estimated against measured volume."},
                        {"table": {
                            "head": ["Category", "Post-void residual (mL)"],
                            "rows": [["Normal", "&lt; 100"], ["Acceptably elevated", "100 – &lt;200"],
                                     ["Incomplete emptying", "200 – &lt;300"], ["Retention", "≥ 300"]],
                            "note": "<b>Table 1.</b> Retention-risk categories, modified from Ballstaedt et al. "
                                    "The original ≥300 mL and ≥400 mL tiers were combined to align with the AUA "
                                    "threshold for chronic urinary retention."}},
                    ],
                },
                {
                    "id": "cohort", "title": "Who took part", "nav": "Who took part", "tag": "Table 2",
                    "blocks": [
                        {"prose": "One hundred women, median age 68 (IQR 55–76), median inter-void interval "
                                  "2 hours. Measured residuals ranged from 1 to 241 mL."},
                        {"table": {
                            "head": ["Characteristic", "Value"],
                            "rows": [["Age, years — median (IQR)", "68 (55.3–76.0)"],
                                     ["Inter-void interval, hours — median (IQR)", "2 (1–3)"],
                                     ["Caffeinated drinks, cups — median (IQR)", "1.0 (0.6–2.0)"],
                                     ["Non-caffeinated drinks, cups — median (IQR)", "5.0 (3.1–7.0)"],
                                     ["Presenting: urinary frequency", "82%"],
                                     ["Presenting: urinary incontinence", "66%"],
                                     ["Presenting: sensation of incomplete emptying", "33%"],
                                     ["Presenting: hesitancy", "21%"],
                                     ["Urgency without incontinence", "62%"],
                                     ["Nocturia", "60%"],
                                     ["Urgency incontinence", "51%"],
                                     ["Stress incontinence", "47%"],
                                     ["Anxiety", "20%"], ["Type 2 diabetes", "18%"],
                                     ["Depression", "16%"], ["Diuretic use", "5%"],
                                     ["Prior pelvic radiation", "2%"]],
                            "note": "<b>Table 2.</b> Symptoms and comorbidities were yes/no survey items; "
                                    "continuous variables are medians with interquartile range."}},
                    ],
                },
                {
                    "id": "results", "title": "What the measurements showed", "nav": "What it shows",
                    "tag": "Table 3 · Figures 1–3",
                    "blocks": [
                        {"stats": [("95%", "normal residual (<100 mL)", "4% acceptably elevated"),
                                   ("1%", "incomplete emptying", "a single participant"),
                                   ("0%", "met retention criteria", "none reached 300 mL"),
                                   ("29.5 mL", "mean measured residual", "vs 43.0 mL estimated")]},
                        {"h3": "The estimates were not accurate"},
                        {"prose": "Twenty-two per cent of women estimated within 30% of their measured "
                                  "value. Estimated and measured volumes were significantly but weakly "
                                  "correlated (slope 0.21, 95% CI 0.06–0.36; p = 0.006), with R² = 0.076 — "
                                  "the self-estimate explains about 8% of the variance, which is a real "
                                  "association and a useless one for any individual patient."},
                        {"figure": {"src": "fig1.jpg",
                                    "caption": "<b>Figure 1.</b> Measured versus estimated post-void residual, "
                                               "stratified by retention category."}},
                        {"h3": "Category accuracy is a mirage"},
                        {"prose": "Eighty-five per cent of women named the correct residual category — but "
                                  "almost entirely because nearly everyone was normal and nearly everyone "
                                  "guessed normal. Among the 15 who estimated an elevation, only 3 had any "
                                  "elevation at all. Self-identification of an abnormal residual has poor "
                                  "positive predictive value."},
                        {"table": {
                            "head": ["Estimated category", "Normal", "Acceptably elevated",
                                     "Incomplete emptying", "Retention", "Total", "Correctly classified"],
                            "rows": [["Normal", "83", "1", "1", "0", "85", "97.6%"],
                                     ["Acceptably elevated", "10", "2", "0", "0", "12", "16.7%"],
                                     ["Incomplete emptying", "2", "1", "0", "0", "3", "0%"],
                                     ["Retention", "0", "0", "0", "0", "0", "—"],
                                     {"cls": "up", "cells": ["Measured total", "95", "4", "1", "0", "100", "85.0%"]}],
                            "note": "<b>Table 3, Panel B.</b> Rows are what participants estimated; columns are "
                                    "what was measured. Correctly classified is the diagonal divided by the "
                                    "row total — the proportion of women choosing a category who were right."}},
                        {"figure": {"src": "fig2.jpg",
                                    "caption": "<b>Figure 2.</b> Distribution of estimated and measured "
                                               "post-void residual volumes."}},
                        {"h3": "Nothing predicted who would estimate well"},
                        {"prose": "Mann-Whitney U tests across every urinary symptom and comorbidity — "
                                  "frequency, incomplete emptying, hesitancy, incontinence, urgency, "
                                  "nocturia, anxiety, depression, diabetes, diuretic use, prior pelvic "
                                  "radiation — found no significant association with estimation accuracy "
                                  "(all p &gt; 0.12). There is no subgroup in whom self-estimation can be "
                                  "trusted more."},
                        {"figure": {"src": "fig3.jpg",
                                    "caption": "<b>Figure 3.</b> Estimation accuracy across urinary symptoms "
                                               "and comorbidities."}},
                    ],
                },
                {
                    "id": "argument", "title": "The argument the paper actually makes", "nav": "The argument",
                    "blocks": [
                        {"callout": "<b>The headline hypothesis failed, and the clinically useful finding "
                                    "came from the denominator.</b> Women cannot estimate their own residual "
                                    "— so self-estimation is not a substitute for measurement. But almost "
                                    "none of them needed the measurement: 95% normal, one woman with "
                                    "incomplete emptying, nobody in retention."},
                        {"prose": "That reframes the requirement. If the point of measuring PVR before "
                                  "treating overactive bladder is to catch retention, and retention is "
                                  "essentially absent in women presenting with OAB symptoms and no history "
                                  "of incomplete emptying, then the requirement is buying very little at the "
                                  "cost of an in-office visit — a visit that, for some women, is the reason "
                                  "care does not happen at all."},
                        {"prose": "The paper therefore argues for deferral rather than substitution: in "
                                  "low-risk women, treatment can reasonably begin in primary care or by "
                                  "telemedicine, with measurement reserved for those whose history warrants "
                                  "it. Reassurance comes from the low baseline risk, not from the patient's "
                                  "guess."},
                    ],
                },
                {
                    "id": "limitations", "title": "Limitations", "nav": "Limitations",
                    "blocks": [
                        {"bullets": [
                            "<b>The excluded women are the ones at risk.</b> Excluding prior catheterization "
                            "or documented incomplete emptying enriched the cohort toward low residuals by "
                            "design. The 1% and 0% figures describe women presenting with OAB symptoms "
                            "without that history — not population baselines.",
                            "<b>Ultrasound, not catheterization.</b> Straight catheterization is the "
                            "reference standard; bladder ultrasound was used as non-invasive and previously "
                            "shown not to differ significantly.",
                            "<b>One measurement, one moment.</b> Residual volume varies between voids and "
                            "over time; a cross-sectional design cannot capture that.",
                            "<b>Anchoring may have inflated estimates.</b> Reference balloons and stated "
                            "normal ranges were given to make estimates meaningful, and may have pushed "
                            "symptomatic women toward guessing high.",
                            "<b>Concurrent OAB medication was not recorded</b>, and it changes emptying "
                            "independently of underlying function.",
                            "<b>Women only.</b> A prostate creates an obstruction risk with no analogue "
                            "here, so none of this transfers to men.",
                        ]},
                    ],
                },
            ],
            "next": "A longitudinal design correlating symptoms with both measured and estimated residual "
                    "over time, and a low-risk rule tested prospectively against in-office evaluation — the "
                    "study that would turn a deferral argument into a pathway.",
            "sidefoot": "Colby Rondeau, MD · Henry M. Blair · Allison Polland, MD<br>Department of Urogynecology, Maimonides Medical Center<br>Brooklyn, NY · 2024–2025",
        },
    },

    {
        "slug": "oab-adi", "tab": "Deprivation & Access", "group": "current",
        "title": "Does neighborhood deprivation predict urogynecologic access in Brooklyn?",
        "kicker": "Cross-sectional study · Maimonides Medical Center · Nov 2024 – Aug 2025",
        "status": "Manuscript V3",
        "summary": "The Area Deprivation Index stands in for a patient's material circumstances across "
                   "American health services research. It was built where distance means a car. Brooklyn is "
                   "not that place — so does it measure what it claims to measure here?",
        "stats": [("120", "women enrolled"), ("30 vs 30 min", "travel time, disadvantaged vs advantaged"),
                  ("$5.00 vs $2.95", "travel cost"), ("91.5% vs 77.2%", "urge frequency (p = 0.033)")],
        "tags": ["Overactive bladder", "Health equity", "Area Deprivation Index", "Urban health", "Telehealth"],
        "page": {"kind": "auto"},
        "paper": {"pdf": "_source/manuscripts/ADI-and-Travel-Time-V3.pdf",
                  "label": "Manuscript V3", "note": "With Colby Rondeau, MD and Allison Polland, MD."},
        "hub": {
            "people": ["Colby Rondeau, MD", "Luke Jenusaitis, MD", "Elizabeth DeSellier",
                                    "Rebecca Bergmann", "Peace Deh", "Michael Silver",
                                    "Henry M. Blair", "Allison Polland, MD"],
            "lede": "Deprivation indices are used as a proxy for the barriers a patient faces, and the "
                    "barrier they most directly encode is travel: in most of the country, a poorer "
                    "neighborhood means a longer, costlier trip to specialty care. New York has a subway. "
                    "This study asks whether the index still tracks access where the transit system does "
                    "not care how wealthy your block is.",
            "status_detail": "Manuscript V3. Single-centre cross-sectional study, IRB approved, enrolling "
                             "November 2024 – August 2025. I am co-corresponding author.",
            "sections": [
                {
                    "id": "design", "title": "How the study was built", "nav": "How it was built",
                    "intro": "A survey study designed so that the null result would still say something — "
                             "by measuring travel burden directly rather than inferring it from the index.",
                    "blocks": [
                        {"h3": "Who was included"},
                        {"prose": "English-speaking women aged 18–85 presenting for evaluation of overactive "
                                  "bladder — urgency, frequency, perceived incomplete emptying, hesitancy or "
                                  "incontinence. Women with known incomplete emptying, prior catheterization "
                                  "or a current catheter were excluded, as were women over 85, to preserve "
                                  "deidentification. Of 144 approached, 120 met criteria."},
                        {"h3": "How deprivation was measured"},
                        {"prose": "Participants located their home on the Neighborhood Atlas — the "
                                  "University of Wisconsin's Area Deprivation Index map — and the ADI value "
                                  "for that block group was recorded, from 1 (least deprived) to 10 (most). "
                                  "Because the distribution in this population was so compressed, scores "
                                  "were dichotomized at advantaged (ADI ≤ 2) versus disadvantaged (ADI ≥ 3), "
                                  "following Gill et al. in a population with similarly limited variation."},
                        {"h3": "What was measured instead of assumed"},
                        {"prose": "Travel time, travel cost, mode of transport (public versus private) and "
                                  "whether the patient was accompanied — asked directly, rather than modelled "
                                  "from address. Symptom severity was captured by presenting complaint and by "
                                  "self-reported inter-void interval as a proxy."},
                        {"h3": "Powering and analysis"},
                        {"prose": "Sixty participants per group gives 80% power at α = 0.05 for an effect "
                                  "size of 0.65 on a two-sided Wilcoxon-Mann-Whitney test — that is, a 65% "
                                  "probability that a random observation from one group exceeds one from the "
                                  "other. Continuous variables were compared with Wilcoxon rank-sum and "
                                  "reported as medians with IQR; categorical variables with chi-square, or "
                                  "Fisher's exact where expected counts fell below five. Comparisons beyond "
                                  "the pre-specified travel-time and travel-cost outcomes were exploratory "
                                  "and not adjusted for multiple testing."},
                        {"callout": "<b>Why the powering matters for reading this study.</b> The design was "
                                    "sized to detect a moderate difference. It did not find one — which is a "
                                    "more informative null than an underpowered study failing to reject."},
                    ],
                },
                {
                    "id": "travel", "title": "Travel burden did not differ", "nav": "Travel burden",
                    "tag": "Table 2 · Figure 1",
                    "blocks": [
                        {"stats": [("30 vs 30 min", "median travel time", "IQR 23.5–45 vs 15–40; p = 0.085"),
                                   ("$5.00 vs $2.95", "median travel cost", "IQR 0.88–11.50 vs 0–7.00; p = 0.062"),
                                   ("31.7% vs 20%", "public transport use", "p = 0.144"),
                                   ("23.3% vs 31.7%", "accompanied to the visit", "p = 0.307")]},
                        {"prose": "Neither primary outcome differed significantly. Both showed a trend in the "
                                  "expected direction — disadvantaged women travelling somewhat longer and "
                                  "paying somewhat more — and both distributions overlapped substantially, "
                                  "with only modest upward shifts."},
                        {"figure": {"src": "fig1.jpg",
                                    "caption": "<b>Figure 1.</b> Distributions of travel time and travel cost "
                                               "by ADI group. The overlap is the finding."}},
                        {"callout": "<b>A trend worth naming honestly.</b> p = 0.062 on cost is not "
                                    "significance, and the paper does not claim it. But a recurring $2 "
                                    "difference each way, across a treatment course requiring repeated "
                                    "visits, can matter to a patient even when it does not reach α = 0.05."},
                        {"figure": {"src": "fig2.jpg",
                                    "caption": "<b>Figure 2.</b> Transport mode and visit accompaniment by "
                                               "ADI group."}},
                    ],
                },
                {
                    "id": "symptoms", "title": "One difference did appear", "nav": "Symptoms",
                    "tag": "Table 1",
                    "blocks": [
                        {"prose": "Disadvantaged women endorsed <b>urinary urge frequency</b> as a presenting "
                                  "complaint far more often — 91.5% versus 77.2% (p = 0.033). No other "
                                  "presenting complaint or comorbidity differed."},
                        {"table": {
                            "head": ["Measure", "Disadvantaged", "Advantaged", "p"],
                            "rows": [{"cls": "up", "cells": ["Urinary urge frequency", "91.5%", "77.2%", "0.033"]},
                                     ["Urinary frequency (without urge)", "76.7%", "75.0%", "0.831"],
                                     ["Inter-void interval, hours (median)", "2 (1–3)", "2 (1–3)", "0.753"],
                                     ["Median age, years", "61.5", "68.5", "0.331"],
                                     ["Travel time, minutes (median)", "30", "30", "0.085"],
                                     ["Travel cost, dollars (median)", "5.00", "2.95", "0.062"],
                                     ["Public transportation", "31.7%", "20.0%", "0.144"],
                                     ["Accompanied to visit", "23.3%", "31.7%", "0.307"]],
                            "note": "<b>Table 1–2, selected rows.</b> Wilcoxon rank-sum for continuous "
                                    "variables, chi-square or Fisher's exact for categorical."}},
                        {"prose": "The distinction between the two frequency items is the interesting part: "
                                  "plain frequency was identical between groups, while <i>urge</i> frequency "
                                  "— the more bothersome symptom — was not. That points at a difference in "
                                  "burden or in delay before presenting, rather than a difference in how far "
                                  "anyone had to travel."},
                        {"h3": "Everything else was null"},
                        {"prose": "Exploratory comparisons across the remaining survey items — leaking with "
                                  "urgency, leaking with Valsalva, urgency-related rushing, nocturia, "
                                  "prolapse symptoms, estimated and measured post-void residual, caffeine and "
                                  "non-caffeine intake, and telehealth experience and willingness — showed no "
                                  "significant differences by ADI group."},
                    ],
                },
                {
                    "id": "reading", "title": "How to read a null result", "nav": "Reading the null",
                    "blocks": [
                        {"callout": "<b>Two explanations fit the data, and they have opposite implications.</b> "
                                    "Either transit genuinely equalizes travel burden in New York, or the "
                                    "index failed to identify who is disadvantaged here."},
                        {"h3": "The transit explanation"},
                        {"prose": "A subway system that costs the same from every neighborhood removes the "
                                  "mechanism through which deprivation usually produces travel burden. If "
                                  "that is what happened, the finding is encouraging: dense transit narrows "
                                  "one specialty-care disparity, and attention should move to the barriers "
                                  "it does not touch."},
                        {"h3": "The instrument explanation"},
                        {"prose": "ADI weights home value heavily. In a city where a modest apartment costs "
                                  "what a comfortable house costs elsewhere, that weighting compresses and "
                                  "left-skews the deprivation distribution — which is exactly why scores had "
                                  "to be dichotomized at 2 rather than at the conventional midpoint. On this "
                                  "reading the null says the index is mis-calibrated for dense urban housing "
                                  "markets, and studies using it here may be measuring housing cost rather "
                                  "than deprivation."},
                        {"prose": "The urge-frequency difference slightly favours the second reading: the "
                                  "groups <i>did</i> differ in something clinically real, so the "
                                  "dichotomization was not pure noise — it simply did not track travel."},
                        {"h3": "Either way, telehealth looks acceptable"},
                        {"prose": "Willingness to use video visits was high in both groups (71.4% and 67.3%), "
                                  "which makes remote care a plausible way to reduce travel burden regardless "
                                  "of which explanation holds."},
                    ],
                },
                {
                    "id": "limitations", "title": "Limitations", "nav": "Limitations",
                    "blocks": [
                        {"bullets": [
                            "<b>Single centre, one city.</b> Findings describe a Brooklyn urogynecology "
                            "clinic; the transit explanation is by construction not generalizable to "
                            "car-dependent settings.",
                            "<b>Compressed ADI distribution.</b> Dichotomizing at ADI 2 was forced by the "
                            "population's homogeneity and departs from conventional cut-points, which limits "
                            "comparison with other ADI literature.",
                            "<b>Self-reported travel.</b> Time and cost came from patients rather than from "
                            "routing data, and are subject to recall.",
                            "<b>Exploratory comparisons were not corrected</b> for multiple testing, so the "
                            "urge-frequency difference should be treated as hypothesis-generating.",
                            "<b>Everyone surveyed had already arrived.</b> The women who could not make the "
                            "trip at all are, by construction, absent from a clinic-based sample — the "
                            "hardest limitation for any access study to escape.",
                        ]},
                    ],
                },
            ],
            "next": "A larger multisite study across cities with different transit density would separate "
                    "the two explanations directly: if the null persists where transit is strong and "
                    "disappears where it is not, the mechanism is transit rather than the instrument.",
            "sidefoot": "Colby Rondeau, MD · Henry M. Blair · Allison Polland, MD<br>Maimonides Medical Center · SUNY Downstate<br>Brooklyn, NY · 2024–2025",
        },
    },

    {
        "slug": "nocturia-goals", "tab": "Nocturia Goals", "group": "current",
        "title": "What do patients with nocturia actually want treated?",
        "kicker": "Patient-reported outcomes · Maimonides Medical Center",
        "status": "Manuscript V3",
        "summary": "Nocturia trials fixate on nightly void count. This project examines patient-defined "
                   "treatment goals and how much nighttime urination patients are willing to tolerate — "
                   "outcomes beyond the number.",
        "tags": ["Nocturia", "Patient-reported outcomes", "Trial design"],
        "paper": {"pdf": "Maimo_Work/7_Nocturia/Henry - V3 - What Do Patients with Nocturia Want Treated_ Patient-Defined Goals and Tolerance Beyond Void Count.pdf",
                  "label": "Manuscript V3", "note": "With Oliver Menken."},
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Oliver Menken", "Henry M. Blair"],
            "lede": "Nocturia trials are built on a countable outcome: voids per night. It is easy to "
                    "measure and easy to compare, and it may not be the thing patients are trying to "
                    "change. A treatment that removes one void from three may or may not be a treatment "
                    "that changes a life.",
            "question": "What outcomes do patients with nocturia actually want from treatment, and how much "
                        "nighttime urination will they tolerate before it matters to them?",
            "approach": [
                "Patients define their own treatment goals rather than choosing from a fixed instrument.",
                "Tolerability thresholds are elicited directly — how many voids a night is acceptable — "
                "instead of inferred from symptom scores.",
                "Patient-defined goals are compared against the void-count endpoints trials use, to see "
                "how far apart the two actually sit.",
            ],
            "status_detail": "Manuscript V3.",
            "next": "If patient-defined goals diverge from void count, the argument follows for a "
                    "goal-attainment endpoint in nocturia trials.",
            "sidefoot": "Oliver Menken · Henry M. Blair<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "retzius-retention", "tab": None, "group": "current",
        "title": "Urinary retention after Retzius-sparing prostatectomy",
        "kicker": "Retrospective cohort · Maimonides Medical Center",
        "status": "Manuscript V1 · IRB protocol in place for a prospective follow-on",
        "summary": "Retzius-sparing robotic prostatectomy gives men better early continence, but preserving "
                   "the anterior compartment may cost postoperative retention — and no study has examined "
                   "retention as a primary outcome or identified who is at risk.",
        "tags": ["Prostate cancer", "RARP", "Urinary retention", "Surgical outcomes"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Edward Wu, MD", "Henry M. Blair", "Ervin Teper, MD",
                                    "David Silver, MD"],
            "lede": "Retzius-sparing robotic prostatectomy is chosen for a reason: men regain continence "
                    "sooner. The anatomy that buys that advantage — an untouched anterior compartment — is "
                    "also the anatomy that could obstruct. Retention after the operation has been reported "
                    "in passing, never as the outcome of interest, and nobody has said which men are at risk.",
            "question": "What is the incidence of urinary retention after Retzius-sparing RARP, and which "
                        "preoperative measurements predict it?",
            "approach": [
                "A retrospective cohort of roughly 200 consecutive patients who underwent Retzius-sparing "
                "RARP, with retention as the primary outcome rather than an incidental complication.",
                "Anatomic predictors: membranous urethral length, intravesical prostatic protrusion and "
                "prostate volume.",
                "Clinical predictors: baseline LUTS, PSA, diabetes, prior retention, prior "
                "ureteral or urethral procedures, cardiovascular and cerebrovascular disease, and a "
                "modified frailty index.",
                "Pharmacologic exposure before and after surgery: alpha-blockers, 5-ARIs and ADT.",
            ],
            "status_detail": "Manuscript V1. An IRB protocol and a 48-reference literature review are in "
                             "place for a prospective follow-on study.",
            "next": "The prospective study, in which the candidate predictors are measured before surgery "
                    "rather than reconstructed from charts — the design that can turn an association into "
                    "a preoperative risk estimate a surgeon could act on.",
            "sidefoot": "Edward Wu, MD · Henry M. Blair · Ervin Teper, MD · David Silver, MD<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "focal-therapy-continence", "tab": None, "group": "current",
        "title": "Continence outcomes after focal therapy for prostate cancer",
        "kicker": "Chart review · Maimonides Medical Center",
        "status": "Early stage",
        "summary": "Urinary outcomes — incontinence and leakage — after HIFU and irreversible "
                   "electroporation, the ablative options offered in place of whole-gland treatment.",
        "tags": ["Prostate cancer", "Focal therapy", "HIFU", "Irreversible electroporation", "Continence"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Christopher Edwards, MD", "Henry M. Blair", "David Silver, MD"],
            "lede": "Focal therapy is offered on a continence argument: treat part of the gland, spare the "
                    "function. That argument deserves outcome data from the men who took it.",
            "question": "What are the urinary continence outcomes — incontinence, leakage — after HIFU and "
                        "irreversible electroporation for prostate cancer?",
            "approach": [
                "Chart review of patients treated with HIFU or irreversible electroporation.",
                "Continence and leakage as the primary outcomes, recorded against baseline function.",
            ],
            "status_detail": "Early stage — cohort assembly underway.",
            "sidefoot": "Christopher Edwards, MD · Henry M. Blair · David Silver, MD<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "ketamine-cystitis", "tab": None, "group": "current",
        "title": "Ketamine cystitis in the United States",
        "kicker": "National epidemiology",
        "status": "Early stage",
        "summary": "Characterizing the incidence and demographics of ketamine-associated cystitis over the "
                   "past decade — positioned to be the largest study of its kind to date.",
        "tags": ["Ketamine cystitis", "Epidemiology", "Substance use", "Real-world data"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Marc Ganz, MD", "Henry M. Blair"],
            "lede": "Ketamine use has moved in a decade from club drug to prescribed treatment for "
                    "depression and chronic pain. Its bladder toxicity is well described in case series "
                    "and poorly described at national scale — which is a problem if prescribing keeps "
                    "rising.",
            "question": "How common is ketamine-associated cystitis in the United States, who develops it, "
                        "and how has that changed over the past decade?",
            "approach": [
                "A national real-world cohort, sized to be the largest characterization of this condition "
                "to date.",
                "Incidence over time, with attention to whether any change tracks the growth in "
                "therapeutic ketamine rather than recreational use alone.",
                "Demographics: age, sex and geography.",
            ],
            "status_detail": "Early stage — cohort definition in progress.",
            "sidefoot": "Marc Ganz, MD · Henry M. Blair<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "urogyn-perceptions",
        "tab": "Urogyn Survey",
        "group": "current",
        "title": "How urology residents see urogynecology",
        "kicker": "National survey \u00b7 US urology residency programs \u00b7 July\u2013August 2026",
        "status": "Three manuscripts drafted \u00b7 three abstracts submitted to the 2027 AUA Annual Meeting",
        "summary": "Urogynecology and reconstructive pelvic surgery takes fellows from both urology and gynaecology, but few come from urology. We surveyed 115 residents nationally about what they are exposed to, who mentors them, what they think the field is, and when they decide. Exposure and mentorship did not explain who was interested.",
        "stats": [
            ("115", "residents responded"),
            ("46.1%", "any fellowship interest"),
            ("28.7%", "have a URPS mentor"),
            ("90.4%", "say URPS belongs in urology"),
        ],
        "tags": [
            "Medical education",
            "Workforce",
            "Urogynecology",
            "Survey research",
            "Fellowship training",
        ],
        "page": {
            "kind": "auto",
        },
        "hub": {
            "people": [
                "Gina DeMeo",
                "Henry M. Blair",
                "Nina Robins",
                "Luke Jenusaitis",
                "Jubin Matloubieh",
            ],
            "lede": "Exposure and mentorship are the standard explanation for why residents do or do not choose a subspecialty. We asked 115 urology residents across the country, and neither one explained who was interested. What did was gender, structured teaching, what residents believed the operating was like \u2014 and, above all, whether they had already made up their minds.",
            "status_detail": "Three manuscripts drafted from one survey; three abstracts submitted to the 2027 AUA Annual Meeting. Approved by the Maimonides Medical Center IRB (2026-02-08-MMC) and funded by the Maimonides Research and Development Foundation.",
            "question": "Urogynecology and reconstructive pelvic surgery takes fellows from both urology and gynaecology, but few come from urology. Is that because residents never see the field, because they think it belongs to someone else, or because of something else entirely?",
            "approach": [
                "A 24-item REDCap survey emailed to program directors and coordinators at every ACGME-accredited US urology residency, July to August 2026, for forwarding to residents. Voluntary and anonymous; 116 returned, one blank, leaving 115.",
                "It asked about training year, age and gender; program type; whether the program had fellowship-trained URPS faculty and an institutional fellowship; seven separate kinds of clinical exposure; the year of first meaningful exposure; mentorship and its influence.",
                "Six perception statements on five-point Likert scales, eight predefined barriers, a free-text question on what would raise interest, and when the fellowship decision was made.",
                "Proportions with Wilson score intervals; two-proportion z-tests with Woolf odds ratios; Mann\u2013Whitney for timing; Cochran\u2013Armitage for the trend across training years; Benjamini\u2013Hochberg correction across the seven exposure types; then multivariable logistic regression, ordinal and dichotomised.",
            ],
            "sections": [
                {
                    "id": "who",
                    "title": "Who answered",
                    "nav": "Who answered",
                    "intro": "115 residents, every training year represented, mostly from academic programs.",
                    "blocks": [
                        {
                            "stats": [
                                ("115", "residents", "of 116 returned"),
                                ("30.1", "mean age", "SD 2.8, range 26\u201342"),
                                ("86.1%", "academic programs", "99 of 115"),
                            ],
                        },
                        {
                            "table": {
                                "head": [
                                    "Characteristic",
                                    "n",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "Women",
                                        "48",
                                        "41.7%",
                                    ],
                                    [
                                        "Men",
                                        "63",
                                        "54.8%",
                                    ],
                                    [
                                        "Non-binary",
                                        "3",
                                        "2.6%",
                                    ],
                                    [
                                        "Preferred not to say",
                                        "1",
                                        "0.9%",
                                    ],
                                    [
                                        "PGY-1",
                                        "25",
                                        "21.7%",
                                    ],
                                    [
                                        "PGY-2",
                                        "19",
                                        "16.5%",
                                    ],
                                    [
                                        "PGY-3",
                                        "27",
                                        "23.5%",
                                    ],
                                    [
                                        "PGY-4",
                                        "17",
                                        "14.8%",
                                    ],
                                    [
                                        "PGY-5",
                                        "22",
                                        "19.1%",
                                    ],
                                    [
                                        "PGY-6",
                                        "5",
                                        "4.3%",
                                    ],
                                ],
                            },
                        },
                    ],
                },
                {
                    "id": "environment",
                    "title": "What residents are actually trained in",
                    "nav": "The environment",
                    "intro": "Three quarters train alongside a fellowship-trained URPS urologist, and three quarters have meaningful exposure by PGY-3. On the face of it, the pipeline is not starved of exposure.",
                    "blocks": [
                        {
                            "table": {
                                "head": [
                                    "URPS educational environment",
                                    "n",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "Fellowship-trained URPS faculty in the department",
                                        "89",
                                        "77.4%",
                                    ],
                                    [
                                        "&nbsp;&nbsp;&nbsp;No such faculty",
                                        "23",
                                        "20.0%",
                                    ],
                                    [
                                        "&nbsp;&nbsp;&nbsp;Unsure",
                                        "3",
                                        "2.6%",
                                    ],
                                    [
                                        "Institutional URPS fellowship",
                                        "43",
                                        "37.4%",
                                    ],
                                    [
                                        "Formal URPS didactics or curriculum",
                                        "77",
                                        "67.0%",
                                    ],
                                    [
                                        "First meaningful exposure \u2014 PGY-1",
                                        "26",
                                        "22.6%",
                                    ],
                                    [
                                        "&nbsp;&nbsp;&nbsp;PGY-2",
                                        "30",
                                        "26.1%",
                                    ],
                                    [
                                        "&nbsp;&nbsp;&nbsp;PGY-3",
                                        "28",
                                        "24.3%",
                                    ],
                                    [
                                        "&nbsp;&nbsp;&nbsp;PGY-4",
                                        "11",
                                        "9.6%",
                                    ],
                                    [
                                        "&nbsp;&nbsp;&nbsp;Never",
                                        "20",
                                        "17.4%",
                                    ],
                                ],
                            },
                        },
                        {
                            "callout": "<b>Faculty buy curriculum, not just contact.</b> Programs with a URPS-trained urologist were far likelier to run formal didactics \u2014 73.0% (65/89) versus 43.5% (10/23), p&nbsp;=&nbsp;0.007. That matters, because didactics is the only kind of exposure that tracked with interest.",
                        },
                    ],
                },
                {
                    "id": "mentorship",
                    "title": "The mentorship gap is not a supply problem",
                    "nav": "Mentorship",
                    "blocks": [
                        {
                            "table": {
                                "head": [
                                    "Mentorship",
                                    "n / N",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "Has a URPS mentor",
                                        "33 / 115",
                                        "28.7%",
                                    ],
                                    [
                                        "Mentor moderately or significantly influential",
                                        "21 / 32",
                                        "65.6%",
                                    ],
                                    [
                                        "Of those without one, said the program could easily provide one",
                                        "60 / 81",
                                        "74.1%",
                                    ],
                                ],
                            },
                        },
                        {
                            "prose": "Fewer than a third had a mentor, and three quarters of those who did not believed one was available for the asking. Mentorship was also independent of exposure: it predicted neither whether meaningful exposure happened (12.1% vs 19.5% reporting none; OR 1.76, 95% CI 0.54\u20135.72; p&nbsp;=&nbsp;0.34) nor when it happened (81.8% vs 69.5% by PGY-3; p&nbsp;=&nbsp;0.18; median PGY-2 in both groups).",
                        },
                        {
                            "callout": "The cheapest finding in the study: programs could pair residents with URPS faculty rather than waiting to be asked.",
                        },
                    ],
                },
                {
                    "id": "perceptions",
                    "title": "What residents think the field is",
                    "nav": "Perceptions",
                    "intro": "Agreement or strong agreement with each statement, among 115 residents.",
                    "blocks": [
                        {
                            "table": {
                                "head": [
                                    "Statement",
                                    "Agree",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "URPS has a clearly defined role within urology",
                                        "104",
                                        "90.4%",
                                    ],
                                    [
                                        "The surgical complexity of URPS is appealing",
                                        "75",
                                        "65.2%",
                                    ],
                                    [
                                        "Work\u2013life balance appears favourable",
                                        "73",
                                        "63.5%",
                                    ],
                                    [
                                        "My program encourages involvement in female pelvic medicine",
                                        "68",
                                        "59.1%",
                                    ],
                                    [
                                        "A career in URPS would be satisfying for me",
                                        "44",
                                        "38.3%",
                                    ],
                                    [
                                        "URPS should primarily be an OBGYN subspecialty",
                                        "3",
                                        "2.6%",
                                    ],
                                ],
                            },
                        },
                        {
                            "prose": "The identity question the field argues about internally is, for residents, settled: 90.4% say URPS belongs in urology and the same proportion reject the idea that it is really a gynaecology subspecialty. The soft spot is further down the list \u2014 only 38.3% expect the career itself to satisfy them, and a third actively disagree.",
                        },
                    ],
                },
                {
                    "id": "interest",
                    "title": "Who is interested, and who is not",
                    "nav": "Interest",
                    "blocks": [
                        {
                            "stats": [
                                ("46.1%", "any interest", "53 of 115; 95% CI 37.3\u201355.2%"),
                                ("60.0% \u2192 27.3%", "PGY-1 to PGY-5", "p = 0.007 for trend"),
                                ("31.7% vs 64.6%", "men vs women", "OR 0.26; p < 0.001"),
                            ],
                        },
                        {
                            "h3": "Interest falls across training",
                        },
                        {
                            "prose": "Interest ran from 60.0% in PGY-1 to 27.3% in PGY-5, with none of the five PGY-6 residents interested (Cochran\u2013Armitage z&nbsp;=&nbsp;\u22122.72, p&nbsp;=&nbsp;0.007). Residents in PGY-4 or later reported interest less often than PGY-1 to 3 (31.8% vs 54.9%; OR 0.38; p&nbsp;=&nbsp;0.016). Cross-sectionally this could be attrition or a cohort difference \u2014 either way the window is early.",
                        },
                        {
                            "h3": "Exposure and mentorship did not sort people",
                        },
                        {
                            "table": {
                                "head": [
                                    "Bivariate association with any interest",
                                    "With",
                                    "Without",
                                    "OR (95% CI)",
                                    "p",
                                ],
                                "rows": [
                                    [
                                        "Moderate or extensive clinical exposure",
                                        "46.6%",
                                        "44.4%",
                                        "1.09 (0.46\u20132.59)",
                                        "0.85",
                                    ],
                                    [
                                        "Didactics or formal curriculum",
                                        "53.2%",
                                        "31.6%",
                                        "2.47 (1.09\u20135.59)",
                                        "0.028*",
                                    ],
                                    [
                                        "Has a URPS mentor",
                                        "48.5%",
                                        "45.1%",
                                        "\u2014",
                                        "0.74",
                                    ],
                                    [
                                        "Male gender",
                                        "31.7%",
                                        "64.6%",
                                        "0.26 (0.12\u20130.56)",
                                        "&lt;0.001",
                                    ],
                                ],
                            },
                        },
                        {
                            "tblnote": "*Did not survive Benjamini\u2013Hochberg correction across the seven exposure types (p = 0.100). Of those seven, didactics was the only one that differed at all.",
                        },
                        {
                            "h3": "The gender gap is not an exposure gap",
                        },
                        {
                            "prose": "Men and women reported similar didactic exposure (69.8% vs 62.5%; p&nbsp;=&nbsp;0.42), similar clinical exposure (73.0% vs 79.2%; p&nbsp;=&nbsp;0.45) and similar mentorship (25.4% vs 35.4%; p&nbsp;=&nbsp;0.25). But didactics worked differently for each: among women, interest was 80.0% with didactics versus 38.9% without (OR 6.29, 1.71\u201323.14; p&nbsp;=&nbsp;0.004); among men, 34.1% versus 26.3% (OR 1.45; p&nbsp;=&nbsp;0.54). The gap was widest precisely where teaching was present.",
                        },
                        {
                            "h3": "Adjusted",
                        },
                        {
                            "table": {
                                "head": [
                                    "Multivariable model",
                                    "OR",
                                    "p",
                                ],
                                "rows": [
                                    [
                                        "Clinical exposure, per level (ordinal interest)",
                                        "1.96",
                                        "0.018",
                                    ],
                                    [
                                        "Male gender (ordinal)",
                                        "0.21",
                                        "&lt;0.001",
                                    ],
                                    [
                                        "Training year, per year (ordinal)",
                                        "0.62",
                                        "0.003",
                                    ],
                                    [
                                        "Strongly agrees surgery is complex and appealing (ordinal)",
                                        "19.93",
                                        "&lt;0.001",
                                    ],
                                    [
                                        "Formal didactic exposure (any interest)",
                                        "6.07",
                                        "0.020",
                                    ],
                                    [
                                        "Male gender (any interest)",
                                        "0.16",
                                        "0.018",
                                    ],
                                    [
                                        "Surgical complexity appeal (any interest)",
                                        "21.65",
                                        "0.043",
                                    ],
                                ],
                            },
                        },
                        {
                            "tblnote": "No mentorship measure was associated with interest in either model.",
                        },
                    ],
                },
                {
                    "id": "timing",
                    "title": "The decision window is the finding",
                    "nav": "Decision timing",
                    "blocks": [
                        {
                            "table": {
                                "head": [
                                    "When the fellowship decision was made",
                                    "n",
                                    "%",
                                    "Any interest",
                                ],
                                "rows": [
                                    [
                                        "Early \u2014 PGY-1 to 2",
                                        "46",
                                        "40.0%",
                                        "10.9%",
                                    ],
                                    [
                                        "Mid-residency \u2014 PGY-3 to 4",
                                        "32",
                                        "27.8%",
                                        "53.1%",
                                    ],
                                    [
                                        "Late \u2014 PGY-5 or later",
                                        "0",
                                        "0%",
                                        "\u2014",
                                    ],
                                    [
                                        "Not yet decided",
                                        "37",
                                        "32.2%",
                                        "83.8%",
                                    ],
                                ],
                            },
                        },
                        {
                            "prose": "Adjusted, mid-residency deciders (OR 23.26) and the undecided (OR 57.45) were far likelier than early deciders to report interest, both p&nbsp;&lt;&nbsp;0.001. Residents who named career uncertainty as a barrier were <i>more</i> interested, not less \u2014 79.3% versus 34.9%, adjusted OR 5.92, p&nbsp;=&nbsp;0.035.",
                        },
                        {
                            "callout": "Read carefully, those odds ratios are partly tautological: residents who have decided have mostly decided against. The honest version is descriptive \u2014 a third of residents are still undecided, and more than four in five of them are at least slightly interested. That is the group worth reaching.",
                        },
                    ],
                },
                {
                    "id": "barriers",
                    "title": "Why not, in residents\u2019 own words",
                    "nav": "Barriers",
                    "blocks": [
                        {
                            "table": {
                                "head": [
                                    "Barrier selected",
                                    "n",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "Preference for another subspecialty",
                                        "75",
                                        "65.2%",
                                    ],
                                    [
                                        "Narrowed scope of practice",
                                        "38",
                                        "33.0%",
                                    ],
                                    [
                                        "Limited exposure",
                                        "34",
                                        "29.6%",
                                    ],
                                    [
                                        "Uncertainty about career plans",
                                        "29",
                                        "25.2%",
                                    ],
                                    [
                                        "Scope overlaps with gynaecology",
                                        "29",
                                        "25.2%",
                                    ],
                                    [
                                        "Lack of mentorship",
                                        "16",
                                        "13.9%",
                                    ],
                                    [
                                        "Other",
                                        "15",
                                        "13.0%",
                                    ],
                                    [
                                        "Work\u2013life balance",
                                        "3",
                                        "2.6%",
                                    ],
                                ],
                            },
                        },
                        {
                            "tblnote": "Residents selected a median of 2 barriers; 39.1% chose one and 31.3% chose three or more.",
                        },
                        {
                            "h3": "The reachable group is smaller than it looks",
                        },
                        {
                            "table": {
                                "head": [
                                    "Among the 62 residents with no interest",
                                    "n",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "Cited only modifiable barriers",
                                        "8",
                                        "12.9%",
                                    ],
                                    [
                                        "Cited only fixed barriers",
                                        "23",
                                        "37.1%",
                                    ],
                                    [
                                        "Cited both",
                                        "26",
                                        "41.9%",
                                    ],
                                    [
                                        "Cited neither",
                                        "5",
                                        "8.1%",
                                    ],
                                ],
                            },
                        },
                        {
                            "prose": "So 49 of 62 uninterested residents (79.0%) named at least one barrier no program can change. Counting barrier frequencies alone would suggest a third of residents might be won over by fixing scope or exposure; counting each resident\u2019s whole set shows that most who name a modifiable barrier name a fixed one too.",
                        },
                        {
                            "h3": "What would change their minds",
                        },
                        {
                            "table": {
                                "head": [
                                    "Theme in 58 free-text answers",
                                    "%",
                                ],
                                "rows": [
                                    [
                                        "More or earlier exposure",
                                        "40%",
                                    ],
                                    [
                                        "Fellowship structure or duration",
                                        "21%",
                                    ],
                                    [
                                        "Broader scope of practice",
                                        "19%",
                                    ],
                                    [
                                        "Fixed disinterest or external constraints",
                                        "17%",
                                    ],
                                    [
                                        "Patient population",
                                        "7%",
                                    ],
                                    [
                                        "Work\u2013life balance",
                                        "2%",
                                    ],
                                ],
                            },
                        },
                        {
                            "prose": "\u201cEarlier surgical exposure in residency and more lectures on those topics earlier as well.\u201d \u00b7 \u201cIf we had more exposure to a Uro trained [URPS] faculty then I would be more interested.\u201d \u00b7 \u201cThe main thing preventing me from pursuing is that it is not a 1 year fellowship.\u201d \u00b7 \u201cBroader training to develop a skill set that equally prepares me for male reconstructive procedures as well.\u201d \u00b7 And, plainly: \u201cI am mainly disinterested due to the patient population. Nothing can really change that.\u201d",
                        },
                        {
                            "h3": "Having no URPS urologist changes what residents complain about",
                        },
                        {
                            "table": {
                                "head": [
                                    "Among the 112 residents who knew",
                                    "No URPS faculty (n=23)",
                                    "Has faculty (n=89)",
                                    "OR (95% CI)",
                                    "p",
                                ],
                                "rows": [
                                    [
                                        "Cited limited exposure",
                                        "52.2%",
                                        "23.6%",
                                        "3.53 (1.36\u20139.16)",
                                        "0.011",
                                    ],
                                    [
                                        "Cited lack of mentorship",
                                        "34.8%",
                                        "9.0%",
                                        "5.40 (1.75\u201316.62)",
                                        "0.004",
                                    ],
                                ],
                            },
                        },
                        {
                            "tblnote": "The other six barriers did not differ by faculty availability (all p \u2265 0.28).",
                        },
                    ],
                },
                {
                    "id": "limits",
                    "title": "What this cannot tell you",
                    "nav": "Limitations",
                    "blocks": [
                        {
                            "bullets": [
                                "Cross-sectional, so the fall in interest across training years could be attrition or a cohort difference, and nothing here establishes cause.",
                                "Distribution through program leadership means there is no exact response rate, and residents interested in URPS were likelier to answer \u2014 so 46.1% is probably an overestimate.",
                                "Women were over-represented (41.7% of respondents versus roughly a third of US urology residents), and women reported more interest, which pushes the same way.",
                                "Residents cluster within programs, and program identity was not collected, so that clustering could not be modelled.",
                                "The multivariable models carry few events per covariate, which is why some intervals are very wide \u2014 the complexity-appeal odds ratios especially.",
                                "Faculty and fellowship presence, exposure and interest were all self-reported; three residents were unsure about their own program.",
                                "Free text was coded by one investigator without an inter-rater measure, and classifying a barrier as modifiable or fixed is a judgment others might make differently.",
                            ],
                        },
                    ],
                },
            ],
            "materials": [
                {
                    "label": "Manuscript \u2014 Exposure isn\u2019t everything (passphrase)",
                    "url": "/downloads/urps-exposure-manuscript/",
                },
                {
                    "label": "Manuscript \u2014 Who owns URPS? (passphrase)",
                    "url": "/downloads/urps-who-owns-manuscript/",
                },
                {
                    "label": "Manuscript \u2014 Why not URPS? (passphrase)",
                    "url": "/downloads/urps-why-not-manuscript/",
                },
                {
                    "label": "Abstract \u2014 Exposure isn\u2019t everything (passphrase)",
                    "url": "/downloads/abstract-urps-exposure/",
                },
                {
                    "label": "Abstract \u2014 Who owns URPS? (passphrase)",
                    "url": "/downloads/abstract-urps-who-owns/",
                },
                {
                    "label": "Abstract \u2014 Why not URPS? (passphrase)",
                    "url": "/downloads/abstract-urps-why-not/",
                },
            ],
            "next": "Three manuscripts are drafted and heading for submission. The implication we would most like to test is whether timetabled URPS teaching in the PGY-2 to PGY-3 window changes anything, because that is where the undecided still are \u2014 and whether framing the field around its full reconstructive scope, male and neurogenic included, moves the men who currently opt out.",
            "about": [
                "<b>My contribution.</b> Study design and the survey instrument, the analysis, and the writing of all three manuscripts.",
                "Approved by the Maimonides Medical Center Institutional Review Board (2026-02-08-MMC). Responses were anonymous; no respondent-level data appears on this page or anywhere on this site.",
            ],
            "sidefoot": "Gina DeMeo \u00b7 Henry M. Blair \u00b7 Nina Robins \u00b7 Luke Jenusaitis \u00b7 Jubin Matloubieh<br>Department of Urology, Maimonides Medical Center<br>Survey fielded July\u2013August 2026",
        },
    },

    {
        "slug": "aua-core-videos", "tab": "AUA Core Videos", "group": "current",
        "title": "AUA Core Curriculum teaching videos",
        "kicker": "American Urological Association · Core Curriculum teaching video submission",
        "status": "Submitted — AUA Core Curriculum, 31 August 2026",
        "summary": "Two procedures residents mostly learn by standing next to someone doing them: "
                   "sacral neuromodulation lead placement and vaginal pessary fitting. Both were "
                   "scripted, filmed and cut as teaching videos and submitted to the AUA's Core "
                   "Curriculum.",
        "stats": [("2", "videos submitted"), ("15:07", "total runtime"),
                  ("6", "pessary types covered"), ("1080p", "filmed and cut")],
        "tags": ["Medical education", "Surgical video", "Sacral neuromodulation",
                 "Pessary", "AUA Core Curriculum"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Luke Jenusaitis, MD", "Allison Polland, MD"],
            "lede": "The AUA Core Curriculum is where urology's apprenticeship gets written down for "
                    "everyone. These are two entries built for it — a sacral neuromodulation lead "
                    "placement and a pessary fitting — scripted, filmed, narrated and cut, and "
                    "submitted on 31 August 2026.",
            "status_detail": "Both videos were submitted to the AUA Core Curriculum on "
                             "<b>31 August 2026</b>, each with its written abstract and a "
                             "non-exclusive license to AUA Education &amp; Research. Runtimes are "
                             "7:58 and 7:09 — both inside the AUA's hard eight-minute cap. Awaiting "
                             "the AUA's decision; the cuts will be linked here once released.",
            "question": "How do you teach a procedure whose difficulty is entirely in the hands — where "
                        "to stand, what to feel for, what the wrong answer looks like — to someone who "
                        "cannot be in the room?",
            "approach": [
                "Each video is scripted section by section against the AUA's teaching-video format, "
                "with every line of narration mapped to the specific footage, still or diagram it "
                "plays over.",
                "Anatomic and procedural diagrams were built from scratch rather than sourced, "
                "because the AUA submission requires clear rights to every element on screen.",
                "Filmed at 1080p and cut to sit under the AUA's eight-minute limit — long enough to "
                "show the judgment, short enough that a trainee will actually watch it.",
                "Each submission is a package: the video, a written abstract, and a signed "
                "non-exclusive license.",
            ],
            "sections": [
                {"id": "snm", "title": "Sacral neuromodulation placement", "nav": "SNM video",
                 "intro": "Runtime 7:58 · submitted 31 August 2026",
                 "blocks": [
                     {"prose": "Percutaneous placement of a peripheral nerve evaluation (PNE) lead for "
                               "sacral neuromodulation, using the Medtronic InterStim system in a "
                               "patient with refractory overactive bladder."},
                     {"h3": "What the video walks through"},
                     {"bullets": [
                         "Patient positioning",
                         "Fluoroscopic localization of the S3 foramen",
                         "Needle and lead placement guided by motor and sensory response",
                         "Securing the lead and connecting an external trial stimulator",
                     ]},
                     {"callout": "Sacral neuromodulation is a reversible, office-based option for "
                                 "patients who have failed conservative and pharmacologic therapy, and "
                                 "a successful trial predicts response to permanent implantation. The "
                                 "video is built around the anatomic landmarks and the troubleshooting "
                                 "points a trainee actually needs."},
                 ]},
                {"id": "pessary", "title": "Vaginal pessaries: types and fitting", "nav": "Pessary video",
                 "intro": "Runtime 7:09 · submitted 31 August 2026",
                 "blocks": [
                     {"prose": "Pessaries are a safe, effective, first-line, non-surgical option for "
                               "pelvic organ prolapse and stress incontinence — and many trainees never "
                               "see a fitting performed. That gap is the reason this video exists."},
                     {"h3": "What the video walks through"},
                     {"bullets": [
                         "The three pessary families — support, space-filling, and incontinence — and "
                         "the six most commonly used types",
                         "A live fitting encounter: positioning, antiseptic prep, and trial of two "
                         "device sizes",
                         "Anatomic predictors of a harder fit: enlarged genital hiatus, "
                         "posterior-predominant prolapse, short vaginal length, advanced-stage prolapse",
                         "Follow-up, self-management, and complication management for safe long-term use",
                     ]},
                 ]},
            ],
            "videos": [
                {"title": "Sacral neuromodulation placement",
                 "caption": "7:58 · submitted to the AUA Core Curriculum, 31 August 2026. The cut will "
                            "be posted here or linked to the AUA's release once a decision is made."},
                {"title": "Vaginal pessaries: types and fitting",
                 "caption": "7:09 · submitted to the AUA Core Curriculum, 31 August 2026. The cut will "
                            "be posted here or linked to the AUA's release once a decision is made."},
            ],
            "materials": [
                {"label": "Watch: sacral neuromodulation placement (passphrase)",
                 "url": "/watch/aua-snm-video/"},
                {"label": "Watch: vaginal pessaries, types and fitting (passphrase)",
                 "url": "/watch/aua-pessary-video/"},
            ],
            "next": "Awaiting the AUA's decision on both submissions. The license is non-exclusive, so "
                    "the cuts can be linked here regardless of the outcome.",
            "sidefoot": "Henry M. Blair · Luke Jenusaitis, MD · Allison Polland, MD<br>"
                        "Department of Urology, Maimonides Medical Center<br>Submitted Aug 31, 2026",
        },
    },

    {
        "slug": "maude-sealing-devices", "tab": "MAUDE Device Safety", "group": "current",
        "title": "Adverse events of two vessel-sealing devices in robotic urologic surgery",
        "kicker": "FDA MAUDE database analysis · Maimonides Medical Center · MSRE, summer 2024",
        "status": "Presented — Society of Urologic Robotic Surgeons Focal Therapy Conference, 2024",
        "summary": "In March 2022 the FDA warned that two widely used robotic vessel-sealing devices could "
                   "fail to seal when too much tissue sits in the jaws. This study went to the FDA's own "
                   "adverse-event database to ask what actually gets reported about them, and whether the "
                   "two devices fail differently.",
        "stats": [("67", "urologic adverse-event reports reviewed"),
                  ("p = 0.025", "severity difference between devices"),
                  ("22% / 19%", "sealing / cutting issues, SynchroSeal")],
        "tags": ["Robotic surgery", "Device safety", "MAUDE", "FDA", "Adverse events"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Christopher Edwards", "Ariel Schulman, MD", "Jacob Khurgin, MD"],
            "lede": "Robotic vessel sealers cut and seal blood vessels in nearly every major urologic "
                    "operation. On 3 March 2022 the FDA issued a field safety notice about two of them — "
                    "SynchroSeal and Vessel Sealer Extend — warning that seals could fail when excessive "
                    "tissue is caught in the jaws. A safety notice says a failure mode is possible; the "
                    "FDA's adverse-event database says what has actually been reported.",
            "question": "What adverse events are reported for the SynchroSeal and Vessel Sealer Extend in "
                        "urologic surgery, do the two devices differ in the severity of what is reported, "
                        "and do the reports match the failure mode the FDA warned about?",
            "approach": [
                "The MAUDE database — the FDA's repository of mandatory manufacturer reports and voluntary "
                "reports from clinicians and patients — was queried for both devices across prostatectomy, "
                "nephrectomy, cystectomy, lymphadenectomy, nephroureterectomy and pyeloplasty.",
                "Every report was read and classified twice: by <b>severity</b>, and by whether the event "
                "was actually <b>related to device use</b> — the second axis matters because a device that "
                "attracts more unrelated reports looks worse than it is.",
                "Python scripts handled the classification and grouping of event descriptions into "
                "comparable categories.",
                "Chi-square analysis compared severity profiles between devices, then was repeated after "
                "excluding unrelated events — the comparison that answers the clinical question.",
                "37 SynchroSeal and 30 Vessel Sealer Extend urologic reports met criteria.",
            ],
            "findings": [
                "SynchroSeal drew more reports overall, but a higher share of them were unrelated to device "
                "use — the raw count is misleading on its own.",
                "After excluding unrelated events, SynchroSeal had significantly <b>fewer</b> severe and "
                "critical events than Vessel Sealer Extend (p = 0.025).",
                "The characteristic SynchroSeal failures were dislodged components, jaw-cover tears and "
                "thermal damage.",
                "Sealing issues appeared in 22% and cutting issues in 19% of urologic events — matching the "
                "failure mode the FDA's notice described, which is the finding that ties the database back "
                "to the warning.",
            ],
            "findings_note": "<b>Why the two-axis classification mattered.</b> Ranked by raw report count, "
                             "one device looks worse. Ranked by severity of events actually attributable to "
                             "the device, the ordering reverses. Reporting volume is not a safety signal.",
            "status_detail": "Conducted through the Medical Student Research Experience at Maimonides in "
                             "summer 2024 and presented at the Society of Urologic Robotic Surgeons Focal "
                             "Therapy Conference, 2024, and at regional surgical meetings.",
            "materials": [{"label": "Conference poster (PDF)", "url": "/downloads/2024-maude-msre-poster.pdf"}],
            "next": "The queries were restricted to urologic reports for time. Extending to all surgical "
                    "specialties would add the statistical power this analysis lacks and test whether the "
                    "severity difference holds outside urology.",
            "sidefoot": "Henry M. Blair · Ariel Schulman, MD · Jacob Khurgin, MD<br>MSRE · Maimonides Medical Center · 2024",
        },
    },

    {
        "slug": "nsqip-pipeline", "tab": "NSQIP Pipeline", "group": "current",
        "title": "A pipeline that turns the NSQIP files into a finished analysis",
        "kicker": "Research tooling \u00b7 ACS NSQIP Participant Use Files",
        "status": "In use \u2014 every NSQIP project on this site was built with it",
        "summary": "The ACS NSQIP public files are twelve years of fixed-width text whose columns appear, "
                   "vanish and change name between years. This is the toolchain I wrote to go from no "
                   "research question at all to a cohort, a live workbook, publication figures and a "
                   "written guide \u2014 about six thousand lines of Python, run by double-clicking one file.",
        "stats": [("6,085", "lines of Python"), ("397", "columns mapped across years"),
                  ("12", "PUF years, 2012\u20132023"), ("14", "statistics as live formulas")],
        "tags": ["NSQIP", "Research tooling", "Reproducibility", "Python", "Health services research"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair"],
            "lede": "Most of the work in a database study is not the analysis. It is turning a vague idea "
                    "into an answerable question, finding out whether the data can answer it, and then "
                    "rebuilding the whole thing when a variable turns out to be missing in 2014. This is "
                    "the machinery I built so that stops being the work.",
            "status_detail": "In active use. Every NSQIP analysis on this site \u2014 bleeding after TURP, "
                             "PVP and HoLEP; open versus robotic simple prostatectomy; prostatectomy in "
                             "the elderly and frail; same-day discharge after robotic prostatectomy; "
                             "opioids at discharge; sacrocolpopexy versus sacrospinous fixation \u2014 was "
                             "produced by this pipeline.",
            "question": "Can the distance between a half-formed research question and a defensible, "
                        "reproducible analysis be made short enough that the question is the hard part again?",
            "approach": [
                "<b>Ask first, extract second.</b> A question builder walks from \u201cno idea yet\u201d to one "
                "specific, feasible question, checked against what the data actually contains, before a "
                "single patient row is read.",
                "<b>A catalog with no patients in it.</b> Every primary CPT code in every year is counted "
                "up front, so feasibility is judged from counts alone.",
                "<b>One map across twelve years.</b> 397 columns are tracked year by year, which is what "
                "makes a 2012\u20132023 cohort possible at all \u2014 the files do not agree with each other "
                "about what they contain.",
                "<b>Statistics that stay live.</b> Rather than pasting numbers, each workbook carries "
                "fourteen custom spreadsheet functions. Change the cohort and every result recalculates "
                "in place.",
                "<b>Figures and a guide, built with it.</b> Each project ends with 300 dpi greyscale "
                "figures and an HTML guide explaining how to read its own workbook.",
                "<b>Rebuild without fear.</b> One command brings every project up to the current pipeline, "
                "backing up first and restoring on failure.",
            ],
            "sections": [
                {"id": "parts", "title": "What it is made of", "nav": "The parts",
                 "intro": "Fifteen Python modules and a double-clickable launcher.",
                 "blocks": [
                     {"table": {"head": ["Component", "Lines", "What it does"],
                                "rows": [
                        ["Question builder", "502", "From no idea to one specific, feasible question"],
                        ["Suggestion library", "353", "Procedure and diagnosis presets, variables, outcomes, analyses"],
                        ["Catalog", "105", "Counts of every primary CPT code in every year"],
                        ["Cohort extractor", "767", "Builds the cohort from the raw fixed-width files"],
                        ["Pipeline", "980", "The run itself, end to end"],
                        ["Workbook writers", "1,558", "The analysis workbook and its sheets"],
                        ["Statistics and figures", "560", "The statistics mirror and the figures"],
                        ["Guides", "443", "A written guide per project, plus one for older projects"],
                        ["Interfaces", "539", "The same questions, in a terminal or by clicking in Chrome"],
                        ["Maintenance", "278", "Rebuild everything; upgrade an existing sheet in place"],
                     ]}},
                 ]},
                {"id": "stats", "title": "Statistics as spreadsheet formulas", "nav": "The statistics",
                 "intro": "A workbook of pasted results goes stale the moment the cohort changes. A "
                          "workbook of formulas cannot.",
                 "blocks": [
                     {"bullets": [
                        "Wilson score intervals for every proportion, rather than the normal "
                        "approximation that misbehaves at the small denominators subgroup analysis produces",
                        "Fisher\u2019s exact test, with chi-squared where that is appropriate",
                        "Katz confidence intervals for risk ratios",
                        "Propensity-matched comparison flags carrying the hazard ratio, its interval and "
                        "the proportional-hazards p",
                        "Formatting functions so counts, percentages, odds ratios and p-values read the "
                        "same way in every table",
                     ]},
                     {"callout": "Fourteen functions in total, installed into each workbook automatically "
                                 "\u2014 so a collaborator opening the sheet gets working statistics rather "
                                 "than a screenshot of mine."},
                 ]},
                {"id": "data", "title": "Data handling", "nav": "Data handling",
                 "blocks": [
                     {"prose": "The NSQIP Participant Use Files are governed by a data-use agreement. The "
                               "raw files, the derived cohorts and the workbook sheet holding "
                               "patient-level rows stay on approved machines and are never published, "
                               "shared or committed. Nothing on this page, and no figure anywhere on this "
                               "site, contains patient-level data."},
                 ]},
            ],
            "next": "Extending the same approach to the other national datasets these projects draw on, "
                    "so a question asked of one can be asked of another without rebuilding the machinery.",
            "sidefoot": "Henry M. Blair<br>Department of Urology, Maimonides Medical Center",
        },
    },
        {
        "slug": "nsqip-opioids", "tab": "Opioids at Discharge", "group": "current",
        "title": "Half leave with opioids after urologic surgery",
        "kicker": "ACS NSQIP Participant Use File · 2024",
        "status": "Abstract submitted — 2027 AUA Annual Meeting",
        "summary": "Opioids prescribed at discharge are a modifiable source of persistent use and diversion. Using national data on discharge prescriptions, we described how often patients leave with an opioid after urologic surgery and how prescribing varies by procedure, surgical approach and patient characteristics.",
        "stats": [("55.4%", "discharged with an opioid"), ("59,773", "patients"), ("26–79%", "range across procedures"), ("2024", "PUF year")],
        "tags": ["Opioid prescribing", "NSQIP", "Quality improvement", "Urologic surgery"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Edward Wu", "Ariel Schulman"],
            "lede": "Opioids prescribed at discharge are a modifiable source of persistent use and diversion. Using national data on discharge prescriptions, we described how often patients leave with an opioid after urologic surgery and how prescribing varies by procedure, surgical approach and patient characteristics.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting. Built with the "
                             "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a>.",
            "question": "How often does a patient leave the hospital with an opioid after urologic surgery, and is that decided by the operation or by the patient?",
            "approach": ["We identified urologic procedures in the 2024 American College of Surgeons National Surgical Quality Improvement Program (ACS NSQIP) Participant Use File.", "Emergent cases, preoperative admission, moribund status, preoperative sepsis or ventilator dependence, and missing length of stay were excluded.", "The primary outcome was any opioid prescription at discharge; the secondary outcome was a prescription above 200 oral morphine milligram equivalents.", "Rates were compared across procedures, approaches and patient groups with unadjusted two-proportion tests."],
            "findings": ["Of 59,773 patients, 33,110 (55.4%) were discharged with an opioid.", "Prescribing ranged from 26.0% after bladder tumor resection to 79.1% after kidney surgery and varied by approach (endoscopic 26.9%, open 65.7%, minimally invasive 75.1%).", "Opioids were prescribed less to patients aged ≥ 70 (45.3% vs 62.2%), and more often to women (62.4% vs 53.8%) and inpatients (61.3% vs 51.5%; all p<0.001).", "Readmission rates were similar in those with vs without an opioid (overall 5.8% vs 6.2%) but also varied by procedure (TURBT 5.7% vs 5.6%; Radical prostatectomy 4.1% vs 5.2%)."],
            "findings_note": "More than half of patients leave the hospital with an opioid after urologic surgery. Procedure type explains far more of the variation (26% to 79%) than any patient factor (45% to 62%). Low prescribing after endoscopic procedures suggests opioid-free discharge is feasible for many patients.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-nsqip-opioids-at-discharge/"}],
            "sidefoot": "Henry M. Blair · Edward Wu · Ariel Schulman<br>Department of Urology, Maimonides Medical Center",
        },
    },
    {
        "slug": "nsqip-bph-bleeding", "tab": "BPH Bleeding", "group": "current",
        "title": "Bleeding after TURP, photoselective vaporization and HoLEP",
        "kicker": "ACS NSQIP Participant Use File · 2012–2024",
        "status": "Abstract submitted — 2027 AUA Annual Meeting",
        "summary": "Laser procedures for benign prostatic hyperplasia are often chosen to limit bleeding, particularly in anticoagulated men. We compared 30-day bleeding after transurethral resection of the prostate (TURP), photoselective vaporization (PVP) and holmium laser enucleation (HoLEP), and described changes in procedure mix and transfusion over 13 years.",
        "stats": [("123,020", "procedures"), ("0.28", "PVP vs TURP transfusion RR"), ("5.8→14.8%", "HoLEP share"), ("13", "years")],
        "tags": ["BPH", "Surgical therapy", "Bleeding", "NSQIP"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Edward Wu", "Michael Lee", "Payam Hakimian"],
            "lede": "Laser procedures for benign prostatic hyperplasia are often chosen to limit bleeding, particularly in anticoagulated men. We compared 30-day bleeding after transurethral resection of the prostate (TURP), photoselective vaporization (PVP) and holmium laser enucleation (HoLEP), and described changes in procedure mix and transfusion over 13 years.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting. Built with the "
                             "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a>.",
            "question": "Laser procedures are chosen to limit bleeding. Across thirteen years of national data, does that hold — and has bleeding fallen for every approach?",
            "approach": ["We identified TURP, PVP and HoLEP cases in the American College of Surgeons National Surgical Quality Improvement Program (ACS NSQIP) Participant Use File, 2012-2024.", "Emergent cases, preoperative admission, moribund status, preoperative sepsis or ventilator dependence, and missing length of stay were excluded.", "Outcomes were transfusion within 72 hours, reoperation and readmission for bleeding, a composite of the three, complications and readmission.", "PVP and HoLEP were compared with TURP using unadjusted relative risks, and yearly transfusion was tested for linear trend."],
            "findings": ["Of 123,020 procedures, 82,020 were TURP, 31,087 PVP and 9,913 HoLEP; HoLEP’s share rose from 5.8% to 14.8%.", "Compared with TURP, PVP had lower transfusion (0.25% vs 0.90%; relative risk 0.28, 95% confidence interval 0.22-0.35) and half the bleeding composite (1.4% vs 2.6%).", "HoLEP had similar bleeding (2.5% vs 2.6%) but fewer serious complications (1.4% vs 1.7%) and readmissions (4.1% vs 5.3%).", "Transfusion fell after all three: TURP 1.7% to 0.6%, PVP 0.5% to 0.0% (both p<0.001), HoLEP 2.5% to 0.5% (p=0.049)."],
            "findings_note": "PVP carried the lowest bleeding risk, while HoLEP matched TURP on bleeding with fewer complications and readmissions. Transfusion after surgery for benign prostatic hyperplasia has become rare nationally, declining for every procedure. It is likely that improved techniques, technology, and experience have contributed to this trend. Comparisons are unadjusted and do not account for prostate size.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-nsqip-bph-bleeding/"}],
            "sidefoot": "Henry M. Blair · Edward Wu · Michael Lee<br>Department of Urology, Maimonides Medical Center",
        },
    },
    {
        "slug": "nsqip-same-day-discharge", "tab": "Same-Day Discharge", "group": "current",
        "title": "The national shift to same-day discharge after robotic prostatectomy",
        "kicker": "ACS NSQIP Participant Use File · 2012–2024",
        "status": "Abstract submitted — 2027 AUA Annual Meeting",
        "summary": "Medicare removed laparoscopic radical prostatectomy from its Inpatient-Only List in January 2018, allowing same-day discharge. We described national uptake of same-day discharge after robot-assisted radical prostatectomy (RARP) and asked whether its growth has been accompanied by more readmissions or complications.",
        "stats": [("119,220", "patients"), ("&lt;1→15.6%", "same-day discharge"), ("0.78", "readmission risk ratio"), ("16×", "growth after 2018")],
        "tags": ["Prostate cancer", "Same-day discharge", "Health policy", "NSQIP"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Edward Wu", "Henry M. Blair", "Ariel Schulman"],
            "lede": "Medicare removed laparoscopic radical prostatectomy from its Inpatient-Only List in January 2018, allowing same-day discharge. We described national uptake of same-day discharge after robot-assisted radical prostatectomy (RARP) and asked whether its growth has been accompanied by more readmissions or complications.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting. Built with the "
                             "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a>.",
            "question": "Medicare opened the door to same-day discharge after prostatectomy in 2018. Did surgeons walk through it, and did readmissions rise when they did?",
            "approach": ["We identified RARP cases (laparoscopic or robotic; 94% robotic where recorded) in the American College of Surgeons National Surgical Quality Improvement Program (ACS NSQIP) Participant Use File, 2012-2024.", "Emergent cases, preoperative admission, moribund status, preoperative sepsis or ventilator dependence, and missing length of stay were excluded.", "Yearly same-day discharge rates were tested for linear trend.", "Thirty-day outcomes were compared with overnight stay, and readmission between 2012-2018 and 2019-2024, using unadjusted relative risks."],
            "findings": ["Of 119,220 patients, 7,088 (5.9%) went home the same day.", "The rate stayed below 1% through 2018, then rose to 1.9% in 2019 and 15.6% in 2024 (p<0.001 for trend), including patients aged 70 or older (0.6% to 8.2%).", "Compared with overnight stay, same-day discharge was associated with lower readmission (3.3% vs 4.2%; relative risk 0.78, 95% confidence interval 0.69-0.89), complications (5.0% vs 6.4%) and reoperation (0.5% vs 1.1%).", "Overall readmission did not change between eras (4.1% vs 4.2%; relative risk 1.02, 0.97-1.08)."],
            "findings_note": "Same-day discharge after RARP grew sixteenfold after 2018 and now applies to about one in six patients, without a rise in national readmission rates. Lower complication rates after same-day discharge likely reflect selection of healthier patients, and comparisons are unadjusted.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-nsqip-same-day-discharge/"}],
            "sidefoot": "Edward Wu · Henry M. Blair · Ariel Schulman<br>Department of Urology, Maimonides Medical Center",
        },
    },
    {
        "slug": "nsqip-rasp-vs-osp", "tab": "RASP vs OSP", "group": "current",
        "title": "The rapid rise of robot-assisted simple prostatectomy",
        "kicker": "ACS NSQIP Participant Use File · 2022–2024",
        "status": "Abstract submitted — 2027 AUA Annual Meeting",
        "summary": "Robot-assisted simple prostatectomy (RASP) is increasingly used for large-gland benign prostatic hyperplasia, but national data on its uptake and early safety compared with open simple prostatectomy (OSP) are limited. We described national adoption of RASP and compared 30-day outcomes between approaches, overall and across patient subgroups.",
        "stats": [("3,033", "simple prostatectomies"), ("73→91%", "robotic share"), ("0.10", "transfusion risk ratio"), ("11.2% vs 28.0%", "any complication")],
        "tags": ["BPH", "Simple prostatectomy", "Robotic surgery", "NSQIP"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Edward Wu", "Henry M. Blair", "Marino Kokolis-Lattanzio", "Ariel Schulman"],
            "lede": "Robot-assisted simple prostatectomy (RASP) is increasingly used for large-gland benign prostatic hyperplasia, but national data on its uptake and early safety compared with open simple prostatectomy (OSP) are limited. We described national adoption of RASP and compared 30-day outcomes between approaches, overall and across patient subgroups.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting. Built with the "
                             "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a>.",
            "question": "Robotic simple prostatectomy has all but replaced the open operation. What did that change in transfusion and complications?",
            "approach": ["We identified simple prostatectomies in 2022-2024 within the American College of Surgeons National Surgical Quality Improvement Program (ACS NSQIP) - either RASP (robot used) or OSP (open, no robot).", "Emergent cases, preoperative admission, moribund status, preoperative sepsis or ventilator dependence, and missing length of stay were excluded.", "Robotic share was tested for linear trend.", "Outcomes were compared with unadjusted relative risks and two-proportion or Fisher’s exact tests.", "Subgroups were defined by anesthesia risk class, frailty, age ≥70 years, obesity and anemia."],
            "findings": ["Of 3,033 simple prostatectomies, 2,580 (85.1%) were RASP, rising from 73.2% in 2022 to 91.2% in 2024 (p-trend<0.001).", "RASP had lower transfusion within 72 hours (1.8% vs 18.3%; relative risk 0.10, 95% confidence interval 0.07-0.14), any complication (11.2% vs 28.0%), readmission (5.5% vs 8.2%) and reoperation (1.6% vs 4.2%).", "Superficial wound infection (0.9% vs 2.6%) and kidney injury (0.7% vs 2.6%) were also less frequent; urinary infection, thromboembolism, pneumonia and sepsis did not differ.", "Lower transfusion held in every subgroup."],
            "findings_note": "RASP now accounts for more than 90% of simple prostatectomies in NSQIP hospitals and is associated with a tenfold lower transfusion rate and less than half the complication rate of OSP, a benefit that persists in older, frail and anemic patients. Comparisons are unadjusted and OSP patients carried more comorbidity, so selection bias is likely.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-nsqip-rasp-vs-osp/"}],
            "sidefoot": "Edward Wu · Henry M. Blair · Marino Kokolis-Lattanzio<br>Department of Urology, Maimonides Medical Center",
        },
    },
    {
        "slug": "nsqip-rasp-elderly", "tab": "RASP in the Elderly", "group": "current",
        "title": "Is anyone too old or too frail for robot-assisted simple prostatectomy?",
        "kicker": "ACS NSQIP Participant Use File · 2022–2024",
        "status": "Abstract submitted — 2027 AUA Annual Meeting",
        "summary": "Robot-assisted simple prostatectomy (RASP) is an established surgical approach for the treatment of large-gland benign prostatic hyperplasia (BPH). However, perioperative outcomes following RASP among elderly and frail patients remain incompletely characterized. This study aimed to evaluate and compare 30-day postoperative complications following RASP across age and frailty subgroups.",
        "stats": [("2,580", "men"), ("26.8%", "aged 75 or older"), ("20.5%", "frail (mFI ≥ 2)"), ("0.1%", "mortality")],
        "tags": ["BPH", "Frailty", "Older adults", "Robotic surgery", "NSQIP"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Edward Wu", "Henry M. Blair", "Ariel Schulman"],
            "lede": "Robot-assisted simple prostatectomy (RASP) is an established surgical approach for the treatment of large-gland benign prostatic hyperplasia (BPH). However, perioperative outcomes following RASP among elderly and frail patients remain incompletely characterized. This study aimed to evaluate and compare 30-day postoperative complications following RASP across age and frailty subgroups.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting. Built with the "
                             "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a>.",
            "question": "Age and frailty are routinely used to steer older men away from robotic simple prostatectomy. Do the outcomes justify that?",
            "approach": ["We identified robotic simple prostatectomies in 2022-2024 within the American College of Surgeons National Surgical Quality Improvement Program (ACS NSQIP).", "Serious complications were defined as wound dehiscence/infection, organ space infections, pneumonia, re-intubation, pulmonary embolism, renal failure, cerebrovascular accident, cardiac arrest, sepsis, and septic shock.", "Outcomes were compared with unadjusted relative risks and two-proportion or Fisher’s exact tests.", "Subgroups were defined by frailty (Modified Frailty Index (mFI) ≥ 2) and elderly status (age ≥75 years)."],
            "findings": ["Of 2,580 men, 691 (26.8%) were aged 75 or older, 519 (20.5%) were frail and 182 (7.2% were both).", "Older men had more complications overall (13.5% vs 10.3%; RR 1.3 95% confidence interval 1.03-1.64), transfusion (3.2% vs 1.3%), non-home discharge (2.0% vs 0.6%) and stays longer than one day (32.9% vs 25.8%), but similar serious complications (3.8% vs 3.4%) and readmission (5.6% vs 5.5%).", "Frail men had longer stays (36.0% vs 25.6%).", "Mortality was 0.1%."],
            "findings_note": "In men aged 75 or older and frail men, RASP was associated with longer stays, more transfusion, and more non-home discharge. However, rates of serious complication, readmission, and mortality remained low and similar to younger, non-frail men. RASP has demonstrated safety in the frail and elderly population with comparable rates of serious complications, readmission, and mortality.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-nsqip-rasp-elderly-frail/"}],
            "sidefoot": "Edward Wu · Henry M. Blair · Ariel Schulman<br>Department of Urology, Maimonides Medical Center",
        },
    },
    {
        "slug": "nsqip-colpopexy", "tab": "Sacrocolpopexy vs SSLF", "group": "current",
        "title": "Robotic sacrocolpopexy versus transvaginal sacrospinous ligament fixation",
        "kicker": "ACS NSQIP Participant Use File · 2022–2024",
        "status": "Abstract submitted — 2027 AUA Annual Meeting",
        "summary": "Apical pelvic organ prolapse can be repaired abdominally with robotic sacrocolpopexy (SCP) or vaginally with sacrospinous ligament fixation (SSLF), with or without a hysterectomy. While vaginal native tissue repairs are often considered a lower risk option, comparative data on postoperative complications between these remain limited. This study compared 30-day postoperative complications.",
        "stats": [("12,623", "patients"), ("6.6% vs 8.8%", "overall complications"), ("0.70", "UTI risk ratio"), ("5.4% vs 14.0%", "stay beyond one day")],
        "tags": ["Pelvic organ prolapse", "Reconstructive surgery", "Urinary tract infection", "NSQIP"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Arsha Venkat", "Edward Wu", "Henry M. Blair", "Allison Polland"],
            "lede": "Apical pelvic organ prolapse can be repaired abdominally with robotic sacrocolpopexy (SCP) or vaginally with sacrospinous ligament fixation (SSLF), with or without a hysterectomy. While vaginal native tissue repairs are often considered a lower risk option, comparative data on postoperative complications between these remain limited. This study compared 30-day postoperative complications.",
            "status_detail": "Abstract submitted to the 2027 AUA Annual Meeting. Built with the "
                             "<a href='/projects/nsqip-pipeline/'>NSQIP pipeline</a>.",
            "question": "Vaginal native-tissue repair is often presented as the lower-risk option for apical prolapse. Does the national record agree?",
            "approach": ["We identified patients who underwent SCP (CPT 57425, designated robotic) or SSLF (CPT 57282) in 2022-2024 in the National Surgical Quality Improvement Program (NSQIP).", "Serious complications were defined as wound dehiscence/infection, organ space infections, pneumonia, re-intubation, pulmonary embolism, renal failure, cerebrovascular accident, cardiac arrest, sepsis, and septic shock.", "Other complications included superficial infections, UTI, deep venous thromboses, and blood transfusions.", "Outcomes were compared with unadjusted relative risks (RR) and two-proportion or Fisher’s exact tests."],
            "findings": ["Of 12,623 patients, 7,589 underwent robotic SCP and 5,034 SSLF; 89% and 94% had concomitant procedures.", "Robotic SCP had fewer overall complications (6.6% vs 8.8%), reoperations (0.9% vs 1.5%) and stays >1 day (5.4% vs 14.0%).", "Serious complications (1.4% vs 1.3%) and readmission (1.9% each) were similar.", "UTI was less common after robotic SCP versus SSLF (3.6% vs 5.1%; RR 0.70, 95% CI 0.60-0.83).", "On subgroup analysis of patients without concomitant procedures, UTI risk remained elevated for the SSLF group (RR 0.56 [0.41-0.77])."],
            "findings_note": "Because SCP addresses all vaginal compartments, fewer SCP patients required concomitant procedures, potentially affecting outcomes. UTI differences suggest that the vaginal approach may influence UTI risk. However, unadjusted comparisons and differences in patient selection and prolapse severity may impact findings. Nonetheless, these results may help counsel patients hesitant about SCP.",
            "materials": [{"label": "Read the abstract (passphrase)",
                           "url": "/downloads/abstract-nsqip-colpopexy/"}],
            "sidefoot": "Arsha Venkat · Edward Wu · Henry M. Blair<br>Department of Urology, Maimonides Medical Center",
        },
    },
    {
        "slug": "dr-hank-med-ed-ai", "tab": None, "group": "earlier",
        "title": "Dr. Hank: a cited-source study assistant for medical students",
        "kicker": "Medical education tooling · personal project",
        "status": "Working prototype",
        "summary": "A study assistant built on a language model that answers Step 1 questions in a fixed "
                   "high-yield structure and — the part that matters — points to the actual page in First "
                   "Aid, AMBOSS or Rx Bricks rather than reproducing it.",
        "tags": ["Medical education", "Language models", "Study tools", "Citations"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair"],
            "lede": "Students asking a language model a Step 1 question get a fluent answer with no way to "
                    "check it, and no path back to the resource they already pay for. The design goal here "
                    "was the opposite: answer in the structure students actually study in, and end every "
                    "answer at a citation they can open.",
            "question": "Can a language model be made genuinely useful for board study without becoming "
                        "either a plagiarism engine or a confident source of unverifiable claims?",
            "approach": [
                "Answers follow a fixed structure — a direct high-yield response, then, where relevant, a "
                "disease breakdown covering pathophysiology and clinical features.",
                "Every answer cites the relevant section of First Aid, AMBOSS or Rx Bricks and links out "
                "to it; content is pointed at rather than reproduced, which keeps the tool on the right "
                "side of both copyright and comprehension.",
                "Response length, format and detail are refined by A/B testing, with user preference on "
                "formatting sampled every ten to twenty interactions.",
            ],
            "status_detail": "Working prototype. Related work: I sit on the ScholarRx Student Advisory "
                             "Committee and assist its AI development team.",
            "next": "The intended direction is a tool that identifies where a student is weak and generates "
                    "against it — practice questions, spaced-repetition decks, case presentations and study "
                    "plans — rather than only answering what is asked.",
            "sidefoot": "Henry M. Blair<br>SUNY Downstate College of Medicine",
            "in_progress": True,
        },
    },

    # ============================================================ earlier work

    {
        "slug": "insula-autism-thesis", "tab": None, "group": "earlier",
        "title": "Altered functional connectivity of the anterior insula in attention networks of autistic individuals",
        "kicker": "Honors thesis · Neuroscience and Behavioral Biology, Emory University · 2023",
        "status": "Defended April 2023 · Emory ETD",
        "summary": "The anterior insula has been studied in autism for years with conflicting results. "
                   "Analyzing sex separately rather than adjusting it away, connectivity with the attention "
                   "networks moved in opposite directions in autistic girls and autistic boys.",
        "tags": ["Autism", "fMRI", "Functional connectivity", "Sex differences", "Anterior insula"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Advisor: Opal Ousley, PhD",
                       "Committee: Gillian Hue, PhD · James Rilling, PhD"],
            "lede": "The anterior insula sits at the junction of the salience and ventral attention "
                    "networks — the machinery that decides what is worth attending to. It has been "
                    "implicated in autism for over a decade, with findings that contradict each other: "
                    "hyperconnectivity in some cohorts, hypoconnectivity in others. One explanation for "
                    "conflicting results is that a real effect is being averaged away.",
            "question": "Does anterior insula connectivity with the salience and ventral attention networks "
                        "differ in autism — and does it differ by sex, in a literature that has mostly "
                        "treated sex as a covariate?",
            "approach": [
                "ROI-to-ROI resting-state functional connectivity between the anterior insula and "
                "pre-specified regions of the salience and ventral attention networks.",
                "Males and females analyzed separately rather than pooled with sex as a covariate — the "
                "decision the whole thesis turns on.",
                "Standard preprocessing across all scans, with ROIs defined a priori and MNI coordinates "
                "reported.",
                "Connectivity matrices regressed against symptom instruments — SRS-2, SCQ and ADI-R — to "
                "test whether the differences carry behavioral meaning.",
            ],
            "findings": [
                "Connectivity differed significantly between autistic and non-autistic children, "
                "concentrated at the temporoparietal junction and supramarginal gyrus.",
                "The direction reversed by sex: <b>increased</b> connectivity in autistic females, "
                "<b>decreased</b> in autistic males — an effect that cancels toward null when the sexes "
                "are pooled.",
                "Preliminary regressions related resting-state connectivity in autistic females to symptom "
                "scores, suggesting connectivity may carry information about severity.",
            ],
            "findings_note": "<b>Why the conflicting literature may be conflicting.</b> If the effect runs "
                             "in opposite directions by sex, then cohorts differing in sex composition will "
                             "disagree — and averaging across sex will find less than either half contains.",
            "status_detail": "Bachelor of Science with Honors, Neuroscience and Behavioral Biology. "
                             "Defended April 2023; archived in the Emory Theses and Dissertations repository.",
            "materials": [
                {"label": "Read the thesis (PDF, 49 pp)", "url": "/downloads/2023-honors-thesis.pdf"},
                {"label": "Emory ETD record", "url": "https://etd.library.emory.edu/concern/etds/ms35tb215"},
            ],
            "next": "The sex-stratified result argues for replication in a larger cohort with enough "
                    "autistic girls to power the female analysis on its own — the sample constraint that "
                    "has shaped this literature from the start.",
            "sidefoot": "Henry M. Blair · Emory University<br>Advisor: Opal Ousley, PhD<br>Defended April 2023",
        },
    },

    {
        "slug": "varvel-ep2-status-epilepticus", "tab": None, "group": "earlier",
        "title": "Peripheral myeloid EP2 activation after status epilepticus",
        "kicker": "Varvel lab · Pharmacology and Chemical Biology, Emory University School of Medicine",
        "status": "Lab work · published as Varvel et al., J Neurosci 2021",
        "summary": "After status epilepticus a multi-part inflammatory response follows, driven partly by "
                   "COX-2 signalling through the EP2 receptor. This work isolated the contribution of "
                   "peripheral myeloid cells — the immune cells that arrive from outside the brain.",
        "tags": ["Epilepsy", "Neuroinflammation", "Status epilepticus", "Myeloid cells", "EP2"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Nicholas H. Varvel, PhD (principal investigator)", "Raymond Dingledine, PhD"],
            "lede": "Status epilepticus is followed by inflammation that does not simply accompany the "
                    "injury but contributes to it. The question this line of work asks is which cells are "
                    "responsible — brain-resident microglia, or myeloid cells recruited from the "
                    "periphery — because only one of those is reachable by a drug that does not cross "
                    "into the brain.",
            "question": "How much of the damaging inflammatory response after status epilepticus is driven "
                        "by EP2 activation on peripheral myeloid cells rather than on brain-resident cells?",
            "approach": [
                "Mouse models of status epilepticus with genetic and pharmacologic manipulation of EP2 "
                "signalling.",
                "Gene expression and PCR-based readouts of the inflammatory response.",
                "Separation of peripheral myeloid contribution from brain-resident microglial contribution.",
            ],
            "status_detail": "Work in Dr. Nicholas Varvel's laboratory at Emory. Published as Varvel NH, "
                             "Espinosa-Garcia C, Hunter-Chang S, et al., <i>Journal of Neuroscience</i> "
                             "2021;41(5):1105–1117.",
            "about": [
                      "I am not an author on the published paper; this page describes the laboratory "
                      "project I worked on, with the publication cited as its outcome."],
            "materials": [{"label": "Varvel et al., J Neurosci 2021 (DOI)",
                           "url": "https://doi.org/10.1523/JNEUROSCI.2040-20.2020"}],
            "sidefoot": "Varvel lab · Emory University School of Medicine",
            "in_progress": True,
        },
    },

    {
        "slug": "varvel-monocyte-engraftment", "tab": None, "group": "earlier",
        "title": "Brain-engrafted monocytes after microglia ablation",
        "kicker": "Varvel lab · Pharmacology and Chemical Biology, Emory University School of Medicine",
        "status": "Lab work · methods published in Methods Mol Biol 2019",
        "summary": "When brain-resident microglia are ablated, monocytes from the periphery move in and "
                   "take up residence. Whether those engrafted cells behave like the microglia they "
                   "replaced is the question the method was built to answer.",
        "tags": ["Neuroimmunology", "Microglia", "Monocytes", "Methods"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Nicholas H. Varvel, PhD (principal investigator)"],
            "lede": "Microglia can be depleted and the brain repopulated by monocytes recruited from the "
                    "blood. Those newcomers look like microglia and sit where microglia sat — but "
                    "functional equivalence is an assumption, not an observation, and it matters for every "
                    "therapy that proposes replacing brain immune cells.",
            "question": "Do peripherally derived monocytes that engraft in the brain after microglial "
                        "ablation function like the microglia they replace?",
            "approach": [
                "Microglial ablation in mouse models followed by engraftment of peripherally derived "
                "monocytes.",
                "Functional characterization of the engrafted population against resident microglia.",
            ],
            "status_detail": "Work in Dr. Nicholas Varvel's laboratory at Emory. Methods published as "
                             "Varvel NH, Ransohoff RM, Neher JJ, <i>Methods in Molecular Biology</i> "
                             "2019;2034:293–301.",
            "about": [
                      "I am not an author on the published methods chapter; this page describes the "
                      "laboratory project I worked on."],
            "materials": [{"label": "Methods Mol Biol 2019 (DOI)",
                           "url": "https://doi.org/10.1007/978-1-4939-9658-2_22"}],
            "sidefoot": "Varvel lab · Emory University School of Medicine",
            "in_progress": True,
        },
    },

    {
        "slug": "varvel-5xfad-inflammation", "tab": None, "group": "earlier",
        "title": "Sex-dependent inflammatory gene induction in prodromal Alzheimer's disease",
        "kicker": "Varvel lab · Pharmacology and Chemical Biology, Emory University School of Medicine",
        "status": "Lab work · published as Manji et al., J Alzheimers Dis 2019",
        "summary": "In the 5xFAD mouse, inflammatory gene induction during the prodromal stage — before "
                   "plaques dominate the picture — differs between males and females.",
        "tags": ["Alzheimer's disease", "Neuroinflammation", "Sex differences", "5xFAD"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Nicholas H. Varvel, PhD", "Thota Ganesh, PhD"],
            "lede": "Alzheimer's disease is roughly twice as common in women, and the inflammatory "
                    "component of the disease is one place that difference could originate. The prodromal "
                    "stage — before pathology is florid — is when a divergence would matter most and is "
                    "hardest to see in people.",
            "question": "Does inflammatory gene induction during the prodromal stage of Alzheimer's "
                        "pathology differ by sex in the 5xFAD mouse?",
            "approach": [
                "5xFAD transgenic mice examined at the prodromal stage rather than after established "
                "pathology.",
                "Inflammatory gene expression profiled and compared between males and females.",
            ],
            "status_detail": "Work in Dr. Nicholas Varvel's laboratory at Emory. Published as Manji Z, "
                             "Rojas A, Wang W, Dingledine R, Varvel NH, Ganesh T, <i>Journal of "
                             "Alzheimer's Disease</i> 2019;70(4):1259–1274.",
            "about": [
                      "I am not an author on the published paper; this page describes the laboratory "
                      "project I worked on."],
            "materials": [{"label": "J Alzheimers Dis 2019 (DOI)", "url": "https://doi.org/10.3233/JAD-180678"}],
            "sidefoot": "Varvel lab · Emory University School of Medicine",
            "in_progress": True,
        },
    },

    {
        "slug": "tbi-stress-pte", "tab": None, "group": "earlier",
        "title": "Traumatic stress at the moment of brain injury and the risk of post-traumatic epilepsy",
        "kicker": "Velíšková lab · Cell Biology & Anatomy, New York Medical College · STAR program · 2019",
        "status": "Presented as a poster, 2019",
        "summary": "Traumatic brain injury can set off epileptogenesis, and clinical data associate severe "
                   "stress at the moment of injury with worse outcomes — but preclinical work had studied "
                   "stress and injury only separately.",
        "tags": ["Epilepsy", "TBI", "Post-traumatic epilepsy", "Stress", "Epileptogenesis"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Aakash Raav", "Aryan Malhotra", "Jana Velíšková, MD, PhD"],
            "lede": "Post-traumatic epilepsy arrives late. Between the injury and the first unprovoked "
                    "seizure lies epileptogenesis — neuronal loss, mossy-fiber sprouting, and a shift "
                    "toward excitation in the hippocampus. Clinically, TBI rarely happens calmly, and "
                    "severe stress at the time of injury is associated with worse progression. No one had "
                    "delivered both insults together in an animal and watched what happened.",
            "question": "Does a severe stress event at the moment of cortical contusion increase seizure "
                        "susceptibility during the epileptogenic period?",
            "approach": [
                "Adult male rats were submerged for 45 seconds — a life-threatening stressor — immediately "
                "before controlled cortical impact. Controls swam freely before the same impact.",
                "Open-field and elevated-plus-maze testing confirmed the stress manipulation had worked, "
                "rather than assuming it.",
                "Seizure susceptibility was measured in a flurothyl chamber at five and ten days after "
                "injury — two points inside the epileptogenic window.",
            ],
            "findings": [
                "At five days the two groups were indistinguishable.",
                "By ten days the stressed animals had a significantly lower threshold for tonic-clonic "
                "seizures (p = 0.02) and spent longer seizing.",
                "The interaction therefore emerges during epileptogenesis rather than at the moment of "
                "injury — consistent with stress acting on the process that builds epilepsy, not on the "
                "injury itself.",
            ],
            "status_detail": "Presented as a poster through the STAR program at New York Medical College, "
                             "2019, under Dr. Jana Velíšková.",
            "materials": [{"label": "Poster (PDF)", "url": "/downloads/2019-tbi-stress-pte-poster.pdf"}],
            "sidefoot": "Velíšková lab · New York Medical College<br>STAR program · 2019",
        },
    },

    {
        "slug": "estrogen-dentate-gyrus", "tab": None, "group": "earlier",
        "title": "Estrogen and the dentate gyrus: response to spatial and environmental novelty",
        "kicker": "Velíšková lab · New York Medical College · STAR program · 2018",
        "status": "Paper and poster · Junior Science and Humanities Symposium",
        "summary": "Around 200,000 oophorectomies are performed in the United States each year, each "
                   "producing an abrupt loss of estradiol. What that loss — and its replacement — does to "
                   "the dentate gyrus was the question of my first study.",
        "tags": ["Estrogen", "Dentate gyrus", "Pattern separation", "Learning and memory"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Raissa Souza", "Sejal Schudasama", "Justin Garrel",
                       "Jana Velíšková, MD, PhD"],
            "lede": "Roughly 200,000 oophorectomies a year in the United States produce surgical menopause "
                    "and a sudden drop in estradiol; many of those women then take estrogen partly for "
                    "cognition. Estrogen receptors are dense in the dentate gyrus, the structure behind "
                    "pattern separation, and the lab had already shown estradiol altering long-term "
                    "potentiation there in vitro. What that did to behavior was open.",
            "question": "Does estradiol replacement after ovariectomy change how animals respond to spatial "
                        "and environmental novelty — the behavior the dentate gyrus is thought to support?",
            "approach": [
                "Eighteen ovariectomized Sprague-Dawley rats, replaced with β-estradiol (2 µg/day for four "
                "days) or oil vehicle, assigned at random.",
                "<b>Environmental change:</b> habituation across three trials in a circular arena with two "
                "objects 30 cm apart, then a single trial in a new square arena with the objects unmoved.",
                "<b>Metric change:</b> the same habituation, then the objects moved from 30 cm to 50 cm "
                "apart.",
                "Exploration scored from overhead video with ANY-maze, plus manual counts of rearing, "
                "object exploration and zone crossings.",
            ],
            "findings": [
                "Estradiol-replaced animals explored significantly less after the environmental change "
                "than oil-injected controls (p = 0.028).",
                "A similar direction followed the metric change.",
                "Together: estradiol modulates dentate-gyrus-mediated responses to novelty — the "
                "behavioral counterpart of the LTP differences the lab had recorded in vitro.",
            ],
            "findings_note": "<b>An honest limitation, noted at the time.</b> The metric change was run on "
                             "the same day as the environmental change, so the animals were no longer "
                             "meeting a novel environment when it began. The write-up called for repeating "
                             "it on its own day with new animals.",
            "status_detail": "Written up for the Junior Science and Humanities Symposium and presented as a "
                             "poster. My first study — run as a high-school student through the STAR "
                             "program at New York Medical College.",
            "materials": [
                {"label": "Paper (PDF, 20 pp)", "url": "/downloads/2018-estrogen-novelty-paper.pdf"},
                {"label": "Poster (PDF)", "url": "/downloads/2018-estrogen-novelty-poster.pdf"},
            ],
            "next": "Eight years later the same question — what estrogen does when it is taken away, and "
                    "what happens when it is given back — is the subject of the vaginal-estrogen study on "
                    "this site.",
            "sidefoot": "Velíšková lab · New York Medical College<br>STAR program · 2018",
        },
    },
]
