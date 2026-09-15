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
