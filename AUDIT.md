# Architecture & Content Audit

Current review: **2026-09-15**  
Original architecture decision: **2026-09-09 (v0.1)**

The original audit established the core decision that still governs the project: the Open Learning Index is a **GitHub-first, data-driven and continuously maintained publication**, not a static article or hand-edited Top 100.

This document now describes the current architecture rather than the superseded v0.1 release plan.

## Current decision

Keep the repository as the source of truth and keep the public experience as a deterministic projection of validated repository data.

The project should remain:

- evidence-first;
- auditable;
- static at publication time;
- explicit about uncertainty;
- strict about what “free” means;
- continuously maintained rather than periodically recreated from scratch.

## Canonical editorial flow

```text
Discovery candidate
      ↓
Shallow Screening
(advance / hold / reject)
      ↓
Deep Review
      ↓
Comparative Admission
      ↓
data/courses.json
      ↓
generated CSV + generated public site
      ↓
generated-site QA
      ↓
GitHub Pages
      ↓
continuous maintenance / challenger monitoring
```

Pre-pipeline reference courses retain their historical provenance. They use the dedicated reference-review ledger rather than fabricated candidate/screening/admission history.

## Source-of-truth hierarchy

1. **`data/courses.json`** — canonical published course set.
2. Current structured review/admission ledgers — evidence and comparative provenance for published candidates.
3. Historical screening/review/admission records — immutable audit trail.
4. Generated outputs such as `data/courses.csv` and `_site/` — disposable projections.

When generated outputs disagree with canonical data, canonical data wins.

## Current repository architecture

```text
open-learning-index/
├── README.md
├── AUDIT.md
├── CONTRIBUTING.md
├── LICENSE
├── LICENSE-DATA
├── LICENSING.md
├── assets/
│   └── project-created README artwork
├── data/
│   ├── courses.json
│   ├── courses.csv
│   ├── categories.json
│   ├── candidates.json / candidates/
│   ├── screening/
│   ├── reviews/
│   ├── reference-reviews.json
│   ├── admissions/
│   └── JSON schemas
├── docs/
│   ├── methodology.md
│   ├── research-protocol.md
│   ├── deep-review-protocol.md
│   ├── admission-protocol.md
│   ├── maintenance.md
│   ├── data-model.md
│   └── version / QA / batch audit trails
├── scripts/
│   ├── validate.py
│   ├── validate_public_site.py
│   ├── generate_csv.py
│   ├── check_staleness.py
│   └── build_public_site.py
├── site/
│   ├── static HTML/CSS/JS source
│   └── original public-site artwork
└── .github/workflows/
    ├── validate.yml
    └── pages.yml
```

## Publication invariants

The current implementation intentionally enforces the following:

- canonical course IDs and canonical URLs are unique;
- every course category must exist in the category registry;
- weighted Quality scores must reproduce from their components;
- current Deep Reviews require a current Shallow Screening decision of `advance`;
- current admissions require the current Deep Review;
- `admit` decisions must be reflected in the canonical course set;
- `do_not_admit` candidates must not leak into the canonical set;
- `reference_verified` courses require a current structured reference review;
- F3/partial-preview resources cannot leak into the public catalogue;
- EN and pt-PT public route pairs must exist where required;
- canonical URLs, hreflang links, internal routes and sitemap entries are checked on the built site;
- GitHub Pages deployment is blocked when generated-site QA fails.

## Free-access model

The project distinguishes:

- **F0** — complete learning path + free provider credential;
- **F1** — complete learning path + meaningful free assessment, but no free formal credential;
- **F2** — substantial complete teaching content, without a free formal completion path;
- **F3** — partial preview, trial or materially incomplete free access.

Only F0–F2 are publication-eligible.

“Free to enrol”, “free trial” and “audit available” are not treated as equivalent claims.

## Current public architecture

The v0.10 public experience is deliberately static and framework-free.

It includes:

- English and European-Portuguese homepage/catalogue routes;
- static EN and pt-PT course-detail pages;
- canonical EN and pt-PT category directories and category pages;
- light/dark themes;
- an original SVG icon system;
- static metadata, sitemap and canonical/hreflang output;
- a generated-site QA gate before Pages deployment.

There is no runtime CMS, database, account system, rating system, analytics dependency or frontend framework.

## Licensing boundary

The repository intentionally uses a split licensing model:

- software and site implementation: **MIT**;
- curated metadata, original editorial annotations and standalone project-created artwork: **CC BY 4.0**;
- third-party course content, names, logos, trademarks and provider materials: not relicensed.

See [LICENSING.md](LICENSING.md).

## Critical risks that remain

1. **Access drift** — a course can become paid, partially free or account-restricted without a major content change.
2. **Link and route decay** — providers can move or retire canonical course pages.
3. **Currentness drift** — fast-moving technical, legal and financial content can degrade quickly.
4. **Credential drift** — free badges, certificates and credit conditions can change independently of course content.
5. **Archive ambiguity** — archived teaching material may remain excellent but lose active support or reproducible assessment.
6. **Prestige bias** — famous providers can still receive excessive benefit of the doubt unless direct alternatives are compared.
7. **Language ambiguity** — instruction language, subtitles and UI language must not be conflated; pt-PT and pt-BR remain distinct.
8. **Third-party rights** — visual polish must not silently import unlicensed provider logos, artwork or screenshots.
9. **Publication regressions** — route/localisation/asset errors are now mitigated by generated-site QA, but live-device visual QA remains useful.
10. **Documentation drift** — architecture and process documentation must evolve with the repository rather than becoming historical fiction.

## Maintenance control point

The current maintenance tracker is **issue #91 — continuous maintenance and challenger monitoring**.

Maintenance should stay targeted:

- scheduled re-verification by risk and `next_review`;
- challenger scans for likely replacements, major new editions and documented gaps;
- no quota-driven broad discovery;
- small, evidence-backed PRs;
- no merge with known blockers.

## Non-goals unless evidence changes

Do not add complexity merely because the site can support it.

The current project does not need, by default:

- a CMS;
- a backend database;
- user accounts;
- public star ratings;
- provider dashboards;
- behavioural analytics;
- a large frontend framework;
- silent machine translation of editorial evidence;
- broad discovery intake when the maintenance pipeline is deliberately gated.

## Verdict

The original architecture decision remains sound.

The project has matured from a schema-and-dataset prototype into a validated editorial pipeline plus a static public publication, without abandoning the source-of-truth and auditability principles that justified the architecture in the first place.
