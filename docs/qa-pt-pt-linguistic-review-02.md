# QA — pt-PT linguistic review 02

Date: 2026-09-16  
Baseline: `4ed46bc50d1b30ef7dea09453681a27ae089e760`  
Scope: continuation of the independent pt-PT linguistic review plus catalogue language/level presentation QA.

## Trigger

After the High-severity/G1–G14 gate, the next pass moved into the Medium backlog and direct live-site presentation QA.

Two catalogue defects were confirmed during this pass:

1. the **Level** filter was alphabetically sorted rather than following a learning progression;
2. Portuguese variants had explicit capitalised labels while other languages were produced by `Intl.DisplayNames` in lower case, creating inconsistent casing in the pt-PT language filter.

## Catalogue fixes

### Level order

The public filter now uses a fixed semantic order rather than locale alphabetic order:

1. Beginner / Principiante
2. Beginner to intermediate / Principiante a intermédio
3. Beginner to advanced / Principiante a avançado
4. Intermediate / Intermédio
5. Intermediate to advanced / Intermédio a avançado
6. Advanced / Avançado
7. Undergraduate / Licenciatura
8. Graduate / Pós-graduação

Range labels remain grouped by their learner entry point. Unknown future levels fall back after the known progression and are then ordered by label.

### Language casing

Portuguese language names are common nouns in Portuguese and are therefore displayed consistently in lower case:

- inglês
- francês
- português (Portugal)
- português (Brasil)
- português (variante não especificada)

The English interface keeps normal English display labels such as `Portuguese (Portugal)`.

A dedicated UI-contract test now locks both the level order and the locale boundary between English and pt-PT language labels.

## Medium linguistic pass

This pass continues the audit rather than declaring the entire Medium backlog closed.

Relative to the High-gate baseline, the branch currently changes presentation text across hundreds of dictionary entries. The main systematic corrections in this pass include:

- **route/pathway → percurso**, followed by Portuguese gender/agreement repair;
- untranslated learner-facing remnants such as `Browser`, `badge`, `quiz` and `Statement of Participation`;
- application of the documented course-title policy to running prose;
- editorial selection terminology such as `survivor` → **candidato remanescente**;
- **canonical bar** → **limiar canónico**;
- education-specific **mastery** terminology → **mestria** where appropriate;
- research-data, database, access and academic-register terminology;
- residual punctuation/agreement defects introduced or exposed by the systematic passes.

The course-title policy is now being applied operationally: canonical course names remain proper nouns inside rationale prose even when a localized display title exists elsewhere in the interface.

## Important boundary

This QA pass changes only the presentation layer.

It does **not** change:

- canonical course titles in `data/courses.json`;
- providers or URLs;
- language provenance;
- F0/F1/F2 access classification;
- Quality or Recommendation scores;
- Deep Review or admission evidence;
- review dates or maintenance cadence.

## Final Medium gate

This document records the intermediate Medium pass that was merged in #145. The subsequent row-by-row reconciliation is recorded in `qa-pt-pt-linguistic-review-01.md`.

The **407 Medium findings are now reconciled** against the post-High dictionary. Rows already corrected by G1–G14 were counted as covered rather than edited again; residual wording and terminology defects found during the clean reconstruction were corrected before closure.

The remaining independent-audit class is **141 Low** findings. Those remain a separate final linguistic pass and must be rechecked against the current dictionary before any change is applied.
