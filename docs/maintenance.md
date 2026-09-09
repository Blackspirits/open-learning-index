# Maintenance & Re-verification Policy

A world-class course index cannot be static. Access models, certificates, editions, URLs and competitors change.

## Cadence

### Every push / pull request — automatic

- JSON syntax/schema validation;
- duplicate IDs and canonical URLs;
- score reproducibility;
- invalid review dates;
- stale-course report.

### Monthly — discovery scan

Search for:

- new university/open-course releases;
- major new editions of existing courses;
- strong specialist courses that could displace an incumbent;
- category gaps.

New discoveries enter a **candidate pool first**. No automatic promotion.

### Rolling re-verification

Use `review_interval_days` per course:

- **60–90 days:** AI, current software/web, cybersecurity, cloud, year-specific courses and rapidly changing platform training.
- **120–180 days:** active business, marketing, project-management and other moderately changing courses.
- **365 days:** stable foundational mathematics, philosophy, classical theory and maintained archival university lectures.

Each review checks at minimum: canonical URL, free-access tier, certificate/credit claims, language availability, course status, major syllabus changes and direct competitors.

### Annually — ranking calibration

- reconsider scoring weights;
- audit category balance and prestige bias;
- re-run head-to-head comparisons;
- review the global Top 100 and all category leaders;
- archive superseded or structurally inferior entries.

## Event-driven review

Review immediately when there is credible evidence of:

- pricing/paywall change;
- F0/F1/F2 → F3 downgrade;
- course retirement/replacement;
- major edition change;
- broken canonical URL;
- substantial learner-facing quality regression;
- a new competitor likely to outperform a current Top course.

## Staleness rules

- `today <= next_review`: current.
- up to 30 days overdue: stale warning.
- more than 30 days overdue: priority re-review.
- more than 2× `review_interval_days` since `last_verified`: temporarily ineligible for S/S+ presentation until verified again.

Staleness does **not** automatically lower Quality Score. It lowers confidence in the published claim.

## When a course becomes paid

Do not delete history.

1. Reclassify the access tier.
2. If only F3 remains, exclude it from the main free-course ranking.
3. Preserve the record/history so old releases and links remain auditable.
4. Search immediately for the best replacement in the same role/category.

## When a better course appears

Run a head-to-head review against the relevant incumbent using the same rubric. The newcomer enters only if it wins clearly or adds a materially different learning path.

This makes the project a **living index**, not a permanent hall of fame.
