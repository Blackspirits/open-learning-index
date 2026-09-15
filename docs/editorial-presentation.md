# Editorial presentation

This update refines the existing static site. It does not alter eligibility, scores, ranking rules, review ledgers or canonical course records.

## Images

- `site/assets/hero-library.webp`: original generated illustration, encoded at 1536 × 1024, approximately 183 KB. Text remains live HTML; the same image and layout rules serve EN/PT and light/dark. Mobile uses a separate, consistently sized image region.
- `site/assets/course-media.json`: provenance for 55 selected images observed on official course/provider pages. Records include the page URL, original image URL, import date and original-byte SHA-256.
- `site/assets/courses/`: locally served WebP copies, downsampled without cropping. Course illustrations and provider branding use separate presentation classes.
- Courses without suitable official images use the existing category icon system and a typeset provider name in a restrained colour panel. These panels are original UI components, not invented institutional logos.
- Images are decorative beside the visible title/provider, have empty alt text, reserve their layout space, and load lazily outside the main hero. Browsing does not contact external image hosts.

Third-party course artwork, logos and trademarks retain their respective owners' rights. They are excluded from the project's MIT and CC BY licences, as described in [LICENSING.md](../LICENSING.md). The provenance manifest identifies the original source; it is not a claim of a new licence or provider endorsement.

## Portuguese presentation

`site/locales/pt-PT.json` maps exact public source strings to Portuguese presentation text. It covers titles, descriptions, prerequisites, resources, scope, credential/credit information, recommendation explanations and displayed admission notes. The dictionary began with machine translation of public repository text, followed by terminology corrections, a title review and manual revision of the main CS50 reading path. Long-form translations have not all received an independent linguistic review.

`scripts/editorial_presentation.py` makes a deep copy for localised rendering. IDs, URLs, provider names, languages, dates, statuses, access classifications and all scores stay unchanged. Source strings themselves are the lookup keys: changed editorial text fails the build until its translation is added, rather than silently publishing an English paragraph on a Portuguese page.

When updating a course:

1. Update the canonical course/review through the normal editorial workflow.
2. Add translations for new or changed displayed strings to the dictionary. Preserve programme brands, identifiers and numerical facts; use European Portuguese.
3. Add an official image to the manifest only when its identity, source and presentation are suitable. A missing image automatically uses the editorial panel.
4. Run the normal validation commands and the presentation tests below.

The public access labels describe what the learner receives. F0/F1/F2 remain canonical filter values and can still occur in the expanded editorial rationale; they are no longer the primary catalogue labels. F3 remains ineligible for publication.

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
