# Python 入門課：依副檔名整理下載資料夾

> 實例二・第 ① 棒（教學設計 Agent）產出。
> 下一棒：程式 Agent 依「程式規格」一節製作 `organize_downloads.py`、`test_organize_downloads.py`、`steps.md`；
> 再下一棒：試學 Agent 照本教材從頭操作。

---

## 1. 目標讀者與學習目標

### 目標讀者

- 剛開始學 Python 的初學者：看過 `print("hello")`，但還沒寫過「會處理真實檔案」的小工具。
- 下載資料夾常常亂成一團，想用程式自動分類的人。

### 學習目標（上完課後，學員能做到）

1. **能說出**一個檔名的副檔名，並用 `Path("photo.JPG").suffix.lower()` 印出 `.jpg`。
2. **能寫出**一段 `if / elif / else`，依副檔名回傳分類資料夾名稱（例如 `images`、`no_extension`）。
3. **能用** `for` 迴圈逐一列出某資料夾**第一層**的檔案，並略過子資料夾。
4. **能把**重複的邏輯包成函式（`def`），並說明函式的輸入與回傳值。
5. **能先用預覽模式確認**「來源 -> 目的」清單，確認沒問題後才加 `--apply` 實際移動。
6. **能解釋**同名檔案為什麼會變成 `report_1.txt`、`report_1_1.txt`，以及為什麼練習只能用臨時假資料。

---

## 2. 先備知識

| 項目 | 要求 | 自我檢查方式 |
| --- | --- | --- |
| 終端機 | 會開 Git Bash，會用 `cd`、`ls` | 能進到課程資料夾並列出檔案 |
| 執行 Python | 會執行 `python 檔名.py` | `python --version` 顯示 3.10 以上 |
| Python 版本 | Python 3.10+ | 同上 |
| 編輯器 | 任一文字編輯器（VS Code、記事本皆可） | 能存檔成 UTF-8 |

> 環境提醒：本課以 **Windows + Git Bash** 為準，指令一律用 `python`（不是 `python3`）。
> 若輸出中文出現亂碼，在指令前加 `PYTHONUTF8=1`，例如 `PYTHONUTF8=1 python organize_downloads.py "$TMP"`。

---

## 3. 安全原則（每一堂都適用）

1. **絕對不要對真實的下載資料夾（`~/Downloads`）執行本課程式。** 所有示範、練習、測試都只用 `TMP=$(cygpath -m "$(mktemp -d)")` 或 Python `tempfile` 建立的臨時資料夾。
2. **先預覽，再 `--apply`。** 預覽只印清單、不改任何檔案；看過清單沒問題才加 `--apply`。
3. **不覆寫。** 目的地已有同名檔案時，程式一律改名（加 `_1`、`_2`…），不會蓋掉舊檔。
4. 練習結束後刪掉臨時資料夾（`rm -rf "$TMP"`，**只刪你自己用 `TMP=$(cygpath -m "$(mktemp -d)")` 建的那個**）。

建立臨時練習資料夾的標準做法（每堂課都會用到）：

> Windows + Git Bash 要用 `cygpath -m` 把 `mktemp -d` 回傳的 `/tmp/tmp.xxx` 轉成 Python 看得懂的路徑（例如 `C:/Users/.../Temp/tmp.xxx`），否則 Python 會回報找不到資料夾；macOS/Linux 直接 `TMP=$(mktemp -d)` 即可。

```bash
TMP=$(cygpath -m "$(mktemp -d)")   # 建立空的臨時資料夾，轉成 Python 看得懂的路徑後存進變數 TMP
echo "$TMP"             # 看一下路徑，確認不是 ~/Downloads
touch "$TMP/photo.JPG" "$TMP/notes.txt" "$TMP/table.csv" "$TMP/script.py" "$TMP/README"
ls "$TMP"
```

---

## 4. 課綱（6 堂，合計約 200 分鐘）

| 堂次 | 主題 | 建議分鐘 |
| --- | --- | --- |
| 第 1 堂 | 變數：檔名與副檔名 | 30 |
| 第 2 堂 | 判斷（if）：決定分類資料夾 | 30 |
| 第 3 堂 | 迴圈（for）：走過資料夾第一層 | 35 |
| 第 4 堂 | 函式（def）：把邏輯包起來 | 35 |
| 第 5 堂 | 副檔名分類：組成完整的分類規則 | 30 |
| 第 6 堂 | 預覽 vs `--apply`、同名碰撞與安全原則 | 40 |

