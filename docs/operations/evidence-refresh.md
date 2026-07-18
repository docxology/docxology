# Evidence and coverage refresh

Public APIs and profile pages are freshness evidence, not automatic replacements
for curated rows. Refresh before a claim-sensitive release, then review every
change before regeneration.

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/refresh_public_sources.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/refresh_public_source_inventory.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/build_github_inventory.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/sync_paired_publications.py --include-aii
```

Apply only strong, reviewed GitHub–Zenodo pairs. Record ambiguous outcomes in
`data/paired-publication-decisions.json`; do not auto-create bibliography rows
from a plausible title match. Rebuild `data/coverage-exceptions.json` to keep
legitimate missing-folder, missing-full-text, no-DOI, no-URL, and non-paper
records explicit.

Google Scholar counts and current organizational roles require direct primary
verification. If a signed-in or otherwise authoritative view is unavailable,
keep the dated snapshot and caveat rather than guessing. Finish with
`regenerate_all.py --validate`, then inspect the newest source, reconciliation,
and pairing reports.
