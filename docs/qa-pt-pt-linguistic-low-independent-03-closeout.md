# QA — pt-PT linguistic Low independent pass 03 / current-state closeout

Date: 2026-09-16  
Baseline: `e50efc5383a14661657e2860480a645816126a32`  
Scope: `site/locales/pt-PT.json`

## Context

The original independent linguistic audit reported **141 Low** findings, but the row-level Low ledger was never versioned. Exact historical reconciliation therefore remains impossible without recovering that source evidence.

To avoid fabricating a 141/141 result, the repository instead records three independent current-state Low passes against the post-Medium dictionary.

## Pass 03 findings

Six current presentation values were corrected:

- three privacy-law descriptions used the English gloss `execution (enforcement)`;
- three chemistry descriptions retained the redundant English gloss `(clickers)` after already translating the concept as **perguntas de resposta imediata**.

For data-protection terminology, official EU Portuguese sources consistently use **aplicação** / **aplicação das regras** for this sense of enforcement:

- https://www.consilium.europa.eu/pt/policies/data-protection-regulation/
- https://www.consilium.europa.eu/pt/press/press-releases/2024/06/13/data-protection-council-agrees-position-on-gdpr-enforcement-rules/

## Intentional English proper names retained

The whole-file scan still encounters a small number of English strings that are not translation defects:

- **Unity Learn Pathway** — official product/path name;
- **Certificate Final Exam** — current official Saylor assessment label;
- **SoundCloud** — brand name.

These are preserved under the course/product-name policy.

## Current-state gate result

Across Low independent passes 01–03, **26 current presentation values** were corrected.

A final scan of all **1,355** pt-PT translation values reports:

- zero known High/Medium regression forms;
- zero audited legacy AO90 forms from the enforced set;
- zero confirmed pt-BR lexical residues from the controlled scan;
- zero double spaces, duplicate punctuation or non-title spaces before punctuation;
- zero generic English residuals from the controlled terminology list, excluding proper names/products documented above;
- zero confirmed article/gender agreement defects from the controlled masculine/feminine scans.

The **current dictionary is therefore clean for the defined Low current-state QA gates**.

## Historical evidence debt

This does **not** claim that the original **141 Low rows** are individually closed. That row-level claim requires recovery of the original ledger.

If that ledger is recovered later, it must be reconciled against the then-current dictionary as a separate historical-evidence gate.

## Boundary

Presentation/localisation only. No canonical course data, providers, URLs, language provenance, access tiers, scores, Deep Reviews, admissions or maintenance dates change.
