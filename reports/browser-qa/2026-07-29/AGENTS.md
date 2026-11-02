# AGENTS.md — `reports/browser-qa/2026-07-29/`

One dated run of the browser QA suite: `manifest.json` records 7 of 7 checks passing
(progressive enhancement, interaction, responsive layout, CSP-adjacent runtime
behaviour), produced by the Playwright-based `code/orchestrators/browser_qa.py` on
2026-07-29. The manifest is the record; read it for check names and details.

- Evidence about that run only. Nothing re-runs in CI, and no gate fails if the site
  regresses afterwards. Results are not hand-editable — re-run the suite instead.
- Like the earlier run, this manifest does not name the source commit it was taken
  against; comparing runs across the series needs the later, commit-bearing manifests.
- Series contract: [`../AGENTS.md`](../AGENTS.md).
