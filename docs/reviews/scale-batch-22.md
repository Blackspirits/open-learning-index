# Deep Review scale batch 22 — Phase 3 closure

## Purpose

Close the final valid `advance` gap after the History & Culture batch and the Phase 3 maintenance reconciliation.

PR #59 removed three records from the active Deep Review queue for evidence-based reasons:

- `blender-fundamentals-45-lts` → `hold` because the official course is still under construction;
- `openlearn-introduction-music-theory` → `reject` because the live practice route retains obsolete Flash/Java instructions and is outcompeted by a stronger current theory/drill system;
- `whoacademy-chemical-hazards-part-2` → `hold` because repeated official-source verification still cannot expose enough granular pedagogy/practice evidence for an auditable score.

That leaves exactly one current `advance` without Deep Review: `whoacademy-good-practices-clinical-trials`.

## New evidence

Earlier Health batches deliberately deferred this WHO course because the public launch evidence did not expose enough internal structure.

WHO has since published a substantially richer primary description on 15 May 2026. It verifies:

- free, online and self-paced access;
- **nine interactive modules**;
- approximately **4.5 hours** of study;
- five universally applicable scientific and ethical principles;
- grounding in WHO's 2024 clinical-trials guidance;
- real-world decision-making and case studies;
- application across settings, disease areas and health systems;
- participant protection, ethical review, community engagement, operational feasibility and public-health relevance.

This is sufficient to score pedagogy, depth and practice without inventing assessment mechanics.

The WHO Academy learner route remains JavaScript-only to public retrieval, so the review remains conservative on Materials and Accessibility and does not claim a free credential.

## Review

| Candidate | Quality | Recommendation | Decisive signal |
|---|---:|---:|---|
| WHO Good Practices for Clinical Trial Design and Implementation | **8.91** | **9.2** | current 2026, nine interactive modules, real-world cases and direct grounding in WHO clinical-trials guidance |

### Calibration against TGHN ICH GCP E6(R3)

The two courses serve adjacent but different needs.

- **WHO Good Practices** is broader and principles-based. It emphasises trial quality, ethics, feasibility, public-health relevance and decision-making across nine modules.
- **TGHN ICH GCP E6(R3)** remains the stronger direct route for learners who specifically need current GCP R3 compliance training, multilingual access and a verified free certificate.

The WHO course therefore earns higher intrinsic Quality through broader applied pedagogy and 2026 primary evidence, while its Recommendation is only modestly above TGHN because the public learner route is less transparent and credential mechanics remain unverified.

## Phase 3 state

After this batch:

- discovery candidates: **290**
- current shallow decisions: **199 advance / 9 hold / 82 reject**
- current Deep Reviews: **199**
- current `advance` candidates without Deep Review: **0**
- Phase 3 coverage: **199 / 199 = 100%**

The nine current holds remain outside Deep Review by design until their specific blockers resolve. They do not count as unreviewed `advance` candidates.

## Gate decision

**Phase 3 is complete.**

This does not admit any candidate into `data/courses.json` and does not create a global ranking.

The next workstream is **Phase 4 — head-to-head admission**:

1. compare reviewed candidates against direct alternatives and current reference fixtures;
2. admit only candidates that beat or materially complement incumbents;
3. control near-duplicates and provider concentration;
4. preserve category coverage and language/access diversity without lowering quality;
5. update `data/courses.json` only through auditable admission decisions.

Global Top 100–150 publication remains downstream of Phase 4.
