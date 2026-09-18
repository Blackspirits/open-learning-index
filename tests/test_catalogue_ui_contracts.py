"""UI contracts for catalogue ordering and locale-aware language presentation."""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "site" / "app.js"
BUILDER = ROOT / "scripts" / "build_public_site.py"


class CatalogueUiContractsTest(unittest.TestCase):
    def test_level_filter_uses_semantic_progression(self):
        source = APP.read_text(encoding="utf-8")
        match = re.search(r"const levelOrder = \[(.*?)\];", source, re.S)
        self.assertIsNotNone(match)
        values = re.findall(r'"([^"]+)"', match.group(1))
        self.assertEqual(
            values,
            [
                "beginner",
                "beginner_to_intermediate",
                "intermediate",
                "intermediate_to_advanced",
                "advanced",
                "undergraduate",
                "graduate",
                "beginner_to_advanced",
            ],
        )
        self.assertIn("levelRank.get(a)", source)
        self.assertIn("progressionGroup.label = copy.progression", source)
        self.assertIn("broadGroup.label = copy.broad", source)
        self.assertIn("shortcutGroup.label = copy.shortcut", source)
        self.assertIn('beginnerFriendly: "Beginner-friendly"', source)
        self.assertIn('beginnerFriendly: "Adequado a principiantes"', source)
        self.assertIn('beginnerFriendly: "Adecuado para principiantes"', source)
        self.assertIn('progression: "Progresión"', source)
        self.assertIn('beginnerFriendly: "Adapté aux débutants"', source)
        self.assertIn('progression: "Progression"', source)

    def test_pt_language_names_are_consistently_lowercase(self):
        source = APP.read_text(encoding="utf-8")
        match = re.search(r'"pt-PT": \{([^}]+)\}', source)
        self.assertIsNotNone(match)
        values = re.findall(r': "([^"]+)"', match.group(1))
        self.assertTrue(values)
        for value in values:
            self.assertEqual(value[0], value[0].lower(), value)
        self.assertIn("labelLanguageOption(a).localeCompare(labelLanguageOption(b), pageLocale)", source)
        self.assertIn("new Option(labelLanguageOption(value), value)", source)

    def test_static_language_maps_keep_locale_boundaries(self):
        source = BUILDER.read_text(encoding="utf-8")
        en = re.search(r"LANGUAGE_LABELS = \{(.*?)\n\}", source, re.S)
        pt = re.search(r"PT_LANGUAGE_LABELS = \{(.*?)\n\}", source, re.S)
        es = re.search(r"ES_LANGUAGE_LABELS = \{(.*?)\n\}", source, re.S)
        fr = re.search(r"FR_LANGUAGE_LABELS = \{(.*?)\n\}", source, re.S)
        self.assertIsNotNone(en)
        self.assertIsNotNone(pt)
        self.assertIsNotNone(es)
        self.assertIsNotNone(fr)
        self.assertIn('"pt-BR": "Portuguese (Brazil)"', en.group(1))
        self.assertIn('"pt-PT": "Portuguese (Portugal)"', en.group(1))
        self.assertIn('"pt-BR": "português (Brasil)"', pt.group(1))
        self.assertIn('"pt-PT": "português (Portugal)"', pt.group(1))
        self.assertIn('"pt-BR": "portugués (Brasil)"', es.group(1))
        self.assertIn('"pt-PT": "portugués (Portugal)"', es.group(1))
        self.assertIn('"pt-BR": "portugais (Brésil)"', fr.group(1))
        self.assertIn('"pt-PT": "portugais (Portugal)"', fr.group(1))


if __name__ == "__main__":
    unittest.main()
