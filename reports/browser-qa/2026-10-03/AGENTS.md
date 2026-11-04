# AGENTS.md — `reports/browser-qa/2026-10-03/`

One dated run of the browser QA suite: `manifest.json` records 8 of 8 checks passing
over progressive enhancement, interaction, responsive layout, and CSP-adjacent runtime
behaviour — the manifest's own `scope` field — produced by the Playwright-based
`code/orchestrators/browser_qa.py`. Read the manifest for the check names and details rather
than trusting this summary.

- The manifest records the tree the run was taken against:
  `generated_at` 2026-10-03T01:08:21Z, `source_commit` `4dabea98`, and
  `source_worktree_clean` false with 2585 modified path(s), so the
  recorded commit does not by itself identify the whole tree rendered.

- This run carries an eighth check, `keyboard shortcuts contain and restore
  focus`, that the runs before 2026-10-02 do not record.
- The manifest records the run only. Nothing re-runs it in CI and no gate fails if the
  site regresses later. Do not hand-edit results; re-run the suite to produce a new
  dated folder.
- The series contract is in [`../AGENTS.md`](../AGENTS.md); repository rules are in
  [`../../AGENTS.md`](../../AGENTS.md).
