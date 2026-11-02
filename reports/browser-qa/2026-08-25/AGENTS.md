# AGENTS.md — `reports/browser-qa/2026-08-25/`

One dated run of the browser QA suite: `manifest.json` records 7 of 7 checks passing
over progressive enhancement, interaction, responsive layout, and CSP-adjacent runtime
behaviour, taken on 2026-08-25 against commit `b08dc428` — with
`source_worktree_clean: false`, so the recorded tree was not a clean checkout of that
commit. Read the manifest for the details.

- The manifest is evidence about that tree at that run only. Nothing re-runs in CI and
  no gate fails if the site regresses afterwards; re-run the suite rather than editing
  results.
- The dirty-worktree flag is the useful part of this record: it says the run cannot be
  reproduced exactly from the named commit. The later 2026-08-26 run records a clean
  tree.
- Series contract: [`../AGENTS.md`](../AGENTS.md).
