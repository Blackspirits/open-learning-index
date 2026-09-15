#!/usr/bin/env python3
"""Build the static Open Learning Index public catalogue from canonical data."""

import argparse
import hashlib
import json
import re
import shutil
import unicodedata
from collections import Counter
from html import escape
from pathlib import Path
from editorial_presentation import localize_course, media_for, media_html, pt
from editorial_presentation import pt as translate_pt

ROOT = Path(__file__).resolve().parents[1]
COURSES = ROOT / "data" / "courses.json"
CATEGORIES = ROOT / "data" / "categories.json"
CANDIDATES = ROOT / "data" / "candidates.json"
REVIEWS_DIR = ROOT / "data" / "reviews"
REFERENCE_REVIEWS = ROOT / "data" / "reference-reviews.json"
ADMISSIONS_DIR = ROOT / "data" / "admissions"
SITE_SOURCE = ROOT / "site"
DEFAULT_OUTPUT = ROOT / "_site"
BASE_URL = "https://blackspirits.github.io/open-learning-index"

THEME_BOOTSTRAP = """<script>
try {
  const saved = localStorage.getItem("oli-theme");
  const theme = saved === "dark" || saved === "light"
    ? saved
    : (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
} catch {}
</script>"""

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
    "pt": "Portuguese (variant unspecified)",
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


PT_CATEGORY_LABELS = {
    "ai-data": "IA e Dados",
    "arts-design": "Artes e Design",
    "business-entrepreneurship": "Negócios e Empreendedorismo",
    "computer-science": "Ciência de Computadores e Software",
    "cybersecurity-it": "Cibersegurança e TI",
    "education-teaching": "Educação e Ensino",
    "engineering-electronics": "Engenharia e Eletrónica",
    "finance-economics": "Finanças e Economia",
    "health-medicine": "Saúde e Medicina",
    "history-culture": "História e Cultura",
    "humanities-philosophy": "Humanidades e Filosofia",
    "languages": "Línguas",
    "law-public-policy": "Direito e Políticas Públicas",
    "marketing-sales": "Marketing e Vendas",
    "math-statistics": "Matemática e Estatística",
    "natural-sciences": "Ciências Naturais",
    "project-product-leadership": "Projeto, Produto e Liderança",
    "psychology-behavior": "Psicologia e Comportamento",
    "writing-communication": "Escrita e Comunicação",
}

CATEGORY_ICON_NAMES = {
    "ai-data": "ai",
    "arts-design": "palette",
    "business-entrepreneurship": "business",
    "computer-science": "code",
    "cybersecurity-it": "shield",
    "education-teaching": "education",
    "engineering-electronics": "engineering",
    "finance-economics": "finance",
    "health-medicine": "health",
    "history-culture": "history",
    "humanities-philosophy": "humanities",
    "languages": "languages",
    "law-public-policy": "law",
    "marketing-sales": "marketing",
    "math-statistics": "math",
    "natural-sciences": "science",
    "project-product-leadership": "leadership",
    "psychology-behavior": "brain",
    "writing-communication": "writing",
}

PT_LEVEL_LABELS = {
    "beginner": "Principiante",
    "beginner_to_intermediate": "Principiante a intermédio",
    "beginner_to_advanced": "Principiante a avançado",
    "intermediate": "Intermédio",
    "intermediate_to_advanced": "Intermédio a avançado",
    "advanced": "Avançado",
    "undergraduate": "Licenciatura",
    "graduate": "Pós-graduação",
}

PT_LANGUAGE_LABELS = {
    "ar": "Árabe",
    "az": "Azeri",
    "bg": "Búlgaro",
    "cs": "Checo",
    "de": "Alemão",
    "en": "Inglês",
    "es": "Espanhol",
    "fr": "Francês",
    "hu": "Húngaro",
    "hy": "Arménio",
    "ja": "Japonês",
    "ka": "Georgiano",
    "ko": "Coreano",
    "pt": "Português (variante não especificada)",
    "pt-BR": "Português (Brasil)",
    "pt-PT": "Português (Portugal)",
    "ro": "Romeno",
    "ru": "Russo",
    "sk": "Eslovaco",
    "tr": "Turco",
    "uk": "Ucraniano",
    "zh": "Chinês",
}


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
    stopwords = {"of", "the", "and", "de", "da", "do", "dos", "das", "e", "et", "la", "le"}
    all_words = [
        "".join(ch for ch in word if ch.isalnum())
        for word in str(value or "").replace("/", " ").split()
    ]
    all_words = [word for word in all_words if word]
    words = [word for word in all_words if word.casefold() not in stopwords] or all_words
    if not words:
        return "OLI"
    if len(words) == 1:
        return words[0][:3].upper()
    return (words[0][0] + words[1][0]).upper()


def static_tag(value: str, extra: str = "") -> str:
    cls = f"mini-tag {extra}".strip()
    return f'<span class="{cls}">{escape(value)}</span>'


