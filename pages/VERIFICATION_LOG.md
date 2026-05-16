---
title: Verification Log
description: Dated independent multi-source verification of the docxology profile's load-bearing claims.
nav: ["Home](../README.md)", "Evidence](EVIDENCE.md)", "Cite & Verify](CITE_VERIFY.md)", "Discovery](DISCOVERY.md)"]
---

# Verification Log

> Independent, primary-source verification of the load-bearing claims on this profile.
> Each row was checked against a source **not controlled by Daniel Ari Friedman**
> (publisher DOI resolvers, IRS data via ProPublica, NSF/Grantome, Stanford PURL,
> ORCID, Wikipedia, independent NFT-history journalism, GitHub API). This page is
> the human-readable companion to [`data/verification-log.json`](../data/verification-log.json)
> and backs the claims ledger in [`pages/EVIDENCE.md`](EVIDENCE.md).
>
> **Method note:** "direct dual-fetch" = two separate non-cached retrievals on the
> stated date returned the same value. "First-party only" = the cited page is
> authoritative for the fact but no source independent of it corroborates the
> specific identifier.

## 2026-05-16 — Independent verification pass

| Claim | Verdict | Primary source (independent) | Notes |
|-------|---------|------------------------------|-------|
| Google Scholar metrics | **Verified, dated** | [scholar.google.com profile `DXjPFtYAAAAJ`](https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en) | Direct dual-fetch 2026-05-16: **764 citations, h-index 15, i10-index 17**. Recorded in [`data/scholar-snapshot.json`](../data/scholar-snapshot.json). Supersedes the prior manually-frozen 812. |
| Stanford PhD (Ecology & Evolution, 2019; advisor Deborah Gordon) | **Verified [HIGH]** | [Stanford PURL `pb813wm1484`](https://purl.stanford.edu/pb813wm1484); [Gordon Lab publications](https://web.stanford.edu/~dmgordon/publications.html) | Year, department, and advisor independently corroborated; Gordon lab lists 7 co-authored papers. |
| NSF Postdoctoral Research Fellowship | **Verified [HIGH]** | [Grantome — NSF award `DBI-2010290`](https://grantome.com/grant/NSF/DBI-2010290) | NSF PRFB FY2020, $138,000, Davis CA. Budget period 2020–2022; 2023 is a no-cost-extension affiliation (ORCID UC Davis 2019–2023), not on the funding record. |
| AII 501(c)(3) status | **Verified [HIGH]** | [ProPublica Nonprofit Explorer — EIN 88-2985125](https://projects.propublica.org/nonprofits/organizations/882985125) | IRS data (independent of self-published pages): 501(c)(3) public charity, ruling **March 2024**. |
| AII officer roles | **Verified [HIGH]** | [activeinference.institute/officers](https://www.activeinference.institute/officers); ProPublica filer-of-record | Friedman President + Treasurer; Mikhailova VP + Secretary (2025–); V. Bleu Knight prior Secretary 2022–2024, current Board member. |
| Karl Friston co-authorship | **Verified [HIGH]** | [Frontiers DOI 10.3389/fnbeh.2021.647732](https://www.frontiersin.org/journals/behavioral-neuroscience/articles/10.3389/fnbeh.2021.647732/full); [PubMed 34248515](https://pubmed.ncbi.nlm.nih.gov/34248515/) | "Active Inferants" — peer-reviewed, Friston a named co-author. |
| Publication record (6-DOI sample) | **Verified [HIGH]** | doi.org / Crossref / PubMed / Europe PMC | All 6 sampled DOIs resolve and confirm Friedman authorship (first author on 4). Zenodo: 36 exact-name / 82 ORCID-linked — exact match to claimed figures. |
| Curio Cards artist (cards 24–26, minted May 9 2017) | **Verified [HIGH]** | [Curio Cards docs](https://docs.curio.cards/the-artists/daniel-friedman); [Wikipedia](https://en.wikipedia.org/wiki/Curio_Cards); [Amy Castor (independent NFT history)](https://amycastor.com/2022/06/04/the-early-history-of-nfts-curio-cards/) | Attribution confirmed by biographical fingerprint, not name-match. Christie's sale (Oct 1 2021, 393 ETH / ~$1.2M, 7 artists) independently corroborated. |
| Christie's lot number `6337619` | **First-party only** | [christies.com/en/lot/lot-6337619](https://www.christies.com/en/lot/lot-6337619) | URL resolves (HTTP 200); Christie's own page matches the exact Curio set. The specific lot **number** is not corroborated by any source independent of Christie's — present as a Christie's reference, not an independently verified identifier. |
| Identity graph (ORCID hub, Wikidata, dblp, Semantic Scholar) | **Verified [HIGH]** | [ORCID 0000-0001-6232-9096](https://orcid.org/0000-0001-6232-9096); [Wikidata Q138781444](https://www.wikidata.org/wiki/Q138781444) / [Q139600792](https://www.wikidata.org/wiki/Q139600792) | All 21 audited identity nodes resolve to one entity. Exposure scoped to professional/artistic identity; no home address, phone, DOB, or personal email exposed. A secondary Scholar ID (`Y2bMf3MAAAAJ`) is linked from ORCID — disambiguate. |
| GitHub footprint | **Verified [HIGH]** | [api.github.com/users/docxology](https://api.github.com/users/docxology); [/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute) | docxology = 286 public repos; AII = 50. `ActiveInferenceInstitute` is a **User** account, not an Organization (`/orgs/` 404s). |
| College of the Redwoods Spring-2026 teaching | **Principal-confirmed** | [github.com/docxology/biol-1](https://github.com/docxology/biol-1), [biol-8](https://github.com/docxology/biol-8) | BIOL-1 (General Biology, Pelican Bay) and BIOL-8 (Human Biology), Spring 2026. Confirmed by the principal as instructor of record; a future-term CR WebAdvisor public schedule may not yet list it. Retained verbatim. |

## Items intentionally softened (precision hygiene)

- **"107 indexed publications"** — not derivable from the primary Scholar profile; replaced with "Scholar-indexed publications" (the specific count was unverifiable).
- **SAB "announced January 2026"** — the 33-member 2026 cohort is corroborated; no independent source confirms a specific announcement month. Now "2026 cohort (33 members)".
- **Taschen *On NFTs* individual inclusion** — the book exists; individual inclusion is self-reported and carries an evidence caveat in the claims ledger (bibliography entry retained).
- **codomyrmex counts** — synced to the repo's own authoritative source (`MODULES.md` / `README` / `inventory.md` = 128 modules, 600 MCP tools); the GitHub repo *description* (127 / 424) is stale.

---

*Maintained alongside [`data/verification-log.json`](../data/verification-log.json). Update both together when a claim is re-verified; record the verification date and the independent source.*
