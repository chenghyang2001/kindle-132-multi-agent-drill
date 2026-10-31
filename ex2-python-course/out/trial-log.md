# 試學日誌（實例二：Python 入門課，接力第 ③ 棒）

> 試學者身分：剛學 Python 的初學者。先讀 `curriculum.md`，再照 `steps.md` 逐步操作。
> 環境：Windows 10 + Git Bash，`Python 3.14.3`，`PYTHONUTF8=1`，本機已設 `MSYS_NO_PATHCONV=1`。
> 全程只在 `mktemp -d` 建的臨時資料夾操作，**沒有碰 `~/Downloads` 或任何真實資料夾**；跑完都已 `rm -rf`。
> 以下輸出皆為實際執行結果（以 `set -x` 記錄命令）；唯一改動是把本機帳號名稱遮成 `<帳號>`，臨時資料夾名稱縮寫為 `tmp.XXXX`。
> 為避免比對檔留在專案資料夾，`before.txt` / `after_preview.txt` 放在另一個 `mktemp -d` 資料夾（`$cmp`），與 `steps.md` 寫在目前目錄的做法略有不同，不影響結果。

---

## 情境 A：完全照 `steps.md` 步驟 0～8

### 步驟 0：確認 Python

```text
$ python --version
Python 3.14.3
```

符合預期（3.10 以上）✅

### 步驟 1：建立臨時資料夾

```text
$ demo=$(cygpath -m "$(mktemp -d)")
$ echo "$demo"
C:/Users/<帳號>/AppData/Local/Temp/tmp.7Gi867OUWY
```

符合預期（`C:/...Temp/tmp.xxx` 格式）✅

### 步驟 2：建立假檔案

```text
$ touch "$demo/photo.JPG" "$demo/notes.txt" "$demo/table.csv" "$demo/script.py" \
        "$demo/README" "$demo/report.txt" "$demo/report_1.txt"
$ mkdir "$demo/subdir" && touch "$demo/subdir/nested.txt"
$ ls -R "$demo"
C:/Users/<帳號>/AppData/Local/Temp/tmp.7Gi867OUWY:
README
notes.txt
photo.JPG
report.txt
report_1.txt
script.py
subdir
table.csv

C:/Users/<帳號>/AppData/Local/Temp/tmp.7Gi867OUWY/subdir:
nested.txt
```

內容符合預期 ✅（我的 shell 不是互動式終端機，所以 `ls` 一行一個；在一般終端機會像 `steps.md` 那樣排成一列，內容相同。）

### 步驟 3：預覽

```text
$ ls -R "$demo" > "$cmp/before.txt"
$ python organize_downloads.py "$demo"
README -> no_extension/README
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
report.txt -> documents/report.txt
report_1.txt -> documents/report_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
共 7 個檔案（預覽模式，沒有移動任何檔案）
加 --apply 才會實際移動
exit=0
```

和 `steps.md` 預期逐字相同 ✅；`subdir/nested.txt` 沒有出現 ✅

### 步驟 4：確認預覽沒改檔

```text
$ ls -R "$demo" > "$cmp/after_preview.txt"
$ diff "$cmp/before.txt" "$cmp/after_preview.txt" && echo "預覽沒有改檔"
預覽沒有改檔
```

符合預期 ✅

### 步驟 5：`--apply`

```text
$ python organize_downloads.py "$demo" --apply
README -> no_extension/README
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
report.txt -> documents/report.txt
report_1.txt -> documents/report_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
已移動 7 個檔案
exit=0
```

符合預期 ✅

### 步驟 6：檢查結果

```text
$ (cd "$demo" && ls -R)
.:
code
data
documents
images
no_extension
subdir

./code:
script.py

./data:
table.csv

./documents:
notes.txt
report.txt
report_1.txt

./images:
photo.JPG

./no_extension:
README

./subdir:
nested.txt

$ find "$demo" -type f | wc -l
8
```

符合預期 ✅；檔案總數：前 8（7 個第一層 + `subdir/nested.txt`）＝ 後 8，沒有遺失 ✅

```text
$ python organize_downloads.py "$demo"
沒有要整理的檔案
```

符合預期 ✅

### 步驟 6-加碼：同名不覆寫

```text
$ touch "$demo/report.txt" "$demo/report_1.txt"
$ python organize_downloads.py "$demo"
report.txt -> documents/report_2.txt
report_1.txt -> documents/report_1_1.txt
共 2 個檔案（預覽模式，沒有移動任何檔案）
加 --apply 才會實際移動
```

和 `steps.md` 預期逐字相同 ✅

### 步驟 8：刪除臨時資料夾

```text
$ rm -rf "$demo" "$cmp"
$ ls "$demo"
ls: cannot access 'C:/Users/<帳號>/AppData/Local/Temp/tmp.7Gi867OUWY': No such file or directory
```

符合預期 ✅

---

