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

    {
        "slug": "adt-initiation",
        "tab": "ADT Initiation",
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
        "tags": ["Prostate cancer", "ADT", "Bone health", "Treatment intensification", "TriNetX", "Health equity"],
        "page": {"kind": "generated", "source": "_source/pca_project_hub_standalone.html", "strip_paper": True},
        "paper": {"pdf": "Maimo_Work/PCa/Henry - PCa Manuscript V7.pdf",
                  "label": "Manuscript V7", "note": "In preparation; not yet under review."},
    },

    {
        "slug": "ve-boxed-warning",
        "tab": "Vaginal Estrogen",
        "title": "Prescribing After the Warning Disappeared",
        "kicker": "Retrospective cohort study · TriNetX Global Collaborative Network",
        "status": "Manuscript V3",
        "summary": "For twenty-two years low-dose vaginal estrogen carried the same boxed warning as "
                   "high-dose systemic hormone therapy. The FDA removed it on 11 November 2025. Nine months "
                   "on either side of that date, prescribing rose — and it rose most in the women the "
                   "warning had most deterred.",
        "stats": [("+14.3%", "use per woman seen"),
                  ("1.29",   "rate ratio in breast-cancer survivors"),
                  ("1.47 / 0.88", "estrogen positive control vs negative controls"),
                  ("192,157","women on vaginal estrogen")],
        "tags": ["Menopause", "GSM", "FDA labeling", "Pharmacoepidemiology", "Breast cancer", "TriNetX"],
        "page": {"kind": "static"},
        "paper": {"pdf": "Maimo_Work/VE/Henry - VE Manuscript V3.pdf",
                  "label": "Manuscript V3", "note": "Co-authored with Dr. Arshia Sandozi."},
    },

    # ---- card-only for now; give each a "page" entry when its hub is built ----

    {
        "slug": "retzius-retention",
        "tab": None,
        "title": "Urinary retention after Retzius-sparing prostatectomy",
        "kicker": "Retrospective cohort · Maimonides Medical Center",
        "status": "Manuscript V1 · with Drs. Teper & Silver",
        "summary": "Retzius-sparing robotic prostatectomy gives men better early continence, but preserving "
                   "the anterior compartment may cost postoperative retention — and no study has examined "
                   "retention as a primary outcome. In ~200 patients I am measuring its incidence and testing "
                   "predictors: membranous urethral length, intravesical prostatic protrusion, prostate "
                   "volume, baseline LUTS, PSA, diabetes, frailty, and peri-operative alpha-blocker, 5-ARI "
                   "and ADT use.",
        "tags": ["Prostate cancer", "RARP", "Urinary retention", "Surgical outcomes"],
        "page": None,
        "sources": {"folder": "Maimo_Work/RxRS-RARP"},
    },

    {
        "slug": "oab-pvr",
        "tab": None,
        "title": "Can women self-estimate their post-void residual?",
        "kicker": "Prospective study · with Colby Rondeau and Dr. Polland",
        "status": "Submitted — Family Practice (Oxford University Press)",
        "summary": "AUA guidelines require a post-void residual measurement to diagnose overactive bladder — "
                   "which needs an in-office ultrasound, at odds with the telemedicine pathway the same "
                   "guidelines endorse. Women could not estimate their own PVR reliably; but incomplete "
                   "emptying was rare and no woman met criteria for retention, so the in-office requirement "
                   "may be safely deferred for low-risk women, opening the door to telemedicine.",
        "tags": ["Overactive bladder", "Telemedicine", "Guidelines", "Access to care"],
        "page": None,
        "sources": {"folder": "Maimo_Work/Colby - OAB + PVR"},
    },

    {
        "slug": "oab-adi",
        "tab": None,
        "title": "Does neighborhood deprivation predict urogynecologic access in Brooklyn?",
        "kicker": "Retrospective cohort · Maimonides Medical Center",
        "status": "Manuscript V3",
        "summary": "A companion overactive-bladder study testing whether the Area Deprivation Index and "
                   "travel burden relate to access and disease severity — and whether ADI is even valid in a "
                   "dense, transit-rich city. It did not track access or severity in Brooklyn, likely because "
                   "public transit blunts the travel barriers seen elsewhere; disadvantaged women were, "
                   "however, more likely to report urge frequency.",
        "tags": ["Overactive bladder", "Health equity", "Area Deprivation Index", "Urban health"],
        "page": None,
        "sources": {"folder": "Maimo_Work/OAB Proj"},
    },

    {
        "slug": "nocturia-goals",
        "tab": None,
        "title": "What do patients with nocturia actually want treated?",
        "kicker": "Patient-reported outcomes · with Oliver Menken",
        "status": "Manuscript V3",
        "summary": "Nocturia trials fixate on nightly void count, but that may not be what patients care "
                   "about. This study examines patient-defined treatment goals and how much nighttime "
                   "urination patients will tolerate — outcomes beyond the void count.",
        "tags": ["Nocturia", "Patient-reported outcomes", "Trial design"],
        "page": None,
        "sources": {"folder": "Maimo_Work/Oliver Menken"},
    },

    {
        "slug": "focal-therapy-continence",
        "tab": None,
        "title": "Continence outcomes after focal therapy for prostate cancer",
        "kicker": "Chart review · Maimonides Medical Center",
        "status": "Early stage",
        "summary": "Urinary outcomes — incontinence and leakage — after HIFU and irreversible "
                   "electroporation, the two ablative options offered in place of whole-gland treatment.",
        "tags": ["Prostate cancer", "Focal therapy", "HIFU", "Continence"],
        "page": None,
    },

    {
        "slug": "ketamine-cystitis",
        "tab": None,
        "title": "Ketamine cystitis in the United States",
        "kicker": "National epidemiology",
        "status": "Early stage",
        "summary": "Characterizing the incidence and demographics of ketamine-associated cystitis over the "
                   "past decade — age, geography, and trajectory — positioned to be the largest study of its "
                   "kind to date.",
        "tags": ["Ketamine cystitis", "Epidemiology", "Substance use"],
        "page": None,
    },

    {
        "slug": "urogyn-perceptions",
        "tab": None,
        "title": "How urology residents perceive urogynecology",
        "kicker": "National survey · every U.S. urology residency",
        "status": "Data collection underway",
        "summary": "A survey distributed to every urology residency in the country, measuring residents' "
                   "knowledge of the urogynecology field and what shapes their perception of it — the "
                   "pipeline question behind a subspecialty shortage.",
        "tags": ["Urogynecology", "Medical education", "Workforce"],
        "page": None,
        "sources": {"folder": "Maimo_Work/Urogynecology Impressions"},
    },

    {
        "slug": "aua-core-videos",
        "tab": None,
        "title": "AUA Core Curriculum instructional videos",
        "kicker": "American Urological Association",
        "status": "Produced",
        "summary": "Instructional videos for the AUA's Core Curriculum: sacral neuromodulation device "
                   "implantation, and pessary fitting.",
        "tags": ["Medical education", "Surgical video", "AUA"],
        "page": None,
        "sources": {"folder": "Maimo_Work/Video_abstracts"},
    },
]

