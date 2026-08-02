# Current Counts Report

Generated: `2026-08-02T22:55:22+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-07-21.json`
- paired_publications: `reports/paired_publications_2026-07-30.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `204`
- Paper-folder docs: `187`
- Full-text extractions: `171`
- Papers with image galleries: `139`
- Total extracted images: `8886`
- Bibliography docs links: `187`

### Types

- Books: `5`
- Courses: `3`
- Papers: `183`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `43`
- Cognitive Security: `34`
- Art & Synergetics: `16`
- Computational: `52`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `94`
- active_inference_institute: `38`
- curated_total: `132`

### Generated Exports

- data_works_json: `204`
- data_software_json: `132`
- data_publications_ld_main_entity: `204`
- data_software_ld_main_entity: `132`

### GitHub Inventory

- total: `387`
- docxology: `347`
- ActiveInferenceInstitute: `40`
- curated: `128`
- uncataloged: `259`
- forks: `245`
- archived: `0`
- public: `387`
- private: `0`
- recently_updated: `124`
- primary_total: `142`
- primary_docxology: `104`
- primary_ActiveInferenceInstitute: `38`
- fork_docxology: `243`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `347`
- GitHub user ActiveInferenceInstitute: `40`
- ORCID work groups: `20`
- PubMed exact author records: `8`
- Europe PMC exact author records: `10`
- Crossref ORCID DOI records: `15`
- Zenodo exact-name creator records: `47`
- Zenodo ORCID-linked records: `131`

### Paired Publications

- github_releases: `1`
- zenodo_records: `135`
- pairs: `0`
- strong_pairs: `0`
- already_reviewed: `0`
- needs_review: `0`
- create_new: `0`
- update_existing: `0`

### Paired Publication Decisions

- decision: `accept`
- groups: `24`
- raw_candidates: `86`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q`
