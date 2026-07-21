# Current Counts Report

Generated: `2026-07-21T12:52:24+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-07-18.json`
- paired_publications: `reports/paired_publications_2026-07-18.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `197`
- Paper-folder docs: `180`
- Full-text extractions: `173`
- Papers with image galleries: `141`
- Total extracted images: `9004`
- Bibliography docs links: `180`

### Types

- Books: `5`
- Courses: `3`
- Papers: `176`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `42`
- Cognitive Security: `32`
- Art & Synergetics: `16`
- Computational: `48`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `62`
- active_inference_institute: `34`
- curated_total: `96`

### Generated Exports

- data_works_json: `197`
- data_software_json: `96`
- data_publications_ld_main_entity: `197`
- data_software_ld_main_entity: `96`

### GitHub Inventory

- total: `385`
- docxology: `345`
- ActiveInferenceInstitute: `40`
- curated: `93`
- uncataloged: `292`
- forks: `243`
- archived: `0`
- public: `385`
- private: `0`
- recently_updated: `122`
- primary_total: `142`
- primary_docxology: `104`
- primary_ActiveInferenceInstitute: `38`
- fork_docxology: `241`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `345`
- GitHub user ActiveInferenceInstitute: `40`
- ORCID work groups: `20`
- PubMed exact author records: `8`
- Europe PMC exact author records: `10`
- Crossref ORCID DOI records: `15`
- Zenodo exact-name creator records: `47`
- Zenodo ORCID-linked records: `131`

### Paired Publications

- github_releases: `2`
- zenodo_records: `133`
- pairs: `1`
- strong_pairs: `1`
- already_reviewed: `0`
- needs_review: `0`
- create_new: `0`
- update_existing: `1`

### Paired Publication Decisions

- decision: `accept`
- groups: `24`
- raw_candidates: `86`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q`
