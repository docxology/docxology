<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Modern Nostr Index Card-based Knowledge Engineering

**Andrew Claros, Daniel Friedman** (2023) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.8118155-blue)](https://doi.org/10.5281/zenodo.8118155)

---

## Abstract

> Some concepts explored related to Knowledge Engineering, Nostr, Large Language Models, Complexity, and more.

## Keywords

`Nostr` · `Complexity` · `Large Language Model` · `Knowledge Engineering`

## Methods

- **Index cards as hashed Nostr notes (JSON to SHA256 ID)** — The notes sketch each index card as a JSON object (username, text, etc.) hashed into a 32-byte SHA256 identifier, with edges defined between card IDs.
- **LLM semantic embeddings attached to index cards** — Proposes using language-model embeddings, translations and summaries so cards act as semantic bridges between texts.
- **Path analysis over composed index-card graphs** — Proposes analyzing paths through card graphs for trivial features (overall length) and subtler ones (e.g. which proportion of links are novel reports).

## Key Findings

- The notes propose linking papers not only by citation edges but by syntactic bridges (keyword cards) and semantic bridges (embeddings).
- The notes argue auto-generated flashcards pose less of an information-overload risk than auto-generated papers, since unused cards are simply ignored and useful ones composed.
- The notes suggest review papers could follow the most popular paths through the card graph and novelty search the least traversed ones.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.8118155](https://doi.org/10.5281/zenodo.8118155)
- Artifact DOI: [10.5281/zenodo.8118156](https://doi.org/10.5281/zenodo.8118156)
- Zenodo record: [https://zenodo.org/records/8118156](https://zenodo.org/records/8118156)
- PDF: [Index_Card_7_5_2023.pdf](Index_Card_7_5_2023.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/8118156)

## Citation

> Andrew Claros, Daniel Friedman (2023). *Modern Nostr Index Card-based Knowledge Engineering*. Zenodo. DOI: 10.5281/zenodo.8118155. URL: https://doi.org/10.5281/zenodo.8118155.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
