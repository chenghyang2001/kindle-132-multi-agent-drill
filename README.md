# K132《用三個實例學會多 Agent 應用》實機演練

2026-10-30 在 hp1（Windows 11）實機演練書中三個實例。每個 Agent 都是獨立的 Claude Code，各佔一個終端格子（MSYS2 tmux＋Windows Terminal，工具 `wpanes`）。

| 實例 | 主 Agent | 子 Agent | 方式 | 資料夾 |
| --- | --- | --- | --- | --- |
| 一 台南兩天一夜 | 代理一 | 景點、交通、預算 | 平行 → 整合 | `ex1-travel/` |
| 二 Python 教材 | 代理二 | 教學設計 → 程式 → 試學 | 接力 | `ex2-python-course/` |
| 三 搜尋錯誤修復 | 代理三 | 修復 → 審查 | 串行＋退回 | `ex3-search-bugfix/` |

- 交接一律用檔案（書第一章原則）：子 Agent 寫 `out/<角色>.md`，完成時寫 `out/<角色>.done`。
- 只用 `main` 分支（書第二章規則），本機 commit。
- 書附配件 `multi-agent-reader-resources-1.0.0.zip` 找不到下載點，依書中內容重建；`ex1-travel/plan-template.md` 的「七項結構」書中未列出，是演練時補的。
- 快速 demo 模式：子 Agent 啟動時設 `DISABLE_WRITER_QA_HOOK=1`，未經 QA／審查。
- 錄影、TTS、上傳紀錄在 `drill/`。

## 成果（2026-10-30）

| 版本 | 連結（YouTube 私人） |
| --- | --- |
| 精華版（約 3 分鐘） | https://youtu.be/Hz5IcLZ8QC0 |
| 語音版（約 5 分鐘） | https://youtu.be/TavwdgrFM-I |
| 完整版（約 35 分鐘） | https://youtu.be/sj59ooLLbOM |
| 播放清單 | https://www.youtube.com/playlist?list=PLXkvXKQreK4A |

- 各實例報告：`ex1-travel/out/REPORT.md`、`ex2-python-course/out/REPORT.md`、`ex3-search-bugfix/out/REPORT.md`
- 錄影原檔在本機 `~/Videos/k132-drill/`（hp1，不進 git）；旁白稿在 `drill/tts/`
