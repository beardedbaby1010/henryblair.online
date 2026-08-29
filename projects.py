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
DOWNLOAD_GATES = {
    "2024-maude-msre-poster.pdf": {
        "title": "Analysis of adverse events, robotic urological surgeries",
        "subtitle": "Conference poster · Society of Urologic Robotic Surgeons Focal Therapy, 2024",
        "back_url": "/projects/maude-sealing-devices/", "back_label": "back to the project",
    },
    "Henry_Blair_CV_2026_Aug.pdf": {
        "title": "Curriculum vitae — Henry M. Blair",
        "subtitle": "Updated August 2026",
        "back_url": "/resume/", "back_label": "back to the resume",
    },
}

# ---------------------------------------------------------------- hand-written pages
PAGES = [
    {"key": "about",   "tab": "About Me",           "href": "/about/",   "file": "about/index.html"},
    {"key": "contact", "tab": "Contact Me",         "href": "/contact/", "file": "contact/index.html"},
    {"key": "resume",  "tab": "Resume",             "href": "/resume/",  "file": "resume/index.html"},
    {"key": "home",    "tab": "Research Portfolio", "href": "/",         "file": "index.html"},
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
        "paper": {"pdf": "Maimo_Work/PCa/Henry - PCa Manuscript V7.pdf",
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
        "paper": {"pdf": "Maimo_Work/VE/Henry - VE Manuscript V3.pdf",
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
        "paper": {"pdf": "Maimo_Work/OAB Proj/PVR/Henry Edits V7 PVR Manuscript Family Practice.pdf",
                  "label": "Manuscript V7", "note": "Submitted to Family Practice (OUP)."},
        "hub": {
            "people": ["Colby Rondeau", "Henry M. Blair", "Sumyia Razzak", "Sarah Chaudhary",
                       "Trashana Smith", "Michael Silver", "Allison Polland, MD"],
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
            "sidefoot": "Colby Rondeau · Henry M. Blair · Dr. Allison Polland<br>Department of Urogynecology, "
                        "Maimonides Medical Center<br>Brooklyn, NY · 2024–2025",
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
                  "label": "Manuscript V3", "note": "With Colby Rondeau and Dr. Allison Polland."},
        "hub": {
            "people": ["Colby Rondeau", "Luke Jenusaitis", "Elizabeth DeSellier", "Rebecca Bergmann",
                       "Peace Deh", "Michael Silver", "Henry M. Blair", "Allison Polland, MD"],
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
            "sidefoot": "Colby Rondeau · Henry M. Blair · Dr. Allison Polland<br>Maimonides Medical Center · "
                        "SUNY Downstate<br>Brooklyn, NY · 2024–2025",
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
        "paper": {"pdf": "Maimo_Work/Oliver Menken/Henry - V3 - What Do Patients with Nocturia Want Treated_ Patient-Defined Goals and Tolerance Beyond Void Count.pdf",
                  "label": "Manuscript V3", "note": "With Oliver Menken."},
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Oliver Menken"],
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
            "sidefoot": "Henry M. Blair · Oliver Menken<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "retzius-retention", "tab": "Retzius-Sparing RARP", "group": "current",
        "title": "Urinary retention after Retzius-sparing prostatectomy",
        "kicker": "Retrospective cohort · Maimonides Medical Center",
        "status": "Manuscript V1 · IRB protocol in place for a prospective follow-on",
        "summary": "Retzius-sparing robotic prostatectomy gives men better early continence, but preserving "
                   "the anterior compartment may cost postoperative retention — and no study has examined "
                   "retention as a primary outcome or identified who is at risk.",
        "tags": ["Prostate cancer", "RARP", "Urinary retention", "Surgical outcomes"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Ervin Teper, MD", "David Silver, MD"],
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
            "sidefoot": "Henry M. Blair · Dr. Ervin Teper · Dr. David Silver<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "focal-therapy-continence", "tab": "Focal Therapy", "group": "current",
        "title": "Continence outcomes after focal therapy for prostate cancer",
        "kicker": "Chart review · Maimonides Medical Center",
        "status": "Early stage",
        "summary": "Urinary outcomes — incontinence and leakage — after HIFU and irreversible "
                   "electroporation, the ablative options offered in place of whole-gland treatment.",
        "tags": ["Prostate cancer", "Focal therapy", "HIFU", "Irreversible electroporation", "Continence"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair"],
            "lede": "Focal therapy is offered on a continence argument: treat part of the gland, spare the "
                    "function. That argument deserves outcome data from the men who took it.",
            "question": "What are the urinary continence outcomes — incontinence, leakage — after HIFU and "
                        "irreversible electroporation for prostate cancer?",
            "approach": [
                "Chart review of patients treated with HIFU or irreversible electroporation.",
                "Continence and leakage as the primary outcomes, recorded against baseline function.",
            ],
            "status_detail": "Early stage — cohort assembly underway.",
            "sidefoot": "Henry M. Blair<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "ketamine-cystitis", "tab": "Ketamine Cystitis", "group": "current",
        "title": "Ketamine cystitis in the United States",
        "kicker": "National epidemiology",
        "status": "Early stage",
        "summary": "Characterizing the incidence and demographics of ketamine-associated cystitis over the "
                   "past decade — positioned to be the largest study of its kind to date.",
        "tags": ["Ketamine cystitis", "Epidemiology", "Substance use", "Real-world data"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair"],
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
            "sidefoot": "Henry M. Blair<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "urogyn-perceptions", "tab": "Urogyn Survey", "group": "current",
        "title": "How urology residents perceive urogynecology",
        "kicker": "National survey · every U.S. urology residency",
        "status": "Data collection underway",
        "summary": "A survey distributed to every urology residency in the country, measuring residents' "
                   "knowledge of urogynecology and what shapes their perception of it — the pipeline "
                   "question behind a subspecialty shortage.",
        "tags": ["Urogynecology", "Medical education", "Workforce", "Survey"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Allison Polland, MD"],
            "lede": "Subspecialty shortages are usually described in terms of positions and pay. Before "
                    "either, there is what trainees think the field is — and residents choose from the "
                    "picture they have, not the one that is accurate.",
            "question": "What do U.S. urology residents know about urogynecology, how do they perceive the "
                        "field, and what shapes that perception during training?",
            "approach": [
                "A survey instrument distributed to every urology residency program in the country.",
                "Knowledge and perception measured separately, since a field can be well regarded and "
                "poorly understood, or the reverse.",
                "Exposure during training recorded alongside, so perception can be read against how much "
                "of the field a resident has actually seen.",
            ],
            "status_detail": "Data collection underway.",
            "sidefoot": "Henry M. Blair · Dr. Allison Polland<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "aua-core-videos", "tab": "AUA Core Videos", "group": "current",
        "title": "AUA Core Curriculum instructional videos",
        "kicker": "American Urological Association · Core Curriculum",
        "status": "Produced · sacral neuromodulation and pessary fitting",
        "summary": "Instructional videos for the AUA's Core Curriculum: sacral neuromodulation device "
                   "implantation, and pessary fitting — procedures taught mostly by watching, filmed so "
                   "they can be watched.",
        "tags": ["Medical education", "Surgical video", "Sacral neuromodulation", "Pessary", "AUA"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Allison Polland, MD"],
            "lede": "Two procedures that residents learn by standing next to someone doing them. The AUA "
                    "Core Curriculum is where that apprenticeship is written down for everyone; these are "
                    "the two entries I filmed, scripted and cut.",
            "question": "How do you teach a procedure whose difficulty is entirely in the hands — where to "
                        "stand, what to feel for, what the wrong answer looks like — to someone who cannot "
                        "be in the room?",
            "approach": [
                "<b>Sacral neuromodulation device implantation</b> — lead placement and implantation, "
                "filmed stepwise with the anatomy called out as it appears.",
                "<b>Pessary fitting</b> — sizing and fitting, including the judgment that decides between "
                "sizes rather than only the technique.",
                "Scripted against the AUA's Core Curriculum format, filmed in theatre, and cut with "
                "captions so a step can be found without watching the whole thing.",
            ],
            "videos": [
                {"title": "Sacral neuromodulation device implantation",
                 "caption": "Final cut is with the AUA. It will be posted here, or linked to the AUA's "
                            "curriculum, once it is released."},
                {"title": "Pessary fitting",
                 "caption": "Final cut is with the AUA. It will be posted here, or linked to the AUA's "
                            "curriculum, once it is released."},
            ],
            "status_detail": "Both videos produced. Final cuts sit with the AUA for the Core Curriculum; "
                             "they will be embedded on this page or linked to the AUA's own release.",
            "sidefoot": "Henry M. Blair · Dr. Allison Polland<br>Department of Urology, Maimonides Medical Center",
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
            "sidefoot": "Henry M. Blair · Dr. Ariel Schulman · Dr. Jacob Khurgin<br>MSRE · Maimonides Medical Center · 2024",
        },
    },

    {
        "slug": "dr-hank-med-ed-ai", "tab": "Med-Ed AI", "group": "current",
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
        "slug": "insula-autism-thesis", "tab": "Honors Thesis", "group": "earlier",
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
            "sidefoot": "Henry M. Blair · Emory University<br>Advisor: Dr. Opal Ousley<br>Defended April 2023",
        },
    },

    {
        "slug": "varvel-ep2-status-epilepticus", "tab": "EP2 & Status Epilepticus", "group": "earlier",
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
            "about": ["<b>My contribution.</b> [Placeholder — describe your specific role on this project "
                      "in your own words: which experiments, which techniques, over what period. I have "
                      "deliberately not invented one. Edit this in projects.py.]",
                      "I am not an author on the published paper; this page describes the laboratory "
                      "project I worked on, with the publication cited as its outcome."],
            "materials": [{"label": "Varvel et al., J Neurosci 2021 (DOI)",
                           "url": "https://doi.org/10.1523/JNEUROSCI.2040-20.2020"}],
            "sidefoot": "Varvel lab · Emory University School of Medicine",
            "in_progress": True,
        },
    },

    {
        "slug": "varvel-monocyte-engraftment", "tab": "Monocyte Engraftment", "group": "earlier",
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
            "about": ["<b>My contribution.</b> [Placeholder — describe your specific role in your own "
                      "words. Edit this in projects.py.]",
                      "I am not an author on the published methods chapter; this page describes the "
                      "laboratory project I worked on."],
            "materials": [{"label": "Methods Mol Biol 2019 (DOI)",
                           "url": "https://doi.org/10.1007/978-1-4939-9658-2_22"}],
            "sidefoot": "Varvel lab · Emory University School of Medicine",
            "in_progress": True,
        },
    },

    {
        "slug": "varvel-5xfad-inflammation", "tab": "5xFAD Inflammation", "group": "earlier",
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
            "about": ["<b>My contribution.</b> [Placeholder — describe your specific role in your own "
                      "words. Edit this in projects.py.]",
                      "I am not an author on the published paper; this page describes the laboratory "
                      "project I worked on."],
            "materials": [{"label": "J Alzheimers Dis 2019 (DOI)", "url": "https://doi.org/10.3233/JAD-180678"}],
            "sidefoot": "Varvel lab · Emory University School of Medicine",
            "in_progress": True,
        },
    },

    {
        "slug": "tbi-stress-pte", "tab": "TBI & Stress", "group": "earlier",
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
        "slug": "estrogen-dentate-gyrus", "tab": "Estrogen & Dentate Gyrus", "group": "earlier",
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
