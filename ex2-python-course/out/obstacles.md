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
