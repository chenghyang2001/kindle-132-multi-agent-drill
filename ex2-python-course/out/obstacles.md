# 理解障礙報告（試學 Agent，接力第 ③ 棒）

> 依據：`out/trial-log.md` 的實際操作結果。程式與教材都沒有修改，只回報。

| 編號 | 位置（哪份文件哪一步） | 障礙描述 | 嚴重度（高/中/低） | 建議修正 | 該退回給（教學設計/程式） |
| --- | --- | --- | --- | --- | --- |
| O-1 | `curriculum.md` 第 3 堂小活動、第 6 堂小活動、練習 2 預期解 | 範例都寫 `demo=$(mktemp -d)` 再 `python organize_downloads.py "$demo"`。實測 Python 收到 `/tmp/tmp.xxx`，回報「錯誤：來源資料夾不存在：\tmp\tmp.xxx」並 exit 2。拿掉 `MSYS_NO_PATHCONV`、開乾淨的 bash 也一樣失敗。初學者照課綱做，第一次執行就會卡住，還會誤以為程式壞了。 | 高 | 課綱所有範例統一改成 `demo=$(cygpath -m "$(mktemp -d)")`（和 `steps.md` 步驟 1 一致），並在第 3 堂加一句說明，或直接指向 `steps.md` 的 💡 說明。 | 教學設計 |
| O-2 | `steps.md` 步驟 1 的 💡 說明 | 說明寫 Windows 版 Python「**有時**」看不懂 `/tmp/...`，「設了 `MSYS_NO_PATHCONV=1` 就**一定**看不懂」。實測沒設也看不懂，讀者可能以為沒設就可以省略 `cygpath`。 | 低 | 改成「Windows 版 Python 看不懂 Git Bash 的 `/tmp/...` 路徑，一律包 `cygpath -m`」。 | 程式（`steps.md` 由程式 Agent 撰寫） |
| O-3 | `curriculum.md` 練習 2、`steps.md` 步驟 3～4 | `before.txt` / `after_preview.txt` 寫在「目前目錄」，也就是專案資料夾。初學者若先 `cd "$demo"` 再執行，比對檔會被當成第一層檔案一起整理（`.txt` → `documents/`），`diff` 結果和預期不符；放在專案資料夾也會留下 git 未追蹤檔（步驟 8 才刪）。 | 低 | 比對檔改放另一個臨時資料夾，例如 `cmp=$(cygpath -m "$(mktemp -d)")`，`ls -R "$demo" > "$cmp/before.txt"`；或註明「不要在 `$demo` 裡面執行」。 | 教學設計（課綱）＋程式（`steps.md`） |
| O-4 | `curriculum.md` 第 2 節先備知識、第 6 堂小活動 | 課綱沒提 `export PYTHONUTF8=1`，在系統編碼 cp950 的 Windows 上，程式的中文訊息（例如「共 7 個檔案…」）可能變亂碼。`steps.md` 步驟 0 有寫，課綱沒有。 | 低 | 第 2 節先備知識補一行「先執行 `export PYTHONUTF8=1`」。 | 教學設計 |
| O-5 | `curriculum.md` 第 4 堂 vs `steps.md` 步驟 7 | 第 4 堂寫 `python -m unittest -v`，`steps.md` 寫 `python -m unittest discover -s . -p 'test_*.py' -v`。兩個都能跑，但初學者會疑惑哪個才對。 | 低 | 擇一統一，或在第 4 堂註明「兩種寫法效果相同，`discover` 是完整寫法」。 | 教學設計 |
| O-6 | `steps.md` 步驟 2、步驟 6 的「你應該看到」 | 預期輸出是 `ls -R` 在互動式終端機的排列（一列多個檔名）；輸出被導向或在非互動環境時會一行一個。內容相同，只有排版不同，不影響操作。 | 低 | 可加一句「排列方式可能不同，檔名一樣就對了」。 | 程式（`steps.md`） |

## 檢查過、沒有障礙的地方

