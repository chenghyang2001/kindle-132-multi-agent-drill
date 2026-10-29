# 試學日誌（實例二・第 ③ 棒：試學 Agent）

- 日期：2026-10-30
- 環境：Windows 11 + Git Bash，`python --version` → `Python 3.14.7`
- 做法：先讀 `curriculum.md`，再照 `steps.md` 步驟 0～9 操作。
- 安全：全程只用 `TMP=$(cygpath -m "$(mktemp -d)")` 建立的臨時資料夾，路徑都是 `C:/Users/USER/AppData/Local/Temp/tmp.xxxx`，**沒有碰 `~/Downloads` 或任何真實資料夾**。每次用完都 `rm -rf` 刪掉。
- 以下的命令與輸出都是實際執行後貼上的（`[rc=N]` 是該行命令的 exit code）。

---

## 總結

| 檢查項目 | 結果 |
| --- | --- |
| 預覽前後檔案清單相同（不改檔） | ✅ `diff` 沒有輸出，印出 `預覽沒改檔`；檔案數 9 → 9 |
| `--apply` 後 `subdir/nested.txt` 仍在原地 | ✅ |
| 沒有檔案被覆寫或遺失 | ✅ 檔案總數 9 → 9；練習三用內容 OLD/R0/R1 確認三個 report 各自保留 |
| 同批次碰撞產生 `report_1_1.txt` | ✅ |
| 單元測試 | ✅ `Ran 8 tests ... OK`（加不加 `PYTHONUTF8=1` 都通過） |
| 三題練習：預測 vs 實際 | ✅ 三題都跟預測一致 |
| steps.md 每一步的「你應該看到」 | ✅ 步驟 0～9 全部符合 |

---

## 步驟 0：進到課程資料夾

```text
$ ls
TASK.md
__pycache__
curriculum.md
organize_downloads.py
out
steps.md
test_organize_downloads.py
[rc=0]

$ python --version
Python 3.14.7
```

符合預期：四個指定檔案都在。另外還看到 `TASK.md`、`__pycache__`、`out`，steps.md 沒有提到，但不影響操作（見障礙 O-6）。

## 步驟 1：建立臨時資料夾

```text
$ TMP=$(cygpath -m "$(mktemp -d)")
$ echo "$TMP"
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD
```

符合預期：格式是 `C:/Users/.../Temp/tmp.xxx`，路徑裡沒有 `Downloads`。

## 步驟 2：建立假檔案

```text
$ mkdir -p "$TMP/documents" "$TMP/subdir"
$ touch "$TMP/photo.JPG" "$TMP/notes.txt" "$TMP/table.csv" "$TMP/script.py" "$TMP/README"
$ touch "$TMP/report.txt" "$TMP/report_1.txt" "$TMP/subdir/nested.txt"
$ touch "$TMP/documents/report.txt"
$ ls -R "$TMP"
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD:
README
documents
notes.txt
photo.JPG
report.txt
report_1.txt
script.py
subdir
table.csv

C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/documents:
report.txt

C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/subdir:
nested.txt

$ find "$TMP" -type f | wc -l
9
```

符合預期：第一層 9 個項目，`documents/report.txt`、`subdir/nested.txt` 都在，總數 9。
（steps.md 寫成一行 `README  documents  notes.txt ...`，我這裡 `ls` 被導到非終端機時一行一個；兩者內容相同。）

## 步驟 3：先預覽

```text
$ ls -R "$TMP" > "$TMP-before.txt"
$ PYTHONUTF8=1 python organize_downloads.py "$TMP"
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
README -> no_extension/README
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
這是預覽，加 --apply 才會實際移動。
[rc=0]
```

符合預期：8 行跟 steps.md 完全相同；`subdir/nested.txt` 沒出現在清單裡。

## 步驟 4：確認預覽沒改檔

```text
$ ls -R "$TMP" | diff "$TMP-before.txt" - && echo "預覽沒改檔"
預覽沒改檔

$ find "$TMP" -type f | wc -l
9
```

符合預期：`diff` 沒有差異，也沒有多出 `images/` 等資料夾；檔案數仍是 9。

## 步驟 5：加 `--apply`

