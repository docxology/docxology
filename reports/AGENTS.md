# AGENTS.md — `reports/`

Public QA receipts, source-review records, and generated summaries. Follow
the root `AGENTS.md` and the report's owning orchestrator or runbook.

- Regenerate receipts with their tools; do not hand-edit results or infer
  successful checks that did not run. Separate local tests, hosted checks,
  and direct live-service observations.
- Preserve dated evidence and binder relationships. Review and track new
  report files before regenerating surfaces that resolve tracked receipts;
  follow `docs/operations/settle.md` for payload and control-tail ordering.
- Inspect report contents before public publication. Exclude credentials,
  private records, and conversation-derived artifacts; preserve unrelated work.
- Commit authorized reports on a work branch; never commit on local `main`.

Use the report's check mode where available and
`uv run python3 code/orchestrators/validate_repo.py` for repository integrity.
