# 程式 Agent 筆記（實例二・第 ② 棒）

## 規格問題

1. **`mktemp -d` 的路徑 Windows Python 讀不到**（curriculum.md §3 的標準做法會失敗）
   - 實測：Git Bash `mktemp -d` 回傳 `/tmp/tmp.xxx`，`python organize_downloads.py "$TMP"` 印出
     `錯誤：找不到資料夾 \tmp\tmp.xxx`、exit 2。
   - 處理：`steps.md` 改用 `TMP=$(cygpath -m "$(mktemp -d)")`（轉成 `C:/.../Temp/tmp.xxx`，bash 與 Python 都能用）。
   - 建議教學設計 Agent 把 curriculum.md §3 與練習二的指令一起改掉（本棒依規定不改 curriculum.md）。

## 實作上的小決定（規格沒寫死的部分）

- `--apply` 中某一筆移動失敗：不中斷其他筆，最後把每筆失敗印到 stderr，exit code 1。
- 移動前再檢查一次目的路徑是否存在，存在就當失敗處理（防止規劃後被別的程式寫入而覆寫）。
- 測試做了 8 項（規格要求 7 項 + 來源錯誤 exit code 2）。
- 「完成：已移動 N 個檔案」中，標準範例的 N 是 7（9 個檔案裡 `documents/report.txt` 已在分類資料夾、`subdir/nested.txt` 在子資料夾，都不移動），不是 curriculum §5.4 舉例寫的 8——那只是範例數字，不衝突。

## 驗證結果

- `PYTHONUTF8=1 python -m unittest discover -s . -p 'test_*.py' -v`：8 tests OK。
- 臨時資料夾冒煙測試：預覽前後 `ls -R` 無差異；`--apply` 後檔案總數 9 → 9，`report_1_1.txt` 產生，`subdir/nested.txt` 留在原處；空資料夾 exit 0、不存在路徑 exit 2。
- 全程未碰 `~/Downloads`。
