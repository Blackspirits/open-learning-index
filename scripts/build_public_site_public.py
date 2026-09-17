#!/usr/bin/env python3
"""Build the public site with every fully reviewed public presentation locale.

This thin configuration layer keeps the stable publication builder unchanged while
adding a reviewed locale only after its editorial dictionary has reached full
coverage. Canonical course/review/admission data are never modified here.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import build_public_site as build


FR_CATEGORY_LABELS = {
    "ai-data": "IA et données",
    "arts-design": "Arts et design",
    "business-entrepreneurship": "Entreprise et entrepreneuriat",
    "computer-science": "Informatique et logiciels",
    "cybersecurity-it": "Cybersécurité et IT",
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
    "undergraduate": "Licence",
    "graduate": "Études supérieures",
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


def configure_french() -> None:
    build.SUPPORTED_PRESENTATION_LOCALES = ("pt-PT", "es", "fr")
    build.PUBLIC_LOCALES = ("en", *build.SUPPORTED_PRESENTATION_LOCALES)
    build.LOCALE_META["fr"] = {"prefix": "fr", "label": "Français", "short": "FR"}
    build.LOCALE_ROUTE_PREFIX["fr"] = "fr"

    build.LOCALE_CATEGORY_LABELS["fr"] = FR_CATEGORY_LABELS
    build.LOCALE_LEVEL_LABELS["fr"] = FR_LEVEL_LABELS
    build.LOCALE_LANGUAGE_LABELS["fr"] = FR_LANGUAGE_LABELS
    build.LOCALE_ACCESS_LABELS["fr"] = {
        "F0": "Cours et attestation gratuits",
        "F1": "Parcours complet avec évaluation",
        "F2": "Contenu pédagogique complet gratuit",
    }
    build.LOCALE_CARD_COPY["fr"] = {
        "recommendation": "Recommandation",
        "quality": "Qualité",
        "verified": "Vérifié",
        "archived": "Archivé",
        "language_prefix": "En",
        "decimal": ",",
    }
    build.LOCALE_MONTHS["fr"] = (
        "janv.", "févr.", "mars", "avr.", "mai", "juin",
        "juil.", "août", "sept.", "oct.", "nov.", "déc.",
    )
    build.LOCALE_DIRECTORY_COPY["fr"] = {
        "title": "Catégories",
        "areas": "domaines d’apprentissage",
        "intro": "Explorez tous les domaines de l’index. Chaque catégorie ne contient que des cours ayant franchi le processus éditorial et de vérification.",
        "top": "Le plus recommandé",
        "course": "cours",
        "courses": "cours",
        "home": "Accueil",
        "courses_nav": "Cours",
        "methodology": "Méthodologie",
        "how": "Comment ça marche",
        "footer": "Sélectionné avec rigueur, auditable et maintenu en continu.",
        "primary_nav": "Navigation principale",
        "mobile_nav": "Navigation mobile",
        "open_nav": "Ouvrir la navigation",
        "search": "Rechercher des cours",
        "theme": "Utiliser le thème sombre",
    }
    build.LOCALE_CATEGORY_COPY["fr"] = {
        "kicker": "Catégorie",
        "home": "Accueil",
        "courses": "Cours",
        "categories": "Catégories",
        "methodology": "Méthodologie",
        "how": "Comment ça marche",
        "description": "Cours gratuits sélectionnés en {category} dans Open Learning Index.",
        "count_one": "{count} cours sélectionné, classé par Recommandation.",
        "count_many": "{count} cours sélectionnés, classés par Recommandation.",
        "start": "Commencez ici",
        "footer": "Sélectionné avec rigueur, auditable et maintenu en continu.",
        "primary_nav": "Navigation principale",
        "mobile_nav": "Navigation mobile",
        "open_nav": "Ouvrir la navigation",
        "search": "Rechercher des cours",
        "breadcrumb": "Fil d’Ariane",
        "theme": "Utiliser le thème sombre",
        "freshness": {
            "fast": "Domaine à évolution rapide : ces cours utilisent des intervalles de révision plus courts car les outils, normes ou plateformes peuvent changer rapidement.",
            "medium": "Domaine activement maintenu : l’accès, le contenu et les changements du fournisseur sont revérifiés à une fréquence modérée.",
            "slow": "Domaine aux fondements stables : l’ancienneté seule n’est pas considérée comme un défaut, mais l’accès et la qualité comparative restent revérifiés.",
        },
    }
    build.LOCALE_COURSE_COPY["fr"] = {
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
        "how": "Comment ça marche",
        "search": "Rechercher des cours",
        "theme": "Utiliser le thème sombre",
        "breadcrumb": "Fil d’Ariane",
        "overall_recommendation": "Recommandation globale",
        "quality": "Qualité",
        "status_aria": "Statut du cours",
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
        "no_preparation": "Aucun besoin de préparation supplémentaire n’est documenté.",
        "what_free": "Ce qui est gratuit",
        "certificate": "Attestation",
        "academic_credit": "Crédits académiques",
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
        "provider": "Fournisseur",
        "language": "Langue",
        "level": "Niveau",
        "status": "Statut",
        "access": "Accès",
        "related_courses": "Cours associés",
        "no_related": "Aucun cours associé n’est actuellement lié.",
        "view_more": "Voir plus en {category} →",
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
        "banner_copy_active": "Vérifié {verified} · prochaine révision {next_review}.",
        "banner_copy_archived": "Archivé mais toujours disponible · vérifié {verified} · prochaine révision {next_review}.",
        "button_active": "Ouvrir le cours officiel →",
        "button_archived": "Voir les ressources archivées →",
    }
    build.LOCALE_QUALITY_COMPONENTS["fr"] = {
        "pedagogy": "Pédagogie",
        "depth": "Profondeur",
        "practice": "Pratique",
        "materials": "Ressources",
        "currency": "Actualité",
        "expertise": "Expertise",
        "accessibility": "Accessibilité",
    }
    build.LOCALE_ACCESS_DETAIL["fr"] = {
        "F0": (
            "Cours complet + attestation gratuite",
            "Parcours d’apprentissage complet avec une attestation de fin gratuite délivrée par le fournisseur.",
        ),
        "F1": (
            "Parcours évalué gratuit",
            "Parcours d’apprentissage complet avec une évaluation gratuite significative, mais sans attestation formelle gratuite.",
        ),
        "F2": (
            "Contenu pédagogique complet",
            "Contenu pédagogique substantiel et complet, mais sans parcours formel de fin gratuit.",
        ),
    }


def patch_static_shells(output: Path) -> None:
    """Add French alternates/menu links to the pre-existing hand-authored shells."""
    routes = {
        Path("index.html"): ("", "fr/"),
        Path("courses/index.html"): ("courses/", "../fr/courses/"),
        Path("methodology/index.html"): ("methodology/", "../fr/methodology/"),
        Path("pt/index.html"): ("", "../fr/"),
        Path("pt/courses/index.html"): ("courses/", "../../fr/courses/"),
        Path("pt/methodology/index.html"): ("methodology/", "../../fr/methodology/"),
        Path("es/index.html"): ("", "../fr/"),
        Path("es/courses/index.html"): ("courses/", "../../fr/courses/"),
        Path("es/methodology/index.html"): ("methodology/", "../../fr/methodology/"),
    }
    for rel, (route, href) in routes.items():
        path = output / rel
        if not path.exists():
            continue
        html = path.read_text(encoding="utf-8")
        if 'hreflang="fr"' not in html:
            alternate = f'  <link rel="alternate" hreflang="fr" href="{build.BASE_URL}/fr/{route}">\n'
            marker = '  <link rel="alternate" hreflang="x-default"'
            if marker in html:
                html = html.replace(marker, alternate + marker, 1)
            else:
                html = html.replace("  <title>", alternate + "  <title>", 1)
        menu = re.search(r'(<details class="language-menu">.*?<nav[^>]*>)(.*?)(</nav></details>)', html, re.S)
        if menu and 'hreflang="fr"' not in menu.group(2):
            replacement = menu.group(1) + menu.group(2) + f'<a href="{href}" lang="fr" hreflang="fr">Français</a>' + menu.group(3)
            html = html[:menu.start()] + replacement + html[menu.end():]
        path.write_text(html, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=build.DEFAULT_OUTPUT)
    args = parser.parse_args()
    configure_french()
    output = args.output.resolve()
    build.build(output)
    patch_static_shells(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
