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

---

## 2026-09-09 — v0.2 batch 2

### Scope

Added **41 further candidates** with an explicit bias toward the categories that batch 1 underrepresented. The discovery pool now contains **82 candidates**, and the complete research universe contains **99 unique learning experiences** when the 17 v0.1 reference fixtures are included.

Batch 2 is stored separately in `data/candidates/batch-02.json`. Validation treats the legacy `data/candidates.json` and every JSON file under `data/candidates/` as one candidate pool, so IDs and canonical URLs must remain unique across batches.

### Candidate distribution

| Category | New candidates |
|---|---:|
| Languages | 6 |
| Business & Entrepreneurship | 5 |
| AI & Data | 5 |
| Project, Product & Leadership | 4 |
| Computer Science & Software | 4 |
| Arts & Design | 3 |
| Cybersecurity & IT | 3 |
| Writing & Communication | 3 |
| Natural Sciences | 2 |
| Health & Medicine | 2 |
| Finance & Economics | 2 |
| Engineering & Electronics | 1 |
| Mathematics & Statistics | 1 |
| History & Culture | 0 |
| Humanities & Philosophy | 0 |
| Marketing & Sales | 0 |
| Psychology & Behaviour | 0 |

### Providers sampled

- HP LIFE
- The Open University / OpenLearn
- Microsoft Learn
- AWS Training and Certification
- FAO elearning Academy
- European Commission / EU Academy
- IBM SkillsBuild
- freeCodeCamp
- Khan Academy

### Why these were added

This batch deliberately mixes institutional, public-sector and specialist learning providers instead of optimising for university prestige alone.

Notable discovery signals include:

- **HP LIFE** for freely credentialled, highly practical business and workplace skills;
- **OpenLearn** for substantial university-authored courses with free statements of participation;
- **Microsoft Learn** for current AI, AI-agent and AI-security learning paths with assessments;
- **FAO elearning Academy** for rigorous professional food, nutrition and climate material with final tests and digital badges;
- **freeCodeCamp** for current project/lab-driven technical certifications and structured language certifications;
- **Khan Academy** for mastery-oriented assessment in statistics, financial literacy and art history;
- **IBM SkillsBuild** for credential-bearing AI, cyber and data pathways;
- **EU Climate Action Academy** for actively maintained climate-action material and a certificate of participation.

### Evidence caveats identified during discovery

Discovery is intentionally not deep review. Several items already have flags for Phase 2:

1. IBM SkillsBuild's public catalog can hand off to a separate learning platform. Stable course-specific canonical launch URLs must be resolved before promotion.
2. HP LIFE exposes Portuguese on several courses, but discovery evidence does not justify assuming `pt-PT`; locale must be classified explicitly.
3. Microsoft AI-901 explicitly lists **Portuguese (Brazil)**, so it must be recorded as `pt-BR`, not generic Portuguese.
4. AWS Cloud Essentials is conservatively classified F2 until meaningful free assessment/completion mechanics are verified.
5. FAO's climate-smart agriculture series states that its courses have final tests and digital badges; the credential path for the individual introductory course must still be checked directly.
6. Some older OpenLearn courses may remain excellent but need a currency check against newer alternatives before deep review.

### Current milestone

The project has reached **99 researched learning experiences** without assigning scores prematurely. This is still below the intended 300–500 candidate universe, so publication of a definitive Top 100 would be methodologically premature.

### Coverage goals for batch 3

Batch 3 should continue discovery while shifting attention toward sources and fields still insufficiently sampled:

1. current Health & Medicine and public-health education, including WHO/OpenWHO/WHO Academy where stable course URLs are available;
2. electronics, embedded systems, robotics, CAD and practical engineering;
3. visual design, photography, music and creative practice;
4. stronger writing, rhetoric and communication curricula;
5. additional high-quality language programmes, especially courses whose instruction/subtitle languages can be verified precisely;
6. marketing and sales alternatives capable of challenging the current HubSpot references;
7. psychology and behavioural science from current university/open providers;
8. business, finance and leadership alternatives from public universities and professional bodies;
9. additional modern AI/Data/Cyber courses only where they add depth or can plausibly displace an incumbent;
10. major open universities and institutions not yet sampled sufficiently, while actively avoiding prestige bias.

The candidate universe should keep growing until category coverage begins to saturate. Only then should Phase 2 shallow screening become the dominant activity.
