# Data Model

`data/courses.json` is canonical. `courses.csv` is generated.

## Core identity

- `id` — stable slug, never recycled.
- `title`, `provider`, `category`, `level`.
- `url` — canonical official learning URL when possible.

## Languages

- `primary_language` — language of instruction.
- `other_languages` — alternate instructional versions or clearly identified supported variants. Keep `pt-PT` and `pt-BR` distinct.

Future versions may split audio, subtitles and interface language into dedicated arrays when evidence is sufficiently reliable.

## Access

- `free_access` — F0/F1/F2/F3 taxonomy.
- `certificate` — separate from free access.
- `academic_credits` — separate from certificate.

## Scores

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

- IDs and canonical URLs must be unique.
- Scores must remain inside 0–10.
- Quality Score must equal the weighted components within rounding tolerance.
- `next_review` must not precede `last_verified`.
- F3 courses are not eligible for the main published ranking.
