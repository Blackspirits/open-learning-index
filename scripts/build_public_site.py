#!/usr/bin/env python3
"""Build the static Open Learning Index public catalogue from canonical data."""

import argparse
import json
import shutil
import unicodedata
from collections import Counter
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "data" / "courses.json"
CATEGORIES = ROOT / "data" / "categories.json"
REVIEWS_DIR = ROOT / "data" / "reviews"
REFERENCE_REVIEWS = ROOT / "data" / "reference-reviews.json"
ADMISSIONS_DIR = ROOT / "data" / "admissions"
SITE_SOURCE = ROOT / "site"
DEFAULT_OUTPUT = ROOT / "_site"
BASE_URL = "https://blackspirits.github.io/open-learning-index"

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

LANGUAGE_LABELS = {
    "ar": "Arabic",
    "az": "Azerbaijani",
    "bg": "Bulgarian",
    "cs": "Czech",
    "de": "German",
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hy": "Armenian",
    "it": "Italian",
    "ja": "Japanese",
    "ka": "Georgian",
    "ko": "Korean",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "pt-BR": "Português (Brasil)",
    "pt-PT": "Português (Portugal)",
    "ro": "Romanian",
    "ru": "Russian",
    "sk": "Slovak",
    "tr": "Turkish",
    "uk": "Ukrainian",
    "vi": "Vietnamese",
    "zh": "Chinese",
}

CATEGORY_SEARCH_ALIASES = {
    "ai-data": "artificial intelligence",
    "computer-science": "cs coding programming",
    "cybersecurity-it": "cyber security information security infosec",
    "math-statistics": "math maths stats",
    "project-product-leadership": "project management product management pm",
}

CONTENT_SEARCH_ALIASES = {
    "machine learning": "ml",
    "javascript": "js",
    "user experience": "ux",
    "user interface": "ui",
    "search engine optimization": "seo",
    "search engine optimisation": "seo",
}

CREDENTIAL_LABELS = {
    "free_provider_certificate": "Free provider completion certificate",
    "free_statement_of_participation": "Free statement of participation",
    "academic_completion_route": "Academic completion route",
    "paid_verified_certificate": "Paid verified certificate",
    "none": "No free completion credential",
}

