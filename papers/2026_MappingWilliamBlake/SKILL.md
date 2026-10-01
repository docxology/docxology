---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls"
description: "A reproducible, rights-bounded digital-humanities workflow that builds and audits a target-ledgered William Blake corpus (texts, images, metadata, analysis, visual summaries) and separates open-source code and project-authored aggregate analytics fro..."
tags: ["william-blake", "digital-humanities", "corpus-acquisition", "source-provenance", "rights-bounded-release"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls*. Zenodo."
doi: "10.5281/zenodo.21047573"
---

# Mapping William Blake's Works: Evidence ledgers, source provenance, text-image diagnostics, and rights-bounded release controls

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: William Blake, digital humanities, corpus acquisition, source provenance.

## Methods

Primary methods and techniques applied in this work:

- **7-phase DAG pipeline (blake) from discovery to reports** — The corpus is built by a directed pipeline of discovery, acquisition, metadata, analysis, visualizations, export, and reports, whose JSON artifacts also populate the manuscript.
- **Versioned canonical target ledger of 104 work-level Blake targets** — A ledger derived from Blake bibliographies, editions, Archive identifiers, and visual catalogues serves as the denominator for coverage claims.
- **Tiered source registry with the William Blake Archive as primary authority** — The registry holds the Blake Archive, Project Gutenberg, and Internet Archive, with the Archive given priority when sources disagree and others used as fallback or corroboration.
- **Descriptive text metrics: tokenization, type-token ratio, lexical sentiment** — Each text-bearing work is tokenized to compute word counts, sentiment, vocabulary richness, and themes, treated as descriptors rather than literary judgments.
- **TF-IDF vectors with deterministic PCA/LSA projection over 162 works** — A 120-term TF-IDF vocabulary is built across text-bearing works and projected onto PCA/LSA axes as a reading instrument over local evidence.

## Key Findings

Core contributions and results:

- The saved run represents 102 of 104 ledger targets (98.1%) but fully meets the required text/image evidence profile for only 90 (86.5%); 12 are partial and 2 missing.
- The text-bearing subset contains 156 works and 216878 words, and joint text-image diagnostics are available for 33 works.
- The ontology module produced a work-theme graph of 356 nodes and 297 edges, including 16 theme nodes.
- The local analysis ledger reports all 340 works analyzed with 0 recorded analysis errors.
- The author frames the contribution as an auditable corpus-governance method, not a completed or exhaustive analysis of Blake's works.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21047573
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with William Blake, digital humanities, corpus acquisition
- Background in Computational fundamentals
- Access to source repository: docxology/blake

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21047573`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
