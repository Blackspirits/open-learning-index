# Phase 5 Gate 3 — re-verification batch 05: session and version-fragile routes

Verified: 2026-09-13

## Scope

This batch closes the remaining publication-risk pass for canonical courses whose usefulness depends unusually strongly on a live session, a bounded enrolment window, or a still-evolving curriculum label.

It deliberately avoids duplicating records already re-verified in earlier Gate 3 batches, including Helsinki Python Programming MOOC 2026 and WIPO DL-101.

Canonical records checked:

- `blcu-umoocs-elementary-spoken-chinese`
- `minato-marugoto-a1-1-integrated`
- `freecodecamp-a2-english-developers`
- `freecodecamp-b1-english-developers`
- `british-council-how-adapt-resources`
- `british-council-helping-teachers-learn`

## Outcome

- **6 / 6 retained**.
- No publication blocker found.
- No score, category, access-tier or credential-type change is justified.
- The canonical set remains **129**.
- The current metadata remains defensible, but these records require tighter monitoring than stable archival or evergreen courses.

## BLCU / UMOOCs — live cohort confirmed

Primary course page:

- https://moocs.unipus.cn/course/7880

The official UMOOCs page currently lists the **15th run**, free of charge, from **24 August to 27 December 2026**.

Current first-party evidence still supports the published learning claims:

- 18-week run;
- 32 videos;
- 10 assessments/exams;
- 32 downloadable resources;
- weighted grading across tests, examinations, video completion and discussion;
- stated passing threshold of 60 points.

The canonical `F1_FULL_ASSESSMENTS` classification remains appropriate. No free formal credential is currently verified.

### Monitoring consequence

This course must **not** be treated as continuously available merely because the current run is active. Re-check before or immediately after **27 December 2026** and require evidence of a successor free run before carrying forward an `active` publication claim into 2027.

## Japan Foundation Minato — bounded learner window confirmed

Canonical page:

- https://minato-jf.jp/CourseDetail/Index/KC26_MGRS_A101_EN01

The current Minato route remains a free self-study A1 integrated course. Current first-party Minato course pages for the same 2026 Marugoto family explicitly state:

- application period: **Anytime**;
- attendance period: **6 months from course start**;
- course type: **Self-Study**;
- course fee: **Free**;
- expected study time for the integrated Katsudoo & Rikai route: **48 hours**;
- passing threshold: **60 points**, using progress, assignments and tests.

The six-month attendance limit is a learner-specific access window, not a cohort closure. `self_paced: true` therefore remains correct, but future QA must verify that the current-year course instance continues to accept registrations.

## freeCodeCamp English for Developers — certifications live, Beta caveat remains

Canonical routes:

- https://www.freecodecamp.org/learn/a2-english-for-developers
- https://www.freecodecamp.org/learn/b1-english-for-developers

Current first-party freeCodeCamp repository evidence continues to list both routes as free language certifications:

- **A2 English for Developers (Beta)**;
- **B1 English for Developers (Beta)**.

The curriculum structure still exposes both certification identifiers, including their certification routes, in the live open-source curriculum.

Primary source:

- https://github.com/freeCodeCamp/freeCodeCamp
- https://github.com/freeCodeCamp/freeCodeCamp/blob/main/curriculum/structure/curriculum.json

The existing canonical treatment is therefore still correct:

- full free credential route retained;
- Beta label retained as a maturity/currentness caveat;
- 90-day review cadence remains justified.

No downgrade is warranted: the Beta label signals active evolution, not incomplete access to the published route.

## British Council TeachingEnglish — fixed 2026–27 availability windows confirmed

### How to adapt resources

Primary sources:

- https://www.teachingenglish.org.uk/training/courses/teachingenglish-how-adapt-resources
- https://www.teachingenglish.org.uk/professional-development-for-teachers/training-courses

The course is currently open and free, with:

- course dates: **1 April 2026 – 31 March 2027**;
- enrolment available until **24 March 2027**;
- self-study modules available before course closure;
- certificate of achievement after successful completion;
- free workbook and supporting resources.

The canonical `F0_FULL_CREDENTIAL` classification remains correct.

### Helping teachers to learn

Primary sources:

- https://www.teachingenglish.org.uk/professional-development-for-teacher-educators/training-courses
- https://www.teachingenglish.org.uk/sites/teacheng/files/2025-04/Helping_teachers_to_learn_workbook_2025.pdf

The teacher-educator course is currently open, with:

- current run: **8 April 2026 – 31 March 2027**;
- enrolment available until **24 March 2027**;
- free self-study access;
- approximately 12 hours of structured learning;
- certificate of achievement after successful module completion.

The canonical `F0_FULL_CREDENTIAL` classification remains correct.

### Monitoring consequence

Both British Council records are self-paced **within a provider-defined availability window**. They should be re-checked before the March 2027 closure rather than assumed evergreen.

## Publication decision

All six records remain defensible for publication.

The material distinction for the public index is not removal but accurate interpretation of availability:

- **BLCU:** cohort/session dependent;
- **Minato:** anytime registration with a six-month learner-specific attendance window;
- **freeCodeCamp A2/B1:** continuously accessible but explicitly Beta/currently evolving;
- **British Council:** self-paced courses with fixed 2026–27 closing dates.

No score or access change is made solely to encode timing information already captured by provider evidence and review cadence.

## Gate 3 status

Earlier Gate 3 batches covered 28 targeted high-risk records. This batch adds **6** additional session/version-fragile records, bringing targeted Gate 3 coverage to **34 records**.

The remaining work is the Phase 5 final publication-readiness gate:

1. run the complete repository validators;
2. confirm generated CSV parity and no known blockers;
3. document final canonical count and provenance;
4. ensure the nine unresolved shallow `hold` records remain excluded from publication;
5. update README/status to publication-ready state;
6. close issue #82 only after all checks are green.
