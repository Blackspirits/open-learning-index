# Phase 5 QA — primary-source re-verification 03

## Scope

Re-verify the complete **Health & Medicine** canonical set against current primary sources:

- WHO Good Practices for Clinical Trial Design and Implementation;
- TGHN ICH Good Clinical Practice E6(R3);
- TGHN Research Ethics Online Training V2;
- TGHN The Data Life Cycle: Practices and Policies;
- FAO Improving nutrition through agriculture and food systems.

This is a publication-currentness and metadata gate. Scores are reopened only if current evidence materially invalidates the scored learning experience.

## Result

**5 / 5 records retained.**

No Quality Score, Recommendation Score, category or language correction is required.

One material access correction is required:

- `whoacademy-good-practices-clinical-trials`: **F2_CONTENT_ONLY → F0_FULL_CREDENTIAL**;
- credential: **none → free_provider_certificate**.

The canonical set remains **129**.

## WHO — Good Practices for Clinical Trial Design and Implementation

WHO's May 2026 launch material confirms that the current course is free, online and self-paced. It consists of nine interactive modules, takes approximately 4.5 hours and applies the 2024 WHO Guidance for Best Practices for Clinical Trials through scientific and ethical principles and real-world decision-making.

During the original Deep Review, public primary evidence was sufficient for the course itself but not for the credential mechanics, so the record was conservatively classified F2.

That evidence gap is now resolved by first-party WHO material describing the same nine-module course: a WHO Science for Health presentation states that a **certificate of completion is awarded after completing all modules and passing a final assessment**. Although that presentation anticipated an earlier launch date, its course structure matches the course WHO subsequently launched in May 2026.

Primary evidence:

- https://www.who.int/news/item/05-05-2026-new-who-online-course-strengthens-good-practices-in-clinical-trials
- https://www.who.int/news-room/events/detail/2026/05/04/default-calendar/strengthening-trust-in-science--launch-of-who-good-practices-for-clinical-trial-design-and-implementation-course
- https://cdn.who.int/media/docs/default-source/immunization/pdvac/pdvac-2025/day-1/6.-relevance-of-the-clinical-trial-action-plan-to-vaccines.pdf?sfvrsn=8977b213_1
- https://whoacademy.org/coursewares/course-v1%3AWHOAcademy-Hosted%2BH0118EN%2BH0118EN_Q1_2025

Decision: retain admission and scores; correct access to `F0_FULL_CREDENTIAL` with a free provider completion certificate. The certificate correction improves access metadata but does not independently justify a score recalibration.

## TGHN — ICH Good Clinical Practice E6(R3)

The current first-party page verifies:

- eight modules / approximately 180 minutes;
- certificate after at least 80% in the final quiz;
- English, Spanish, French and Portuguese;
- full restructuring around the final ICH E6(R3) version published on 6 January 2025;
- current alignment with international GCP standards.

TGHN's FAQ separately confirms that its training and issued certificates are completely free.

Primary evidence:

- https://globalhealthtrainingcentre.tghn.org/ich-gcp-r3/
- https://globalhealthtrainingcentre.tghn.org/FAQ/

Decision: retain `F0_FULL_CREDENTIAL`, free provider certificate, existing languages and 90-day cadence.

## TGHN — Research Ethics Online Training V2

The current course remains a ten-module route, approximately 15–30 minutes per module. It explicitly provides quizzes and certificates at an 80% threshold and covers the same applied ethics path used in the Deep Review.

TGHN's FAQ confirms both free access and free certificates.

Primary evidence:

- https://globalhealthtrainingcentre.tghn.org/research-ethics-online-training-v2/
- https://globalhealthtrainingcentre.tghn.org/FAQ/

Decision: retain `F0_FULL_CREDENTIAL`, free provider certificate and 120-day cadence.

## TGHN — The Data Life Cycle: Practices and Policies

The current route remains an updated relaunch of the former Data Sharing course. Its published learning set still covers:

- principles and public-health value of data sharing;
- data management;
- ethics;
- governance, policy and access;
- data quality;
- costing;
- repositories.

The page says the course is still under development and that additional modules are planned. This is **not a newly discovered blocker**: the Phase 3 Deep Review explicitly recorded the `course-expanding` state and admitted the current published units as a research-data-governance foundation, not as full data-manager training.

The existing modules are independently usable, assessed and award electronic certificates at an 80% threshold. TGHN's FAQ confirms training and certificates are free.

Primary evidence:

- https://globalhealthtrainingcentre.tghn.org/data-sharing-v2/
- https://globalhealthtrainingcentre.tghn.org/FAQ/

Decision: retain admission, `F0_FULL_CREDENTIAL` and the existing caveat. Do not misrepresent it as a comprehensive data-management qualification.

## FAO — Improving nutrition through agriculture and food systems

The current FAO course page remains live and exposes five scenario-based lessons linking agriculture, food systems and nutrition-sensitive policy/programme design.

The current certification route requires completion plus a final exam with at least 75% and issues an FAO digital badge. FAO's current Academy documentation confirms that its e-learning initiatives/courses are free of charge and that digital badges are its verifiable learning credentials.

Primary evidence:

- https://elearning.fao.org/course/view.php?id=307
- https://elearning.fao.org/mod/page/view.php?id=5179&lang=en
- https://elearning.fao.org/mod/page/view.php?id=4534&lang=en
- https://www.fao.org/nutrition/policies-programmes/e-learning/en/

Decision: retain `F0_FULL_CREDENTIAL`, free badge and 120-day cadence. The existing currency score remains intentionally conservative; this gate verifies current availability and credential mechanics, not a redesign of the course content.

## Canonical changes

- WHO Good Practices: F2 → F0; `none` → `free_provider_certificate`; first-party credential evidence added.
- TGHN ICH GCP E6(R3): `last_verified` → 2026-09-13; TGHN free-certificate FAQ added as evidence.
- TGHN Research Ethics V2: `last_verified` → 2026-09-13; TGHN free-certificate FAQ added as evidence.
- TGHN Data Life Cycle: `last_verified` → 2026-09-13; TGHN free-certificate FAQ added as evidence.
- FAO nutrition/agri-food: `last_verified` → 2026-09-13; current Academy certification/free-access evidence added.

The Gate 2 access/credential distribution is reconciled accordingly:

- F0: **73**;
- F1: **24**;
- F2: **32**;
- free provider certificates: **44**;
- no formal free credential: **55**.

## Next gate

Continue Gate 3 with **Law & Public Policy**, prioritising courses whose usefulness depends on current law, human-rights frameworks, institutional rules or active course availability.

After law:

1. session/cohort-dependent routes;
2. remaining fragile vendor/version-dependent records;
3. final publication-readiness gate.

Broad discovery remains paused.