```text
$ PYTHONUTF8=1 python organize_downloads.py "$TMP" --apply
已移動：notes.txt -> documents/notes.txt
已移動：photo.JPG -> images/photo.JPG
已移動：README -> no_extension/README
已移動：report.txt -> documents/report_1.txt
已移動：report_1.txt -> documents/report_1_1.txt
已移動：script.py -> code/script.py
已移動：table.csv -> data/table.csv
完成：已移動 7 個檔案。
[rc=0]
```

符合預期：跟 steps.md 完全相同，總數 7。

## 步驟 6：檢查結果

```text
$ ls -R "$TMP"
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD:
code
data
documents
images
no_extension
subdir

.../code:
script.py

.../data:
table.csv

.../documents:
notes.txt
report.txt
report_1.txt
report_1_1.txt

.../images:
photo.JPG

.../no_extension:
README

.../subdir:
nested.txt

$ find "$TMP" -type f | wc -l
9

$ find "$TMP" -type f | sort
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/code/script.py
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/data/table.csv
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/documents/notes.txt
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/documents/report.txt
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/documents/report_1.txt
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/documents/report_1_1.txt
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/images/photo.JPG
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/no_extension/README
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD/subdir/nested.txt
```

（`ls -R` 的子資料夾標題為了好讀，縮寫成 `...`；完整路徑都在上面 `find` 的輸出裡。）

符合預期：

- 第一層只剩 6 個資料夾。
- `documents/` 有 `notes.txt  report.txt  report_1.txt  report_1_1.txt`，三個 report 都在。
- `images/photo.JPG` 大小寫沒變。
- `subdir/nested.txt` 仍在原地。
- 檔案總數 9，跟步驟 2 一樣：沒有遺失或覆寫。

## 步驟 7（加碼）：錯誤情況

```text
$ PYTHONUTF8=1 python organize_downloads.py "$TMP/不存在"; echo "exit code = $?"
錯誤：找不到資料夾 C:\Users\USER\AppData\Local\Temp\tmp.3BufdHtHDD\不存在
exit code = 2

$ mkdir "$TMP/empty"
$ PYTHONUTF8=1 python organize_downloads.py "$TMP/empty"; echo "exit code = $?"
沒有要整理的檔案
exit code = 0
```

符合預期。我額外多試了兩種情況（steps.md 沒有要求）：

```text
$ PYTHONUTF8=1 python organize_downloads.py "$TMP/images/photo.JPG"; echo "exit code = $?"
錯誤：C:\Users\USER\AppData\Local\Temp\tmp.3BufdHtHDD\images\photo.JPG 不是資料夾
exit code = 2

$ PYTHONUTF8=1 python organize_downloads.py "$TMP"; echo "exit code = $?"   # 已整理過再跑一次
沒有要整理的檔案
exit code = 0
```

符合 curriculum 5.6 的規格。分類資料夾不會被再整理一次。

## 步驟 8：自動測試

依任務指定的寫法（不加 `PYTHONUTF8`）和 steps.md 的寫法（有加）各跑一次：

```text
$ python -m unittest discover -s . -p 'test_*.py' -v
test_bad_source_exit_code (test_organize_downloads.OrganizeDownloadsTest.test_bad_source_exit_code) ... ok
test_categories_case_insensitive (test_organize_downloads.OrganizeDownloadsTest.test_categories_case_insensitive) ... ok
test_empty_folder (test_organize_downloads.OrganizeDownloadsTest.test_empty_folder) ... ok
test_existing_target_collision (test_organize_downloads.OrganizeDownloadsTest.test_existing_target_collision) ... ok
test_no_extension (test_organize_downloads.OrganizeDownloadsTest.test_no_extension) ... ok
test_preview_does_not_change_files (test_organize_downloads.OrganizeDownloadsTest.test_preview_does_not_change_files) ... ok
test_same_batch_collision (test_organize_downloads.OrganizeDownloadsTest.test_same_batch_collision) ... ok
test_subdir_not_moved (test_organize_downloads.OrganizeDownloadsTest.test_subdir_not_moved) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.044s

OK
[rc=0]

$ PYTHONUTF8=1 python -m unittest discover -s . -p 'test_*.py' -v
（同上 8 行 ok）
Ran 8 tests in 0.073s

OK
[rc=0]
```

