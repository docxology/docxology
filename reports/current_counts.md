# Current Counts Report

Generated: `2026-07-01T00:30:29+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-06-18.json`
- paired_publications: `reports/paired_publications_2026-07-01.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `181`
- Paper-folder docs: `164`
- Bibliography docs links: `164`

### Types

- Books: `5`
- Courses: `3`
- Papers: `160`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `22`
- Active Inference: `39`
- Cognitive Security: `31`
- Art & Synergetics: `15`
- Computational: `38`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `61`
- active_inference_institute: `34`
- curated_total: `95`

### Generated Exports

- data_works_json: `181`
- data_software_json: `95`
- data_publications_ld_main_entity: `181`
- data_software_ld_main_entity: `95`

### GitHub Inventory

- total: `373`
- docxology: `319`
- ActiveInferenceInstitute: `54`
- curated: `94`
- uncataloged: `279`
- forks: `252`
- archived: `0`
- public: `373`
- private: `0`
- recently_updated: `92`

### Public Source Snapshot

- GitHub user docxology: `317`
- GitHub user ActiveInferenceInstitute: `54`
- ORCID work groups: `20`
- PubMed exact author records: `8`

### Paired Publications

- github_releases: `166`
- zenodo_records: `117`
- pairs: `240`
- strong_pairs: `33`
- already_reviewed: `0`
- needs_review: `207`
- create_new: `2`
- update_existing: `31`

### Paired Publication Decisions

- decision: `accept`
- groups: `24`
- raw_candidates: `86`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q`
