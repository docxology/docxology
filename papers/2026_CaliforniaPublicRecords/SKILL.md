---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "California Public Records: A Technical and Legal Reference for the Post-AB 473 Era"
description: "A technical and legal reference to California public-records ecosystem, anchored by the CPRA recodified by AB 473."
tags: ["california-public-records-act", "open-data", "ckan", "socrata", "arcgis", "cognitive-security", "civic-technology"]
domain: "Cognitive Security"
citation: "Daniel Ari Friedman (2026). *California Public Records: A Technical and Legal Reference for the Post-AB 473 Era*. Zenodo."
doi: "10.5281/zenodo.20789899"
artifact_doi: "10.5281/zenodo.20789916"
---

# California Public Records: A Technical and Legal Reference for the Post-AB 473 Era

**Daniel Ari Friedman** (2026) · Cognitive Security

## Context

This work addresses topics in **Cognitive Security**: California Public Records Act, open data, CKAN, Socrata.

## Methods

Primary methods and techniques applied in this work:

- **Registry-first compilation of CPRA statutes, portals, exemptions and datasets** — Held every cited section number, portal URL, schema field and dataset in Python registries under src/, with prose counts resolved from them at build time.
- **Standard-library Python clients for California API surfaces** — Wrote working clients for CKAN Action API, Socrata SoQL, ArcGIS GeoServices REST, CIMIS REST, OpenJustice CSV and LegiScan endpoints.
- **Metadata-schema validators (DCAT, CKAN, Dublin Core, RIPA stop data)** — Implemented schema validators that accept a mapping and return a report of missing fields and warnings.
- **Offline no-mocks test suite with optional live endpoint checks** — Validated registries, clients and schemas against a real local HTTP server, plus optional live checks against California open-data endpoints.
- **Cross-vendor citation verification (leginfo, Justia, FindLaw)** — Source-verified statute citations against leginfo and re-confirmed selected ones via Justia and FindLaw, removing those that could not be verified.

## Key Findings

Core contributions and results:

- The reference compiles California's public-records ecosystem into a machine-readable artifact: 22 CPRA statute sections, 17 portals, 7 exemption clusters and an 8-dataset OpenJustice taxonomy.
- It notes that the AB 473 recodification made no substantive changes to disclosure rights but split the exemption list into independent code sections for readability.
- Top-line verdict is 'CERTIFY-WITH-RESIDUALS': four CPRA sections from the upstream research document were misattributed or unverifiable and deliberately omitted.
- A scaffolded citation-laundering example was rejected: § 7928.200 does not govern peace-officer records, so that mandate is pinned to Penal Code § 832.7.
- The package's generator methods are pure functions of the registries, so re-running them yields byte-identical output apart from a single provenance timestamp.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2020_EmergentTeams](../2020_EmergentTeams/)
- [2020_FacilitatorsCatechism](../2020_FacilitatorsCatechism/)
- [2020_GreatPreset](../2020_GreatPreset/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20789899
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-21T00:00:00Z
- Artifact DOI: 10.5281/zenodo.20789916

## Prerequisites

- Familiarity with California Public Records Act, open data, CKAN
- Background in Cognitive Security fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20789899`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
