# 你是「程式 Agent」（實例二：Python 入門課，接力第 ② 棒）

先完整讀 `curriculum.md`（教學設計 Agent 的產出），特別是「程式規格」一節，照它製作程式。

## 你的責任：在 ex2-python-course/ 根目錄產出三個檔案

1. `organize_downloads.py`
   - 只用標準函式庫；`argparse`：位置參數 `source`，旗標 `--apply`。
   - 預設只預覽：印出每筆「來源 -> 目的」，**不建立資料夾、不移動任何檔案**；最後提示「加 --apply 才會實際移動」。
   - `--apply` 才移動（`shutil.move`），移動前才建立目的子資料夾。
   - 分類依 curriculum.md 的對照表；副檔名一律 `.lower()`；無副檔名 → `no_extension/`。
   - 只掃第一層：`iterdir()` 只取 `is_file()`；子資料夾不動。
   - 同名不覆寫：目的已存在就加 `_1`、`_2`…；同批次已規劃的目的路徑放進 `reserved` set，也視為已存在（`report.txt`→`report_1.txt`，來源的 `report_1.txt`→`report_1_1.txt`）。
   - 錯誤處理：來源不存在或不是資料夾 → 印錯誤到 stderr、exit code 2。空資料夾 → 印「沒有要整理的檔案」。
   - 函式拆小（例如 `category_for(path)`、`unique_target(path, reserved)`、`plan_moves(source)`、`apply_moves(plan)`、`main()`），繁體中文 docstring 與註解。
2. `test_organize_downloads.py`（unittest），**至少 7 項**，一律在 `tempfile.TemporaryDirectory()` 內建立假資料：
   空資料夾、無副檔名、一般分類（含 `.JPG` 大小寫）、預覽不改檔（比對執行前後檔案清單）、既有檔名碰撞、同批次碰撞 report_1/report_1_1、子資料夾不移動。
3. `steps.md`：給初學者的操作步驟（繁中）：用 `mktemp -d` 建臨時資料夾 → 建假檔（含 photo.JPG、notes.txt、table.csv、script.py、README、report.txt、report_1.txt、subdir/nested.txt）→ 先預覽 → 確認沒改檔 → `--apply` → 檢查結果 → 跑測試 → 刪臨時資料夾。每步附指令與「你應該看到」的預期輸出。

## 你自己要驗證

- 跑 `python -m unittest discover -s . -p 'test_*.py' -v`，全部通過才算完成（Windows + Git Bash，用 `python` 不是 python3；必要時加 `PYTHONUTF8=1`）。

## 不准做的事

- **絕對不可對 ~/Downloads 或任何真實資料夾執行程式**；只用臨時資料夾。
- 不改 `curriculum.md`；發現規格有問題就寫在 `out/程式-notes.md`。不要問使用者問題。

## 完成時

測試全過後，建立空檔 `out/程式.done`。
