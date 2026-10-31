# 程式 Agent 筆記（接力第 ② 棒）

## 產出

- `organize_downloads.py`：`category_for` / `unique_target` / `plan_moves` / `apply_moves` / `main`，只用標準函式庫。
- `test_organize_downloads.py`：9 項 unittest（prompt 要求的 7 項 + 來源不存在 exit 2 + `--apply` 會移動），全部通過。
- `steps.md`：初學者操作步驟，每步附「你應該看到」的實際輸出（已在臨時資料夾實測）。

## 發現的規格問題（未改 curriculum.md）

1. **`mktemp -d` 路徑在 Windows Python 看不懂**（影響最大）
   - curriculum.md 第 3、6 堂與練習 2 都用 `demo=$(mktemp -d)` 再 `python organize_downloads.py "$demo"`。
   - 實測本機環境設了 `MSYS_NO_PATHCONV=1`，Git Bash 不轉換路徑，Python 收到 `/tmp/tmp.xxx`，
     解析成 `\tmp\tmp.xxx` → 「來源資料夾不存在」，exit 2。
   - 對策：`steps.md` 改用 `demo=$(cygpath -m "$(mktemp -d)")`，有沒有設該變數都能用。
   - 建議教學設計 Agent 把課綱中的範例指令也改成這個寫法，否則試學 Agent 照課綱做會失敗。
2. **錯誤 exit code**：curriculum 只說「非 0」，prompt 指定 2；照 prompt 用 2。
   `--apply` 搬移時發生 OSError 則回傳 1（規格未定義，自行決定）。
3. **第 4 堂函式簽名**：課綱寫 `category_for(filename: str)`，程式接受 `str` 或 `Path`（內部用 `Path(...)` 包），兩種都相容。
4. **預覽輸出格式**：規格只說「來源 -> 目的」，程式印相對於來源資料夾的路徑（例：`photo.JPG -> images/photo.JPG`），用 `/` 分隔，跨平台一致。

## 驗證

```text
PYTHONUTF8=1 python -m unittest discover -s . -p 'test_*.py' -v
Ran 9 tests ... OK
```

另在 `cygpath -m "$(mktemp -d)"` 臨時資料夾實跑預覽 / diff / `--apply` / 錯誤路徑 / 空資料夾，結果符合規格，跑完已刪除。未對任何真實資料夾執行。