def static_catalogue_card(course: dict, href_prefix: str = "../", is_pt=False) -> str:
    title = pt(course["title"]) if is_pt else course["title"]
    category = PT_CATEGORY_LABELS[course["category"]] if is_pt else course["category_name"]
    language = PT_LANGUAGE_LABELS.get(course["primary_language"], label_language(course["primary_language"])) if is_pt else label_language(course["primary_language"])
    language = f"Em {language[0].lower()}{language[1:]}" if is_pt else f"In {language}"
    level = PT_LEVEL_LABELS.get(course["level"], label_level(course["level"])) if is_pt else label_level(course["level"])
    access = {"F0":"Curso e credencial gratuitos", "F1":"Percurso completo com avaliação", "F2":"Conteúdos completos gratuitos"}[course["access_short"]] if is_pt else course["access_label"]
    label = "Recomendação" if is_pt else "Recommendation"
    score = f'{float(course["recommendation_score"]):.1f}'
    if is_pt: score = score.replace('.', ',')
    archive = static_tag("Arquivado" if is_pt else "Archived", "tag-archive") if course["status"] == "active_archive" else ""
    root = "../" + href_prefix if is_pt else href_prefix
    return (
        '<article class="catalogue-card">' + media_html(course, root)
        + '<div class="card-body"><div class="card-heading">'
        + f'<p class="provider">{escape(course["provider"])}</p>'
        + f'<h3><a href="{href_prefix}courses/{escape(course["id"])}/">{escape(title)}</a></h3></div>'
        + '<div class="catalogue-card-head">'
        + f'<span class="score-pill" aria-label="{label} {score} / 10">{score}</span>'
        + f'<span class="score-context">{label}</span></div>'
        + f'<div class="mini-tags">{static_tag(category, "tag-category")}{static_tag(language)}{static_tag(level)}{archive}</div>'
        + f'<div class="access-line"><span data-icon="access" aria-hidden="true"></span><span>{escape(access)}</span></div>'
        + '</div></article>'
    )


def static_catalogue_card_pt(course: dict, href_prefix: str = "../../") -> str:
    return static_catalogue_card(course, href_prefix, is_pt=True)


def original_title_html(course):
    original = course.get("original_title")
    if not original or original == course["title"]:
        return ""
    # The language of the canonical title can differ from the teaching language.
    original_language = {
        'openclassrooms-initiez-vous-gestion-projet': 'fr',
        'fun-boite-outils-philosophie-politique': 'fr',
        'fun-la-musique-quelle-histoire': 'fr',
        'blcu-umoocs-elementary-spoken-chinese': 'zh',
    }.get(course['id'], 'en')
    return f'<details class="original-title"><summary>Título original</summary><p lang="{original_language}">{escape(original)}</p></details>'


def render_static_course(course: dict, course_by_id: dict, candidate_by_id: dict) -> str:
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
        + '/"><span class="related-mark" data-icon="curated" aria-hidden="true"></span><span><strong>'
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
            candidate = candidate_by_id.get(item)
            label = candidate.get("title") if candidate else readable_id(item)
            comparisons.append(f'<li>{escape(label)}</li>')

    banner_title = "This course is archived" if archived else "This course is active"
    banner_copy = (
        f"Archived but still available · verified {course['last_verified']} · next review {course['next_review']}."
        if archived
        else f"Verified {course['last_verified']} · next review {course['next_review']}."
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
    ).replace("</", "<\\/")

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <link rel="canonical" href="{escape(url, quote=True)}">
  <link rel="alternate" hreflang="en" href="{escape(url, quote=True)}">
  <link rel="alternate" hreflang="pt-PT" href="{escape(BASE_URL + "/pt/courses/" + course["id"] + "/", quote=True)}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(course['title'], quote=True)} · Open Learning Index">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(url, quote=True)}">
  <title>{escape(course['title'])} · Open Learning Index</title>
  <link rel="stylesheet" href="../../styles.css">
  <link rel="stylesheet" href="../../editorial.css">
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <a class="skip-link" href="#course-detail">Skip to course details</a>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="../../" aria-label="Open Learning Index home">
        <span class="brand-symbol" data-icon="brand" aria-hidden="true"></span><span>Open Learning Index</span>
      </a>
      <nav class="main-nav" aria-label="Primary navigation">
        <a href="../../courses/">Courses</a>
        <a href="../../categories/">Categories</a>
        <a href="../../#about">Principles</a>
        <a href="../../#how-it-works">How it works</a>
      </nav>
      <details class="mobile-nav">
        <summary aria-label="Open navigation"><span class="menu-icon" aria-hidden="true"></span></summary>
        <nav aria-label="Mobile navigation"><a href="../../">Home</a><a href="../../courses/">Courses</a><a href="../../categories/">Categories</a><a href="../../#about">Principles</a><a href="../../#how-it-works">How it works</a></nav>
      </details>
      <div class="nav-actions"><a class="icon-link" href="../../courses/" aria-label="Search courses"><span data-icon="search" aria-hidden="true"></span></a><a class="language-switch" href="../../pt/courses/{escape(course["id"])}/" lang="pt-PT" hreflang="pt-PT" aria-label="Português (Portugal)">PT-PT</a><button class="theme-toggle" type="button" data-theme-toggle aria-label="Use dark theme" title="Use dark theme"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button></div>
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
        {original_title_html(course)}
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
      <span class="status-banner-icon" data-icon="status" aria-hidden="true"></span>
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
        </section>

        <section id="details" class="content-section">
          <h2>Before you start</h2>
          {before_html}
        </section>

        <section class="content-section">
          <h2>What is free</h2>
          <p><strong>{escape(course["access_label"])}</strong> — {escape(course["access_description"])}</p>
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
        {media_html(course)}
        <section class="sidebar-card">
          <h2>Course at a glance</h2>
          <dl class="glance-list">
            <div><span class="glance-icon" data-icon="provider" aria-hidden="true"></span><dt>Provider</dt><dd>{escape(course["provider"])}</dd></div>
            <div><span class="glance-icon" data-icon="globe" aria-hidden="true"></span><dt>Language</dt><dd>{escape(languages)}</dd></div>
            <div><span class="glance-icon" data-icon="level" aria-hidden="true"></span><dt>Level</dt><dd>{escape(label_level(course["level"]))}</dd></div>
            <div><span class="glance-icon" data-icon="clock" aria-hidden="true"></span><dt>Status</dt><dd>{escape(status)}</dd></div>
            <div><span class="glance-icon" data-icon="access" aria-hidden="true"></span><dt>Access</dt><dd>{escape(course["access_label"])}</dd></div>
          </dl>
        </section>

        <section class="sidebar-card">
          <h2>Related courses</h2>
          <div class="related-list">{related_html or '<p class="muted">No related course is currently linked.</p>'}</div>
          <p class="related-more"><a class="related-more-link" href="../../categories/{escape(course["category"])}/">View more in {escape(course["category_name"])} →</a></p>
        </section>
      </aside>
    </div>
  </main>

  <footer class="site-footer"><div class="shell footer-inner">
    <div><strong>Open Learning Index</strong><p>Curated, auditable and continuously maintained.</p></div>
    <div class="footer-links"><a href="../../">Home</a><a href="../../courses/">Courses</a><a href="https://github.com/Blackspirits/open-learning-index/blob/main/docs/methodology.md">Methodology</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a><a href="../../pt/courses/{escape(course["id"])}/" lang="pt-PT" hreflang="pt-PT">Português</a></div>
  </div></footer>
  <script src="../../icons.js" defer></script>
  <script src="../../theme.js" defer></script>
