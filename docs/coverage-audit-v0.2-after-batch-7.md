# Coverage & Saturation Audit — v0.2 after Batch 7

**Audit date:** 2026-09-10  
**Discovery candidates:** 286  
**Reference fixtures:** 17  
**Total researched learning experiences:** 303  
**Shallow-screened candidates:** 15

## Executive conclusion

Batch 7 closes the three largest numerical category gaps without proving that every category is geographically or pedagogically saturated.

The project should **not** return to broad 40-course harvesting. Shallow screening is now the primary workstream. Discovery becomes a smaller corrective track whose only job is to fill demonstrated blind spots or introduce credible challengers.

The evidence-based stopping target remains approximately **320–350 serious candidates**. At 286, one final targeted discovery wave of roughly **30–40 high-value candidates** is likely sufficient unless screening exposes a new structural gap.

## Candidate coverage by category

| Category | Candidates | Post-Batch-7 state |
|---|---:|---|
| AI & Data | 20 | Screen now; discovery only for exceptional new challengers |
| Arts & Design | 19 | Screen now; photography/practice-led gaps only |
| History & Culture | 19 | Numerical gap closed; screen while testing geographic diversity |
| Humanities & Philosophy | 19 | Numerical gap closed; screen while testing tradition/provider diversity |
| Finance & Economics | 19 | Numerical gap closed; screen with strict jurisdiction/currency checks |
| Languages | 18 | Screen now; continue only for high-quality original-language pathways |
| Natural Sciences | 16 | Screen now; selective current challengers only |
| Computer Science & Software | 15 | Strong field; screen now |
| Cybersecurity & IT | 14 | Screening already started; continue screening |
| Law & Public Policy | 14 | Screen now; jurisdictional diversity remains relevant |
| Mathematics & Statistics | 14 | Quality field now sufficient to screen; only elite challengers needed |
| Health & Medicine | 14 | Screen now with strongest currency threshold |
| Engineering & Electronics | 13 | Screen now; selective robotics/control/CAD gaps |
| Marketing & Sales | 12 | Screen now |
| Psychology & Behaviour | 12 | Screen now; aggressively reject outdated science |
| Writing & Communication | 12 | Screen now |
| Business & Entrepreneurship | 12 | Screen now |
| Project, Product & Leadership | 12 | Screen now |
| Education & Teaching | 12 | Screen now |
| **Total** | **286** | |

## What changed after Batch 7

### History & Culture

The category grows from 7 to 19 candidates. It now includes world-history, methodology, European and American history, comparative revolutions/industrialisation, music history and Egyptology. The numeric shortage is solved.

The remaining risk is **geographic concentration**. A final targeted pass should prefer excellent African, Asian, Latin American, Middle Eastern, Iberian or global-history sources rather than more Yale/OpenLearn variants.

### Finance & Economics

The category grows from 9 to 19 and now has microeconomics, macroeconomics, development economics, personal finance, public-policy microeconomics and economic-crisis material. The field is large enough for real head-to-head comparison.

The remaining risks are jurisdiction sensitivity and provider concentration. Practical finance courses must not receive timelessness assumptions that are acceptable for basic economic theory.

### Humanities & Philosophy

The category grows from 9 to 19, adding critical thinking, ethics, political philosophy, literary theory and academic religious studies. It is ready for screening.

A final targeted pass should favour traditions, regions and intellectual histories not already represented by a predominantly Western anglophone canon.

### Mathematics & Statistics

The category grows from 10 to 14. The additions are not filler: MIT probability/statistics, real analysis, complex analysis and number theory are serious challengers with substantial exercises or assessment material. Candidate volume is now sufficient because incumbent quality is unusually high.

### Computer Science & Software

The category grows from 11 to 15 with a current Missing Semester, Berkeley CS 61A/61C and a French Inria semantic-web MOOC. The remaining task is screening, especially public-route completeness for Berkeley.

## Screening signal

The first shallow tranche screened 15 candidates: **14 advance, 1 hold, 0 reject**.

This does **not** imply a 93% expected survival rate. The calibration tranche intentionally selected high-confidence Cisco, Kaggle and Fortinet candidates to validate the evidence model. Subsequent tranches must deliberately include ambiguous, redundant and weaker records and are expected to be much more selective.

The FortiGate Operator hold demonstrates that the gate is working: a strong course is not allowed to inherit an F0 claim merely because its provider offers some free training. Credential cost/eligibility must be explicit.

## Saturation decision

A category is now treated as **screening-ready** if it has enough plausible competitors to make eliminations meaningful, even if a final niche discovery pass remains open.

After Batch 7, **all 19 categories are screening-ready**.

This does not mean all 19 are fully saturated. The following cross-category blind spots remain worth a final targeted discovery pass:

1. high-quality original-language courses beyond English, especially `pt-PT`, French, Spanish, German and Japanese;
2. geographically broader History & Culture and Humanities sources;
3. current practical Finance/Accounting outside a small provider cluster;
4. selective modern Natural Sciences and Health resources where currency matters;
5. exceptional hands-on engineering, electronics, robotics, CAD/control or maker learning;
6. any newly discovered course that is a credible category-leader challenger rather than merely acceptable.

## Recommended final discovery wave

Target **30–40 candidates**, not 40 by default. Stop early if marginal-value discovery collapses.

Admission to this final discovery wave should require at least one of:

- fills a documented geographic/language/provider gap;
- introduces a materially different learning method;
- covers an important subfield absent from the pool;
- is recent enough to challenge a dated incumbent;
- has unusually strong free assessment, labs, projects, credential or academic-credit value;
- plausibly competes for the eventual top tier of its category.

Do not add near-duplicate courses simply to reach 320.

## Recommended screening pace

Shallow screening should now run in mixed-provider tranches of roughly **25–40 candidates**. Each tranche should contain both strong and questionable records to avoid calibration bias.

Suggested order:

1. AI & Data + Cybersecurity & IT
2. Marketing & Sales + Business & Entrepreneurship + Project/Product/Leadership
3. Psychology & Behaviour + Health & Medicine + Education & Teaching
4. Arts & Design + Languages + Writing & Communication
5. Natural Sciences + Engineering & Electronics + Mathematics & Statistics
6. History & Culture + Humanities & Philosophy + Finance & Economics + Law & Public Policy
7. Computer Science & Software final pass

Candidates marked `advance` become eligible for deep review; `hold` items require a specific evidence resolution; `reject` items stay in research history but leave the active finalist pool.

## Architecture decision

`data/screening/*.json` is the authoritative **decision ledger** for shallow review. Discovery batch records remain immutable research intake evidence. The latest record with `is_current=true` determines the current shallow-review outcome for a candidate.

This avoids rewriting historical discovery batches merely to update workflow status. The legacy `stage` field in candidate records should therefore be treated as the intake-stage snapshot until a later schema migration removes or redefines it.

## Decision

**Primary workstream:** shallow screening.  
**Secondary workstream:** one final targeted discovery wave toward roughly 320–350 serious candidates.  
**Do not begin global ranking yet.** Quality scoring starts only after shallow survivors have been verified deeply enough for fair head-to-head comparison.
