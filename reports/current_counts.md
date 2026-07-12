# Current Counts Report

Generated: `2026-07-12T21:57:18+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-07-10.json`
- paired_publications: `reports/paired_publications_2026-07-12.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `193`
- Paper-folder docs: `176`
- Full-text extractions: `173`
- Papers with image galleries: `141`
- Total extracted images: `9004`
- Bibliography docs links: `176`

### Types

- Books: `5`
- Courses: `3`
- Papers: `172`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `42`
- Cognitive Security: `31`
- Art & Synergetics: `15`
- Computational: `46`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `61`
- active_inference_institute: `34`
- curated_total: `95`

### Generated Exports

- data_works_json: `193`
- data_software_json: `95`
- data_publications_ld_main_entity: `193`
- data_software_ld_main_entity: `95`

### GitHub Inventory

- total: `379`
- docxology: `341`
- ActiveInferenceInstitute: `38`
- curated: `92`
- uncataloged: `287`
- forks: `241`
- archived: `0`
- public: `379`
- private: `0`
- recently_updated: `121`
- primary_total: `138`
- primary_docxology: `102`
- primary_ActiveInferenceInstitute: `36`
- fork_docxology: `239`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `340`
- GitHub user ActiveInferenceInstitute: `38`
- ORCID work groups: `20`
- PubMed exact author records: `8`

### Paired Publications

- github_releases: `175`
- zenodo_records: `128`
- pairs: `375`
- strong_pairs: `40`
- already_reviewed: `0`
- needs_review: `335`
- create_new: `0`
- update_existing: `40`

### Paired Publication Decisions

- decision: `accept`
- groups: `24`
- raw_candidates: `86`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q`
