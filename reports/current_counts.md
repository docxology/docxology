# Current Counts Report

Generated: `2026-07-10T19:58:03+00:00`

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
- paired_publications: `reports/paired_publications_2026-07-10.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `192`
- Paper-folder docs: `175`
- Bibliography docs links: `175`

### Types

- Books: `5`
- Courses: `3`
- Papers: `171`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `41`
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

- data_works_json: `192`
- data_software_json: `95`
- data_publications_ld_main_entity: `192`
- data_software_ld_main_entity: `95`

### GitHub Inventory

- total: `378`
- docxology: `340`
- ActiveInferenceInstitute: `38`
- curated: `92`
- uncataloged: `286`
- forks: `241`
- archived: `0`
- public: `378`
- private: `0`
- recently_updated: `120`
- primary_total: `137`
- primary_docxology: `101`
- primary_ActiveInferenceInstitute: `36`
- fork_docxology: `239`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `340`
- GitHub user ActiveInferenceInstitute: `38`
- ORCID work groups: `20`
- PubMed exact author records: `8`

### Paired Publications

- github_releases: `174`
- zenodo_records: `121`
- pairs: `332`
- strong_pairs: `39`
- already_reviewed: `0`
- needs_review: `293`
- create_new: `2`
- update_existing: `37`

### Paired Publication Decisions

- decision: `accept`
- groups: `24`
- raw_candidates: `86`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `cd code/tests && PYTHONDONTWRITEBYTECODE=1 uv run pytest -q`
