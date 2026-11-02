# AGENTS.md — `reports/browser-qa/2026-08-26/`

One dated run of the repository's browser QA suite: `manifest.json` is the run's
record, produced by `code/orchestrators/browser_qa.py` (Playwright) on 2026-08-26
against commit `5c25de20`. The manifest records 7 of 7 checks passing over
progressive enhancement, interaction, responsive, and CSP-adjacent runtime
behavior — read it for the exact scope, counts, and commit rather than trusting
this summary.

- The manifest is evidence about that run at that commit only. Nothing here re-runs
  in CI, and no gate fails if the site later regresses. Do not hand-edit results or
  manufacture a passing check in JSON; re-run the suite and let it write a new
  dated folder.
- The series contract is in [`../AGENTS.md`](../AGENTS.md); report retention and
  what reaches the deployed site projection are covered in
  [`../../AGENTS.md`](../../AGENTS.md). Older dated runs stay in the repository but
  are dropped from the Pages projection.
- The interactive-layer behavior this suite exercises is specified in
  [`../../../docs/operations/site-runtime.md`](../../../docs/operations/site-runtime.md);
  a screenshot or manifest here is not a live check of the current site.
