#!/usr/bin/env python3
"""Build the static Open Learning Index public catalogue from canonical data."""

import argparse
import json
import shutil
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "data" / "courses.json"
CATEGORIES = ROOT / "data" / "categories.json"
SITE_SOURCE = ROOT / "site"
DEFAULT_OUTPUT = ROOT / "_site"

ACCESS = {
    "F0_FULL_CREDENTIAL": {
        "short": "F0",
        "label": "Full course + free credential",
        "description": "Complete learning path with a free provider completion credential.",
    },
    "F1_FULL_ASSESSMENTS": {
        "short": "F1",
        "label": "Full assessed learning path",
        "description": "Complete learning path with meaningful free assessment, but no free formal credential.",
    },
    "F2_CONTENT_ONLY": {
        "short": "F2",
        "label": "Full teaching content",
        "description": "Substantial complete teaching content, but no free formal completion path.",
    },
}


def score_tier(score: float) -> str:
    if score >= 9.5:
        return "S+"
    if score >= 9.0:
        return "S"
    if score >= 8.5:
        return "A+"
    return "A"


def normalize_search_text(value: str) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.lower().split())


def is_publication_eligible(course: dict) -> bool:
    return (
        course.get("free_access") in ACCESS
        and course.get("status") in {"active", "active_archive"}
    )


def build_public_course(course: dict, categories: dict) -> dict:
    item = dict(course)
    item["category_name"] = categories[course["category"]]["name"]
    item["category_freshness"] = categories[course["category"]]["freshness"]
    item["quality_tier"] = score_tier(float(course["quality_score"]))
    item["recommendation_tier"] = score_tier(float(course["recommendation_score"]))

    access = ACCESS[course["free_access"]]
    item["access_short"] = access["short"]
    item["access_label"] = access["label"]
    item["access_description"] = access["description"]
    item["has_free_credential"] = course["free_access"] == "F0_FULL_CREDENTIAL"
    item["has_free_academic_credit"] = str(course.get("academic_credits", "")).startswith("free_")

    searchable = [
        course.get("title", ""),
        course.get("provider", ""),
        item["category_name"],
        course.get("level", ""),
        course.get("primary_language", ""),
        " ".join(course.get("other_languages", [])),
        course.get("why_recommended", ""),
    ]
    item["search_text"] = normalize_search_text(" ".join(searchable))
    return item


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build(output: Path) -> None:
    courses = json.loads(COURSES.read_text(encoding="utf-8"))
    category_rows = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    categories = {row["id"]: row for row in category_rows}

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(SITE_SOURCE, output)

    public_courses = [
        build_public_course(course, categories)
        for course in courses
        if is_publication_eligible(course)
    ]

    ids = [course["id"] for course in public_courses]
    if len(ids) != len(set(ids)):
        raise SystemExit("ERROR: duplicate course id in public build")

    expected_ids = {
        course["id"] for course in courses if is_publication_eligible(course)
    }
    if set(ids) != expected_ids:
        missing = sorted(expected_ids - set(ids))
        extra = sorted(set(ids) - expected_ids)
        raise SystemExit(
            f"ERROR: public build mismatch; missing={missing}, extra={extra}"
        )

    if any(course["free_access"] == "F3_PARTIAL_PREVIEW" for course in public_courses):
        raise SystemExit("ERROR: F3 course leaked into public catalogue")

    access_counts = Counter(course["access_short"] for course in public_courses)
    language_counts = Counter(course["primary_language"] for course in public_courses)

    meta = {
        "canonical_count": len(courses),
        "published_count": len(public_courses),
        "category_count": len(category_rows),
        "access_counts": dict(sorted(access_counts.items())),
        "language_counts": dict(sorted(language_counts.items())),
        "source_files": ["data/courses.json", "data/categories.json"],
    }

    write_json(output / "data" / "catalog.json", public_courses)
    write_json(output / "data" / "categories.json", category_rows)
    write_json(output / "data" / "meta.json", meta)

    required = [
        output / "index.html",
        output / "app.js",
        output / "course.html",
        output / "course.js",
        output / "styles.css",
        output / "data" / "catalog.json",
        output / "data" / "meta.json",
    ]
    missing_files = [str(path.relative_to(output)) for path in required if not path.exists()]
    if missing_files:
        raise SystemExit(f"ERROR: public build missing required files: {missing_files}")

    try:
        output_label = output.relative_to(ROOT)
    except ValueError:
        output_label = output

    print(
        f"Built {len(public_courses)} public courses from {len(courses)} canonical records "
        f"across {len(category_rows)} categories into {output_label}."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Build directory (default: _site)",
    )
    args = parser.parse_args()
    build(args.output.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
