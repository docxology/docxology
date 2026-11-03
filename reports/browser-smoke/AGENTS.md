# AGENTS.md — `reports/browser-smoke/`

The browser smoke-test series: one dated folder per run, most recently `2026-10-05/`
(observed 2026-11-02), whose
`manifest.json` records 10 of 10 selector-based checks passing (with a screenshot and
its SHA-256 per check) against commit `a7ef3df9` with a dirty worktree. The suite is
`code/orchestrators/browser_smoke.py`.

- Selector checks are shallow by design: a passing run says the core elements appeared,
  not that a page is correct. Nothing re-runs in CI, so the record ages without failing.
- Refresh by running the suite; it writes a new dated folder instead of updating this
  one. Do not edit manifests or screenshots by hand.
- Report policy: [`../AGENTS.md`](../AGENTS.md).
