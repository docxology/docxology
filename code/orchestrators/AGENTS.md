# AGENTS.md — `code/orchestrators/`

Runnable generators, source-intake tools, and validators for the public
`docxology/docxology` repository. Follow the root and `code/AGENTS.md` rules.

- Inspect the script's declared source inputs and write scope before running it.
  Use `GENERATED.md` for the source-to-output rebuild commands and the ordered
  `regenerate_all.py` pipeline when several generated layers change.
- Edit authoritative sources; rebuild owned outputs with their generators.
  Keep network intake and reviewed source corrections distinct from rendering.
- Preserve concurrent edits and keep private records, credentials, and
  conversation-derived material out of public sources and reports.
- Commit authorized changes on a work branch; never commit on local `main`.
  Follow `docs/operations/settle.md` for publication and binder ordering.

Run focused checks for changed scripts, then `uv run python3 -m pytest code/tests -q`
and `uv run python3 code/orchestrators/validate_repo.py` for substantive changes.
