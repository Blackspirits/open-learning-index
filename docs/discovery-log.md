# Discovery Log

This file records discovery work before courses receive a deep review or ranking score. Discovery is deliberately broader than publication: presence here is **not an endorsement**.

## 2026-09-09 — v0.2 batch 1

### Scope

Added **41 new candidates** from official provider/course pages. Combined with the 17 reference fixtures already in `data/courses.json`, the current research universe contains **58 unique learning experiences** before later discovery batches.

### Candidate distribution

| Category | New candidates |
|---|---:|
| Computer Science & Software | 7 |
| Mathematics & Statistics | 6 |
| Natural Sciences | 6 |
| Humanities & Philosophy | 6 |
| History & Culture | 3 |
| Engineering & Electronics | 2 |
| Finance & Economics | 2 |
| Arts & Design | 2 |
| AI & Data | 1 |
| Cybersecurity & IT | 1 |
| Health & Medicine | 1 |
| Languages | 1 |
| Marketing & Sales | 1 |
| Psychology & Behaviour | 1 |
| Writing & Communication | 1 |
| Business & Entrepreneurship | 0 |
| Project, Product & Leadership | 0 |

### Providers sampled

- MIT OpenCourseWare
- Open Yale Courses
- Carnegie Mellon University Open Learning Initiative
- The Open University / OpenLearn
- Marginal Revolution University
- Saylor University
- Unity Learn
- The Odin Project
- Nand2Tetris
- fast.ai
- HubSpot Academy

### Evidence standard used in this batch

Every entry has an official provider/course URL and an observation of its apparent free-access tier. These observations are **provisional** until shallow screening verifies hidden paywalls, assessment access, credential rules, language variants, prerequisites and course completeness.

No Quality Score or Recommendation Score is assigned at discovery stage. Scoring before the deep-review evidence exists would create false precision.

### Early signals

Candidates that clearly warrant head-to-head review include MIT's independent-study mathematics sequence, MIT 6.006 and 6.042J, Nand2Tetris, fast.ai Practical Deep Learning, The Odin Project, CMU OLI statistics, Yale's strongest humanities/science archives, and the updated OpenLearn cybersecurity course.

This statement does not guarantee admission to the final index.

### Coverage gaps for batch 2

Batch 2 should deliberately overweight categories underrepresented here rather than keep harvesting computer science:

1. Business & Entrepreneurship
2. Project, Product & Leadership
3. Languages beyond beginner French
4. Health & Medicine with current clinical/public-health material
5. Arts & Design beyond Unity
6. Writing & Communication
7. Modern AI/Data alternatives capable of challenging current leaders
8. Electronics, embedded systems and practical engineering

It should also inspect strong public/specialist sources such as Cisco Networking Academy / Skills for All, OpenWHO, HP LIFE, additional OpenLearn badged courses, university language initiatives, Google/Microsoft/AWS training where the full learning path is genuinely free, and other reputable open-course institutions.

### Next gate

Do not promote these 41 entries directly into `courses.json`.

The next operation is **Phase 2 — shallow screen**:

- confirm F0/F1/F2 vs F3;
- confirm canonical direct course URL;
- verify instruction and subtitle/localisation languages;
- confirm meaningful exercises/projects/assessments;
- identify obviously dated or incomplete material;
- reject marketing-only or redundant candidates;
- identify direct competitors for deep review.
