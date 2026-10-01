---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation"
description: "We present a modular, citation-bound data compendium for the Grateful Dead universe — shows, songs, performances, personnel timelines, venues, recordings, and reception — and a category-theoretic interpretation of the performance graph. The work is g..."
tags: ["grateful-dead", "setlist-data", "category-theory", "music-information-retrieval", "reproducible-data-compendium"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation*. Zenodo."
doi: "10.5281/zenodo.20482025"
---

# The Music Never Stopped: A Grateful Data Compendium with a Category-Theoretic Interpretation

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: grateful dead, setlist data, category theory, music information retrieval.

## Methods

Primary methods and techniques applied in this work:

- **Integration of nine primary Grateful Dead data sources into one schema** — Setlist.fm, SetList Program, CMU archive, GDsets, gdshowsdb, Internet Archive, whitegum, dead.net and Wikipedia are parsed by testable modules and merged.
- **Deterministic canonical-slug merge with frozen-dataclass schema** — Entities validate inputs and use canonical-slug primary keys so cross-source joins reduce to dictionary lookups; integration is a sort-keyed merge.
- **Completeness audit, figure-validation gate, and first-principles claim ledger** — Runtime checks certify referential integrity and non-degenerate figures; a ledger classifies each major result by inputs, assumptions, and limits.
- **First-order Markov model of within-show song order with permutation-null FDR screen** — Fits song-to-song transition probabilities, audits support thresholds, and screens transitions against a permutation null under FDR control.
- **Category-theoretic constructions: date poset, show category, functors, spans** — Builds setlist and lineup functors from dates into sets, an active-roster presheaf, and performances as spans between show and song.

## Key Findings

Core contributions and results:

- The committed compendium contains 3341 ingested shows, 645 songs, 912 venues, and 40757 performance rows.
- Completeness is referential only: 282 of the 3341 catalogued shows have an empty setlist in gdshowsdb.
- Repertoire is highly skewed: the song-performance Gini coefficient is 0.74 and the top decile of songs accounts for 50.61% of non-segment performances.
- The most frequent explicit segue in the corpus is the structural "drums" -> "space" passage, with 1197 occurrences.
- Wide pullbacks over a show recover its setlist and over a song recover its performance history, while the active roster is a non-monotone presheaf on the date poset.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20482025
- PDF SHA-256: 296b3b5c5e9f3d628e15ae5d467dd5cc418bd018f0166194c9494b33b3367dda
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:55Z

## Prerequisites

- Familiarity with grateful dead, setlist data, category theory
- Background in Computational fundamentals
- Access to source repository: docxology/grateful_data

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20482025`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
