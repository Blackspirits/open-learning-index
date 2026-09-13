# Phase 4 admission calibration 01

## Purpose

Test the Phase 4 admission model on a deliberately mixed set before category-scale decisions.

This calibration is not a score threshold. It tests whether the project can:

- admit a course because it adds a genuinely missing learning role;
- preserve a strong archive when stable fundamentals outweigh tooling age;
- admit non-English coverage without lowering the quality bar;
- refuse an excellent course when a stronger published pathway makes it redundant;
- control provider concentration;
- refuse a useful specialist microcourse when the canonical set already covers the learning need better.

## Decisions

| Candidate | Quality | Recommendation | Decision | Main reason |
|---|---:|---:|---|---|
| Nand2Tetris | 9.48 | 9.6 | **admit** | unique twelve-project first-principles systems pathway |
| MIT 6.006 Algorithms | 9.18 | 9.2 | **admit** | dedicated rigorous algorithms gap; archive age is mostly tooling, not conceptual |
| Al Jazeera Learning Arabic | 8.88 | 9.0 | **admit** | broad Arabic pathway fills a proven language gap at a strong quality level |
| Odin Foundations | 8.90 | 9.2 | **admit** | best beginner bridge into real web-development workflow before Full Stack Open |
| freeCodeCamp Responsive Web Design v9 | 8.72 | 9.0 | **do_not_admit** | excellent course, but narrower marginal value after Odin + Full Stack Open |
| HubSpot Content Marketing | 8.39 | 8.5 | **do_not_admit** | stronger broad HubSpot incumbent plus severe provider-concentration risk |
| Kaggle Intermediate Machine Learning | 8.62 | 8.8 | **do_not_admit** | useful four-hour accelerator, but canonical ML coverage is already substantially stronger |

## Calibration findings

### 1. Quality is necessary, not sufficient

freeCodeCamp Responsive Web Design is an A+ resource with strong practice, current content and a free credential.

It is still not admitted because the published learner pathway is better served by:

- **Odin Foundations** for beginner developer workflow and broader HTML/CSS/JavaScript integration;
- **Full Stack Open** for the later intermediate full-stack stage.

This is the intended Phase 4 behaviour: preserve the course as reviewed evidence without giving every strong resource a publication slot.

### 2. Archive age remains subject-sensitive

MIT 6.006 is a 2011 archive and explicitly contains obsolete Python 2.7 / Athena setup details.

That does not outweigh the current value of its algorithms, analysis, recitations, problem sets, programming assignments, exams and solutions. Stable theoretical content survives the archive test; stale tooling is documented rather than hidden.

### 3. Coverage diversity cannot override quality

Al Jazeera Learning Arabic is not admitted merely because Arabic was under-covered.

It earns admission because the Deep Review found a strong open pathway from introductory material toward proficiency, with authentic text/audio, interactive exercises, placement and rich supporting tools. The language gap matters only after the quality threshold is independently met.

### 4. Provider concentration is a real admission filter

HubSpot Content Marketing is a valid current free certification.

It does not add enough marginal value beside the stronger existing **HubSpot Digital Marketing** canonical record, while the reviewed Marketing pool is already overwhelmingly HubSpot-heavy. Admitting adjacent certifications without a distinct learning-role gain would reproduce a provider catalogue rather than curate it.

### 5. Microcourse usefulness is not the same as core-index value

Kaggle Intermediate Machine Learning is highly useful after basic ML.

The canonical set already contains:

- Kaggle Intro to Machine Learning;
- Google Machine Learning Crash Course;
- CS50 AI.

The four-hour intermediate workflow module adds useful refinements, but not enough new coverage to justify a fourth core ML slot.

## Canonical-set effect

This calibration adds four courses to `data/courses.json`:

1. `nand2tetris`
2. `mit-6-006-algorithms`
3. `aljazeera-learning-arabic-general-language`
4. `odin-foundations`

Canonical records rise from **17 to 21**.

The three `do_not_admit` candidates remain in discovery/screening/Deep Review history and can be reconsidered later if incumbents degrade or coverage needs change.

## Gate result

If repository validation passes, the admission model is calibrated well enough to scale category by category.

The next pass should process a complete comparison family rather than cherry-picking globally by score.
