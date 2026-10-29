# 實例三 獨立審查報告（Review Agent）

- 日期：2026-10-30
- 方式：唯讀審查。沒有改任何 `.js` 檔，只寫了本檔與 `out/審查.done`。
- 比較基準：`git diff HEAD`（commit `fdb54a0`「建立故障前版本」）＋ `search_faulty.js`
- 結論：**修復正確，可以合併**。沒有必須修正的問題，只有 3 項選用建議。

## 檢查清單

| # | 情境 | 輸入 | 修復版 `search.js` 實際結果 | 故障版 `search_faulty.js` 實際結果 | 判定 |
| --- | --- | --- | --- | --- | --- |
| 1 | 空字串 | `""` | `[]` | 拋出 `Error: 搜尋關鍵字不可為空` | ✅ 通過 |
| 2a | 只有空白 | `"   "` | `[]` | 拋出例外 | ✅ 通過 |
| 2b | 含 tab／換行的空白 | `" \t\n "` | `[]` | 拋出例外 | ✅ 通過 |
| 3a | 一般關鍵字 | `"python"` | `[{"title":"Python 入門"}]` | 相同 | ✅ 通過 |
| 3b | 大寫關鍵字 | `"PYTHON"` | `[{"title":"Python 入門"}]` | 相同 | ✅ 通過 |
| 3c | 前後有空白的關鍵字 | `"  python  "` | `[{"title":"Python 入門"}]` | 相同 | ✅ 通過 |
| 4 | 找不到 | `"不存在"` | `[]` | 相同 | ✅ 通過 |
| 5a | null | `null` | `[]` | `[]`（只是剛好沒有標題含 `"null"`） | ✅ 通過 |
| 5b | undefined | `undefined` | `[]` | `[]`（同上，比對字串 `"undefined"`） | ✅ 通過 |
| 附 | 數字（非字串） | `123` | `[]` | `[]`（舊版會比對 `"123"`） | ✅ 通過（行為改變，見建議 3） |

### 範圍與改動大小

| 項目 | 結果 | 判定 |
| --- | --- | --- |
| 只改了搜尋相關檔案 | `git diff --stat HEAD -- .` 只有 `search.js`（2 行）和 `test_search.js`（+1／改 1 行） | ✅ |
| 改動最小 | `search.js` 只換第 7、8 行，沒有重構、沒有加功能 | ✅ |
| `search_faulty.js` 沒被動到 | `git diff --quiet HEAD -- search_faulty.js` 成功；SHA256 與 `out/_pre_review.sha` 相符 | ✅ |
| 測試確實能抓到原始 bug | 故障版 `node test_search.js ./search_faulty.js` → exit 1，訊息 `whitespace query failed`；修復版 → exit 0 | ✅ |
| 修復報告內容屬實 | `out/fix-report.md` 的 diff、測試結果、exit code 都和我重跑的結果一致 | ✅ |

## 必須修正

無。

## 選用建議

1. **檔頭註解還寫「故障版本」**
   - 位置：`search.js:2-4`
   - 觸發條件：任何人閱讀 `search.js`。
   - 影響：註解說「會拋出例外」，和現在的行為相反，容易讓人誤以為這是壞掉的檔案、或和 `search_faulty.js` 搞混。不影響執行。建議改成描述修復後的行為（空查詢回傳 `[]`）。

2. **測試沒有涵蓋大小寫、前後空白、tab／換行**
   - 位置：`test_search.js:15-20`
   - 觸發條件：以後有人改動 `trim()` 或 `toLowerCase()`。
   - 影響：現有 6 個情境不會抓到這類回歸。這次審查已手動確認這些情境都正確。可以加 `searchItems("PYTHON", items)`、`searchItems("  python  ", items)`、`searchItems(" \t\n ", items)` 三行斷言。

3. **非字串查詢（例如數字）的行為改變了**
   - 位置：`search.js:7`
   - 觸發條件：呼叫端傳入數字等非字串，例如 `searchItems(123, items)`。
   - 影響：舊版會用 `"123"` 去比對標題；新版一律回傳 `[]`。目前需求沒有要支援數字搜尋，修復報告第 4 節也寫明這個假設，所以不算錯。若以後要支援，可改成 `query == null ? "" : String(query).trim().toLowerCase()`。

（範圍外、沒有列為問題：`search.js:10` 的 `String(item.title)` 會把 `title: null` 變成 `"null"`，所以搜尋 `"null"` 會找到這筆。這是舊版就有的行為，不在本次修復範圍內。）

## 執行的指令與實際輸出

### 1. 比較改動

```
$ git diff HEAD -- search.js test_search.js
-  const keyword = typeof query === "string" ? query.trim().toLowerCase() : query;
-  if (keyword === "") throw new Error("搜尋關鍵字不可為空");
+  const keyword = typeof query === "string" ? query.trim().toLowerCase() : "";
+  if (keyword === "") return [];
...
 assert.deepEqual(searchItems(null, items), []);
-console.log("5 個搜尋情境全部通過");
+assert.deepEqual(searchItems(undefined, items), []);
+console.log("6 個搜尋情境全部通過");

$ git diff --stat HEAD -- .
 ex3-search-bugfix/search.js      | 4 ++--
 ex3-search-bugfix/test_search.js | 3 ++-
 2 files changed, 4 insertions(+), 3 deletions(-)

$ git diff --quiet HEAD -- search_faulty.js && echo "search_faulty.js unchanged"
search_faulty.js unchanged

$ sha256sum -c out/_pre_review.sha
search.js: OK
test_search.js: OK
search_faulty.js: OK
```

### 2. 用 `node -e` 逐一呼叫 `searchItems`（修復版與故障版）

```
== ./search.js
empty "" => []
spaces "   " => []
tab/nl " \t\n " => []
python "python" => [{"title":"Python 入門"}]
PYTHON "PYTHON" => [{"title":"Python 入門"}]
padded "  python  " => [{"title":"Python 入門"}]
nomatch "不存在" => []
null null => []
undefined undefined => []
number 123 => []
null-title-item "null" => [{"title":null}]
== ./search_faulty.js
empty "" => THROW Error: 搜尋關鍵字不可為空
spaces "   " => THROW Error: 搜尋關鍵字不可為空
tab/nl " \t\n " => THROW Error: 搜尋關鍵字不可為空
python "python" => [{"title":"Python 入門"}]
PYTHON "PYTHON" => [{"title":"Python 入門"}]
padded "  python  " => [{"title":"Python 入門"}]
nomatch "不存在" => []
null null => []
undefined undefined => []
number 123 => []
null-title-item "null" => [{"title":null}]
```

### 3. 回歸測試

```
$ node test_search.js
6 個搜尋情境全部通過
exit=0

$ node test_search.js ./search_faulty.js
AssertionError [ERR_ASSERTION]: Got unwanted exception: whitespace query failed: expected [] without throwing
Actual message: "搜尋關鍵字不可為空"
exit=1
```
