# AGENTS.md — `code/tests/`

Regression and repository-invariant tests for the public repository. Follow
the root and `code/AGENTS.md` rules and the declared Python runtime.

- Use disposable `tmp_path` fixtures for mutation tests. Never tamper with
  tracked outputs: parallel readers and interrupted runs must leave the
  checkout intact.
- Test meaningful source, identity, evidence, and failure boundaries. Keep
  synthetic fixtures public and free of credentials or private records.
- Run the focused tests for a change before the substantive-change gate:
  `uv run python3 -m pytest code/tests -q`.
- Validate generated layers with
  `uv run python3 code/orchestrators/validate_repo.py`; rebuild drift with the
  owning generator rather than editing a golden output to hide a failure.
- Preserve concurrent edits. Commit authorized changes on a work branch;
  never commit on local `main`.
