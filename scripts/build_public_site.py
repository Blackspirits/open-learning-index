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
from editorial_presentation import localize_course, media_for, media_html, translate_text

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
SUPPORTED_PRESENTATION_LOCALES = ("pt-PT", "es", "fr")
PUBLIC_LOCALES = ("en", *SUPPORTED_PRESENTATION_LOCALES)

LOCALE_META = {
    "en": {"prefix": "", "label": "English", "short": "EN"},
    "pt-PT": {"prefix": "pt", "label": "Português (Portugal)", "short": "PT-PT"},
}


def locale_url(locale: str, route: str = "") -> str:
    prefix = LOCALE_META[locale]["prefix"]
    base = f"{BASE_URL}/{prefix}/" if prefix else f"{BASE_URL}/"
    return base + route.lstrip("/")


def alternate_links(route: str) -> str:
    return "\n".join(
        f'  <link rel="alternate" hreflang="{locale}" '
        f'href="{escape(locale_url(locale, route), quote=True)}">'
        for locale in PUBLIC_LOCALES
    )


def language_control(current_locale: str, hrefs: dict[str, str]) -> str:
    aria_label = {
        "pt-PT": "Idioma",
        "es": "Idioma",
        "fr": "Langue",
    }.get(current_locale, "Language")
    others = [locale for locale in PUBLIC_LOCALES if locale != current_locale]
    if len(PUBLIC_LOCALES) == 2:
        locale = others[0]
        meta = LOCALE_META[locale]
        return (
            f'<a class="language-switch" href="{escape(hrefs[locale])}" '
            f'lang="{locale}" hreflang="{locale}" aria-label="{escape(meta["label"])}">'
            f'{escape(meta["short"])}</a>'
        )

    current = LOCALE_META[current_locale]
    links = "".join(
        f'<a href="{escape(hrefs[locale])}" lang="{locale}" hreflang="{locale}">'
        f'{escape(LOCALE_META[locale]["label"])}</a>'
        for locale in PUBLIC_LOCALES
    )
    return (
        '<details class="language-menu">'
        f'<summary aria-label="{escape(aria_label)}">{escape(current["short"])}</summary>'
        f'<nav aria-label="{escape(aria_label)}">{links}</nav>'
        '</details>'
    )

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
    "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese (Portugal)",
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
    "ar": "árabe",
    "az": "azeri",
    "bg": "búlgaro",
    "cs": "checo",
    "de": "alemão",
    "en": "inglês",
    "es": "espanhol",
    "fr": "francês",
    "hu": "húngaro",
    "hy": "arménio",
    "ja": "japonês",
    "ka": "georgiano",
    "ko": "coreano",
    "pt": "português (variante não especificada)",
    "pt-BR": "português (Brasil)",
    "pt-PT": "português (Portugal)",
    "ro": "romeno",
    "ru": "russo",
    "sk": "eslovaco",
    "tr": "turco",
    "uk": "ucraniano",
    "zh": "chinês",
}


LOCALE_ROUTE_PREFIX = {
    "en": "",
    "pt-PT": "pt",
}

LOCALE_CATEGORY_LABELS = {
    "pt-PT": PT_CATEGORY_LABELS,
}

LOCALE_LEVEL_LABELS = {
    "pt-PT": PT_LEVEL_LABELS,
}

LOCALE_LANGUAGE_LABELS = {
    "pt-PT": PT_LANGUAGE_LABELS,
}

LOCALE_ACCESS_LABELS = {
    "pt-PT": {
        "F0": "Curso e credencial gratuitos",
        "F1": "Percurso completo com avaliação",
        "F2": "Conteúdos completos gratuitos",
    },
}

LOCALE_CARD_COPY = {
    "en": {
        "recommendation": "Recommendation",
        "quality": "Quality",
        "verified": "Verified",
        "archived": "Archived",
        "language_prefix": "In",
        "decimal": ".",
    },
    "pt-PT": {
        "recommendation": "Recomendação",
        "quality": "Qualidade",
        "verified": "Verificado",
        "archived": "Arquivado",
        "language_prefix": "Em",
        "decimal": ",",
    },
}

LOCALE_MONTHS = {
    "en": ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"),
    "pt-PT": ("jan.", "fev.", "mar.", "abr.", "mai.", "jun.", "jul.", "ago.", "set.", "out.", "nov.", "dez."),
}


LOCALE_DIRECTORY_COPY = {
    "en": {
        "title": "Categories",
        "areas": "learning areas",
        "intro": "Explore every area in the index. Each category contains only courses that passed the editorial and verification process.",
        "top": "Top recommendation",
        "course": "course",
        "courses": "courses",
        "home": "Home",
        "courses_nav": "Courses",
        "methodology": "Methodology",
        "how": "How it works",
        "footer": "Curated, auditable and continuously maintained.",
        "primary_nav": "Primary navigation",
        "mobile_nav": "Mobile navigation",
        "open_nav": "Open navigation",
        "search": "Search courses",
        "theme": "Use dark theme",
    },
    "pt-PT": {
        "title": "Categorias",
        "areas": "áreas de aprendizagem",
        "intro": "Explora todas as áreas do índice. Cada categoria reúne apenas cursos que passaram o processo editorial e de verificação.",
        "top": "Mais recomendado",
        "course": "curso",
        "courses": "cursos",
        "home": "Início",
        "courses_nav": "Cursos",
        "methodology": "Metodologia",
        "how": "Como funciona",
        "footer": "Curado, auditável e continuamente mantido.",
        "primary_nav": "Navegação principal",
        "mobile_nav": "Navegação móvel",
        "open_nav": "Abrir navegação",
        "search": "Pesquisar cursos",
        "theme": "Usar tema escuro",
    },
}

LOCALE_CATEGORY_COPY = {
    "en": {
        "kicker": "Category",
        "home": "Home",
        "courses": "Courses",
        "categories": "Categories",
        "methodology": "Methodology",
        "how": "How it works",
        "description": "Curated free courses in {category} from the Open Learning Index.",
        "count_one": "{count} curated course, ordered by Recommendation.",
        "count_many": "{count} curated courses, ordered by Recommendation.",
        "start": "Start here",
        "footer": "Curated, auditable and continuously maintained.",
        "primary_nav": "Primary navigation",
        "mobile_nav": "Mobile navigation",
        "open_nav": "Open navigation",
        "search": "Search courses",
        "breadcrumb": "Breadcrumb",
        "theme": "Use dark theme",
        "freshness": {
            "fast": "Fast-moving field: courses here use shorter review intervals because tools, standards or platforms can change quickly.",
            "medium": "Actively maintained field: access, content and provider changes are re-checked on a moderate cadence.",
            "slow": "Foundational field: age alone is not treated as a defect, while access and comparative quality are still re-verified.",
        },
    },
    "pt-PT": {
        "kicker": "Categoria",
        "home": "Início",
        "courses": "Cursos",
        "categories": "Categorias",
        "methodology": "Metodologia",
        "how": "Como funciona",
        "description": "Cursos gratuitos selecionados em {category} no Open Learning Index.",
        "count_one": "{count} curso selecionado, ordenado por Recomendação.",
        "count_many": "{count} cursos selecionados, ordenados por Recomendação.",
        "start": "Começar aqui",
        "footer": "Curado, auditável e continuamente mantido.",
        "primary_nav": "Navegação principal",
        "mobile_nav": "Navegação móvel",
        "open_nav": "Abrir navegação",
        "search": "Pesquisar cursos",
        "breadcrumb": "Navegação estrutural",
        "theme": "Usar tema escuro",
        "freshness": {
            "fast": "Área de rápida mudança: estes cursos usam intervalos de revisão mais curtos porque ferramentas, normas ou plataformas podem mudar rapidamente.",
            "medium": "Área ativamente mantida: acesso, conteúdo e alterações da entidade são reverificados com uma cadência moderada.",
            "slow": "Área de fundamentos estáveis: a idade, por si só, não é tratada como defeito, mantendo-se a reverificação do acesso e da qualidade comparativa.",
        },
    },
}


