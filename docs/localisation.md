# Localisation policy

The Open Learning Index treats localisation as an editorial surface, not as a cosmetic language switch.

## Current public locales

- `en` — source/public default;
- `pt-PT` — complete European-Portuguese presentation localisation with checked-in editorial translations;
- `es` — complete Spanish presentation localisation with checked-in editorial translations;
- `fr` — complete French presentation localisation with checked-in editorial translations.

## Architecture

Canonical course data and review ledgers remain source-language records. Public translations live only in the presentation layer.

`scripts/editorial_presentation.py` provides locale-generic translation helpers and `localize_course(course, locale=...)`.

The generated public catalogue exposes translations as:

```json
{
  "presentations": {
    "pt-PT": {
      "title": "...",
      "description": "..."
    },
    "es": {
      "title": "...",
      "description": "..."
    },
    "fr": {
      "title": "...",
      "description": "..."
    }
  }
}
```

The legacy `presentation_pt` projection is retained temporarily for backwards compatibility and should be removed only after all public consumers have migrated.

`scripts/build_public_site_public.py` is the publication configuration layer for the complete reviewed locale set. It reuses the stable deterministic builder and enables a locale only after its dictionary has passed the publication gate. `scripts/validate_public_site_public.py` extends generated-site QA to the same public-locale matrix.

## Publication gate for a new locale

A new language must **not** receive public routes until all of the following are true:

1. interface/navigation copy is complete;
2. category, level, language and access labels are complete;
3. methodology/trust copy is complete;
4. every learner-facing editorial source string used by currently published courses has a reviewed translation;
5. no silent English fallback is used for a page presented as fully localised;
6. locale-specific linguistic QA passes;
7. generated route, canonical, hreflang, sitemap and runtime validation passes.

Use:

```bash
python scripts/check_locale_coverage.py --locale pt-PT --enforce
python scripts/check_locale_coverage.py --locale es --enforce
python scripts/check_locale_coverage.py --locale fr --enforce
```

For a future locale, a deterministic source template can be generated with:

```bash
python scripts/check_locale_coverage.py --locale <locale> --write-template /tmp/<locale>.json
```

The template contains only strings required by the **current public catalogue**, rather than every historical string ever seen in the repository.

## Planned order

English, European Portuguese, Spanish and French are public. No fifth locale should be added merely to increase language count. A future locale must have a clear accessibility/coverage benefit and pass the same complete editorial and generated-site gates before publication.

Quality remains more important than locale count.

## Translation workflow

Machine translation may be used to create a first draft, but it is not sufficient for publication by itself.

Terminology that must remain consistent includes:

- Quality / Recommendation distinction;
- F0 / F1 / F2 / F3 access taxonomy;
- credential vs academic credit;
- Deep Review / admission terminology where exposed;
- provider and course proper names;
- language variants and regional labels.

A translation service with glossary support is preferable for producing draft files because terminology can be controlled, but all public locale files remain checked into the repository and subject to repository QA.

### Large locale dictionaries

A locale dictionary may be one `site/locales/<locale>.json` file or deterministic non-overlapping fragments in `site/locales/<locale>/*.json`. Fragment filenames sort lexically and duplicate source keys are a hard error. New large locales should use fragments so translation review can be incremental without enabling partial public routes.
