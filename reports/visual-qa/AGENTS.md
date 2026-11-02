# AGENTS.md — `reports/visual-qa/`

The visual QA series: one dated folder per run, most recently `2026-10-05/`
(observed 2026-11-02), holding
per-page, per-viewport screenshots (26 of them) with a `manifest.json` that states
plainly that human review is still required and carries a `review` block recording who
reviewed it and when.

- Snapshots guard against obvious layout regressions; they are not an approval. The
  manifest's review status is the only place a review is recorded — do not write one
  yourself.
- Refresh by re-running the suite (`code/orchestrators/browser_smoke.py` writes the
  screenshots used here); a new run writes a new dated folder.
- Report policy: [`../AGENTS.md`](../AGENTS.md).
