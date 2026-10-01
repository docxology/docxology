# AGENTS.md — `pages/`

Public Markdown catalogs, profiles, and documentation, including generated
reports. Follow the root `AGENTS.md` and `AGENT_START.md` source-of-truth rules.

- `BIBLIOGRAPHY.md` owns work identity and verified author lists;
  `SOFTWARE.md` owns the curated software catalog. Use `GENERATED.md` to
  identify generated pages and rebuild them from their authoritative sources.
- After bibliography or software edits, run the corresponding HTML sync
  orchestrator with `--apply`, then regenerate dependent exports in order.
- Link to generated count and Scholar snapshots instead of repeating
  volatile totals in hand-authored prose. Keep claims tied to dated evidence.
- Preserve concurrent edits and keep private records, credentials, and
  conversation-derived artifacts out of public documentation.
- Commit authorized changes on a work branch; never commit on local `main`.

Run `uv run python3 code/orchestrators/validate_repo.py` and, after substantive
changes, `uv run python3 -m pytest code/tests -q`.
