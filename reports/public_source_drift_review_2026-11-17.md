# Public-source drift review — 2026-11-17

Resolves the normalized observation drift reported in docxology/docxology#76 against the November 6 baseline. The November 17 snapshot contains 21 successful primary endpoint checks. All older snapshots are retained.

The fresh GitHub account observation and complete inventory agree on 269 public docxology repositories and 47 ActiveInferenceInstitute repositories. The prior checked-in complete inventory already contained 268 docxology repositories; the new public hybrid-aif fork is retained as fork_not_curated under TODO.md DOC-005, with immutable GitHub identities in data/repository-exclusions.json. No curated software row is added.

Zenodo exact-name query results changed from 85 to 100; ORCID-linked results changed from 174 to 188. Each query contains 16 added editions; their union contains 17. The prior GNN edition 23902909 was replaced in both queries; Observers edition 23719196 was also replaced in the ORCID query. Primary record APIs bind every added edition to an already-curated concept:

| Observed edition DOI | Existing concept DOI | Primary source |
| --- | --- | --- |
| 10.5281/zenodo.24092899 | 10.5281/zenodo.24061758 | [Zenodo record](https://zenodo.org/api/records/24092899) |
| 10.5281/zenodo.24094526 | 10.5281/zenodo.17114383 | [Zenodo record](https://zenodo.org/api/records/24094526) |
| 10.5281/zenodo.24094527 | 10.5281/zenodo.16887790 | [Zenodo record](https://zenodo.org/api/records/24094527) |
| 10.5281/zenodo.24094530 | 10.5281/zenodo.16887767 | [Zenodo record](https://zenodo.org/api/records/24094530) |
| 10.5281/zenodo.24124416 | 10.5281/zenodo.24069414 | [Zenodo record](https://zenodo.org/api/records/24124416) |
| 10.5281/zenodo.24124417 | 10.5281/zenodo.24069423 | [Zenodo record](https://zenodo.org/api/records/24124417) |
| 10.5281/zenodo.24124418 | 10.5281/zenodo.24069450 | [Zenodo record](https://zenodo.org/api/records/24124418) |
| 10.5281/zenodo.24124419 | 10.5281/zenodo.24069456 | [Zenodo record](https://zenodo.org/api/records/24124419) |
| 10.5281/zenodo.24124420 | 10.5281/zenodo.24069255 | [Zenodo record](https://zenodo.org/api/records/24124420) |
| 10.5281/zenodo.24124421 | 10.5281/zenodo.24069474 | [Zenodo record](https://zenodo.org/api/records/24124421) |
| 10.5281/zenodo.24124425 | 10.5281/zenodo.24069438 | [Zenodo record](https://zenodo.org/api/records/24124425) |
| 10.5281/zenodo.24124428 | 10.5281/zenodo.24069487 | [Zenodo record](https://zenodo.org/api/records/24124428) |
| 10.5281/zenodo.24124429 | 10.5281/zenodo.24069433 | [Zenodo record](https://zenodo.org/api/records/24124429) |
| 10.5281/zenodo.24147321 | 10.5281/zenodo.24062584 | [Zenodo record](https://zenodo.org/api/records/24147321) |
| 10.5281/zenodo.24147945 | 10.5281/zenodo.24034464 | [Zenodo record](https://zenodo.org/api/records/24147945) |
| 10.5281/zenodo.24151588 | 10.5281/zenodo.18288113 | [Zenodo record](https://zenodo.org/api/records/24151588) |
| 10.5281/zenodo.24167564 | 10.5281/zenodo.7803313 | [Zenodo record](https://zenodo.org/api/records/24167564) |

These observations require no new bibliography row or canonical DOI change. Public query totals include software and editions and are not bibliography work counts. Twelve raw observation decisions were replaced in place with hashes from the exact November 6/November 17 comparison; account/repository activity and star changes are acknowledged separately from the three normalized drift labels.

The refreshed broad source inventory retains the same five explicit unavailable-profile sections as the baseline (DBLP, ResearchGate, SciProfiles, PhilPeople and Semantic Scholar). These failures are not interpreted as missing works or grounds to alter claims. No new Scholar observation was made; existing verified metrics are preserved. The advisory-board count, the pre-existing docxology/.github catalog-classification item, and the older GitHub–Zenodo pairing report remain explicit deferred items in the generated review. None changes the three normalized drift observations reviewed for issue #76.

Evidence: reports/public_source_snapshot_2026-11-17.json, reports/public_source_inventory_2026-11-17.json, and the paired public_source_review_2026-11-17.json / .md records. The scheduled November 16 artifact was inspected but not adopted as the new baseline because its GitHub count predates hybrid-aif becoming public.
