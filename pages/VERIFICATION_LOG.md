---
title: Verification Log
description: Dated independent multi-source verification of the docxology profile's load-bearing claims.
nav: ["Home](../README.md)", "Evidence](EVIDENCE.md)", "Cite & Verify](CITE_VERIFY.md)", "Discovery](DISCOVERY.md)"]
---

# Verification Log

> Primary-source verification and explicitly labeled review of the load-bearing claims on this profile.
> Each row identifies whether it rests on an independent record, a first-party record,
> a direct authenticated observation, or principal confirmation. This page is the
> human-readable companion to [`data/verification-log.json`](../data/verification-log.json)
> and backs the claims ledger in [`pages/EVIDENCE.md`](EVIDENCE.md).
>
> **Method note:** "direct dual-fetch" = two separate non-cached retrievals on the
> stated date returned the same value. "First-party only" = the cited page is
> authoritative for the fact but no source independent of it corroborates the
> specific identifier.

## 2026-08-26 — Review-gated primary-source refresh

| Claim | Verdict | Primary source | Notes |
|-------|---------|----------------|-------|
| Google Scholar metrics | **Verified, dated** | [canonical Scholar profile `DXjPFtYAAAAJ`](https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en) | Direct authenticated observation: **815 citations, h-index 14, i10-index 16**. Bound to the current snapshot by [`data/scholar-verification-receipt.json`](../data/scholar-verification-receipt.json). |
| Stanford PhD (Biology, 2019; advisor Deborah Gordon) | **Verified [HIGH]** | [Stanford MODS record `pb813wm1484`](https://purl.stanford.edu/pb813wm1484.mods) | Confirms Daniel Ari Friedman, Stanford Biology, a 2019 PhD thesis, and Deborah M. Gordon as degree supervisor. |
| NSF Postdoctoral Fellowship | **Verified [HIGH]** | [NSF award `DBI-2010290`](https://api.nsf.gov/services/v1/awards/2010290.json) | Official award dates: 2020-10-01 to 2023-09-30; UC Davis performance location and named co-training arrangement. |
| AII current officers and governance | **First-party + IRS** | [AII officers](https://activeinference.institute/structure/officers/); [ProPublica IRS record](https://projects.propublica.org/nonprofits/organizations/882985125) | Friedman is President & Treasurer; Mikhailova is Vice President & Secretary. AII remains 501(c)(3), EIN 88-2985125. Historic Knight office dates were not reverified. |
| AII current board | **First-party current** | [Board of Directors](https://activeinference.institute/structure/board-of-directors/) | **11 current members**. |
| AII current Scientific Advisory Board | **First-party current** | [Scientific Advisory Board](https://activeinference.institute/structure/scientific-advisory-board/) | **32 current members**; 31 link to public pages. |
| AII Textbook Group | **First-party current** | [Textbook Group](https://activeinference.institute/projects/textbook-group/) | Nine completed cohorts on the 2022 textbook plus a first 2026 Fundamentals cohort currently live. |
| COGSEC research context | **Public-source** | [PubMed PMID 38735269](https://pubmed.ncbi.nlm.nih.gov/38735269/); [COGSEC R&D](https://www.cogsec.org/r-d-initiatives-3) | Supports the existing cautious research/publication-context claim without adding a personal title. |
| Curio Cards 24–26 | **First-party current** | [Curio artist documentation](https://docs.curio.cards/the-artists/daniel-friedman); [Curio project documentation](https://docs.curio.cards/) | Friedman created cards 24–26. The collection debuted May 9, 2017; original cards were minted during 2017. |
| Christie's Curio sale | **First-party only** | [Christie's guide](https://www.christies.com/en/stories/a-to-z-nft-collecting-guide-b9f875b864c7488eb094595ced7d60cd) | Full set plus 17b, seven artists: New York, September 30, 2021, 393 ETH / $1,202,108. |
| ORCID and secondary Scholar link | **Verified [HIGH]** | [ORCID public person record](https://pub.orcid.org/v3.0/0000-0001-6232-9096/person) | Confirms ORCID 0000-0001-6232-9096 and the secondary Scholar link; the canonical metrics profile is a local policy backed by the authenticated Scholar receipt. |
| College of the Redwoods teaching | **Principal-confirmed** | [BIOL-1](https://github.com/docxology/biol-1); [BIOL-8](https://github.com/docxology/biol-8) | BIOL-1 at Pelican Bay in Spring and Fall 2026; BIOL-8 in Spring 2026. This is an instructor-of-record update, not a public-schedule assertion. |

## 2026-06-09 — Public-source refresh for discovery and generated reports

| Claim | Verdict | Primary source (independent) | Notes |
|-------|---------|------------------------------|-------|
| GitHub footprint | **Verified [HIGH]** | [api.github.com/users/docxology](https://api.github.com/users/docxology); [/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute) | docxology = **307** public repos; AII = **52** as of 2026-06-09. `ActiveInferenceInstitute` remains a **User** account, not an Organization (`/orgs/` 404s). |
| Publication index freshness | **Verified, dated** | [`reports/public_source_snapshot_2026-06-09.json`](../reports/public_source_snapshot_2026-06-09.json); [`reports/public_source_inventory_2026-06-09.json`](../reports/public_source_inventory_2026-06-09.json) | PubMed exact-author = 8; Europe PMC exact-author = 10; Crossref ORCID DOI records = 15; Zenodo exact-name = **40**; Zenodo ORCID-linked = **98**. Public API counts are freshness checks and include versioned/software records, not a replacement for the curated 154-row bibliography. |

## 2026-06-07 — Public-source refresh for discovery and generated reports

| Claim | Verdict | Primary source (independent) | Notes |
|-------|---------|------------------------------|-------|
| GitHub footprint | **Verified [HIGH]** | [api.github.com/users/docxology](https://api.github.com/users/docxology); [/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute) | docxology = **306** public repos; AII = **51** as of 2026-06-07. `ActiveInferenceInstitute` remains a **User** account, not an Organization (`/orgs/` 404s). |
| Publication index freshness | **Verified, dated** | [`reports/public_source_snapshot_2026-06-07.json`](../reports/public_source_snapshot_2026-06-07.json); [`reports/public_source_inventory_2026-06-07.json`](../reports/public_source_inventory_2026-06-07.json) | PubMed exact-author = 8; Europe PMC exact-author = 10; Crossref ORCID DOI records = 15; Zenodo exact-name = **40**; Zenodo ORCID-linked = **98**. Public API counts are freshness checks and include versioned/software records, not a replacement for the curated 154-row bibliography. |

## 2026-06-04 — Targeted API refresh for publication/software counts

| Claim | Verdict | Primary source (independent) | Notes |
|-------|---------|------------------------------|-------|
| GitHub footprint | **Verified [HIGH]** | [api.github.com/users/docxology](https://api.github.com/users/docxology); [/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute) | docxology = **305** public repos; AII = **51** as of 2026-06-04. `ActiveInferenceInstitute` remains a **User** account, not an Organization (`/orgs/` 404s). |
| Publication index freshness | **Verified, dated** | [`reports/public_source_snapshot_2026-06-04.json`](../reports/public_source_snapshot_2026-06-04.json); [`reports/public_source_inventory_2026-06-04.json`](../reports/public_source_inventory_2026-06-04.json) | PubMed exact-author = 8; Europe PMC exact-author = 10; Crossref ORCID DOI records = 15; Zenodo exact-name = **40**; Zenodo ORCID-linked = **98**. Public API counts are freshness checks and include versioned/software records, not a replacement for the curated 154-row bibliography. |

## 2026-05-16 — Independent verification pass

| Claim | Verdict | Primary source (independent) | Notes |
|-------|---------|------------------------------|-------|
| Google Scholar metrics | **Verified, dated** | [scholar.google.com profile `DXjPFtYAAAAJ`](https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en) | Direct dual-fetch 2026-05-16: **764 citations, h-index 15, i10-index 17**. Recorded in [`data/scholar-snapshot.json`](../data/scholar-snapshot.json). Supersedes the prior manually-frozen 812. |
| Stanford PhD (Ecology & Evolution, 2019; advisor Deborah Gordon) | **Verified [HIGH]** | [Stanford PURL `pb813wm1484`](https://purl.stanford.edu/pb813wm1484); [Gordon Lab publications](https://web.stanford.edu/~dmgordon/publications.html) | Year, department, and advisor independently corroborated; Gordon lab lists 7 co-authored papers. |
| NSF Postdoctoral Research Fellowship | **Historical 2026-05-16 pass; superseded for current wording** | [Grantome — NSF award `DBI-2010290`](https://grantome.com/grant/NSF/DBI-2010290) | See the 2026-08-26 primary-source refresh for the current official NSF award dates (2020-10-01 to 2023-09-30); this historical row is retained as a dated audit record. |
| AII 501(c)(3) status | **Verified [HIGH]** | [ProPublica Nonprofit Explorer — EIN 88-2985125](https://projects.propublica.org/nonprofits/organizations/882985125) | IRS data (independent of self-published pages): 501(c)(3) public charity, ruling **March 2024**. |
| AII officer roles | **Historical 2026-05-16 pass; superseded for current wording** | [activeinference.institute/structure/officers](https://activeinference.institute/structure/officers/); ProPublica filer-of-record | See the 2026-08-26 first-party refresh for current officer roles; this historical row is retained without reasserting historic office dates as current-source facts. |
| Karl Friston co-authorship | **Verified [HIGH]** | [Frontiers DOI 10.3389/fnbeh.2021.647732](https://www.frontiersin.org/journals/behavioral-neuroscience/articles/10.3389/fnbeh.2021.647732/full); [PubMed 34248515](https://pubmed.ncbi.nlm.nih.gov/34248515/) | "Active Inferants" — peer-reviewed, Friston a named co-author. |
| Publication record (6-DOI sample) | **Verified [HIGH]** | doi.org / Crossref / PubMed / Europe PMC | All 6 sampled DOIs resolve and confirm Friedman authorship (first author on 4). Zenodo: 38 exact-name / 91 ORCID-linked as of 2026-05-28; superseded for current count surfaces by the 2026-06-04 API refresh above. |
| Curio Cards artist (cards 24–26) | **Historical 2026-05-16 pass; superseded for current wording** | [Curio Cards docs](https://docs.curio.cards/the-artists/daniel-friedman); [Wikipedia](https://en.wikipedia.org/wiki/Curio_Cards); [Amy Castor (independent NFT history)](https://amycastor.com/2022/06/04/the-early-history-of-nfts-curio-cards/) | See the 2026-08-26 first-party refresh: the collection debuted May 9, 2017 and original cards were minted during 2017; Christie's states September 30, 2021 for its New York sale. |
| Christie's lot number `6337619` | **First-party only** | [christies.com/en/lot/lot-6337619](https://www.christies.com/en/lot/lot-6337619) | URL resolves (HTTP 200); Christie's own page matches the exact Curio set. The specific lot **number** is not corroborated by any source independent of Christie's — present as a Christie's reference, not an independently verified identifier. |
| Identity graph (ORCID hub, Wikidata, dblp, Semantic Scholar) | **Verified [HIGH]** | [ORCID 0000-0001-6232-9096](https://orcid.org/0000-0001-6232-9096); [Wikidata Q138781444](https://www.wikidata.org/wiki/Q138781444) / [Q139600792](https://www.wikidata.org/wiki/Q139600792) | All 21 audited identity nodes resolve to one entity. Exposure scoped to professional/artistic identity; no home address, phone, DOB, or personal email exposed. A secondary Scholar ID (`Y2bMf3MAAAAJ`) is linked from ORCID — disambiguate. |
| GitHub footprint | **Verified [HIGH]** | [api.github.com/users/docxology](https://api.github.com/users/docxology); [/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute) | docxology = 299 public repos; AII = 51 as of 2026-05-28; superseded for current count surfaces by the 2026-06-04 API refresh above. `ActiveInferenceInstitute` is a **User** account, not an Organization (`/orgs/` 404s). |
| College of the Redwoods Spring-2026 teaching | **Principal-confirmed** | [github.com/docxology/biol-1](https://github.com/docxology/biol-1), [biol-8](https://github.com/docxology/biol-8) | BIOL-1 (General Biology, Pelican Bay) and BIOL-8 (Human Biology), Spring 2026. Confirmed by the principal as instructor of record; a future-term CR WebAdvisor public schedule may not yet list it. Retained verbatim. |

## Items intentionally softened (precision hygiene)

- **"107 indexed publications"** — not derivable from the primary Scholar profile; replaced with "Scholar-indexed publications" (the specific count was unverifiable).
- **SAB announcement/count wording** — the historical 2026-05-16 count is superseded by the 2026-08-26 first-party refresh, which lists 32 current members; no independent source confirms a specific announcement month.
- **Taschen *On NFTs* individual inclusion** — the book exists; individual inclusion is self-reported and carries an evidence caveat in the claims ledger (bibliography entry retained).
- **codomyrmex counts** — synced to the repo's own authoritative source (`MODULES.md` / `README` / `inventory.md` = 128 modules, 600 MCP tools); the GitHub repo *description* (127 / 424) is stale.

---

*Maintained alongside [`data/verification-log.json`](../data/verification-log.json). Update both together when a claim is re-verified; record the verification date and whether the evidence is independent, first-party, direct-authenticated, or principal-confirmed.*
