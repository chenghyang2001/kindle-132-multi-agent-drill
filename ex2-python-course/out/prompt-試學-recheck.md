# 試學 Agent：重驗單

程式與教材已依你的 out/obstacles.md 修正。請以初學者身分重驗（規則同 out/prompt-試學.md：只用 `cygpath -m "$(mktemp -d)"` 臨時資料夾、不碰 ~/Downloads、不改程式與教材、貼實際命令與輸出）：

1. O-1：在一個臨時資料夾裡 `cd` 進去、`TMP=""`，執行 `python <課程資料夾>/organize_downloads.py "$TMP"` 與加 `--apply`，確認 exit 2 且檔案沒動。
2. O-2～O-6：逐項確認 curriculum.md／steps.md 已改好。
3. 重新照 steps.md 跑一次完整流程（預覽不改檔、apply、report_1_1.txt、subdir/nested.txt 不動、檔案總數不變）與測試。

把結果追加到 `out/trial-log.md` 最後（標題「## 重驗（第 2 輪）」），並在 `out/obstacles.md` 最後加「## 重驗結果」表：每個 O-編號 → 已解決／未解決＋證據；新發現的障礙另列。
完成後建立空檔 `out/試學-recheck.done`。
