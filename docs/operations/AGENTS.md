# AGENTS.md — `docs/operations/`

The operating runbooks, with [`development.md`](development.md) as the entry point for
source authority, configuration ownership, and verification boundaries;
[`maintenance-log.md`](maintenance-log.md) is the historical record rather than a
procedure.

- These describe procedures, and some of them cannot be executed from a checkout: the
  publication-sync and Google Search Console runbooks need network access or a signed-in
  browser. Read a runbook before promising it can be automated.
- After changing a generated surface, the ordered pipeline matters — the authoritative
  plan is `uv run python3 code/orchestrators/regenerate_all.py --list`, and
  `GENERATED.md` is the output matrix. Do not maintain a second list here.
- Nothing tests the runbooks themselves; `validate_repo.py` and the Python suite check
  the repository, not these documents.

Docs-tree guide: [`../AGENTS.md`](../AGENTS.md).