</body>
</html>
"""

def render_static_course_pt(course: dict, course_by_id: dict, candidate_by_id: dict) -> str:
    course = localize_course(course)
    localized_courses = {key: {**value, "title": pt(value["title"])} for key, value in course_by_id.items()}
    localized_candidates = {key: {**value, "title": pt(value["title"])} for key, value in candidate_by_id.items()}
    html = render_static_course(course, localized_courses, localized_candidates)
    html = html.replace('src="../../assets/', 'src="../../../assets/')
    html = html.replace('href="../../editorial.css"', 'href="../../../editorial.css"')
    for source in [*CREDENTIAL_LABELS.values(), *CREDIT_LABELS.values()]:
        html = html.replace(escape(source), escape(pt(source)))
    en_url = f"{BASE_URL}/courses/{course['id']}/"
    pt_url = f"{BASE_URL}/pt/courses/{course['id']}/"
    category_pt = PT_CATEGORY_LABELS.get(course["category"], course["category_name"])
    level_en = label_level(course["level"])
    level_pt = PT_LEVEL_LABELS.get(course["level"], level_en)
    language_en = label_language(course["primary_language"])
    language_pt = PT_LANGUAGE_LABELS.get(course["primary_language"], language_en)
    languages_en = " · ".join(
        label_language(code)
        for code in [course["primary_language"], *course.get("other_languages", [])]
    )
    languages_pt = " · ".join(
        PT_LANGUAGE_LABELS.get(code, label_language(code))
        for code in [course["primary_language"], *course.get("other_languages", [])]
    )
    archived = course["status"] == "active_archive"

    replacements = {
        '<html lang="en">': '<html lang="pt-PT">',
        en_url: pt_url,
        '<link rel="stylesheet" href="../../styles.css">': '<link rel="stylesheet" href="../../../styles.css">',
        '<script src="../../icons.js" defer></script>': '<script src="../../../icons.js" defer></script>',
        '<script src="../../theme.js" defer></script>': '<script src="../../../theme.js" defer></script>',
        'Skip to course details': 'Saltar para os detalhes do curso',
        'aria-label="Primary navigation"': 'aria-label="Navegação principal"',
        'aria-label="Open navigation"': 'aria-label="Abrir navegação"',
        'aria-label="Mobile navigation"': 'aria-label="Navegação móvel"',
        '>Courses</a>': '>Cursos</a>',
        '>Categories</a>': '>Categorias</a>',
        '>Principles</a>': '>Princípios</a>',
        '>How it works</a>': '>Como funciona</a>',
        'aria-label="Search courses"': 'aria-label="Pesquisar cursos"',
        'aria-label="Breadcrumb"': 'aria-label="Navegação estrutural"',
        '>Home</a>': '>Início</a>',
        'aria-label="Overall recommendation"': 'aria-label="Recomendação geral"',
        '<span>Overall recommendation</span>': '<span>Recomendação geral</span>',
        '<span>Quality</span>': '<span>Qualidade</span>',
        'aria-label="Course status"': 'aria-label="Estado do curso"',
        'aria-label="Course page sections"': 'aria-label="Secções da página do curso"',
        '>Overview</a>': '>Visão geral</a>',
        '>Details</a>': '>Detalhes</a>',
        '>Quality</a>': '>Qualidade</a>',
        '>Evidence</a>': '>Evidência</a>',
        '>Alternatives</a>': '>Alternativas</a>',
        '<h2>About this course</h2>': '<h2>Sobre este curso</h2>',
        '<h2>Before you start</h2>': '<h2>Antes de começar</h2>',
        '<h3>Prerequisites</h3>': '<h3>Pré-requisitos</h3>',
        '<h3>Required resources</h3>': '<h3>Recursos necessários</h3>',
        '<h3>Scope</h3>': '<h3>Âmbito</h3>',
        '<h2>What is free</h2>': '<h2>O que é gratuito</h2>',
        '<strong>Certificate:</strong>': '<strong>Certificado:</strong>',
        '<strong>Academic credit:</strong>': '<strong>Créditos académicos:</strong>',
        '<h2>Quality review</h2>': '<h2>Revisão de qualidade</h2>',
        '<h3>Recommendation rationale</h3>': '<h3>Justificação da recomendação</h3>',
        '<h3>Learning need</h3>': '<h3>Necessidade de aprendizagem</h3>',
        '<h3>Why it adds value</h3>': '<h3>Porque acrescenta valor</h3>',
        '<summary>Admission decision rationale</summary>': '<summary>Justificação da decisão de admissão</summary>',
        '<h2>Evidence and verification</h2>': '<h2>Evidência e verificação</h2>',
        'Last checked:': 'Última verificação:',
        'Next scheduled review:': 'Próxima revisão prevista:',
        '<h2>Compared against</h2>': '<h2>Comparado com</h2>',
        'No direct comparator is recorded for this course.': 'Não existe um comparador direto registado para este curso.',
        '<h2>Course at a glance</h2>': '<h2>Resumo do curso</h2>',
        '<dt>Provider</dt>': '<dt>Entidade</dt>',
        '<dt>Language</dt>': '<dt>Idioma</dt>',
        '<dt>Level</dt>': '<dt>Nível</dt>',
        '<dt>Status</dt>': '<dt>Estado</dt>',
        '<dt>Access</dt>': '<dt>Acesso</dt>',
        '<h2>Related courses</h2>': '<h2>Cursos relacionados</h2>',
        'Curated, auditable and continuously maintained.': 'Curado, auditável e continuamente mantido.',
        '>Methodology</a>': '>Metodologia</a>',
        '>GitHub</a>': '>GitHub</a>',
        f'>{escape(course["category_name"])}</a>': f'>{escape(category_pt)}</a>',
        static_tag(course["category_name"], "tag-category"): static_tag(category_pt, "tag-category"),
        static_tag(language_en): static_tag(language_pt),
        static_tag(level_en): static_tag(level_pt),
        '<span>Pedagogy</span>': '<span>Pedagogia</span>',
        '<span>Depth</span>': '<span>Profundidade</span>',
        '<span>Practice</span>': '<span>Prática</span>',
        '<span>Materials</span>': '<span>Materiais</span>',
        '<span>Currency</span>': '<span>Atualidade</span>',
        '<span>Expertise</span>': '<span>Especialização</span>',
        '<span>Accessibility</span>': '<span>Acessibilidade</span>',
        ' · free</dd>': ' · gratuito</dd>',
    }
    for old, new in replacements.items():
        html = html.replace(old, new)

    html = html.replace(
        f'<link rel="alternate" hreflang="en" href="{escape(pt_url, quote=True)}">',
        f'<link rel="alternate" hreflang="en" href="{escape(en_url, quote=True)}">',
    )
    html = html.replace(
        f'<dd>{escape(languages_en)}</dd>',
        f'<dd>{escape(languages_pt)}</dd>',
    )
    html = html.replace(
        f'<dd>{escape(level_en)}</dd>',
        f'<dd>{escape(level_pt)}</dd>',
    )

    access_labels_pt = {
        "F0": ("Curso completo + credencial gratuita", "Percurso completo com credencial de conclusão gratuita emitida pelo fornecedor."),
        "F1": ("Percurso avaliado gratuito", "Percurso completo com avaliação gratuita significativa, mas sem credencial formal gratuita."),
        "F2": ("Conteúdo pedagógico completo", "Conteúdo pedagógico substancial e completo, mas sem percurso formal de conclusão gratuito."),
    }
    access_label_pt, access_description_pt = access_labels_pt.get(
        course["access_short"],
        (course["access_label"], course["access_description"]),
    )
    html = html.replace(course["access_label"], access_label_pt)
    html = html.replace(course["access_description"], access_description_pt)

    html = html.replace(
        f'<a href="../../categories/{escape(course["category"])}/">{escape(category_pt)}</a>',
        f'<a href="../../categories/{escape(course["category"])}/">{escape(category_pt)}</a>',
    )

    html = html.replace(
        f'<a class="language-switch" href="../../pt/courses/{escape(course["id"])}/" lang="pt-PT" hreflang="pt-PT" aria-label="Português (Portugal)">PT-PT</a>',
        f'<a class="language-switch" href="../../../courses/{escape(course["id"])}/" lang="en" hreflang="en" aria-label="English">EN</a>',
    )

    html = html.replace(
        f'<a href="../../pt/courses/{escape(course["id"])}/" lang="pt-PT" hreflang="pt-PT">Português</a>',
        f'<a href="../../../courses/{escape(course["id"])}/" lang="en" hreflang="en">English</a>',
    )

    status_en = "Archived but still available" if archived else "Active"
    status_pt = "Arquivado mas disponível" if archived else "Ativo"
    html = html.replace(f'<dd>{escape(status_en)}</dd>', f'<dd>{escape(status_pt)}</dd>')

    tag_en = static_tag("Archived" if archived else "Active", "tag-archive" if archived else "")
    tag_pt = static_tag("Arquivado" if archived else "Ativo", "tag-archive" if archived else "")
    html = html.replace(tag_en, tag_pt)

    banner_title_en = "This course is archived" if archived else "This course is active"
    banner_title_pt = "Este curso está arquivado" if archived else "Este curso está ativo"
    banner_copy_en = (
        f"Archived but still available · verified {course['last_verified']} · next review {course['next_review']}."
        if archived
        else f"Verified {course['last_verified']} · next review {course['next_review']}."
    )
    banner_copy_pt = (
        f"Arquivado mas disponível · verificado em {course['last_verified']} · próxima revisão {course['next_review']}."
        if archived
        else f"Verificado em {course['last_verified']} · próxima revisão {course['next_review']}."
    )
    banner_button_en = "View archived materials →" if archived else "Open official course →"
    banner_button_pt = "Ver materiais arquivados →" if archived else "Abrir curso oficial →"
    html = html.replace(banner_title_en, banner_title_pt)
    html = html.replace(banner_copy_en, banner_copy_pt)
    html = html.replace(banner_button_en, banner_button_pt)

    html = html.replace(
        f'<a class="related-more-link" href="../../categories/{escape(course["category"])}/">View more in {escape(course["category_name"])} →</a>',
        f'<a class="related-more-link" href="../../categories/{escape(course["category"])}/">Ver mais em {escape(category_pt)} →</a>',
    )

    html = html.replace(' · source ', ' · fonte ')
    html = html.replace('No additional preparation requirements are documented.', 'Não estão documentados requisitos de preparação adicionais.')
    html = html.replace('No related course is currently linked.', 'Não existem cursos relacionados associados.')
    html = html.replace('Open Learning Index home', 'Página inicial do Open Learning Index')
    html = html.replace('Use dark theme', 'Usar tema escuro')
    # Format scores, without changing JSON-LD, URLs, percentages or review dates.
    import re
    html = re.sub(r'>([0-9]+)\.([0-9])</strong>', r'>\1,\2</strong>', html)
    html = re.sub(r'>([0-9]+)\.([0-9])</span>', r'>\1,\2</span>', html)
    return html




def render_category_directory(category_rows: list[dict], courses: list[dict], pt: bool = False) -> str:
    url = f"{BASE_URL}/pt/categories/" if pt else f"{BASE_URL}/categories/"
    other_url = f"{BASE_URL}/categories/" if pt else f"{BASE_URL}/pt/categories/"
    counts = Counter(course["category"] for course in courses)
    leaders = {}
    for category in category_rows:
        ranked = sorted(
            (course for course in courses if course["category"] == category["id"]),
            key=lambda item: (
                -float(item["recommendation_score"]),
                -float(item["quality_score"]),
                item["title"],
            ),
        )
        leaders[category["id"]] = ranked[0] if ranked else None

    cards = []
    for category in category_rows:
        category_id = category["id"]
        name = PT_CATEGORY_LABELS.get(category_id, category["name"]) if pt else category["name"]
        leader = leaders.get(category_id)
        icon = CATEGORY_ICON_NAMES.get(category_id, "curated")
        href = f"{category_id}/"
        course_count = counts.get(category_id, 0)
        leader_html = (
            f'<small>{"Mais recomendado" if pt else "Top recommendation"}: '
            f'<strong>{escape(translate_pt(leader["title"]) if pt else leader["title"])}</strong></small>'
            if leader
            else ""
        )
        cards.append(
            f'<a class="category-directory-card" href="{escape(href)}">'
            f'<span class="category-icon icon-{escape(category_id)}" data-icon="{escape(icon)}" aria-hidden="true"></span>'
            '<span class="category-directory-copy">'
            f'<strong>{escape(name)}</strong>'
            f'<span>{course_count} {"curso" if pt and course_count == 1 else "cursos" if pt else "course" if course_count == 1 else "courses"}</span>'
            f'{leader_html}</span>'
            '<span class="category-directory-arrow" data-icon="arrow" aria-hidden="true"></span>'
            '</a>'
        )

    lang = "pt-PT" if pt else "en"
    title = "Categorias" if pt else "Categories"
    kicker = "19 áreas de aprendizagem" if pt else "19 learning areas"
    intro = (
        "Explora todas as áreas do índice. Cada categoria reúne apenas cursos que passaram o processo editorial e de verificação."
        if pt
        else "Explore every area in the index. Each category contains only courses that passed the editorial and verification process."
    )
    home_label = "Início" if pt else "Home"
    courses_label = "Cursos" if pt else "Courses"
    principles_label = "Princípios" if pt else "Principles"
    how_label = "Como funciona" if pt else "How it works"
    methodology_label = "Metodologia" if pt else "Methodology"
    footer_copy = "Curado, auditável e continuamente mantido." if pt else "Curated, auditable and continuously maintained."
    switch_label = "English" if pt else "Português"
    switch_short = "EN" if pt else "PT-PT"
    switch_lang = "en" if pt else "pt-PT"
    root = "../../" if pt else "../"
    home_href = "../" if pt else "../"
    courses_href = "../courses/" if pt else "../courses/"
    principles_href = "../#about" if pt else "../#about"
    how_href = "../#how-it-works" if pt else "../#how-it-works"
    css_href = "../../styles.css" if pt else "../styles.css"
    icons_href = "../../icons.js" if pt else "../icons.js"
    theme_href = "../../theme.js" if pt else "../theme.js"
    switch_href = "../../categories/" if pt else "../pt/categories/"
    canonical_en = f"{BASE_URL}/categories/"
    canonical_pt = f"{BASE_URL}/pt/categories/"

    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(intro, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <link rel="canonical" href="{escape(url, quote=True)}">
  <link rel="alternate" hreflang="en" href="{escape(canonical_en, quote=True)}">
  <link rel="alternate" hreflang="pt-PT" href="{escape(canonical_pt, quote=True)}">
  <title>{escape(title)} · Open Learning Index</title>
  <link rel="stylesheet" href="{css_href}">
  <link rel="stylesheet" href="{css_href.replace("styles.css", "editorial.css")}">
</head>
<body>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="{home_href}" aria-label="Open Learning Index"><span class="brand-symbol" data-icon="brand" aria-hidden="true"></span><span>Open Learning Index</span></a>
      <nav class="main-nav" aria-label="{"Navegação principal" if pt else "Primary navigation"}">
        <a href="{courses_href}">{courses_label}</a>
        <a class="active" href="./">{title}</a>
        <a href="{principles_href}">{principles_label}</a>
        <a href="{how_href}">{how_label}</a>
      </nav>
      <details class="mobile-nav"><summary aria-label="{"Abrir navegação" if pt else "Open navigation"}"><span class="menu-icon" aria-hidden="true"></span></summary>
        <nav aria-label="{"Navegação móvel" if pt else "Mobile navigation"}"><a href="{home_href}">{home_label}</a><a href="{courses_href}">{courses_label}</a><a href="./">{title}</a><a href="{principles_href}">{principles_label}</a><a href="{how_href}">{how_label}</a></nav>
      </details>
      <div class="nav-actions">
        <a class="icon-link" href="{courses_href}" aria-label="{"Pesquisar cursos" if pt else "Search courses"}"><span data-icon="search" aria-hidden="true"></span></a>
        <a class="language-switch" href="{switch_href}" lang="{switch_lang}" hreflang="{switch_lang}" aria-label="{switch_label}">{switch_short}</a>
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="{"Usar tema escuro" if pt else "Use dark theme"}" title="{"Usar tema escuro" if pt else "Use dark theme"}"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button>
      </div>
    </div>
  </header>
  <main class="shell category-directory-page">
    <header class="category-directory-header">
      <p class="section-kicker">{escape(kicker)}</p>
      <h1>{escape(title)}</h1>
      <p>{escape(intro)}</p>
    </header>
    <div class="category-directory-grid">{"".join(cards)}</div>
  </main>
  <footer class="site-footer"><div class="shell footer-inner">
    <div><strong>Open Learning Index</strong><p>{escape(footer_copy)}</p></div>
    <div class="footer-links"><a href="{home_href}">{home_label}</a><a href="{courses_href}">{courses_label}</a><a href="https://github.com/Blackspirits/open-learning-index/blob/main/docs/methodology.md">{methodology_label}</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a><a href="{switch_href}" lang="{switch_lang}" hreflang="{switch_lang}">{switch_label}</a></div>
  </div></footer>
  <script src="{icons_href}" defer></script>
  <script src="{theme_href}" defer></script>
</body>
</html>
"""


