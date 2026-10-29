# 實例二：Python 教材製作（第四章）— 主 Agent 任務

先讀 `../drill/ORCHESTRATION.md`，session 名稱 `ex2`，資料夾 `ex2-python-course`。

## 書中總提示詞（逐字）

```
請以接力式多 Agent 製作 Python 入門課：依副檔名整理下載資料夾。
交付繁體中文教材、可執行範例程式及三題練習。

依序執行：
1. 教學設計 Agent 產出學習目標、課綱、先備知識及練習題。
2. 程式 Agent 讀取課綱後，製作範例程式與操作步驟。
3. 試學 Agent 按教材從頭操作，記錄執行結果及理解障礙。
4. 主 Agent 整合問題、安排修正並確認最終驗證結果。

只用 Python 標準函式庫，只在臨時測試資料夾使用自行建立的假資料。
預設只預覽整理結果；實際移動須使用明確參數，同名檔案不得覆寫。
不要操作真實下載資料夾。

驗收空資料夾、無副檔名、一般副檔名分類、預覽不改檔、既有檔名碰撞
及同批次目的路徑不衝突；測試只操作臨時假資料。

請提供恰好三題練習：
1. 預測 `photo.JPG`、`notes.txt`、`table.csv`、`script.py`、`README` 的分類。
2. 比較預覽與 `--apply`，要求先預覽且只用臨時假資料。
3. 說明 `report.txt`／`report_1.txt` 的同批次碰撞結果，以及只掃來源資料夾第一層的限制。

實際執行須回報命令與觀察結果；未執行者明確標記待驗證。
```

## 子 Agent（三格接力，嚴格依序：① 寫完才派 ②，② 寫完才派 ③）

| 格 | 角色 | 輸入 | 輸出 | 完成檔 |
| --- | --- | --- | --- | --- |
| ① | 教學設計 | 本任務 | `curriculum.md`（學習目標、先備知識、課綱：變數／判斷／迴圈／函式／副檔名分類、恰好三題練習與預期解） | `out/教學設計.done` |
| ② | 程式 | `curriculum.md` | `organize_downloads.py`（預設只預覽，`--apply` 才移動，同名不覆寫，同批次目的路徑用 reserved 集合避免衝突，只掃第一層）、`test_organize_downloads.py`（unittest，至少 7 項：空資料夾、無副檔名、一般分類、預覽不改檔、既有檔名碰撞、同批次碰撞 report_1/report_1_1、子資料夾不移動；一律 `tempfile.TemporaryDirectory()`）、`steps.md` 操作步驟 | `out/程式.done` |
| ③ | 試學 | `curriculum.md`、`steps.md`、程式 | `out/trial-log.md`（操作日誌：實際命令＋輸出）、`out/obstacles.md`（理解障礙報告）；只在 `mktemp -d` 臨時資料夾用假資料，確認 `subdir/nested.txt` 不被移動 | `out/試學.done` |

- 這台是 Windows＋MSYS2 bash：Python 指令用 `python`（不是 `python3`）；測試命令 `python -m unittest discover -s . -p 'test_*.py'`。
- **絕對不可碰真實下載資料夾**（`~/Downloads`）。

## 主 Agent 整合

1. 依試學報告的障礙，必要時退回教學設計或程式 Agent 修正（寫 fix prompt），再請試學 Agent 重驗。
2. 自己跑一次測試，記錄實際輸出。
3. `out/REPORT.md` 加上最終課時結構與三題答案摘要。

## 驗收清單（書中）

- [ ] 教材能讓目標讀者一步步做完
- [ ] 預覽模式不改任何檔案
- [ ] 測試涵蓋一般分類、空資料夾、無副檔名、同名檔案（含同批次碰撞）
- [ ] 沒有覆寫或遺失檔案，也沒碰真實下載資料夾
- [ ] 試學報告附實際操作證據，或明確寫出還沒驗證的部分
