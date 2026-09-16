#!/usr/bin/env python3
"""Report and enforce editorial translation coverage for presentation locales."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import build_public_site as build

ROOT = Path(__file__).resolve().parents[1]
LOCALES = ROOT / "site" / "locales"

LOCALIZED_FIELDS = {
    "review": (
        "prerequisites",
        "required_resources",
        "scope_notes",
        "credential",
        "academic_credits",
        "recommendation_rationale",
    ),
    "admission": (
        "learning_need",
        "marginal_value",
        "decision_rationale",
    ),
}


def required_editorial_strings() -> dict[str, set[str]]:
    courses = json.loads(build.COURSES.read_text(encoding="utf-8"))
    category_rows = json.loads(build.CATEGORIES.read_text(encoding="utf-8"))
    categories = {row["id"]: row for row in category_rows}
    reviews = build.load_current_records(build.REVIEWS_DIR, "reviewed_on")
    reference_reviews = build.load_current_records(
        build.REFERENCE_REVIEWS, "reviewed_on", "course_id"
    )
    admissions = build.load_current_records(build.ADMISSIONS_DIR, "decided_on")

    required: dict[str, set[str]] = {}

    def add(value: str | None, origin: str) -> None:
        if not value:
            return
        required.setdefault(value, set()).add(origin)

    for course in courses:
        if not build.is_publication_eligible(course):
            continue
        item = build.build_public_course(course, categories)
        item["editorial"] = build.editorial_projection(
            course, reviews, reference_reviews, admissions
        )

        add(item.get("title"), f'{course["id"]}.title')
        add(item.get("why_recommended"), f'{course["id"]}.why_recommended')

        for section, keys in LOCALIZED_FIELDS.items():
            block = item.get("editorial", {}).get(section, {})
            for key in keys:
                add(block.get(key), f'{course["id"]}.{section}.{key}')

    return required


def read_locale(locale: str) -> dict[str, str]:
    path = LOCALES / f"{locale}.json"
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"ERROR: locale file must be a JSON object: {path}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True)
    parser.add_argument("--enforce", action="store_true")
    parser.add_argument(
        "--write-template",
        type=Path,
        help="Write a deterministic JSON template with every required source string.",
    )
    args = parser.parse_args()

    required = required_editorial_strings()
    translations = read_locale(args.locale)

    missing = sorted(
        source
        for source in required
        if not isinstance(translations.get(source), str) or not translations[source].strip()
    )
    covered = len(required) - len(missing)
    coverage = 100.0 if not required else covered / len(required) * 100

    print(
        f"{args.locale}: {covered}/{len(required)} required editorial strings "
        f"covered ({coverage:.2f}%)."
    )

    if missing:
        print(f"Missing: {len(missing)}")
        for source in missing[:20]:
            origins = ", ".join(sorted(required[source])[:3])
            print(f"- {source[:180]} [{origins}]")
        if len(missing) > 20:
            print(f"... and {len(missing) - 20} more")

    if args.write_template:
        template = {
            source: translations.get(source, "")
            for source in sorted(required)
        }
        args.write_template.parent.mkdir(parents=True, exist_ok=True)
        args.write_template.write_text(
            json.dumps(template, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote translation template: {args.write_template}")

    if args.enforce and missing:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
