# Discovery Batch 03 — 2026-09-09

Discovery records are research candidates, **not endorsements or final rankings**. No Quality Score or Recommendation Score is assigned until the evidence required by the deep-review protocol exists.

## Scope

Added **41 candidates**, taking the discovery pool from 82 to **123 candidates**. Together with the 17 v0.1 reference fixtures, the current research universe contains **140 unique learning experiences**.

This batch deliberately targets practical engineering, current health/research training, creative learning, languages and psychology rather than harvesting more generic computer-science MOOCs.

## Category distribution

| Category | New candidates |
|---|---:|
| Engineering & Electronics | 10 |
| Health & Medicine | 10 |
| Languages | 8 |
| Arts & Design | 7 |
| Psychology & Behaviour | 3 |
| AI & Data | 2 |
| Mathematics & Statistics | 1 |
| All other categories | 0 |

## Providers sampled

- Nordic Developer Academy
- MathWorks
- Ableton
- musictheory.net
- Blender Studio
- The Open University / OpenLearn
- Canva Design School
- Language Transfer
- Global Health Training Centre / The Global Health Network
- WHO Academy

## Strong discovery signals

### Embedded systems and engineering

Nordic Developer Academy is a particularly strong discovery source: its courses combine protocol/firmware theory, hardware exercises, lesson quizzes and completion certificates. `nRF Connect SDK Fundamentals` reaches beyond vendor-button-clicking into Zephyr RTOS, devicetree, Kconfig, GPIO/UART/I2C and concurrency. The main caveat is that the **course is free while compatible development hardware is not**; the final index must distinguish access cost from optional/required equipment cost.

MathWorks' Onramp model is also unusually strong for free vendor training. MathWorks explicitly states that **Onramp courses are free for everyone**, do not require a paid Online Training Suite subscription, do not expire, provide browser access, assessments/feedback and course certificates. This batch samples MATLAB, Simulink, Stateflow, machine learning, deep learning, image processing, optimisation and signal processing rather than treating the whole platform as one course.

### Creative practice

`Blender Fundamentals 4.5 LTS` is a current official curriculum with a large fully free sequence covering first steps, modelling, sculpting, UV unwrapping, rigging, animation, materials, lighting/rendering, compositing and video editing, plus mini assignments.

Ableton's `Learning Music` is a strong example of interactive pedagogy: no prior experience or equipment is required and learners make beats, scales, chords, basslines and melodies directly in the browser. `Learning Synths` is retained as a candidate but needs JavaScript-dependent shallow verification.

Canva Design School now offers free certification courses. `Canva essentials` was updated in June 2026 and includes activities plus a 19-question certification test; `Graphic design essentials` covers transferable design principles as well as Canva-specific implementation.

### Languages

Language Transfer adds a qualitatively different teaching model to the pool: guided reasoning and transfer between known and target-language structures rather than vocabulary drills. Complete Spanish, Greek and Swahili are especially interesting. Intro French, Italian, Turkish and Arabic are complete *introductory* products but have narrower scope, which must affect comparison against full language curricula.

`Complete German` is intentionally included as a likely negative-control candidate: the provider explicitly states that the course remains unfinished. It is marked F3 and should probably fail shallow screening unless its status changes. Keeping transparent near-misses in the research pool helps demonstrate that discovery is not equivalent to endorsement.

### Health and research practice

The Global Health Training Centre supplies unusually practical, peer-reviewed and freely certified training in clinical research, ICH GCP E6(R3), research ethics, clinical data management, data lifecycle practice and clinical laboratory quality. The 2025-aligned ICH E6(R3) course is particularly current.

WHO Academy contributes a newly launched 2026 clinical-trial best-practices course, One Health training and the chemical-hazards sequence. WHO confirms that these learning experiences are free, but the Academy application is JavaScript-dependent, so assessment and credential mechanics are conservatively left at F2 until verified interactively.

### Psychology

`Psychology around the world` was first published in 2025 and directly addresses cultural limitations in historically Western-heavy psychological research. Two older OpenLearn courses are retained as candidates but explicitly flagged for currency comparison rather than receiving automatic prestige credit.

## Language observations

- Ableton exposes many localisations including a generic `Português`; do **not** infer pt-PT or pt-BR without evidence.
- Global Health Training Centre exposes `Português` on several courses but does not state the locale on the public pages inspected; keep it unresolved.
- MathWorks says Onramps are progressively available in multiple standard languages; each individual course must be checked before adding `other_languages`.
- Language Transfer entries distinguish **instruction language** (`en`) from **target language** (`es`, `el`, `sw`, `fr`, `it`, `tr`, `ar`, `de`).

## Access/quality caveats to verify in Phase 2

1. Nordic courses are free but some labs require paid physical hardware; model this separately from course-access cost.
2. MathWorks Onramps require a free MathWorks account but no product licence or paid OTS subscription for browser use.
3. `Learning Synths` requires JavaScript and needs a direct review of scope, language support and completion mechanics.
4. `musictheory.net` has free lessons; confirm the breadth and integration of its free exercise system before final F1 classification.
5. `An introduction to music theory` is pedagogically substantial but was last updated in 2019; compare it head-to-head with newer interactive alternatives.
6. Language Transfer Intro courses should not be penalised for a paywall they do not have, but their deliberately narrower learning scope must be visible in recommendation scoring.
7. Language Transfer `Complete German` is unfinished and currently F3.
8. Older OpenLearn psychology courses require evidence-currency review.
9. WHO Academy course access is confirmed free, but credential/assessment mechanics remain unresolved due to the JavaScript application shell.
10. WHO and TGHN Portuguese variants must not be labelled `pt-PT` or `pt-BR` until explicitly verified.

## Milestone

The research universe now stands at **140 learning experiences**. This is meaningful breadth but still below the intended 300–500-candidate discovery universe.

The next batch should rebalance again rather than continue over-sampling the newly strengthened categories.

## Batch 4 priorities

1. Marketing & Sales beyond HubSpot/Canva.
2. Business, entrepreneurship, finance and accounting from universities/professional bodies.
3. Project/Product/Leadership with deeper project work than short badges.
4. Writing, rhetoric, journalism and professional communication.
5. Natural sciences, astronomy, earth/environmental science and laboratory learning.
6. History and humanities from institutions not already dominated by the Yale archive.
7. Photography, drawing and visual practice with meaningful exercises.
8. Additional psychology/behavioural science only when current or methodologically distinctive.
9. Cybersecurity/networking via Cisco and other hands-on providers once stable direct course URLs are verified.
10. Courses in languages other than English, especially native-language instruction rather than translated subtitles.

## Gate

Do not move any Batch 03 candidate into `data/courses.json` merely because it looks promising. Promotion still requires shallow screening, evidence capture, deep scoring and head-to-head comparison where an incumbent exists.
