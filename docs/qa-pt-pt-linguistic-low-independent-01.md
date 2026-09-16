# QA — pt-PT linguistic Low independent pass 01

Date: 2026-09-16  
Baseline: `6891cb2041d91b300d4ed02b48dfbfbb97d0e7a4`  
Scope: `site/locales/pt-PT.json`

## Context

The original independent linguistic audit reported **141 Low** findings, but its row-level ledger was never committed to the repository. The repository therefore retains the count and remediation history, but not enough evidence to reconstruct those 141 rows exactly.

This pass does **not** claim to replace or close that missing ledger.

Instead, it performs a new independent Low-severity review against the current post-Medium dictionary and records only defects that can be verified directly in the checked-in presentation text.

## Pass 01 findings

The first pass corrects **19 current presentation entries** with high-confidence style, grammar or consistency defects:

- agreement around course-title references;
- incomplete phrases such as “four exams and a final” where the source clearly means a final exam;
- implicit course-title subjects with wrong grammatical gender;
- residual explanatory English such as `vendor training`;
- duplicated wording in `Introduction to Data Science de Dados`;
- `final assignment` rendered only as “um final” instead of **trabalho final**;
- an awkward person-like rendering of a specialist course;
- `Relaunch` / `Data Sharing course` left untranslated in running Portuguese prose;
- technical-gender consistency: **múltiplos/vários frameworks**;
- terminology consistency: **nuvem** rather than residual **cloud** in Portuguese explanatory prose;
- residual noun-phrase fragments such as **Atual especialista...** rewritten as explicit **Curso especializado...** descriptions;
- residual “um final” wording clarified as **exame final** where the source explicitly denotes a final exam.

Course and product names remain unchanged where they function as proper names.

## Regression protection

`tests/test_editorial_presentation.py` now blocks the malformed forms corrected in this pass.

## Boundary

This is presentation-only QA. It does not change canonical course records, titles, URLs, providers, language provenance, access tiers, scores, Deep Reviews, admissions or maintenance dates.

## Remaining gate

The historical **141 Low** count remains unresolved as a row-level ledger because that source evidence is absent from the repository.

Further Low work should continue as independently documented current-state passes. If the original ledger is recovered later, it should be reconciled separately against the then-current dictionary rather than assumed equivalent to these new passes.
