# v0.2 Discovery Batch 5 — 2026-09-10

## Scope

Batch 5 adds **41 discovery candidates** and raises the admission bar: every entry either expands provider diversity, strengthens an under-covered field, adds a materially different learning path, or plausibly challenges an existing category leader.

The project now contains **205 discovery candidates** plus the **17 v0.1 reference fixtures**, for **222 researched learning experiences** in total.

Presence in this batch is not endorsement. No new candidate receives a Quality Score or Recommendation Score at discovery stage.

## Distribution

| Category | New candidates |
|---|---:|
| Cybersecurity & IT | 10 |
| AI & Data | 7 |
| Mathematics & Statistics | 2 |
| Law & Public Policy | 6 |
| Education & Teaching | 5 |
| Natural Sciences | 5 |
| Arts & Design | 3 |
| Languages | 3 |
| **Total** | **41** |

## Taxonomy improvement

Batch 5 introduces two first-class categories that were previously being forced into overly broad buckets:

- `law-public-policy` — **Law & Public Policy**
- `education-teaching` — **Education & Teaching**

`data/categories.json` is now treated as the authoritative category registry. The validator checks that both reference/approved courses and discovery candidates use registered category IDs, preventing the schema and dataset from silently drifting apart.

Existing older candidates are not automatically reclassified just because the new categories now exist. Semantic reclassification should be deliberate and auditable during shallow screening.

## Providers added or strengthened

- Cisco Networking Academy
- Fortinet Training Institute
- Kaggle Learn
- Harvard University
- MIT OpenCourseWare
- Saylor University
- WIPO Academy
- Council of Europe HELP Programme
- The Open University / OpenLearn
- British Council TeachingEnglish
- NASA Science
- Khan Academy / Pixar
- Figma
- Stanford / Marc Levoy public course materials
- The Japan Foundation — Minato
- TV5MONDE
- Deutsche Welle

## Strong discovery signals

- **Cisco Ethical Hacker** is unusually substantial for a free vendor course: current Cisco documentation describes roughly 70 hours, 34 labs, extensive interactive practice, a final exam, a skills-based assessment and a digital badge.
- **Cisco's networking/cybersecurity sequence** now gives the candidate universe a coherent practical ladder rather than isolated awareness courses.
- **Kaggle Intermediate Machine Learning, SQL, Pandas and Data Visualization** provide compact executable pathways with no-cost certificates and can be tested head-to-head against longer university material for practical value per hour.
- **Harvard Stat 110** and **MIT 18.650** give statistics/probability two rigorous academic challengers with extensive open materials.
- **WIPO DL-101** is a rare combination of specialist institutional authority, meaningful depth, free access and a free formal certificate; however, it runs in scheduled sessions.
- **Council of Europe HELP** exposes a large multilingual self-learning catalogue with public access and digital statements of accomplishment. Deep review must decide whether the umbrella catalogue belongs in the final index or should be replaced by selected individual HELP courses.
- **Take your teaching online** is a substantial Open University badged course rather than a short awareness resource.
- **British Council TeachingEnglish** provides current, free teacher-development courses with certificates, but several operate in annual/time-limited windows and therefore need faster maintenance cadence.
- **NASA Open Science 101** is a current public five-module scientific-practice course with a badge and certificate.
- **Figma Getting started in design** is explicitly built as a free self-paced design-fundamentals curriculum with practical exercises, not merely product documentation.
- **Marugoto A1-1** from the Japan Foundation offers 48 hours of integrated Japanese study with assignments and tests for free.
- **TV5MONDE Première classe** and **DW Nicos Weg** introduce large public-service language-learning experiences built around authentic audiovisual material and interactive exercises.

## Evidence and access caveats

1. `F0`, `F1` and `F2` remain **provisional discovery classifications** until shallow review checks the complete learner journey while logged in where necessary.
2. Cisco exposes multiple language/localisation routes. Do not infer `pt-PT` from a generic Portuguese label; individual variants must be verified explicitly.
3. Fortinet states that its self-paced learning content is free, while optional labs and certification products can be paid. `FortiGate Operator` is therefore conservatively F1 until the cost/status of its associated online exam and badge is confirmed.
4. WIPO DL-101 is free and certificate-bearing, but registration/course windows are scheduled. Availability must be modelled separately from permanent self-paced access.
5. WIPO IP Panorama 2.0 is explicitly free but currently lists no certificate; its final F1/F2 classification depends on the depth of meaningful assessment.
6. OpenLearn law courses are strong and badged but Scotland-specific and last updated around 2020; transferability and currency must be considered during deep review.
7. British Council courses can close enrolment even when the course remains listed. `Communicative tasks` requires rapid re-check because the current enrolment window closes in September 2026.
8. NASA Open Science 101 is cross-disciplinary scientific practice rather than a subject course; its best category should be revisited before v1.0.
9. Stanford CS 178 has excellent public lecture material but is explicitly not a current MOOC and retains obsolete Flash-era components. It is included as a discovery challenger, not a presumptive finalist.
10. The DW learning site is sometimes difficult for automated crawlers. Nicos Weg should receive a manual browser check during shallow screening rather than be rejected solely due to crawler behaviour.

## Negative evidence captured

Discovery also checked the widely recommended ISC2 Certified in Cybersecurity free-training route. The **One Million Certified in Cybersecurity** free-enrolment programme ended in May 2026, so it is **not** being added as a current genuinely-free candidate. This is exactly why the index must verify present-day access rather than repeat old recommendation lists.

## Next gate

The universe is now large enough that discovery quality matters more than raw count. Batch 6 should still expand coverage, but must strongly prefer providers and fields not yet adequately represented: public policy/government, education science, environmental science, economics/finance alternatives, medicine/public health, engineering/CAD, writing/journalism, non-English original courses and genuinely strong current AI/cyber challengers.

At roughly **260–300 total learning experiences**, run a formal coverage audit before deciding whether discovery should continue toward 400–500 or whether some categories have already reached saturation and can enter shallow screening early.
