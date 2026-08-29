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
        "kicker": "Prospective study · Maimonides Medical Center",
        "status": "Submitted — Family Practice (Oxford University Press)",
        "summary": "AUA guidelines require a post-void residual measurement to diagnose overactive bladder — "
                   "which needs an in-office ultrasound, at odds with the telemedicine pathway the same "
                   "guidelines endorse. We asked whether women can estimate their own PVR.",
        "tags": ["Overactive bladder", "Telemedicine", "Guidelines", "Access to care"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Colby Rondeau", "Allison Polland, MD"],
            "lede": "A guideline can contradict itself. AUA guidance endorses telemedicine as a way to "
                    "evaluate overactive bladder, and separately requires a post-void residual measurement "
                    "to make the diagnosis — which requires the office visit telemedicine was meant to "
                    "avoid. This study asks whether the requirement can be met another way: can a woman "
                    "estimate her own PVR?",
            "question": "If in-office PVR measurement is what blocks telemedical evaluation of overactive "
                        "bladder, can patients estimate their own residual accurately enough to substitute "
                        "for it — and if not, is the requirement doing enough work to justify the barrier?",
            "approach": [
                "Women presenting with overactive-bladder symptoms estimated their post-void residual "
                "before it was measured by bladder scan, following earlier work in which patients estimated "
                "<b>voided</b> volumes accurately.",
                "Agreement between estimated and measured PVR was assessed against the thresholds that "
                "actually matter clinically — incomplete emptying and frank retention — rather than by "
                "correlation alone.",
                "The prevalence of incomplete emptying and retention in this population was measured "
                "directly, since the value of a screening requirement depends on how often it finds "
                "anything.",
            ],
            "findings": [
                "Women could <b>not</b> reliably estimate their own PVR — self-estimation is not a "
                "substitute for measurement.",
                "But incomplete emptying was rare and no woman met criteria for retention.",
                "So the argument the paper makes is not that patients can self-measure; it is that the "
                "requirement can be safely deferred for low-risk women with OAB symptoms and no retention "
                "history — which reopens the telemedicine pathway the guidelines already endorse.",
            ],
            "findings_note": "<b>A negative result doing useful work.</b> The headline finding failed; the "
                             "clinically relevant one came from the denominator. Both are reported.",
            "status_detail": "Submitted to <i>Family Practice</i> (Oxford University Press).",
            "next": "If the deferral argument holds, the natural follow-on is a telemedicine pathway with "
                    "an explicit low-risk rule, tested prospectively against in-office evaluation.",
            "sidefoot": "Henry M. Blair · Colby Rondeau · Dr. Allison Polland<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
        },
    },

    {
        "slug": "oab-adi", "tab": "Deprivation & Access", "group": "current",
        "title": "Does neighborhood deprivation predict urogynecologic access in Brooklyn?",
        "kicker": "Retrospective cohort · Maimonides Medical Center",
        "status": "Manuscript V3",
        "summary": "A companion overactive-bladder study testing whether the Area Deprivation Index and "
                   "travel burden relate to access and disease severity — and whether ADI is even a valid "
                   "instrument in a dense, transit-rich city.",
        "tags": ["Overactive bladder", "Health equity", "Area Deprivation Index", "Urban health"],
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Henry M. Blair", "Allison Polland, MD"],
            "lede": "The Area Deprivation Index is used across American health services research as a "
                    "stand-in for a patient's material circumstances. It was built on neighborhoods where "
                    "distance means a car. Brooklyn is not that place — and if the index's mechanism is "
                    "travel burden, it may not measure what it claims to measure here.",
            "question": "Do neighborhood deprivation and travel burden predict access to urogynecologic "
                        "care and severity at presentation in Brooklyn — and is ADI a valid instrument in "
                        "a dense city with robust public transit?",
            "approach": [
                "Patients seen for overactive bladder were linked to their neighborhood ADI and to "
                "estimates of travel time and travel cost to the clinic.",
                "Two questions were asked separately: whether deprivation tracks access and severity, and "
                "whether ADI behaves as a valid instrument in this setting at all.",
                "Symptom severity at presentation and follow-up attendance were the outcomes, rather than "
                "a single composite of 'access'.",
            ],
            "findings": [
                "ADI did not track access or severity in this population — the expected gradient was "
                "largely absent.",
                "Travel cost and travel time, measured directly, were associated with poorer follow-up and "
                "with more severe presentation.",
                "Disadvantaged women were more likely to report urge urinary frequency.",
            ],
            "findings_note": "<b>The methodological point.</b> Where transit blunts distance, a deprivation "
                             "index built on car-dependent geography can go quiet while the underlying "
                             "barrier is still there and still measurable — a caution about importing "
                             "these indices into urban populations unexamined.",
            "status_detail": "Manuscript V3.",
            "next": "Replication in other transit-dense cities would establish whether this is a Brooklyn "
                    "finding or a property of urban geography generally.",
            "sidefoot": "Henry M. Blair · Dr. Allison Polland<br>Department of Urology, Maimonides Medical Center",
            "in_progress": True,
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
