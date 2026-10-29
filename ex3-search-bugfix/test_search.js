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
