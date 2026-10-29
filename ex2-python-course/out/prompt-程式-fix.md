# 程式 Agent：修正單（第 1 輪，依試學報告 out/obstacles.md）

只改 `organize_downloads.py`、`test_organize_downloads.py`、`steps.md`（不改 curriculum.md，教學設計 Agent 同時在改它）。

1. **O-1（高）**：來源參數是空字串或只有空白時，印 `錯誤：沒有指定資料夾（$TMP 可能是空的，請回步驟 1 重新建立）` 到 stderr、exit 2，不可把 `Path("")` 當成 `.`。補一項測試（空字串來源 → exit 2，且目前資料夾檔案沒被動）。
2. **O-1 教材部分**：steps.md 步驟 3、5（以及其他用到 `"$TMP"` 執行程式的地方）前加一行 `[ -n "$TMP" ] || echo "TMP 是空的，請回步驟 1"`，並提醒「關掉終端機後 TMP 會不見，要重做步驟 1」。
3. **O-5（低）**：錯誤訊息中的路徑改用 `as_posix()`，跟預覽輸出斜線一致；steps.md 對應的預期輸出同步更新。
4. **O-6（低）**：steps.md 步驟 0 加註「可能還有 TASK.md、out、__pycache__ 等，不用理會」；步驟 2 加註「排列方式可能不同，名稱對得上就好」。

改完跑 `python -m unittest discover -s . -p 'test_*.py' -v`，全過才算完成；只用臨時資料夾，不碰 ~/Downloads。
完成後建立空檔 `out/程式-fix.done`。