CREDIT_LABELS = {
    "none": "No academic credit",
    "none_by_default": "No academic credit by default",
    "optional_paid_or_external": "Optional paid or external credit route",
    "free_ects_available": "Free ECTS available",
    "free_ects_available_subject_to_rules": "Free ECTS available subject to eligibility rules",
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
    search_base = normalize_search_text(" ".join(searchable))
    aliases = [CATEGORY_SEARCH_ALIASES.get(course["category"], "")]
    aliases.extend(
        alias
        for phrase, alias in CONTENT_SEARCH_ALIASES.items()
        if phrase in search_base
    )
    item["search_text"] = normalize_search_text(f"{search_base} {' '.join(aliases)}")
    return item


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_current_records(source: Path, date_field: str, id_field: str = "candidate_id") -> dict:
    """Index the latest current ledger record for each subject ID."""
    index = {}
    paths = sorted(source.glob("*.json")) if source.is_dir() else ([source] if source.exists() else [])
    for path in paths:
        rows = json.loads(path.read_text(encoding="utf-8"))
        for row in rows:
            if row.get("is_current") is False:
                continue
            subject_id = row.get(id_field)
            if not subject_id:
                continue
            existing = index.get(subject_id)
            if existing is None or row.get(date_field, "") >= existing.get(date_field, ""):
                index[subject_id] = row
    return index


def editorial_projection(course: dict, reviews: dict, reference_reviews: dict, admissions: dict) -> dict:
    deep_review = reviews.get(course["id"])
    reference_review = reference_reviews.get(course["id"])
    review = deep_review or reference_review
    admission = admissions.get(course["id"])

    projected = {
        "review_status": course.get("review_status"),
        "has_current_deep_review": bool(deep_review),
        "has_current_reference_review": bool(reference_review),
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

    if course.get("review_status") == "reference_verified":
        if reference_review:
            projected["reference_note"] = (
                "This pre-existing reference course was retained through the v0.5 "
                "reference-fixture reconciliation and was recalibrated in v0.8 against "
                "the current evidence and scoring rubric without rewriting its pipeline history."
            )
        else:
            projected["reference_note"] = (
                "This pre-existing reference course was retained through the v0.5 "
                "reference-fixture reconciliation and publication QA. It is scheduled "
                "for one-time recalibration against the current Deep Review / Phase 4 rubric."
            )

    return projected


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def label_level(value: str) -> str:
    return " ".join(part.capitalize() for part in str(value or "").split("_"))


def label_language(value: str) -> str:
    return LANGUAGE_LABELS.get(value, value)


def readable_id(value: str) -> str:
    return " ".join(part.capitalize() for part in str(value or "").split("-"))


def static_score(label: str, score, tier: str) -> str:
    return (
        '<div class="score">'
        f'<span>{escape(label)}</span><strong>{float(score):.1f}</strong>'
        f'<small>{escape(tier)}</small></div>'
    )


def static_fact(label: str, value: str) -> str:
    return f"<div><dt>{escape(label)}</dt><dd>{escape(str(value))}</dd></div>"


def provider_initials(value: str) -> str:
    words = [
        "".join(ch for ch in word if ch.isalnum())
        for word in str(value or "").replace("/", " ").split()
    ]
    words = [word for word in words if word]
    if not words:
        return "OLI"
    if len(words) == 1:
        return words[0][:3].upper()
    return (words[0][0] + words[1][0]).upper()


def static_tag(value: str, extra: str = "") -> str:
    cls = f"mini-tag {extra}".strip()
    return f'<span class="{cls}">{escape(value)}</span>'


def static_catalogue_card(course: dict, href_prefix: str = "../") -> str:
    archive = (
        static_tag("Archived", "tag-archive")
        if course["status"] == "active_archive"
        else ""
    )
    return (
        '<article class="catalogue-card">'
        '<div class="catalogue-card-head">'
        f'<span class="score-pill">{float(course["recommendation_score"]):.1f}</span>'
        '<span class="bookmark" aria-hidden="true">♡</span></div>'
        f'<div class="provider-mark large" aria-hidden="true">{escape(provider_initials(course["provider"]))}</div>'
        f'<h3><a href="{href_prefix}courses/{escape(course["id"])}/">{escape(course["title"])}</a></h3>'
        f'<p class="provider">{escape(course["provider"])}</p>'
        '<div class="card-spacer"></div><div class="mini-tags">'
        f'{static_tag(course["category_name"], "tag-category")}'
        f'{static_tag(label_language(course["primary_language"]))}'
        f'{static_tag(label_level(course["level"]))}'
        f'{archive}</div>'
        '<div class="access-line">'
        f'<strong>{escape(course["access_short"])}</strong>'
        f'<span>{escape(course["access_label"])}</span></div>'
        '</article>'
    )


def render_static_course(course: dict, course_by_id: dict) -> str:
    editorial = course.get("editorial") or {}
    review = editorial.get("review") or {}
    admission = editorial.get("admission") or {}
    url = f"{BASE_URL}/courses/{course['id']}/"
    description = course.get("why_recommended", "")
    languages = " · ".join(
        label_language(code)
        for code in [course["primary_language"], *course.get("other_languages", [])]
    )
    archived = course["status"] == "active_archive"
    status = "Archived but still available" if archived else "Active"
    certificate = review.get("credential") or CREDENTIAL_LABELS.get(
        course.get("certificate"), readable_id(course.get("certificate"))
    )
    credit = review.get("academic_credits") or CREDIT_LABELS.get(
        course.get("academic_credits"), readable_id(course.get("academic_credits"))
    )

    comparison_ids = []
    for item in [*(admission.get("comparison_set") or []), *(review.get("comparators") or [])]:
        if item and item != course["id"] and item not in comparison_ids:
            comparison_ids.append(item)

    related_courses = []
    for item in comparison_ids:
        compared = course_by_id.get(item)
        if compared and compared not in related_courses:
            related_courses.append(compared)
        if len(related_courses) >= 2:
            break
    if len(related_courses) < 2:
        same_category = sorted(
            (
                item for item in course_by_id.values()
                if item["id"] != course["id"] and item["category"] == course["category"]
            ),
            key=lambda item: (
                -float(item["recommendation_score"]),
                -float(item["quality_score"]),
                item["title"],
            ),
        )
        for item in same_category:
            if item not in related_courses:
                related_courses.append(item)
            if len(related_courses) >= 2:
                break

    related_html = "".join(
        '<a class="related-course" href="../../courses/'
        + escape(item["id"])
        + '/"><span class="related-mark" aria-hidden="true">'
        + escape(provider_initials(item["provider"]))
        + '</span><span><strong>'
        + escape(item["title"])
        + '</strong><small>'
        + escape(item["provider"])
        + '</small></span><span class="related-score">'
        + f'{float(item["recommendation_score"]):.1f}'
        + '</span></a>'
        for item in related_courses
    )

    component_evidence = review.get("component_evidence") or {}
    components = "".join(
        '<div class="component-item">'
        f'<span>{escape(key.capitalize())}</span>'
        f'<div class="component-meter" aria-hidden="true"><i style="width:{float(value) * 10}%"></i></div>'
        f'<strong>{float(value):.1f}</strong></div>'
        for key, value in course["quality_components"].items()
    )

    evidence_urls = []
    for evidence_url in [*(review.get("evidence") or []), *(course.get("evidence") or [])]:
        if evidence_url not in evidence_urls:
            evidence_urls.append(evidence_url)
    evidence_items = []
    for index, evidence_url in enumerate(evidence_urls, 1):
        try:
            host = evidence_url.split("/")[2].removeprefix("www.")
        except IndexError:
            host = "source"
        evidence_items.append(
            f'<li><a href="{escape(evidence_url)}" target="_blank" rel="noopener noreferrer">'
            f'{escape(host)} · source {index} ↗</a></li>'
        )

    before_parts = []
    if review.get("prerequisites"):
        before_parts.append(
            f'<h3>Prerequisites</h3><p>{escape(review["prerequisites"])}</p>'
        )
    if review.get("required_resources"):
        before_parts.append(
            f'<h3>Required resources</h3><p>{escape(review["required_resources"])}</p>'
        )
    if review.get("scope_notes"):
        before_parts.append(
            f'<h3>Scope</h3><p>{escape(review["scope_notes"])}</p>'
        )
    before_html = "".join(before_parts) or "<p>No additional preparation requirements are documented.</p>"

    score_parts = []
    if review.get("recommendation_rationale"):
        score_parts.append(
            f'<h3>Recommendation rationale</h3><p>{escape(review["recommendation_rationale"])}</p>'
        )
    if admission.get("learning_need"):
        score_parts.append(
            f'<h3>Learning need</h3><p>{escape(admission["learning_need"])}</p>'
        )
    if admission.get("marginal_value"):
        score_parts.append(
            f'<h3>Why it adds value</h3><p>{escape(admission["marginal_value"])}</p>'
        )
    if admission.get("decision_rationale"):
        score_parts.append(
            '<details class="editorial-details"><summary>Admission decision rationale</summary>'
            f'<p>{escape(admission["decision_rationale"])}</p></details>'
        )

    comparisons = []
    for item in comparison_ids:
        compared = course_by_id.get(item)
        if compared:
            comparisons.append(
                f'<li><a href="../../courses/{escape(item)}/">{escape(compared["title"])}</a></li>'
            )
        else:
            comparisons.append(f'<li>{escape(readable_id(item))}</li>')

    banner_title = "This course is archived" if archived else "This course is active"
    banner_copy = (
        "The course is no longer actively running. Substantial teaching materials may still remain available for reference."
        if archived
        else "The canonical route is currently active and has been checked against the published evidence."
    )
    banner_button = "View archived materials →" if archived else "Open official course →"

    schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Course",
            "name": course["title"],
            "description": description,
            "url": url,
            "sameAs": course["url"],
            "isAccessibleForFree": True,
            "inLanguage": [course["primary_language"], *course.get("other_languages", [])],
            "educationalLevel": label_level(course["level"]),
            "provider": {"@type": "Organization", "name": course["provider"]},
        },
        ensure_ascii=False,
    ).replace("</", "<\/")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{escape(url, quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(course['title'], quote=True)} · Open Learning Index">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(url, quote=True)}">
  <title>{escape(course['title'])} · Open Learning Index</title>
  <link rel="stylesheet" href="../../styles.css">
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <a class="skip-link" href="#course-detail">Skip to course details</a>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="../../" aria-label="Open Learning Index home">
        <span class="brand-symbol" aria-hidden="true">↟</span><span>Open Learning Index</span>
      </a>
      <nav class="main-nav" aria-label="Primary navigation">
        <a href="../../courses/">Courses</a>
        <a href="../../#categories">Categories</a>
        <a href="../../#about">About</a>
        <a href="../../#how-it-works">How it works</a>
      </nav>
      <div class="nav-actions"><a class="icon-link" href="../../courses/" aria-label="Search courses">⌕</a><span class="language-switch">◎ EN</span></div>
    </div>
  </header>

  <main id="course-detail" class="shell course-page">
    <nav class="course-breadcrumbs" aria-label="Breadcrumb">
      <a href="../../">Home</a><span>›</span>
      <a href="../../categories/{escape(course["category"])}/">{escape(course["category_name"])}</a><span>›</span>
      <span>{escape(course["title"])}</span>
    </nav>

    <section class="course-title-grid">
      <div class="course-heading-main">
        <h1>{escape(course["title"])}</h1>
        <p class="course-provider-line">{escape(course["provider"])}</p>
        <div class="course-meta-tags">
          {static_tag(course["category_name"], "tag-category")}
          {static_tag(label_language(course["primary_language"]))}
          {static_tag(label_level(course["level"]))}
          {static_tag("Archived" if archived else "Active", "tag-archive" if archived else "")}
        </div>
      </div>
      <aside class="course-score-card" aria-label="Overall recommendation">
        <span>Overall recommendation</span>
        <div class="course-score-main"><strong>{float(course["recommendation_score"]):.1f}</strong><small>/ 10</small></div>
        <div class="quality-line"><span>Quality</span><strong>{float(course["quality_score"]):.1f}</strong></div>
        <div class="score-meter" aria-hidden="true"><i style="width:{float(course["quality_score"]) * 10}%"></i></div>
      </aside>
    </section>

    <section class="status-banner" aria-label="Course status">
      <span class="status-banner-icon" aria-hidden="true">▤</span>
      <div><strong>{escape(banner_title)}</strong><small>{escape(banner_copy)}</small></div>
      <a href="{escape(course["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(banner_button)}</a>
    </section>

    <nav class="course-tabs" aria-label="Course page sections">
      <a href="#overview">Overview</a>
      <a href="#details">Details</a>
      <a href="#quality">Quality</a>
      <a href="#evidence">Evidence</a>
      <a href="#alternatives">Alternatives</a>
    </nav>

    <div class="course-layout">
      <div class="course-content">
        <section id="overview" class="content-section">
          <h2>About this course</h2>
          <p>{escape(description)}</p>
          {f'<p>{escape(review["scope_notes"])}</p>' if review.get("scope_notes") else ""}
        </section>

        <section id="details" class="content-section">
          <h2>Before you start</h2>
          {before_html}
          <h3>Course materials</h3>
          <a class="course-materials-link" href="{escape(course["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(banner_button)}</a>
        </section>

        <section class="content-section">
          <h2>What is free</h2>
          <p><strong>{escape(course["access_short"])} · {escape(course["access_label"])}</strong> — {escape(course["access_description"])}</p>
          <p><strong>Certificate:</strong> {escape(certificate)}</p>
          <p><strong>Academic credit:</strong> {escape(credit)}</p>
        </section>

        <section id="quality" class="content-section">
          <h2>Quality review</h2>
          <div class="quality-panel"><div class="component-grid">{components}</div></div>
          {"".join(score_parts)}
        </section>

        <section id="evidence" class="content-section">
          <h2>Evidence and verification</h2>
          <p>Last checked: <strong>{escape(course["last_verified"])}</strong> · Next scheduled review: <strong>{escape(course["next_review"])}</strong>.</p>
          <ul class="evidence-list">{"".join(evidence_items)}</ul>
        </section>

        <section id="alternatives" class="content-section">
          <h2>Compared against</h2>
          {f'<ul class="comparison-list">{"".join(comparisons)}</ul>' if comparisons else '<p>No direct comparator is recorded for this course.</p>'}
        </section>
      </div>

      <aside class="course-sidebar">
        <section class="sidebar-card">
          <h2>Course at a glance</h2>
          <dl class="glance-list">
            <div><span class="glance-icon" aria-hidden="true">⌂</span><dt>Provider</dt><dd>{escape(course["provider"])}</dd></div>
            <div><span class="glance-icon" aria-hidden="true">◎</span><dt>Language</dt><dd>{escape(languages)}</dd></div>
            <div><span class="glance-icon" aria-hidden="true">▥</span><dt>Level</dt><dd>{escape(label_level(course["level"]))}</dd></div>
            <div><span class="glance-icon" aria-hidden="true">◷</span><dt>Status</dt><dd>{escape(status)}</dd></div>
            <div><span class="glance-icon" aria-hidden="true">⌘</span><dt>Access</dt><dd>{escape(course["access_short"])} · free</dd></div>
          </dl>
        </section>

        <section class="sidebar-card">
          <h2>Related courses</h2>
          <div class="related-list">{related_html or '<p class="muted">No related course is currently linked.</p>'}</div>
          <p style="margin:12px 0 0"><a href="../../categories/{escape(course["category"])}/">View more in {escape(course["category_name"])} →</a></p>
        </section>
      </aside>
    </div>
  </main>

  <footer class="site-footer"><div class="shell footer-inner">
    <div><strong>Open Learning Index</strong><p>Source data and methodology are public and auditable.</p></div>
    <div class="footer-links"><a href="../../courses/">Courses</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a></div>
  </div></footer>
