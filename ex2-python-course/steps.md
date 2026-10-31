# 操作步驟：用 `organize_downloads.py` 整理臨時資料夾

> 環境：Windows + Git Bash，Python 3.10 以上，一律用 `python`（不是 `python3`）。
> 🔴 **安全原則**：全程只用 `mktemp -d` 建的臨時資料夾，**不要**對你真正的下載資料夾執行。

以下指令都在本專案資料夾（有 `organize_downloads.py` 的那層）執行。

---

## 步驟 0：進到專案資料夾、確認 Python

```bash
cd ex2-python-course        # 換成你放這份教材的位置
python --version
export PYTHONUTF8=1         # 讓中文訊息不會變亂碼
```

**你應該看到**：`Python 3.10.x` 以上的版本號（例如 `Python 3.12.4`）。

---

## 步驟 1：建立臨時資料夾

```bash
demo=$(cygpath -m "$(mktemp -d)")
echo "$demo"
```

**你應該看到**：一個類似 `C:/Users/你的帳號/AppData/Local/Temp/tmp.AbC123xyz` 的路徑。

> 💡 為什麼要包一層 `cygpath -m`？`mktemp -d` 給的是 Git Bash 的 `/tmp/...` 路徑，
> Windows 版 Python 有時看不懂（電腦若設了 `MSYS_NO_PATHCONV=1` 就一定看不懂，
> 會出現「來源資料夾不存在」）。`cygpath -m` 把它轉成 `C:/...` 格式，Git Bash 和 Python 都看得懂。

---

## 步驟 2：建立假檔案

```bash
touch "$demo/photo.JPG" "$demo/notes.txt" "$demo/table.csv" "$demo/script.py" \
      "$demo/README" "$demo/report.txt" "$demo/report_1.txt"
mkdir "$demo/subdir" && touch "$demo/subdir/nested.txt"
ls -R "$demo"
```

**你應該看到**：

```text
C:/Users/.../tmp.AbC123xyz:
README  notes.txt  photo.JPG  report.txt  report_1.txt  script.py  subdir  table.csv

C:/Users/.../tmp.AbC123xyz/subdir:
nested.txt
```

---

## 步驟 3：先預覽（不加 `--apply`）

先存一份「執行前」的檔案清單，等一下用來比對：

```bash
ls -R "$demo" > before.txt
python organize_downloads.py "$demo"
```

**你應該看到**：

```text
README -> no_extension/README
notes.txt -> documents/notes.txt
photo.JPG -> images/photo.JPG
report.txt -> documents/report.txt
report_1.txt -> documents/report_1.txt
script.py -> code/script.py
table.csv -> data/table.csv
共 7 個檔案（預覽模式，沒有移動任何檔案）
加 --apply 才會實際移動
```

注意：

- `photo.JPG` 進 `images/`，因為副檔名先轉小寫變成 `.jpg`。
- `README` 沒有副檔名，進 `no_extension/`，不是 `others/`。
- `subdir/nested.txt` **沒有出現**，因為程式只看第一層。

---

## 步驟 4：確認預覽沒有改任何檔案

```bash
ls -R "$demo" > after_preview.txt
diff before.txt after_preview.txt && echo "預覽沒有改檔"
```

**你應該看到**：

```text
預覽沒有改檔
```

（`diff` 沒印出任何差異，代表前後一模一樣。）

---

## 步驟 5：加 `--apply` 實際移動

```bash
python organize_downloads.py "$demo" --apply
```

**你應該看到**：同樣 7 行「來源 -> 目的」，最後一行變成：

```text
已移動 7 個檔案
```

---

## 步驟 6：檢查結果

```bash
(cd "$demo" && ls -R)
```

**你應該看到**：

```text
.:
code  data  documents  images  no_extension  subdir

./code:
script.py

./data:
table.csv

./documents:
notes.txt  report.txt  report_1.txt

./images:
photo.JPG

./no_extension:
README

./subdir:
nested.txt
```

- 根目錄不再有那 7 個檔案，都進了分類資料夾。
- `subdir/nested.txt` 原封不動。

再執行一次預覽看看：

```bash
python organize_downloads.py "$demo"
```

**你應該看到**：`沒有要整理的檔案`（第一層已經沒有檔案了）。

### 步驟 6-加碼：同名不覆寫、同批次碰撞

`documents/` 裡已經有 `report.txt` 和 `report_1.txt`。再放兩個同名檔進第一層試試：

```bash
touch "$demo/report.txt" "$demo/report_1.txt"
python organize_downloads.py "$demo"
```

**你應該看到**：

```text
report.txt -> documents/report_2.txt
report_1.txt -> documents/report_1_1.txt
共 2 個檔案（預覽模式，沒有移動任何檔案）
加 --apply 才會實際移動
```

- `report.txt`：`report.txt`、`report_1.txt` 都已存在，所以用 `report_2.txt`。
- `report_1.txt`：原檔名的 stem 是 `report_1`，加流水號變 `report_1_1.txt`。
- 已存在的檔案**不會被覆寫**。想實際移動就加 `--apply`。

---

## 步驟 7：跑單元測試

```bash
python -m unittest discover -s . -p 'test_*.py' -v
```

**你應該看到**：每一項後面是 `... ok`，最後是：

```text
----------------------------------------------------------------------
Ran 9 tests in 0.0xxs

OK
```

（測試自己會用 `tempfile` 建臨時資料夾，跑完自動刪除，不會動到你的檔案。）

---

## 步驟 8：刪掉臨時資料夾與比對檔

```bash
rm -rf "$demo" before.txt after_preview.txt
ls "$demo"
```

**你應該看到**：`ls: cannot access '...': No such file or directory`，代表已刪乾淨。

---

## 常見錯誤

| 你看到 | 原因 | 怎麼辦 |
| --- | --- | --- |
| `錯誤：來源資料夾不存在：\tmp\tmp...` | Python 看不懂 `/tmp/...` 路徑 | 步驟 1 用 `demo=$(cygpath -m "$(mktemp -d)")` |
| `錯誤：來源不是資料夾：...` | 傳進去的是檔案不是資料夾 | 改傳資料夾路徑 |
| 中文變亂碼 | 終端機編碼是 cp950 | 先執行 `export PYTHONUTF8=1` |
| `python: command not found` | 沒裝 Python 或沒加進 PATH | 安裝 Python 3.10+，重開 Git Bash |
