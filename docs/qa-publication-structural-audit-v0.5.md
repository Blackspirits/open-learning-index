# Phase 5 QA — publication-quality structural audit

## Purpose

Audit the complete canonical set after Phase 4 and reference-fixture reconciliation for publication-level structural risks:

- category balance;
- provider concentration;
- language accessibility;
- free-access models;
- credential mix;
- review cadence and staleness.

This gate does **not** re-score courses and does not use quotas.

## Dataset entering the audit

- **129 canonical approved/reference courses**
- **112 Phase 4 admits**
- **17 reconciled reference fixtures**
- **19 represented categories**
- **0 overdue canonical reviews** as of 2026-09-13

## Category coverage

Canonical counts range from **3 to 11** per category.

Largest:
- Languages — 11
- Computer Science & Software — 10
- Humanities & Philosophy — 10
- Natural Sciences — 10
- Mathematics & Statistics — 9
- Finance & Economics — 9
- Arts & Design — 9

Smallest:
- Education & Teaching — 3
- Marketing & Sales — 4
- Business & Entrepreneurship — 4
- Engineering & Electronics — 4

### QA decision

**No category-count blocker.**

A smaller category is not automatically under-covered. Phase 4 deliberately rejected weaker or redundant survivors rather than filling a quota. All 19 categories retain multiple distinct learning roles.

Future targeted discovery is justified only if monitoring identifies a **material missing learning need**, not because a category has fewer records than another.

## Provider concentration

Largest providers across the full canonical set:

| Provider | Courses | Share |
|---|---:|---:|
| MIT OpenCourseWare | 14 | 10.9% |
| The Open University / OpenLearn | 14 | 10.9% |
| Open Yale Courses | 13 | 10.1% |
| Saylor University | 13 | 10.1% |
| Khan Academy | 6 | 4.7% |
| Cisco Networking Academy | 6 | 4.7% |

No single provider exceeds **10.9%** globally.

The top four providers together account for **54 / 129 = 41.9%** of the canonical set.

### Local concentration hotspots

Several categories remain visibly provider-heavy:

- MIT — 6 / 9 Mathematics & Statistics;
- Open Yale Courses — 5 / 10 Humanities & Philosophy and 4 / 10 Natural Sciences;
- Cisco — 5 / 7 Cybersecurity & IT;
- HubSpot — 3 / 4 Marketing & Sales;
- MathWorks — 3 / 4 Engineering & Electronics;
- Council of Europe HELP — 3 / 5 Law & Public Policy;
- TGHN — 3 / 5 Health & Medicine.

### QA decision

**No automatic provider-pruning correction.**

These clusters were explicitly tested during Phase 4 and retained only where courses serve distinct learning roles. Removing courses merely to make the provider distribution look more even would reduce learning coverage.

However, provider concentration is a publication-quality risk and should remain visible in future QA. New courses from already-dominant providers should continue to face a higher marginal-value bar.

## Language accessibility

Primary instruction language:

- English — **120 / 129 = 93.0%**
- French — 4
- European Portuguese — 2
- Arabic — 1
- German — 1
- Chinese — 1

Only **9 / 129** courses have a non-English primary instruction language.

Only **6** additional courses currently expose verified alternate instruction languages:

- Google Machine Learning Crash Course — pt-BR;
- Hugging Face Agents Course — fr;
- TGHN ICH GCP E6(R3) — es, fr, pt;
- Unity Junior Programmer — de, ja, fr, pt, zh, es, ru, ko;
- WIPO DL-101 General Course on Intellectual Property — fr, ar, ru, es;
- Council of Europe HELP Cybercrime and Electronic Evidence — ar, az, bg, cs, fr, hu, hy, ka, pt, ro, sk, es, tr, uk.

