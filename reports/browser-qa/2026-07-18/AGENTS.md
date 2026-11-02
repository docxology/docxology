# AGENTS.md — `reports/browser-qa/2026-07-18/`

One dated run of the browser QA suite: `manifest.json` records 7 of 7 checks passing
over progressive enhancement, interaction, responsive layout, and CSP-adjacent runtime
behaviour, produced by the Playwright-based `code/orchestrators/browser_qa.py` on
2026-07-18. Read the manifest for the check names and details rather than trusting this
summary.

- The manifest records the run only. Nothing re-runs it in CI and no gate fails if the
  site regresses later. Do not hand-edit results; re-run the suite to produce a new
  dated folder.
- This run's manifest does not record the source commit it was taken against — an
  absence worth noticing when comparing runs. Later manifests do.
- The series contract is in [`../AGENTS.md`](../AGENTS.md); repository rules are in
  [`../../AGENTS.md`](../../AGENTS.md).