LOCALE_COURSE_COPY = {
    "en": {
        "original_title": "Original title",
        "skip": "Skip to course details",
        "home_aria": "Open Learning Index home",
        "primary_nav": "Primary navigation",
        "open_nav": "Open navigation",
        "mobile_nav": "Mobile navigation",
        "home": "Home",
        "courses": "Courses",
        "categories": "Categories",
        "methodology": "Methodology",
        "how": "How it works",
        "search": "Search courses",
        "theme": "Use dark theme",
        "breadcrumb": "Breadcrumb",
        "overall_recommendation": "Overall recommendation",
        "quality": "Quality",
        "status_aria": "Course status",
        "sections_aria": "Course page sections",
        "overview": "Overview",
        "details": "Details",
        "evidence": "Evidence",
        "compared": "Compared",
        "why_recommend": "Why we recommend it",
        "before_start": "Before you start",
        "prerequisites": "Prerequisites",
        "required_resources": "Required resources",
        "scope": "Scope",
        "no_preparation": "No additional preparation requirements are documented.",
        "what_free": "What is free",
        "certificate": "Certificate",
        "academic_credit": "Academic credit",
        "quality_review": "Quality review",
        "learning_need": "Learning need",
        "why_value": "Why it adds value",
        "admission_rationale": "Admission decision rationale",
        "evidence_verification": "Evidence and verification",
        "last_checked": "Last checked",
        "next_review": "Next scheduled review",
        "compared_against": "Compared against",
        "no_comparator": "No direct comparator is recorded for this course.",
        "course_glance": "Course at a glance",
        "provider": "Provider",
        "language": "Language",
        "level": "Level",
        "status": "Status",
        "access": "Access",
        "related_courses": "Related courses",
        "no_related": "No related course is currently linked.",
        "view_more": "View more in {category} →",
        "footer": "Curated, auditable and continuously maintained.",
        "course_source": "Course source",
        "repository_source": "Repository source",
        "community_reference": "Community reference",
        "supporting_source": "Supporting source",
        "active": "Active",
        "archived": "Archived",
        "archived_available": "Archived but still available",
        "banner_active": "This course is active",
        "banner_archived": "This course is archived",
        "banner_copy_active": "Verified {verified} · next review {next_review}.",
        "banner_copy_archived": "Archived but still available · verified {verified} · next review {next_review}.",
        "button_active": "Open official course →",
        "button_archived": "View archived materials →",
    },
    "pt-PT": {
        "original_title": "Título original",
        "skip": "Saltar para os detalhes do curso",
        "home_aria": "Página inicial do Open Learning Index",
        "primary_nav": "Navegação principal",
        "open_nav": "Abrir navegação",
        "mobile_nav": "Navegação móvel",
        "home": "Início",
        "courses": "Cursos",
        "categories": "Categorias",
        "methodology": "Metodologia",
        "how": "Como funciona",
        "search": "Pesquisar cursos",
        "theme": "Usar tema escuro",
        "breadcrumb": "Navegação estrutural",
        "overall_recommendation": "Recomendação geral",
        "quality": "Qualidade",
        "status_aria": "Estado do curso",
        "sections_aria": "Secções da página do curso",
        "overview": "Visão geral",
        "details": "Detalhes",
        "evidence": "Evidência",
        "compared": "Comparação",
        "why_recommend": "Porque recomendamos este curso",
        "before_start": "Antes de começar",
        "prerequisites": "Pré-requisitos",
        "required_resources": "Recursos necessários",
        "scope": "Âmbito",
        "no_preparation": "Não estão documentados requisitos de preparação adicionais.",
        "what_free": "O que é gratuito",
        "certificate": "Certificado",
        "academic_credit": "Créditos académicos",
        "quality_review": "Revisão de qualidade",
        "learning_need": "Necessidade de aprendizagem",
        "why_value": "Porque acrescenta valor",
        "admission_rationale": "Justificação da decisão de admissão",
        "evidence_verification": "Evidência e verificação",
        "last_checked": "Última verificação",
        "next_review": "Próxima revisão prevista",
        "compared_against": "Comparado com",
        "no_comparator": "Não existe um comparador direto registado para este curso.",
        "course_glance": "Resumo do curso",
        "provider": "Entidade",
        "language": "Idioma",
        "level": "Nível",
        "status": "Estado",
        "access": "Acesso",
        "related_courses": "Cursos relacionados",
        "no_related": "Não existem cursos relacionados associados.",
        "view_more": "Ver mais em {category} →",
        "footer": "Curado, auditável e continuamente mantido.",
        "course_source": "Fonte do curso",
        "repository_source": "Fonte de repositório",
        "community_reference": "Referência da comunidade",
        "supporting_source": "Fonte de apoio",
        "active": "Ativo",
        "archived": "Arquivado",
        "archived_available": "Arquivado mas disponível",
        "banner_active": "Este curso está ativo",
        "banner_archived": "Este curso está arquivado",
        "banner_copy_active": "Verificado em {verified} · próxima revisão {next_review}.",
        "banner_copy_archived": "Arquivado mas disponível · verificado em {verified} · próxima revisão {next_review}.",
        "button_active": "Abrir curso oficial →",
        "button_archived": "Ver materiais arquivados →",
    },
}

LOCALE_QUALITY_COMPONENTS = {
    "en": {
        "pedagogy": "Pedagogy",
        "depth": "Depth",
        "practice": "Practice",
        "materials": "Materials",
        "currency": "Currency",
        "expertise": "Expertise",
        "accessibility": "Accessibility",
    },
    "pt-PT": {
        "pedagogy": "Pedagogia",
        "depth": "Profundidade",
        "practice": "Prática",
        "materials": "Materiais",
        "currency": "Atualidade",
        "expertise": "Especialização",
        "accessibility": "Acessibilidade",
    },
}

LOCALE_ACCESS_DETAIL = {
    "en": {
        "F0": (
            "Full course + free credential",
            "Complete learning path with a free provider completion credential.",
        ),
        "F1": (
            "Full assessed learning path",
            "Complete learning path with meaningful free assessment, but no free formal credential.",
        ),
        "F2": (
            "Full teaching content",
            "Substantial complete teaching content, but no free formal completion path.",
        ),
    },
    "pt-PT": {
        "F0": (
            "Curso completo + credencial gratuita",
            "Percurso completo com credencial de conclusão gratuita emitida pelo fornecedor.",
        ),
        "F1": (
            "Percurso avaliado gratuito",
            "Percurso completo com avaliação gratuita significativa, mas sem credencial formal gratuita.",
        ),
        "F2": (
            "Conteúdo pedagógico completo",
            "Conteúdo pedagógico substancial e completo, mas sem percurso formal de conclusão gratuito.",
        ),
    },
}


# Spanish public-presentation extension.  The canonical/editorial source data stays
# unchanged; only learner-facing presentation labels and prose are localised.
LOCALE_META["es"] = {"prefix": "es", "label": "Español", "short": "ES"}
LOCALE_ROUTE_PREFIX["es"] = "es"

