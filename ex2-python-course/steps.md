# 操作步驟：用臨時假資料試跑 organize_downloads.py

> 環境：Windows + Git Bash，指令用 `python`（不是 `python3`）。
> **全程只用臨時資料夾，絕對不要對 `~/Downloads` 執行。**
> 中文若顯示亂碼，在 `python` 前面加 `PYTHONUTF8=1`（下面的指令都已經加好）。

---

## 步驟 0：進到課程資料夾

```bash
cd ex2-python-course      # 換成你電腦上課程資料夾的實際位置
ls
```

**你應該看到**：清單裡有 `organize_downloads.py`、`test_organize_downloads.py`、`steps.md`、`curriculum.md`。
（可能還有 `TASK.md`、`out`、`__pycache__` 等，不用理會。）

---

## 步驟 1：建立臨時資料夾

```bash
TMP=$(cygpath -m "$(mktemp -d)")
echo "$TMP"
```

**你應該看到**：類似 `C:/Users/你的名字/AppData/Local/Temp/tmp.AbC123xyz` 的路徑（每次都不一樣）。
**確認路徑裡沒有 `Downloads`** 再往下做。

> 為什麼要加 `cygpath -m`？Git Bash 的 `mktemp -d` 會給 `/tmp/tmp.xxx` 這種路徑，
> 但 Windows 版 Python 看不懂，會回「錯誤：找不到資料夾」。
> `cygpath -m` 把它轉成 `C:/...` 格式，Git Bash 和 Python 都看得懂。

> ⚠️ **`TMP` 只存在這個終端機視窗裡。** 關掉終端機（或開新視窗）後 `TMP` 會變成空的，
> 這時要**重做步驟 1、2**。後面每次執行程式前都會先檢查一次 `TMP` 是不是空的。

---

## 步驟 2：建立假檔案

```bash
mkdir -p "$TMP/documents" "$TMP/subdir"
touch "$TMP/photo.JPG" "$TMP/notes.txt" "$TMP/table.csv" "$TMP/script.py" "$TMP/README"
touch "$TMP/report.txt" "$TMP/report_1.txt" "$TMP/subdir/nested.txt"
touch "$TMP/documents/report.txt"     # 先在目的地放一個同名檔，等一下看碰撞
ls -R "$TMP"
find "$TMP" -type f | wc -l
```

**你應該看到**：

- 第一層有 `README  documents  notes.txt  photo.JPG  report.txt  report_1.txt  script.py  subdir  table.csv`
  （排列方式可能不同，例如一行一個，名稱對得上就好）
- `documents:` 底下有 `report.txt`
- `subdir:` 底下有 `nested.txt`
- 最後一行數字是 `9`（總共 9 個檔案）

---

## 步驟 3：先預覽（不會動任何檔案）

```bash
if [ -z "$TMP" ]; then
  echo "TMP 是空的，請回步驟 1"
else
  ls -R "$TMP" > "$TMP-before.txt"      # 先存一份「執行前」清單（存在 $TMP 外面）
  PYTHONUTF8=1 python organize_downloads.py "$TMP"
fi
```

整段一起貼上即可。`TMP` 是空的時，只會印 `TMP 是空的，請回步驟 1`，其他指令**都不會執行**（不會產生 `-before.txt`），這時回步驟 1、2 重建。
（就算漏了檢查，程式也會印 `錯誤：沒有指定資料夾（$TMP 可能是空的，請回步驟 1 重新建立）` 並停下，不會整理目前的資料夾。）

**你應該看到**：

```text
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
README -> no_extension/README
report.txt -> documents/report_1.txt
report_1.txt -> documents/report_1_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
這是預覽，加 --apply 才會實際移動。
```

注意 `report.txt` 變成 `report_1.txt`（因為 `documents/report.txt` 已經存在），
`report_1.txt` 又變成 `report_1_1.txt`（因為 `report_1.txt` 這個位置已經被前一個檔案預訂了）。
`subdir/nested.txt` 沒出現在清單裡——程式只看第一層。

---

## 步驟 4：確認預覽真的沒改檔

```bash
ls -R "$TMP" | diff "$TMP-before.txt" - && echo "預覽沒改檔"
```

**你應該看到**：只有一行 `預覽沒改檔`。
`diff` 沒印出任何差異，代表預覽前後的檔案清單一模一樣，也沒有多出 `images/` 之類的資料夾。

---

## 步驟 5：加 `--apply` 實際移動

```bash
if [ -z "$TMP" ]; then
  echo "TMP 是空的，請回步驟 1"
else
  PYTHONUTF8=1 python organize_downloads.py "$TMP" --apply
fi
```

若只印出 `TMP 是空的，請回步驟 1`，代表終端機重開過，程式沒有執行，回步驟 1 重來。

**你應該看到**：

```text
已移動：notes.txt -> documents/notes.txt
已移動：photo.JPG -> images/photo.JPG
已移動：README -> no_extension/README
已移動：report.txt -> documents/report_1.txt
已移動：report_1.txt -> documents/report_1_1.txt
已移動：script.py -> code/script.py
已移動：table.csv -> data/table.csv
完成：已移動 7 個檔案。
```

---

## 步驟 6：檢查結果

```bash
ls -R "$TMP"
find "$TMP" -type f | wc -l
```

**你應該看到**：

- 第一層只剩資料夾：`code  data  documents  images  no_extension  subdir`
- `documents:` 底下有 `notes.txt  report.txt  report_1.txt  report_1_1.txt`（三個 report 都在，沒有被覆寫）
- `images:` 底下是 `photo.JPG`（檔名大小寫沒變）
- `subdir:` 底下仍然是 `nested.txt`（子資料夾沒被動）
- 檔案總數仍是 `9`，和步驟 2 一樣

---

## 步驟 7（加碼）：試試錯誤情況

```bash
if [ -z "$TMP" ]; then
  echo "TMP 是空的，請回步驟 1"
else
  PYTHONUTF8=1 python organize_downloads.py "$TMP/不存在"; echo "exit code = $?"
  mkdir "$TMP/empty"
  PYTHONUTF8=1 python organize_downloads.py "$TMP/empty"; echo "exit code = $?"
  PYTHONUTF8=1 python organize_downloads.py ""; echo "exit code = $?"
fi
```

**你應該看到**：

- 第一個：`錯誤：找不到資料夾 C:/Users/.../Temp/tmp.xxx/不存在`（斜線方向跟你輸入的一樣），接著 `exit code = 2`
- 第二個：`沒有要整理的檔案`，接著 `exit code = 0`
- 第三個（模擬 `TMP` 是空的）：`錯誤：沒有指定資料夾（$TMP 可能是空的，請回步驟 1 重新建立）`，接著 `exit code = 2`，目前資料夾的檔案完全沒被動

---

## 步驟 8：跑自動測試

```bash
PYTHONUTF8=1 python -m unittest discover -s . -p 'test_*.py' -v
```

**你應該看到**：9 行 `... ok`，最後是

```text
Ran 9 tests in 0.0xxs

OK
```

（測試會自己建臨時資料夾，不會碰你的 `$TMP`，也不會碰真實資料夾。）

---

## 步驟 9：刪掉臨時資料夾

```bash
echo "$TMP"                     # 再確認一次：這是你在步驟 1 建的臨時路徑
rm -rf "$TMP" "$TMP-before.txt"
ls "$TMP" 2>&1
```

**你應該看到**：`ls` 回報 `No such file or directory`，代表已經刪乾淨。
**只刪 `$TMP`**，不要手滑改成其他路徑。
