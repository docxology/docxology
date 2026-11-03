# AGENTS.md — `.github/workflows/`

The Actions workflows: `validate.yml` (the correctness gate —
`code/orchestrators/validate_repo.py` plus the Python suite), `pages.yml` (Pages
deploy), `browser-qa.yml`, `freshness.yml`, `live-verify.yml`, and
`indexnow-on-push.yml`.

- `validate.yml` is the gate to reproduce locally: `uv run python3
  code/orchestrators/validate_repo.py`, `uv run python3 -m pytest code/tests -q`, and
  `uv run --group lint ruff check code`. The workflow file itself is the authority on
  what it runs; this guide is not updated with it.
- The network-dependent workflows (freshness, live verification, IndexNow promotion)
  cannot be reproduced offline; they leave dated evidence under `reports/`.
- Secrets are configured in GitHub, never in the repository.

Repository rules: [root guide](../../AGENTS.md).
