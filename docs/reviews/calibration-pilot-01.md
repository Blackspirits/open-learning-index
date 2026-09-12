# Deep Review Calibration Pilot 01 — 2026-09-12

## Purpose

This pilot calibrates Phase 3 scoring before Deep Review scales across the full survivor pool. It deliberately mixes fast-moving and stable subjects, F0/F1/F2 access, active and archival resources, hardware friction, non-English delivery, professional training and university courseware.

No record here is a final admission or ranking decision. Phase 4 head-to-head admission remains separate.

## Pilot set and scores

| Candidate | Quality | Recommendation | Main calibration signal |
|---|---:|---:|---|
| MIT 6.006 Introduction to Algorithms | 9.21 | 9.2 | Stable fundamentals can remain highly current despite archival age |
| MIT Missing Semester 2026 | 9.04 | 9.4 | Current, highly practical tooling path with exceptional time-to-value |
| Nordic nRF Connect SDK Fundamentals | 8.92 | 7.9 | Excellent teaching/practice, but required hardware materially lowers recommendation |
| fast.ai Practical Deep Learning | 8.88 | 7.9 | Excellent pedagogy and projects; 2022 flagship edition needs a real AI-currency penalty |
| WIPO DL-101 Intellectual Property | 8.80 | 9.1 | Authoritative, current, deep, assessed and free; session windows are modest friction |
| OpenLearn Teaching and learning tricky topics | 8.75 | 8.7 | Older publication date is tolerable for comparatively stable pedagogy |
| Cisco Data Analytics Essentials | 8.70 | 8.9 | Strong lab density and assessment make a professional beginner path competitive |
| Yale HIST 119 Civil War | 8.65 | 8.6 | Exceptional expertise/depth, weaker independent feedback and older historiography |
| NAU Saúde das Populações | 8.45 | 7.5 | High substantive quality and 2 ECTS, but current catalogue marks it archived |
| HubSpot Content Marketing | 8.42 | 8.4 | Strong professional utility, with provider-framing and project-depth limits |
| Saylor BUS205 Business Law | 8.40 | 8.0 | Recent maintenance helps, but US jurisdiction and limited authentic legal work matter |
| Microsoft Learn AI Concepts | 8.19 | 8.4 | Extremely current and accessible, but deliberately short and broad rather than deep |

Quality spread: **8.19–9.21**. Recommendation spread: **7.5–9.4**.

## Calibration findings

### 1. Quality and recommendation are meaningfully different

The strongest evidence is Nordic and NAU. Nordic scores highly on pedagogy, practice and currency but requires compatible physical hardware; NAU has substantial pt-PT academic value and 2 ECTS but is currently marked archived. Their recommendation scores therefore fall well below their intrinsic quality.

Conversely, Microsoft Learn AI Concepts has a lower Quality Score because its 3h51m path is intentionally broad and shallow, but its Recommendation Score is slightly higher because it is exceptionally current, free, low-friction and useful as a 2026 orientation path.

### 2. Currency must remain subject-sensitive

MIT 6.006 is from 2011 but its algorithms foundations are stable and its full problem/exam package remains excellent. It should not receive the same age penalty as a 2022 deep-learning/tooling course.

fast.ai remains one of the strongest pedagogical experiences in the pilot, yet a serious current index cannot ignore that the flagship Part 1 is explicitly the 2022 edition. The currency component therefore pulls its weighted Quality Score below otherwise comparable top-tier material.

### 3. Free credentials do not inflate quality

F0 status does not automatically improve component scores. HubSpot and Saylor both offer free credentials but remain around 8.4 quality because depth, practice type, provider framing and jurisdiction matter independently.

Likewise, MIT 6.006 and Missing Semester are F2 yet score at or above 9.0 because the educational experience itself is unusually strong.

### 4. Practice requires more than quizzes

The pilot distinguishes authentic doing from retrieval assessment. Nordic, Cisco, fast.ai and Missing Semester receive high Practice scores because learners build, debug, query, configure or ship things. WIPO and Saylor have meaningful assessments, but mostly knowledge checks and exams, so their Practice scores stay lower.

### 5. Archive status belongs primarily in recommendation/accessibility, not as an automatic quality collapse

Yale HIST 119 remains a deep, expertly taught course. NAU Saúde das Populações remains substantively strong. Their archival status affects access, learner completion and current recommendation more directly than core pedagogy/depth.

## Evidence-sensitive caveats

- NAU currently labels Saúde das Populações as archived; its learner-facing course page still documents quizzes, certificate mechanics and 2 ECTS, so the quality record is preserved while recommendation is penalized.
- WIPO DL-101 has active 2026 registration/course windows and repeated sessions, supporting high currency and a current completion route.
- Saylor BUS205 syllabus was last modified on 2 October 2025 and explicitly documents free enrollment, final exam and certificate; optional ACE credit requires a $5 proctored exam and is not treated as free academic credit.
- fast.ai remains fully accessible, but the public flagship Part 1 explicitly identifies itself as the 2022 course.

## Calibration decision

The rubric is **good enough to scale**, with three operational anchors to preserve consistency:

1. score `currency` by subject volatility, never by publication year alone;
2. score `practice` by authenticity and feedback value, not by the mere presence of quizzes;
3. use `recommendation_score` to express current learner friction, prerequisites, hardware, archive state, jurisdiction and realistic alternatives without contaminating intrinsic quality.

The pilot deliberately contains strong survivors, so the Quality Score range is narrower than the eventual full pool. This is acceptable. Recommendation Score already demonstrates enough separation to support later head-to-head comparison.

## Next gate

Scale Deep Review in category-aware batches, starting with fast-moving categories while the evidence is freshest. Preserve comparator evidence and do not publish final tiers until enough of each competitive field has been reviewed head-to-head.
