# Phase 4 admission ledger

This directory stores auditable head-to-head admission decisions.

Admission records do not duplicate Deep Review scoring evidence. They record the comparative decision: whether a current Deep-Reviewed `advance` candidate materially improves the canonical published index.

See `docs/admission-protocol.md` and `data/admission.schema.json`.

A current `admit` record must correspond to a canonical record in `data/courses.json`; a current `do_not_admit` record must not.