ES_CATEGORY_LABELS = {
    "ai-data": "IA y Datos",
    "arts-design": "Artes y Diseño",
    "business-entrepreneurship": "Negocios y Emprendimiento",
    "computer-science": "Informática y Software",
    "cybersecurity-it": "Ciberseguridad y TI",
    "education-teaching": "Educación y Enseñanza",
    "engineering-electronics": "Ingeniería y Electrónica",
    "finance-economics": "Finanzas y Economía",
    "health-medicine": "Salud y Medicina",
    "history-culture": "Historia y Cultura",
    "humanities-philosophy": "Humanidades y Filosofía",
    "languages": "Idiomas",
    "law-public-policy": "Derecho y Políticas Públicas",
    "marketing-sales": "Marketing y Ventas",
    "math-statistics": "Matemáticas y Estadística",
    "natural-sciences": "Ciencias Naturales",
    "project-product-leadership": "Proyectos, Producto y Liderazgo",
    "psychology-behavior": "Psicología y Comportamiento",
    "writing-communication": "Escritura y Comunicación",
}
ES_LEVEL_LABELS = {
    "beginner": "Principiante",
    "beginner_to_intermediate": "Principiante a intermedio",
    "beginner_to_advanced": "Principiante a avanzado",
    "intermediate": "Intermedio",
    "intermediate_to_advanced": "Intermedio a avanzado",
    "advanced": "Avanzado",
    "undergraduate": "Grado",
    "graduate": "Posgrado",
}
ES_LANGUAGE_LABELS = {
    "ar": "árabe", "az": "azerí", "bg": "búlgaro", "cs": "checo",
    "de": "alemán", "en": "inglés", "es": "español", "fr": "francés",
    "hu": "húngaro", "hy": "armenio", "it": "italiano", "ja": "japonés",
    "ka": "georgiano", "ko": "coreano", "nl": "neerlandés", "pl": "polaco",
    "pt": "portugués (variante no especificada)",
    "pt-BR": "portugués (Brasil)", "pt-PT": "portugués (Portugal)",
    "ro": "rumano", "ru": "ruso", "sk": "eslovaco", "tr": "turco",
    "uk": "ucraniano", "vi": "vietnamita", "zh": "chino",
}
LOCALE_CATEGORY_LABELS["es"] = ES_CATEGORY_LABELS
LOCALE_LEVEL_LABELS["es"] = ES_LEVEL_LABELS
LOCALE_LANGUAGE_LABELS["es"] = ES_LANGUAGE_LABELS
LOCALE_ACCESS_LABELS["es"] = {
    "F0": "Curso y credencial gratuitos",
    "F1": "Itinerario completo con evaluación",
    "F2": "Contenido completo gratuito",
}
LOCALE_CARD_COPY["es"] = {
    "recommendation": "Recomendación",
    "quality": "Calidad",
    "verified": "Verificado",
    "archived": "Archivado",
    "language_prefix": "En",
    "decimal": ",",
}
LOCALE_MONTHS["es"] = (
    "ene.", "feb.", "mar.", "abr.", "may.", "jun.",
    "jul.", "ago.", "sept.", "oct.", "nov.", "dic.",
)
LOCALE_DIRECTORY_COPY["es"] = {
    "title": "Categorías",
    "areas": "áreas de aprendizaje",
    "intro": "Explora todas las áreas del índice. Cada categoría contiene únicamente cursos que han superado el proceso editorial y de verificación.",
    "top": "Más recomendado",
    "course": "curso",
    "courses": "cursos",
    "home": "Inicio",
    "courses_nav": "Cursos",
    "methodology": "Metodología",
    "how": "Cómo funciona",
    "footer": "Curado, auditable y mantenido de forma continua.",
    "primary_nav": "Navegación principal",
    "mobile_nav": "Navegación móvil",
    "open_nav": "Abrir navegación",
    "search": "Buscar cursos",
    "theme": "Usar tema oscuro",
}
LOCALE_CATEGORY_COPY["es"] = {
    "kicker": "Categoría",
    "home": "Inicio",
    "courses": "Cursos",
    "categories": "Categorías",
    "methodology": "Metodología",
    "how": "Cómo funciona",
    "description": "Cursos gratuitos seleccionados de {category} en Open Learning Index.",
    "count_one": "{count} curso seleccionado, ordenado por Recomendación.",
    "count_many": "{count} cursos seleccionados, ordenados por Recomendación.",
    "start": "Empieza aquí",
    "footer": "Curado, auditable y mantenido de forma continua.",
    "primary_nav": "Navegación principal",
    "mobile_nav": "Navegación móvil",
    "open_nav": "Abrir navegación",
    "search": "Buscar cursos",
    "breadcrumb": "Ruta de navegación",
    "theme": "Usar tema oscuro",
    "freshness": {
        "fast": "Área de cambio rápido: estos cursos usan intervalos de revisión más cortos porque las herramientas, normas o plataformas pueden cambiar rápidamente.",
        "medium": "Área mantenida activamente: el acceso, el contenido y los cambios del proveedor se vuelven a comprobar con una frecuencia moderada.",
        "slow": "Área de fundamentos estables: la antigüedad por sí sola no se considera un defecto, aunque se siguen verificando el acceso y la calidad comparativa.",
    },
}
LOCALE_COURSE_COPY["es"] = {
    "original_title": "Título original",
    "skip": "Saltar a los detalles del curso",
    "home_aria": "Página inicial de Open Learning Index",
    "primary_nav": "Navegación principal",
    "open_nav": "Abrir navegación",
    "mobile_nav": "Navegación móvil",
    "home": "Inicio",
    "courses": "Cursos",
    "categories": "Categorías",
    "methodology": "Metodología",
    "how": "Cómo funciona",
    "search": "Buscar cursos",
    "theme": "Usar tema oscuro",
    "breadcrumb": "Ruta de navegación",
    "overall_recommendation": "Recomendación general",
    "quality": "Calidad",
    "status_aria": "Estado del curso",
    "sections_aria": "Secciones de la página del curso",
    "overview": "Resumen",
    "details": "Detalles",
    "evidence": "Evidencia",
    "compared": "Comparación",
    "why_recommend": "Por qué recomendamos este curso",
    "before_start": "Antes de empezar",
    "prerequisites": "Prerrequisitos",
    "required_resources": "Recursos necesarios",
    "scope": "Alcance",
    "no_preparation": "No se documentan requisitos adicionales de preparación.",
    "what_free": "Qué es gratuito",
    "certificate": "Certificado",
    "academic_credit": "Créditos académicos",
    "quality_review": "Revisión de calidad",
    "learning_need": "Necesidad de aprendizaje",
    "why_value": "Por qué aporta valor",
    "admission_rationale": "Justificación de la decisión de admisión",
    "evidence_verification": "Evidencia y verificación",
    "last_checked": "Última verificación",
    "next_review": "Próxima revisión prevista",
    "compared_against": "Comparado con",
    "no_comparator": "No hay ningún comparador directo registrado para este curso.",
    "course_glance": "Resumen del curso",
    "provider": "Entidad",
    "language": "Idioma",
    "level": "Nivel",
    "status": "Estado",
    "access": "Acceso",
    "related_courses": "Cursos relacionados",
    "no_related": "No hay cursos relacionados vinculados.",
    "view_more": "Ver más en {category} →",
    "footer": "Curado, auditable y mantenido de forma continua.",
    "course_source": "Fuente del curso",
    "repository_source": "Fuente del repositorio",
    "community_reference": "Referencia de la comunidad",
    "supporting_source": "Fuente de apoyo",
    "active": "Activo",
    "archived": "Archivado",
    "archived_available": "Archivado pero disponible",
    "banner_active": "Este curso está activo",
    "banner_archived": "Este curso está archivado",
    "banner_copy_active": "Verificado el {verified} · próxima revisión {next_review}.",
    "banner_copy_archived": "Archivado pero disponible · verificado el {verified} · próxima revisión {next_review}.",
    "button_active": "Abrir curso oficial →",
    "button_archived": "Ver materiales archivados →",
}
LOCALE_QUALITY_COMPONENTS["es"] = {
    "pedagogy": "Pedagogía",
    "depth": "Profundidad",
    "practice": "Práctica",
    "materials": "Materiales",
    "currency": "Actualidad",
    "expertise": "Especialización",
    "accessibility": "Accesibilidad",
}
LOCALE_ACCESS_DETAIL["es"] = {
    "F0": (
        "Curso completo + credencial gratuita",
        "Itinerario de aprendizaje completo con una credencial gratuita de finalización emitida por el proveedor.",
    ),
    "F1": (
        "Itinerario evaluado gratuito",
        "Itinerario de aprendizaje completo con evaluación gratuita significativa, pero sin credencial formal gratuita.",
    ),
    "F2": (
        "Contenido pedagógico completo",
        "Contenido pedagógico sustancial y completo, pero sin una vía formal y gratuita de finalización.",
    ),
}


# French public-presentation extension. Canonical/editorial records stay unchanged;
# only learner-facing presentation labels and prose are localised.
LOCALE_META["fr"] = {"prefix": "fr", "label": "Français", "short": "FR"}
LOCALE_ROUTE_PREFIX["fr"] = "fr"