def render_static_category(category: dict, courses: list[dict], pt: bool = False) -> str:
    category_id = category["id"]
    category_name = PT_CATEGORY_LABELS.get(category_id, category["name"]) if pt else category["name"]
    rows = sorted(
        (course for course in courses if course["category"] == category_id),
        key=lambda item: (
            -float(item["recommendation_score"]),
            -float(item["quality_score"]),
            item["title"],
        ),
    )
    cards = "".join(
        static_catalogue_card_pt(course, "../../") if pt else static_catalogue_card(course, "../../")
        for course in rows
    )
    url = f"{BASE_URL}/pt/categories/{category_id}/" if pt else f"{BASE_URL}/categories/{category_id}/"
    en_url = f"{BASE_URL}/categories/{category_id}/"
    pt_url = f"{BASE_URL}/pt/categories/{category_id}/"
    lang = "pt-PT" if pt else "en"
    root = "../../../" if pt else "../../"
    home_href = "../../" if pt else "../../"
    courses_href = "../../courses/" if pt else "../../courses/"
    categories_href = "../"
    principles_href = "../../#about" if pt else "../../#about"
    how_href = "../../#how-it-works" if pt else "../../#how-it-works"
    css_href = "../../../styles.css" if pt else "../../styles.css"
    icons_href = "../../../icons.js" if pt else "../../icons.js"
    theme_href = "../../../theme.js" if pt else "../../theme.js"
    switch_href = f"../../../categories/{category_id}/" if pt else f"../../pt/categories/{category_id}/"
    switch_label = "English" if pt else "Português"
    switch_short = "EN" if pt else "PT-PT"
    switch_lang = "en" if pt else "pt-PT"
    home_label = "Início" if pt else "Home"
    courses_label = "Cursos" if pt else "Courses"
    categories_label = "Categorias" if pt else "Categories"
    principles_label = "Princípios" if pt else "Principles"
    how_label = "Como funciona" if pt else "How it works"
    methodology_label = "Metodologia" if pt else "Methodology"
    kicker = "Categoria" if pt else "Category"
    description = (
        f"Cursos gratuitos selecionados em {category_name} no Open Learning Index."
        if pt
        else f"Curated free courses in {category_name} from the Open Learning Index."
    )
    count_copy = (
        f'{len(rows)} {"curso selecionado" if len(rows) == 1 else "cursos selecionados"}, ordenados por Recomendação.'
        if pt
        else f'{len(rows)} curated course{"s" if len(rows) != 1 else ""}, ordered by Recommendation.'
    )
    footer_copy = "Curado, auditável e continuamente mantido." if pt else "Curated, auditable and continuously maintained."

    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <link rel="canonical" href="{escape(url, quote=True)}">
  <link rel="alternate" hreflang="en" href="{escape(en_url, quote=True)}">
  <link rel="alternate" hreflang="pt-PT" href="{escape(pt_url, quote=True)}">
  <meta property="og:title" content="{escape(category_name, quote=True)} · Open Learning Index">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(url, quote=True)}">
  <title>{escape(category_name)} · Open Learning Index</title>
  <link rel="stylesheet" href="{css_href}">
  <link rel="stylesheet" href="{css_href.replace("styles.css", "editorial.css")}">
