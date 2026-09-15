"""Prevent cached scripts/data from a previous release breaking a new page."""
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_public_site import version_public_assets


class PublicAssetVersionTest(unittest.TestCase):
    def test_data_and_style_changes_invalidate_dependents_deterministically(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "data").mkdir()
            (root / "pt/courses/example").mkdir(parents=True)
            files = {
                "app.js": 'fetch("data/catalog.json"); fetch("data/meta.json");',
                "theme.js": 'const theme = "light";',
                "styles.css": 'body { color: black; }',
                "data/catalog.json": '[{"title":"Old title"}]',
                "data/meta.json": '{"published_count":1}',
            }
            for name, content in files.items():
                (root / name).write_text(content, encoding="utf-8")
            for route, prefix in (("index.html", ""), ("pt/courses/example/index.html", "../../../")):
                (root / route).write_text(
                    f'<link href="{prefix}styles.css"><script src="{prefix}app.js"></script>'
                    f'<script src="{prefix}theme.js"></script><a href="{prefix}courses/">Courses</a>'
                    '<script src="https://example.com/external.js"></script>', encoding="utf-8")

            def snapshot():
                return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*") if p.is_file()}

            version_public_assets(root)
            first = snapshot()
            self.assertRegex(first["app.js"].decode(), r'data/catalog\.json\?v=[a-f0-9]{16}')
            nested = first["pt/courses/example/index.html"].decode()
            self.assertRegex(nested, r'src="../../../app\.js\?v=[a-f0-9]{16}"')
            self.assertIn('href="../../../courses/"', nested)
            self.assertIn('src="https://example.com/external.js"', nested)
            version_public_assets(root)
            self.assertEqual(first, snapshot())

            (root / "data/catalog.json").write_text('[{"title":"New title"}]', encoding="utf-8")
            (root / "styles.css").write_text('body { color: navy; }', encoding="utf-8")
            version_public_assets(root)
            second = snapshot()
            self.assertNotEqual(first["app.js"], second["app.js"])
            for asset in ("app.js", "styles.css"):
                pattern = re.escape(asset) + r'\?v=[a-f0-9]{16}'
                self.assertNotEqual(re.search(pattern, first["index.html"].decode()).group(),
                                    re.search(pattern, second["index.html"].decode()).group())
            self.assertEqual(first["theme.js"], second["theme.js"])


if __name__ == "__main__":
    unittest.main()
