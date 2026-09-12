# Deep-review ledger

This directory stores auditable Phase 3 deep-review records for discovery candidates that currently passed shallow screening with `decision=advance`.

Deep-review records are **not** final publication records and do not by themselves admit a course to the public index. Phase 4 head-to-head admission remains separate.

Each JSON file is validated against `data/deep-review.schema.json`. Historical reviews are preserved: a later review can supersede an earlier record using `supersedes_review_id`, while at most one review per candidate may have `is_current=true`.

Scores must follow `docs/methodology.md` exactly. Each numeric component also requires explicit component-level evidence so the score is auditable rather than reputation-based.
