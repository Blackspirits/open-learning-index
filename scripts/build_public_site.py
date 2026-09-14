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
REVIEWS_DIR = ROOT / "data" / "reviews"
ADMISSIONS_DIR = ROOT / "data" / "admissions"
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


def load_current_records(directory: Path, date_field: str) -> dict:
    """Index the latest current ledger record for each candidate ID."""
    index = {}
    for path in sorted(directory.glob("*.json")):
        rows = json.loads(path.read_text(encoding="utf-8"))
        for row in rows:
            if row.get("is_current") is False:
                continue
            candidate_id = row.get("candidate_id")
            if not candidate_id:
                continue
            existing = index.get(candidate_id)
            if existing is None or row.get(date_field, "") >= existing.get(date_field, ""):
                index[candidate_id] = row
    return index


def editorial_projection(course: dict, reviews: dict, admissions: dict) -> dict:
    review = reviews.get(course["id"])
    admission = admissions.get(course["id"])

    projected = {
        "review_status": course.get("review_status"),
        "has_current_deep_review": bool(review),
        "has_current_admission": bool(admission),
    }

    if review:
        projected["review"] = {
            "prerequisites": review.get("prerequisites"),
            "required_resources": review.get("required_resources"),
            "scope_notes": review.get("scope_notes"),
            "credential": review.get("credential"),
            "academic_credits": review.get("academic_credits"),
            "recommendation_rationale": review.get("recommendation_rationale"),
            "component_evidence": review.get("component_evidence") or {},
            "comparators": review.get("comparators") or [],
            "evidence": review.get("evidence") or [],
        }

    if admission:
        projected["admission"] = {
            "learning_need": admission.get("learning_need"),
            "decision_rationale": admission.get("decision_rationale"),
            "marginal_value": admission.get("marginal_value"),
            "comparison_set": admission.get("comparison_set") or [],
            "incumbent_ids": admission.get("incumbent_ids") or [],
            "complements_course_ids": admission.get("complements_course_ids") or [],
            "outcompeted_by_ids": admission.get("outcompeted_by_ids") or [],
        }

    if course.get("review_status") == "reference_verified" and not review:
        projected["reference_note"] = (
            "This pre-existing reference course was retained through the v0.5 "
            "reference-fixture reconciliation and publication QA. It is scheduled "
            "for one-time recalibration against the current Deep Review / Phase 4 rubric."
        )

    return projected


def build(output: Path) -> None:
    courses = json.loads(COURSES.read_text(encoding="utf-8"))
    category_rows = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    categories = {row["id"]: row for row in category_rows}
    reviews = load_current_records(REVIEWS_DIR, "reviewed_on")
    admissions = load_current_records(ADMISSIONS_DIR, "decided_on")

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(SITE_SOURCE, output)

    public_courses = []
    for course in courses:
        if not is_publication_eligible(course):
            continue
        item = build_public_course(course, categories)
        item["editorial"] = editorial_projection(course, reviews, admissions)
        public_courses.append(item)

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