FR_CATEGORY_LABELS = {
    "ai-data": "IA et données",
    "arts-design": "Arts et design",
    "business-entrepreneurship": "Entreprise et entrepreneuriat",
    "computer-science": "Informatique et logiciels",
    "cybersecurity-it": "Cybersécurité et informatique",
    "education-teaching": "Éducation et enseignement",
    "engineering-electronics": "Ingénierie et électronique",
    "finance-economics": "Finance et économie",
    "health-medicine": "Santé et médecine",
    "history-culture": "Histoire et culture",
    "humanities-philosophy": "Sciences humaines et philosophie",
    "languages": "Langues",
    "law-public-policy": "Droit et politiques publiques",
    "marketing-sales": "Marketing et vente",
    "math-statistics": "Mathématiques et statistiques",
    "natural-sciences": "Sciences naturelles",
    "project-product-leadership": "Projet, produit et leadership",
    "psychology-behavior": "Psychologie et comportement",
    "writing-communication": "Écriture et communication",
}
FR_LEVEL_LABELS = {
    "beginner": "Débutant",
    "beginner_to_intermediate": "Débutant à intermédiaire",
    "beginner_to_advanced": "Débutant à avancé",
    "intermediate": "Intermédiaire",
    "intermediate_to_advanced": "Intermédiaire à avancé",
    "advanced": "Avancé",
    "undergraduate": "Premier cycle universitaire",
    "graduate": "Deuxième/troisième cycle universitaire",
}
FR_LANGUAGE_LABELS = {
    "ar": "arabe", "az": "azéri", "bg": "bulgare", "cs": "tchèque",
    "de": "allemand", "en": "anglais", "es": "espagnol", "fr": "français",
    "hu": "hongrois", "hy": "arménien", "it": "italien", "ja": "japonais",
    "ka": "géorgien", "ko": "coréen", "nl": "néerlandais", "pl": "polonais",
    "pt": "portugais (variante non précisée)",
    "pt-BR": "portugais (Brésil)", "pt-PT": "portugais (Portugal)",
    "ro": "roumain", "ru": "russe", "sk": "slovaque", "tr": "turc",
    "uk": "ukrainien", "vi": "vietnamien", "zh": "chinois",
}
LOCALE_CATEGORY_LABELS["fr"] = FR_CATEGORY_LABELS
LOCALE_LEVEL_LABELS["fr"] = FR_LEVEL_LABELS
LOCALE_LANGUAGE_LABELS["fr"] = FR_LANGUAGE_LABELS
LOCALE_ACCESS_LABELS["fr"] = {
    "F0": "Cours et attestation gratuits",
    "F1": "Parcours complet avec évaluation",
    "F2": "Contenu pédagogique complet et gratuit",
}
LOCALE_CARD_COPY["fr"] = {
    "recommendation": "Recommandation",
    "quality": "Qualité",
    "verified": "Vérifié",
    "archived": "Archivé",
    "language_prefix": "En",
    "decimal": ",",
}
LOCALE_MONTHS["fr"] = (
    "janv.", "févr.", "mars", "avr.", "mai", "juin",
    "juil.", "août", "sept.", "oct.", "nov.", "déc.",
)
LOCALE_DIRECTORY_COPY["fr"] = {
    "title": "Catégories",
    "areas": "domaines d’apprentissage",
    "intro": "Explorez tous les domaines de l’index. Chaque catégorie ne contient que des cours ayant passé le processus éditorial et de vérification.",
    "top": "Meilleure recommandation",
    "course": "cours",
    "courses": "cours",
    "home": "Accueil",
    "courses_nav": "Cours",
    "methodology": "Méthodologie",
    "how": "Fonctionnement",
    "footer": "Sélectionné avec rigueur, auditable et maintenu en continu.",
    "primary_nav": "Navigation principale",
    "mobile_nav": "Navigation mobile",
    "open_nav": "Ouvrir la navigation",
    "search": "Rechercher des cours",
    "theme": "Utiliser le thème sombre",
}
LOCALE_CATEGORY_COPY["fr"] = {
    "kicker": "Catégorie",
    "home": "Accueil",
    "courses": "Cours",
    "categories": "Catégories",
    "methodology": "Méthodologie",
    "how": "Fonctionnement",
    "description": "Cours gratuits sélectionnés en {category} dans Open Learning Index.",
    "count_one": "{count} cours sélectionné, classé par Recommandation.",
    "count_many": "{count} cours sélectionnés, classés par Recommandation.",
    "start": "Commencer ici",
    "footer": "Sélectionné avec rigueur, auditable et maintenu en continu.",
    "primary_nav": "Navigation principale",
    "mobile_nav": "Navigation mobile",
    "open_nav": "Ouvrir la navigation",
    "search": "Rechercher des cours",
    "breadcrumb": "Fil d’Ariane",
    "theme": "Utiliser le thème sombre",
    "freshness": {
        "fast": "Domaine à évolution rapide : les cours utilisent des intervalles de révision plus courts, car les outils, normes ou plateformes peuvent changer rapidement.",
        "medium": "Domaine activement maintenu : l’accès, le contenu et les changements du fournisseur sont revérifiés à une fréquence modérée.",
        "slow": "Domaine fondamental stable : l’ancienneté seule n’est pas considérée comme un défaut, tandis que l’accès et la qualité comparative restent revérifiés.",
    },
}
LOCALE_COURSE_COPY["fr"] = {
    "original_title": "Titre original",
    "skip": "Aller aux détails du cours",
    "home_aria": "Accueil d’Open Learning Index",
    "primary_nav": "Navigation principale",
    "open_nav": "Ouvrir la navigation",
    "mobile_nav": "Navigation mobile",
    "home": "Accueil",
    "courses": "Cours",
    "categories": "Catégories",
    "methodology": "Méthodologie",
    "how": "Fonctionnement",
    "search": "Rechercher des cours",
    "theme": "Utiliser le thème sombre",
    "breadcrumb": "Fil d’Ariane",
    "overall_recommendation": "Recommandation générale",
    "quality": "Qualité",
    "status_aria": "État du cours",
    "sections_aria": "Sections de la page du cours",
    "overview": "Vue d’ensemble",
    "details": "Détails",
    "evidence": "Éléments probants",
    "compared": "Comparaison",
    "why_recommend": "Pourquoi nous recommandons ce cours",
    "before_start": "Avant de commencer",
    "prerequisites": "Prérequis",
    "required_resources": "Ressources nécessaires",
    "scope": "Périmètre",
    "no_preparation": "Aucune exigence de préparation supplémentaire n’est documentée.",
    "what_free": "Ce qui est gratuit",
    "certificate": "Attestation",
    "academic_credit": "Crédits universitaires",
    "quality_review": "Évaluation de la qualité",
    "learning_need": "Besoin d’apprentissage",
    "why_value": "Pourquoi il apporte de la valeur",
    "admission_rationale": "Justification de la décision d’admission",
    "evidence_verification": "Éléments probants et vérification",
    "last_checked": "Dernière vérification",
    "next_review": "Prochaine révision prévue",
    "compared_against": "Comparé à",
    "no_comparator": "Aucun comparateur direct n’est enregistré pour ce cours.",
    "course_glance": "Le cours en bref",
    "provider": "Organisme",
    "language": "Langue",
    "level": "Niveau",
    "status": "État",
    "access": "Accès",
    "related_courses": "Cours associés",
    "no_related": "Aucun cours associé n’est actuellement lié.",
    "view_more": "Voir plus dans {category} →",
    "footer": "Sélectionné avec rigueur, auditable et maintenu en continu.",
    "course_source": "Source du cours",
    "repository_source": "Source du dépôt",
    "community_reference": "Référence communautaire",
    "supporting_source": "Source complémentaire",
    "active": "Actif",
    "archived": "Archivé",
    "archived_available": "Archivé mais toujours disponible",
    "banner_active": "Ce cours est actif",
    "banner_archived": "Ce cours est archivé",
    "banner_copy_active": "Vérifié le {verified} · prochaine révision {next_review}.",
    "banner_copy_archived": "Archivé mais toujours disponible · vérifié le {verified} · prochaine révision {next_review}.",
    "button_active": "Ouvrir le cours officiel →",
    "button_archived": "Voir les contenus archivés →",
}
LOCALE_QUALITY_COMPONENTS["fr"] = {
    "pedagogy": "Pédagogie",
    "depth": "Profondeur",
    "practice": "Pratique",
    "materials": "Supports",
    "currency": "Actualité",
    "expertise": "Expertise",
    "accessibility": "Accessibilité",
}
LOCALE_ACCESS_DETAIL["fr"] = {
    "F0": (
        "Cours complet + attestation gratuite",
        "Parcours d’apprentissage complet avec une attestation de réussite gratuite délivrée par le fournisseur.",
    ),
    "F1": (
        "Parcours évalué gratuit",
        "Parcours d’apprentissage complet avec une évaluation gratuite significative, mais sans attestation formelle gratuite.",
    ),
    "F2": (
        "Contenu pédagogique complet",
        "Contenu pédagogique substantiel et complet, mais sans parcours formel de validation gratuit.",
    ),
}


def locale_source_text(text: str, locale: str) -> str:
    if locale == "en" or not text:
        return text
    return translate_text(locale, text)


def locale_score(value: float, locale: str) -> str:
    formatted = f"{float(value):.1f}"
    decimal = LOCALE_CARD_COPY.get(locale, LOCALE_CARD_COPY["en"])["decimal"]
    return formatted if decimal == "." else formatted.replace(".", decimal)


def locale_category_label(course: dict, locale: str) -> str:
    return LOCALE_CATEGORY_LABELS.get(locale, {}).get(
        course["category"],
        course["category_name"],
    )


def locale_level_label(value: str, locale: str) -> str:
    return LOCALE_LEVEL_LABELS.get(locale, {}).get(value, label_level(value))