## 情境 B：prompt 指定的完整假資料（目的地已有 `documents/report.txt`）

假資料：`photo.JPG`、`notes.txt`、`table.csv`、`script.py`、`README`、`report.txt`、`report_1.txt`、`subdir/nested.txt`，另外先建 `documents/report.txt`（內容 `ORIGINAL`）。來源的 `report.txt` / `report_1.txt` 分別寫入 `SRC-report` / `SRC-report_1`，用來確認沒有被覆寫。

```text
$ mkdir "$demo/documents" && echo "ORIGINAL" > "$demo/documents/report.txt"
$ echo "SRC-report" > "$demo/report.txt"; echo "SRC-report_1" > "$demo/report_1.txt"
$ find "$demo" -type f | sort > "$cmp/before.txt"; wc -l < "$cmp/before.txt"
9

$ python organize_downloads.py "$demo"
README -> no_extension/README
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
共 7 個檔案（預覽模式，沒有移動任何檔案）
加 --apply 才會實際移動

$ find "$demo" -type f | sort > "$cmp/after_preview.txt"
$ diff "$cmp/before.txt" "$cmp/after_preview.txt" && echo "預覽沒有改檔"
預覽沒有改檔

$ python organize_downloads.py "$demo" --apply
README -> no_extension/README
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
已移動 7 個檔案

$ (cd "$demo" && find . -type f | sort)
./code/script.py
./data/table.csv
./documents/notes.txt
./documents/report.txt
./documents/report_1.txt
./documents/report_1_1.txt
./images/photo.JPG
./no_extension/README
./subdir/nested.txt

$ find "$demo" -type f | wc -l
9
$ test -f "$demo/subdir/nested.txt" && echo "nested.txt 仍在原地"
nested.txt 仍在原地
$ cat "$demo/documents/report.txt" "$demo/documents/report_1.txt" "$demo/documents/report_1_1.txt"
ORIGINAL
SRC-report
SRC-report_1
```

| 必查項目 | 結果 |
| --- | --- |
| 預覽前後檔案清單相同 | ✅ `diff` 無差異 |
| `--apply` 後 `subdir/nested.txt` 仍在原地 | ✅ |
| 檔案總數不變（沒有遺失） | ✅ 前 9 ＝ 後 9 |
| 沒有覆寫 | ✅ `documents/report.txt` 仍是 `ORIGINAL`，兩個來源檔內容各自保留 |
| 同批次碰撞出現 `report_1_1.txt` | ✅ |

結果與 `curriculum.md` 4.5 節範例、練習 3 預期解一致 ✅

---

## 額外檢查：照 `curriculum.md` 原寫法（不包 `cygpath`）

`curriculum.md` 第 3 堂、第 6 堂小活動、練習 2 都寫 `demo=$(mktemp -d)`，沒有 `cygpath -m`。

```text
$ echo "MSYS_NO_PATHCONV=${MSYS_NO_PATHCONV:-<未設>}"
MSYS_NO_PATHCONV=1
$ raw=$(mktemp -d); touch "$raw/photo.JPG"
$ python organize_downloads.py "$raw"; echo "exit=$?"
錯誤：來源資料夾不存在：\tmp\tmp.kBR2DKBlAg
exit=2

$ env -u MSYS_NO_PATHCONV python organize_downloads.py "$raw"; echo "exit=$?"
錯誤：來源資料夾不存在：\tmp\tmp.kBR2DKBlAg
exit=2

$ env -u MSYS_NO_PATHCONV bash --norc --noprofile -c 'raw=$(mktemp -d); touch "$raw/photo.JPG"; python organize_downloads.py "$raw"; echo "exit=$?"; rm -rf "$raw"'
錯誤：來源資料夾不存在：\tmp\tmp.bp9i4eB2pg
exit=2
```

❌ 照課綱原寫法會失敗。就算拿掉 `MSYS_NO_PATHCONV`、開一個乾淨的 bash 也一樣失敗，所以不只是「設了那個變數」才會出問題（和 `steps.md` 那段 💡 說明的「有時」不同）。用 `steps.md` 的 `cygpath -m` 寫法就沒問題。→ 列入障礙 O-1。

## 額外檢查：來源不是資料夾

```text
$ f=$(cygpath -m "$(mktemp)"); python organize_downloads.py "$f"; echo "exit=$?"
錯誤：來源不是資料夾：C:\Users\<帳號>\AppData\Local\Temp\tmp.okPAPZ4rcq
exit=2
```

符合 `steps.md`「常見錯誤」表 ✅

---

## 步驟 7：單元測試

