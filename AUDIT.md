# Architecture & Content Audit — v0.1

Date: 2026-09-09

## Decision

Proceed with a **GitHub-first, data-driven and continuously maintained** project. CSV is an export, not the source of truth.

### Canonical flow

`courses.json` → schema/score/staleness validation → generated `courses.csv` → generated README/site views

JSON is canonical because courses need arrays (languages, evidence), structured scoring, access models, review metadata and future history fields that CSV represents poorly.

## Critical risks

1. “Free” is ambiguous: full course, audit, preview, certificate and assessment access are different products.
2. Pricing and access can change without course content changing.
3. Prestige bias can substitute brand recognition for pedagogy.
4. Technology is over-represented in most public free-course lists.
5. Old ≠ bad and current ≠ good; currency must be subject-sensitive.
6. Comparing linear algebra, philosophy and marketing on one global axis is imperfect.
7. UI language, subtitles and instruction language are frequently conflated; pt-PT and pt-BR must stay distinct.
8. Link rot, geoblocking and enrolment restrictions can silently invalidate a recommendation.
9. The same course can appear on official sites and third-party platforms with different free-access rules.
10. Completion badges, verified certificates and academic credits are not equivalent.
11. A static Top 100 will decay. Maintenance must be part of the data model, not an afterthought.

## Architecture

```text
open-learning-index/
├── README.md
├── AUDIT.md
├── CONTRIBUTING.md
├── LICENSE
├── LICENSE-DATA
├── data/
│   ├── courses.json
│   ├── courses.csv
│   ├── course.schema.json
│   └── categories.json
├── docs/
│   ├── methodology.md
│   ├── research-protocol.md
│   ├── maintenance.md
│   └── data-model.md
├── scripts/
│   ├── validate.py
│   ├── generate_csv.py
│   └── check_staleness.py
└── .github/workflows/
    └── validate.yml
```

## Release strategy

- **v0.1:** architecture, methodology, maintenance policy and reference fixtures.
- **v0.2:** ≥300-candidate pool + shallow screening.
- **v0.3:** deep review of finalists; evidence/language/access audit.
- **v1.0:** ~100–150 approved resources, global Top 100 and category rankings.
- **v1.1+:** GitHub Pages/search UI, automated discovery aids and community review workflow.

## Acceptance gate before v0.2

- Every reference record validates against the schema.
- Scores are reproducible from components.
- No duplicate IDs or canonical URLs.
- F0/F1/F2/F3 cases are representable without editorial hacks.
- Language and credential fields survive JSON → CSV conversion.
- Every record has a risk-based review interval and next-review date.

## Verdict

**Audit-first approach approved.** The ranking should be treated as a maintained dataset, not a one-off article.
