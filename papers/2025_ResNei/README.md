<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 ResNei: Solution Design Document

**Janna Lumiruusu, Daniel Friedman, Shagor Rahman, Vladimir Baulin, Andrew Pashea** (2025) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.15389682-blue)](https://doi.org/10.5281/zenodo.15389682)

---

## Abstract

> ResNei — Research Neighbourhood – is an AI-augmented environment designed to transform how we discover, analyse, and connect ideas. At its core is the Research Discovery Engine, which constructs a living, responsive knowledge graph through the distillation of verified concepts and the dynamic linking of an evolving corpus of scientific knowledge. This graph is structured as a set of Conceptual...

## Keywords

`ResNei` · `Research Neighbourhood` · `collaborative research` · `distributed collaboration` · `interdisciplinary` · `knowledge sharing`

## Methods

- **Action-Intention interaction model (no predictive intent inference yet)** — Design treats explicit user actions (uploading, annotating, opening a concept map) as signals of research direction; the document states intent is not yet inferred predictively.
- **Knowledge graph of Conceptual Nexus Models (Research Discovery Engine)** — The proposed core engine builds a knowledge graph structured as Conceptual Nexus Models, modular representations of connected ideas from a research corpus.
- **Proposed full-stack architecture (PDF.js, ElasticSearch, graph DB, Docker)** — Specifies frontend/backend components including PDF.js and LaTeX rendering, NLP document processing, ElasticSearch indexing, a graph database, and Docker/CI deployment.
- **Assumptions and harms/risks/amelioration tables** — Tabulates nine usage assumptions and a set of potential harms (e.g. algorithmic misrepresentation, marginalisation of less-cited research) with proposed mitigations.
- **Neuro-informed cognitive load design principles** — Applies progressive disclosure, contextual cues, fault tolerance (undo/redo, version history), and adaptive complexity, referencing a neuroscience-informed UX table.

## Key Findings

- The document presents ResNei as an AI-augmented research discovery and collaboration environment, and states the project is in early development with working prototypes.
- It proposes an initial force-directed concept graph, similar to a simplified Obsidian.md structure, deferring clustering and semantic zooming to later work.
- To counter misplaced trust, the design frames AI outputs as provisional suggestions and the knowledge graph as a navigational aid rather than a definitive map.
- The authors state they are now seeking stakeholders, with special attention to trans- and interdisciplinary spaces, as they move from prototyping to implementation.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.15389682](https://doi.org/10.5281/zenodo.15389682)
- Zenodo record: [https://zenodo.org/records/15389682](https://zenodo.org/records/15389682)
- PDF: [2025_ResNei.pdf](2025_ResNei.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/15389682)

## Citation

> Janna Lumiruusu, Daniel Friedman, Shagor Rahman, Vladimir Baulin, Andrew Pashea (2025). *ResNei: Solution Design Document*. Zenodo. DOI: 10.5281/zenodo.15389682. URL: https://doi.org/10.5281/zenodo.15389682.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
