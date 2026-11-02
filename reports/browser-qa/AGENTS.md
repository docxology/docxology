# AGENTS.md — `reports/browser-qa/`

The browser QA series: one `YYYY-MM-DD/` folder per run, each holding a `manifest.json`
that records the checks, their outcome, the tool (Playwright), and — in the later runs —
the source commit and whether the worktree was clean. The suite itself is
`code/orchestrators/browser_qa.py`.

- The series is a record, not a gate: nothing in CI re-runs it, and no check fails when
  the site regresses after a run. To refresh, run the suite; it writes a new dated
  folder rather than updating one.
- Read the manifest for scope and counts. The runs differ in what they record — the
  earliest two do not name a source commit — so compare runs by their manifests, not by
  their dates alone.
- The folder list is longer than this guide's evidence: as of 2026-11-02 the series has
  fourteen dated runs, and only three of them plus the newest have their own guide.

Report policy and retention: [`../AGENTS.md`](../AGENTS.md); repository rules:
[`../../AGENTS.md`](../../AGENTS.md).