### 第 1 堂：變數——檔名與副檔名（30 分鐘）

- **學習重點**
  - 變數是「貼了名字的盒子」，可以裝字串、路徑。
  - 用 `pathlib.Path` 把字串變成路徑物件，取出檔名（`.name`）、主檔名（`.stem`）、副檔名（`.suffix`）。
  - 副檔名大小寫不一定一致（`.JPG`、`.jpg`），要用 `.lower()` 統一。
- **程式概念**：變數指派、字串、`from pathlib import Path`、`.name` / `.stem` / `.suffix`、`.lower()`、`print()`。
- **小活動**
  1. 在 Python 互動模式輸入：

     ```python
     from pathlib import Path
     file_path = Path("photo.JPG")
     print(file_path.name, file_path.stem, file_path.suffix, file_path.suffix.lower())
     ```

     預期看到：`photo.JPG photo .JPG .jpg`
  2. 換成 `Path("README")`，觀察 `.suffix` 是空字串 `''`（這就是「無副檔名」）。
  3. 換成 `Path(".gitignore")`，觀察 `.suffix` 也是 `''`（以點開頭的隱藏檔，Python 視為沒有副檔名）。

### 第 2 堂：判斷（if）——決定分類資料夾（30 分鐘）

- **學習重點**
  - `if / elif / else` 依條件走不同路線。
  - `in` 可以檢查「某值是否在一組值裡」：`ext in {".jpg", ".png"}`。
  - 「空字串」要優先判斷，才能分到 `no_extension`。
- **程式概念**：比較運算、`in`、集合 `{...}`、`if / elif / else`、空字串判斷 `ext == ""`。
- **小活動**
  1. 寫一段程式：給定 `ext = ".png"`，用 `if` 印出 `images`；再改成 `.csv` 印出 `data`；改成 `""` 印出 `no_extension`；改成 `.zip` 印出 `others`。
  2. 討論：如果忘了 `.lower()`，`.JPG` 會被分到哪裡？（答：`others`，這就是 bug）

### 第 3 堂：迴圈（for）——走過資料夾第一層（35 分鐘）

- **學習重點**
  - `for` 迴圈一次處理一個項目。
  - `Path(資料夾).iterdir()` 只列出**第一層**，不會往子資料夾裡鑽。
  - 用 `is_file()` 只留下檔案，子資料夾（例如 `subdir/`）跳過不處理。
  - 用 `sorted()` 讓順序固定，每次執行結果一樣。
- **程式概念**：`for ... in ...`、`iterdir()`、`is_file()`、`continue`、`sorted()`。
- **小活動**
  1. 在臨時資料夾多建一個子資料夾：`mkdir "$TMP/subdir" && touch "$TMP/subdir/nested.txt"`。
  2. 寫迴圈印出 `$TMP` 第一層的檔案名稱，確認 `nested.txt` **沒有**出現、`subdir` 也沒有被當成檔案印出。

### 第 4 堂：函式（def）——把邏輯包起來（35 分鐘）

- **學習重點**
  - 函式 = 有名字、可重複呼叫的一段程式；有輸入（參數）、有輸出（`return`）。
  - 一個函式只做一件事，名字要說清楚它做什麼。
  - 拿第 2 堂的 `if` 改寫成 `category_for(path)`，給檔案回傳分類資料夾名稱。
- **程式概念**：`def`、參數、`return`、docstring（`"""說明"""`）、呼叫函式。
- **小活動**
  1. 寫 `def category_for(path):`，用第 2 堂的判斷回傳分類名稱。
  2. 用迴圈對 `["photo.JPG", "notes.txt", "README"]` 逐一呼叫，印出「檔名 -> 分類」。
  3. 討論：為什麼把邏輯包成函式後比較好測試？（答：可以單獨給輸入、檢查輸出，不用真的搬檔案）

### 第 5 堂：副檔名分類——組成完整的分類規則（30 分鐘）

- **學習重點**
  - 用「對照表」（字典）取代一長串 `if`，新增分類只要加一行。
  - 完整分類規則見「程式規格」一節的對照表。
  - 規劃「來源 -> 目的」：目的路徑 = 來源資料夾 / 分類資料夾 / 檔名。
