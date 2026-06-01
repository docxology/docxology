# Public-Source Reconciliation Report

Generated: 2026-05-30T18:40:20.762085+00:00

Snapshot: [`reports/public_source_snapshot_2026-05-30.json`](public_source_snapshot_2026-05-30.json)

This report compares curated local counts against public authority/source indexes. Differences are expected unless the relationship says otherwise.

| Comparison | Local | Public | Relationship | Interpretation |
| --- | ---: | ---: | --- | --- |
| Curated bibliography vs ORCID work groups | 150 | 20 | not expected to match | The local bibliography intentionally includes presentations, courses, books, software-linked works, and local documentation. ORCID groups external works by identifier/version. |
| Curated bibliography vs PubMed exact author records | 150 | 8 | subset | PubMed only covers biomedical/indexed literature and is a strict subset of the curated bibliography. |
| Curated bibliography vs Crossref ORCID DOI records | 150 | 15 | subset | Crossref captures DOI records attached to the ORCID; Zenodo, books, courses, and non-DOI works may be absent or represented elsewhere. |
| Curated bibliography vs Zenodo ORCID-linked records | 150 | 93 | overlapping sets | Zenodo includes versioned records and software archives; the local bibliography normalizes selected works into one curated table. |
| Catalogued docxology software vs GitHub public repository count | 50 | 300 | curated subset | SOFTWARE.md intentionally catalogs selected owned repositories; GitHub counts all public repositories including forks and uncatalogued experiments. |
| Catalogued AII contributions vs AII GitHub public repository count | 32 | 51 | curated subset | SOFTWARE.md lists AII repositories with docxology contributions, not every public AII repository. |

## Maintenance Use

- Use this report to decide whether a public-source change requires curated copy updates.
- Do not automatically overwrite curated counts when public indexes have different scope.
- Re-run `code/orchestrators/refresh_public_sources.py` before updating this report.