The Unity alternatives were added during Gate 3 batch 02. WIPO and HELP Cybercrime language metadata was corrected during Gate 3 batch 04 from current first-party catalog/training pages. For WIPO, customised Chinese/Portuguese regional variants are not merged into `other_languages` without equivalence evidence for the standard 55-hour route.

Across primary + verified alternate instruction languages, the canonical set exposes:

- English — 120 courses;
- French — 9;
- European Portuguese — 2;
- Brazilian Portuguese — 1;
- Arabic — 3;
- German — 2;
- Chinese — 2;
- Spanish — 4;
- generic Portuguese — 3;
- Japanese — 1;
- Russian — 2;
- Korean — 1;
- Azerbaijani — 1;
- Bulgarian — 1;
- Czech — 1;
- Hungarian — 1;
- Armenian — 1;
- Georgian — 1;
- Romanian — 1;
- Slovak — 1;
- Turkish — 1;
- Ukrainian — 1.

### QA decision

**Material publication limitation; not an automatic release blocker.**

The index is heavily English-centric.

This must not be hidden or solved by lowering the quality threshold. Instead:

1. disclose the concentration in publication documentation;
2. preserve existing high-quality non-English coverage;
3. allow targeted corrective discovery when a genuinely strong non-English course can fill a proven gap;
4. keep the already identified pt-PT AI/ML and legal-education gaps on the monitoring/research agenda.

The project should not claim multilingual completeness.

## Free-access profile

- F0 — full learning route + free credential: **73 / 129 = 56.6%**
- F1 — full learning route + assessments, no verified free credential: **24 / 129 = 18.6%**
- F2 — substantive educational content free, no full free assessment/credential path: **32 / 129 = 24.8%**

### QA decision

**Healthy access distribution.**

A credential is not required for admission, but every canonical record must continue to expose its educational core without mandatory payment.

Gate 3 batch 03 corrected WHO Good Practices for Clinical Trial Design and Implementation from F2 to F0 after first-party WHO evidence resolved the previously unverified completion-certificate mechanics. The F0/F1/F2 distinction remains essential in the publication surface.

## Credential profile

- no formal free credential — 55
- free provider certificate — 41
- free badge — 12
- free badge + statement — 8
- free statement of participation — 6
- free Statement of Accomplishment — 3
- other explicit credential models — 4

### QA decision

**No credential-distribution blocker.**

Credential availability remains metadata, not a substitute for teaching quality. Gate 3 batch 04 also corrects the three Council of Europe HELP self-learning credentials from the overly generic `free_provider_certificate` label to the provider’s exact electronic Statement of Accomplishment terminology.

## Review cadence

As of 2026-09-13:

- overdue — **0**
- due within 90 days — **38**
- due in 91–180 days — **64**
- due later — **27**

The earliest scheduled reviews include:

- Helsinki Python MOOC 2026 — 2026-11-08;
- OpenAI Agents & Workflows — 2026-11-08;
- Hugging Face Agents Course — 2026-11-12;
- multiple CS/AI/security references — 2026-12-08;
- several high-volatility admissions — 2026-12-11 / 2026-12-12.

### QA decision

**No staleness blocker.**

The cadence is appropriately shorter in fast-changing technical, legal, health and vendor-tooling domains.

## Structural QA outcome

No canonical record is removed by this gate.

The principal publication-level risk is **English-language concentration**, followed by provider concentration in several categories. Both are real and documented, but neither justifies deleting strong courses or admitting weaker alternatives.

The canonical set remains **129**.

## Next gate — targeted primary-source re-verification

Before publication readiness, re-verify the highest-risk canonical records against current primary sources, prioritising:

1. AI & Data;
2. Computer Science & Software;
3. Cybersecurity & IT;
4. Health & Medicine;
5. Law & Public Policy;
6. fast-changing vendor-tooling courses;
7. session/cohort-dependent courses.

The goal is to confirm current:
- free access;
- route completeness;
- credential mechanics;
- links;
- status/version;
- material curriculum currency.

Broad discovery remains paused.
