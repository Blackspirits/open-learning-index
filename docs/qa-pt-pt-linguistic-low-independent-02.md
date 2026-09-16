# QA — pt-PT linguistic Low independent pass 02

Date: 2026-09-16  
Baseline: `784b2847bd917a7b5bbbcef2f5f71988981abdb7`  
Scope: `site/locales/pt-PT.json`

## Trigger

After Low independent pass 01, a controlled agreement scan checked masculine and feminine course-description nouns against nearby articles, adjectives and passive participles.

## Finding

One high-confidence defect remained:

- `uma curso panorâmico completo ... não é substituída`

It is corrected to:

- `um curso panorâmico completo ... não é substituído`

The mirrored scan for feminine nouns followed by masculine passive/adjectival agreement found no confirmed defects.

## Regression protection

`tests/test_editorial_presentation.py` now blocks the malformed article and the specific passive-agreement regression.

## Boundary

This is a current-state Low-severity correction. It does not reconstruct the missing historical 141-row Low ledger and does not change canonical course data, scores, access, evidence or admissions.
