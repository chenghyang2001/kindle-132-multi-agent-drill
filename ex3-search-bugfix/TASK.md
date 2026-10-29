# 實例三：搜尋錯誤修復（第五章）— 主 Agent 任務

先讀 `../drill/ORCHESTRATION.md`，session 名稱 `ex3`，資料夾 `ex3-search-bugfix`。

## 開始前（主 Agent 自己做）

依 `BOOK_CODE.md` 建立 `search_faulty.js`（故障版）、`search.js`（起始內容與故障版相同）、`test_search.js`（書中版本），然後 `git add` + commit「建立故障前版本」。跑一次 `node test_search.js ./search_faulty.js` 確認退出碼 1（重現問題），記進 timeline。

## 書中總提示詞（3.1，逐字）

```
請用修復與獨立審查兩個子 Agent，處理搜尋框輸入空白時出錯的問題。

主 Agent：
- 先閱讀目標專案規範，確認啟動方式、重現步驟及預期行為。
- 缺少專案或重現資料時先回報缺口，不虛構已修復成果。
- 將修改限制在搜尋相關範圍，負責整合與最後驗收。

修復 Agent：
- 先重現問題，建立能捕捉原始錯誤的回歸測試，再做最小修改。
- 執行相關測試，回報修改檔案、原因、命令與結果。

審查 Agent：
- 修復完成後只讀檢查差異與相關程式。
- 檢查空字串、只有空白、正常關鍵字及查無結果等情境。
- 每個問題附檔案位置、觸發條件與影響。
- 區分必須修復的問題與可選建議。

有必要問題時交回修復 Agent，修改後重新驗證。
完成條件：原始錯誤已修復、正常搜尋仍可使用、相關測試通過，
且必要審查問題均已處理。無法執行的檢查須明確回報。
```

## 子 Agent（兩格左右，串行）

| 格 | 角色 | 輸入 | 輸出 | 完成檔 |
| --- | --- | --- | --- | --- |
| ① | 修復 | 故障行為說明、`search_faulty.js`、`test_search.js` | 最小修改後的 `search.js`、必要時擴充 `test_search.js`（例如加 `undefined`）、`out/fix-report.md`（修改檔案、原因、命令與結果） | `out/修復.done` |
| ② | 審查 | `git diff`、`search.js`、`test_search.js` | `out/review.md`（逐項檢查空字串／只有空白／正常關鍵字／查無結果／null；每個問題附檔案位置、觸發條件、影響；分「必須修復」與「可選建議」）；**只讀，不改任何程式檔** | `out/審查.done` |

- 修復完成（`修復.done` 出現）才派審查。審查有「必須修復」→ 寫 fix prompt 退回修復 Agent，改完再請審查 Agent 重看。
- 只修空白與空字串，不做功能增強；不可宣稱網站或 UI 已修復（只做模組級驗證）。

## 主 Agent 最後驗收（分開執行，不要放進 set -e）

```
node test_search.js ./search_faulty.js   # 預期退出碼 1，訊息含 whitespace query failed
node test_search.js ./search.js          # 預期退出碼 0
node test_search.js                      # 預期退出碼 0
```

把三條命令的實際輸出與退出碼寫進 `out/REPORT.md`，並 commit「修復搜尋空白輸入」。
