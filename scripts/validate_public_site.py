#!/usr/bin/env python3
"""Validate the generated public site as a static publication artifact."""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

BASE_URL = "https://blackspirits.github.io/open-learning-index"
BASE_PATH = "/open-learning-index/"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[tuple[str, str]] = []
        self.lang: str | None = None
        self.h1_count = 0
        self.title_depth = 0
        self.title_parts: list[str] = []
        self.canonicals: list[str] = []
        self.alternates: dict[str, str] = {}
        self.has_data_icon = False
        self.has_theme_toggle = False
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "html":
            self.lang = values.get("lang")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self.title_depth += 1
        elif tag == "a":
            href = values.get("href")
            if href:
                self.links.append(("href", href))
        elif tag in {"img", "script"}:
            src = values.get("src")
            if src:
                self.links.append(("src", src))
                if tag == "script":
                    self.scripts.append(src)
        elif tag == "link":
            href = values.get("href")
            rel = set((values.get("rel") or "").split())
            if href:
                self.links.append(("href", href))
            if "canonical" in rel and href:
                self.canonicals.append(href)
            if "alternate" in rel and href and values.get("hreflang"):
                self.alternates[values["hreflang"]] = href

        if values.get("data-icon"):
            self.has_data_icon = True
        if "data-theme-toggle" in values:
            self.has_theme_toggle = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return "".join(self.title_parts).strip()


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def resolve_internal_target(site: Path, page: Path, raw_url: str) -> Path | None:
    value = raw_url.strip()
    if not value or value.startswith("#"):
        return None

    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return None

    path = unquote(parsed.path)
    if not path:
        return None

    if path.startswith(BASE_PATH):
        target = site / path[len(BASE_PATH):]
    elif path.startswith("/"):
        target = site / path.lstrip("/")
    else:
        target = page.parent / path

    target = target.resolve()
    try:
        target.relative_to(site.resolve())
    except ValueError:
        return target

    if path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def route_to_file(site: Path, url: str) -> Path | None:
    if not url.startswith(BASE_URL):
        return None
    path = url[len(BASE_URL):].split("?", 1)[0].split("#", 1)[0]
    if path in {"", "/"}:
        return site / "index.html"
    target = site / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    return target


def expected_url_for_page(site: Path, page: Path) -> str | None:
    rel = page.relative_to(site).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel in {"404.html", "course.html"}:
        return None
    if rel.endswith("/index.html"):
        route = rel[: -len("index.html")]
        return f"{BASE_URL}/{route}"
    return None


def parse_page(path: Path) -> PageParser:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def validate_page(site: Path, page: Path, errors: list[str]) -> PageParser:
    parser = parse_page(page)
    rel = page.relative_to(site).as_posix()

    if not parser.lang:
        fail(errors, f"{rel}: missing html lang")
    if not parser.title:
        fail(errors, f"{rel}: missing title")
    if parser.h1_count != 1:
        fail(errors, f"{rel}: expected exactly one h1, found {parser.h1_count}")

    if rel.startswith("pt/") and parser.lang != "pt-PT":
        fail(errors, f"{rel}: pt route must use lang=pt-PT")
    if not rel.startswith("pt/") and rel not in {"404.html", "course.html"} and parser.lang != "en":
        fail(errors, f"{rel}: English route must use lang=en")

    expected_url = expected_url_for_page(site, page)
    if expected_url:
        if parser.canonicals != [expected_url]:
            fail(
                errors,
                f"{rel}: canonical mismatch; expected {expected_url}, found {parser.canonicals}",
            )

    if parser.has_data_icon and not any(urlsplit(src).path.endswith("icons.js") for src in parser.scripts):
        fail(errors, f"{rel}: data-icon markup requires icons.js")
    if parser.has_theme_toggle and not any(urlsplit(src).path.endswith("theme.js") for src in parser.scripts):
        fail(errors, f"{rel}: theme toggle requires theme.js")

    for attr, raw_url in parser.links:
        target = resolve_internal_target(site, page, raw_url)
        if target is None:
            continue
        try:
            target.relative_to(site.resolve())
        except ValueError:
            fail(errors, f"{rel}: {attr} escapes site root: {raw_url}")
            continue
        if not target.exists():
            fail(errors, f"{rel}: broken internal {attr}: {raw_url}")

    return parser


