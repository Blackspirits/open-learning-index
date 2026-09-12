# Deep Review Protocol

## Purpose

Deep Review is Phase 3 of the Open Learning Index pipeline. It converts a shallow-screen survivor into an evidence-backed, comparable evaluation without yet admitting it to the published index.

Only candidates whose **current** shallow-screen decision is `advance` are eligible.

Deep-review records live in `data/reviews/*.json` and are validated against `data/deep-review.schema.json`.

## Evidence sequence

For each candidate, verify and record:

1. current canonical learner-facing route and free-access tier;
2. syllabus, scope and intended level;
3. teaching design and sequencing;
4. exercises, projects, labs or other practice;
5. learning materials and supporting resources;
6. prerequisites and required hardware/software/accounts/cloud spend;
7. currency relative to subject volatility;
8. instructor/provider expertise relevant to the subject;
9. certificate and academic-credit mechanics;
10. instruction and subtitle languages;
11. strongest direct alternatives among current candidates and reference fixtures.

Official provider/course sources are preferred. Supplementary independent evidence may inform learner experience, but it cannot be the sole proof of access, price, credential or academic-credit claims.

## Scoring

Use the weights defined in `docs/methodology.md` exactly:

| Component | Weight |
|---|---:|
| Pedagogy | 25% |
| Depth | 20% |
| Practice | 20% |
| Materials | 10% |
| Currency | 10% |
| Expertise | 10% |
| Accessibility | 5% |

`quality_score = Σ(component × weight)`

Every component score requires a corresponding `component_evidence` explanation. Provider prestige alone is never evidence for a high score.

### Quality vs recommendation

**Quality Score** asks how good the resource is on its own terms.

**Recommendation Score** asks how strongly a learner should choose it over realistic alternatives today. It may reflect prerequisites, time-to-value, friction, duplicated coverage, portability, current availability and the strength of direct substitutes.

A free credential may improve convenience or recommendation value, but it does not automatically increase pedagogy, depth or practice.

## Subject-sensitive currency

Currency must be judged against the field:

- archival mathematics, philosophy or foundational science may remain excellent for years;
- AI, software, cybersecurity, cloud, law, finance, health and fast-changing tools require stricter recency checks;
- a current wrapper around materially stale teaching content does not erase the underlying currency problem.

## Comparators

Each review should identify realistic direct alternatives whenever they exist.

Comparator IDs may reference:

- another discovery candidate; or
- an approved/reference record in `data/courses.json`.

Deep Review does **not** make the final admission decision. Phase 4 decides whether a reviewed candidate beats or materially complements incumbents serving the same learning need.

## Historical integrity

At most one deep-review record per candidate may have `is_current=true`.

A later review preserves the old record and points to it with `supersedes_review_id`. Historical evidence and score changes are never overwritten silently.

If a current learner-route check reveals that the course no longer satisfies the shallow gate, update the shallow-screen ledger first; a current deep review requires a current shallow decision of `advance`.

## Calibration pilot

Before scaling across the survivor pool, review a mixed 12-candidate pilot spanning:

- stable fundamentals and fast-moving technical content;
- F0, F1 and F2 access;
- active and archival resources;
- project/lab-heavy and lecture/content-heavy formats;
- at least one non-English course;
- at least one hardware/tooling-friction case;
- at least one near-duplicate or provider-concentration comparison.

The pilot is a calibration gate. Check that evidence quality is consistent, Quality Scores recompute exactly, Recommendation Scores remain distinct, and the score spread is discriminative enough for later head-to-head admission.

Do not publish a global Top 100–150 from the pilot.
