# 實例三 修復報告（Fix Agent）

- 日期：2026-10-30
- 環境：Node.js v24.19.0、Windows 11、Git Bash
- 範圍：只驗證模組層級（`searchItems` 函式），**沒有**宣稱網站或 UI 已修好。

## 1. 重現（修改前）

修改前 `search.js` 與 `search_faulty.js` 完全相同（`diff search.js search_faulty.js` → 無差異，輸出 `SAME`）。

| 指令 | exit code | 關鍵訊息 |
| --- | --- | --- |
| `node test_search.js ./search.js` | 1 | `AssertionError [ERR_ASSERTION]: Got unwanted exception: whitespace query failed: expected [] without throwing` / `Actual message: "搜尋關鍵字不可為空"`（search.js:8） |
| `node test_search.js ./search_faulty.js` | 1 | 同上（search_faulty.js:8） |

結論：回歸測試第一個 `assert.doesNotThrow`（空白查詢 `"   "`）確實能抓到原始錯誤，故障版會失敗。

## 2. 修改的檔案與原因

### `search.js`（2 行）

```diff
-  const keyword = typeof query === "string" ? query.trim().toLowerCase() : query;
-  if (keyword === "") throw new Error("搜尋關鍵字不可為空");
+  const keyword = typeof query === "string" ? query.trim().toLowerCase() : "";
+  if (keyword === "") return [];
```

- 第 8 行：空字串／只有空白時改成回傳 `[]`，不再丟例外。這是 bug 本身。
- 第 7 行：非字串查詢（`null`、`undefined`）原本會原樣傳給 `includes()`，被轉成字串 `"null"`／`"undefined"` 去比對。只是剛好沒有標題含這些字才回傳 `[]`。改成視為空字串，讓它們一律走「回傳 `[]`」。
- 一般關鍵字搜尋（trim + 不分大小寫 + `includes`）和查無結果的行為都沒改，也沒有重構或加功能。
- 沒改檔頭註解「故障版本」字樣，維持最小改動。主 Agent 可視需要調整。

### `test_search.js`（+1 行、改 1 行）

```diff
 assert.deepEqual(searchItems(null, items), []);
+assert.deepEqual(searchItems(undefined, items), []);
-console.log("5 個搜尋情境全部通過");
+console.log("6 個搜尋情境全部通過");
```

- 依任務第 2 步的許可，加入 `undefined` 案例。原本的邏輯和 `whitespace query failed` 訊息都保留，通過數字由 5 改成 6。
- 註：Edit 後 PostToolUse 格式化 hook 曾把 `items` 陣列壓成一行。我已用 node 腳本還原原本排版，最終 diff 只有上面這 2 行。

### 沒有動的檔案

`search_faulty.js`、`BOOK_CODE.md`、`TASK.md` 都沒改。

## 3. 修改後的測試

| 指令 | 實際輸出 | exit code | 預期 |
| --- | --- | --- | --- |
| `node test_search.js ./search.js` | `6 個搜尋情境全部通過` | 0 | 0 ✅ |
| `node test_search.js` | `6 個搜尋情境全部通過` | 0 | 0 ✅ |
| `node test_search.js ./search_faulty.js` | `AssertionError [ERR_ASSERTION]: Got unwanted exception: whitespace query failed: expected [] without throwing` / `Actual message: "搜尋關鍵字不可為空"` | 1 | 1，含 whitespace query failed ✅ |

其他輔助指令：

- `diff search_faulty.js search.js` → 只有第 7、8 行不同（exit 1，代表有差異）
- `git diff --stat -- test_search.js`（還原排版後）→ `1 file changed, 2 insertions(+), 1 deletion(-)`

## 4. 假設

1. 「null 查詢回傳 `[]`」也適用於 `undefined` 和其他非字串型別（如數字），一律視為空查詢。任務沒有要求支援數字搜尋，所以不另外處理。
2. `items` 是陣列、元素有 `title`，這和原本的行為一樣，不在本次修復範圍內。
3. 依指示沒有 git commit／push，由主 Agent 整合。
