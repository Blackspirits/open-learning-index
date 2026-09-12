# Deep Review Calibration Pilot 01 — 2026-09-12

## Purpose

This is the required mixed 12-candidate calibration gate before Deep Review scales across the full survivor pool. It deliberately mixes fast-moving and stable subjects, F0/F1/F2 access, active and archival resources, project-heavy and lecture-heavy learning, pt-PT delivery, hardware friction and provider-concentration cases.

One planned pilot candidate changed during current-route verification. `nau-saude-populacoes-futuro-sustentavel` is now surfaced by NAU as archived and no current enrolment/completion route was visible, so it was **not** deep-reviewed. It was replaced by the current `advance` candidate `nau-academia-empreendedorismo`, which preserves the pilot's pt-PT and academic-credit calibration role. The archived health candidate requires shallow re-screening separately.

## Pilot scores

| Candidate | Quality | Recommendation | Key calibration signal |
|---|---:|---:|---|
| `microsoft-learn-ai-concepts` | 8.01 | 8.3 | Very current but short and light on practice |
| `fastai-practical-deep-learning` | 8.95 | 8.4 | Excellent pedagogy/practice; 2022 practical stack penalizes recommendation |
| `cisco-data-analytics-essentials` | 8.59 | 8.8 | Labs, exams and portfolio lift practical value |
| `mit-6-006-algorithms` | 9.18 | 9.2 | Stable fundamentals remain exceptional despite old Python tooling |
| `mit-missing-semester-2026` | 9.01 | 9.4 | Current tooling + authentic practice produce highest recommendation |
| `nordic-nrf-connect-sdk-fundamentals` | 8.89 | 7.9 | Strong course quality, materially reduced recommendation by hardware friction |
| `nau-academia-empreendedorismo` | 8.04 | 8.2 | Strong pt-PT accessibility and 1 ECTS, moderate depth |
| `openlearn-teaching-learning-tricky-topics` | 8.43 | 8.0 | Practice-led pedagogy remains good; 2019 evidence base caps current recommendation |
| `saylor-bus205-business-law` | 8.31 | 8.2 | Refreshed structure is strong; US-jurisdiction specificity constrains portability |
| `wipo-dl101-intellectual-property` | 8.66 | 8.8 | 55-hour authoritative specialist path; scheduled cohorts add friction |
| `hubspot-content-marketing` | 8.39 | 8.5 | Current, free and assessed; provider concentration and limited project evidence remain caveats |
| `yale-hist-119-civil-war` | 8.52 | 8.3 | Exceptional lectures/expertise, weaker independent practice and older historiography |

## Distribution

- Quality Score range: **8.01–9.18**
- Quality Score mean: **8.58**
- Quality Score population standard deviation: **0.36**
- Recommendation Score range: **7.9–9.4**
- Recommendation Score mean: **8.50**

The spread is deliberately narrower than a discovery/shallow pool because these are all survivors, but it is sufficiently discriminative for head-to-head work. The scores do not collapse into provider prestige: Microsoft scores lower than several independent/open providers because the path is short and lightly practical; Nordic's recommendation drops sharply despite high instruction quality because hardware is mandatory; F2 MIT/Yale resources are not punished merely for lacking credentials.

## Calibration checks

### Evidence, not prestige

Pass. The highest Quality Score belongs to MIT 6.006 because of full-course depth, problem sets, exams, recitations and solutions — not simply because it is MIT. Microsoft Learn remains near the bottom of the pilot on Quality despite being current and professionally authoritative because it is under four hours and concept-heavy.

### Subject-sensitive currency

Pass. MIT 6.006 receives only a modest currency penalty because algorithms are stable; fast.ai receives a larger one because a 2022 framework/model ecosystem ages quickly; current 2026 Missing Semester receives full currency credit; 2019 OpenLearn pedagogy remains useful but is not treated as fully current.

### Credentials do not inflate pedagogy

Pass. F0 status helps access/recommendation mechanics but does not automatically raise pedagogy. NAU, Saylor, HubSpot and WIPO receive differentiated component scores based on actual design and depth.

### F2 is not penalized for lacking certificates

Pass. MIT 6.006 and Missing Semester score in the top group despite F2 access. Yale's lower recommendation is driven by weak structured practice and historiographic age, not lack of a certificate by itself.

### Accessibility captures real friction

Pass. Nordic's required development kit drives Accessibility to 6.0 and Recommendation to 7.9. WIPO loses some accessibility for cohort registration windows. Free browser-only paths score higher.

### Quality and recommendation remain distinct

Pass. The clearest divergences are Nordic (8.89 Quality / 7.9 Recommendation), fast.ai (8.95 / 8.4), Missing Semester (9.01 / 9.4), and Cisco Data Analytics (8.59 / 8.8).

### Weighted Quality Score recomputation

Pass pending repository CI. All scores were calculated with the fixed methodology weights: pedagogy 25%, depth 20%, practice 20%, materials 10%, currency 10%, expertise 10%, accessibility 5%.

## Calibration decision

**Provisional pass.** The rubric is producing explainable, subject-sensitive and meaningfully differentiated results. If repository validation confirms exact score recomputation and schema integrity, Deep Review can scale in category-aware batches.

Recommended scale-up order:

1. AI & Data + Computer Science & Software + Cybersecurity & IT — freshness first.
2. Health & Medicine + Psychology & Behaviour + Law & Public Policy + Finance & Economics — evidence/currency-sensitive domains.
3. Engineering & Electronics + Natural Sciences + Mathematics & Statistics.
4. Business, Marketing, Project/Product/Leadership, Education and Writing.
5. Languages, Arts/Design, History/Culture and Humanities/Philosophy with direct head-to-head clustering.

No candidate is admitted to the published index by this pilot. Phase 4 head-to-head admission remains separate.
