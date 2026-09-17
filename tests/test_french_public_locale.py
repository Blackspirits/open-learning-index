from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class FrenchPublicLocaleTests(unittest.TestCase):
    def test_public_build_wrapper_enables_french(self):
        source = (ROOT / "scripts" / "build_public_site_public.py").read_text(encoding="utf-8")
        self.assertIn('("pt-PT", "es", "fr")', source)
        self.assertIn('build.LOCALE_META["fr"]', source)
        self.assertIn('build.LOCALE_COURSE_COPY["fr"]', source)
        self.assertIn('build.LOCALE_ACCESS_DETAIL["fr"]', source)

    def test_public_validator_requires_french(self):
        source = (ROOT / "scripts" / "validate_public_site_public.py").read_text(encoding="utf-8")
        self.assertIn('"fr": "fr"', source)
        self.assertIn('presentations.fr.description', source)
        self.assertIn('app-fr.js', source)

    def test_french_static_shells_exist(self):
        pages = [
            ROOT / "site" / "fr" / "index.html",
            ROOT / "site" / "fr" / "courses" / "index.html",
            ROOT / "site" / "fr" / "methodology" / "index.html",
        ]
        for page in pages:
            with self.subTest(page=page):
                self.assertTrue(page.is_file())
                html = page.read_text(encoding="utf-8")
                self.assertIn('<html lang="fr">', html)
                self.assertIn('hreflang="fr"', html)
                self.assertIn('Français', html)

    def test_french_runtime_consumes_locale_keyed_presentation(self):
        source = (ROOT / "site" / "app-fr.js").read_text(encoding="utf-8")
        self.assertIn('course.presentations?.fr', source)
        self.assertIn('Recommandation', source)
        self.assertIn('Qualité', source)
        self.assertIn('fr/courses/', source)

    def test_ci_uses_public_locale_build_and_validation(self):
        for relative in [
            Path(".github/workflows/validate.yml"),
            Path(".github/workflows/pages.yml"),
        ]:
            source = (ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(path=relative):
                self.assertIn("build_public_site_public.py", source)
                self.assertIn("validate_public_site_public.py", source)
                self.assertIn("--locale fr --enforce", source)


if __name__ == "__main__":
    unittest.main()
