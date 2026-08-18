import json
import tempfile
import unittest
from pathlib import Path

from main import load_spec, render, safe_relative_path


class CodeWriterTests(unittest.TestCase):
    def test_rejects_absolute_and_parent_paths(self):
        with self.assertRaises(ValueError):
            safe_relative_path("/tmp/out.py")
        with self.assertRaises(ValueError):
            safe_relative_path("../out.py")
        with self.assertRaises(ValueError):
            safe_relative_path(".github/workflows/evil.yml")

    def test_plan_detects_create_and_update(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            existing = root / "src" / "old.py"
            existing.parent.mkdir(parents=True)
            existing.write_text("old\n", encoding="utf-8")
            spec = {
                "files": [
                    {"path": "src/old.py", "content": "new\n"},
                    {"path": "src/new.py", "content": "created\n"},
                ]
            }
            changes = render(root, spec)
            self.assertEqual({str(x[0]) for x in changes}, {"src/old.py", "src/new.py"})
            self.assertTrue(any(x[2] for x in changes))
            self.assertTrue(any(not x[2] for x in changes))

    def test_spec_must_have_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({}), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_spec(path)


if __name__ == "__main__":
    unittest.main()
