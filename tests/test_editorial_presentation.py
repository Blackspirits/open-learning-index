"""Protect the bilingual presentation boundary and static media delivery."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_public_site as build
from editorial_presentation import localize_course, media_for, media_html, pt, translate_text, translations_for, MEDIA


class EditorialPresentationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        courses = json.loads(build.COURSES.read_text(encoding='utf-8'))
        categories = {c['id']:c for c in json.loads(build.CATEGORIES.read_text(encoding='utf-8'))}
        reviews = build.load_current_records(build.REVIEWS_DIR, 'reviewed_on')
        references = build.load_current_records(build.REFERENCE_REVIEWS, 'reviewed_on', 'course_id')
        admissions = build.load_current_records(build.ADMISSIONS_DIR, 'decided_on')
        cls.reviews = reviews
        cls.courses = []
        for course in courses:
            if build.is_publication_eligible(course):
                item = build.build_public_course(course, categories)
                item['editorial'] = build.editorial_projection(course, reviews, references, admissions)
                cls.courses.append(item)

    def test_every_published_course_has_complete_localisation_without_mutation(self):
        for course in self.courses:
            with self.subTest(course=course['id']):
                before = copy.deepcopy(course)
                translated = localize_course(course)
                self.assertEqual(course, before)
                for field in ('id','url','primary_language','other_languages','quality_components','quality_score','recommendation_score','free_access','status','last_verified','next_review'):
                    self.assertEqual(translated[field], course[field])
                self.assertEqual(translated['original_title'], course['title'])
                self.assertTrue(translated['title'])
                self.assertTrue(translated['why_recommended'])

    def test_missing_translation_blocks_silent_english_fallback(self):
        with self.assertRaisesRegex(ValueError, 'Missing Portuguese'):
            pt('A newly edited sentence without a reviewed translation entry.')

    def test_localisation_helpers_are_locale_generic_without_changing_pt_pt(self):
        self.assertIs(translations_for('pt-PT'), translations_for('pt-PT'))
        source = self.courses[0]['title']
        self.assertEqual(translate_text('pt-PT', source), pt(source))
        translated = localize_course(self.courses[0], locale='pt-PT')
        self.assertEqual(translated['title'], pt(source))
        with self.assertRaisesRegex(ValueError, 'Unsupported presentation locale'):
            translations_for('zz-ZZ')

    def test_known_machine_translation_semantic_traps_are_blocked(self):
        translations = build.translate_pt.__globals__['TRANSLATIONS']
        values = list(translations.values())
        self.assertFalse(any('24 horas por dia' in value for value in values))
        self.assertFalse(any('moeda 10.0' in value.lower() or 'moeda 10,0' in value.lower() for value in values))

    def test_unverified_third_party_media_falls_back_to_original_editorial_panels(self):
        course = next(c for c in self.courses if c['id'] == 'harvard-cs50x')
        index = {c['id']:c for c in self.courses}
        en = build.render_static_course(course, index, {})
        translated = build.render_static_course_pt(course, index, {})
        self.assertNotIn('assets/courses/harvard-cs50x.webp', en)
        self.assertNotIn('assets/courses/harvard-cs50x.webp', translated)
        self.assertIn('media-editorial', en)
        self.assertNotIn('F0 ·', translated)
        self.assertIn('Título original', translated)
        self.assertIn('CS50: Introdução à ciência de computadores', translated)
        self.assertIn('Ciência de Computadores e Software</a>', translated)

    def test_pt_pt_audit_global_invariants(self):
        translations = build.translate_pt.__globals__['TRANSLATIONS']
        legacy_ao90 = (
            'excepcional', 'excepcionalmente', 'actuais', 'actual', 'activo',
            'interactivo', 'interactiva', 'interactivos', 'interactivas',
            'projecto', 'concepção', 'reacção', 'auto-formativo',
            'co-requisito', 'vídeo-aulas',
        )
        for source, value in translations.items():
            with self.subTest(source=source[:100]):
                self.assertNotIn('\\u200b', value)
                lowered = value.lower()
                for forbidden in legacy_ao90:
                    self.assertNotIn(forbidden.lower(), lowered)
                if 'lecture' in source.lower():
                    self.assertNotIn('palestra', lowered)
                if 'badge' in source.lower():
                    self.assertNotIn('crachá', lowered)
                    self.assertNotIn('selo', lowered)
                    self.assertNotIn('distintivo', lowered)
                    if 'emblema' in lowered:
                        self.assertTrue('emblema digital' in lowered or 'emblemas digitais' in lowered)
                if source.lower().startswith(('browser', 'web browser')):
                    self.assertNotIn('Browser', value)
                if 'european-portuguese' in source.lower():
                    self.assertNotIn('europeu-português', lowered)
                    self.assertNotIn('entre europeu e português', lowered)
                if 'currency' in source.lower():
                    self.assertNotIn('moeda', lowered)
                    self.assertNotIn('monetári', lowered)
                if ('live' in source.lower() and
                        ('exam' in source.lower() or 'certification' in source.lower())):
                    self.assertNotIn('ao vivo', lowered)
                    self.assertNotIn('em direto', lowered)

    def test_pt_pt_medium_agreement_regressions_are_blocked(self):
        translations = build.translate_pt.__globals__['TRANSLATIONS']
        values = list(translations.values())
        forbidden = (
            'um função',
            'o seu função',
            'percurso interativo gratuita',
            'percurso OCW gratuita',
            'percurso interativo completo é executada',
            'percurso de vendas dedicada',
            'Percurso de segurança de endpoint densa',
        )
        for value in values:
            for bad in forbidden:
                self.assertNotIn(bad, value)

    def test_pt_pt_low_independent_pass_01_regressions_are_blocked(self):
        translations = build.translate_pt.__globals__['TRANSLATIONS']
        forbidden = (
            'permanece mais ampla',
            'quatro exames e um final',
            'vendor training',
            'Introduction to Data Science de Dados',
            'um trabalho intercalar e um final',
            'é um atual especialista',
            'Relaunch atualizado',
            'Data Sharing course',
            'múltiplas frameworks',
            'várias frameworks',
            'na cloud',
            'um final com soluções completas',
            'Atual especialista',
        )
        for source, value in translations.items():
            with self.subTest(source=source[:100]):
                for bad in forbidden:
                    self.assertNotIn(bad, value)

    def test_pt_pt_low_independent_pass_02_regressions_are_blocked(self):
        translations = build.translate_pt.__globals__['TRANSLATIONS']
        for source, value in translations.items():
            with self.subTest(source=source[:100]):
                self.assertNotIn('uma curso', value)
                self.assertNotIn('curso panorâmico completo de ciência política que não é substituída', value)

    def test_pt_pt_low_independent_pass_03_regressions_are_blocked(self):
        translations = build.translate_pt.__globals__['TRANSLATIONS']
        for source, value in translations.items():
            with self.subTest(source=source[:100]):
                self.assertNotIn('(enforcement)', value)
                self.assertNotIn('(clickers)', value)

    def test_pt_pt_language_labels_are_complete_and_consistently_lowercase(self):
        language_codes = {
            code
            for course in self.courses
            for code in [course['primary_language'], *course.get('other_languages', [])]
        }
        self.assertTrue(language_codes.issubset(build.PT_LANGUAGE_LABELS))
        for code in sorted(language_codes):
            with self.subTest(code=code):
                label = build.PT_LANGUAGE_LABELS[code]
                first_alpha = next((char for char in label if char.isalpha()), '')
                self.assertTrue(first_alpha)
                self.assertEqual(first_alpha, first_alpha.lower())

    def test_catalogue_level_filter_uses_pedagogical_progression(self):
        app_js = (ROOT / 'site' / 'app.js').read_text(encoding='utf-8')
        match = __import__('re').search(
            r'const levelOrder = \[(.*?)\];',
            app_js,
            flags=__import__('re').S,
        )
        self.assertIsNotNone(match)
        actual = __import__('re').findall(r'"([^"]+)"', match.group(1))
        self.assertEqual(
            actual,
            [
                'beginner',
                'beginner_to_intermediate',
                'intermediate',
                'intermediate_to_advanced',
                'advanced',
                'undergraduate',
                'graduate',
                'beginner_to_advanced',
            ],
        )
        self.assertIn('Progressão', app_js)
        self.assertIn('Abrangente', app_js)
        self.assertIn('Adequado a principiantes', app_js)
        self.assertIn('optgroup', app_js)


    def test_english_learner_facing_review_prose_has_no_portuguese_leakage(self):
        import re
        # These fields are projected directly into the English course page before
        # pt-PT localisation. Accented Portuguese tokens here indicate a source-
        # language boundary regression, not merely an untranslated UI label.
        portuguese = re.compile(
            r'\\b(?:nenhum|nenhuma|gratuit[oa]s?|avaliação|certificação|certificado|'
            r'navegador|aprendentes?|percurso|ensino|conteúdo|pré-requisitos?|'
            r'créditos? académicos?|línguas?)\\b',
            flags=re.IGNORECASE,
        )
        learner_fields = (
            'credential',
            'academic_credits',
            'scope_notes',
            'prerequisites',
            'required_resources',
            'recommendation_rationale',
        )
        for course_id, review in self.reviews.items():
            for field in learner_fields:
                value = review.get(field)
                if not value:
                    continue
                with self.subTest(course=course_id, field=field):
                    self.assertIsNone(
                        portuguese.search(value),
                        f'Portuguese leaked into English source field {course_id}.{field}: {value}',
                    )

    def test_public_course_pages_hide_internal_calibration_jargon(self):
        index = {course['id']: course for course in self.courses}
        forbidden = ('pre-pipeline', 'reference-fixture reconciliation', 'recalibration trims')
        for course in self.courses:
            html = build.render_static_course(course, index, {})
            for phrase in forbidden:
                with self.subTest(course=course['id'], phrase=phrase):
                    self.assertNotIn(phrase, html.lower())


    def test_catalogue_cards_surface_decision_data_without_decorative_media(self):
        course = self.courses[0]
        html = build.static_catalogue_card(course)
        self.assertIn('card-score-row', html)
        self.assertIn('card-rationale', html)
        self.assertIn('verified-line', html)
        self.assertIn(f'{course["quality_score"]:.1f}', html)
        self.assertIn(course['quality_tier'], html)
        self.assertIn(course['why_recommended'], html)
        self.assertNotIn('course-media', html)
        self.assertNotIn('media-provider-name', html)

    def test_catalogue_search_supports_prefix_matching(self):
        app_js = (ROOT / 'site' / 'app.js').read_text(encoding='utf-8')
        self.assertIn('token.startsWith(word)', app_js)
        self.assertIn('word.length >= 2', app_js)

    def test_access_icon_does_not_signal_a_locked_course(self):
        icons_js = (ROOT / 'site' / 'icons.js').read_text(encoding='utf-8')
        self.assertIn('access:', icons_js)
        self.assertNotIn('M7 11V8a5 5 0 0 1 10 0v3', icons_js)


    def test_category_cards_can_drop_redundant_category_labels(self):
        course = self.courses[0]
        normal = build.static_catalogue_card(course)
        category_page = build.static_catalogue_card(course, show_category=False)
        self.assertIn('tag-category', normal)
        self.assertNotIn('tag-category', category_page)
        self.assertIn(course['why_recommended'], category_page)
        self.assertIn('verified-line', category_page)

    def test_public_evidence_labels_are_descriptive_not_numbered(self):
        index = {course['id']: course for course in self.courses}
        course = next(c for c in self.courses if c.get('editorial', {}).get('review', {}).get('evidence'))
        html = build.render_static_course(course, index, {})
        self.assertNotIn(' · source 1', html)
        self.assertNotIn(' · source 2', html)
        self.assertRegex(
            html,
            r'(Course source|Repository source|Community reference|Supporting source) · ',
        )

    def test_methodology_routes_exist_in_both_public_locales(self):
        self.assertTrue((ROOT / 'site' / 'methodology' / 'index.html').is_file())
        self.assertTrue((ROOT / 'site' / 'pt' / 'methodology' / 'index.html').is_file())
        en = (ROOT / 'site' / 'methodology' / 'index.html').read_text(encoding='utf-8')
        pt_page = (ROOT / 'site' / 'pt' / 'methodology' / 'index.html').read_text(encoding='utf-8')
        self.assertIn('Quality Score', en)
        self.assertIn('F0', en)
        self.assertIn('Manutenção contínua', pt_page)
        self.assertIn('F0', pt_page)

    def test_course_navigation_keeps_methodology_on_site(self):
        index = {course['id']: course for course in self.courses}
        html = build.render_static_course(self.courses[0], index, {})
        self.assertIn('href="../../methodology/">Methodology</a>', html)
        self.assertNotIn('github.com/Blackspirits/open-learning-index/blob/main/docs/methodology.md', html)


    def test_catalogue_runtime_uses_locale_keyed_presentation_payloads(self):
        app_js = (ROOT / 'site' / 'app.js').read_text(encoding='utf-8')
        self.assertIn('course.presentations?.[locale]', app_js)
        self.assertIn('localeRoutePrefixes', app_js)
        self.assertNotIn('return isPt ? course.presentation_pt.why_recommended', app_js)

        for course in self.courses:
            localized = localize_course(course, locale='pt-PT')
            presentation = {
                'title': localized['title'],
                'description': localized['why_recommended'],
            }
            with self.subTest(course=course['id']):
                self.assertTrue(presentation['description'])
                self.assertEqual(presentation['description'], localized['why_recommended'])



    def test_public_build_declares_locale_keyed_presentations(self):
        builder = (ROOT / 'scripts' / 'build_public_site.py').read_text(encoding='utf-8')
        self.assertIn('SUPPORTED_PRESENTATION_LOCALES = ("pt-PT",)', builder)
        self.assertIn('item["presentations"][locale]', builder)
        self.assertIn('item["presentation_pt"] = dict(item["presentations"]["pt-PT"])', builder)

    def test_functional_control_borders_use_accessible_tokens(self):
        css = (ROOT / 'site' / 'styles.css').read_text(encoding='utf-8')
        self.assertIn('--control-border: #7d919c;', css)
        self.assertIn('--control-border: #526b77;', css)
        self.assertIn('border: 1px solid var(--control-border);', css)

    def test_course_media_requires_explicit_reuse_rights_before_publication(self):
        for course_id, media in MEDIA.items():
            with self.subTest(course=course_id):
                self.assertTrue(media['source_page'].startswith('https://'))
                self.assertTrue(media['source_image'].startswith('https://'))
                self.assertEqual(len(media['sha256']), 64)
                self.assertIn(media.get('rights_status'), {'unverified', 'verified_reuse'})
                if media.get('published'):
                    self.assertEqual(media.get('rights_status'), 'verified_reuse')
                    asset = (ROOT/'site'/media['src']).resolve()
                    asset.relative_to((ROOT/'site/assets/courses').resolve())
                    self.assertTrue(asset.is_file())

    def test_new_course_without_artwork_gets_accessible_editorial_panel(self):
        course = {**self.courses[0], 'id':'new-course-without-artwork', 'provider':'A & B <School>'}
        self.assertEqual(media_for(course)['kind'], 'editorial')
        html = media_html(course)
        self.assertIn('aria-hidden="true"', html)
        self.assertIn('A &amp; B &lt;School&gt;', html)
        self.assertNotIn('<img', html)


if __name__ == '__main__':
    unittest.main()