- **程式概念**：字典 `dict`、`for` 走訪字典、路徑相加 `source / "images" / name`。
- **小活動**
  1. 把分類規則寫成字典 `{"images": {".jpg", ".jpeg", ".png", ".gif"}, ...}`，改寫 `category_for`。
  2. 對臨時資料夾每個檔案印出 `photo.JPG -> images/photo.JPG` 這樣的清單（只印、不搬）。
  3. 先預測再核對：`table.XLSX`、`archive.tar.gz`、`.gitignore` 各會分到哪？（答：`data/`、`others/`（只看最後的 `.gz`）、`no_extension/`）

### 第 6 堂：預覽 vs `--apply`、同名碰撞與安全原則（40 分鐘）

- **學習重點**
  - **預覽模式（預設）**：只印「來源 -> 目的」，不建資料夾、不搬檔案。
  - **`--apply`**：真的建立分類資料夾並移動檔案（`shutil.move`）。
  - 用 `argparse` 讀取命令列參數：位置參數 `source`、旗標 `--apply`。
  - **同名不覆寫**：目的地已有 `report.txt` → 改成 `report_1.txt`，再撞就 `report_2.txt`。
  - **同批次碰撞**：同一次執行中，已經規劃過的目的路徑記在 `reserved` 集合，後面的檔案不能再用同一個路徑。
  - **只掃第一層**的限制：子資料夾裡的檔案不會被整理。
  - 回顧安全原則：只用臨時假資料、先預覽、絕不碰 `~/Downloads`。
- **程式概念**：`argparse`、`shutil.move`、`Path.mkdir(parents=True, exist_ok=True)`、`while` 迴圈找可用檔名、`set` 與 `in`。
- **小活動**
  1. 建立假資料（含 `documents/report.txt` 先放在目的地）後先跑預覽，用 `ls -R` 比對前後完全一樣。
  2. 加 `--apply` 再跑，`ls -R` 檢查結果：檔案數量不變、`subdir/nested.txt` 仍在原地。
  3. 找出 `report_1_1.txt` 是怎麼產生的（對應練習三）。

---

## 5. 程式規格（給程式 Agent）

> 程式 Agent 請**完全照這一節**實作；有疑問寫在 `out/程式-notes.md`，不要自行改規格。

### 5.1 基本要求

| 項目 | 規格 |
| --- | --- |
| 程式檔名 | `organize_downloads.py`（放在 ex2-python-course/ 根目錄） |
| 測試檔名 | `test_organize_downloads.py`（`unittest`） |
| 操作步驟 | `steps.md`（給初學者，繁中，每步附指令與「你應該看到」） |
| 函式庫 | **只用標準函式庫**：`pathlib`、`argparse`、`shutil`、`tempfile`、`unittest`（`sys` 用於 stderr / exit code 亦可） |
| Python 版本 | 3.10+ |
| 用法 | `python organize_downloads.py <來源資料夾> [--apply]` |
| 語言 | docstring 與註解一律繁體中文；輸出訊息繁體中文 |
| 環境 | Windows + Git Bash；指令用 `python`；必要時加 `PYTHONUTF8=1` |

### 5.2 分類對照表

副檔名先 `.lower()` 再比對（以 `Path.suffix` 為準，只看最後一個點之後的部分）：

| 副檔名（轉小寫後） | 目的資料夾 |
| --- | --- |
| `.jpg` `.jpeg` `.png` `.gif` | `images/` |
| `.txt` `.md` `.pdf` `.docx` | `documents/` |
| `.csv` `.xlsx` | `data/` |
| `.py` `.js` `.sh` | `code/` |
| 其他任何副檔名（例如 `.zip`、`.gz`） | `others/` |
| **無副檔名**（`suffix == ""`，例如 `README`、`.gitignore`） | `no_extension/` |

- 分類資料夾建立在**來源資料夾底下**：例如 `<來源>/images/photo.JPG`。
- 移動後**保留原檔名大小寫**（`photo.JPG` 仍叫 `photo.JPG`，不改成小寫）。

### 5.3 掃描範圍

- 只掃來源資料夾**第一層**：`sorted(source.iterdir())`，只取 `is_file()` 為真的項目。
- 子資料夾（例如 `subdir/`）整個略過，裡面的檔案（`subdir/nested.txt`）**不移動**。
- 分類資料夾本身（`images/`、`documents/`…）是資料夾，同樣略過，不會被再整理。
- 處理順序用 `sorted()` 依名稱排序，確保碰撞結果可預測（`report.txt` 排在 `report_1.txt` 前面）。

### 5.4 預覽與 `--apply`

