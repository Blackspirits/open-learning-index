# v0.2 Discovery Batch 4 — 2026-09-10

## Scope

Batch 4 adds **41 discovery candidates** and deliberately rebalances the research universe toward marketing and sales, business operations, finance/accounting, entrepreneurship, leadership, professional communication, history/humanities, creative industries and natural sciences.

After structural validation, the project reaches **164 discovery candidates** and **181 total researched learning experiences** including the 17 v0.1 reference fixtures.

Presence in this batch is not endorsement. No new candidate receives a Quality Score or Recommendation Score at discovery stage.

## Distribution

| Category | New candidates |
|---|---:|
| Marketing & Sales | 10 |
| Business & Entrepreneurship | 6 |
| Finance & Economics | 5 |
| History & Culture | 4 |
| Humanities & Philosophy | 3 |
| Writing & Communication | 4 |
| Arts & Design | 4 |
| Natural Sciences | 3 |
| Project, Product & Leadership | 2 |
| **Total** | **41** |

## Providers sampled

- HubSpot Academy
- Saylor University
- The Open University / OpenLearn
- MIT OpenCourseWare
- Open Yale Courses

## Strong discovery signals

- **HubSpot AEO Fundamentals** is a 2026-era candidate that targets answer-engine optimisation and AI-mediated search rather than relying on retired SEO material.
- **HubSpot Email Marketing**, **Revenue Operations** and **Inbound Sales** add practical, freely credentialled marketing and growth pathways.
- **Saylor BUS103, BUS203, BUS300 and BUS305** provide longer-form structured alternatives with assessments and free certificates in accounting, marketing, operations and entrepreneurship.
- **MIT 15.393 Nuts and Bolts of New Ventures** is a recent 2025 OpenCourseWare edition covering customer discovery, venture economics, finance, legal issues, operations and pitching.
- **MIT Finance Theory I** adds a rigorous finance benchmark with lectures, problem material and exams.
- **OpenLearn Effective communication in the workplace** provides a substantial badged communication pathway rather than a short awareness course.
- **OpenLearn Empires: power, resistance, legacies** is a comparatively recent history course with explicit source criticism and historiographical aims.
- **Yale CHEM 125a/125b** provide a coherent two-semester organic-chemistry sequence with problem sets and examinations.

## Integrity check and duplicate cleanup

The first CI run correctly rejected six proposed entries because they duplicated courses already present elsewhere in the discovery pool: HubSpot Content Marketing, Yale Political Philosophy, Yale Modern Poetry, OpenLearn Lottery of Birth, and the canonical URLs for Yale PHYS 200 and PHYS 201.

They were replaced rather than ignored by the validator:

- HubSpot Email Marketing Certification;
- OpenLearn What is politics?;
- OpenLearn Human rights and law;
- OpenLearn Empires: power, resistance, legacies;
- Yale Freshman Organic Chemistry I;
- Yale Freshman Organic Chemistry II.

This is evidence that cross-batch duplicate validation is doing useful work before publication.

## Evidence caveats

1. HubSpot certification access is currently described as free, but language availability differs by certification and must be recorded course-by-course during shallow review.
2. HubSpot's old SEO certification was retired in 2026; this batch intentionally uses the newer AEO Fundamentals course instead of treating retired SEO material as current.
3. OpenLearn courses generally provide a free statement of participation, and some provide a digital badge. The exact credential type must be normalised during shallow review instead of treating every OpenLearn reward as identical.
4. Several OpenLearn, MIT and Yale courses are older. Age alone is not a rejection criterion, but currency must be scored relative to subject volatility and compared with newer alternatives.
5. MIT OpenCourseWare and Open Yale Courses entries are classified F2 at discovery because the learning materials are open while formal completion credentials are not part of the free course experience.
6. Saylor pages currently advertise free certificates; course versions and any college-credit mechanisms must remain separate from the free-learning classification.
7. Yale ASTR 160 is pedagogically interesting but materially dated as a frontier-science course; deep review must distinguish timeless scientific reasoning from obsolete frontier claims.
8. `Human rights and law` is temporarily mapped to Humanities & Philosophy. The taxonomy should be audited before v1.0 because Law & Public Policy may deserve a first-class category.

## Next gate

Do not promote these entries directly into `data/courses.json`.

After this batch, discovery should continue toward 300–500 candidates, but the marginal-value rule becomes stricter: future batches should add either new provider diversity, under-covered categories, materially different learning paths, or plausible challengers to category leaders.

Batch 5 should prioritise cybersecurity/networking with stable direct URLs, current natural sciences outside the existing MIT/Yale concentration, statistics/data-science alternatives, law/public policy, education/teaching, high-quality language programmes, design/photography practice, and non-English original courses where language metadata can be verified precisely.
