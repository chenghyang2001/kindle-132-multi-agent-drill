# 第五章書中程式碼（逐字抄錄，供主 Agent 建立 search_faulty.js 與 test_search.js）

## search_faulty.js（故障版）

```js
"use strict";
/**
 * 搜尋資料（故障版本）：當查詢為空字串或只有空白時會拋出例外，
 * 導致整個搜尋功能中斷。這是一個需要修復的常見錯誤。
 */
function searchItems(query, items) {
  const keyword = typeof query === "string" ? query.trim().toLowerCase() : query;
  if (keyword === "") throw new Error("搜尋關鍵字不可為空");
  return items.filter((item) =>
    String(item.title).toLowerCase().includes(keyword),
  );
}
if (typeof module !== "undefined") {
  module.exports = { searchItems };
}
```

## 起始狀態

演練開始時 `search.js` 與 `search_faulty.js` 內容相同（都是故障版），由修復 Agent 修正 `search.js`。

## test_search.js（書中版本，修復 Agent 可擴充）

```js
"use strict";
const assert = require("node:assert/strict");
// 預設驗證修復版；也可用命令列參數選擇故障版，執行相同回歸檢查。
const modulePath = process.argv[2] || "./search.js";
const { searchItems } = require(modulePath);
const items = [
  { title: "Python 入門" },
  { title: "台南旅行" },
];
// 同一個空白輸入回歸檢查：故障版應失敗，修復版應通過。
assert.doesNotThrow(
  () => assert.deepEqual(searchItems("   ", items), []),
  "whitespace query failed: expected [] without throwing",
);
assert.deepEqual(searchItems("python", items), [{ title: "Python 入門" }]);
assert.deepEqual(searchItems("   ", items), []);
assert.deepEqual(searchItems("", items), []);
assert.deepEqual(searchItems("不存在", items), []);
assert.deepEqual(searchItems(null, items), []);
console.log("5 個搜尋情境全部通過");
```

## 驗收命令（在 ex3-search-bugfix/ 執行，不要放進 set -e）

```
node test_search.js ./search_faulty.js   # 預期退出碼 1，訊息含 whitespace query failed
node test_search.js ./search.js          # 預期退出碼 0，「5 個搜尋情境全部通過」
node test_search.js                      # 同上
```
