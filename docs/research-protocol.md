# Research Protocol

## Objective

Build a candidate universe broad enough that the final Top 100–150 is the result of comparison, not memory, brand familiarity or an arbitrary number of links.

## Phase 1 — Discovery

Discovery began with a broad target of **300–500 candidates** across all categories, using major universities, open-course initiatives, public institutions, specialist academies and high-quality industry training.

Coverage audits changed the operational target: the project now aims for roughly **320–350 serious candidates** unless evidence shows meaningful blind spots remain. Expansion toward 400–500 is permitted only when it increases competitive coverage rather than catalogue volume.

Discovery is intentionally permissive. Inclusion in the candidate pool is not endorsement, and discovery records remain immutable research-intake evidence.

## Phase 2 — Shallow screen

Shallow screening is an evidence gate, not a quality-scoring exercise. Do **not** assign final 0–10 Quality or Recommendation scores here.

Verify at minimum:

1. current canonical learner-facing URL;
2. actual current free-access tier through the complete learner journey;
3. instructional completeness;
4. meaningful assessment, labs or projects when claimed;
5. credential mechanics and whether any exam/certificate is genuinely free;
6. instruction languages and known subtitle languages without conflating the two;
7. prerequisites and required hardware/software/cloud spend;
8. obvious currency problems relative to subject volatility;
9. redundancy against clearly stronger candidates;
10. strength and recency of evidence.

### Decisions

- `advance` — survives the shallow gate and becomes eligible for deep review;
- `hold` — potentially strong, but a specific unresolved evidence/access issue blocks advancement;
- `reject` — fails an exclusion criterion or is clearly redundant/inferior enough that deep review would be wasteful.

Typical shallow rejects include:

- F3-only access;
- dead or abandoned course without a substantively usable archive;
- poor instructional completeness;
- duplicated mirror when an official source exists;
- unsupported claims about free certification, credits or full access;
- narrow product marketing presented as education;
- materially obsolete content in a fast-moving subject;
- near-duplicate pathway material that adds no plausible value over a stronger sibling candidate.

### Decision ledger

Shallow-screening evidence lives in `data/screening/*.json` and is validated against `data/screening.schema.json`.

Discovery rows are not rewritten merely to record review outcomes. The current shallow status is the screening record for that candidate where `is_current=true`. A later re-screen creates a new record and can point to the previous record with `supersedes_screen_id`.

This keeps discovery history and review history independently auditable.

## Phase 3 — Deep review

Only `advance` candidates receive expensive deep review. Verify and compare:

1. syllabus and scope;
2. teaching quality and pedagogical design;
3. exercises, projects and labs;
4. depth relative to the intended level;
5. prerequisites and learner accessibility;
6. currency relative to subject volatility;
7. instructor/provider expertise;
8. access model and hidden paywalls;
9. certificate and academic-credit claims;
10. instruction, subtitle and interface languages;
11. strongest direct alternatives and incumbent category leaders.

Deep review is where auditable component scores can be assigned. Scores should represent evidence, not provider reputation alone.

## Phase 4 — Head-to-head admission

A new course does not enter simply because it is good. It should beat or materially complement the weakest incumbent serving the same learning need.

Near-duplicate courses from one provider compete against each other. Provider prestige never guarantees multiple final-list slots.

## Phase 5 — Publish

Publish global and category rankings only after coverage saturation and deep-review comparison are credible: repeated targeted discovery should stop producing plausible category-leader challengers at a meaningful rate, and the active survivor pool should be sufficiently reviewed for fair ranking.

## Parallel workflow during v0.2

After Batch 6, the project intentionally stopped treating discovery and screening as sequential global phases.

- **Primary workstream:** shallow screening of the existing pool.
- **Secondary workstream:** targeted discovery for documented language, geography, provider or subfield gaps.
- **Gate:** no global ranking until the survivor set is deep-review ready.

This hybrid workflow reduces research waste: weak candidates can be eliminated while the remaining discovery gaps are still being closed.

## Research log

Every screening and deep review records the date and evidence URLs. Important access, decision or score changes must be explainable from a commit, screening record or review note.
