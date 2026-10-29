# 教學設計 Agent：修正單（第 1 輪）

程式 Agent 在 `out/程式-notes.md` 回報：Git Bash 的 `mktemp -d` 回傳 `/tmp/tmp.xxx`，Windows 的 Python 讀不到（錯誤：找不到資料夾 \tmp\tmp.xxx）。
`steps.md` 已改用 `TMP=$(cygpath -m "$(mktemp -d)")`。

請修改 `curriculum.md`：
1. §3 安全原則與練習二（以及其他出現 `mktemp -d` 的地方）改成 `TMP=$(cygpath -m "$(mktemp -d)")`，並加一句說明：Windows + Git Bash 要用 cygpath -m 轉成 Python 看得懂的路徑；macOS/Linux 直接 `TMP=$(mktemp -d)` 即可。
2. §5.4 的「已移動 N 個檔案」範例數字若與標準範例不符（標準範例實際是 7），改成一致或註明是示意。
3. 其他內容不要動，練習仍必須恰好三題。

完成後建立空檔 `out/教學設計-fix.done`。
