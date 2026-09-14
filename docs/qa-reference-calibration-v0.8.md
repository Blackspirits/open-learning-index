# v0.8 reference-course calibration

Verified: 2026-09-14

## Purpose

Close v0.8 Gate 5 without rewriting project history.

The 17 `reference_verified` courses pre-date the candidate → Shallow Screening → Deep Review → Phase 4 path. Phase 5 v0.5 already reconciled all 17 individually against the admitted field and retained them only where they still added value.

The remaining gap was evidence depth and calibration comparability: the reference records had component scores under the same 25/20/20/10/10/10/5 weights, but did not expose the structured `component_evidence`, prerequisites/resources and recommendation rationale required of later candidates.

## Architecture decision

Do **not** create fake discovery candidates or fake shallow `advance` decisions.

Instead:

- `data/reference-reviews.json` stores the one-time reference calibration evidence;
- `data/reference-review.schema.json` validates the ledger;
- each current reference review preserves the prior component scores, Quality Score and Recommendation Score;
- current scores/components must match `data/courses.json`;
- every `reference_verified` canonical course must have exactly one current reference review;
- comparator IDs must resolve to a known candidate or canonical course;
- the public build projects the reference-review evidence onto course pages using the same learner-facing evidence surface as Deep Reviews;
- provenance remains explicit: these are reconciled pre-Phase-4 references, not retroactively promoted candidates.

This keeps the pipeline truthful while giving reference courses equivalent evidence depth.

## Result

- **17 / 17** reference courses received structured calibration evidence.
- **2 / 17** score sets were confirmed without change.
- **15 / 17** received evidence-backed recalibration.
- **0 / 17** were removed.
- Existing `review_status=reference_verified` is preserved.
- All 17 were re-verified on **2026-09-14** and their next-review dates were recomputed from the existing risk-based intervals.

The recalibration is deliberately asymmetric. It does not force scores into a target distribution; changes occur where the later rubric exposes an over-generous component, archival/currentness penalty, practice gap or recommendation distinction.

## Score changes

| Course | Quality | Recommendation | Decisive calibration reason |
|---|---:|---:|---|
| `harvard-cs50x` | 9.88 → 9.69 | 9.9 → 9.8 | Near-perfect legacy components normalized; role unchanged. |
| `harvard-cs50p` | 9.68 → 9.53 | 9.6 → 9.5 | Strong practice retained; depth/materials aligned to calibrated scale. |
| `harvard-cs50-ai` | 9.62 → 9.54 | 9.7 → 9.5 | Project strength retained; fast-moving AI currency/recommendation made more conservative. |
| `harvard-cs50-sql` | 9.58 → 9.47 | 9.6 → 9.5 | Database leader retained; legacy near-perfect components normalized. |
| `helsinki-full-stack-open` | 9.64 → 9.61 | 9.9 → 9.8 | Only minor normalization; still exceptional and current. |
| `helsinki-python-mooc-2026` | 9.67 → 9.61 | 9.7 → 9.7 | Recommendation confirmed; small component normalization. |
| `portswigger-web-security-academy` | 9.9 → 9.83 | 9.9 → 9.8 | Exceptional labs/currentness retained; non-practice perfect scores reduced. |
| `google-ml-crash-course` | 9.44 → 9.44 | 9.5 → 9.5 | Confirmed under current rubric. |
| `mit-18-06sc-linear-algebra` | 9.74 → 9.58 | 9.6 → 9.6 | Exceptional stable archive retained; perfect legacy components normalized. |
| `yale-game-theory` | 9.36 → 9.05 | 9.2 → 9 | Archive assessment/support receive less credit than original classroom design. |
| `yale-introduction-psychology` | 9 → 8.4 | 8.9 → 8.4 | Material 2007 currency risk and weak replicability of original assessment; Saylor remains current default. |
| `yale-death` | 9.06 → 8.77 | 9 → 8.8 | Stable philosophy remains strong; public archive lacks original feedback/practice environment. |
| `yale-financial-markets-2011` | 9.05 → 8.61 | 8.8 → 8.4 | 2011 institutional/regulatory examples require current supplementation. |
| `hubspot-digital-marketing` | 8.95 → 8.62 | 9.2 → 9 | Compact breadth is valuable, but depth/project practice were previously generous. |
| `pmi-kickoff` | 8.91 → 8.65 | 9 → 9 | Quality reflects sub-hour depth; recommendation stays high for its narrow onboarding role. |
| `openai-agents-workflows` | 9.09 → 9.09 | 9.4 → 9.4 | Confirmed under current rubric. |
| `kaggle-intro-machine-learning` | 9.02 → 8.83 | 9.2 → 9 | Excellent practice/onboarding, but three-hour scope limits depth and breadth. |

## Interpretation

### Current technical leaders remain leaders

PortSwigger, CS50, Helsinki and MIT Linear Algebra remain exceptional. The main correction is removal of legacy clusters of 10.0/near-10 component scores where the later Phase 3/4 calibration uses more discriminating evidence.

### Archive age is domain-sensitive

Age is not penalised mechanically:

- MIT Linear Algebra remains extremely strong because undergraduate linear algebra is stable and the self-study package is unusually complete.
- Yale Death remains strong because the philosophical content is durable.
- Yale Psychology receives the largest reduction because empirical psychology has materially changed since 2007 and the public archive does not reproduce the original assessed classroom environment.
- Yale Financial Markets receives a stronger currency penalty because regulation, institutions, products and examples have changed materially since 2011.

### Recommendation remains distinct from Quality

PMI KICKOFF is the clearest example: its intrinsic depth is limited by design, but its Recommendation stays at **9.0** because it is an unusually low-friction, authoritative starting point.

Likewise, the archival Yale courses can remain useful while scoring below stronger present-day defaults for the same broad learning need.

## Evidence chain

This gate builds on, rather than replaces:

- `docs/qa-reference-reconciliation-v0.5.md` — 17/17 incumbent reconciliation;
- `docs/qa-reverification-01-technical-references.md` — current primary-source re-verification of ten volatile technical references;
- current official course/provider pages stored in each reference-review record.

Historical scores are preserved inside each v0.8 calibration record as `prior_quality_components`, `prior_quality_score` and `prior_recommendation_score`.

## Gate result

Reference provenance is now explicit, structurally validated and learner-facing.

The 17 records are directly comparable to later admissions at the evidence/scoring layer without pretending that they passed through a pipeline that did not exist when they entered the canonical set.

Next gate: final v0.8 QA against the remaining reproduced medium/low audit findings and a green repository CI run.
