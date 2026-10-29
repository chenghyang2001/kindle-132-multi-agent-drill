# 實例二報告：Python 入門課「依副檔名整理下載資料夾」（接力式多 Agent）

## 1. 用了幾個 Agent

主 Agent（本 session `代理二`）＋ 3 個子 Agent，各自在螢幕 2 的 wpanes 格子裡跑獨立的 Claude Code（session `ex2`），交接全部靠檔案。

| 格 | 角色 | 輸入 | 輸出 | 完成檔 |
| --- | --- | --- | --- | --- |
| ① | 教學設計 | `out/prompt-教學設計.md` | `curriculum.md` | `out/教學設計.done` |
| ② | 程式 | `curriculum.md`、`out/prompt-程式.md` | `organize_downloads.py`、`test_organize_downloads.py`、`steps.md`、`out/程式-notes.md` | `out/程式.done` |
| ③ | 試學 | `curriculum.md`、`steps.md`、程式 | `out/trial-log.md`、`out/obstacles.md` | `out/試學.done` |

## 2. 順序與交接（時間軸見 `out/timeline.tsv`）

1. ① 教學設計寫 `curriculum.md`（6 堂、恰好三題）→ 主 Agent 驗收結構後才派 ②。
2. ② 程式寫程式＋測試＋步驟；在 `程式-notes.md` 回報規格問題：Git Bash `mktemp -d` 回傳 `/tmp/...`，Windows Python 讀不到。
3. **退回 ①（fix 1）**：curriculum 全面改用 `TMP=$(cygpath -m "$(mktemp -d)")`。
4. ③ 試學照教材從頭操作，回報 6 項障礙（O-1～O-6），其中 **O-1 高嚴重度**：新開終端機 `$TMP` 是空的時，`Path("")` 等於目前資料夾，`--apply` 會把課程檔案搬走。
5. **同時退回 ② 與 ①**（改不同檔案，互不衝突）：
   - ②（程式-fix）：空白來源參數 → exit 2 並補測試；錯誤訊息改用 `as_posix()`；steps.md 加 TMP 檢查與說明（O-1、O-5、O-6）。
   - ①（fix 2）：安全原則加 TMP 檢查、互動模式進出說明、各堂練習檔起手式、練習二驗證檔路徑（O-1～O-4）。
6. **③ 重驗**：O-1～O-6 全部已解決（O-2 互動模式卡住與否因環境非互動終端機，仍待驗證）；新增 2 項低嚴重度 N-1、N-2。
7. **再退回 ② 與 ①**：N-1 steps.md 檢查行改成 `if/else` 會中止；N-2 第 3、5 堂起手式加參數防呆。
8. 主 Agent 自行驗收（下節）→ 關格子 → `ALL.done`。

## 3. 驗收（主 Agent 實際執行，完整輸出在 `out/main-verify.log`）

```
$ python -m unittest discover -s . -p 'test_*.py' -v
Ran 9 tests in 0.077s
OK
```

9 項測試：空資料夾、無副檔名、一般分類（含 .JPG 大小寫）、預覽不改檔、既有檔名碰撞、同批次碰撞 report_1/report_1_1、子資料夾不移動、來源錯誤 exit 2、空字串來源 exit 2。全部用 `tempfile.TemporaryDirectory()`。

臨時資料夾（`cygpath -m "$(mktemp -d)"`）端到端：

```
前：總數 9
$ python organize_downloads.py "$TMP"
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
...（共 7 筆）
這是預覽，加 --apply 才會實際移動。
預覽前後 diff：無差異（不改檔）
$ python organize_downloads.py "$TMP" --apply
完成：已移動 7 個檔案。
後：總數 9（documents/ 內 report.txt、report_1.txt、report_1_1.txt 都在；subdir/nested.txt 留在原地）
$ python organize_downloads.py "" --apply
錯誤：沒有指定資料夾（$TMP 可能是空的，請回步驟 1 重新建立）   exit=2
$ python organize_downloads.py "$EMPTY"
沒有要整理的檔案   exit=0
```

| 書中驗收項 | 結果 | 證據 |
| --- | --- | --- |
| 教材能讓目標讀者一步步做完 | ✅ | 試學 Agent 兩輪照 steps.md 全程做完（`out/trial-log.md`），障礙已修 |
| 預覽模式不改任何檔案 | ✅ | 預覽前後 `find` diff 無差異；測試 `test_preview_does_not_change_files` |
| 測試涵蓋一般分類、空資料夾、無副檔名、同名（含同批次） | ✅ | 9 tests OK |
| 沒有覆寫或遺失檔案，沒碰真實下載資料夾 | ✅ | apply 前後總數 9→9；所有操作都在 Temp 臨時資料夾；程式只在註解中提到 ~/Downloads |
| 試學報告附實際操作證據／標出未驗證部分 | ✅ | trial-log 附命令＋輸出；O-2 互動模式明確標「待驗證」 |

## 4. 最終課時結構（`curriculum.md`，6 堂約 200 分鐘）

| 堂 | 主題 | 分鐘 |
| --- | --- | --- |
| 1 | 變數——檔名與副檔名（`.suffix`、`.lower()`、互動模式） | 30 |
| 2 | 判斷（if）——決定分類資料夾 | 30 |
| 3 | 迴圈（for）——走過資料夾第一層（`sys.argv[1]`） | 35 |
| 4 | 函式（def）——把邏輯包起來 | 35 |
| 5 | 副檔名分類——組成完整分類規則 | 30 |
| 6 | 預覽 vs `--apply`、同名碰撞與安全原則 | 40 |

## 5. 三題練習答案摘要

1. **預測分類**：`photo.JPG`→`images/`（副檔名先轉小寫）、`notes.txt`→`documents/`、`table.csv`→`data/`、`script.py`→`code/`、`README`→`no_extension/`。
2. **預覽 vs `--apply`**：預設只印「來源 -> 目的」、不建資料夾不移檔；`--apply` 才移動。一定先預覽，且只在 `cygpath -m "$(mktemp -d)"` 臨時假資料上做；驗證方式是預覽前後 `ls -R` 存檔後 `diff` 無差異。
3. **同批次碰撞與第一層限制**：目的地已有 `documents/report.txt` 時，來源 `report.txt`→`documents/report_1.txt`（並記入 reserved），來源 `report_1.txt` 因該路徑已被保留→`documents/report_1_1.txt`；程式只掃來源第一層，`subdir/nested.txt` 不會被處理。

## 6. 未解決／待確認

- O-2：Git Bash（mintty）直接輸入 `python` 進入互動模式是否會卡住、`winpty python` 是否有效——子 Agent 環境不是互動式終端機，**待驗證**。教材已提供 `python lesson1.py` 替代做法（已驗證可行）。
- N-1、N-2 的修正由子 Agent 完成並自測；第三輪未再派試學 Agent 重驗，主 Agent 只做了上面的端到端與測試驗收。
