# Repository classification

`data/github-repositories.json` is the complete generated public inventory. It is
not the curated software catalog. `data/repository-classification.json` classifies
inventory rows outside that catalog, including deferred reviews and acknowledged
exclusions.

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

## Exclusion provenance

`data/repository-exclusions.json` (schema 1.4) records reviewed decisions to keep
a repository outside the curated catalog. Acknowledged rows remain in the
generated classification with `review_status: acknowledged`; they do not become
software-catalog entries. Every entry records *how* the decision was reached in
`reviewed_by`, and the two values are never blurred:

| `reviewed_by` | Meaning | Extra requirement |
| --- | --- | --- |
| `principal` | The principal reviewed this specific repository on `reviewed_at`. | — |
| `standing_policy` | An already-recorded principal decision was applied to a repository nobody looked at individually. | `policy_source` must name that decision, and the entry must be a fork. |

`classify_repositories.py` enforces both requirements. A `standing_policy`
entry without a `policy_source`, or one covering a primary repository, is a
validation error rather than a quietly acknowledged row — a primary repository
is always an individual call.

The standing policy in force is the principal's 2026-08-26 decision recorded in
`TODO.md` DOC-005: public forks stay `fork_not_curated`. A new fork appearing in
an inventory refresh may be recorded under it; anything else waits for a
decision.

Each exclusion must record the inventory's `full_name`, `github_id`, and
`github_node_id`, along with its declared reason, note, reviewer, and review date.
The classifier acknowledges it only when the exact name and both immutable
identities match and the reason fits the repository's fork/primary state. A
transferred or recreated repository cannot inherit a decision from its path.

## Local membership and ordered passes

- The inventory's `curated` flag is derived directly from `pages/SOFTWARE.md`
  (`curated_keys()` in `build_github_inventory.py`). After a catalog edit,
  `render_github_inventory.py` refreshes those flags and counts and rebuilds both
  inventory pages locally, preserving retained GitHub facts and their observation
  timestamp. This step is included in `regenerate_all.py`; a new network fetch is
  needed only when deliberately refreshing GitHub observations.
- `classify_repositories.py` also reads `data/software.json` and omits a row when
  either that export or the inventory marks it curated. Local regeneration can
  therefore clear a catalog promotion without another GitHub request. The
  classifier preserves `generated_at` when its body is unchanged; that timestamp
  does not establish fresh network evidence.
- The driver runs two ordered passes by default. They refresh consumers such as
  current counts that run before `export_agent_data.py` produces updated software
  data. Use one `regenerate_all.py --validate` invocation after a catalog edit;
  an extra invocation is not part of the normal procedure. See
  [regeneration.md](regeneration.md) for diagnostic pass counts and cache rules.
