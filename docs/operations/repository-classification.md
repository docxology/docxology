# Repository classification

`data/github-repositories.json` is the complete generated public inventory. It is
not the curated software catalog. `data/repository-classification.json` is the
review queue for inventory rows that are not present in `pages/SOFTWARE.md`.

## Refresh and inspect

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/build_github_inventory.py
uv run python3 code/orchestrators/classify_repositories.py
uv run python3 code/orchestrators/classify_repositories.py --check
```

Each queue row preserves ownership, fork/archive/privacy state, language,
topics, update signal, description text, and a derived description-quality
signal (`missing`, `short`, or `substantive`). The quality signal is triage
metadata, not a judgment about the repository.

## Manual catalog decision

Review primary repositories in bounded batches. A fork is not promoted solely
because it is visible in the inventory. Promote a repository only after a
human confirms that it belongs in the curated software table, then update
`pages/SOFTWARE.md` and run:

```bash
uv run python3 code/orchestrators/regenerate_all.py --validate
```

Never invent a publication row from a repository description. Use the
publication-sync runbook for GitHub release + Zenodo evidence.

## Operational notes (learned 2026-08-07)

- The `curated` flag lives in `data/github-repositories.json` and is computed at
  build time from `data/software.json` (`curated_keys()` in
  `build_github_inventory.py`). After promoting a repo in `pages/SOFTWARE.md` you
  MUST rebuild the inventory before `classify_repositories.py` stops queueing it:
  `GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/build_github_inventory.py`
  (the script reads `GITHUB_TOKEN`, not `GH_TOKEN`; unauthenticated runs 403 after
  ~60 requests/hour). The classifier preserves its `generated_at` when the body is
  unchanged, so a stale-looking timestamp is expected for a stable queue.
- `regenerate_all.py` runs `build_current_counts.py` and `classify_repositories.py`
  BEFORE `export_agent_data.py` (which rewrites `data/software.json`), so on the
  pass that changes SOFTWARE.md the recorded export counts / curated flags come
  from the previous pass. After any SOFTWARE.md count change, run the pipeline
  twice (or run `build_current_counts.py` + `classify_repositories.py` again
  after `regenerate_all.py`) and then re-run `pytest code/tests` - the
  `test_count_consistency` suite catches the one-pass drift
  (`data_software_json` vs `curated_total`).
