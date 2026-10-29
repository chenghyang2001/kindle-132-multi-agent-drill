# 理解障礙報告（實例二・試學 Agent）

> 試學身分：剛學 Python 的初學者，照 `curriculum.md` → `steps.md` 實際操作（日誌見 `out/trial-log.md`）。
> 主流程（steps.md 步驟 0～9、8 項測試、三題練習）**全部符合預期**；以下是操作中卡住、可能誤解或有安全風險的地方。

| 編號 | 位置（哪份文件哪一步） | 障礙描述 | 嚴重度（高/中/低） | 建議修正 | 該退回給（教學設計/程式） |
| --- | --- | --- | --- | --- | --- |
| O-1 | `organize_downloads.py` `main()`；`steps.md` 步驟 3、5（`"$TMP"`） | 新開 Git Bash 後 `$TMP` 是空的，`python organize_downloads.py ""` 會把 `Path("")` 當成 `.`，也就是整理**目前所在的資料夾**。我在臨時資料夾只用預覽模式驗證過：它把 `curriculum.md`、`organize_downloads.py`、`steps.md` 都規劃要搬（見 trial-log「額外發現」）。初學者照步驟 0 會待在課程資料夾，這時再跑步驟 5 的 `--apply`，課程檔案就會被搬走。這違反「只動臨時資料夾」的安全原則。 | 高 | 程式：來源參數是空字串（或去掉空白後是空的）時，印 `錯誤：沒有指定資料夾（$TMP 可能是空的）` 到 stderr，exit 2；並補一項測試。教材：步驟 3、5 前加一行 `[ -n "$TMP" ] \|\| echo "TMP 是空的，請回步驟 1"`，並提醒「關掉終端機後 TMP 會不見」。 | 程式（主要）＋教學設計 |
| O-2 | `curriculum.md` 第 1 堂小活動 1「在 Python 互動模式輸入」 | 教材沒說怎麼進入或離開互動模式（輸入 `python` → 看到 `>>>` → 用 `exit()` 離開）。另外 Git Bash（mintty）直接打 `python` 時，互動模式常常卡住沒有反應，有時要改用 `winpty python` 或 `python -i`。**待驗證**：我的執行環境不是互動式終端機，沒辦法實測卡住的現象；我改用 `python -c` 確認輸出是 `photo.JPG photo .JPG .jpg`。 | 中 | 第 1 堂加一小段：「輸入 `python` 會出現 `>>>`；若沒反應改用 `winpty python`；結束輸入 `exit()`」。或改成「把程式存成 `lesson1.py` 再用 `python lesson1.py` 執行」。 | 教學設計 |
| O-3 | `curriculum.md` 第 2～5 堂小活動（「寫一段程式」「寫迴圈印出 `$TMP` 第一層」） | 沒說程式要寫在哪個檔案、怎麼執行。第 3 堂要在 Python 裡讀 `$TMP` 路徑，但還沒教 `sys.argv` 或 `os.environ`，初學者不知道怎麼把 Bash 變數交給 Python。 | 中 | 每堂指定練習檔名（如 `lesson3.py`），給起手式，例如 `import sys; folder = Path(sys.argv[1])`，執行時用 `python lesson3.py "$TMP"`；或直接請學員把 `echo "$TMP"` 的路徑貼進程式。 | 教學設計 |
| O-4 | `curriculum.md` 練習二預期解「驗證方法」第 1、3 步 | 寫的是 `ls -R "$TMP" > before.txt`，括號又說「存在 `$TMP` 外面」。實際上它會存在**目前資料夾**（課程資料夾），留下 `before.txt`、`after.txt` 兩個垃圾檔，而且第 3 節的清理指令 `rm -rf "$TMP"` 不會刪到它們。steps.md 用的是 `"$TMP-before.txt"`，兩份文件寫法不一致，初學者會搞混。 | 低 | 練習二改成跟 steps.md 一樣用 `"$TMP-before.txt"`／`"$TMP-after.txt"`，清理時一併 `rm -f`。 | 教學設計 |
| O-5 | `steps.md` 步驟 7；`organize_downloads.py` 錯誤訊息 | 使用者輸入的是 `C:/.../不存在`（斜線），錯誤訊息印的卻是 `C:\...\不存在`（反斜線）。初學者可能以為路徑被改掉了。steps.md 只寫 `...不存在`，不算錯，但沒有說明為什麼斜線方向不同。 | 低 | 錯誤訊息改用 `source.as_posix()`，跟預覽輸出的斜線一致；或在 steps.md 註明「Windows 會顯示成反斜線，這是正常的」。 | 程式（或教學設計擇一） |
| O-6 | `steps.md` 步驟 0、步驟 2 的「你應該看到」 | 步驟 0 的 `ls` 實際還會看到 `TASK.md`、`out`、`__pycache__`（跑過測試後會出現），steps.md 沒提，初學者可能以為多了東西是錯的。步驟 2 寫成同一行用空白隔開，但 `ls -R` 依終端機寬度和是否導向，也可能一行一個。 | 低 | 步驟 0 加註「可能還有其他檔案或 `__pycache__`，不用理會」；步驟 2 加註「排列方式可能不同，名稱對得上就好」。 | 教學設計 |

## 已檢查、沒有障礙的地方

- `curriculum.md` 第 3 節建臨時資料夾的做法：用 `cygpath -m` 的版本可以正常運作；不加 `cygpath` 會得到 `錯誤：找不到資料夾 \tmp\tmp.xxx`，跟文件說明一致。
- 第 1 堂 `.suffix` 示範、第 5 堂 `table.XLSX`／`archive.tar.gz`／`.gitignore` 的預測題：實際結果跟教材答案一致。
- 程式規格 5.2～5.6（分類表、只掃第一層、預覽不建資料夾、同名不覆寫、`report_1_1.txt`、空資料夾、來源不存在或不是資料夾時 exit 2）：全部照規格運作。
- 測試：任務指定的 `python -m unittest discover -s . -p 'test_*.py' -v` 不加 `PYTHONUTF8` 也是 8 項全過。
- 三題練習的預期解：跟實際執行結果完全一致。
- 沒有修改任何程式或教材，也沒有碰 `~/Downloads`。