def locale_language_label(code: str, locale: str) -> str:
    return LOCALE_LANGUAGE_LABELS.get(locale, {}).get(code, label_language(code))


def locale_course_copy(course: dict, locale: str) -> tuple[str, str]:
    if locale == "en":
        return course["title"], course["why_recommended"]
    presentation = (course.get("presentations") or {}).get(locale)
    if presentation:
        return presentation["title"], presentation["description"]
    localized = localize_course(course, locale=locale)
    return localized["title"], localized["why_recommended"]


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


def format_review_month(value: str, locale: str = "en") -> str:
    year, month, _day = value.split("-")
    names = LOCALE_MONTHS.get(locale, LOCALE_MONTHS["en"])
    return f"{names[int(month) - 1]} {year}"


def static_catalogue_card(
    course: dict,
    href_prefix: str = "../",
    locale: str = "en",
    show_category: bool = True,
    media_root: str | None = None,
) -> str:
    title, rationale = locale_course_copy(course, locale)
    category = locale_category_label(course, locale)
    language_label = locale_language_label(course["primary_language"], locale)
    language_prefix = LOCALE_CARD_COPY.get(locale, LOCALE_CARD_COPY["en"])["language_prefix"]
    if locale in {"pt-PT", "es", "fr"}:
        language_label = language_label[0].lower() + language_label[1:]
    language = f"{language_prefix} {language_label}"
    level = locale_level_label(course["level"], locale)
    access = LOCALE_ACCESS_LABELS.get(locale, {}).get(
        course["access_short"],
        course["access_label"],
    )
    copy = LOCALE_CARD_COPY.get(locale, LOCALE_CARD_COPY["en"])
    rec_score = f'{float(course["recommendation_score"]):.1f}'
    quality_score = f'{float(course["quality_score"]):.1f}'
    if copy["decimal"] != ".":
        rec_score = rec_score.replace(".", copy["decimal"])
        quality_score = quality_score.replace(".", copy["decimal"])
    archive = (
        static_tag(copy["archived"], "tag-archive")
        if course["status"] == "active_archive"
        else ""
    )
    category_tag = static_tag(category, "tag-category") if show_category else ""
    if media_root is None:
        media_root = href_prefix
    return (
        '<article class="catalogue-card">'
        + media_html(course, root=media_root)
        + '<div class="card-body"><div class="card-heading">'
        + f'<p class="provider">{escape(course["provider"])}</p>'
        + f'<h3><a href="{href_prefix}courses/{escape(course["id"])}/">{escape(title)}</a></h3></div>'
        + '<div class="card-score-row">'
        + f'<span class="card-score card-score-primary" aria-label="{copy["recommendation"]} {rec_score} / 10"><strong>{rec_score}</strong><small>{copy["recommendation"]}</small></span>'
        + f'<span class="card-score" aria-label="{copy["quality"]} {quality_score} / 10"><strong>{quality_score}</strong><small>{copy["quality"]}</small></span>'
        + static_tag(course["quality_tier"], "tag-tier")
        + '</div>'
        + f'<p class="card-rationale">{escape(rationale)}</p>'
        + f'<div class="mini-tags">{category_tag}{static_tag(language)}{static_tag(level)}{archive}</div>'
        + '<div class="card-footer">'
        + f'<div class="access-line"><span data-icon="access" aria-hidden="true"></span><span>{escape(access)}</span></div>'
        + f'<span class="verified-line">{copy["verified"]} {escape(format_review_month(course["last_verified"], locale))}</span>'
        + '</div></div></article>'
    )


def static_catalogue_card_pt(
    course: dict,
    href_prefix: str = "../../",
    show_category: bool = True,
) -> str:
    return static_catalogue_card(
        course,
        href_prefix,
        locale="pt-PT",
        show_category=show_category,
    )


def original_title_html(course: dict, locale: str = "en") -> str:
    original = course.get("original_title")
    if not original or original == course["title"]:
        return ""
    original_language = {
        "openclassrooms-initiez-vous-gestion-projet": "fr",
        "fun-boite-outils-philosophie-politique": "fr",
        "fun-la-musique-quelle-histoire": "fr",
        "blcu-umoocs-elementary-spoken-chinese": "zh",
    }.get(course["id"], "en")
    label = LOCALE_COURSE_COPY[locale]["original_title"]
    return (
        f'<details class="original-title"><summary>{escape(label)}</summary>'
        f'<p lang="{original_language}">{escape(original)}</p></details>'
    )


def render_static_course(
    course: dict,
    course_by_id: dict,
    candidate_by_id: dict,
    locale: str = "en",
) -> str:
    if locale != "en":
        course = localize_course(course, locale=locale)

    copy = LOCALE_COURSE_COPY[locale]
    localized = locale != "en"
    site_root = "../../../" if localized else "../../"
    route = f"courses/{course['id']}/"
    url = locale_url(locale, route)

    locale_hrefs = {}
    for target in PUBLIC_LOCALES:
        prefix = LOCALE_META[target]["prefix"]
        target_route = f"{prefix}/{route}" if prefix else route
        locale_hrefs[target] = site_root + target_route

    editorial = course.get("editorial") or {}
    review = editorial.get("review") or {}
    admission = editorial.get("admission") or {}
    description = course.get("why_recommended", "")
    category_name = locale_category_label(course, locale)
    languages = " · ".join(
        locale_language_label(code, locale)
        for code in [course["primary_language"], *course.get("other_languages", [])]
    )
    level = locale_level_label(course["level"], locale)

    archived = course["status"] == "active_archive"
    status = copy["archived_available"] if archived else copy["active"]

    raw_certificate = CREDENTIAL_LABELS.get(
        course.get("certificate"),
        readable_id(course.get("certificate")),
    )
    certificate = review.get("credential") or locale_source_text(raw_certificate, locale)

    raw_credit = CREDIT_LABELS.get(
        course.get("academic_credits"),
        readable_id(course.get("academic_credits")),
    )
    credit = review.get("academic_credits") or locale_source_text(raw_credit, locale)

    access_label, access_description = LOCALE_ACCESS_DETAIL[locale].get(
        course["access_short"],
        (course["access_label"], course["access_description"]),
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
                item
                for item in course_by_id.values()
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

    related_html_parts = []
    for item in related_courses:
        related_title, _ = locale_course_copy(item, locale)
        related_html_parts.append(
            '<a class="related-course" href="../../courses/'
            + escape(item["id"])
            + '/"><span class="related-mark" data-icon="curated" aria-hidden="true"></span><span><strong>'
            + escape(related_title)
            + '</strong><small>'
            + escape(item["provider"])
            + '</small></span><span class="related-score">'
            + locale_score(item["recommendation_score"], locale)
            + '</span></a>'
        )
    related_html = "".join(related_html_parts)

    component_labels = LOCALE_QUALITY_COMPONENTS[locale]
    components = "".join(
        '<div class="component-item">'
        f'<span>{escape(component_labels.get(key, key.capitalize()))}</span>'
        f'<div class="component-meter" aria-hidden="true"><i style="width:{float(value) * 10}%"></i></div>'
        f'<strong>{locale_score(value, locale)}</strong></div>'
        for key, value in course["quality_components"].items()
    )

    evidence_urls = []
    for evidence_url in [*(review.get("evidence") or []), *(course.get("evidence") or [])]:
        if evidence_url not in evidence_urls:
            evidence_urls.append(evidence_url)

    evidence_items = []
    try:
        canonical_host = course["url"].split("/")[2].removeprefix("www.")
    except IndexError:
        canonical_host = ""

    for evidence_url in evidence_urls:
        try:
            host = evidence_url.split("/")[2].removeprefix("www.")
        except IndexError:
            host = "source"
        if host == canonical_host:
            source_kind = copy["course_source"]
        elif host == "github.com":
            source_kind = copy["repository_source"]
        elif host.startswith("forum.") or ".forum." in host:
            source_kind = copy["community_reference"]
        else:
            source_kind = copy["supporting_source"]
        evidence_items.append(
            f'<li><a href="{escape(evidence_url)}" target="_blank" rel="noopener noreferrer">'
            f'{escape(source_kind)} · {escape(host)} ↗</a></li>'
        )

    before_parts = []
    if review.get("prerequisites"):
        before_parts.append(
            f'<h3>{escape(copy["prerequisites"])}</h3><p>{escape(review["prerequisites"])}</p>'
        )
    if review.get("required_resources"):
        before_parts.append(
            f'<h3>{escape(copy["required_resources"])}</h3><p>{escape(review["required_resources"])}</p>'
        )
    if review.get("scope_notes"):
        before_parts.append(
            f'<h3>{escape(copy["scope"])}</h3><p>{escape(review["scope_notes"])}</p>'
        )
    before_html = "".join(before_parts) or f'<p>{escape(copy["no_preparation"])}</p>'

    score_parts = []
    if admission.get("learning_need"):
        score_parts.append(
            f'<h3>{escape(copy["learning_need"])}</h3><p>{escape(admission["learning_need"])}</p>'
        )
    if admission.get("marginal_value"):
        score_parts.append(
            f'<h3>{escape(copy["why_value"])}</h3><p>{escape(admission["marginal_value"])}</p>'
        )
    if admission.get("decision_rationale"):
        score_parts.append(
            f'<details class="editorial-details"><summary>{escape(copy["admission_rationale"])}</summary>'
            f'<p>{escape(admission["decision_rationale"])}</p></details>'
        )

    comparisons = []
    for item in comparison_ids:
        compared = course_by_id.get(item)
        if compared:
            compared_title, _ = locale_course_copy(compared, locale)
            comparisons.append(
                f'<li><a href="../../courses/{escape(item)}/">{escape(compared_title)}</a></li>'
            )
        else:
            candidate = candidate_by_id.get(item)
            if candidate and candidate.get("title"):
                label = locale_source_text(candidate["title"], locale)
            else:
                label = readable_id(item)
            comparisons.append(f'<li>{escape(label)}</li>')

    banner_title = copy["banner_archived"] if archived else copy["banner_active"]
    banner_copy = (
        copy["banner_copy_archived"] if archived else copy["banner_copy_active"]
    ).format(
        verified=course["last_verified"],
        next_review=course["next_review"],
    )
    banner_button = copy["button_archived"] if archived else copy["button_active"]

    recommendation_score = locale_score(course["recommendation_score"], locale)
    quality_score = locale_score(course["quality_score"], locale)
    status_tag = static_tag(
        copy["archived"] if archived else copy["active"],
        "tag-archive" if archived else "",
    )

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
            "educationalLevel": level,
            "provider": {"@type": "Organization", "name": course["provider"]},
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")

    home_href = "../../"
    courses_href = "../../courses/"
    categories_href = "../../categories/"
    methodology_href = "../../methodology/"
    how_href = "../../#how-it-works"
    styles_href = site_root + "styles.css"
    editorial_css_href = site_root + "editorial.css"
    icons_href = site_root + "icons.js"
    theme_href = site_root + "theme.js"

    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <link rel="canonical" href="{escape(url, quote=True)}">
{alternate_links(route)}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(course['title'], quote=True)} · Open Learning Index">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{escape(url, quote=True)}">
  <title>{escape(course['title'])} · Open Learning Index</title>
  <link rel="stylesheet" href="{styles_href}">
  <link rel="stylesheet" href="{editorial_css_href}">
  <script type="application/ld+json">{schema}</script>
