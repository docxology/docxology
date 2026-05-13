---
title: "EVIDENCE - Daniel Ari Friedman"
description: "Claim-level evidence ledger with source links, confidence, caveats, and maintenance ownership."
keywords: "Daniel Ari Friedman, evidence ledger, claims, verification, source freshness"
---
<div align="center">

# Evidence Ledger

> **Navigation**: [🏠 Home](../README.md) | [🧭 Discovery](DISCOVERY.md) | [🧾 Cite & Verify](CITE_VERIFY.md) | [📚 Bibliography](BIBLIOGRAPHY.md)

[Website version](../evidence.html) · [Source claims JSON](../data/claims.json) · [Reconciliation JSON](../data/reconciliation.json) · [Latest public-source snapshot](../reports/public_source_snapshot_2026-05-13.json)

</div>

---

This ledger records selected public claims, the type of source backing each claim, the confidence level, and the caveat that should travel with the claim.

| Claim | Status | Confidence | Checked | Owner | Sources | Caveat |
| --- | --- | --- | --- | --- | --- | --- |
| The curated bibliography contains 115 works. | curated-local | high | 2026-05-13 | ARCHIVIST | [pages/BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md)<br>[publications.html](../publications.html)<br>[data/works.json](../data/works.json) | Curated count includes papers, books, presentations, courses, playbooks, and series. |
| The repository contains 108 per-paper documentation folders. | curated-local | high | 2026-05-13 | MAINTAINER | [papers/](../papers/)<br>[papers/README.md](../papers/README.md)<br>[papers/paper_metadata.json](../papers/paper_metadata.json) | Not every bibliography row has a paper folder; media/course rows may not. |
| The docxology GitHub profile has 286 public repositories. | public-api | high | 2026-05-13 | INTEGRATOR | [https://api.github.com/users/docxology](https://api.github.com/users/docxology)<br>[reports/public_source_snapshot_2026-05-13.json](../reports/public_source_snapshot_2026-05-13.json) | GitHub profile count includes forks and repositories not catalogued in SOFTWARE.md. |
| The Active Inference Institute GitHub organization has 50 public repositories. | public-api | high | 2026-05-13 | INTEGRATOR | [https://api.github.com/users/ActiveInferenceInstitute](https://api.github.com/users/ActiveInferenceInstitute)<br>[reports/public_source_snapshot_2026-05-13.json](../reports/public_source_snapshot_2026-05-13.json) | Local software catalog tracks 32 AII repositories with docxology contributions. |
| ORCID 0000-0001-6232-9096 is the canonical researcher identifier. | public-identifier | high | 2026-05-13 | ARCHIVIST | [https://orcid.org/0000-0001-6232-9096](https://orcid.org/0000-0001-6232-9096)<br>[https://pub.orcid.org/v3.0/0000-0001-6232-9096/works](https://pub.orcid.org/v3.0/0000-0001-6232-9096/works) | ORCID public work groups may lag new deposits and may group versions differently. |
| Curio Cards 24, 25, and 26 are early Ethereum art NFTs minted on May 9, 2017. | public-profile | medium | 2026-05-13 | RESEARCHER | [https://curio.cards/artist/danielfriedman/](https://curio.cards/artist/danielfriedman/)<br>[https://www.christies.com/en/lot/lot-6337619](https://www.christies.com/en/lot/lot-6337619)<br>[papers/2024_CurioCards/README.md](../papers/2024_CurioCards/README.md) | Use conservative phrasing; broader first/earliest claims vary by source and definition. |

## Maintenance Notes

- Prefer public APIs as freshness checks, not as automatic overrides of curated local metadata.
- If a claim changes, update `code/orchestrators/export_agent_data.py`, regenerate `data/claims.json`, and then regenerate this page.
- Use conservative language when an external source depends on definitions that vary across communities.
