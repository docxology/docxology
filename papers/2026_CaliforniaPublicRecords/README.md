<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🛡️ California Public Records: A Technical and Legal Reference for the Post-AB 473 Era

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20789899-blue)](https://doi.org/10.5281/zenodo.20789899)

---

## Abstract

> A technical and legal reference to California public-records ecosystem, anchored by the CPRA recodified by AB 473.

## Keywords

`California Public Records Act` · `open data` · `CKAN` · `Socrata` · `ArcGIS` · `cognitive security` · `civic technology`

## Methods

- **Registry-first compilation of CPRA statutes, portals, exemptions and datasets** — Held every cited section number, portal URL, schema field and dataset in Python registries under src/, with prose counts resolved from them at build time.
- **Standard-library Python clients for California API surfaces** — Wrote working clients for CKAN Action API, Socrata SoQL, ArcGIS GeoServices REST, CIMIS REST, OpenJustice CSV and LegiScan endpoints.
- **Metadata-schema validators (DCAT, CKAN, Dublin Core, RIPA stop data)** — Implemented schema validators that accept a mapping and return a report of missing fields and warnings.
- **Offline no-mocks test suite with optional live endpoint checks** — Validated registries, clients and schemas against a real local HTTP server, plus optional live checks against California open-data endpoints.
- **Cross-vendor citation verification (leginfo, Justia, FindLaw)** — Source-verified statute citations against leginfo and re-confirmed selected ones via Justia and FindLaw, removing those that could not be verified.

## Key Findings

- The reference compiles California's public-records ecosystem into a machine-readable artifact: 22 CPRA statute sections, 17 portals, 7 exemption clusters and an 8-dataset OpenJustice taxonomy.
- It notes that the AB 473 recodification made no substantive changes to disclosure rights but split the exemption list into independent code sections for readability.
- Top-line verdict is 'CERTIFY-WITH-RESIDUALS': four CPRA sections from the upstream research document were misattributed or unverifiable and deliberately omitted.
- A scaffolded citation-laundering example was rejected: § 7928.200 does not govern peace-officer records, so that mandate is pinned to Penal Code § 832.7.
- The package's generator methods are pure functions of the registries, so re-running them yields byte-identical output apart from a single provenance timestamp.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.20789899](https://doi.org/10.5281/zenodo.20789899)
- Artifact DOI: [10.5281/zenodo.20789916](https://doi.org/10.5281/zenodo.20789916)
- Zenodo record: [https://zenodo.org/records/20789916](https://zenodo.org/records/20789916)
- PDF: [Friedman_2026_California_8f09eac2.pdf](Friedman_2026_California_8f09eac2.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20789916)

## Citation

> Daniel Ari Friedman (2026). *California Public Records: A Technical and Legal Reference for the Post-AB 473 Era*. Zenodo. DOI: 10.5281/zenodo.20789899. URL: https://doi.org/10.5281/zenodo.20789899.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
