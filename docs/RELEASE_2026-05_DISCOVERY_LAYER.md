# Release Snapshot: 2026-05 Discovery Layer

Date: 2026-05-13

This release snapshot describes the current public-index state. Create the Git tag after committing the repository state:

```bash
git tag -a 2026-05-discovery-layer -m "2026-05 discovery layer"
```

## Included Surface

- 115 curated bibliography works.
- 108 per-work paper documentation folders.
- 116 generated work HTML files, including the index page.
- Domain landing pages for Entomology, Active Inference, Cognitive Security, Art & Synergetics, and Computational Methods.
- Search UI, OpenSearch descriptor, RSS feed, DataCatalog, citation exports, and agent-facing JSON indexes.
- Evidence ledger with confidence, caveats, source links, and public-source reconciliation.
- Static accessibility report and Playwright visual QA screenshots.

## Validation Gate

Before tagging, run:

```bash
python3 code/orchestrators/validate_repo.py
git diff --check
cd code/tests && uv run pytest -q
```
