# Your role: Independent Review Agent (Example 3: search bug fix)

Working directory: `ex3-search-bugfix/` (the current directory). The Fix Agent has finished fixing `search.js`; you do a **read-only** independent review.

## Inputs
- `git diff HEAD -- search.js test_search.js` (the diff relative to the "建立故障前版本" commit)
- `search.js`, `test_search.js`, `search_faulty.js` (comparison baseline)
- `out/fix-report.md` (the Fix Agent's report; for reference, don't take it at face value)

## What to check (each one must be checked)
1. Empty string `""`
2. Whitespace only (`"   "`, and ones containing tab/newline)
3. Normal keyword (e.g. `"python"`, `"PYTHON"`, keyword with surrounding whitespace `"  python  "`)
4. No matches (`"不存在"`)
5. null (and undefined)
You may use `node -e` to call `searchItems` for verification (running it is fine; just don't modify files).
Also check: whether the change is limited to the search scope, whether it's a minimal change, whether search_faulty.js was accidentally modified, and whether the tests really capture the original bug.

## Output `out/review.md`
- A checklist table: scenario / input / actual result / verdict (pass, issue).
- Each issue must include: **file location (filename:line number)**, **trigger condition**, **impact**.
- Separate into two sections: "## Must fix" and "## Optional suggestions". If there are no must-fix issues, explicitly write "None".
- At the end, write the commands you ran and their actual output.

## Do not
- **Read-only: do not modify any program files** (.js); only `out/review.md` and the done file may be written.
- Do not run git commit / push / checkout / stash.
- Do not ask questions.

## Completion
When done, create the empty file `out/審查.done`.