</head>
<body>
  <a class="skip-link" href="#course-detail">{escape(copy["skip"])}</a>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="{home_href}" aria-label="{escape(copy["home_aria"])}">
        <span class="brand-symbol" data-icon="brand" aria-hidden="true"></span><span>Open Learning Index</span>
      </a>
      <nav class="main-nav" aria-label="{escape(copy["primary_nav"])}">
        <a href="{courses_href}">{escape(copy["courses"])}</a>
        <a href="{categories_href}">{escape(copy["categories"])}</a>
        <a href="{methodology_href}">{escape(copy["methodology"])}</a>
        <a href="{how_href}">{escape(copy["how"])}</a>
      </nav>
      <details class="mobile-nav">
        <summary aria-label="{escape(copy["open_nav"])}"><span class="menu-icon" aria-hidden="true"></span></summary>
        <nav aria-label="{escape(copy["mobile_nav"])}"><a href="{home_href}">{escape(copy["home"])}</a><a href="{courses_href}">{escape(copy["courses"])}</a><a href="{categories_href}">{escape(copy["categories"])}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="{how_href}">{escape(copy["how"])}</a></nav>
      </details>
      <div class="nav-actions"><a class="icon-link" href="{courses_href}" aria-label="{escape(copy["search"])}"><span data-icon="search" aria-hidden="true"></span></a>{language_control(locale, locale_hrefs)}<button class="theme-toggle" type="button" data-theme-toggle aria-label="{escape(copy["theme"])}" title="{escape(copy["theme"])}"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button></div>
    </div>
  </header>

  <main id="course-detail" class="shell course-page">
    <nav class="course-breadcrumbs" aria-label="{escape(copy["breadcrumb"])}">
      <a href="{home_href}">{escape(copy["home"])}</a><span>›</span>
      <a href="../../categories/{escape(course["category"])}/">{escape(category_name)}</a><span>›</span>
      <span>{escape(course["title"])}</span>
    </nav>

    <section class="course-title-grid">
      <div class="course-heading-main">
        <h1>{escape(course["title"])}</h1>
        {original_title_html(course, locale)}
        <p class="course-provider-line">{escape(course["provider"])}</p>
        <div class="course-meta-tags">
          {static_tag(category_name, "tag-category")}
          {static_tag(locale_language_label(course["primary_language"], locale))}
          {static_tag(level)}
          {status_tag}
        </div>
      </div>
      <aside class="course-score-card" aria-label="{escape(copy["overall_recommendation"])}">
        <span>{escape(copy["overall_recommendation"])}</span>
        <div class="course-score-main"><strong>{recommendation_score}</strong><small>/ 10</small></div>
        <div class="quality-line"><span>{escape(copy["quality"])}</span><strong>{quality_score}</strong></div>
        <div class="score-meter" aria-hidden="true"><i style="width:{float(course["quality_score"]) * 10}%"></i></div>
      </aside>
    </section>

    <section class="status-banner" aria-label="{escape(copy["status_aria"])}">
      <span class="status-banner-icon" data-icon="status" aria-hidden="true"></span>
      <div><strong>{escape(banner_title)}</strong><small>{escape(banner_copy)}</small></div>
      <a href="{escape(course["url"], quote=True)}" target="_blank" rel="noopener noreferrer">{escape(banner_button)}</a>
    </section>

    <nav class="course-tabs" aria-label="{escape(copy["sections_aria"])}">
      <a href="#overview">{escape(copy["overview"])}</a>
      <a href="#details">{escape(copy["details"])}</a>
      <a href="#quality">{escape(copy["quality"])}</a>
      <a href="#evidence">{escape(copy["evidence"])}</a>
      <a href="#alternatives">{escape(copy["compared"])}</a>
    </nav>

    <div class="course-layout">
      <div class="course-content">
        <section id="overview" class="content-section">
          <h2>{escape(copy["why_recommend"])}</h2>
          <p>{escape(description)}</p>
        </section>

        <section id="details" class="content-section">
          <h2>{escape(copy["before_start"])}</h2>
          {before_html}
        </section>

        <section class="content-section">
          <h2>{escape(copy["what_free"])}</h2>
          <p><strong>{escape(access_label)}</strong> — {escape(access_description)}</p>
          <p><strong>{escape(copy["certificate"])}:</strong> {escape(certificate)}</p>
          <p><strong>{escape(copy["academic_credit"])}:</strong> {escape(credit)}</p>
        </section>

        <section id="quality" class="content-section">
          <h2>{escape(copy["quality_review"])}</h2>
          <div class="quality-panel"><div class="component-grid">{components}</div></div>
          {"".join(score_parts)}
        </section>

        <section id="evidence" class="content-section">
          <h2>{escape(copy["evidence_verification"])}</h2>
          <p>{escape(copy["last_checked"])}: <strong>{escape(course["last_verified"])}</strong> · {escape(copy["next_review"])}: <strong>{escape(course["next_review"])}</strong>.</p>
          <ul class="evidence-list">{"".join(evidence_items)}</ul>
        </section>

        <section id="alternatives" class="content-section">
          <h2>{escape(copy["compared_against"])}</h2>
          {f'<ul class="comparison-list">{"".join(comparisons)}</ul>' if comparisons else f'<p>{escape(copy["no_comparator"])}</p>'}
        </section>
      </div>

      <aside class="course-sidebar">
        {media_html(course, root=site_root)}
        <section class="sidebar-card">
          <h2>{escape(copy["course_glance"])}</h2>
          <dl class="glance-list">
            <div><span class="glance-icon" data-icon="provider" aria-hidden="true"></span><dt>{escape(copy["provider"])}</dt><dd>{escape(course["provider"])}</dd></div>
            <div><span class="glance-icon" data-icon="globe" aria-hidden="true"></span><dt>{escape(copy["language"])}</dt><dd>{escape(languages)}</dd></div>
            <div><span class="glance-icon" data-icon="level" aria-hidden="true"></span><dt>{escape(copy["level"])}</dt><dd>{escape(level)}</dd></div>
            <div><span class="glance-icon" data-icon="clock" aria-hidden="true"></span><dt>{escape(copy["status"])}</dt><dd>{escape(status)}</dd></div>
            <div><span class="glance-icon" data-icon="access" aria-hidden="true"></span><dt>{escape(copy["access"])}</dt><dd>{escape(access_label)}</dd></div>
          </dl>
        </section>

        <section class="sidebar-card">
          <h2>{escape(copy["related_courses"])}</h2>
          <div class="related-list">{related_html or f'<p class="muted">{escape(copy["no_related"])}</p>'}</div>
          <p class="related-more"><a class="related-more-link" href="../../categories/{escape(course["category"])}/">{escape(copy["view_more"].format(category=category_name))}</a></p>
        </section>
      </aside>
    </div>
  </main>

  <footer class="site-footer"><div class="shell footer-inner">
    <div><strong>Open Learning Index</strong><p>{escape(copy["footer"])}</p></div>
    <div class="footer-links"><a href="{home_href}">{escape(copy["home"])}</a><a href="{courses_href}">{escape(copy["courses"])}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a></div>
  </div></footer>
  <script src="{icons_href}" defer></script>
  <script src="{theme_href}" defer></script>
