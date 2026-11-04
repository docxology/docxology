# AGENTS.md — `reports/visual-qa/2026-10-05/`

One dated set from the visual and smoke QA lane.

`manifest.json` records 26 full-page screenshots taken by
the Playwright-based `code/orchestrators/visual_qa.py`.
The manifest's own note:

> "Human review still required; these snapshots guard against obvious layout regressions."

This folder holds 26 screenshots and the manifest; read the manifest for the
page list rather than trusting this summary.

- The manifest records the tree the run was taken against:
  `generated_at` 2026-10-05T15:10:56Z, `source_commit` `a7ef3df9`, and
  `source_worktree_clean` false with 52 modified path(s), so the
  recorded commit does not by itself identify the whole tree rendered.
- The `review` block reads `"status": "pending"` with `reviewed_by` and
  `reviewed_at` null: a human has not signed this set off. Do not read it as
  approved, and do not edit the manifest to record a review.
- `code/orchestrators/prune_old_reports.py` may prune a superseded dated screenshot
  set to bound the working tree; it requires a reviewed provenance record in
  `data/report-retention.json`, and git history retains anything pruned. Nothing in
  the repository reads an older set.
- Repository rules are in [`../../AGENTS.md`](../../AGENTS.md).
