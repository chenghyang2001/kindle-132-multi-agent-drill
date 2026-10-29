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
