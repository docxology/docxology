# Current Counts Report

Generated: `2026-09-04T06:11:51+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-09-04.json`
- paired_publications: `reports/paired_publications_2026-09-04.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `212`
- Paper-folder docs: `195`
- Full-text extractions: `190`
- Papers with image galleries: `139`
- Total extracted images: `8944`
- Bibliography docs links: `195`

### Types

- Books: `5`
- Courses: `3`
- Papers: `190`
- Playbooks: `2`
- Presentations: `9`
- Report: `1`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `45`
- Cognitive Security: `37`
- Art & Synergetics: `16`
- Computational: `54`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `109`
- active_inference_institute: `39`
- curated_total: `148`

### Generated Exports

- data_works_json: `212`
- data_software_json: `148`
- data_publications_ld_main_entity: `212`
- data_software_ld_main_entity: `148`

### GitHub Inventory

- total: `249`
- docxology: `206`
- ActiveInferenceInstitute: `43`
- curated: `147`
- uncataloged: `102`
- forks: `88`
- archived: `5`
- public: `249`
- private: `0`
- recently_updated: `187`
- primary_total: `161`
- primary_docxology: `120`
- primary_ActiveInferenceInstitute: `41`
- fork_docxology: `86`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `206`
- GitHub user ActiveInferenceInstitute: `43`
- ORCID work groups: `20`
- PubMed exact author records: `8`
- Europe PMC exact author records: `10`
- Crossref ORCID DOI records: `15`
- Zenodo exact-name creator records: `61`
- Zenodo ORCID-linked records: `148`

### Paired Publications

- github_releases: `231`
- zenodo_records: `151`
- pairs: `450`
- strong_pairs: `48`
- already_reviewed: `398`
- needs_review: `5`
- create_new: `0`
- update_existing: `47`

### Paired Publication Decisions

- decision: `accept`
- groups: `72`
- raw_candidates: `487`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows. R26-R27 record CogSecSkills and Codomyrmex version-history decisions under already-cited DOIs. R71 records the untagged Codomyrmex v1.3.0 release as already represented, and R72 records Active Fedference v1.0.4 as a version-specific artifact under its existing concept DOI without a duplicate bibliography row.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q`
