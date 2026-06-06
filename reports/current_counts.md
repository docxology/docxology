# Current Counts Report

Generated: `2026-06-04T22:33:24+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-06-04.json`
- paired_publications: `reports/paired_publications_2026-06-04.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `154`
- Paper-folder docs: `147`
- Bibliography docs links: `147`

### Types

- Books: `5`
- Courses: `3`
- Papers: `133`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `21`
- Active Inference: `35`
- Cognitive Security: `26`
- Art & Synergetics: `15`
- Computational: `24`
- AII Ecosystem: `5`
- Presentations & Media: `15`
- Genetics & Biomedical: `13`

### Software

- docxology_owned: `56`
- active_inference_institute: `32`
- curated_total: `88`

### Generated Exports

- data_works_json: `154`
- data_software_json: `88`
- data_publications_ld_main_entity: `154`
- data_software_ld_main_entity: `88`

### GitHub Inventory

- total: `356`
- docxology: `305`
- ActiveInferenceInstitute: `51`
- curated: `88`
- uncataloged: `268`
- forks: `248`
- archived: `0`
- public: `356`
- private: `0`
- recently_updated: `89`

### Public Source Snapshot

- GitHub user docxology: `305`
- GitHub user ActiveInferenceInstitute: `51`
- ORCID work groups: `20`
- PubMed exact author records: `8`

### Paired Publications

- github_releases: `109`
- zenodo_records: `100`
- pairs: `95`
- strong_pairs: `17`
- needs_review: `78`
- create_new: `4`
- update_existing: `13`

### Paired Publication Decisions

- decision: `accept`
- groups: `18`
- raw_candidates: `78`
- note: `User instructed: Accept for all. Acceptance records the candidate GitHub release + Zenodo record relation; software-only records remain software/version metadata rather than new bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q`
