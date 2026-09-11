# Current Counts Report

Generated: `2026-09-11T19:11:19+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-09-11.json`
- paired_publications: `reports/paired_publications_2026-09-11.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `214`
- Paper-folder docs: `197`
- Full-text extractions: `190`
- Papers with image galleries: `139`
- Total extracted images: `8944`
- Bibliography docs links: `197`

### Types

- Books: `5`
- Courses: `3`
- Papers: `192`
- Playbooks: `2`
- Presentations: `9`
- Report: `1`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `45`
- Cognitive Security: `37`
- Art & Synergetics: `16`
- Computational: `56`
- AII Ecosystem: `6`
- Presentations & Media: `15`
- Genetics & Biomedical: `15`

### Software

- docxology_owned: `110`
- active_inference_institute: `39`
- curated_total: `149`

### Generated Exports

- data_works_json: `214`
- data_software_json: `149`
- data_publications_ld_main_entity: `214`
- data_software_ld_main_entity: `149`

### GitHub Inventory

- total: `256`
- docxology: `213`
- ActiveInferenceInstitute: `43`
- curated: `149`
- uncataloged: `107`
- forks: `89`
- archived: `5`
- public: `256`
- private: `0`
- recently_updated: `194`
- primary_total: `167`
- primary_docxology: `126`
- primary_ActiveInferenceInstitute: `41`
- fork_docxology: `87`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `214`
- GitHub user ActiveInferenceInstitute: `43`
- ORCID work groups: `20`
- PubMed exact author records: `8`
- Europe PMC exact author records: `10`
- Crossref ORCID DOI records: `15`
- Zenodo exact-name creator records: `65`
- Zenodo ORCID-linked records: `153`

### Paired Publications

- github_releases: `240`
- zenodo_records: `156`
- pairs: `463`
- strong_pairs: `52`
- already_reviewed: `413`
- needs_review: `0`
- create_new: `1`
- update_existing: `49`

### Paired Publication Decisions

- decision: `accept`
- groups: `81`
- raw_candidates: `508`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows. R26-R27 record CogSecSkills and Codomyrmex version-history decisions under already-cited DOIs. R71 records the untagged Codomyrmex v1.3.0 release as already represented, and R72 records Active Fedference v1.0.4 as a version-specific artifact under its existing concept DOI without a duplicate bibliography row. R73 records the re-fingerprinted untagged Codomyrmex v1.3.0 release from the 2026-09-04 report as superseded under R71 precedent, and R74 records GNN v3.2.0 as a version-specific release of its represented work. R75-R76 record the rotating Codomyrmex draft URLs as superseded under R71/R73 precedent, and R77-R78 record the ActiveInferAnts and CEREBRUM releases as version-specific artifacts under the represented Cognitive Integrity Framework DOI after the principal classified cognitive_integrity as curated. R79 records the Cognitive Diagrams v2.5.0 release (2026-09-10 scan) as version-history-only under the already-cited concept DOI 10.5281/zenodo.19695259. R80 records the six GitHub release pairs (v0.3.0-v1) under the canonical curated EvoJump concept 10.5281/zenodo.22664675 as software-catalog (SOFTWARE.md already lists EvoJump; the citable paper remains bibliography row #12, concept 10.5281/zenodo.17229924), and R81 records the GitHub-Zenodo automated integration archive concept 10.5281/zenodo.22664645 (docxology/EvoJump-v0.5.2.zip, zip-only) as a superseded duplicate deposit.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q`