符合預期：8 行 `ok`，最後是 `OK`。測試涵蓋 curriculum 5.8 要求的 7 項，另外多一項錯誤 exit code。

## 步驟 9：刪掉臨時資料夾

```text
$ echo "$TMP"
C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD
$ rm -rf "$TMP" "$TMP-before.txt"
$ ls "$TMP" 2>&1
ls: cannot access 'C:/Users/USER/AppData/Local/Temp/tmp.3BufdHtHDD': No such file or directory
```

符合預期。

---

## 課綱小活動抽查

### 第 1 堂（互動模式的內容改用 `python -c` 執行）

```text
$ PYTHONUTF8=1 python -c 'from pathlib import Path
file_path = Path("photo.JPG")
print(file_path.name, file_path.stem, file_path.suffix, file_path.suffix.lower())
print(repr(Path("README").suffix)); print(repr(Path(".gitignore").suffix))'
photo.JPG photo .JPG .jpg
''
''
```

符合 curriculum：`photo.JPG photo .JPG .jpg`；`README`、`.gitignore` 的 suffix 都是 `''`。
**待驗證**：在 Git Bash 直接輸入 `python` 進入互動模式（`>>>`）這件事，我沒有實際操作，因為我的執行環境不是互動式終端機（見障礙 O-2）。

### 第 5 堂小活動 3（先預測再核對）

我的預測：`table.XLSX` → `data/`；`archive.tar.gz` → `others/`（只看 `.gz`）；`.gitignore` → `no_extension/`。

```text
$ touch "$TMP/table.XLSX" "$TMP/archive.tar.gz" "$TMP/.gitignore"
$ PYTHONUTF8=1 python organize_downloads.py "$TMP"
.gitignore -> no_extension/.gitignore
archive.tar.gz -> others/archive.tar.gz
table.XLSX -> data/table.XLSX
這是預覽，加 --apply 才會實際移動。
```

預測正確。

### 環境說明驗證

不加 `cygpath -m` 時（驗證 curriculum／steps 步驟 1 的說法）：

```text
RAW=/tmp/tmp.1zVmTyaXSR
$ PYTHONUTF8=1 python organize_downloads.py "$RAW"
錯誤：找不到資料夾 \tmp\tmp.1zVmTyaXSR
exit=2
```

跟 steps.md 的說明一致：沒有轉換的話，Python 會回報找不到資料夾。

不加 `PYTHONUTF8=1` 時，這台機器的中文輸出沒有亂碼：

```text
$ python organize_downloads.py "$T2"
a.txt -> documents/a.txt
這是預覽，加 --apply 才會實際移動。
exit=0
```

---

## 三題練習

### 練習一：預測分類結果

**我的預測（執行前寫下）**：photo.JPG → `images/`（`.JPG` 轉小寫成 `.jpg`）、notes.txt → `documents/`、table.csv → `data/`、script.py → `code/`、README → `no_extension/`。輸出會按檔名排序，大寫的 `README` 排在 `script.py` 前面。

```text
$ touch "$TMP/photo.JPG" "$TMP/notes.txt" "$TMP/table.csv" "$TMP/script.py" "$TMP/README"
$ PYTHONUTF8=1 python organize_downloads.py "$TMP"
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
README -> no_extension/README
script.py -> code/script.py
table.csv -> data/table.csv
這是預覽，加 --apply 才會實際移動。
```

**核對**：5 個檔案都跟預測一致，也跟 curriculum 的預期解一致。目的檔名保留 `photo.JPG` 的大寫。

### 練習二：比較預覽與 `--apply`

**我的預測**：預覽只印清單和提示，`diff` 不會有輸出、檔案數 5 → 5、不會多出資料夾；`--apply` 會建立 5 個分類資料夾並搬完 5 個檔案，最後印 `完成：已移動 5 個檔案。`，檔案數仍是 5。

（清單檔存到 `$TMP-before.txt`，也就是 `$TMP` 外面；curriculum 寫的是 `before.txt`，見障礙 O-4。）

