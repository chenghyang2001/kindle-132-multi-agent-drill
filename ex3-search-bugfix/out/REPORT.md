# Example 3: Search bug fix — main Agent report

- Date: 2026-10-30; session `ex3`; environment Node.js v24.19.0 / Windows 11 / Git Bash
- Scope: **module-level verification only** (`searchItems`); not claiming the website or UI is fixed.

## Agents used (1 main + 2 sub, run sequentially)

| Agent | What it did | Input | Output |
| --- | --- | --- | --- |
| Main Agent | Built the three files from BOOK_CODE.md, reproduced the problem, committed "建立故障前版本" (fdb54a0); wrote the task prompts, dispatched, ran acceptance, integrated, committed | BOOK_CODE.md, TASK.md | `search_faulty.js`, `search.js`, `test_search.js`, `out/prompt-*.md`, this report |
| ① Fix (pane 1) | Reproduced first (exit 1) → confirmed the regression test catches the original error → minimal change to `search.js` (2 lines) → added an `undefined` case → reran tests | Bug description, `search_faulty.js`, `test_search.js` | Fixed `search.js`, extended `test_search.js`, `out/fix-report.md`, `out/修復.done` |
| ② Review (pane 2) | Read-only review of the diff and related code; checked empty string / whitespace only (incl. tab, newline) / normal keyword (case, surrounding whitespace) / no matches / null / undefined / number | `git diff HEAD`, `search.js`, `test_search.js`, `search_faulty.js`, `fix-report.md` | `out/review.md`, `out/審查.done` |

## Order and handoff

1. Main Agent reproduces → commit → open two panes (left: fix, right: review)
2. Send `prompt-修復.md` → wait for `out/修復.done` → main Agent reads the diff and fix-report
3. Record SHA256 of `search.js`/`test_search.js`/`search_faulty.js` (`out/_pre_review.sha`) → send `prompt-審查.md` → wait for `out/審查.done`
4. After review, `sha256sum -c` all OK → confirms the Review Agent stayed read-only
5. Review must-fix = **none** → no bounce-back to the Fix Agent (no fix loop was needed this round)
6. Main Agent runs the three acceptance commands separately → writes this report → commit "修復搜尋空白輸入"

All handoffs went through files; detailed times are in `out/timeline.tsv`.

## Change contents

```diff
# search.js
-  const keyword = typeof query === "string" ? query.trim().toLowerCase() : query;
-  if (keyword === "") throw new Error("搜尋關鍵字不可為空");
+  const keyword = typeof query === "string" ? query.trim().toLowerCase() : "";
+  if (keyword === "") return [];
# test_search.js
+assert.deepEqual(searchItems(undefined, items), []);
-console.log("5 個搜尋情境全部通過");
+console.log("6 個搜尋情境全部通過");
```

## Acceptance (each run separately, not under set -e)

| Command | Actual output (key lines) | Exit code | Expected | Result |
| --- | --- | --- | --- | --- |
| `node test_search.js ./search_faulty.js` | `AssertionError [ERR_ASSERTION]: Got unwanted exception: whitespace query failed: expected [] without throwing` | 1 | 1, contains whitespace query failed | ✅ |
| `node test_search.js ./search.js` | `6 個搜尋情境全部通過` | 0 | 0 | ✅ |
| `node test_search.js` | `6 個搜尋情境全部通過` | 0 | 0 | ✅ |

Completion criteria from the book prompt:

- Original error fixed (empty string / whitespace no longer throw): ✅
- Normal search still works (`"python"` → `[{title:"Python 入門"}]`): ✅
- Related tests pass: ✅ (6/6)
- Must-fix review issues handled: ✅ (none)
- Review Agent read-only: ✅ (SHA256 matches)

## Optional suggestions not applied (outside the "only fix whitespace and empty string" scope)

1. The header comment in `search.js` still says "faulty version" (`search.js:2-4`); it no longer matches the behavior. Kept unchanged to keep the change minimal and match the book's starting text.
2. Tests don't cover case, surrounding whitespace, or tab/newline (the review confirmed these manually).
3. Non-string queries (e.g. a number) now always return `[]`; the old version compared them after string conversion. The requirement doesn't call for number search.

## Checks not performed / open items

- No website or UI here, so no browser-side verification; only module-level verification.
- The panes' Claude status bar header showed the leftover name "ex2-試學" at startup; it changed after `/rename`, and the work was unaffected.
