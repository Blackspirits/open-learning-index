# Phase 5 QA — primary-source re-verification 02

## Scope

Re-verify eight high-volatility admitted technical records, prioritising the exact risk families left after batch 01:

- AI agents;
- developer tooling;
- version-sensitive game-development tooling;
- Cisco data/security pathways.

This is a currentness and publication-metadata pass, not a re-scoring exercise.

## Result

**8 / 8 records retained.**

No access-tier, certificate-type, category, Quality Score or Recommendation Score change is required.

Five records move their canonical `last_verified` date from **2026-09-12** to **2026-09-13**. The three Cisco security records were already verified on 2026-09-13 during their final Phase 4 admission pass and are spot-checked here without an artificial second date change.

## Hugging Face — AI Agents Course

The official living course still states that it is free, supports audit or certification routes, uses hands-on assignments and a final challenge, and has no certification deadline.

The current certification pages still expose both the Unit 1 certificate path and the final-project certificate path.

Primary evidence:

- https://huggingface.co/learn/agents-course/en/unit0/introduction
- https://huggingface.co/learn/agents-course/en/unit1/get-your-certificate
- https://huggingface.co/learn/agents-course/unit4/get-your-certificate

Decision: retain `F0_FULL_CREDENTIAL`, free provider certificate, 60-day review cadence.

## Developer tooling

### The Odin Project — Foundations

The current Foundations route still covers command line, Git, HTML, CSS, JavaScript, debugging and multiple projects.

The provider FAQ explicitly confirms that the curriculum is free and that no completion certificate is issued. The contribution page also confirms that the curriculum is actively maintained by the open-source community.

Primary evidence:

- https://www.theodinproject.com/paths/foundations/courses/foundations
- https://www.theodinproject.com/lessons/foundations-how-this-course-will-work
- https://www.theodinproject.com/faq
- https://www.theodinproject.com/contributing

Decision: retain `F1_FULL_ASSESSMENTS`, no certificate. Evidence is strengthened.

### MIT — The Missing Semester of Your CS Education — 2026

The official 2026 site remains live and explicitly covers the current cohort's shell environment, development tools, debugging/profiling, Git, packaging/shipping code, agentic coding and code quality.

The site also explicitly identifies the material as the **2026** edition and links the recorded 2026 lectures.

Primary evidence:

- https://missing.csail.mit.edu/

Decision: retain `F2_CONTENT_ONLY`; no credential is claimed.

## Unity Learn — Junior Programmer

The current official pathway remains a twelve-week guided route with version control, debugging, project management, portfolio work, UI programming, optimisation, OOP and application scripting.

The current version page states that the pathway supports the available versions and that its content presently uses **Unity 6.3**.

The completion page continues to document the pathway badge issued through Credly.

### Metadata correction

The current pathway explicitly exposes these additional available languages:

- German;
- Japanese;
- French;
- Portuguese;
- Chinese;
- Spanish;
- Russian;
- Korean.

Canonical `other_languages` is therefore corrected to:

`de, ja, fr, pt, zh, es, ru, ko`

No regional Portuguese variant is inferred because the official page labels the option only as **Português**.

Primary evidence:

- https://learn.unity.com/pathway/junior-programmer
- https://learn.unity.com/pathway/junior-programmer/unity-version
- https://learn.unity.com/pathway/junior-programmer/completed?version=6.0

Decision: retain `F0_FULL_CREDENTIAL` / free badge. Update the Gate 2 language-accessibility counts so publication documentation remains consistent with canonical data.

## Cisco Networking Academy

The four Cisco records checked in this batch remain live on their current official NetAcad course routes:

- Data Analytics Essentials;
- Cyber Threat Management;
- Ethical Hacker;
- Networking Basics.

Cisco's official course material continues to support the recorded learning roles and digital-badge model. Current NetAcad landing pages are JavaScript-heavy, so detailed module/lab corroboration still relies partly on Cisco's own published course-catalog/course-overview material rather than inferred third-party summaries.

### Data Analytics Essentials

The official route remains live. Cisco's published course material continues to describe the applied analytics path through spreadsheets, SQL, Tableau, labs/exams and portfolio work, with a digital badge.

Primary evidence:

- https://www.netacad.com/courses/data-analytics-essentials
- https://www.netacad.com/sites/default/files/course-catalog.pdf

Decision: retain `F0_FULL_CREDENTIAL` / free badge and advance canonical verification to 2026-09-13.

### Cyber Threat Management

The current course route remains live. Cisco's official catalog describes the governance/risk/threat-management role, six modules, labs/Packet Tracer activities, assessment and digital badge.

Primary evidence:

- https://www.netacad.com/courses/cyber-threat-management
- https://www.netacad.com/sites/default/files/course-catalog.pdf

Decision: retain existing metadata. Canonical date was already 2026-09-13.

### Ethical Hacker

The current route remains live. Cisco's official course overview documents the 70-hour pathway, 34 labs, 86 interactive activities/quizzes, final exam, skills-based assessment and digital badge.

Primary evidence:

- https://www.netacad.com/courses/ethical-hacker
- https://www.netacad.com/sites/default/files/course-catalog.pdf

Decision: retain existing metadata. Canonical date was already 2026-09-13.

### Networking Basics

The current route remains live. Cisco's official material documents the general networking foundation, hands-on labs, interactive assessment and digital badge.

Primary evidence:

- https://www.netacad.com/courses/networking-basics
- https://www.netacad.com/sites/default/files/course-catalog.pdf

Decision: retain existing metadata. Canonical date was already 2026-09-13.

## Canonical changes

Changed records:

- `huggingface-agents-course` — `last_verified` → 2026-09-13;
- `cisco-data-analytics-essentials` — `last_verified` → 2026-09-13;
- `odin-foundations` — `last_verified` → 2026-09-13, `next_review` → 2026-12-12, stronger primary evidence;
- `unity-junior-programmer` — `last_verified` → 2026-09-13, `next_review` → 2026-12-12, verified alternate languages added;
- `mit-missing-semester-2026` — `last_verified` → 2026-09-13, `next_review` → 2026-12-12.

No canonical record is removed.

## Next gate

Continue Gate 3 with the highest-risk non-technical publication records:

1. Health & Medicine / clinical-research routes;
2. Law & Public Policy routes whose usefulness depends on current law or institutional frameworks;
3. session/cohort-dependent courses;
4. remaining vendor tooling where access or version mechanics are unusually fragile.

Broad discovery remains paused.
