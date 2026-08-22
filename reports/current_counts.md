# Current Counts Report

Generated: `2026-08-22T20:39:33+00:00`

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
- paired_publications: `reports/paired_publications_2026-08-10.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `209`
- Paper-folder docs: `192`
- Full-text extractions: `171`
- Papers with image galleries: `139`
- Total extracted images: `8944`
- Bibliography docs links: `192`

### Types

- Books: `5`
- Courses: `3`
- Papers: `188`
- Playbooks: `2`
- Presentations: `9`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `45`
- Cognitive Security: `35`
- Art & Synergetics: `16`
- Computational: `54`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `105`
- active_inference_institute: `41`
- curated_total: `146`

### Generated Exports

- data_works_json: `209`
- data_software_json: `146`
- data_publications_ld_main_entity: `209`
- data_software_ld_main_entity: `146`

### GitHub Inventory

- total: `244`
- docxology: `201`
- ActiveInferenceInstitute: `43`
- curated: `143`
- uncataloged: `101`
- forks: `87`
- archived: `0`
- public: `244`
- private: `0`
- recently_updated: `147`
- primary_total: `157`
- primary_docxology: `116`
- primary_ActiveInferenceInstitute: `41`
- fork_docxology: `85`
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

- github_releases: `221`
- zenodo_records: `147`
- pairs: `418`
- strong_pairs: `46`
- already_reviewed: `28`
- needs_review: `345`
- create_new: `0`
- update_existing: `45`

### Paired Publication Decisions

- decision: `accept`
- groups: `27`
- raw_candidates: `114`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows. R26-R27 record CogSecSkills (9 release pairs) and Codomyrmex (18 release pairs) supersession/version-history decisions under already-cited DOIs so versioned GitHub releases do not create duplicate bibliography rows.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q`