</head>
<body>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="{home_href}" aria-label="Open Learning Index"><span class="brand-symbol" data-icon="brand" aria-hidden="true"></span><span>Open Learning Index</span></a>
      <nav class="main-nav" aria-label="{"Navegação principal" if pt else "Primary navigation"}"><a href="{courses_href}">{courses_label}</a><a class="active" href="{categories_href}">{categories_label}</a><a href="{principles_href}">{principles_label}</a><a href="{how_href}">{how_label}</a></nav>
      <details class="mobile-nav"><summary aria-label="{"Abrir navegação" if pt else "Open navigation"}"><span class="menu-icon" aria-hidden="true"></span></summary><nav aria-label="{"Navegação móvel" if pt else "Mobile navigation"}"><a href="{home_href}">{home_label}</a><a href="{courses_href}">{courses_label}</a><a href="{categories_href}">{categories_label}</a><a href="{principles_href}">{principles_label}</a><a href="{how_href}">{how_label}</a></nav></details>
      <div class="nav-actions"><a class="icon-link" href="{courses_href}" aria-label="{"Pesquisar cursos" if pt else "Search courses"}"><span data-icon="search" aria-hidden="true"></span></a><a class="language-switch" href="{switch_href}" lang="{switch_lang}" hreflang="{switch_lang}" aria-label="{switch_label}">{switch_short}</a><button class="theme-toggle" type="button" data-theme-toggle aria-label="{"Usar tema escuro" if pt else "Use dark theme"}" title="{"Usar tema escuro" if pt else "Use dark theme"}"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button></div>
    </div>
  </header>
  <main class="shell category-page">
    <nav class="course-breadcrumbs" aria-label="{"Navegação estrutural" if pt else "Breadcrumb"}"><a href="{categories_href}">{categories_label}</a><span>›</span><span>{escape(category_name)}</span></nav>
    <header class="category-page-header"><p class="section-kicker">{kicker}</p><h1>{escape(category_name)}</h1><p>{escape(count_copy)}</p></header>
    <div class="course-grid catalogue-grid">{cards}</div>
  </main>
  <footer class="site-footer"><div class="shell footer-inner"><div><strong>Open Learning Index</strong><p>{escape(footer_copy)}</p></div><div class="footer-links"><a href="{home_href}">{home_label}</a><a href="{courses_href}">{courses_label}</a><a href="{categories_href}">{categories_label}</a><a href="https://github.com/Blackspirits/open-learning-index/blob/main/docs/methodology.md">{methodology_label}</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a><a href="{switch_href}" lang="{switch_lang}" hreflang="{switch_lang}">{switch_label}</a></div></div></footer>
  <script src="{icons_href}" defer></script>
  <script src="{theme_href}" defer></script>
