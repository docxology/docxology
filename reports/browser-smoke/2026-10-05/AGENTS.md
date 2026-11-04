# AGENTS.md — `reports/browser-smoke/2026-10-05/`

One dated set from the visual and smoke QA lane.

`manifest.json` records 10 of 10 selector checks
passing, each with a full-page PNG screenshot beside it, produced by
the Playwright-based `code/orchestrators/browser_smoke.py`.
The manifest's own note:

> "Selector-based smoke checks for core local site behavior."

This folder holds 10 screenshots and the manifest; read the manifest for the
page list rather than trusting this summary.

- The manifest records the tree the run was taken against:
  `generated_at` 2026-10-05T15:10:40Z, `source_commit` `a7ef3df9`, and
  `source_worktree_clean` false with 52 modified path(s), so the
  recorded commit does not by itself identify the whole tree rendered.
- `code/orchestrators/prune_old_reports.py` may prune a superseded dated screenshot
  set to bound the working tree; it requires a reviewed provenance record in
  `data/report-retention.json`, and git history retains anything pruned. Nothing in
  the repository reads an older set.
- Repository rules are in [`../../AGENTS.md`](../../AGENTS.md).
