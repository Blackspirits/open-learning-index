# Data Model

`data/courses.json` is canonical for approved/reference course records. Discovery intake lives in `data/candidates.json` and versioned files under `data/candidates/`. Shallow-review decisions live separately under `data/screening/`. `courses.csv` is generated.

## Core identity

- `id` — stable slug, never recycled.
- `title`, `provider`, `category`, `level`.
- `url` — canonical official learning URL when possible.

## Category registry

`data/categories.json` is the authoritative taxonomy registry. Every course and candidate `category` must reference one of its IDs; CI rejects unregistered categories.

Categories are allowed to evolve when discovery exposes a real information-architecture problem. New categories require an explicit taxonomy change rather than silently inventing strings inside course records. Existing records are reclassified deliberately during review so taxonomy migrations remain auditable.

## Languages

Approved/reference records currently use:

- `primary_language` — language of instruction.
- `other_languages` — alternate instructional versions or clearly identified supported variants.

Keep `pt-PT` and `pt-BR` distinct.

Shallow-screen records already use explicit `instruction_languages` and `subtitle_languages` arrays because review must not confuse translated subtitles with the language of instruction.

Before v1.0, the publication schema should also model interface language and original-language/translation provenance explicitly.

## Access

- `free_access` / `observed_free_access` — F0/F1/F2/F3 taxonomy.
- certificate or credential claims remain separate from learning access.
- academic credits remain separate from certificate/credential status.

A provider offering some free training does not prove that an associated exam, certificate, cloud resource, proprietary tool or required hardware is free.

## Discovery intake

Candidate batches are historical research intake. They contain the evidence and classification available when a resource was discovered.

They are intentionally not rewritten merely to reflect later review decisions. The legacy candidate `stage` field should therefore be interpreted as an intake snapshot until a future migration removes or redefines it.

## Shallow-screening ledger

`data/screening/*.json` is validated by `data/screening.schema.json`.

Each record identifies a candidate and records:

- `decision` — `advance`, `hold` or `reject`;
- evidence date and canonical URL;
- observed free-access tier;
- instruction and subtitle languages known at screening time;
- credential mechanics;
- completeness;
- evidence URLs and rationale;
- flags for unresolved risks.

At most one screening record for a candidate may have `is_current=true`. A later re-screen can supersede an earlier decision with `supersedes_screen_id`, preserving the old evidence rather than overwriting history.

## Scores

Final scoring does **not** happen during discovery or shallow screening.

For deep-reviewed approved/finalist records:

- `quality_components` — auditable component scores.
- `quality_score` — weighted result.
- `recommendation_score` — present-day editorial recommendation.

## Maintenance

- `last_verified` — latest evidence-based review.
- `review_interval_days` — risk-based cadence.
- `next_review` — expected re-verification date.
- `review_status` — review maturity/state.
- `status` — active, active_archive, retired or unavailable.

## Invariants

- IDs and canonical URLs must be unique across their relevant pools.
- Every category must exist in `data/categories.json`.
- Screening records may reference only known discovery candidates.
- Screening IDs are unique and a candidate may have at most one current shallow decision.
- Scores must remain inside 0–10.
- Quality Score must equal the weighted components within rounding tolerance.
- `next_review` must not precede `last_verified`.
- F3 courses are not eligible for the main published ranking.
