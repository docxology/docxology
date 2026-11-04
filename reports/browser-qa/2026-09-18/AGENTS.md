# AGENTS.md — `reports/browser-qa/2026-09-18/`

One dated run of the browser QA suite: `manifest.json` records 7 of 7 checks passing
over progressive enhancement, interaction, responsive layout, and CSP-adjacent runtime
behaviour — the manifest's own `scope` field — produced by the Playwright-based
`code/orchestrators/browser_qa.py`. Read the manifest for the check names and details rather
than trusting this summary.

- The manifest records the tree the run was taken against:
  `generated_at` 2026-09-18T03:31:39Z, `source_commit` `0febd8e0` and
  `source_worktree_clean` true.

- The seven checks are the same seven the other runs in this series record.
- The manifest records the run only. Nothing re-runs it in CI and no gate fails if the
  site regresses later. Do not hand-edit results; re-run the suite to produce a new
  dated folder.
- The series contract is in [`../AGENTS.md`](../AGENTS.md); repository rules are in
  [`../../AGENTS.md`](../../AGENTS.md).
