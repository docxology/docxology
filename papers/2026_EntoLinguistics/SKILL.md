---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology"
description: "<p>Release v1.1.1 of the Ento-Linguistics research project.</p><p>Corpus: 7,609 PubMed abstracts (full search surface drained), 7,073 PMC open-access full texts, 2,460 BHL historical documents (1850&ndash;1970), 61 arXiv preprints, 536/536 OpenAlex c..."
tags: ["entolinguistics"]
domain: "Entomology"
citation: "Daniel Ari Friedman, Tucker Cahill Chambers (2026). *Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology*. Zenodo."
doi: "10.5281/zenodo.19574117"
---

# Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · Entomology

## Context

This work addresses topics in **Entomology**: EntoLinguistics.

## Methods

Primary methods and techniques applied in this work:

- **Corpus of 369 entomology publications mined from PubMed and arXiv** — Literature-mining classes queried PubMed (ants/eusocial/colony terms) and arXiv q-bio, then deduplicated and quality-filtered the records.
- **Seed-expansion term extraction into six Ento-Linguistic domains** — Tokens matched to domain seed lexicons (e.g. Power & Labor, Kin & Relatedness, Economics) are extended to co-occurring tokens in a 3-token window.
- **Semantic entropy of terms via k-means over TF-IDF usage contexts** — Ambiguity of each sufficiently attested term is scored as Shannon entropy (bits) over clustered usage contexts.
- **Six-layer deterministic analysis pipeline including networks and CACE scoring** — Layers cover extraction, entropy, domain statistics, conceptual networks/centrality, rhetorical scoring, and CACE meta-standard evaluation.

## Key Findings

Core contributions and results:

- The corpus (48787 tokens) yields 888 candidate terms, 261 of them assigned to domains, across 6 conceptual clusters linked by 9 weighted relationships.
- Terminology networks are strongly modular with cross-domain bridging, most prominently in Power and Labor, which has 43 bridging terms.
- 16.9% of the 261 domain-assigned terms exhibit context-dependent semantic drift.
- Economics terms have the highest mean semantic entropy (1.21 bits) of all domains despite having zero bridging terms.
- CACE scoring of the "slave" to "host worker" reform shows aggregate scores rising from 0.38 to 0.81.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2016_AntGenetics](../2016_AntGenetics/)
- [2016_ForagingGene](../2016_ForagingGene/)
- [2017_MutAnts](../2017_MutAnts/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.19574117
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:53Z

## Prerequisites

- Familiarity with EntoLinguistics
- Background in Entomology fundamentals
- Access to source repository: docxology/ento_linguistics

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.19574117`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