</body>
</html>
"""


def render_static_course_pt(
    course: dict,
    course_by_id: dict,
    candidate_by_id: dict,
) -> str:
    return render_static_course(
        course,
        course_by_id,
        candidate_by_id,
        locale="pt-PT",
    )


def render_category_directory(
    category_rows: list[dict],
    courses: list[dict],
    locale: str = "en",
) -> str:
    copy = LOCALE_DIRECTORY_COPY[locale]
    localized = locale != "en"
    site_root = "../../" if localized else "../"
    route = "categories/"
    url = locale_url(locale, route)
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
        category_stub = {"category": category_id, "category_name": category["name"]}
        name = locale_category_label(category_stub, locale)
        leader = leaders.get(category_id)
        icon = CATEGORY_ICON_NAMES.get(category_id, "curated")
        course_count = counts.get(category_id, 0)
        count_label = copy["course"] if course_count == 1 else copy["courses"]
        if leader:
            leader_title, _ = locale_course_copy(leader, locale)
            leader_html = (
                f'<small>{escape(copy["top"])}: '
                f'<strong>{escape(leader_title)}</strong></small>'
            )
        else:
            leader_html = ""
        cards.append(
            f'<a class="category-directory-card" href="{escape(category_id + "/")}">'
            f'<span class="category-icon icon-{escape(category_id)}" data-icon="{escape(icon)}" aria-hidden="true"></span>'
            '<span class="category-directory-copy">'
            f'<strong>{escape(name)}</strong>'
            f'<span>{course_count} {escape(count_label)}</span>'
            f'{leader_html}</span>'
            '<span class="category-directory-arrow" data-icon="arrow" aria-hidden="true"></span>'
            '</a>'
        )

    locale_hrefs = {}
    for target in PUBLIC_LOCALES:
        prefix = LOCALE_META[target]["prefix"]
        target_route = f"{prefix}/categories/" if prefix else "categories/"
        locale_hrefs[target] = site_root + target_route

    title = copy["title"]
    kicker = f'{len(category_rows)} {copy["areas"]}'
    home_href = "../"
    courses_href = "../courses/"
    methodology_href = "../methodology/"
    how_href = "../#how-it-works"
    css_href = site_root + "styles.css"
    icons_href = site_root + "icons.js"
    theme_href = site_root + "theme.js"

    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(copy["intro"], quote=True)}">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <link rel="canonical" href="{escape(url, quote=True)}">
{alternate_links(route)}
  <title>{escape(title)} · Open Learning Index</title>
  <link rel="stylesheet" href="{css_href}">
  <link rel="stylesheet" href="{css_href.replace("styles.css", "editorial.css")}">
</head>
<body>
  <header class="topbar">
    <div class="shell topbar-inner">
      <a class="brand" href="{home_href}" aria-label="Open Learning Index"><span class="brand-symbol" data-icon="brand" aria-hidden="true"></span><span>Open Learning Index</span></a>
      <nav class="main-nav" aria-label="{escape(copy["primary_nav"])}">
        <a href="{courses_href}">{escape(copy["courses_nav"])}</a>
        <a class="active" href="./">{escape(title)}</a>
        <a href="{methodology_href}">{escape(copy["methodology"])}</a>
        <a href="{how_href}">{escape(copy["how"])}</a>
      </nav>
      <details class="mobile-nav"><summary aria-label="{escape(copy["open_nav"])}"><span class="menu-icon" aria-hidden="true"></span></summary>
        <nav aria-label="{escape(copy["mobile_nav"])}"><a href="{home_href}">{escape(copy["home"])}</a><a href="{courses_href}">{escape(copy["courses_nav"])}</a><a href="./">{escape(title)}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="{how_href}">{escape(copy["how"])}</a></nav>
      </details>
      <div class="nav-actions">
        <a class="icon-link" href="{courses_href}" aria-label="{escape(copy["search"])}"><span data-icon="search" aria-hidden="true"></span></a>
        {language_control(locale, locale_hrefs)}
        <button class="theme-toggle" type="button" data-theme-toggle aria-label="{escape(copy["theme"])}" title="{escape(copy["theme"])}"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button>
      </div>
    </div>
  </header>
  <main class="shell category-directory-page">
    <header class="category-directory-header">
      <p class="section-kicker">{escape(kicker)}</p>
      <h1>{escape(title)}</h1>
      <p>{escape(copy["intro"])}</p>
    </header>
    <div class="category-directory-grid">{"".join(cards)}</div>
  </main>
  <footer class="site-footer"><div class="shell footer-inner">
    <div><strong>Open Learning Index</strong><p>{escape(copy["footer"])}</p></div>
    <div class="footer-links"><a href="{home_href}">{escape(copy["home"])}</a><a href="{courses_href}">{escape(copy["courses_nav"])}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a></div>
  </div></footer>
  <script src="{icons_href}" defer></script>
  <script src="{theme_href}" defer></script>
</body>
</html>
"""

