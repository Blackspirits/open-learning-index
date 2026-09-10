# v0.2 Discovery Batch 6 — 2026-09-10

## Scope

Batch 6 adds **41 discovery candidates** with a deliberate corrective bias toward the categories that remained thinnest after Batch 5, while also improving non-English and Portuguese-European coverage.

After this batch, the project contains **246 discovery candidates + 17 reference fixtures = 263 researched learning experiences**.

Presence in this batch is not endorsement. No new candidate receives a Quality Score or Recommendation Score at discovery stage.

## Distribution

| Category | New candidates |
|---|---:|
| Psychology & Behaviour | 8 |
| Law & Public Policy | 8 |
| Education & Teaching | 7 |
| Project, Product & Leadership | 6 |
| AI & Data | 5 |
| Writing & Communication | 4 |
| Business & Entrepreneurship | 1 |
| Marketing & Sales | 1 |
| Health & Medicine | 1 |
| **Total** | **41** |

## Providers sampled

- Saylor University
- MIT OpenCourseWare
- The Open University / OpenLearn
- NAU and Portuguese university/public-sector partners
- Council of Europe HELP
- British Council TeachingEnglish
- European School Education Platform
- OpenClassrooms
- Hugging Face

## Strong discovery signals

- **Council of Europe HELP** provides an unusually strong model for genuinely free legal education: public self-learning, knowledge tests and downloadable Statements of Accomplishment. The updated **Artificial Intelligence and Human Rights** course is especially current.
- **NAU** materially improves the index's Portuguese-European coverage. Several candidates combine free assessment and certificates; the NOVA entrepreneurship course advertises **1 ECTS**, while *Saúde das Populações para um Futuro Sustentável* advertises **2 ECTS**.
- **Hugging Face AI Agents Course**, **Audio Course** and **Deep Reinforcement Learning Course** use completely free certification processes tied to hands-on assignments rather than passive video completion.
- **Saylor PSYCH101** and **BUS402** add long-form, assessed, free-certificate alternatives in psychology and project management.
- **OpenLearn Forensic psychology** provides an eight-week applied pathway with quizzes and recognition, while **Open education** adds a substantial advanced treatment of OER, MOOCs and open pedagogy.
- **OpenClassrooms Apprenez à apprendre** was updated in September 2026 and provides a useful French-original learning-skills candidate with quizzes and practical exercises.

## Validation-driven replacements

The first CI run detected four proposals that overlapped earlier research: two OpenLearn psychology entries, an OpenLearn online-teaching URL, and Google Machine Learning Crash Course, which already exists among the reference/approved records. Duplicate protections were kept intact. Those four slots were replaced with **Making sense of ourselves**, **Living psychology: animal minds**, **Open education**, and the **Hugging Face Audio Course**.

## Evidence caveats

1. NAU has both native NAU courses and courses that may later move to edX under PortugalX. Shallow review must verify current enrolment availability rather than assuming a visible catalogue page guarantees an active learner path.
2. Some NAU AI course pages clearly expose assessments but do not clearly state a free completion credential, so they remain F1 rather than F0 at discovery stage.
3. Council of Europe HELP course announcements are sometimes more stable/indexable than the Moodle launch URLs. Shallow review must resolve the current direct learning URL for publication.
4. Older MIT/OpenLearn psychology material must be checked against current research; age alone is not a rejection criterion, but psychology is not treated as timeless.
5. The European School Education Platform AI-literacy candidate remains `UNVERIFIED` until the complete learner journey and completion mechanics are confirmed.
6. OpenClassrooms courses expose complete lessons and quizzes for free accounts, but certificate mechanics must be checked before any F0 classification.
7. `primary_language` now includes explicit `pt-PT` where the course is clearly produced for Portuguese learners by Portuguese institutions. Future review should still record interface, instruction and subtitle language separately when applicable.

## Gate after Batch 6

Batch 6 triggers the first formal coverage audit. The project should **not** simply continue adding 41-course batches until an arbitrary number is reached.

The next phase should be hybrid:

- continue discovery only in categories or provider/language segments that remain under-covered;
- start shallow screening immediately in categories that already have enough plausible contenders;
- stop discovery in a category once additional candidates cease to add provider diversity, materially different pedagogy or a plausible challenger to an incumbent.

See [`docs/coverage-audit-v0.2.md`](../coverage-audit-v0.2.md).
