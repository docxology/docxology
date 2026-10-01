# AGENTS.md — `data/`

Public source snapshots, reviewed evidence caches, and generated site indexes.
Follow the root `AGENTS.md` and `AGENT_START.md` source-of-truth rules.

- Consult `GENERATED.md` before editing a JSON file. Change curated sources
  or reviewed snapshots directly when authorized; rebuild generated indexes
  with their owning orchestrators and the ordered regeneration pipeline.
- Preserve source provenance, DOI roles, and evidence bindings. Scholar
  changes require the root policy's direct authenticated observation and
  snapshot-bound verification receipt before public propagation.
- Keep private records, credentials, and conversation-derived artifacts out
  of this public directory. Preserve unrelated concurrent changes.
- Commit authorized changes on a work branch; never commit on local `main`.

Validate dependent outputs with `uv run python3 code/orchestrators/validate_repo.py`
and run `uv run python3 -m pytest code/tests -q` after substantive changes.