</body>
</html>
"""

def version_public_assets(output: Path) -> None:
    """Keep each page's scripts, styles and fetched catalogue on one revision."""
    app_path = output / "app.js"
    app = app_path.read_text(encoding="utf-8")
    for name in ("catalog", "meta"):
        revision = hashlib.sha256((output / "data" / f"{name}.json").read_bytes()).hexdigest()[:16]
        app = re.sub(
            rf'"data/{name}\.json(?:\?v=[a-f0-9]+)?"',
            f'"data/{name}.json?v={revision}"',
            app,
        )
    write_text(app_path, app)
    revisions = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()[:16]
        for path in output.iterdir() if path.suffix in {".css", ".js"}
    }
    pattern = re.compile(r'((?:src|href)="(?:\.\.?/)*)([^"/?]+\.(?:css|js))(?:\?v=[a-f0-9]+)?"')

    def version_reference(match):
        prefix, name = match.groups()
        return f'{prefix}{name}?v={revisions[name]}"' if name in revisions else match.group(0)

    for page in output.rglob("*.html"):
        write_text(page, pattern.sub(version_reference, page.read_text(encoding="utf-8")))


def build(output: Path) -> None:
    courses = json.loads(COURSES.read_text(encoding="utf-8"))
    category_rows = json.loads(CATEGORIES.read_text(encoding="utf-8"))
    candidate_rows = json.loads(CANDIDATES.read_text(encoding="utf-8"))
    categories = {row["id"]: row for row in category_rows}
    candidate_by_id = {row["id"]: row for row in candidate_rows}
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
        item["media"] = media_for(item)
        localized = localize_course(item)
        item["presentation_pt"] = {"title": localized["title"], "description": localized["why_recommended"]}
        item["search_text"] += " " + localized["title"] + " " + localized["why_recommended"] + " " + PT_CATEGORY_LABELS[item["category"]]
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
    language_counts = Counter(
        code
        for course in public_courses
        for code in [course["primary_language"], *course.get("other_languages", [])]
    )

    meta = {
        "canonical_count": len(courses),
        "published_count": len(public_courses),
        "category_count": len(category_rows),
        "access_counts": dict(sorted(access_counts.items())),
        "language_counts": dict(sorted(language_counts.items())),
        "language_count": len(language_counts),
        "source_files": ["data/courses.json", "data/categories.json", "data/candidates.json"],
    }

    write_json(output / "data" / "catalog.json", public_courses)
    write_json(output / "data" / "categories.json", category_rows)
    write_json(output / "data" / "meta.json", meta)

    course_by_id = {course["id"]: course for course in public_courses}
    for course in public_courses:
        write_text(
            output / "courses" / course["id"] / "index.html",
            render_static_course(course, course_by_id, candidate_by_id),
        )
        write_text(
            output / "pt" / "courses" / course["id"] / "index.html",
            render_static_course_pt(course, course_by_id, candidate_by_id),
        )

    write_text(
        output / "categories" / "index.html",
        render_category_directory(category_rows, public_courses, pt=False),
    )
    write_text(
        output / "pt" / "categories" / "index.html",
        render_category_directory(category_rows, public_courses, pt=True),
    )

    for category in category_rows:
        write_text(
            output / "categories" / category["id"] / "index.html",
            render_static_category(category, public_courses, pt=False),
        )
        write_text(
            output / "pt" / "categories" / category["id"] / "index.html",
            render_static_category(category, public_courses, pt=True),
        )

    sitemap_urls = [
        f"{BASE_URL}/",
        f"{BASE_URL}/courses/",
        f"{BASE_URL}/categories/",
        f"{BASE_URL}/pt/",
        f"{BASE_URL}/pt/courses/",
        f"{BASE_URL}/pt/categories/",
    ]
    sitemap_urls.extend(f"{BASE_URL}/courses/{course['id']}/" for course in public_courses)
    sitemap_urls.extend(f"{BASE_URL}/pt/courses/{course['id']}/" for course in public_courses)
    sitemap_urls.extend(f"{BASE_URL}/categories/{category['id']}/" for category in category_rows)
    sitemap_urls.extend(f"{BASE_URL}/pt/categories/{category['id']}/" for category in category_rows)
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
<main class="shell course-page"><section class="empty"><h1>Page not found</h1>
<p>That Open Learning Index page does not exist.</p><p><a href="./">Return to the catalogue</a></p>
</section></main></body></html>""",
    )

    required = [
        output / "index.html",
        output / "courses" / "index.html",
        output / "pt" / "index.html",
        output / "pt" / "courses" / "index.html",
        output / "categories" / "index.html",
        output / "pt" / "categories" / "index.html",
        output / "assets" / "hero-library.webp",
        output / "app.js",
        output / "icons.js",
        output / "theme.js",
        output / "course.html",
        output / "styles.css",
        output / "data" / "catalog.json",
        output / "data" / "meta.json",
        output / "sitemap.xml",
        output / "robots.txt",
        output / "404.html",
    ]
    required.extend(output / "courses" / course["id"] / "index.html" for course in public_courses)
    required.extend(output / "pt" / "courses" / course["id"] / "index.html" for course in public_courses)
    required.extend(output / "categories" / category["id"] / "index.html" for category in category_rows)
    required.extend(output / "pt" / "categories" / category["id"] / "index.html" for category in category_rows)
    missing_files = [str(path.relative_to(output)) for path in required if not path.exists()]
    if missing_files:
        raise SystemExit(f"ERROR: public build missing required files: {missing_files}")

    version_public_assets(output)

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