def render_static_category(
    category: dict,
    courses: list[dict],
    locale: str = "en",
) -> str:
    copy = LOCALE_CATEGORY_COPY[locale]
    localized = locale != "en"
    site_root = "../../../" if localized else "../../"
    category_id = category["id"]
    category_stub = {"category": category_id, "category_name": category["name"]}
    category_name = locale_category_label(category_stub, locale)

    rows = sorted(
        (course for course in courses if course["category"] == category_id),
        key=lambda item: (
            -float(item["recommendation_score"]),
            -float(item["quality_score"]),
            item["title"],
        ),
    )
    cards = "".join(
        static_catalogue_card(
            course,
            "../../",
            locale=locale,
            show_category=False,
            media_root=site_root,
        )
        for course in rows
    )

    route = f"categories/{category_id}/"
    url = locale_url(locale, route)
    locale_hrefs = {}
    for target in PUBLIC_LOCALES:
        prefix = LOCALE_META[target]["prefix"]
        target_route = f"{prefix}/{route}" if prefix else route
        locale_hrefs[target] = site_root + target_route

    count_template = copy["count_one"] if len(rows) == 1 else copy["count_many"]
    count_copy = count_template.format(count=len(rows))
    description = copy["description"].format(category=category_name)
    freshness_copy = copy["freshness"].get(category.get("freshness"), "")

    leader = rows[0] if rows else None
    if leader:
        leader_title, leader_rationale = locale_course_copy(leader, locale)
        leader_html = (
            f'<p><strong>{escape(copy["start"])}:</strong> '
            f'<a href="../../courses/{escape(leader["id"])}/">{escape(leader_title)}</a> — '
            f'{escape(leader_rationale)}</p>'
        )
    else:
        leader_html = ""

    home_href = "../../"
    courses_href = "../../courses/"
    categories_href = "../"
    methodology_href = "../../methodology/"
    how_href = "../../#how-it-works"
    css_href = site_root + "styles.css"
    icons_href = site_root + "icons.js"
    theme_href = site_root + "theme.js"

    return f"""<!doctype html>
<html lang="{locale}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <link rel="canonical" href="{escape(url, quote=True)}">
{alternate_links(route)}
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
      <nav class="main-nav" aria-label="{escape(copy["primary_nav"])}"><a href="{courses_href}">{escape(copy["courses"])}</a><a class="active" href="{categories_href}">{escape(copy["categories"])}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="{how_href}">{escape(copy["how"])}</a></nav>
      <details class="mobile-nav"><summary aria-label="{escape(copy["open_nav"])}"><span class="menu-icon" aria-hidden="true"></span></summary><nav aria-label="{escape(copy["mobile_nav"])}"><a href="{home_href}">{escape(copy["home"])}</a><a href="{courses_href}">{escape(copy["courses"])}</a><a href="{categories_href}">{escape(copy["categories"])}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="{how_href}">{escape(copy["how"])}</a></nav></details>
      <div class="nav-actions"><a class="icon-link" href="{courses_href}" aria-label="{escape(copy["search"])}"><span data-icon="search" aria-hidden="true"></span></a>{language_control(locale, locale_hrefs)}<button class="theme-toggle" type="button" data-theme-toggle aria-label="{escape(copy["theme"])}" title="{escape(copy["theme"])}"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button></div>
    </div>
  </header>
  <main class="shell category-page">
    <nav class="course-breadcrumbs" aria-label="{escape(copy["breadcrumb"])}"><a href="{categories_href}">{escape(copy["categories"])}</a><span>›</span><span>{escape(category_name)}</span></nav>
    <header class="category-page-header"><p class="section-kicker">{escape(copy["kicker"])}</p><h1>{escape(category_name)}</h1><p>{escape(count_copy)}</p></header>
    <section class="category-context"><p>{escape(freshness_copy)}</p>{leader_html}</section>
    <div class="course-grid catalogue-grid">{cards}</div>
  </main>
  <footer class="site-footer"><div class="shell footer-inner"><div><strong>Open Learning Index</strong><p>{escape(copy["footer"])}</p></div><div class="footer-links"><a href="{home_href}">{escape(copy["home"])}</a><a href="{courses_href}">{escape(copy["courses"])}</a><a href="{categories_href}">{escape(copy["categories"])}</a><a href="{methodology_href}">{escape(copy["methodology"])}</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a></div></div></footer>
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
        item["presentations"] = {}
        for locale in SUPPORTED_PRESENTATION_LOCALES:
            localized = localize_course(item, locale=locale)
            item["presentations"][locale] = {
                "title": localized["title"],
                "description": localized["why_recommended"],
            }
        # Backwards-compatible projection retained while the runtime still accepts
        # the pre-generic Portuguese payload.
        item["presentation_pt"] = dict(item["presentations"]["pt-PT"])
        for locale in SUPPORTED_PRESENTATION_LOCALES:
            presentation = item["presentations"][locale]
            category_label = LOCALE_CATEGORY_LABELS.get(locale, {}).get(
                item["category"],
                item["category_name"],
            )
            item["search_text"] += (
                " " + presentation["title"]
                + " " + presentation["description"]
                + " " + category_label
            )
        item["search_text"] = normalize_search_text(item["search_text"])
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
        "latest_verification": max(course["last_verified"] for course in public_courses),
        "source_files": ["data/courses.json", "data/categories.json", "data/candidates.json"],
    }

    write_json(output / "data" / "catalog.json", public_courses)
    write_json(output / "data" / "categories.json", category_rows)
    write_json(output / "data" / "meta.json", meta)

    # Keep the homepage useful even if JavaScript is unavailable or fails to load.
    # The runtime still re-hydrates these values from data/meta.json.
    for locale in PUBLIC_LOCALES:
        prefix = LOCALE_META[locale]["prefix"]
        locale_root = output / prefix if prefix else output
        homepage = locale_root / "index.html"
        html = homepage.read_text(encoding="utf-8")
        stat_values = {
            "stat-courses": str(meta["published_count"]),
            "stat-categories": str(meta["category_count"]),
            "stat-languages": str(meta["language_count"]),
            "stat-verified": format_review_month(meta["latest_verification"], locale),
        }
        for element_id, value in stat_values.items():
            pattern = rf'(<strong id="{re.escape(element_id)}">)[^<]*(</strong>)'
            html, count = re.subn(pattern, rf'\g<1>{value}\g<2>', html, count=1)
            if count != 1:
                raise SystemExit(
                    f"ERROR: homepage stat placeholder missing for {locale}: {element_id}"
                )
        write_text(homepage, html)

    course_by_id = {course["id"]: course for course in public_courses}
    for locale in PUBLIC_LOCALES:
        prefix = LOCALE_META[locale]["prefix"]
        locale_root = output / prefix if prefix else output

        for course in public_courses:
            write_text(
                locale_root / "courses" / course["id"] / "index.html",
                render_static_course(
                    course,
                    course_by_id,
                    candidate_by_id,
                    locale=locale,
                ),
            )

        write_text(
            locale_root / "categories" / "index.html",
            render_category_directory(category_rows, public_courses, locale=locale),
        )

        for category in category_rows:
            write_text(
                locale_root / "categories" / category["id"] / "index.html",
                render_static_category(category, public_courses, locale=locale),
            )

    sitemap_urls = []
    for locale in PUBLIC_LOCALES:
        prefix = LOCALE_META[locale]["prefix"]
        locale_base = f"{BASE_URL}/{prefix}/" if prefix else f"{BASE_URL}/"
        sitemap_urls.extend(
            [
                locale_base,
                locale_base + "courses/",
                locale_base + "categories/",
                locale_base + "methodology/",
            ]
        )
        sitemap_urls.extend(
            locale_base + f"courses/{course['id']}/"
            for course in public_courses
        )
        sitemap_urls.extend(
            locale_base + f"categories/{category['id']}/"
            for category in category_rows
        )
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
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#ffffff">
  {THEME_BOOTSTRAP}
  <title>Page not found · Open Learning Index</title>
  <link rel="stylesheet" href="/open-learning-index/styles.css">
  <link rel="stylesheet" href="/open-learning-index/editorial.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="topbar"><div class="shell topbar-inner">
    <a class="brand" href="/open-learning-index/" aria-label="Open Learning Index home"><span class="brand-symbol" data-icon="brand" aria-hidden="true"></span><span>Open Learning Index</span></a>
    <nav class="main-nav" aria-label="Primary navigation"><a href="/open-learning-index/">Home</a><a href="/open-learning-index/courses/">Courses</a><a href="/open-learning-index/categories/">Categories</a><a href="/open-learning-index/methodology/">Methodology</a></nav>
    <div class="nav-actions"><a class="language-switch" href="/open-learning-index/pt/" lang="pt-PT" hreflang="pt-PT">PT-PT</a><button class="theme-toggle" type="button" data-theme-toggle aria-label="Use dark theme" title="Use dark theme"><span data-theme-icon data-icon="moon" aria-hidden="true"></span></button></div>
  </div></header>
  <main id="main-content" class="shell not-found-page"><section class="empty"><p class="section-kicker">404</p><h1>Page not found</h1><p>That Open Learning Index page does not exist or has moved.</p><div class="methodology-actions"><a class="button button-primary" href="/open-learning-index/courses/">Browse courses</a><a class="button button-ghost" href="/open-learning-index/">Return home</a></div></section></main>
  <footer class="site-footer"><div class="shell footer-inner"><div><strong>Open Learning Index</strong><p>Curated, auditable and continuously maintained.</p></div><div class="footer-links"><a href="/open-learning-index/">Home</a><a href="/open-learning-index/courses/">Courses</a><a href="/open-learning-index/methodology/">Methodology</a><a href="https://github.com/Blackspirits/open-learning-index">GitHub</a></div></div></footer>
  <script src="/open-learning-index/icons.js" defer></script>
  <script src="/open-learning-index/theme.js" defer></script>
</body>
</html>""",
    )

    required = [
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
    for locale in PUBLIC_LOCALES:
        prefix = LOCALE_META[locale]["prefix"]
        locale_root = output / prefix if prefix else output
        required.extend(
            [
                locale_root / "index.html",
                locale_root / "courses" / "index.html",
                locale_root / "categories" / "index.html",
                locale_root / "methodology" / "index.html",
            ]
        )
        required.extend(
            locale_root / "courses" / course["id"] / "index.html"
            for course in public_courses
        )
        required.extend(
            locale_root / "categories" / category["id"] / "index.html"
            for category in category_rows
        )
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
