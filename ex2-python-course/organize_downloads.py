"""依副檔名整理資料夾第一層的檔案（Python 入門課範例程式）。

用法：
    python organize_downloads.py <來源資料夾>           # 只預覽，不改任何檔案
    python organize_downloads.py <來源資料夾> --apply   # 實際移動

安全提醒：練習時只對 mktemp -d 或 tempfile 建立的臨時資料夾執行。
"""
import argparse
import shutil
import sys
from pathlib import Path

# 分類對照表：資料夾名稱 → 副檔名（一律小寫）
CATEGORIES = {
    "images": (".jpg", ".jpeg", ".png", ".gif"),
    "documents": (".txt", ".md", ".pdf", ".docx"),
    "data": (".csv", ".xlsx"),
    "code": (".py", ".js", ".sh"),
}
OTHERS = "others"
NO_EXTENSION = "no_extension"


def category_for(path) -> str:
    """回傳檔案應放入的分類資料夾名稱。

    副檔名先轉小寫再比對，所以 photo.JPG 會進 images。
    沒有副檔名（例如 README）回傳 no_extension，查不到的副檔名回傳 others。
    """
    ext = Path(path).suffix.lower()
    if ext == "":
        return NO_EXTENSION
    for folder, extensions in CATEGORIES.items():
        if ext in extensions:
            return folder
    return OTHERS


def unique_target(target: Path, reserved: set) -> Path:
    """回傳不會衝突的目的路徑。

    目的路徑「已存在」或「本批次已規劃（在 reserved 中）」都算衝突，
    衝突時以原始檔名的 stem 加 _1、_2…，直到不衝突為止。
    """
    if not target.exists() and target not in reserved:
        return target
    counter = 1
    while True:
        candidate = target.with_name(f"{target.stem}_{counter}{target.suffix}")
        if not candidate.exists() and candidate not in reserved:
            return candidate
        counter += 1


def plan_moves(source: Path) -> list:
    """規劃要移動的檔案，回傳 [(來源, 目的), ...]，不會改動任何檔案。

    只看來源資料夾第一層的檔案，子資料夾（含分類資料夾）一律跳過。
    依檔名排序處理，讓同批次碰撞的改名結果可預測。
    """
    reserved = set()
    plan = []
    files = sorted((p for p in source.iterdir() if p.is_file()), key=lambda p: p.name)
    for src in files:
        target = unique_target(source / category_for(src) / src.name, reserved)
        reserved.add(target)
        plan.append((src, target))
    return plan


def apply_moves(plan: list) -> None:
    """依規劃實際移動檔案；移動前才建立目的子資料夾。"""
    for src, dst in plan:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))


def main(argv=None) -> int:
    """命令列進入點，回傳 exit code（0 成功、2 來源資料夾有問題）。"""
    parser = argparse.ArgumentParser(description="依副檔名整理資料夾第一層的檔案")
    parser.add_argument("source", help="要整理的來源資料夾")
    parser.add_argument("--apply", action="store_true", help="實際移動檔案（預設只預覽）")
    args = parser.parse_args(argv)

    source = Path(args.source)
    if not source.exists():
        print(f"錯誤：來源資料夾不存在：{source}", file=sys.stderr)
        return 2
    if not source.is_dir():
        print(f"錯誤：來源不是資料夾：{source}", file=sys.stderr)
        return 2

    plan = plan_moves(source)
    if not plan:
        print("沒有要整理的檔案")
        return 0

    for src, dst in plan:
        # 用相對於來源資料夾的路徑顯示，比較好讀
        print(f"{src.relative_to(source).as_posix()} -> {dst.relative_to(source).as_posix()}")

    if args.apply:
        try:
            apply_moves(plan)
        except OSError as exc:
            print(f"錯誤：移動檔案失敗：{exc}", file=sys.stderr)
            return 1
        print(f"已移動 {len(plan)} 個檔案")
    else:
        print(f"共 {len(plan)} 個檔案（預覽模式，沒有移動任何檔案）")
        print("加 --apply 才會實際移動")
    return 0


if __name__ == "__main__":
    sys.exit(main())
