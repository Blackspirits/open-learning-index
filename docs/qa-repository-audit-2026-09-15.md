# Repository and publication audit — 2026-09-15

## Scope

This audit reviews the current `main` state after the v0.10 public-experience work and the editorial-presentation/cache fixes in PRs #139–#140.

It covers:

- canonical dataset structure and publication invariants;
- language metadata, with special attention to Portuguese variants;
- EN/pt-PT presentation and translation quality;
- public-site architecture, routes and deployment;
- README/banner consistency;
- licensing and bundled visual assets;
- whether another full course re-verification is justified now.

This is **not** a new Discovery or ranking cycle.

## Repository state entering the audit

- 142 canonical courses;
- 111 active and 31 active archives;
- 75 F0 / 24 F1 / 43 F2;
- 17 `reference_verified` + 125 `phase4_admitted`;
- 19 categories;
- no open pull requests;
- issue #91 remains the maintenance control point;
- latest GitHub Pages deployment on the audited `main` revision completed successfully.

## Dataset structural result

No blocker was found in the canonical identity/score structure:

- no duplicate canonical course IDs;
- no duplicate canonical URLs;
- no duplicate title+provider pairs found in the 142-course set;
- no non-HTTPS canonical URLs found;
- no obvious affiliate/tracking parameters found in canonical URLs;
- no duplicate values inside `other_languages`;
- no course repeats its primary language inside `other_languages`;
- Quality scores continue to be reproducible from the weighted component model through repository CI.

## Portuguese language audit

The canonical publication currently contains:

- **13** courses whose primary language is explicitly `pt-PT`;
- **1** verified alternate `pt-BR` route — Google Machine Learning Crash Course;
- **3** alternate Portuguese routes where the provider currently says only “Português” / “POR”, without identifying Portugal vs Brazil.

The three unresolved records are:

| Course | Canonical language state | Primary evidence | Decision |
|---|---|---|---|
| `unity-junior-programmer` | `en` + generic `pt` alternate | https://learn.unity.com/pathway/junior-programmer | Keep `pt`; Unity lists “Português” but no regional variant |
| `coe-help-cybercrime-electronic-evidence` | `en` + generic `pt` alternate | https://www.coe.int/en/web/octopus/training | Keep `pt`; Council of Europe lists POR/Portuguese without a regional variant |
| `tghn-ich-gcp-e6-r3` | `en` + generic `pt` alternate | https://globalhealthtrainingcentre.tghn.org/ich-gcp-r3/ | Keep `pt`; TGHN lists “Português” without a regional variant |

Google explicitly labels the ML Crash Course locale **Português – Brasil**, so `pt-BR` remains verified:

- https://developers.google.com/machine-learning/crash-course?hl=pt-br

### Policy correction

A bare `pt` must never be silently displayed as Portugal or Brazil.

The publication model now treats it as an explicit unresolved state:

- primary Portuguese on a published course must be `pt-PT` or `pt-BR`;
- bare `pt` is permitted only as an alternate language when the provider itself does not identify the region;
- such a record requires `language_notes` documenting the uncertainty;
- the public UI renders it as **Portuguese (variant unspecified)** / **Português (variante não especificada)**.

This preserves evidence instead of inventing regional provenance.

## pt-PT presentation audit

The site has a substantial checked-in pt-PT presentation dictionary. Its coverage checks are strong, but completeness is not the same thing as linguistic correctness.

The audit confirmed that the Codex review findings on PR #139 were still present in `main`:

1. Quality-component **Currency** had been translated as monetary “moeda” in one rationale instead of **Atualidade**.
2. Three total-duration phrases using “24-hour” had become **“24 horas por dia”**, materially changing course workload.

Those four semantic defects are corrected in this audit and regression-tested.

### Remaining linguistic risk

The long-form dictionary began with machine translation and has not received an independent line-by-line European-Portuguese review. A second linguistic QA pass is still worthwhile, especially for:

- false friends such as “survey”;
- Brazilian-Portuguese vocabulary leaking into pt-PT;
- literal English editorial idioms such as “route”, “anchor”, “survivor” and “currency”;
- workload/duration units;
- legal, health and academic terminology.

This is a **presentation-language QA** task. It does not justify changing canonical course facts or scores.

## Banner / visual identity

The repository README banner was still based on the previous mountain concept, while the live site now uses the warm editorial-library hero introduced in PR #139.

The banner is therefore replaced with an original SVG using the current site vocabulary:

- warm ivory paper;
- deep petrol/navy text;
- muted teal;
- open books, paper and library/shelf forms;
- the live headline direction, “Learning opens new horizons.”

No third-party course/provider artwork is used in the banner.

## Public-site architecture and deployment

The architecture remains sound:

- static generated site;
- deterministic canonical JSON projection;
- EN and pt-PT route families;
- course/category canonical and hreflang output;
- content-addressed local asset revisions;
- generated-site QA before Pages deployment;
- no runtime CMS/database/account system.

The latest audited Pages run completed successfully after PR #140.

## Licensing audit

The top-level MIT licence and split-licensing documentation are internally coherent.

One **material blocker** remains in the current public presentation:

- `site/assets/course-media.json` tracks 55 locally bundled third-party course/provider images;
- it records source page/image provenance and hashes;
- it does **not** record a reuse licence, permission or rights basis for any of the 55 assets;
- `CONTRIBUTING.md` correctly says third-party artwork should not be added unless reuse rights are verified.

Source attribution is not, by itself, evidence that redistribution is permitted.

### Required gate

Until reuse rights are individually verified, the robust publication choice is to stop bundling/serving those 55 images and use the project's original editorial fallback panels instead.

If an image is later restored, its manifest record should include an explicit reuse basis, not only provenance.

## Do the 142 courses need another complete factual review now?

No.

A full second re-verification on 2026-09-15 would duplicate work performed only 1–3 days ago and would conflict with the maintenance plan's targeted cadence.

The correct immediate factual checks were the three unresolved Portuguese variants above. None can honestly be converted to pt-PT or pt-BR from current provider evidence.

The next scheduled editorial gate remains:

- **2026-09-21** — re-check `fun-hieroglyphes-egyptiens`;
- **2026-10-13** — due-soon review window begins;
- **2026-11-12** — first canonical reviews due.

## External second opinion

A second model is useful for **independent pt-PT linguistic QA** of the presentation dictionary.

It should **not** be used as the authority for course availability, price, language variant, credential or currentness. Those facts must continue to come from official provider sources and the repository evidence pipeline.

## Verdict

The data/ranking architecture remains strong and the published course set does not need an immediate wholesale re-review.

The audit finds three concrete hardening tasks:

1. make generic Portuguese uncertainty explicit — addressed here;
2. correct known pt-PT semantic translation failures — addressed here;
3. remove or rights-verify the 55 locally bundled third-party course images — **addressed by the follow-up media-rights hardening PR**: all 55 records are now unpublished/unverified and the local binary copies are removed.

With the media-rights gate closed, the project should return to issue #91 maintenance rather than reopening broad redesign or Discovery.
