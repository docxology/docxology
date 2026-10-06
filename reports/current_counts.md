# Current Counts Report

Generated: `2026-10-05T22:43:25+00:00`

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
- public_source_snapshot: `reports/public_source_snapshot_2026-09-30.json`
- paired_publications: `reports/paired_publications_2026-09-24.json`
- paired_publication_decisions: `data/paired-publication-decisions.json`

## Counts

- Bibliography works: `220`
- Paper-folder docs: `203`
- Full-text extractions: `199`
- Papers with image galleries: `145`
- Total extracted images: `8959`
- Bibliography docs links: `203`

### Types

- Books: `5`
- Courses: `3`
- Papers: `199`
- Playbooks: `2`
- Presentations: `8`
- Report: `1`
- Series: `2`

### Domains

- Entomology: `23`
- Active Inference: `47`
- Cognitive Security: `37`
- Art & Synergetics: `16`
- Computational: `63`
- AII Ecosystem: `6`
- Presentations & Media: `14`
- Genetics & Biomedical: `13`

### Software

- docxology_owned: `120`
- active_inference_institute: `39`
- curated_total: `159`

### Generated Exports

- data_works_json: `220`
- data_software_json: `159`
- data_publications_ld_main_entity: `220`
- data_software_ld_main_entity: `159`

### GitHub Inventory

- total: `267`
- docxology: `224`
- ActiveInferenceInstitute: `43`
- curated: `153`
- uncataloged: `114`
- forks: `97`
- archived: `5`
- public: `267`
- private: `0`
- recently_updated: `207`
- primary_total: `170`
- primary_docxology: `129`
- primary_ActiveInferenceInstitute: `41`
- fork_docxology: `95`
- fork_ActiveInferenceInstitute: `2`

### Public Source Snapshot

- GitHub user docxology: `230`
- GitHub user ActiveInferenceInstitute: `44`
- ORCID work groups: `20`
- PubMed exact author records: `8`
- Europe PMC exact author records: `10`
- Crossref ORCID DOI records: `15`
- Zenodo exact-name creator records: `71`
- Zenodo ORCID-linked records: `159`

### Paired Publications

- github_releases: `254`
- zenodo_records: `162`
- pairs: `470`
- strong_pairs: `57`
- already_reviewed: `415`
- needs_review: `0`
- create_new: `0`
- update_existing: `55`

### Paired Publication Decisions

- decision: `accept`
- groups: `88`
- raw_candidates: `524`
- note: `Manual review decisions accept represented GitHub release + Zenodo record relations; software-only records remain software/version metadata unless a bibliography folder is explicitly curated. R20-R24 record CEREBRUM, SIA, and On-Policy Distillation supersession/version-history decisions so newer versions do not create duplicate bibliography rows. R26-R27 record CogSecSkills and Codomyrmex version-history decisions under already-cited DOIs. R71 records the untagged Codomyrmex v1.3.0 release as already represented, and R72 records Active Fedference v1.0.4 as a version-specific artifact under its existing concept DOI without a duplicate bibliography row. R73 records the re-fingerprinted untagged Codomyrmex v1.3.0 release from the 2026-09-04 report as superseded under R71 precedent, and R74 records GNN v3.2.0 as a version-specific release of its represented work. R75-R76 record the rotating Codomyrmex draft URLs as superseded under R71/R73 precedent, and R77-R78 record the ActiveInferAnts and CEREBRUM releases as version-specific artifacts under the represented Cognitive Integrity Framework DOI after the principal classified cognitive_integrity as curated. R79 records the Cognitive Diagrams v2.5.0 release (2026-09-10 scan) as version-history-only under the already-cited concept DOI 10.5281/zenodo.19695259. R80 records the six GitHub release pairs (v0.3.0-v1) under the canonical curated EvoJump concept 10.5281/zenodo.22664675 as software-catalog (SOFTWARE.md already lists EvoJump; the citable paper remains bibliography row #12, concept 10.5281/zenodo.17229924), and R81 records the GitHub-Zenodo automated integration archive concept 10.5281/zenodo.22664645 (docxology/EvoJump-v0.5.2.zip, zip-only) as a superseded duplicate deposit. R82-R83 (2026-09-17 scan) record the fep_lean v1.2.0 and GeneralizedNotationNotation v3.4.0 releases as version-history-only under their already-cited citation DOIs (10.5281/zenodo.19699233 row #113 and 10.5281/zenodo.7803313 row #168), both pairs lacking github_release_mentions_doi cross-link evidence, so neither creates a duplicate bibliography row.`

## Validation

- `uv run python3 code/orchestrators/validate_repo.py`
- `PYTHONDONTWRITEBYTECODE=1 uv run python3 -m pytest code/tests -q`
