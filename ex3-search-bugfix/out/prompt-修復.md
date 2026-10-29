# Your role: Fix Agent (Example 3: search bug fix)

Working directory: `ex3-search-bugfix/` (the current directory). You are one of two sub-agents; the main Agent handles integration and final acceptance.

## Bug behavior
`searchItems(query, items)` throws "搜尋關鍵字不可為空" when the search box input is an empty string or only whitespace, which breaks the entire search feature.
Expected behavior: empty string, whitespace-only, and null queries all return `[]` without throwing; normal keyword search (case-insensitive) keeps working; no matches returns `[]`.

## Inputs
- `search_faulty.js` (faulty version; **do not modify**, used as the regression baseline)
- `search.js` (currently identical to the faulty version; **this is what you fix**)
- `test_search.js` (the book's regression test)

## Your responsibilities (in order)
1. Reproduce first: run `node test_search.js ./search.js` and `node test_search.js ./search_faulty.js`, record the exit codes and key error messages.
2. Confirm the regression test captures the original error (the `doesNotThrow` on the whitespace query must fail on the faulty version). If needed, you may extend `test_search.js` with `undefined` as a case (keep the file's original logic and the "whitespace query failed" message; update the passing-count text accordingly).
3. Make a **minimal change** to `search.js`: change only what's needed for empty/whitespace/null input; do not refactor or enhance features.
4. Run the tests again:
   - `node test_search.js ./search.js` (should be 0)
   - `node test_search.js` (should be 0)
   - `node test_search.js ./search_faulty.js` (should be 1, message contains whitespace query failed)
5. Write `out/fix-report.md`: changed files, the reason for each change, every command run, and its actual output and exit code.

## Do not
- Do not modify `search_faulty.js`, `BOOK_CODE.md`, or `TASK.md`.
- Do not add new features (e.g. fuzzy search, sorting) or touch non-search files.
- Do not claim the website or UI has been fixed (this is module-level verification only).
- Do not run git commit / push (the main Agent will commit).
- Do not ask questions; use your judgment based on the principles above and write your assumptions into the report.

## Completion
When done, create the empty file `out/修復.done` (e.g. `touch out/修復.done`).
