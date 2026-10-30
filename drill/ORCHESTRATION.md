# 主 Agent 指揮子 Agent 的固定做法（三個實例共用）

你是某個實例的**主 Agent**。每個子 Agent 是一個獨立的 Claude Code，跑在螢幕 2 的一個格子裡。你用 `wpanes`（已在 PATH，Git Bash 版）開格子、送任務、讀畫面；**交接一律靠檔案**。

以下 `<S>` 是你的 session 名稱（ex1／ex2／ex3），`<EX>` 是你的實例資料夾（例如 `ex1-travel`），都在 `~/workspace/kindle-132-multi-agent-drill/` 底下。

## 0. 時間軸紀錄（剪影片用，必做）

每個重要事件追加一行到 `<EX>/out/timeline.tsv`：

```bash
printf '%s\t%s\n' "$(date +%s)" "事件說明" >> <EX>/out/timeline.tsv
```

至少記：開子 Agent 視窗、每個子 Agent 收到任務、每個 .done 出現、退回修正、驗收結果、完成。

## 1. 開子 Agent 視窗

```bash
cd ~/workspace/kindle-132-multi-agent-drill
env -u TMUX -u TMUX_PANE wpanes open -Session <S> -Titles "角色1,角色2,角色3" -Monitor 2 -Cwd "$(cygpath -w "$PWD/<EX>")"
# 一定要 env -u TMUX：你自己在 tmux 格子裡，不清掉會變成 tmux 套 tmux
```

兩個子 Agent 時給兩個名稱（左右兩格）。

## 2. 每格啟動 Claude（快速 demo 模式）

```bash
printf '%s\n' 'export DISABLE_WRITER_QA_HOOK=1; claude --permission-mode bypassPermissions' > <EX>/out/_start.txt
for p in 1 2 3; do wpanes send $p -Stdin -Session <S> < <EX>/out/_start.txt; done
sleep 20
wpanes capture 1 -Session <S> -Lines 8     # 要看到 bypass permissions on
```

若畫面出現「Do you trust the files in this folder?」：游標預設在「No, exit」，要先 `wpanes keys N Up -Session <S>` 再 `wpanes keys N Enter -Session <S>`（直接 Enter 會退出 Claude）。

再為每格改名：`printf '%s\n' '/rename <S>-角色1' > <EX>/out/_rn1.txt; wpanes send 1 -Stdin -Session <S> < <EX>/out/_rn1.txt`

## 3. 派任務給子 Agent

1. 把該角色的完整任務寫成 `<EX>/out/prompt-<角色>.md`（可多行，寫清楚：共同條件、你的責任、不准做的事、輸出檔路徑、完成時要建立 `out/<角色>.done`）。
2. 送進格子的**只能是一行**（Claude 輸入框按 Enter 就送出，多行會被拆開）：

```bash
printf '%s\n' '請讀 out/prompt-角色1.md 並完整照做；完成後依檔案最後的指示建立 done 檔。' > <EX>/out/_go1.txt
wpanes send 1 -Stdin -Session <S> < <EX>/out/_go1.txt
```

## 4. 等待與監看

```bash
until [ -f <EX>/out/角色1.done ]; do sleep 15; done      # 外層請自己加逾時（例如 25 分鐘）
```

等待期間每 1～2 分鐘 `wpanes capture N -Session <S> -Lines 15` 看一下；子 Agent 若停下來問問題，用 `wpanes send` 回一行答案（依書中原則自行判斷，不要回頭問使用者）。

## 5. 驗收、整合、收尾

1. 讀子 Agent 的輸出檔，照實例 TASK.md 的驗收清單逐項檢查；有問題就寫 `prompt-<角色>-fix.md` 退回修正，再等新的 done 檔。
2. 整合成實例要求的最終產物。
3. 寫 `<EX>/out/REPORT.md`：用了幾個 Agent、每個做了什麼（輸入／輸出檔）、順序與交接、驗收逐項結果（附實際命令與輸出）、未解決的待確認事項。
4. 子 Agent 全部做完後 `wpanes close -Session <S>`，最後建立 `<EX>/out/ALL.done`。

## 規則

- **絕不可對 session `WIN` 送任何東西**（那是你自己所在的主控視窗）。所有 wpanes 指令都帶 `-Session <S>`。
- 不要呼叫 `wpanes.bat` / `win3.bat`。
- 不要問使用者問題，全程自主完成；做不到的事寫進 REPORT.md。
- 不要 git push；可以在 `<EX>/` 內 `git add` + `git commit`（只用 main 分支）。
