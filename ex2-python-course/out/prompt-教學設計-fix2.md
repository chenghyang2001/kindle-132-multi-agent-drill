# 教學設計 Agent：修正單（第 2 輪，依試學報告 out/obstacles.md）

只改 `curriculum.md`（程式 Agent 同時在改程式與 steps.md，不要碰它們）。練習仍必須恰好三題。

1. **O-1（高）**：§3 安全原則加一條：執行程式前先確認 `[ -n "$TMP" ]`；關掉終端機後 TMP 會不見，必須重建；永遠不要在課程資料夾裡對空的 `$TMP` 執行 `--apply`。程式現在遇到空字串會 exit 2。
2. **O-2（中）**：第 1 堂說明如何進出互動模式（輸入 `python` 看到 `>>>`；Git Bash 沒反應改用 `winpty python`；`exit()` 離開），並提供替代做法：存成 `lesson1.py` 再 `python lesson1.py`。
3. **O-3（中）**：第 2～5 堂每個小活動指定練習檔名（`lesson2.py`…`lesson5.py`），給起手式（例如第 3 堂 `import sys` / `from pathlib import Path` / `folder = Path(sys.argv[1])`），執行方式 `python lesson3.py "$TMP"`；說明 `sys.argv[1]` 就是命令列第一個參數。
4. **O-4（低）**：練習二預期解的驗證方法改成 `ls -R "$TMP" > "$TMP-before.txt"`／`"$TMP-after.txt"`（與 steps.md 一致），清理時一併 `rm -f "$TMP-before.txt" "$TMP-after.txt"`。

完成後建立空檔 `out/教學設計-fix2.done`。
