# GitHub and Zenodo Publication Sync

This is the canonical runbook for checking GitHub releases against Zenodo records and adding new or updated publications to the unified bibliography.

Use this workflow when new GitHub releases, Zenodo deposits, PDFs, or DOI versions may have appeared. The automation keeps [`pages/BIBLIOGRAPHY.md`](../../pages/BIBLIOGRAPHY.md), [`data/works.json`](../../data/works.json), paper folders, generated paper pages, and site indexes aligned.

## Source Contract

- [`code/orchestrators/sync_paired_publications.py`](../../code/orchestrators/sync_paired_publications.py) is the canonical GitHub Releases + Zenodo Records pairing tool.
- GitHub releases provide source-repository and release context. Zenodo records provide DOI, archival metadata, record URLs, and downloadable PDFs.
- Strong `create_new` and `update_existing` actions may be applied automatically with `--apply`.
- `needs_review` actions are review-only. Do not auto-apply them without manual curation.
- Same-title / same-GitHub-release Zenodo versions update the existing row instead of creating duplicate bibliography entries.
- Public APIs are freshness checks. Curated local rows remain the source of truth after review and application.

## Preconditions

Use a GitHub token so rate limits do not truncate repository or release scans:

```bash
GITHUB_TOKEN="$(gh auth token)"
export GITHUB_TOKEN
```

Before applying changes, check the worktree and preserve unrelated edits:

```bash
git status --short --branch
```

If other work is present, layer the publication-sync changes on top without reverting or normalizing unrelated files.

## Refresh Public Sources

Run these when you need the public-source snapshots and GitHub inventory current before a pairing decision:

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/refresh_public_sources.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/refresh_public_source_inventory.py
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/build_github_inventory.py
```

The generated reports under [`reports/`](../../reports/) are evidence snapshots. They support review but do not replace the curated bibliography.

## Dry Run Pairing

Run the pairing scan without changing curated files:

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/sync_paired_publications.py --include-aii
```

This writes `reports/paired_publications_YYYY-MM-DD.json`. Review:

- `counts.github_releases`, `counts.zenodo_records`, and `counts.pairs` for scan coverage.
- `counts.create_new`, `counts.update_existing`, and `counts.needs_review` for action load.
- `actions[].action_type`:
  - `create_new`: strong GitHub + Zenodo pair not already represented in the bibliography.
  - `update_existing`: existing row/folder should receive newer DOI, version, PDF, metadata, or source links.
  - `needs_review`: plausible but ambiguous pair; inspect manually before changing curated files.
  - `already_reviewed`: exact release/record pair is recorded in `data/paired-publication-decisions.json` as represented, superseded, or version-history-only; do not create a duplicate row.
- `warnings[]` for API or metadata issues that may affect completeness.

Validate the latest cached report:

```bash
uv run python3 code/orchestrators/sync_paired_publications.py --check
```

## Apply Strong Pairs

Apply only strong create/update actions:

```bash
GITHUB_TOKEN="$(gh auth token)" uv run python3 code/orchestrators/sync_paired_publications.py --include-aii --apply
```

By default, apply mode downloads available Zenodo PDFs and updates curated/generated source surfaces. Use `--no-download-files` only when intentionally deferring PDFs.

Expected source-owned updates include:

- bibliography rows in [`pages/BIBLIOGRAPHY.md`](../../pages/BIBLIOGRAPHY.md)
- per-paper folders under [`papers/`](../../papers/) with `README.md`, `AGENTS.md`, `SKILL.md`, `metadata.json`, `CITATION.cff`, and PDFs when available
- [`papers/paper_metadata.json`](../../papers/paper_metadata.json)
- [`papers/README.md`](../../papers/README.md) and [`papers/AGENTS.md`](../../papers/AGENTS.md)
- software cross-links in [`pages/SOFTWARE.md`](../../pages/SOFTWARE.md) when a paired repository should be catalogued

Apply mode also runs the publication regeneration chain for bibliography exports, publications HTML, software exports, domain/work/paper pages, catalog/search/feed/sitemap, asset audit, and generated manifest.

## Manual Review Path

For `needs_review` actions, inspect the GitHub release, Zenodo record, DOI, title, creator list, repository URL, and PDF before deciding.

Record manual decisions in [`data/paired-publication-decisions.json`](../../data/paired-publication-decisions.json) and, when useful, in a dated review queue under [`reports/`](../../reports/). An `accept` or `superseded` decision records the GitHub release + Zenodo record relationship; it does not by itself require a new bibliography row when the record is software/version metadata, version history, or an already represented work. Exact reviewed pairs will be reported as `already_reviewed` on future scans.

If the item is a real publication but cannot be safely auto-applied:

1. Add or update the row in [`pages/BIBLIOGRAPHY.md`](../../pages/BIBLIOGRAPHY.md).
2. Create or update the matching `papers/YYYY_Topic/` folder with `README.md`, `AGENTS.md`, `SKILL.md`, `metadata.json`, `CITATION.cff`, and any public PDF.
3. Update [`papers/paper_metadata.json`](../../papers/paper_metadata.json) and paper indexes if the folder set changed.
4. Run the regeneration and validation commands below.

Do not create duplicate rows for newer Zenodo versions of the same work; update the existing row and preserve version-chain context where useful.

## Regenerate Dependent Surfaces

After any apply or manual curation, run the broad refresh sequence:

```bash
uv run python3 code/orchestrators/build_paper_pages.py
uv run python3 code/orchestrators/build_sitemap.py
uv run python3 code/orchestrators/build_generated_manifest.py
uv run python3 code/orchestrators/build_resume.py --all
uv run python3 code/orchestrators/validate_repo.py
uv run pytest code/tests -q
```

If bibliography, software, evidence, or reconciliation data changed outside the apply path, also run the specific generator listed in [`GENERATED.md`](../../GENERATED.md) before validation.

## Acceptance Checks

Before committing or pushing, confirm:

- [`publications.html`](../../publications.html) includes each new or updated work.
- [`data/works.json`](../../data/works.json) includes the canonical DOI and paper-folder path.
- Each publication folder has `README.md`, `AGENTS.md`, `SKILL.md`, `metadata.json`, and at least one local artifact link when a PDF exists.
- [`papers/<folder>/index.html`](../../papers/) exists for every bibliography row with a docs path.
- [`sitemap.xml`](../../sitemap.xml), [`search-index.json`](../../search-index.json), [`GENERATED.md`](../../GENERATED.md), and [`data/generated-manifest.json`](../../data/generated-manifest.json) reflect the new public URLs.

After push, verify representative live URLs:

```bash
curl -L -I https://danielarifriedman.com/publications.html
curl -L -I https://danielarifriedman.com/data/works.json
curl -L -I https://danielarifriedman.com/papers/<folder>/
curl -L -I https://danielarifriedman.com/papers/<folder>/README.md
curl -L -I https://danielarifriedman.com/papers/<folder>/<paper>.pdf
```
