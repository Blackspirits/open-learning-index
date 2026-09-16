"""Presentation-only localisation and artwork. Canonical records are never changed."""
import copy
import json
from html import escape
from pathlib import Path

SITE = Path(__file__).resolve().parents[1] / 'site'


def read_map(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


_TRANSLATION_CACHE = {}


def translations_for(locale):
    if locale not in _TRANSLATION_CACHE:
        path = SITE / 'locales' / f'{locale}.json'
        if not path.exists():
            raise ValueError(f'Unsupported presentation locale: {locale}')
        _TRANSLATION_CACHE[locale] = read_map(path)
    return _TRANSLATION_CACHE[locale]


def translate_text(locale, text):
    if not text:
        return text
    translations = translations_for(locale)
    if text not in translations:
        language = {'pt-PT': 'Portuguese'}.get(locale, locale)
        raise ValueError(f'Missing {language} presentation translation: {text[:100]}')
    return translations[text]


# Backwards-compatible alias retained while callers move to locale-generic helpers.
TRANSLATIONS = translations_for('pt-PT')


def pt(text):
    return translate_text('pt-PT', text)


def localize_course(course, locale='pt-PT'):
    item = copy.deepcopy(course)
    item['original_title'] = course['title']
    item['title'] = translate_text(locale, course['title'])
    item['why_recommended'] = translate_text(locale, course['why_recommended'])
    for section, keys in {
        'review': ('prerequisites','required_resources','scope_notes','credential','academic_credits','recommendation_rationale'),
        'admission': ('learning_need','marginal_value','decision_rationale'),
    }.items():
        block = item.get('editorial', {}).get(section, {})
        for key in keys:
            if block.get(key):
                block[key] = translate_text(locale, block[key])
    return item


MEDIA = read_map(SITE / 'assets/course-media.json')
ICONS = dict(zip(
    ['ai-data','arts-design','business-entrepreneurship','computer-science','cybersecurity-it','education-teaching','engineering-electronics','finance-economics','health-medicine','history-culture','humanities-philosophy','languages','law-public-policy','marketing-sales','math-statistics','natural-sciences','project-product-leadership','psychology-behavior','writing-communication'],
    ['ai','palette','business','code','shield','education','engineering','finance','health','history','humanities','languages','law','marketing','math','science','leadership','brain','writing']))


def media_for(course):
    record = MEDIA.get(course['id'])
    if (
        record
        and record.get('published') is True
        and record.get('rights_status') == 'verified_reuse'
        and record.get('src')
    ):
        return {'src':record['src'], 'kind':record['kind']}
    return {'kind':'editorial','icon':ICONS.get(course['category'],'education')}


def media_html(course, root='../../', eager=False):
    media = media_for(course)
    if media.get('src'):
        return (f'<div class="course-media media-{escape(media["kind"])}" aria-hidden="true">'
                f'<img src="{root}{escape(media["src"])}" alt="" width="800" height="450" '
                f'loading="{"eager" if eager else "lazy"}" decoding="async"></div>')
    return (f'<div class="course-media media-editorial media-{escape(course["category"])}" aria-hidden="true">'
            f'<span class="media-symbol" data-icon="{escape(media["icon"])}"></span>'
            f'<span class="media-provider-name">{escape(course["provider"])}</span></div>')