</body>
</html>
"""


def render_static_category(category: dict, courses: list[dict]) -> str:
    url = f"{BASE_URL}/categories/{category['id']}/"
    rows = sorted(
        (course for course in courses if course["category"] == category["id"]),
        key=lambda item: (
            -float(item["recommendation_score"]),
            -float(item["quality_score"]),
            item["title"],
        ),
    )
    cards = "".join(static_catalogue_card(course, "../../") for course in rows)
    description = f"Curated free courses in {category['name']} from the Open Learning Index."
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{escape(url, quote=True)}">
  <meta property="og:title" content="{escape(category['name'], quote=True)} · Open Learning Index">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(url, quote=True)}">
  <title>{escape(category['name'])} · Open Learning Index</title>
  <link rel="stylesheet" href="../../styles.css">
</head>
<body>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="../../" aria-label="Open Learning Index home"><span class="brand-symbol" aria-hidden="true">↟</span><span>Open Learning Index</span></a>
      <nav class="main-nav" aria-label="Primary navigation"><a href="../../courses/">Courses</a><a class="active" href="../../#categories">Categories</a><a href="../../#about">About</a><a href="../../#how-it-works">How it works</a></nav>
      <div class="nav-actions"><a class="icon-link" href="../../courses/" aria-label="Search courses">⌕</a><span class="language-switch">◎ EN</span></div>
    </div>
  </header>
  <main class="shell category-page">
    <header class="category-page-header"><p class="section-kicker">Category</p><h1>{escape(category["name"])}</h1><p>{len(rows)} curated course{"s" if len(rows) != 1 else ""}, ordered by Recommendation.</p></header>
    <div class="course-grid catalogue-grid">{cards}</div>
  </main>
  <footer class="site-footer"><div class="shell footer-inner"><div><strong>Open Learning Index</strong><p>Curated category view generated from canonical data.</p></div><div class="footer-links"><a href="../../courses/">Browse all courses</a></div></div></footer>
</body>
</html>
"""