- `curriculum.md` 第 1～6 堂的學習重點與程式概念，和 `organize_downloads.py` 的實作一致（`suffix.lower()`、查表、`iterdir()` + `is_file()`、`reserved` 集合、`argparse --apply`）。
- 4.3 分類表：練習 1 實跑 5/5 符合。
- 4.4 掃描範圍：`subdir/nested.txt` 在預覽和 `--apply` 都沒被處理。
- 4.5 同名與同批次碰撞：情境 B 與練習 3 都得到 `report_1.txt`、`report_1_1.txt`，原檔 `documents/report.txt` 內容不變；`steps.md` 6-加碼得到 `report_2.txt`、`report_1_1.txt`，和文件逐字一致。
- 4.2 錯誤處理：來源不存在、來源不是資料夾，都印清楚訊息並以 exit 2 結束。
- `steps.md` 步驟 0～8 的「你應該看到」全部和實際輸出一致（O-6 的排版差異除外）。
- 單元測試 9 項全數通過，與 `steps.md` 步驟 7 預期相符。
- 安全原則：教材與測試都沒有出現對 `~/Downloads` 執行的指令。

## 重驗結果

> 第 2 輪重驗（`out/prompt-試學-recheck.md`），證據詳見 `out/trial-log.md`〈重驗（第 2 輪）〉R-1～R-7。

| 編號 | 結果 | 證據 |
| --- | --- | --- |
| O-1（高） | 已解決 | 課綱第 3、6 堂與練習 2 都改成 `demo=$(cygpath -m "$(mktemp -d)")`，第 3 堂附 💡 說明。原樣執行三處都是 exit 0、正常輸出，沒有出現「來源資料夾不存在」（R-1、R-2、R-3）。 |
| O-2（低） | 已解決 | `steps.md` 步驟 1 💡 改為「Windows 版 Python 看不懂這種路徑……所以**一律**用 `cygpath -m`」（R-4）。 |
| O-3（低） | 部分解決（`steps.md` 已解決／`curriculum.md` 未解決） | `steps.md` 新增 `cmp` 臨時資料夾放比對檔，步驟 8 一併刪除，實跑正常（R-5）。`curriculum.md` 練習 2 仍是 `ls -R "$demo" > before.txt`，原樣執行後 `git status` 顯示 `?? before.txt`、`?? after_preview.txt`，練習也沒有清理指令（R-3）。→ 殘留部分列為 O-7。 |
| O-4（低） | 已解決 | `curriculum.md` 第 2 節先備知識新增「開始前先執行 `export PYTHONUTF8=1`……」（R-4）。 |
| O-5（低） | 已解決 | `curriculum.md` 第 4 堂改為 `python -m unittest discover -s . -p 'test_*.py' -v`，並註明與簡寫等效（R-4）；實跑 9 tests OK（R-7）。 |
| O-6（低） | 已解決 | `steps.md` 步驟 2、6 都加了「（排列方式可能不同，例如一行一個檔名；檔名一樣就對了。）」（R-4）。 |

### 新發現的障礙

| 編號 | 位置（哪份文件哪一步） | 障礙描述 | 嚴重度（高/中/低） | 建議修正 | 該退回給（教學設計/程式） |
| --- | --- | --- | --- | --- | --- |
| O-7 | `curriculum.md` 練習 2 預期解（O-3 的殘留） | 比對檔 `before.txt`、`after_preview.txt` 仍寫在目前目錄（專案資料夾），會留下 git 未追蹤檔，練習也沒有清理指令；和 `steps.md` 新版的 `cmp` 寫法不一致，初學者兩份文件對照時會困惑。 | 低 | 比照 `steps.md`：加 `cmp=$(cygpath -m "$(mktemp -d)")`，改成 `"$cmp/before.txt"`、`"$cmp/after_preview.txt"`，最後加 `rm -rf "$demo" "$cmp"`。 | 教學設計 |

除 O-7 外沒有新障礙。重新檢查過的地方：課綱第 3、6 堂、練習 2 的原樣操作；`steps.md` 步驟 0～8（含 6-加碼）；prompt 指定的完整假資料（含預先存在的 `documents/report.txt`）；單元測試；兩份文件都沒有對 `~/Downloads` 的指令。