- **預設（沒加 `--apply`）= 預覽**：
  - 每筆印一行：`<來源檔名> -> <分類資料夾>/<目的檔名>`，例如 `photo.JPG -> images/photo.JPG`。
  - **不建立任何資料夾、不移動任何檔案**。
  - 最後一行提示：`這是預覽，加 --apply 才會實際移動。`
- **加 `--apply`**：
  - 依規劃逐筆 `shutil.move`；移動前才用 `mkdir(parents=True, exist_ok=True)` 建立目的子資料夾。
  - 每筆印一行（格式同上，可加「已移動：」前綴），最後印總數，例如 `完成：已移動 7 個檔案。`（以標準範例第一層 7 個檔案為例：photo.JPG、notes.txt、table.csv、script.py、README、report.txt、report_1.txt；實際數字依檔案數而定）
- 來源資料夾沒有任何第一層檔案時：印 `沒有要整理的檔案`，正常結束（exit code 0）。

### 5.5 同名不覆寫與同批次碰撞

- 規劃每個檔案的目的路徑時，若該路徑**已存在於磁碟**，或**已在本次的 `reserved` 集合中**，就視為「被佔用」。
- 被佔用時依序嘗試 `<stem>_1<suffix>`、`<stem>_2<suffix>`…，直到找到沒被佔用的路徑。
  - `<stem>` 是**該來源檔自己的主檔名**（例如 `report_1.txt` 的 stem 是 `report_1`，所以候選是 `report_1_1.txt`）。
  - 無副檔名時 suffix 為空：`README` → `README_1`。
- 找到後把該路徑加入 `reserved`，後續檔案不得再規劃到同一路徑。
- **絕不覆寫任何既有檔案**；整理前後檔案總數必須相同。
- 標準範例（試學與測試都要驗證）：
  - 目的地已有 `documents/report.txt`；來源第一層有 `report.txt`、`report_1.txt`。
  - `report.txt` → `documents/report.txt` 已存在 → 規劃成 `documents/report_1.txt`（加入 reserved）。
  - `report_1.txt` → `documents/report_1.txt` 已在 reserved → 規劃成 `documents/report_1_1.txt`。

### 5.6 錯誤處理

| 情況 | 行為 |
| --- | --- |
| 來源路徑不存在 | 錯誤訊息印到 stderr（例如 `錯誤：找不到資料夾 <路徑>`），exit code **2** |
| 來源路徑是檔案不是資料夾 | 錯誤訊息印到 stderr（例如 `錯誤：<路徑> 不是資料夾`），exit code **2** |
| 來源資料夾為空（或只有子資料夾） | 印 `沒有要整理的檔案`，exit code 0 |
| 移動時發生 `OSError`（權限等） | 印出是哪個檔案失敗與原因到 stderr，不可吞掉錯誤；exit code 非 0 |

### 5.7 建議函式拆分

| 函式 | 輸入 | 回傳 / 作用 |
| --- | --- | --- |
| `category_for(path)` | 檔案路徑 | 分類資料夾名稱字串（`"images"`、`"no_extension"`…） |
| `unique_target(path, reserved)` | 預定目的路徑、已保留集合 | 不被佔用的目的路徑（考慮磁碟既有檔與 reserved） |
| `plan_moves(source)` | 來源資料夾 | `[(來源路徑, 目的路徑), ...]` 清單，不動任何檔案 |
| `apply_moves(plan)` | 規劃清單 | 建立資料夾並移動檔案 |
| `main()` | 命令列參數 | 解析 `argparse`、呼叫上述函式、印輸出、決定 exit code |

### 5.8 測試要求（`test_organize_downloads.py`）

- 一律在 `tempfile.TemporaryDirectory()` 內建立假資料；**絕對不可操作 `~/Downloads` 或任何真實資料夾**。
- 至少 7 項：
  1. 空資料夾 → 規劃清單為空。
  2. 無副檔名（`README`）→ `no_extension/`。
  3. 一般分類（含 `photo.JPG` 大小寫）→ `images/`、`documents/`、`data/`、`code/`、`others/`。
  4. 預覽不改檔：執行前後的檔案清單完全相同。
  5. 既有檔名碰撞：目的地已有 `documents/report.txt` → 規劃成 `report_1.txt`。
  6. 同批次碰撞：`report.txt` → `report_1.txt`、`report_1.txt` → `report_1_1.txt`。
  7. 子資料夾不移動：`--apply` 後 `subdir/nested.txt` 仍在原地。
- 執行方式：`python -m unittest discover -s . -p 'test_*.py' -v`，全部通過。