```text
$ python -m unittest discover -s . -p 'test_*.py' -v
test_general_categories_with_uppercase (test_organize_downloads.TestCategoryFor.test_general_categories_with_uppercase)
一般分類，含 .JPG 大寫。 ... ok
test_no_extension (test_organize_downloads.TestCategoryFor.test_no_extension)
無副檔名進 no_extension，不是 others。 ... ok
test_apply_moves_files (test_organize_downloads.TestOrganize.test_apply_moves_files)
--apply 會建立分類資料夾並移動檔案。 ... ok
test_empty_folder (test_organize_downloads.TestOrganize.test_empty_folder)
空資料夾印「沒有要整理的檔案」。 ... ok
test_existing_name_not_overwritten (test_organize_downloads.TestOrganize.test_existing_name_not_overwritten)
目的地已有同名檔 → 改名 _1，原檔不被覆寫。 ... ok
test_missing_source_exit_2 (test_organize_downloads.TestOrganize.test_missing_source_exit_2)
來源不存在 → stderr 錯誤、exit code 2。 ... ok
test_preview_does_not_change_files (test_organize_downloads.TestOrganize.test_preview_does_not_change_files)
預覽模式前後檔案清單完全一樣。 ... ok
test_same_batch_collision (test_organize_downloads.TestOrganize.test_same_batch_collision)
同批次碰撞：report.txt → report_1.txt，report_1.txt → report_1_1.txt。 ... ok
test_subfolder_not_moved (test_organize_downloads.TestOrganize.test_subfolder_not_moved)
子資料夾與其內容不移動。 ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.037s

OK
exit=0
```

符合預期（9 項全 ok）✅

---

## 三題練習（先預測，再實跑核對）

### 練習 1：預測分類

**我的預測（執行前）**：`photo.JPG` → `images`（`.JPG` 先轉小寫成 `.jpg`）、`notes.txt` → `documents`、`table.csv` → `data`、`script.py` → `code`、`README` → `no_extension`（沒有副檔名，`suffix` 是空字串，不是 `others`）。

**實跑**：

```text
$ python -c "
from organize_downloads import category_for
for n in ['photo.JPG','notes.txt','table.csv','script.py','README']:
    print(n, '->', category_for(n))
"
photo.JPG -> images
notes.txt -> documents
table.csv -> data
script.py -> code
README -> no_extension
```

預測 5/5 正確，與課綱預期解一致 ✅

### 練習 2：比較預覽與 `--apply`

**我的預測**：預覽印 2 行「來源 -> 目的」加總結，`diff` 無差異；`--apply` 後只剩 `documents/notes.txt`、`images/photo.JPG`，根目錄沒有檔案。另外預測：照課綱原文 `demo=$(mktemp -d)` 會出現「來源資料夾不存在」（見上面的額外檢查），所以我改用 `steps.md` 的 `cygpath -m` 寫法。

**實跑**（路徑包 `cygpath -m`，比對檔放 `$cmp`）：

```text
$ touch "$demo/photo.JPG" "$demo/notes.txt"
$ ls -R "$demo" > "$cmp/before.txt"
$ python organize_downloads.py "$demo"
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
共 2 個檔案（預覽模式，沒有移動任何檔案）
加 --apply 才會實際移動
$ ls -R "$demo" > "$cmp/after_preview.txt"
$ diff "$cmp/before.txt" "$cmp/after_preview.txt" && echo "預覽沒有改檔"
預覽沒有改檔
$ python organize_downloads.py "$demo" --apply
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
已移動 2 個檔案
$ (cd "$demo" && ls -R)
.:
documents
images

./documents:
notes.txt

./images:
photo.JPG
```

預測正確，與課綱預期解一致 ✅（前提：路徑要包 `cygpath -m`）

### 練習 3：同批次碰撞與第一層限制

**我的預測**：`report.txt` → `documents/report_1.txt`（因為 `documents/report.txt` 已存在）；`report_1.txt` → `documents/report_1_1.txt`（`report_1.txt` 剛被保留）；原本的 `documents/report.txt` 不動；`subdir/nested.txt` 不處理、留在原地。

**實跑**：

```text
$ mkdir "$demo/documents" "$demo/subdir"
$ touch "$demo/documents/report.txt" "$demo/report.txt" "$demo/report_1.txt" "$demo/subdir/nested.txt"
$ python organize_downloads.py "$demo" --apply
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
已移動 2 個檔案
$ (cd "$demo" && find . -type f | sort)
./documents/report.txt
./documents/report_1.txt
./documents/report_1_1.txt
./subdir/nested.txt
```

預測正確，與課綱預期解一致 ✅

---

## 結論

- `steps.md` 步驟 0～8（含 6-加碼）全部實際執行，輸出都和「你應該看到」相符；沒有「待驗證」的步驟。
- prompt 指定的必查項目（預覽不改檔、`nested.txt` 留在原地、檔案數不變、不覆寫、出現 `report_1_1.txt`）全部通過。
- 9 項單元測試全部通過。
- 主要障礙：`curriculum.md` 範例指令用沒包 `cygpath` 的 `mktemp -d`，在本機會失敗（詳見 `obstacles.md` O-1）。
