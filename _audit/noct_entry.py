# -*- coding: utf-8 -*-
NOCTURIA = '''    {
        "slug": "nocturia-goals", "tab": "Nocturia Goals", "group": "current",
        "title": "What do patients with nocturia actually want treated?",
        "kicker": "EpiNP \\u00b7 US population-based cross-sectional survey \\u00b7 adults 30 and older",
        "status": "Manuscript V3 \\u00b7 abstract prepared for the 2027 AUA Annual Meeting",
        "summary": "Nocturia trials judge success by one number: voids per night. We asked 7,539 adults "
                   "what they would actually like treated. Fewer voids was the most common single answer "
                   "\\u2014 and a majority wanted something else.",
        "stats": [("7,539", "respondents"),
                  ("52.6%", "wanted something other than fewer voids"),
                  ("1", "void tolerated before seeking care"),
                  ("14.3%", "bothered enough to want treatment")],
        "tags": ["Nocturia", "Patient-reported outcomes", "Trial design", "EpiNP", "Endpoints"],
        "paper": {"pdf": "Maimo_Work/7_Nocturia/Henry - V3 - What Do Patients with Nocturia Want Treated_ Patient-Defined Goals and Tolerance Beyond Void Count.pdf",
                  "label": "Manuscript V3", "note": "With Oliver Menken."},
        "page": {"kind": "auto"},
        "hub": {
            "people": ["Oliver B. Menken", "Benjamin H. Parker", "Henry M. Blair",
                       "Isabel X. Guan", "Jeffrey P. Weiss, MD, PhD"],
            "lede": "Nocturia trials are built on a countable outcome: voids per night. It is easy to "
                    "measure and easy to compare, and it may not be the thing patients are trying to "
                    "change. A treatment that removes one void from three may or may not be a treatment "
                    "that changes a life. So we asked.",
            "status_detail": "Manuscript V3 complete; abstract prepared for the 2027 AUA Annual Meeting. "
                             "Secondary analysis of the EpiNP baseline survey "
                             "(<a href=\\'https://clinicaltrials.gov/study/NCT04125186\\'>NCT04125186</a>).",
            "sections": [
                {"id": "question", "title": "The question", "nav": "The question",
                 "blocks": [
                     {"prose": [
                         "Guidelines and trials characterise nocturia treatment success almost entirely "
                         "through two numbers: the change in mean nocturnal voids per night, and the "
                         "proportion of patients reaching a 50% reduction. No minimal clinically "
                         "important difference has ever been established empirically \\u2014 in its "
                         "absence, Cochrane reviewers adopted one fewer void per night as a working "
                         "threshold.",
                         "But bother does not rise linearly with void count. Patients with one nightly "
                         "episode can be meaningfully bothered, and the steepest rise in bother falls "
                         "across the second and third. A drop from four voids to three may be nothing "
                         "like a drop from two to one. And the count says nothing at all about which "
                         "part of the symptom \\u2014 the waking, the sleep, the urgency, the leakage "
                         "\\u2014 a patient most wants addressed."]},
                     {"callout": "How many nocturnal voids will patients tolerate before they want "
                                 "treatment, how much reduction has to happen before they would call a "
                                 "medication effective, and what do they want treated in the first "
                                 "place?"},
                 ]},
                {"id": "design", "title": "How it was done", "nav": "How it was done",
                 "blocks": [
                     {"prose":
                         "The Epidemiology of Nocturnal Polyuria study (EpiNP) is a US population-based "
                         "cross-sectional survey of community-dwelling adults aged 30 and over, recruited "
                         "to approximate the general population by age, sex and race. This is a secondary "
                         "analysis of its baseline web survey \\u2014 specifically the nocturia "
                         "treatment-preference and medication items \\u2014 and does not use the "
                         "three-day bladder diary component."},
                     {"h3": "What was asked"},
                     {"bullets": [
                         "<b>Desire for treatment.</b> Whether the respondent was bothered by nighttime "
                         "urination enough to want to reduce it. Yes or no.",
                         "<b>Tolerance threshold.</b> How many nighttime urinations they were willing to "
                         "live with without pursuing treatment.",
                         "<b>Primary treatment goal.</b> One of five mutually exclusive options: fewer "
                         "nighttime urinations, better sleep, less nighttime urgency, no nighttime "
                         "leakage, or other.",
                         "<b>Meaningful-improvement threshold.</b> How many fewer voids a night it would "
                         "take to recognise that a medication was working. Secondary endpoint.",
                     ]},
                     {"h3": "Cohort and analysis"},
                     {"prose":
                         "Of the 10,190 EpiNP baseline respondents, 7,539 had complete data on every core "
                         "preference variable and formed the primary complete-case cohort; records routed "
                         "past the preference items by skip logic, or carrying placeholder or "
                         "out-of-range values, were excluded before analysis. Counts are reported as "
                         "median [IQR] and proportions with Wilson score intervals. Goal distributions "
                         "were compared with Pearson chi-square tests, and two logistic models were "
                         "fitted \\u2014 one for wanting treatment, one for choosing a goal other than "
                         "fewer voids. Analyses were run and independently validated in SPSS."},
                 ]},
                {"id": "cohort", "title": "Who answered", "nav": "Who answered",
                 "tag": "Table 1",
                 "blocks": [
                     {"table": {
                         "head": ["Characteristic", "Value"],
                         "rows": [
                             ["Primary complete-case cohort, n", "7,539"],
                             ["Age, years \\u2014 median [IQR]", "57 [43\\u201366]"],
                             ["Male sex, n (%)", "3,480 (46.2%)"],
                             ["Female sex, n (%)", "4,059 (53.8%)"],
                             ["Nocturnal voids tolerated without treatment \\u2014 median [IQR]",
                              "1 [1\\u20132]"],
                             ["Wanted treatment or reduction, n (%; 95% CI)",
                              "1,081 (14.3%; 13.6\\u201315.2)"],
                             ["Secondary cohort with a valid meaningful-improvement answer, n", "1,082"],
                             ["Voids of reduction needed to perceive benefit \\u2014 median [IQR]",
                              "1 [0\\u20132]"],
                         ],
                         "note": "<b>Table 1.</b> Counts as median [interquartile range]; proportions "
                                 "with Wilson score 95% confidence intervals."}},
                     {"callout": "Most people were not asking for help. Only one in seven was bothered "
                                 "enough to want treatment at all, and the median respondent was "
                                 "prepared to live with one void a night. That is the backdrop against "
                                 "which a one-void reduction has to be judged."},
                 ]},
                {"id": "goals", "title": "What they want treated", "nav": "What they want",
                 "tag": "Table 2",
                 "blocks": [
                     {"prose":
                         "Fewer nighttime urinations was the most common single answer. It was also a "
                         "minority answer: 3,969 of 7,539 respondents \\u2014 52.6% \\u2014 named "
                         "something else as the thing they most wanted treated."},
                     {"table": {
                         "head": ["Primary treatment goal", "n / N", "% (95% CI)"],
                         "rows": [
                             ["Fewer nighttime urinations", "3,570 / 7,539", "47.4% (46.2\\u201348.5)"],
                             ["Better or improved sleep", "2,185 / 7,539", "29.0% (28.0\\u201330.0)"],
                             ["Less nighttime urgency", "1,003 / 7,539", "13.3% (12.6\\u201314.1)"],
                             ["No nighttime leakage", "511 / 7,539", "6.8% (6.2\\u20137.4)"],
                             ["Other", "270 / 7,539", "3.6% (3.2\\u20134.0)"],
                             {"cls": "up", "cells": ["<b>Any non-void-count goal, combined</b>",
                                                     "<b>3,969 / 7,539</b>",
                                                     "<b>52.6% (51.5\\u201353.8)</b>"]},
                         ],
                         "note": "<b>Table 2.</b> Wilson score 95% confidence intervals. The five goals "
                                 "were not chosen with equal frequency (chi-square goodness-of-fit, "
                                 "p &lt; 0.001)."}},
                     {"callout": "Sleep alone \\u2014 29.0% \\u2014 is chosen nearly twice as often as "
                                 "urgency and leakage combined. An endpoint that counts voids records "
                                 "none of it."},
                 ]},
                {"id": "threshold", "title": "What counts as better",
                 "nav": "What counts as better",
                 "blocks": [
                     {"prose":
                         "Among the 1,082 respondents who answered the secondary item, the median "
                         "reduction needed to recognise that a medication was working was one fewer void "
                         "per night [IQR 0\\u20132]. That is the one number in this study that agrees "
                         "with current practice: Cochrane\\u2019s working threshold of one void, adopted "
                         "for want of an empirical anchor, turns out to be roughly where patients put "
                         "it too."},
                     {"callout": "So the magnitude trials use is about right. What they measure is not."},
                 ]},
                {"id": "subgroups", "title": "Who wants what", "nav": "Who wants what",
                 "tag": "Table 3",
                 "blocks": [
                     {"table": {
                         "head": ["Comparison", "Goal emphasised", "Subgroup vs referent", "p"],
                         "rows": [
                             ["Female vs male", "Better or improved sleep", "31.1% vs 26.5%",
                              "&lt; 0.001"],
                             ["Female vs male", "Fewer nighttime urinations", "42.5% vs 53.0%",
                              "&lt; 0.001"],
                             ["Age &gt; 65 vs \\u2264 65 years", "Better or improved sleep",
                              "32.2% vs 27.8%", "&lt; 0.001"],
                             ["Overactive bladder vs none", "Less nighttime urgency", "20.5% vs 12.9%",
                              "&lt; 0.001"],
                         ],
                         "note": "<b>Table 3.</b> Proportion within each subgroup selecting the "
                                 "indicated goal; p values are Pearson chi-square tests of the overall "
                                 "goal distribution within each comparison. Exploratory and "
                                 "hypothesis-generating."}},
                     {"prose":
                         "Men chose void count; women chose sleep. Older respondents chose sleep more "
                         "often than younger ones. Respondents with overactive bladder chose urgency "
                         "relief at nearly twice the rate of those without. A single endpoint applied "
                         "across all of them measures each group\\u2019s priority with different "
                         "fidelity."},
                 ]},
                {"id": "models", "title": "What predicts each", "nav": "What predicts each",
                 "tag": "Tables 4\\u20135",
                 "blocks": [
                     {"h3": "Who wants treatment at all"},
                     {"table": {
                         "head": ["Predictor", "aOR", "95% CI", "p"],
                         "rows": [
                             {"cls": "up", "cells": ["Overactive bladder", "4.95",
                                                     "3.93\\u20136.22", "&lt; 0.001"]},
                             ["Insomnia or sleep difficulty", "1.68", "1.41\\u20132.00", "&lt; 0.001"],
                             ["Mobility limitation", "1.58", "1.30\\u20131.91", "&lt; 0.001"],
                             ["Diabetes", "1.40", "1.18\\u20131.67", "&lt; 0.001"],
                             ["Diuretic use", "1.38", "1.15\\u20131.66", "&lt; 0.001"],
                             ["Male sex", "1.24", "1.08\\u20131.43", "0.002"],
                             ["Age, per year", "0.99", "0.98\\u20130.99", "&lt; 0.001"],
                             ["Hypertension", "1.14", "0.97\\u20131.32", "0.102"],
                             ["Sleep apnea requiring CPAP or device", "1.05", "0.86\\u20131.29", "0.614"],
                             ["Heart disease or condition", "0.94", "0.74\\u20131.19", "0.617"],
                         ],
                         "note": "<b>Table 4.</b> Outcome: bothered enough to want treatment or "
                                 "reduction (1,081 events among 7,539). All predictors mutually "
                                 "adjusted."}},
                     {"h3": "Who wants something other than fewer voids"},
                     {"table": {
                         "head": ["Predictor", "aOR", "95% CI", "p"],
                         "rows": [
                             {"cls": "up", "cells": ["Overactive bladder", "1.30",
                                                     "1.04\\u20131.62", "0.023"]},
                             ["Insomnia or sleep difficulty", "1.29", "1.13\\u20131.48", "&lt; 0.001"],
                             ["Age, per year", "1.01", "1.00\\u20131.01", "0.002"],
                             ["Hypertension", "0.89", "0.81\\u20130.99", "0.038"],
                             {"cls": "down", "cells": ["Male sex", "0.67", "0.61\\u20130.73",
                                                       "&lt; 0.001"]},
                             ["Diuretic use", "1.12", "0.98\\u20131.29", "0.107"],
                             ["Heart disease or condition", "1.12", "0.94\\u20131.33", "0.197"],
                             ["Mobility limitation", "1.09", "0.94\\u20131.28", "0.260"],
                             ["Sleep apnea requiring CPAP or device", "1.07", "0.92\\u20131.25", "0.364"],
                             ["Diabetes", "1.01", "0.88\\u20131.15", "0.924"],
                         ],
                         "note": "<b>Table 5.</b> Outcome: selecting any goal other than fewer "
                                 "nighttime urinations (3,969 events among 7,539). All predictors "
                                 "mutually adjusted."}},
                     {"callout": "The two models point the same way. Overactive bladder and insomnia "
                                 "\\u2014 the phenotypes most likely to want treatment at all \\u2014 "
                                 "are also the ones most likely to want something other than a lower "
                                 "count. The patients a trial is most likely to enrol are the patients "
                                 "its endpoint serves worst."},
                 ]},
                {"id": "limitations", "title": "What this cannot tell you",
                 "nav": "Limitations",
                 "blocks": [
                     {"bullets": [
                         "Cross-sectional and self-reported throughout, including every comorbidity: "
                         "these are conditions respondents say they were diagnosed with, not chart "
                         "diagnoses.",
                         "Respondents came from an online research panel, so internet access and panel "
                         "membership are built into the sample even though recruitment targeted the "
                         "general population by age, sex and race.",
                         "A single most-important goal was forced from five fixed options. Someone who "
                         "wants both fewer voids and better sleep had to discard one.",
                         "The complete-case restriction drops 2,651 of 10,190 respondents. Those routed "
                         "past the preference items by skip logic are not missing at random.",
                         "The subgroup comparisons are exploratory and were not corrected for multiple "
                         "testing.",
                         "Preferences stated on a survey are not the same as choices made in a clinic "
                         "with a prescription in front of you.",
                     ]},
                 ]},
            ],
            "next": "If what patients want treated is not what trials measure, the argument follows for "
                    "a goal-attainment endpoint \\u2014 one that asks whether the outcome a patient "
                    "named actually improved \\u2014 reported alongside void count rather than instead "
                    "of it.",
            "sidefoot": "Oliver B. Menken \\u00b7 Henry M. Blair \\u00b7 Jeffrey P. Weiss, MD, PhD<br>"
                        "Department of Urology, SUNY Downstate Health Sciences University",
            "footnote": "Every number on this page is read from the V3 manuscript tables.",
        },
    },
'''