def validate_publication_routes(site: Path, errors: list[str]) -> None:
    catalog_path = site / "data" / "catalog.json"
    categories_path = site / "data" / "categories.json"
    meta_path = site / "data" / "meta.json"

    for path in (catalog_path, categories_path, meta_path):
        if not path.exists():
            fail(errors, f"missing generated data file: {path.relative_to(site)}")
            return

    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    categories = json.loads(categories_path.read_text(encoding="utf-8"))
    meta = json.loads(meta_path.read_text(encoding="utf-8"))

    if meta.get("published_count") != len(catalog):
        fail(errors, "data/meta.json published_count does not match catalog.json")
    if meta.get("category_count") != len(categories):
        fail(errors, "data/meta.json category_count does not match categories.json")

    for course in catalog:
        course_id = course["id"]
        for rel in (
            Path("courses") / course_id / "index.html",
            Path("pt") / "courses" / course_id / "index.html",
        ):
            if not (site / rel).exists():
                fail(errors, f"missing published course route: {rel.as_posix()}")

    for category in categories:
        category_id = category["id"]
        for rel in (
            Path("categories") / category_id / "index.html",
            Path("pt") / "categories" / category_id / "index.html",
        ):
            if not (site / rel).exists():
                fail(errors, f"missing category route: {rel.as_posix()}")

    for rel in (
        Path("categories") / "index.html",
        Path("pt") / "categories" / "index.html",
    ):
        if not (site / rel).exists():
            fail(errors, f"missing category directory: {rel.as_posix()}")

    for rel in (
        Path("methodology") / "index.html",
        Path("pt") / "methodology" / "index.html",
    ):
        if not (site / rel).exists():
            fail(errors, f"missing methodology route: {rel.as_posix()}")


def validate_locale_pairs(site: Path, pages: dict[Path, PageParser], errors: list[str]) -> None:
    for rel, parser in pages.items():
        rel_posix = rel.as_posix()
        if rel_posix.startswith("courses/") and rel_posix.endswith("/index.html"):
            pt_rel = Path("pt") / rel
            if pt_rel not in pages:
                fail(errors, f"{rel_posix}: missing pt-PT counterpart")
            expected_pt = f"{BASE_URL}/pt/{rel_posix[:-len('index.html')]}"
            if parser.alternates.get("pt-PT") != expected_pt:
                fail(errors, f"{rel_posix}: missing or incorrect pt-PT alternate")

        if rel_posix.startswith("categories/") and rel_posix.endswith("index.html"):
            pt_rel = Path("pt") / rel
            if pt_rel not in pages:
                fail(errors, f"{rel_posix}: missing pt-PT counterpart")
            expected_pt = f"{BASE_URL}/pt/{rel_posix[:-len('index.html')]}"
            if parser.alternates.get("pt-PT") != expected_pt:
                fail(errors, f"{rel_posix}: missing or incorrect pt-PT alternate")

        if rel_posix.startswith("pt/courses/") and rel_posix.endswith("/index.html"):
            en_rel = Path(*rel.parts[1:])
            expected_en = f"{BASE_URL}/{en_rel.as_posix()[:-len('index.html')]}"
            if parser.alternates.get("en") != expected_en:
                fail(errors, f"{rel_posix}: missing or incorrect English alternate")

        if rel_posix.startswith("pt/categories/") and rel_posix.endswith("index.html"):
            en_rel = Path(*rel.parts[1:])
            expected_en = f"{BASE_URL}/{en_rel.as_posix()[:-len('index.html')]}"
            if parser.alternates.get("en") != expected_en:
                fail(errors, f"{rel_posix}: missing or incorrect English alternate")

        if rel_posix == "methodology/index.html":
            expected_pt = f"{BASE_URL}/pt/methodology/"
            if parser.alternates.get("pt-PT") != expected_pt:
                fail(errors, f"{rel_posix}: missing or incorrect pt-PT alternate")

        if rel_posix == "pt/methodology/index.html":
            expected_en = f"{BASE_URL}/methodology/"
            if parser.alternates.get("en") != expected_en:
                fail(errors, f"{rel_posix}: missing or incorrect English alternate")


def validate_sitemap(site: Path, pages: dict[Path, PageParser], errors: list[str]) -> None:
    sitemap_path = site / "sitemap.xml"
    if not sitemap_path.exists():
        fail(errors, "missing sitemap.xml")
        return

    root = ET.fromstring(sitemap_path.read_text(encoding="utf-8"))
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    urls = [node.text or "" for node in root.findall("sm:url/sm:loc", ns)]
    sitemap_set = set(urls)

    for url in urls:
        target = route_to_file(site, url)
        if target is None or not target.exists():
            fail(errors, f"sitemap points to missing route: {url}")

    for rel, parser in pages.items():
        if rel.as_posix() in {"404.html", "course.html"}:
            continue
        if parser.canonicals:
            canonical = parser.canonicals[0]
            if canonical.startswith(BASE_URL) and canonical not in sitemap_set:
                fail(errors, f"{rel.as_posix()}: canonical route missing from sitemap")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path, help="Generated public-site directory")
    args = parser.parse_args()

    site = args.site.resolve()
    if not site.exists():
        print(f"ERROR: site directory does not exist: {site}", file=sys.stderr)
        return 1

    errors: list[str] = []
    html_files = sorted(site.rglob("*.html"))
    if not html_files:
        print("ERROR: no HTML files found in generated site", file=sys.stderr)
        return 1

    pages: dict[Path, PageParser] = {}
    for page in html_files:
        parsed = validate_page(site, page, errors)
        pages[page.relative_to(site)] = parsed

    validate_publication_routes(site, errors)
    validate_locale_pairs(site, pages, errors)
    validate_sitemap(site, pages, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Public-site QA failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(f"OK: public-site QA validated {len(html_files)} HTML pages and internal routes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
