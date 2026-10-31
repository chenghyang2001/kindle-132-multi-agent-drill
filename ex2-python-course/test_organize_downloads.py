"""organize_downloads.py 的單元測試；所有假資料都建在 tempfile 臨時資料夾內。"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import organize_downloads as od


def make_files(root: Path, names) -> None:
    """在 root 底下建立空的假檔案（名稱可含子資料夾）。"""
    for name in names:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()


def snapshot(root: Path) -> list:
    """列出 root 底下所有檔案與資料夾的相對路徑，用來比對前後是否有變。"""
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*"))


def run_main(args) -> tuple:
    """執行 main()，回傳 (exit code, stdout, stderr)。"""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = od.main(args)
    return code, out.getvalue(), err.getvalue()


class TestCategoryFor(unittest.TestCase):
    def test_general_categories_with_uppercase(self):
        """一般分類，含 .JPG 大寫。"""
        cases = {
            "photo.JPG": "images",
            "notes.txt": "documents",
            "table.csv": "data",
            "script.py": "code",
            "unknown.xyz": "others",
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(od.category_for(name), expected)

    def test_no_extension(self):
        """無副檔名進 no_extension，不是 others。"""
        self.assertEqual(od.category_for("README"), "no_extension")


class TestOrganize(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_empty_folder(self):
        """空資料夾印「沒有要整理的檔案」。"""
        code, out, _ = run_main([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("沒有要整理的檔案", out)
        self.assertEqual(od.plan_moves(self.root), [])

    def test_missing_source_exit_2(self):
        """來源不存在 → stderr 錯誤、exit code 2。"""
        code, _, err = run_main([str(self.root / "nope")])
        self.assertEqual(code, 2)
        self.assertIn("錯誤", err)

    def test_preview_does_not_change_files(self):
        """預覽模式前後檔案清單完全一樣。"""
        make_files(self.root, ["photo.JPG", "notes.txt", "README", "subdir/nested.txt"])
        before = snapshot(self.root)
        code, out, _ = run_main([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("photo.JPG -> images/photo.JPG", out)
        self.assertIn("加 --apply 才會實際移動", out)
        self.assertEqual(snapshot(self.root), before)

    def test_apply_moves_files(self):
        """--apply 會建立分類資料夾並移動檔案。"""
        make_files(self.root, ["photo.JPG", "README", "table.csv"])
        code, _, _ = run_main([str(self.root), "--apply"])
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "images" / "photo.JPG").is_file())
        self.assertTrue((self.root / "no_extension" / "README").is_file())
        self.assertTrue((self.root / "data" / "table.csv").is_file())
        self.assertFalse((self.root / "photo.JPG").exists())

    def test_existing_name_not_overwritten(self):
        """目的地已有同名檔 → 改名 _1，原檔不被覆寫。"""
        make_files(self.root, ["documents/report.txt", "report.txt"])
        (self.root / "documents" / "report.txt").write_text("old", encoding="utf-8")
        run_main([str(self.root), "--apply"])
        self.assertEqual((self.root / "documents" / "report.txt").read_text(encoding="utf-8"), "old")
        self.assertTrue((self.root / "documents" / "report_1.txt").is_file())

    def test_same_batch_collision(self):
        """同批次碰撞：report.txt → report_1.txt，report_1.txt → report_1_1.txt。"""
        make_files(self.root, ["documents/report.txt", "report.txt", "report_1.txt"])
        plan = od.plan_moves(self.root)
        mapping = {src.name: dst.relative_to(self.root).as_posix() for src, dst in plan}
        self.assertEqual(mapping, {
            "report.txt": "documents/report_1.txt",
            "report_1.txt": "documents/report_1_1.txt",
        })
        run_main([str(self.root), "--apply"])
        self.assertEqual(
            sorted(p.name for p in (self.root / "documents").iterdir()),
            ["report.txt", "report_1.txt", "report_1_1.txt"],
        )

    def test_subfolder_not_moved(self):
        """子資料夾與其內容不移動。"""
        make_files(self.root, ["subdir/nested.txt", "notes.txt"])
        run_main([str(self.root), "--apply"])
        self.assertTrue((self.root / "subdir" / "nested.txt").is_file())
        self.assertFalse((self.root / "documents" / "nested.txt").exists())
        self.assertTrue((self.root / "documents" / "notes.txt").is_file())


if __name__ == "__main__":
    unittest.main()
