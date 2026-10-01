---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Modern Nostr Index Card-based Knowledge Engineering"
description: "Some concepts explored related to Knowledge Engineering, Nostr, Large Language Models, Complexity, and more.&nbsp;"
tags: ["nostr", "complexity", "large-language-model", "knowledge-engineering"]
domain: "Active Inference"
citation: "Andrew Claros, Daniel Friedman (2023). *Modern Nostr Index Card-based Knowledge Engineering*. Zenodo."
doi: "10.5281/zenodo.8118155"
artifact_doi: "10.5281/zenodo.8118156"
---

# Modern Nostr Index Card-based Knowledge Engineering

**Andrew Claros, Daniel Friedman** (2023) · Active Inference

## Context

This work addresses topics in **Active Inference**: Nostr, Complexity, Large Language Model, Knowledge Engineering.

## Methods

Primary methods and techniques applied in this work:

- **Index cards as hashed Nostr notes (JSON to SHA256 ID)** — The notes sketch each index card as a JSON object (username, text, etc.) hashed into a 32-byte SHA256 identifier, with edges defined between card IDs.
- **LLM semantic embeddings attached to index cards** — Proposes using language-model embeddings, translations and summaries so cards act as semantic bridges between texts.
- **Path analysis over composed index-card graphs** — Proposes analyzing paths through card graphs for trivial features (overall length) and subtler ones (e.g. which proportion of links are novel reports).

## Key Findings

Core contributions and results:

- The notes propose linking papers not only by citation edges but by syntactic bridges (keyword cards) and semantic bridges (embeddings).
- The notes argue auto-generated flashcards pose less of an information-overload risk than auto-generated papers, since unused cards are simply ignored and useful ones composed.
- The notes suggest review papers could follow the most popular paths through the card graph and novelty search the least traversed ones.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.8118155
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-05-30T18:56:21Z
- Artifact DOI: 10.5281/zenodo.8118156

## Prerequisites

- Familiarity with Nostr, Complexity, Large Language Model
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.8118155`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
