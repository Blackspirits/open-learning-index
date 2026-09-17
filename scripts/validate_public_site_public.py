#!/usr/bin/env python3
"""Validate the generated public site with every published locale enabled."""

from __future__ import annotations

import json
from pathlib import Path

import validate_public_site as validate


validate.PUBLIC_LOCALES = {
    "en": "",
    "pt-PT": "pt",
    "es": "es",
    "fr": "fr",
}

_original_validate_page = validate.validate_page
_original_runtime_contract = validate.validate_catalogue_runtime_contract


def validate_page_with_french(site: Path, page: Path, errors: list[str]):
    local_errors: list[str] = []
    parsed = _original_validate_page(site, page, local_errors)
    rel = page.relative_to(site).as_posix()
    if rel.startswith("fr/") and parsed.lang == "fr":
        local_errors = [
            error
            for error in local_errors
            if error != f"{rel}: route must use lang=en"
        ]
    errors.extend(local_errors)
    return parsed


def validate_runtime_with_french(site: Path, errors: list[str]) -> None:
    _original_runtime_contract(site, errors)
    catalog_path = site / "data" / "catalog.json"
    if catalog_path.exists():
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        missing = [
            course.get("id", "<unknown>")
            for course in catalog
            if not ((course.get("presentations") or {}).get("fr") or {}).get("description")
        ]
        if missing:
            validate.fail(
                errors,
                "catalogue runtime contract: missing presentations.fr.description for "
                + ", ".join(missing[:10]),
            )
    app_path = site / "app-fr.js"
    if not app_path.exists():
        validate.fail(errors, "catalogue runtime contract: missing app-fr.js")
    else:
        source = app_path.read_text(encoding="utf-8")
        if "course.presentations?.fr" not in source:
            validate.fail(
                errors,
                "catalogue runtime contract: app-fr.js does not consume presentations.fr",
            )


validate.validate_page = validate_page_with_french
validate.validate_catalogue_runtime_contract = validate_runtime_with_french


if __name__ == "__main__":
    raise SystemExit(validate.main())
