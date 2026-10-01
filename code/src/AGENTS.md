# AGENTS.md — `code/src/`

Shared parsers, renderers, and validation contracts for the public repository.
Follow the root and `code/AGENTS.md` rules, including the `docxology_tools`
import bootstrap and generated-output ownership boundaries.

- Inspect callers and connected generators before changing shared behavior.
  Preserve authoritative source identity and reject invalid input explicitly.
- Keep source changes reviewable with focused failure-case regressions.
  Obtain fresh independent review for shared infrastructure or security changes.
- Preserve concurrent edits and exclude private records, credentials, and
  conversation-derived material from public artifacts.
- Commit authorized changes on a work branch; never commit on local `main`.

Run focused tests, then `uv run python3 -m pytest code/tests -q` and
`uv run python3 code/orchestrators/validate_repo.py` for substantive changes.
Regenerate affected outputs using `GENERATED.md` and the ordered pipeline.
