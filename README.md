# Open Learning Index

![Open Learning Index banner](assets/open-learning-index-banner.svg)

> A rigorously curated, continuously maintained index of exceptional free courses and open learning experiences.

**[Browse the public index](https://blackspirits.github.io/open-learning-index/)** · **[Português (Portugal)](https://blackspirits.github.io/open-learning-index/pt/)** · [Methodology](docs/methodology.md) · [Contributing](CONTRIBUTING.md)

[![Validate dataset](https://github.com/Blackspirits/open-learning-index/actions/workflows/validate.yml/badge.svg)](https://github.com/Blackspirits/open-learning-index/actions/workflows/validate.yml)
[![Deploy public index](https://github.com/Blackspirits/open-learning-index/actions/workflows/pages.yml/badge.svg)](https://github.com/Blackspirits/open-learning-index/actions/workflows/pages.yml)

## What this project does

The Open Learning Index answers a simple question that ordinary course lists usually do not:

**Which genuinely free learning resources are good enough to recommend today?**

Every published course is evaluated with evidence for:

- teaching quality and depth;
- exercises, projects and assessment;
- materials and learner autonomy;
- currentness and maintenance;
- expertise and credibility;
- accessibility, language and prerequisites;
- what is actually free;
- whether a stronger alternative already exists.

Institutional prestige alone is not enough. Old, incomplete, shallow or technically obsolete courses are penalised or excluded.

## Current publication

As of **2026-09-15**:

| Metric | Current state |
|---|---:|
| Canonical published courses | **142** |
| Primary-language pt-PT courses | **13** |
| F0 — full course + free credential | **75** |
| F1 — full assessed learning path | **24** |
| F2 — full teaching content | **43** |
| Current advances Deep-Reviewed | **216 / 216** |
| Current advances Phase-4 decided | **216 / 216** |
| Holds excluded pending evidence | **5** |

The public site is generated deterministically from the canonical repository data.  
**`data/courses.json` is the source of truth.**

## What “free” means

| Tier | Meaning | Main ranking |
|---|---|:---:|
| **F0** | Full learning path + free provider completion credential | ✅ |
| **F1** | Full learning path + meaningful free assessment/labs, but no free formal credential | ✅ |
| **F2** | Substantial complete teaching content, but no free formal completion path | ✅ |
| **F3** | Preview, trial or partial access only | ❌ |

The project does not treat “free to enrol” or “free trial” as equivalent to a genuinely free course.

## How a course gets into the index

```text
Discovery
   ↓
Shallow Screening
   ↓
Deep Review
   ↓
Head-to-head Admission
   ↓
QA & Publication
   ↓
Continuous Maintenance
```

### 1. Discovery

Serious candidates are collected without premature scoring.

### 2. Shallow Screening

Current access, completeness, language, assessment, credential mechanics, obvious currentness problems and redundancy are checked.

Allowed decisions are only `advance`, `hold` or `reject`.

### 3. Deep Review

Advanced candidates are scored on pedagogy, depth, practice, materials, currency, expertise and accessibility.

**Quality** and **Recommendation** are deliberately separate.

### 4. Head-to-head Admission

A course enters the canonical set only if it is clearly strong enough **and** either beats or materially complements the existing field.

A stronger English course does not automatically make a strong pt-PT alternative redundant when language is a genuine access barrier.

### 5. Continuous Maintenance

Published courses are re-verified on a risk-based schedule. Pricing changes, broken links, retirement, new editions, quality regressions and strong challengers can trigger immediate review.

## Explore the project

| Resource | Purpose |
|---|---|
| **[Public index](https://blackspirits.github.io/open-learning-index/)** | Homepage, discovery and editorial context |
| **[All courses](https://blackspirits.github.io/open-learning-index/courses/)** | Search, filter and rank all published courses |
| **[Categories](https://blackspirits.github.io/open-learning-index/categories/)** | Browse all 19 canonical learning areas |
| **[Índice em pt-PT](https://blackspirits.github.io/open-learning-index/pt/)** | European-Portuguese public interface |
| **[Categorias em pt-PT](https://blackspirits.github.io/open-learning-index/pt/categories/)** | Localised category discovery |
| [Methodology](docs/methodology.md) | Scoring model and free-access taxonomy |
| [Research protocol](docs/research-protocol.md) | Discovery and screening rules |
| [Deep Review protocol](docs/deep-review-protocol.md) | Evidence and scoring requirements |
| [Reference calibration](docs/qa-reference-calibration-v0.8.md) | Provenance and current calibration of pre-Phase-4 reference courses |
| [Admission protocol](docs/admission-protocol.md) | Comparative Phase-4 rules |
| [Maintenance policy](docs/maintenance.md) | Re-verification, challengers and retirement |
| [Data model](docs/data-model.md) | Canonical fields and invariants |
| [v0.10 public experience hardening](docs/v0.10-public-experience-hardening.md) | Current visual, accessibility, localisation and publication QA |
| [v0.8 hardening](docs/v0.8-hardening.md) | Earlier trust, discovery, accessibility and indexability QA |
| [v0.7 public experience](docs/v0.7-public-experience.md) | Original public-site architecture decision |
| [Architecture audit](AUDIT.md) | Project architecture decisions and risks |

### Audit trail

The full research history is intentionally public:

- [`data/candidates/`](data/candidates/) — immutable Discovery intake;
- [`data/screening/`](data/screening/) — Shallow Screening decisions;
- [`data/reviews/`](data/reviews/) — Deep Review evidence and scores for discovery candidates;
- [`data/reference-reviews.json`](data/reference-reviews.json) — structured calibration evidence for the 17 pre-Phase-4 reference courses;
- [`data/admissions/`](data/admissions/) — comparative admission decisions;
- [`docs/discovery/`](docs/discovery/) — Discovery notes;
- [`docs/screening/`](docs/screening/) — screening rationale;
- [`docs/reviews/`](docs/reviews/) — Deep Review reports;
- [`docs/admissions/`](docs/admissions/) — admission reports.

Nothing needs to be inferred from a hidden spreadsheet or private ranking process.

## Public site

The public experience is now in **v0.10**: a modern, responsive light/dark interface with English and European-Portuguese routes for the homepage, catalogue, course details and category discovery.

The site remains static and is generated from canonical JSON plus validated editorial ledgers, with no CMS, database, user accounts, analytics or frontend framework runtime. Canonical category pages and localized course routes are indexable, and the Pages deployment is gated on generated-site QA.

The pt-PT route localises the interface, taxonomy, course titles and displayed editorial text through a checked-in presentation dictionary. Canonical records and review ledgers remain unchanged. Course pages retain the original title, and original evidence is available through the English route and source links. Proper names such as Full Stack Open and KICKOFF are preserved.

Course artwork is served locally, with source attribution recorded in an asset manifest. Courses without suitable official artwork use a consistent editorial panel. See [editorial presentation](docs/editorial-presentation.md) for translation maintenance, artwork provenance and validation.

### Build locally

```bash
python -m pip install -r requirements-dev.txt
python scripts/build_public_site.py
python -m http.server 8000 --directory _site
```

Then open `http://localhost:8000`.

## Validation

Repository CI checks the canonical data, generated CSV parity, review freshness, deterministic public-site generation and the built site's internal routes, locale pairs, canonical URLs, sitemap coverage and required assets.

Useful local commands:

```bash
python scripts/validate.py
python scripts/generate_csv.py
python scripts/check_staleness.py
python scripts/build_public_site.py
python scripts/validate_public_site.py _site
```

Generated output is disposable. Do not edit `_site/` or `data/courses.csv` as independent sources of truth.

## Maintenance promise

The Open Learning Index is **not a frozen “Top 100” list**.

Typical review cadence:

- AI, software, cybersecurity and other fast-moving fields: **60–90 days**;
- active general courses: **120–180 days**;
- stable archival/fundamental courses: up to **365 days**;
- methodology/ranking recalibration: **annually**;
- challenger discovery: **targeted and recurring**, not quantity-driven.

A course that becomes paid-only, incomplete, stale or clearly inferior can leave the main ranking while remaining in the audit history.

## Project philosophy

- **Quality over quantity.**
- Evidence over prestige.
- Currentness matters more in fast-moving fields.
- Language accessibility matters when quality remains high.
- Uncertainty is recorded rather than guessed away.
- New courses should improve the index, not merely make it longer.
- The repository is the source of truth; the public site is a projection of it.

## Licensing

- Repository software (including scripts and site implementation): **MIT**
- Curated metadata and original editorial annotations: **CC BY 4.0**
- Third-party course materials, names, logos and trademarks remain subject to their respective owners and licences.

See **[LICENSING.md](LICENSING.md)** for the exact scope.
