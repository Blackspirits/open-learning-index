"""Protect the bilingual presentation boundary and static media delivery."""
import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import build_public_site as build
from editorial_presentation import localize_course, media_for, media_html, pt, MEDIA


class EditorialPresentationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        courses = json.loads(build.COURSES.read_text(encoding='utf-8'))
        categories = {c['id']:c for c in json.loads(build.CATEGORIES.read_text(encoding='utf-8'))}
        reviews = build.load_current_records(build.REVIEWS_DIR, 'reviewed_on')
        references = build.load_current_records(build.REFERENCE_REVIEWS, 'reviewed_on', 'course_id')
        admissions = build.load_current_records(build.ADMISSIONS_DIR, 'decided_on')
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
