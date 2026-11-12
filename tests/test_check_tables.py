import importlib.util
import io
import os
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

SCRIPT = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "skills", "project-rules", "scripts", "check_tables.py",
)
spec = importlib.util.spec_from_file_location("check_tables", SCRIPT)
check_tables = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_tables)

GOOD = "| a  | b  |\n|----|----|\n| 1  | 2  |\n"
BAD = "| a  | b  |\n|----|----|\n| 1  | 22 |\n| 1 | 2 |\n"


class CheckTablesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, name, text):
        p = os.path.join(self.tmp.name, name)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        return p

    def run_main(self, *paths):
        out = io.StringIO()
        with redirect_stdout(out):
            code = check_tables.main(list(paths))
        return code, out.getvalue()

    def test_aligned_passes(self):
        code, out = self.run_main(self.write("a.md", GOOD))
        self.assertEqual(code, 0)
        self.assertIn("All tables aligned.", out)

    def test_reports_all_files(self):
        a = self.write("a.md", BAD)
        b = self.write("b.md", BAD)
        code, out = self.run_main(a, b)
        self.assertEqual(code, 1)
        self.assertIn(a, out)
        self.assertIn(b, out)

    def test_skips_fences(self):
        for fence in ("```", "~~~", "````"):
            p = self.write("f.md", f"{fence}\n{BAD}{fence}\n")
            code, _ = self.run_main(p)
            self.assertEqual(code, 0, fence)

    def test_table_after_fence_checked(self):
        p = self.write("f.md", f"```\nx\n```\n\n{BAD}")
        self.assertEqual(self.run_main(p)[0], 1)

    def test_indented_table(self):
        text = "- item\n\n" + "".join("  " + l + "\n" for l in BAD.splitlines())
        code, out = self.run_main(self.write("i.md", text))
        self.assertEqual(code, 1)
        self.assertIn(":6:", out)

    def test_indented_aligned_passes(self):
        text = "".join("   " + l + "\n" for l in GOOD.splitlines())
        self.assertEqual(self.run_main(self.write("i.md", text))[0], 0)

    def test_escaped_pipe(self):
        text = "| a \\| b | c |\n|--------|---|\n| x      | y |\n"
        code, _ = self.run_main(self.write("e.md", text))
        self.assertEqual(code, 0)

    def run_err(self, *paths):
        err = io.StringIO()
        with redirect_stderr(err):
            code, out = self.run_main(*paths)
        return code, out, err.getvalue()

    def test_missing_file(self):
        missing = os.path.join(self.tmp.name, "missing.md")
        bad = self.write("b.md", BAD)
        code, out, err = self.run_err(missing, bad)
        self.assertEqual(code, 1)
        self.assertIn(missing + ": file not found", err)
        self.assertIn(bad, out)

    def test_directory_and_bad_utf8(self):
        p = os.path.join(self.tmp.name, "x.md")
        with open(p, "wb") as f:
            f.write(b"\xff\xfe\x80")
        for path in (self.tmp.name, p):
            code, _, err = self.run_err(path)
            self.assertEqual(code, 1)
            self.assertIn("cannot read file", err)

    def test_fence_in_list_item(self):
        p = self.write("l.md", "- ```\n  " + BAD.splitlines()[2] + "\n  | 1 | 2 |\n  ```\n")
        self.assertEqual(self.run_main(p)[0], 0)

    def test_unicode_width_as_before(self):
        text = "| é | b |\n|---|---|\n| x | y |\n"
        self.assertEqual(self.run_main(self.write("u.md", text))[0], 0)


if __name__ == "__main__":
    unittest.main()
