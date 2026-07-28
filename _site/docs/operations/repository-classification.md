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
