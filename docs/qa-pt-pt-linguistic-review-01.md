# QA — pt-PT linguistic review 01

Date: 2026-09-15  
Baseline: `5d1262eb9b1d2187fecace4c9b30c709210b0b58`  
Scope: `site/locales/pt-PT.json`

## Trigger

An independent full-file linguistic review examined all **1,355** pt-PT presentation entries. It reported **800 findings across 527 entries (39%)**:

- **252 High**
- **407 Medium**
- **141 Low**

The strongest defects were concentrated in long-form rationale/decision text rather than short factual fields. The review identified systematic machine-translation artefacts, including false friends, pre-AO90 spellings, altered proper names/acronyms, misleading academic terminology, zero-width spaces and a small number of meaning inversions.

This QA gate is a presentation-only correction. It does not change canonical course records, provider URLs, scores, recommendation ranks, access tiers, review dates, admissions or language provenance.

## Remediation gate

This pass applies:

1. every **High** finding from the supplied audit ledger;
2. all occurrences covered by the audit's fourteen global rules, including Medium/Low rows where necessary;
3. a deterministic final normalisation pass for the rules that are safe to enforce mechanically.

The applied selection contains **346 audit rows**: all 252 High findings plus 94 additional G1–G14 findings.

### G1–G14

- **G1** — survey-course false friends → *curso panorâmico / panorama* according to context;
- **G2** — audited pre-AO90 forms → AO90;
- **G3** — academic *lecture(s)* → *aula(s)*, not *palestra(s)*;
- **G4** — *badge* → **emblema digital**;
- **G5** — editorial *pool* → **lote**, not *mercado/piscina*;
- **G6** — *midterm / term exams* → **teste intercalar / testes de frequência**;
- **G7** — learning-platform *unit tests* → **testes por unidade**; genuine software unit tests remain **testes unitários**;
- **G8** — mathematical *proof(s)* → **demonstração/demonstrações**;
- **G9** — algorithms terminology: **greedy (guloso)**, **grafos**, **ordenação**, **ordenação topológica**;
- **G10** — Quality criterion *Currency* → **Atualidade**;
- **G11** — *live* meaning launched/available → **disponível**; genuinely synchronous live events remain **ao vivo**;
- **G12** — *Browser / Web browser* → **Navegador**;
- **G13** — *European-Portuguese* → **português europeu**;
- **G14** — remove U+200B zero-width spaces.

A post-application scanner reports no residual violations for G1–G6 and G8–G14. The sole G7 scanner hit is intentional: a Python course describes genuine software **unit tests**, so **testes unitários** is correct there.

## High-severity classes corrected

The applied High findings include, among others:

- altered names/acronyms such as **E-E-A-T**, **Algorithmi**, **Regulação Digital**, **Ciência Aberta e Dados FAIR**, **WEIRD**, **Language Transfer** and **Nordic**;
- meaning inversions such as *Living course* → *curso presencial*, *explicitly not clinical* and imperative readings of *Complete ...*;
- scoring terminology such as *Currency* incorrectly rendered as money;
- academic false friends around *survey*, *midterm*, *proof*, *practice exam*, *unit tests*, *lecture*, *audit* and *notebook*;
- technical false friends in databases, BLE, profiling, algorithms and mathematics;
- five regressions where source Portuguese had been replaced by English;
- all audited U+200B invisible characters.

## Course-title policy

The title-policy ambiguity identified by the review is resolved as follows:

1. the canonical title in `data/courses.json` remains the exact provider/source title;
2. pt-PT cards/headings may use a manually reviewed **display translation** while retaining and exposing the original title;
3. inside explanatory prose, course titles are treated as proper nouns and use the canonical/original form; the surrounding sentence is translated instead;
4. provider/product/programme/method names are not machine-translated;
5. named families such as **Onramp** and **Complete X** remain original unless a separately documented project-wide rule is adopted for the whole family;
6. official provider-localised Portuguese titles may be used when their provenance is explicit.

This avoids constructions where translated titles become common nouns (for example, a course title being rendered as “a aula ...”) while preserving learner-friendly display localisation.

## Remaining backlog

This gate does **not** claim that all 800 findings are closed. The **407 Medium** and **141 Low** findings remain a deliberate follow-up backlog except where they were included by G1–G14.

The next linguistic pass should prioritise:

- remaining technical/academic terminology;
- consistent route/pathway terminology, preferring **percurso** where appropriate;
- application of the title policy to the remaining Medium/Low title-consistency findings;
- pt-PT score-number formatting consistency in the UI.

No course-content or scoring re-review is implied by this language QA.
