# Editorial presentation

This update refines the existing static site. It does not alter eligibility, scores, ranking rules, review ledgers or canonical course records.

## Images

- `site/assets/hero-library.webp`: original generated illustration, encoded at 1536 × 1024, approximately 183 KB. Text remains live HTML; the same image and layout rules serve EN/PT and light/dark. Mobile uses a separate, consistently sized image region.
- `site/assets/course-media.json` retains provenance for 55 images previously observed on official course/provider pages. Records include the page URL, original image URL, import date, original-byte SHA-256, publication state and rights status.
- Those 55 third-party images are currently marked `rights_status: unverified` and `published: false`. Their local binary copies are not distributed by the repository or public build.
- Course cards/details therefore use the original category icon system and a typeset provider name in a restrained editorial panel unless a future media record carries an explicit verified reuse basis.
- The original generated `site/assets/hero-library.webp` remains project artwork and is unaffected.

Source provenance alone is not treated as reuse permission. A third-party image can return only after its reuse licence/permission is verified and recorded.

## Portuguese presentation

`site/locales/pt-PT.json` maps exact public source strings to Portuguese presentation text. It covers titles, descriptions, prerequisites, resources, scope, credential/credit information, recommendation explanations and displayed admission notes. The dictionary began with machine translation of public repository text, followed by terminology corrections and manual review. On 2026-09-15 the full 1,355-entry dictionary received an independent pt-PT/AO90 linguistic review: 800 findings were recorded across 527 entries (252 High, 407 Medium, 141 Low). The first remediation gate applies every High finding plus the fourteen audited global terminology rules; Medium/Low findings remain an explicit follow-up backlog rather than being treated as resolved. Known semantic machine-translation failures are treated as defects and protected by regression tests.

`scripts/editorial_presentation.py` makes a deep copy for localised rendering. IDs, URLs, provider names, languages, dates, statuses, access classifications and all scores stay unchanged. Source strings themselves are the lookup keys: changed editorial text fails the build until its translation is added, rather than silently publishing an English paragraph on a Portuguese page.

When updating a course:

1. Update the canonical course/review through the normal editorial workflow.
2. Add translations for new or changed displayed strings to the dictionary. Preserve programme brands, identifiers and numerical facts; use European Portuguese.
3. Add third-party artwork only when its identity, source, presentation and reuse rights are verified. Record `rights_status: verified_reuse` and `published: true`; otherwise the editorial panel is mandatory.
4. Run the normal validation commands and the presentation tests below.

The public language labels also preserve uncertainty: `pt-PT` and `pt-BR` are named explicitly, while provider-labelled generic `pt` is displayed as “Portuguese (variant unspecified)” / “Português (variante não especificada)”. The public access labels describe what the learner receives. F0/F1/F2 remain canonical filter values and can still occur in the expanded editorial rationale; they are no longer the primary catalogue labels. F3 remains ineligible for publication.

### Course-title policy

Course titles are proper-name data, not ordinary prose. The presentation layer follows these rules:

- the canonical title in `data/courses.json` is always the provider/source title and is never rewritten for localisation;
- a pt-PT **display title** may be a manually reviewed translation in cards/headings, while the page continues to expose the original title;
- when a course is mentioned as a proper noun inside explanatory prose, use the canonical/original course title and translate the surrounding sentence, not the title itself;
- provider, product, programme and method names such as **Full Stack Open**, **Creative Core**, **KICKOFF**, **Language Transfer**, **Thinking Method**, **Nordic**, and named course families are not machine-translated;
- families such as **Onramp** and **Complete X** stay in their original form unless a separately documented project-wide rule is adopted and applied consistently to the whole family;
- an official provider-localised Portuguese title may be used when that provenance is explicit; do not invent a Portuguese title from the institution, country or vocabulary.

This separates learner-friendly display localisation from factual title identity and prevents translated titles from turning into misleading common nouns inside rationale text.

## Interaction and layout

- Cards use one flowing title/provider block in grid and list modes; long titles cannot collide with provider names.
- Filter chips expose current selections, support individual removal and preserve state when switching language. Clear is hidden without active filters.
- Sorting is grouped with the grid/list controls. The sort selector remains associated with the filter form.
- The mobile menu closes on navigation, outside interaction and Escape, restoring focus on Escape.
- Course section links stay visible while reading and mark the current section. On mobile, the main content precedes supporting cards.
- Light category tags/search placeholders and dark view controls have stronger contrast. Search receives a visible focus ring.

## Validation

The build adds content-based revision parameters to local CSS/JavaScript references and to the catalogue/metadata URLs fetched by the app. A catalogue change also changes the app revision, so returning visitors receive matching page assets and data instead of mixing releases from their browser cache. Unchanged builds keep identical URLs.

```sh
python -m unittest discover -s tests -p 'test_*.py'
python scripts/validate.py
python scripts/generate_csv.py
git diff --exit-code -- data/courses.csv
python scripts/build_public_site.py
python scripts/validate_public_site.py _site
python scripts/check_staleness.py
```

Presentation tests cover translation completeness and immutability, fail-fast handling of changed source text, EN/PT asset roots, original-title access, local image provenance and safe fallback rendering. Generated-site QA validates all 330 routes and internal links. Browser checks additionally cover desktop/mobile layouts, both themes/locales, long titles in list view, search/filter state, keyboard focus and menu dismissal.

## Hero generation

The hero was generated with the built-in image generation tool. See [hero prompt](hero-library-prompt.txt) for the exact prompt. The original PNG is retained outside the repository; the project uses the optimised WebP copy above.