---

## 6. 練習（共三題）

> 作答方式：先在紙上寫下你的**預測**，再用臨時資料夾實際跑程式核對。

### 練習一：預測分類結果

**題目**：臨時資料夾裡有以下 5 個檔案，執行預覽後，它們各會被分到哪個資料夾？
`photo.JPG`、`notes.txt`、`table.csv`、`script.py`、`README`

**預期解**：

| 檔案 | 分類 | 理由 |
| --- | --- | --- |
| `photo.JPG` | `images/` | 副檔名 `.JPG` 先轉小寫成 `.jpg`，屬於圖片 |
| `notes.txt` | `documents/` | `.txt` 屬於文件 |
| `table.csv` | `data/` | `.csv` 屬於資料 |
| `script.py` | `code/` | `.py` 屬於程式碼 |
| `README` | `no_extension/` | 沒有副檔名（`suffix` 是空字串） |

重點：程式比對前一律 `.lower()`，所以 `.JPG`、`.Jpg`、`.jpg` 都進 `images/`；但移動後檔名本身仍保留 `photo.JPG`。

### 練習二：比較預覽與 `--apply`

**題目**：用 `TMP=$(cygpath -m "$(mktemp -d)")` 建立臨時假資料（Windows + Git Bash 要用 cygpath -m 轉成 Python 看得懂的路徑；macOS/Linux 直接 `TMP=$(mktemp -d)` 即可；**不可用 `~/Downloads`**），先執行預覽、再執行 `--apply`。說明兩者差異，並寫出你如何**驗證**預覽真的沒有改到任何檔案。

**預期解**：

- **預覽**（不加 `--apply`）：只印出「來源 -> 目的」清單與「加 --apply 才會實際移動」提示，**不建資料夾、不移動檔案**。
- **`--apply`**：建立分類資料夾，真的把檔案搬過去。
- 驗證方法：
  1. 預覽前存下清單：`ls -R "$TMP" > before.txt`（存在 `$TMP` 外面）。
  2. 執行預覽：`python organize_downloads.py "$TMP"`。
  3. 預覽後再存：`ls -R "$TMP" > after.txt`，`diff before.txt after.txt` 應該**沒有任何輸出**（代表沒改檔）。
  4. 執行 `python organize_downloads.py "$TMP" --apply`，再 `ls -R "$TMP"`：出現 `images/` 等資料夾，檔案已移入。
  5. 數檔案總數：`find "$TMP" -type f | wc -l` 在 apply 前後相同（沒有遺失或覆寫）。
- 安全原則：一定先預覽、確認清單正確才 `--apply`；只用臨時假資料。

### 練習三：同批次碰撞與「只掃第一層」

**題目**：臨時資料夾裡已先有 `documents/report.txt`，來源第一層另有 `report.txt`、`report_1.txt`，以及子資料夾裡的 `subdir/nested.txt`。執行後：
(a) 兩個 report 檔各會變成什麼名字？為什麼？
(b) `subdir/nested.txt` 會怎樣？這代表程式有什麼限制？

**預期解**：

- (a)
  - `report.txt` → 目的 `documents/report.txt` 已存在 → 改成 `documents/report_1.txt`，並記入 reserved。
  - `report_1.txt` → 目的 `documents/report_1.txt` 雖然磁碟上還不存在，但已被同批次的 `report.txt` 預訂（在 reserved 裡）→ 改成 `documents/report_1_1.txt`。
  - 結果：`documents/` 裡有 `report.txt`（原本的）、`report_1.txt`、`report_1_1.txt`，三個檔都在，沒有覆寫。
- (b)
  - `subdir/nested.txt` **不會被移動**，仍留在 `subdir/` 裡。
  - 限制：程式只掃來源資料夾**第一層**，子資料夾（以及已存在的分類資料夾）一律略過；子資料夾裡的檔案需要另外處理（例如之後學遞迴時再擴充）。

---

## 7. 交付物對照（給後續 Agent）

| 交付物 | 負責 | 位置 |
| --- | --- | --- |
| `curriculum.md`（本檔） | 教學設計 Agent | ex2-python-course/ |
| `organize_downloads.py` | 程式 Agent | ex2-python-course/ |
| `test_organize_downloads.py` | 程式 Agent | ex2-python-course/ |
| `steps.md` | 程式 Agent | ex2-python-course/ |
| `out/trial-log.md`、`out/obstacles.md` | 試學 Agent | ex2-python-course/out/ |
