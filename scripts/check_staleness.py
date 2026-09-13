#!/usr/bin/env python3
import argparse
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "data/courses.json"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Report canonical-course review freshness and optionally enforce the maintenance SLA."
    )
    parser.add_argument(
        "--enforce-priority",
        action="store_true",
        help="Exit non-zero when any course is more than 30 days overdue or beyond 2x its review interval.",
    )
    parser.add_argument(
        "--as-of",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="Evaluate freshness on a specific date (useful for deterministic audits/tests).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    today = args.as_of
    courses = json.loads(COURSES.read_text(encoding="utf-8"))

    current = []
    due_soon = []
    overdue_warning = []
    priority = []
    critical = []

    for course in courses:
        next_review = date.fromisoformat(course["next_review"])
        last_verified = date.fromisoformat(course["last_verified"])
        interval = course["review_interval_days"]
        days_until_review = (next_review - today).days
        days_since_verified = (today - last_verified).days

        record = {
            "course": course,
            "days_until_review": days_until_review,
            "days_since_verified": days_since_verified,
        }

        if days_since_verified > 2 * interval:
            critical.append(record)
        elif days_until_review < -30:
            priority.append(record)
        elif days_until_review < 0:
            overdue_warning.append(record)
        elif days_until_review <= 30:
            due_soon.append(record)
        else:
            current.append(record)

    print(f"Maintenance review status as of {today.isoformat()}:")
    print(f"- current (>30 days until review): {len(current)}")
    print(f"- due within 30 days: {len(due_soon)}")
    print(f"- overdue by <=30 days: {len(overdue_warning)}")
    print(f"- priority overdue (>30 days): {len(priority)}")
    print(f"- critical (>2x review interval since verification): {len(critical)}")

    if due_soon:
        print("\nDue within 30 days:")
        for item in sorted(
            due_soon,
            key=lambda x: (x["days_until_review"], x["course"]["id"]),
        ):
            course = item["course"]
            print(
                f'- {course["id"]}: due {course["next_review"]} '
                f'({item["days_until_review"]} day(s)); interval {course["review_interval_days"]}d'
            )

    if overdue_warning:
        print("\nStale warnings (<=30 days overdue):")
        for item in sorted(
            overdue_warning,
            key=lambda x: (x["days_until_review"], x["course"]["id"]),
        ):
            course = item["course"]
            print(
                f'- {course["id"]}: {-item["days_until_review"]} day(s) overdue; '
                f'last verified {course["last_verified"]}'
            )

    if priority:
        print("\nPriority re-reviews (>30 days overdue):")
        for item in sorted(
            priority,
            key=lambda x: (x["days_until_review"], x["course"]["id"]),
        ):
            course = item["course"]
            print(
                f'- {course["id"]}: {-item["days_until_review"]} day(s) overdue; '
                f'last verified {course["last_verified"]}'
            )

    if critical:
        print("\nCritical publication-ineligible records (>2x review interval):")
        for item in sorted(
            critical,
            key=lambda x: (-x["days_since_verified"], x["course"]["id"]),
        ):
            course = item["course"]
            print(
                f'- {course["id"]}: {item["days_since_verified"]} day(s) since verification; '
                f'interval {course["review_interval_days"]}d; next review {course["next_review"]}'
            )

    if args.enforce_priority and (priority or critical):
        print(
            "\nERROR: maintenance SLA breached. Re-verify priority/critical records before the scheduled gate can pass."
        )
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
