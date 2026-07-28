---
title: "CITE & VERIFY - Daniel Ari Friedman"
description: "How to cite this repository and verify key public claims."
keywords: "Daniel Ari Friedman, cite, citation, verification, ORCID, bibliography"
---
<div align="center">

# Cite & Verify

> **Navigation**: [🏠 Home](../README.md) | [📚 Bibliography](BIBLIOGRAPHY.md) | [🧾 Evidence](EVIDENCE.md) | [🧭 Discovery](DISCOVERY.md) | [🔗 Links](LINKS.md)

**Preferred citation metadata, public identifiers, and source-of-truth rules**

*Last updated: 2026-05-13*

[Website version](../cite-verify.html) · [CITATION.cff](../CITATION.cff) · [CodeMeta](../codemeta.json) · [BibTeX](../bibliography.bib) · [CSL JSON](../bibliography.csl.json) · [RIS](../bibliography.ris)

</div>

---

## Preferred Repository Citation

Use [`CITATION.cff`](../CITATION.cff) for the machine-readable repository citation.

```text
Friedman, Daniel Ari. docxology: Daniel Ari Friedman public research and software index. 2026. https://github.com/docxology/docxology
```

## Preferred Name and Identifiers

| Field | Value |
|---|---|
| Preferred name | Daniel Ari Friedman |
| ORCID | [0000-0001-6232-9096](https://orcid.org/0000-0001-6232-9096) |
| Wikidata | [Q138781444](https://www.wikidata.org/wiki/Q138781444) |
| Google Scholar | [DXjPFtYAAAAJ](https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en) |
| Homepage | [danielarifriedman.com](https://danielarifriedman.com/) |
| GitHub | [github.com/docxology](https://github.com/docxology) |

## Citation Exports

The unified bibliography is exported for common tools:

| Format | File | Use |
|---|---|---|
| BibTeX | [`bibliography.bib`](../bibliography.bib) | LaTeX, BibTeX, Pandoc, citation managers |
| CSL JSON | [`bibliography.csl.json`](../bibliography.csl.json) | citeproc, Pandoc, Zotero-adjacent workflows |
| RIS | [`bibliography.ris`](../bibliography.ris) | Zotero, EndNote, Mendeley-style imports |
| Works JSON | [`data/works.json`](../data/works.json) | Agentic discovery and structured site tooling |

Regenerate them from the curated bibliography:

```bash
python3 code/orchestrators/export_bibliography.py
```

## Verification Rules

1. Treat [`BIBLIOGRAPHY.md`](BIBLIOGRAPHY.md) as the curated publication source of truth.
2. Treat [`publications.html`](../publications.html) as the canonical HTML rendering of that bibliography.
3. Treat [`SOFTWARE.md`](SOFTWARE.md) as the curated software catalog.
4. Treat [`DISCOVERY.md`](DISCOVERY.md) as the public-source query map.
5. Treat [`EVIDENCE.md`](EVIDENCE.md) and [`data/claims.json`](../data/claims.json) as the current claim ledger.
6. Treat public API counts as freshness checks, not automatic replacements for curated site copy.

## Humility Rules for Reuse

- Prefer exact counts with dates over timeless superlatives.
- Keep “curated catalog” counts separate from “public API” counts.
- Use conservative wording for early NFT history unless the source defines the comparison class.
- Do not import OpenAlex or search-engine counts without reconciling them against ORCID, DOI, and the curated bibliography.

---

<div align="center">

*Part of [docxology/docxology](https://github.com/docxology/docxology) — see [EVIDENCE.md](EVIDENCE.md) for claim-level provenance.*

</div>