```text
$ ls -R "$TMP" > "$TMP-before.txt"
$ find "$TMP" -type f | wc -l
5
$ PYTHONUTF8=1 python organize_downloads.py "$TMP"
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
README -> no_extension/README
script.py -> code/script.py
table.csv -> data/table.csv
這是預覽，加 --apply 才會實際移動。
$ ls -R "$TMP" > "$TMP-after.txt"
$ diff "$TMP-before.txt" "$TMP-after.txt"; echo "diff rc=$?"
diff rc=0
$ PYTHONUTF8=1 python organize_downloads.py "$TMP" --apply
已移動：notes.txt -> documents/notes.txt
已移動：photo.JPG -> images/photo.JPG
已移動：README -> no_extension/README
已移動：script.py -> code/script.py
已移動：table.csv -> data/table.csv
完成：已移動 5 個檔案。
$ ls -R "$TMP"
.../tmp.1FYV3WDOqJ:
code
data
documents
images
no_extension
（各資料夾內分別是 script.py / table.csv / notes.txt / photo.JPG / README）
$ find "$TMP" -type f | wc -l
5
```

**核對**：跟預測一致。預覽前後 `diff` 沒有輸出（rc=0），`--apply` 之前和之後的檔案數都是 5。

### 練習三：同批次碰撞與「只掃第一層」

**我的預測**：

- (a) `report.txt` → `documents/report.txt` 已經存在，所以改成 `documents/report_1.txt` 並記進 reserved。`report_1.txt` 想去 `documents/report_1.txt`，那個位置剛被前一個檔案預訂了，所以改成 `documents/report_1_1.txt`。
- (b) `subdir/nested.txt` 不會動，因為程式只掃第一層。

為了確認沒有覆寫，我在三個檔案裡各寫入不同內容（舊檔 OLD、report.txt R0、report_1.txt R1）：

```text
$ mkdir -p "$TMP/documents" "$TMP/subdir"
$ touch "$TMP/documents/report.txt" "$TMP/report.txt" "$TMP/report_1.txt" "$TMP/subdir/nested.txt"
$ echo OLD > "$TMP/documents/report.txt"; echo R0 > "$TMP/report.txt"; echo R1 > "$TMP/report_1.txt"
$ find "$TMP" -type f | wc -l
4
$ PYTHONUTF8=1 python organize_downloads.py "$TMP"
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
這是預覽，加 --apply 才會實際移動。
$ PYTHONUTF8=1 python organize_downloads.py "$TMP" --apply
已移動：report.txt -> documents/report_1.txt
已移動：report_1.txt -> documents/report_1_1.txt
完成：已移動 2 個檔案。
$ ls -R "$TMP"
.../tmp.UE4N2ktA6M:
documents
subdir

.../documents:
report.txt
report_1.txt
report_1_1.txt

.../subdir:
nested.txt
$ for f in "$TMP"/documents/*; do echo "$(basename "$f"): $(cat "$f")"; done
report.txt: OLD
report_1.txt: R0
report_1_1.txt: R1
$ find "$TMP" -type f | wc -l
4
```

**核對**：跟預測一致。內容 OLD／R0／R1 各自保留，證明舊檔沒有被覆寫；檔案數 4 → 4；`subdir/nested.txt` 沒動。

---

## 額外發現：`$TMP` 是空的時候，程式會整理「目前所在的資料夾」

情境：初學者關掉 Git Bash 再開一個新的，接著直接從步驟 3 或步驟 5 往下做。新視窗沒有 `TMP` 這個變數，`"$TMP"` 就變成空字串。我在另一個臨時資料夾裡放了 3 個假的教材檔模擬這種情況，**只跑預覽**：

```text
$ cd C:/Users/USER/AppData/Local/Temp/tmp.LUgoLszw4a   # 模擬：使用者人在某資料夾，且新開終端機 TMP 未設定
$ echo "[$TMP]"
[]
$ PYTHONUTF8=1 python organize_downloads.py "$TMP"   # 只跑預覽
curriculum.md -> documents/curriculum.md
organize_downloads.py -> code/organize_downloads.py
steps.md -> documents/steps.md
這是預覽，加 --apply 才會實際移動。
exit=0
```

`Path("")` 等於 `.`，也就是目前所在的資料夾。如果使用者正照 steps.md 步驟 0 待在課程資料夾裡，再跑步驟 5 的 `--apply`，課程檔案（包括 `organize_downloads.py` 本身）就會被搬進 `code/`、`documents/`。詳見障礙 O-1。