# ---------------------------------------------------------------- earlier work
# Emory honors thesis, college and high-school posters. Fill this in and the
# build renders an "Earlier work" section on the portfolio page.
EARLIER = [

    {
        "title": "Altered functional connectivity of the anterior insula in attention networks",
        "kicker": "Honors thesis · Neuroscience and Behavioral Biology, Emory University · advisor Opal Ousley, PhD",
        "year": 2023,
        "summary": "The anterior insula has been studied in autism for years with conflicting results. "
                   "Analyzing sex separately, I measured ROI-to-ROI resting-state connectivity between the "
                   "anterior insula and the salience and ventral attention networks. Connectivity differed by "
                   "sex in opposite directions — increased in autistic girls, decreased in autistic boys — "
                   "most clearly at the temporoparietal junction and supramarginal gyrus, and preliminary "
                   "regressions related that connectivity to symptom scores (SRS-2, SCQ, ADI-R). A finding "
                   "that argues sex belongs in the analysis rather than in the covariates. Defended April 2023.",
        "thumb": "/earlier/thumbs/2023-honors-thesis.jpg",
        "links": [{"label": "Read the thesis (PDF, 49 pp)", "url": "/earlier/files/2023-honors-thesis.pdf"},
                  {"label": "Emory ETD record", "url": "https://etd.library.emory.edu/concern/etds/ms35tb215"}],
    },

    {
        "title": "Traumatic stress at the moment of brain injury and the risk of post-traumatic epilepsy",
        "kicker": "STAR program · Department of Cell Biology & Anatomy, New York Medical College · with Dr. Jana Velíšková",
        "year": 2019,
        "summary": "Traumatic brain injury can set off epileptogenesis — the months or years of neuronal "
                   "loss, mossy-fiber sprouting and shifting excitation that precede a first unprovoked "
                   "seizure. Clinically, severe stress at the moment of injury is associated with worse "
                   "outcomes, but preclinical work had studied stress and injury separately and never "
                   "together. Adult male rats were submerged for 45 seconds before a controlled cortical "
                   "impact; controls swam freely before the same impact. Open-field and elevated-plus-maze "
                   "testing confirmed the stress manipulation, then flurothyl seizure thresholds were measured "
                   "at five and ten days. At five days the groups were indistinguishable; by ten days the "
                   "stressed animals had a lower threshold for tonic-clonic seizures (p = 0.02) and seized "
                   "longer — the interaction emerging inside the epileptogenic window rather than at the "
                   "moment of injury.",
        "thumb": "/earlier/thumbs/2019-tbi-stress-pte-poster.jpg",
        "links": [{"label": "Poster (PDF)", "url": "/earlier/files/2019-tbi-stress-pte-poster.pdf"}],
    },

    {
        "title": "Estrogen and the dentate gyrus: response to spatial and environmental novelty",
        "kicker": "STAR program · New York Medical College · with Dr. Jana Velíšková",
        "year": 2018,
        "summary": "Roughly 200,000 oophorectomies are performed in the United States each year, each one "
                   "producing surgical menopause and a sudden drop in estradiol; many of those women then take "
                   "estrogen therapy partly for cognition. Estrogen receptors are dense in the dentate gyrus, "
                   "the structure behind pattern separation, and in vitro work in the lab had shown estradiol "
                   "altering long-term potentiation there — but the behavioral consequence was open. Eighteen "
                   "ovariectomized rats received β-estradiol (2 µg/day for four days) or oil, then met an "
                   "environmental change (a new arena) and a metric change (objects moved from 30 to 50 cm). "
                   "Estradiol-replaced animals explored significantly less after the environmental change "
                   "(p = 0.028), consistent with estradiol shaping dentate-mediated learning. Written up for "
                   "the Junior Science and Humanities Symposium and presented as a poster — my first study, "
                   "run as a high-school student in the STAR program, and the first time I worked on what "
                   "estrogen does after it is taken away.",
        "thumb": "/earlier/thumbs/2018-estrogen-novelty-poster.jpg",
        "links": [{"label": "Paper (PDF, 20 pp)", "url": "/earlier/files/2018-estrogen-novelty-paper.pdf"},
                  {"label": "Poster (PDF)", "url": "/earlier/files/2018-estrogen-novelty-poster.pdf"}],
    },
]
