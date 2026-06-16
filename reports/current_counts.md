# Current Counts Report

Generated: `2026-06-16T03:36:11+00:00`

This generated report is the repo-local plaintext target for volatile totals. Hand-authored docs should link here, to the canonical source tables, or to generated JSON rather than repeating these values.

Regenerate:

```bash
uv run python3 code/orchestrators/build_current_counts.py
```

Check without writing:

```bash
uv run python3 code/orchestrators/build_current_counts.py --check
```

## Canonical Sources

- bibliography: `pages/BIBLIOGRAPHY.md`
- paper_folders: `papers/README.md`
- software_catalog: `pages/SOFTWARE.md`
- works_export: `data/works.json`
- software_export: `data/software.json`
- github_inventory: `data/github-repositories.json`
- public_source_snapshot: `reports/public_source_snapshot_2026-06-09.json`
- paired_publications: `reports/paired_publications_2026-06-09.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `168`
- Paper-folder docs: `151`
- Bibliography docs links: `151`

### Types

- Books: `5`
- Courses: `3`
- Papers: `147`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `22`
- Active Inference: `38`
- Cognitive Security: `30`
- Art & Synergetics: `15`
- Computational: `27`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `58`
- active_inference_institute: `33`
- curated_total: `91`

### Generated Exports

- data_works_json: `168`
- data_software_json: `91`
- data_publications_ld_main_entity: `168`
- data_software_ld_main_entity: `91`

### GitHub Inventory

- total: `360`
- docxology: `308`
- ActiveInferenceInstitute: `52`
- curated: `89`
- uncataloged: `271`
- forks: `249`
- archived: `0`
- public: `360`
- private: `0`
- recently_updated: `93`

### Public Source Snapshot

- GitHub user docxology: `307`
- GitHub user ActiveInferenceInstitute: `52`
- ORCID work groups: `20`
- PubMed exact author records: `8`

### Paired Publications

- github_releases: `112`
- zenodo_records: `101`
- pairs: `116`
- strong_pairs: `17`
- needs_review: `99`
- create_new: `0`
- update_existing: `17`

### Paired Publication Decisions

- decision: `accept`
- groups: `19`
- raw_candidates: `81`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R19 adds docxology/itrace v0.4.1 as bibliography folder 2026_ITrace with DOI 10.5281/zenodo.20614909.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q`
