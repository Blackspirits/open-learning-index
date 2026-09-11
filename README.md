# Open Learning Index

> A rigorously curated, continuously maintained index of the world's best genuinely free courses and open learning experiences.

**Status:** v0.2 — targeted discovery + shallow screening. **286 discovery candidates + 17 reference fixtures = 303 researched learning experiences.** **211 candidates have now been shallow-screened** across eight tranches; current reference records are calibration fixtures, not the final Top 100.

## Goal

Review a broad evidence-based candidate universe across technology, sciences, mathematics, business, finance, law and public policy, education, humanities, arts, psychology, history, languages and other fields, then publish only ~100–150 exceptional resources.

The original discovery target was **300–500 serious candidates**. After formal coverage audits, the project moved to a hybrid strategy: shallow screening is now the primary workstream while discovery continues only for documented gaps and credible category-leader challengers. The current evidence-based stopping target remains roughly **320–350 candidates**, with expansion toward 400–500 only if a later saturation audit still finds meaningful blind spots.

The project separates **absolute quality** from **recommendation**, records exactly what “free” means, tracks instruction/subtitle languages, and re-verifies courses on a risk-based schedule so the rankings do not become stale.

## Start here

- [`AUDIT.md`](AUDIT.md) — architecture decisions and risks.
- [`docs/methodology.md`](docs/methodology.md) — scoring and free-access taxonomy.
- [`docs/research-protocol.md`](docs/research-protocol.md) — candidate → approved workflow.
- [`docs/maintenance.md`](docs/maintenance.md) — discovery, re-verification and retirement policy.
- [`docs/data-model.md`](docs/data-model.md) — canonical fields and invariants.
- [`docs/coverage-audit-v0.2.md`](docs/coverage-audit-v0.2.md) — first formal saturation and coverage audit.
- [`docs/coverage-audit-v0.2-after-batch-7.md`](docs/coverage-audit-v0.2-after-batch-7.md) — second saturation audit after crossing 300 researched experiences.
- [`docs/screening/shallow-01.md`](docs/screening/shallow-01.md) — first shallow-screening calibration tranche.
- [`docs/screening/shallow-02.md`](docs/screening/shallow-02.md) — first deliberately selective mixed-provider screening tranche.
- [`docs/screening/shallow-03.md`](docs/screening/shallow-03.md) — currency-sensitive psychology, health and education screening tranche.
- [`docs/screening/shallow-04.md`](docs/screening/shallow-04.md) — arts/design, languages and communication screening tranche.
- [`docs/screening/shallow-05.md`](docs/screening/shallow-05.md) — natural sciences, engineering/electronics and mathematics/statistics screening tranche.
- [`docs/screening/shallow-06.md`](docs/screening/shallow-06.md) — history/culture, humanities/philosophy, finance/economics and law/public-policy screening tranche.
- [`docs/screening/shallow-07.md`](docs/screening/shallow-07.md) — computer science/software and AI/data screening tranche.
- [`docs/screening/shallow-08.md`](docs/screening/shallow-08.md) — history/culture, humanities/philosophy and project/product/leadership screening tranche.
- [`data/categories.json`](data/categories.json) — authoritative category registry.
- [`data/courses.json`](data/courses.json) — approved/reference canonical dataset.
- [`data/courses.csv`](data/courses.csv) — generated spreadsheet-friendly export.
- [`data/candidates/`](data/candidates/) — immutable discovery batches.
- [`data/screening/`](data/screening/) — evidence-backed shallow-screening decision ledger.

## Free access taxonomy

| Code | Meaning | Main ranking |
|---|---|---:|
| F0 | Full learning path + free completion credential | ✅ |
| F1 | Full path + meaningful free assessment/labs | ✅ |
| F2 | Substantive teaching content free; no free formal completion path | ✅ |
| F3 | Preview/trial/partial access only | ❌ |

## Review pipeline

1. **Discovery** — collect serious candidates without assigning final scores.
2. **Shallow screening** — verify access, completeness, evidence, languages, assessment/credential mechanics, obvious currency issues and redundancy.
3. **Deep review** — score teaching quality, depth, practice, materials, currency, expertise and accessibility with direct alternatives in view.
4. **Head-to-head admission** — a course enters only if it beats or materially complements the incumbent field.
5. **Publish and maintain** — global/category rankings plus scheduled re-verification.

Shallow decisions are `advance`, `hold` or `reject`. They are recorded separately from discovery intake so the full research history remains auditable.

## Maintenance promise

The index is **not a frozen “Top 100”**.

- Automated structural checks: every push/PR.
- Discovery scan for new candidates: monthly.
- Fast-moving courses (AI, software, cybersecurity, cloud): usually every 60–90 days.
- Active general courses: every 120–180 days.
- Stable archival/fundamental courses: up to 365 days.
- Full methodology and ranking recalibration: annually.
- Immediate review when a link breaks, pricing/free access changes, or credible evidence is reported.

A course that becomes F3-only is removed from the main ranking but kept in history. A course whose review is substantially overdue is flagged stale and can be temporarily excluded until re-verified.

## Data philosophy

`courses.json` is the source of truth for approved/reference records. Discovery batches are immutable research intake; `data/screening/` records review decisions. CSV and future README/site views are generated from canonical data. Never maintain the same facts independently in multiple formats.

## Licensing

Repository code/scripts: MIT. Curated metadata and original editorial annotations: CC BY 4.0. Course materials remain owned/licensed by their respective providers.
