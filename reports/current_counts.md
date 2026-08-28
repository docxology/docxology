# Current Counts Report

Generated: `2026-08-28T21:34:19+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-08-26.json`
- paired_publications: `reports/paired_publications_2026-08-28.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `211`
- Paper-folder docs: `194`
- Full-text extractions: `189`
- Papers with image galleries: `139`
- Total extracted images: `8944`
- Bibliography docs links: `194`

### Types

- Books: `5`
- Courses: `3`
- Papers: `190`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `45`
- Cognitive Security: `35`
- Art & Synergetics: `16`
- Computational: `56`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `108`
- active_inference_institute: `39`
- curated_total: `147`

### Generated Exports

- data_works_json: `211`
- data_software_json: `147`
- data_publications_ld_main_entity: `211`
- data_software_ld_main_entity: `147`

### GitHub Inventory

- total: `245`
- docxology: `202`
- ActiveInferenceInstitute: `43`
- curated: `147`
- uncataloged: `98`
- forks: `87`
- archived: `5`
- public: `245`
- private: `0`
- recently_updated: `182`
- primary_total: `158`
- primary_docxology: `117`
- primary_ActiveInferenceInstitute: `41`
- fork_docxology: `85`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `202`
- GitHub user ActiveInferenceInstitute: `43`
- ORCID work groups: `20`
- PubMed exact author records: `8`
- Europe PMC exact author records: `10`
- Crossref ORCID DOI records: `15`
- Zenodo exact-name creator records: `59`
- Zenodo ORCID-linked records: `145`

### Paired Publications

- github_releases: `229`
- zenodo_records: `150`
- pairs: `449`
- strong_pairs: `48`
- already_reviewed: `399`
- needs_review: `3`
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
