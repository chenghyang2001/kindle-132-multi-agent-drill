"""依副檔名整理資料夾第一層的檔案（Python 入門課教材程式）。

用法：
    python organize_downloads.py <來源資料夾>           # 預覽，只印清單、不動檔案
    python organize_downloads.py <來源資料夾> --apply   # 實際建立分類資料夾並移動

安全原則：練習時只對 `mktemp -d` 建立的臨時資料夾執行，絕不對 ~/Downloads 執行。
"""
import argparse
import shutil
import sys
from pathlib import Path

# 分類對照表：新增分類只要在這裡加一行
CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif"},
    "documents": {".txt", ".md", ".pdf", ".docx"},
    "data": {".csv", ".xlsx"},
    "code": {".py", ".js", ".sh"},
}
NO_EXTENSION = "no_extension"
OTHERS = "others"

EXIT_BAD_SOURCE = 2
EXIT_MOVE_FAILED = 1


def category_for(path):
    """回傳檔案該放的分類資料夾名稱。

    副檔名先轉小寫再比對，所以 photo.JPG 與 photo.jpg 都會進 images。
    Path.suffix 只看最後一個點：archive.tar.gz 的 suffix 是 .gz → others。
    """
    ext = Path(path).suffix.lower()
    # 空字串要先判斷，README、.gitignore 這類檔案才會分到 no_extension
    if ext == "":
        return NO_EXTENSION
    for folder, extensions in CATEGORIES.items():
        if ext in extensions:
            return folder
    return OTHERS


def unique_target(path, reserved):
    """回傳一個沒被佔用的目的路徑。

    「被佔用」= 磁碟上已存在，或已在本次批次的 reserved 集合中。
    被佔用時依序嘗試 <stem>_1<suffix>、<stem>_2<suffix>…
    stem 用的是該檔自己的主檔名，所以 report_1.txt 的候選是 report_1_1.txt。
    """
    path = Path(path)
    candidate = path
    counter = 1
    while candidate.exists() or candidate in reserved:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        counter += 1
    return candidate


def plan_moves(source):
    """規劃 [(來源路徑, 目的路徑), ...]，不建立資料夾也不移動任何檔案。

    只掃第一層、只取檔案；子資料夾（含既有的分類資料夾）整個略過。
    依名稱排序，讓同名碰撞的結果每次都一樣。
    """
    source = Path(source)
    reserved = set()
    plan = []
    for item in sorted(source.iterdir()):
        if not item.is_file():
            continue
        wanted = source / category_for(item) / item.name
        target = unique_target(wanted, reserved)
        reserved.add(target)
        plan.append((item, target))
    return plan


def describe(src, dst, source):
    """把一筆規劃轉成「來源檔名 -> 分類資料夾/目的檔名」字串。"""
    return f"{src.name} -> {dst.relative_to(source).as_posix()}"


def apply_moves(plan):
    """依規劃建立目的資料夾並移動檔案，回傳 (成功數, 失敗清單)。

    某一筆失敗不會中斷其他筆，但失敗會收集起來回報，不會被吞掉。
    """
    moved = 0
    failures = []
    for src, dst in plan:
        try:
            # 移動前才建資料夾：預覽模式永遠不會走到這裡
            dst.parent.mkdir(parents=True, exist_ok=True)
            # 再確認一次不覆寫（規劃後到移動前，磁碟可能被別的程式改過）
            if dst.exists():
                raise FileExistsError(f"目的地已存在：{dst}")
            shutil.move(str(src), str(dst))
            moved += 1
        except OSError as error:
            failures.append((src, error))
    return moved, failures


def build_parser():
    """建立命令列參數解析器。"""
    parser = argparse.ArgumentParser(
        description="依副檔名整理資料夾第一層的檔案（預設只預覽）。"
    )
    parser.add_argument("source", help="要整理的來源資料夾")
    parser.add_argument(
        "--apply", action="store_true", help="實際建立分類資料夾並移動檔案"
    )
    return parser


def main(argv=None):
    """解析參數、規劃、預覽或移動，回傳 exit code。"""
    args = build_parser().parse_args(argv)

    # Path("") 會變成「目前資料夾」；$TMP 沒設定時就會誤整理課程資料夾，必須擋下
    if args.source.strip() == "":
        print(
            "錯誤：沒有指定資料夾（$TMP 可能是空的，請回步驟 1 重新建立）",
            file=sys.stderr,
        )
        return EXIT_BAD_SOURCE

    source = Path(args.source)
    # 錯誤訊息用斜線，跟預覽輸出一致，初學者才不會以為路徑被改掉
    if not source.exists():
        print(f"錯誤：找不到資料夾 {source.as_posix()}", file=sys.stderr)
        return EXIT_BAD_SOURCE
    if not source.is_dir():
        print(f"錯誤：{source.as_posix()} 不是資料夾", file=sys.stderr)
        return EXIT_BAD_SOURCE

    plan = plan_moves(source)
    if not plan:
        print("沒有要整理的檔案")
        return 0

    if not args.apply:
        for src, dst in plan:
            print(describe(src, dst, source))
        print("這是預覽，加 --apply 才會實際移動。")
        return 0

    moved, failures = apply_moves(plan)
    failed_sources = {src for src, _ in failures}
    for src, dst in plan:
        if src not in failed_sources:
            print(f"已移動：{describe(src, dst, source)}")
    for src, error in failures:
        print(f"錯誤：移動 {src.name} 失敗：{error}", file=sys.stderr)
    print(f"完成：已移動 {moved} 個檔案。")
    return EXIT_MOVE_FAILED if failures else 0


if __name__ == "__main__":
    sys.exit(main())