def build(output: Path) -> None:
    courses = json.loads(COURSES.read_text(encoding="utf-8"))
    category_rows = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    categories = {row["id"]: row for row in category_rows}
    reviews = load_current_records(REVIEWS_DIR, "reviewed_on")
    reference_reviews = load_current_records(REFERENCE_REVIEWS, "reviewed_on", "course_id")
    admissions = load_current_records(ADMISSIONS_DIR, "decided_on")

    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(SITE_SOURCE, output)

    public_courses = []
    for course in courses:
        if not is_publication_eligible(course):
            continue
        item = build_public_course(course, categories)
        item["editorial"] = editorial_projection(course, reviews, reference_reviews, admissions)
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

    course_by_id = {course["id"]: course for course in public_courses}
    for course in public_courses:
        write_text(
            output / "courses" / course["id"] / "index.html",
            render_static_course(course, course_by_id),
        )

    for category in category_rows:
        write_text(
            output / "categories" / category["id"] / "index.html",
            render_static_category(category, public_courses),
        )

    sitemap_urls = [f"{BASE_URL}/", f"{BASE_URL}/pt/"]
    sitemap_urls.extend(f"{BASE_URL}/courses/{course['id']}/" for course in public_courses)
    sitemap_urls.extend(f"{BASE_URL}/categories/{category['id']}/" for category in category_rows)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{escape(url)}</loc></url>\n" for url in sitemap_urls)
        + "</urlset>\n"
    )
    write_text(output / "sitemap.xml", sitemap)
    write_text(
        output / "robots.txt",
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n",
    )
    write_text(
        output / "404.html",
        """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Page not found · Open Learning Index</title>
<link rel="stylesheet" href="styles.css"></head><body>
<main class="shell detail-main"><section class="empty"><h1>Page not found</h1>
<p>That Open Learning Index page does not exist.</p><p><a href="./">Return to the catalogue</a></p>
</section></main></body></html>""",
    )

    required = [
        output / "index.html",
        output / "app.js",
        output / "course.html",
        output / "course.js",
        output / "styles.css",
        output / "data" / "catalog.json",
        output / "data" / "meta.json",
        output / "sitemap.xml",
        output / "robots.txt",
        output / "404.html",
    ]
    required.extend(output / "courses" / course["id"] / "index.html" for course in public_courses)
    required.extend(output / "categories" / category["id"] / "index.html" for category in category_rows)
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
