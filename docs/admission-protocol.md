# Phase 4 admission protocol

## Purpose

Phase 4 decides whether a Deep-Reviewed candidate improves the published Open Learning Index.

A high Quality Score or Recommendation Score is **not** an automatic admission. The decision is comparative: a candidate must beat or materially complement the strongest realistic alternatives serving the same learning need.

## Eligibility

Only a candidate with:

1. current shallow decision `advance`; and
2. a current valid Deep Review

may receive a current Phase 4 admission decision.

If current verification exposes an access, completeness or currency blocker, correct the shallow ledger first. Do not use Phase 4 to hide a maintenance problem.

## Decisions

- `admit` — the candidate materially improves the canonical published set and is promoted into `data/courses.json`.
- `do_not_admit` — the candidate remains a valid reviewed resource, but adds insufficient marginal value versus stronger or more useful alternatives.

There is deliberately no Phase 4 `hold`. Evidence/access blockers belong in shallow maintenance.

## Comparison unit

Do not compare all courses globally by score.

Define a **learning need** and compare:

- direct candidates serving that need;
- relevant approved/reference incumbents in `data/courses.json`;
- adjacent complements when overlap is material.

A comparison family may contain courses with different levels or formats when they compete for the same learner choice, but distinct specialist roles should not be collapsed merely to reduce count.

## Marginal-value test

An `admit` decision should satisfy at least one strong condition:

1. clearly better overall recommendation for the same learning need;
2. materially stronger pedagogy, depth or practice that changes the learner choice;
3. meaningfully newer/current coverage in a volatile field;
4. a distinct specialist role not already served well;
5. meaningful language or accessibility coverage without a substantial quality sacrifice;
6. a superior free-access/credential path that materially lowers learner friction.

Provider prestige, a small score edge, or a free certificate alone are not sufficient.

## Redundancy and provider concentration

Near-duplicates compete against each other.

Multiple courses from one provider may be admitted only when each serves a clearly distinct learning need or level. Provider concentration is a publication-quality risk, not a reason to distort Phase 3 scores.

## Incumbent relationships

Admission records explicitly distinguish:

- `displaced_course_ids` — canonical records the candidate should replace;
- `complements_course_ids` — incumbents the candidate adds meaningful value beside;
- `outcompeted_by_ids` — stronger alternatives explaining a `do_not_admit` decision.

Empty arrays are valid when the relationship is not applicable.

## Promotion integrity

Discovery records remain immutable historical intake.

When a candidate is admitted:

- its stable candidate ID becomes the canonical `data/courses.json` ID;
- the published score/components must match the current Deep Review;
- the published canonical URL must match the current Deep Review;
- the admission decision and course promotion happen in the same validated state.

This is the only permitted candidate/course ID overlap.

## Historical integrity

Admission records live in `data/admissions/*.json` and are validated against `data/admission.schema.json`.

At most one current admission decision may exist per candidate. A later decision preserves history with `supersedes_admission_id`.

## Calibration gate

Before category-scale admission, run a mixed calibration pass including:

- clear admit;
- high-scoring redundancy non-admit;
- provider-concentration case;
- archive/current trade-off;
- language/access diversity case;
- short specialist versus broad foundation.

Do not begin large-scale promotion until the calibration decisions survive CI and remain editorially coherent.
