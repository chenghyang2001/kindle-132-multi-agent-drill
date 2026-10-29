"""organize_downloads.py 的單元測試。

所有測試都在 tempfile.TemporaryDirectory() 裡建立假資料，
絕不碰 ~/Downloads 或任何真實資料夾。
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import organize_downloads as od


def make_files(root, names):
    """在 root 底下建立空檔案（名稱可含子資料夾，例如 subdir/nested.txt）。"""
    for name in names:
        file_path = root / name
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text("", encoding="utf-8")


def snapshot(root):
    """回傳 root 底下所有檔案與資料夾的相對路徑集合，用來比對前後是否一樣。"""
    return {p.relative_to(root).as_posix() for p in root.rglob("*")}


def run_main(argv):
    """執行 main()，回傳 (exit code, stdout, stderr)。"""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = od.main(argv)
    return code, out.getvalue(), err.getvalue()


class OrganizeDownloadsTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def plan_names(self):
        """把規劃轉成 {來源檔名: 目的相對路徑}，方便比對。"""
        return {
            src.name: dst.relative_to(self.root).as_posix()
            for src, dst in od.plan_moves(self.root)
        }

    # 1. 空資料夾
    def test_empty_folder(self):
        self.assertEqual(od.plan_moves(self.root), [])
        code, out, _ = run_main([str(self.root)])
        self.assertEqual(code, 0)
        self.assertIn("沒有要整理的檔案", out)

    # 2. 無副檔名
    def test_no_extension(self):
        make_files(self.root, ["README", ".gitignore"])
        self.assertEqual(
            self.plan_names(),
            {"README": "no_extension/README", ".gitignore": "no_extension/.gitignore"},
        )

    # 3. 一般分類（含大寫 .JPG）
    def test_categories_case_insensitive(self):
        make_files(
            self.root,
            ["photo.JPG", "notes.txt", "table.csv", "script.py", "archive.tar.gz"],
        )
        self.assertEqual(
            self.plan_names(),
            {
                "photo.JPG": "images/photo.JPG",
                "notes.txt": "documents/notes.txt",
                "table.csv": "data/table.csv",
                "script.py": "code/script.py",
                "archive.tar.gz": "others/archive.tar.gz",
            },
        )

    # 4. 預覽不改檔
    def test_preview_does_not_change_files(self):
        make_files(self.root, ["photo.JPG", "notes.txt", "README", "subdir/nested.txt"])
        before = snapshot(self.root)
        code, out, _ = run_main([str(self.root)])
        self.assertEqual(code, 0)
        self.assertEqual(snapshot(self.root), before)
        self.assertIn("photo.JPG -> images/photo.JPG", out)
        self.assertIn("加 --apply 才會實際移動", out)

    # 5. 既有檔名碰撞
    def test_existing_target_collision(self):
        make_files(self.root, ["documents/report.txt", "report.txt"])
        self.assertEqual(self.plan_names(), {"report.txt": "documents/report_1.txt"})

    # 6. 同批次碰撞：report_1 / report_1_1
    def test_same_batch_collision(self):
        make_files(self.root, ["documents/report.txt", "report.txt", "report_1.txt"])
        self.assertEqual(
            self.plan_names(),
            {
                "report.txt": "documents/report_1.txt",
                "report_1.txt": "documents/report_1_1.txt",
            },
        )
        code, _, _ = run_main([str(self.root), "--apply"])
        self.assertEqual(code, 0)
        docs = sorted(p.name for p in (self.root / "documents").iterdir())
        self.assertEqual(docs, ["report.txt", "report_1.txt", "report_1_1.txt"])

    # 7. 子資料夾不移動
    def test_subdir_not_moved(self):
        make_files(self.root, ["notes.txt", "subdir/nested.txt"])
        count_before = sum(1 for p in self.root.rglob("*") if p.is_file())
        code, out, _ = run_main([str(self.root), "--apply"])
        self.assertEqual(code, 0)
        self.assertTrue((self.root / "subdir" / "nested.txt").is_file())
        self.assertTrue((self.root / "documents" / "notes.txt").is_file())
        count_after = sum(1 for p in self.root.rglob("*") if p.is_file())
        self.assertEqual(count_before, count_after)
        self.assertIn("完成：已移動 1 個檔案。", out)

    # 8. 錯誤：來源不存在 / 不是資料夾 → exit code 2
    def test_bad_source_exit_code(self):
        code, _, err = run_main([str(self.root / "nope")])
        self.assertEqual(code, 2)
        self.assertIn("找不到資料夾", err)
        make_files(self.root, ["file.txt"])
        code, _, err = run_main([str(self.root / "file.txt")])
        self.assertEqual(code, 2)
        self.assertIn("不是資料夾", err)


if __name__ == "__main__":
    unittest.main()
