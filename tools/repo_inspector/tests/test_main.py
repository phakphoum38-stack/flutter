import tempfile
import unittest
from pathlib import Path

from tools.repo_inspector.main import build_summary, scan


class RepoInspectorTests(unittest.TestCase):
    def test_scans_python_and_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "sample.py").write_text("class A:\n    def run(self):\n        return 1\n", encoding="utf-8")
            (root / "README.md").write_text("# Title\n\n## Section\n", encoding="utf-8")
            records = scan(root)
            summary = build_summary(records)
            self.assertEqual(summary["python_files"], 1)
            self.assertEqual(summary["markdown_files"], 1)
            self.assertEqual(summary["python_classes"], 1)
            self.assertEqual(summary["python_functions"], 1)

    def test_skips_build_and_git_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "build").mkdir()
            (root / "build" / "ignored.py").write_text("this is not parsed", encoding="utf-8")
            records = scan(root)
            self.assertEqual(records, [])

    def test_detects_python_syntax_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "broken.py").write_text("def broken(:\n", encoding="utf-8")
            records = scan(root)
            self.assertEqual(len(records), 1)
            self.assertIsNotNone(records[0].python_syntax_error)
            self.assertEqual(build_summary(records)["python_syntax_errors"], 1)


if __name__ == "__main__":
    unittest.main()
