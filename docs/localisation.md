# Localisation policy

The Open Learning Index treats localisation as an editorial surface, not as a cosmetic language switch.

## Current public locales

- `en` — source/public default;
- `pt-PT` — complete presentation localisation with checked-in editorial translations.

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
    }
  }
}
```

The legacy `presentation_pt` projection is retained temporarily for backwards compatibility and should be removed only after all public consumers have migrated.

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
```

For a future locale, a deterministic source template can be generated with:

```bash
python scripts/check_locale_coverage.py --locale es --write-template /tmp/es.json
```

The template contains only strings required by the **current public catalogue**, rather than every historical string ever seen in the repository.

## Planned order

The preferred next locale is **Spanish (`es`)**, followed by **French (`fr`)** after Spanish has passed full coverage and linguistic QA.

This ordering is not a commitment to publish incomplete translations. Quality remains more important than locale count.

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
