# Coverage Audit — v0.2 after Batch 6

**Audit date:** 2026-09-10  
**Discovery candidates:** 246  
**Reference fixtures:** 17  
**Total researched learning experiences:** 263

## Executive conclusion

The project has enough breadth to stop treating discovery as a single global phase.

The best next architecture is a **hybrid pipeline**:

1. begin **shallow screening now** in categories that already have a credible competitive field;
2. continue targeted discovery in categories that remain thin or institutionally concentrated;
3. aim for roughly **320–350 serious candidates**, not 500 by default;
4. only push toward 400–500 if the next saturation audit still finds meaningful blind spots.

A fixed target of 500 would now create quantity pressure and increase low-value duplicates. The stopping criterion should be evidence of category saturation, not a round number.

## Candidate coverage by category

| Category | Candidates | Audit state |
|---|---:|---|
| AI & Data | 20 | Start shallow screening |
| Arts & Design | 19 | Start shallow screening; continue only for strong practice-led/photography gaps |
| Languages | 18 | Start shallow screening; improve original-language and CEFR-path diversity |
| Natural Sciences | 16 | Start shallow screening; seek newer non-MIT/Yale challengers selectively |
| Cybersecurity & IT | 14 | Start shallow screening |
| Health & Medicine | 14 | Start shallow screening; retain strict currency checks |
| Law & Public Policy | 14 | Start shallow screening; improve jurisdictional diversity |
| Engineering & Electronics | 13 | Start shallow screening; selectively add robotics/CAD/control alternatives |
| Marketing & Sales | 12 | Start shallow screening |
| Psychology & Behaviour | 12 | Start shallow screening; penalise outdated science aggressively |
| Writing & Communication | 12 | Start shallow screening |
| Business & Entrepreneurship | 12 | Start shallow screening |
| Project, Product & Leadership | 12 | Start shallow screening |
| Education & Teaching | 12 | Start shallow screening |
| Computer Science & Software | 11 | Strong quality despite modest count; targeted discovery only |
| Mathematics & Statistics | 10 | Targeted discovery still useful |
| Humanities & Philosophy | 9 | Continue discovery |
| Finance & Economics | 9 | Continue discovery |
| History & Culture | 7 | Highest-priority discovery gap |

## Saturation rule

Candidate count alone is not enough. A category is considered provisionally saturated only when all three conditions are met:

- **volume:** enough plausible candidates exist for meaningful comparison;
- **provider diversity:** the field is not dominated by one institution or ecosystem;
- **path diversity:** candidates include materially different pedagogical models, levels or specialisations rather than near-duplicates.

A category can therefore have 15 candidates and still need discovery, while another with 10 exceptionally diverse candidates may already be ready for screening.

## Highest-priority discovery gaps

### 1. History & Culture

Only 7 candidates. The current pool is too dependent on a small number of anglophone providers. Next discovery should seek high-quality global/world-history, regional-history, archaeology, cultural-history and museum/public-humanities learning from additional institutions and non-English originals.

### 2. Finance & Economics

Nine candidates is not enough for a final global ranking. Add current personal finance, accounting/financial literacy, macro/micro, behavioural economics and applied corporate-finance alternatives, while distinguishing timeless theory from jurisdiction-sensitive material.

### 3. Humanities & Philosophy

Nine candidates gives useful foundations but insufficient breadth. Seek ethics, logic, political thought, literature, religion as an academic subject, classics and philosophy of science from providers beyond the current Yale/OpenLearn concentration.

### 4. Mathematics & Statistics

The existing candidates are unusually strong, so this is a quality rather than quantity gap. Continue only for major challengers in probability, calculus, discrete mathematics, statistics and applied mathematical reasoning.

### 5. Non-English originals

Batch 6 materially improves `pt-PT` and French coverage, but English still dominates the project. Discovery should deliberately include strong original-language courses in Portuguese, French, Spanish, German, Japanese and other languages instead of counting translated interfaces as equivalent diversity.

## Categories where shallow screening should begin immediately

AI/Data, Arts/Design, Languages, Natural Sciences, Cybersecurity/IT, Health/Medicine, Law/Public Policy, Engineering/Electronics, Marketing/Sales, Psychology/Behaviour, Writing/Communication, Business/Entrepreneurship, Project/Product/Leadership and Education/Teaching now have enough candidates to begin eliminating weak, redundant, dated or partially-free entries.

Computer Science should also begin screening because its candidate count understates the strength and depth of the existing field: Harvard CS50, Helsinki, MIT, Full Stack Open, The Odin Project and related references already provide strong competitive anchors.

## Language-model audit

The current candidate schema stores `primary_language` plus free-text `language_notes`. That is sufficient for discovery but not for publication.

Before v1.0, the canonical course schema should distinguish at least:

- `instruction_languages`
- `subtitle_languages`
- `interface_languages`
- `original_language`
- `translation_status` or equivalent provenance

`pt-PT` and `pt-BR` must remain separate. A course with an English lecture and Portuguese subtitles must never be presented as a Portuguese-language course.

This schema migration should occur **after shallow screening**, when fewer records remain and language evidence is being verified anyway.

## Free-access audit

The F0/F1/F2/F3 model remains sound, but discovery evidence has shown why it must be verified through the complete learner journey.

Particular risks:

- catalogue pages that remain visible after enrolment closes;
- platforms that move a course to a paid/verified track;
- free videos but paid labs or graded work;
- free assessment but paid certificate;
- free certificate claims that apply only to one cohort;
- hardware, cloud credits or proprietary software required to complete practical work.

No course should be promoted to the final ranking solely from a marketing/catalogue page.

## Provider-concentration risk

OpenLearn, Saylor, MIT/Yale archives and several technology vendors are intentionally well represented during discovery. This is acceptable now, but the final index must not become a provider leaderboard.

During shallow screening, near-duplicate courses from the same provider should compete against each other. The final list should retain multiple courses from one provider only when each independently earns its place and covers materially different learning outcomes.

## Recommended next milestone

### Track A — Shallow screen

Start with the most saturated categories and verify:

- actual current free access;
- canonical working course URL;
- instruction/subtitle/interface languages;
- assessment and credential mechanics;
- course completeness;
- prerequisites and practical requirements;
- obvious currency problems;
- redundancy against stronger candidates.

### Track B — Discovery Batch 7

Add only approximately **35–45 high-value candidates**, prioritising:

1. History & Culture
2. Finance & Economics
3. Humanities & Philosophy
4. Mathematics & Statistics challengers
5. original-language non-English courses
6. selective Computer Science systems/fundamentals gaps

After Batch 7, run a second saturation audit. If the pool is around **285–310 candidates**, one final targeted batch may be enough to reach the evidence-based stopping point near 320–350.

## Decision

**Do not wait for 500 candidates before screening.**  
**Do not stop discovery entirely at 246 candidates either.**

The optimal strategy is now parallel, evidence-driven and category-specific. This reduces research waste while preserving the project's original promise: publish only the world's strongest genuinely free learning experiences, not the largest list of links.
