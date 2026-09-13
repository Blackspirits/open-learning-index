# Phase 5 QA — reference fixture reconciliation

## Purpose

Reconcile the **17 pre-existing canonical reference fixtures** against the now-complete Phase 4 admitted set before publication QA proceeds.

Phase 4 ended with:

- 199 / 199 current `advance` candidates decided;
- 112 `admit`;
- 87 `do_not_admit`;
- 129 records in `data/courses.json` = 112 Phase 4 admits + 17 pre-existing reference fixtures.

Reference status is not a permanent exemption from comparison. A fixture should remain canonical only if it still improves the publication set after the full admitted pool is known.

## Result

**17 / 17 reference fixtures retained.**

No fixture is retired in this gate.

This is not a blanket grandfathering decision. Every fixture was checked against the Phase 4 family in which it functions as an incumbent or comparator.

## Retained active/current fixtures

| Fixture | QA decision | Decisive reason |
|---|---|---|
| `harvard-cs50x` | retain | Still the strongest broad CS entry reference; Phase 4 additions complement rather than replace it |
| `harvard-cs50p` | retain | Strong Python-specific foundation; outcompetes weaker Python candidates |
| `harvard-cs50-ai` | retain | Deep project-based AI foundation; remains complementary to Google MLCC and newer agent routes |
| `harvard-cs50-sql` | retain | Strong database/SQL foundation; clearly outcompetes compact SQL microcourses |
| `helsinki-full-stack-open` | retain | Current high-depth full-stack incumbent; Odin full-stack path was not admitted against it |
| `helsinki-python-mooc-2026` | retain | Current long-form Python path with strong practice; remains distinct from CS50P |
| `portswigger-web-security-academy` | retain | Continuously updated, lab-dense web-security category leader |
| `google-ml-crash-course` | retain | Current interactive ML foundation; still a core AI/ML incumbent |
| `hubspot-digital-marketing` | retain | Broad digital-marketing anchor; later HubSpot admissions were restricted to distinct roles |
| `pmi-kickoff` | retain | Concise authoritative project-management entry point complementing deeper long-form PM study |
| `openai-agents-workflows` | retain | Low-friction practical agent/workflow route; complements the more technical Hugging Face Agents course |
| `kaggle-intro-machine-learning` | retain | Strong hosted-practice ML onboarding; adjacent Kaggle microcourses were pruned rather than duplicated |

## Retained stable archives

| Fixture | QA decision | Decisive reason |
|---|---|---|
| `mit-18-06sc-linear-algebra` | retain | Mathematics is stable and the archive remains an exceptional self-study linear-algebra package |
| `yale-game-theory` | retain | Core strategic concepts remain durable; no admitted course replaces the same game-theory learning need |
| `yale-death` | retain | Stable specialist philosophy role; Phase 4 humanities pass explicitly retained it |

## Retained archives with explicit currentness caveats

### `yale-introduction-psychology`

Retain as a **historical lecture reference**, not the default current psychology route.

Phase 4 admitted `saylor-psych101-introduction-psychology` as the safer current assessed foundation. Yale remains useful because its lecture pedagogy and conceptual exposition still add value, but users should not infer that its scientific framing is the most current available.

### `yale-financial-markets-2011`

Retain as an **archival finance reference**, not a modern all-in-one finance curriculum.

Phase 4 explicitly rejected the 2008 MIT Finance Theory archive for current-core use and documented that no current broad free finance-theory winner exists. The Yale fixture still adds substantial foundations in risk, behavioural finance, securities, insurance and banking, while its canonical description already warns that dated examples require current supplementation.

This fixture should be re-evaluated if a strong current broad free finance-theory course is found.

## QA conclusions

1. The 17 fixtures still add marginal value after full Phase 4 comparison.
2. None is silently grandfathered: each has a documented incumbent role.
3. Archive age is treated by domain:
   - stable mathematics/philosophy/game theory can tolerate age better;
   - psychology and finance require explicit caveats and stronger monitoring.
4. Retaining all 17 does **not** freeze them permanently. Monitoring or future targeted discovery may displace them.
5. The canonical count therefore remains **129** after Gate 1.

## Next gate

Run publication-quality QA across all 129 canonical records:

- provider concentration;
- category balance and remaining gaps;
- instruction-language concentration;
- access / credential integrity;
- link and availability checks;
- high-volatility currentness;
- review cadence and `next_review`;
- metadata consistency and CSV parity.

Broad discovery remains paused.
