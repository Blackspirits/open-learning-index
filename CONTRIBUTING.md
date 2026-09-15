# Contributing

Contributions are welcome when they improve the quality, accuracy, auditability or usability of the Open Learning Index.

The repository is evidence-first. A famous provider, a high review score elsewhere, or a popular course is not enough on its own.

## Before you start

Read the relevant protocol before editing data:

- [Methodology](docs/methodology.md)
- [Research protocol](docs/research-protocol.md)
- [Deep Review protocol](docs/deep-review-protocol.md)
- [Admission protocol](docs/admission-protocol.md)
- [Maintenance policy](docs/maintenance.md)
- [Data model](docs/data-model.md)

For new courses, follow the existing pipeline rather than editing the canonical index directly:

```text
Discovery → Shallow Screening → Deep Review → Scoring/Ranking → QA → Publication → Monitoring
```

During Shallow Screening the only valid decisions are `advance`, `hold` and `reject`.

## Proposing a course

A proposal should include:

- canonical official URL;
- provider;
- primary instruction language and known subtitle/alternate languages;
- why it may materially improve the index;
- current free-access model (F0/F1/F2/F3);
- evidence for certificates or academic credit if claimed;
- prerequisites and required resources when material;
- closest strong alternatives considered.

Do not assign a final ranking at Discovery. New courses enter the candidate pool first.

## Reporting or correcting an existing course

Please report when a listed course:

- becomes paid or only partially free;
- changes certificate or credit conditions;
- is archived, retired, replaced or moved;
- changes language availability materially;
- receives a major new edition;
- develops significant learner-facing quality problems;
- has a broken or redirected canonical URL;
- is clearly outperformed by a serious new challenger.

Maintenance changes should use current primary evidence and preserve history. When a current screening, Deep Review or admission decision changes, use the repository's supersession fields instead of silently overwriting the old decision.

## Evidence rules

- Prefer the official course page, provider, institution, documentation or official repository.
- Use secondary sources only when primary evidence is insufficient, and say why.
- Verify current availability, access tier, language, status and version before making a claim.
- Distinguish clearly between free teaching content, free assessment, free credentials and paid verification.
- Do not infer missing facts from provider reputation or marketing language.
- Record uncertainty explicitly.
- Keep pt-PT and pt-BR distinct.
- Do not convert generic provider-labelled “Português” to pt-PT or pt-BR by inference. On a published record, bare `pt` is allowed only as a documented alternate with `language_notes`; primary Portuguese must be resolved before publication.
- Avoid affiliate, referral and tracking links.
- Do not copy provider marketing descriptions into editorial fields.

## Editorial and scoring rules

- Quality > quantity.
- Currentness has extra weight in fast-moving fields such as AI, software, cybersecurity, law, finance and digital tools.
- Old, abandoned, incomplete or technically obsolete material must be penalised.
- Quality and Recommendation are separate concepts.
- A new candidate is admitted only if it clearly beats or materially complements relevant incumbents.
- Do not lower the threshold merely to fill a category.
- Different target languages can represent genuinely different learner needs.

## Local validation

Use Python 3.12 or later.

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python scripts/generate_csv.py
git diff --exit-code -- data/courses.csv
python scripts/check_staleness.py
python scripts/build_public_site.py
python scripts/validate_public_site.py _site
```

For deterministic freshness testing:

```bash
python scripts/check_staleness.py --as-of YYYY-MM-DD
python scripts/check_staleness.py --enforce-priority --as-of YYYY-MM-DD
```

Do not edit `_site/` directly. It is generated output.

`data/courses.json` is canonical. If it changes, regenerate `data/courses.csv` with the existing script rather than treating the CSV as an independent source.

## Pull requests

Keep changes small and auditable.

A good PR should:

- explain the learner-facing or maintenance reason for the change;
- cite the primary evidence used;
- identify affected course IDs;
- preserve historical records when a decision is superseded;
- avoid unrelated formatting or refactors;
- pass the repository validator, deterministic site build and generated-site QA;
- call out unresolved uncertainty or blockers explicitly.

Do not merge known blockers merely to keep a batch moving.

## Site and design contributions

The public site is deliberately static and framework-free. Visual improvements are welcome when they preserve:

- accessibility and keyboard navigation;
- responsive behaviour;
- reduced-motion support;
- deterministic builds;
- static indexability;
- the canonical-data/source-of-truth model.

Do not add provider logos, course artwork or other third-party assets unless their reuse rights are verified. Prefer the project's original SVG icon and visual system when a neutral interface symbol is sufficient.

The pt-PT interface localises UI text. Canonical course titles, provider names and editorial evidence must not be silently machine-translated.

## Licensing of contributions

By contributing original material, you agree that it may be distributed under the licence applicable to that part of the repository:

- software contributions under MIT;
- curated metadata and original editorial annotations under CC BY 4.0.

Third-party content is not relicensed by this project. See [LICENSING.md](LICENSING.md).
