<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19574117-blue)](https://doi.org/10.5281/zenodo.19574117)

---

## Abstract

> Scientific language does not merely describe biological phenomena; it actively constitutes the generative models through which researchers parse complex systems. This paper makes three core contributions to understanding—and correcting—the epistemic consequences of this constitutive role. First, we introduce a six-domain Ento-Linguistic framework that decomposes the terminological landscape of insect research into analytically tractable themes, isolating domains where anthropomorphic language most severely distorts causal modeling. Second, we develop an open-source computational pipeline that integrates automated term extraction, co-occurrence network construction, and information-theoretic ambiguity scoring with principles from Active Inference and Complex Systems Theory. Third, we propose and validate four evidence-based meta-standards—Clarity, Appropriateness, Consistency, and Evolvability (CACE)—as a formalized protocol for lexical engineering. Analysis of a corpus encompassing 369 entomological publications (48787 tokens; 7105 unique token types; Type–Token Ratio 0.1456) extracts 888 candidate terms (with 261 assigned to specific semantic domains across 6 conceptual clusters linked by 9 weighted relationships). The resulting terminology networks display strong modularity alongside systematic cross-domain bridging—most prominently in the Power and Labor domain, where 43 bridging terms generate extensive semantic bleed-over into adjacent domains. Terms such as “queen” (241 occurrences), “worker” (269), and “caste” (121) implicitly impose hierarchical control topologies onto biological structures that are fundamentally stigmergic and decentralized. Across all 261 domain-assigned terms, 16.9% exhibit context-dependent semantic drift, demonstrating how conceptual constructs like “individuality” span multiple biological scales and consequently blur the formal systemic boundaries (Markov Blankets) required for mathematically rigorous modeling. The accompanying fully reproducible computational pipeline provides the quantitative analytical tools necessary for a more self-aware and epistemically rigorous scientific practice. All code and data are available at https://github.com/docxology/ento_linguistics.

## Methods

- **Corpus of 369 entomology publications mined from PubMed and arXiv** — Literature-mining classes queried PubMed (ants/eusocial/colony terms) and arXiv q-bio, then deduplicated and quality-filtered the records.
- **Seed-expansion term extraction into six Ento-Linguistic domains** — Tokens matched to domain seed lexicons (e.g. Power & Labor, Kin & Relatedness, Economics) are extended to co-occurring tokens in a 3-token window.
- **Semantic entropy of terms via k-means over TF-IDF usage contexts** — Ambiguity of each sufficiently attested term is scored as Shannon entropy (bits) over clustered usage contexts.
- **Six-layer deterministic analysis pipeline including networks and CACE scoring** — Layers cover extraction, entropy, domain statistics, conceptual networks/centrality, rhetorical scoring, and CACE meta-standard evaluation.

## Key Findings

- The corpus (48787 tokens) yields 888 candidate terms, 261 of them assigned to domains, across 6 conceptual clusters linked by 9 weighted relationships.
- Terminology networks are strongly modular with cross-domain bridging, most prominently in Power and Labor, which has 43 bridging terms.
- 16.9% of the 261 domain-assigned terms exhibit context-dependent semantic drift.
- Economics terms have the highest mean semantic entropy (1.21 bits) of all domains despite having zero bridging terms.
- CACE scoring of the "slave" to "host worker" reform shows aggregate scores rising from 0.38 to 0.81.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/ento_linguistics](https://github.com/docxology/ento_linguistics)
- GitHub release: [v1.1.1](https://github.com/docxology/ento_linguistics/releases/tag/v1.1.1)
- DOI: [10.5281/zenodo.19574117](https://doi.org/10.5281/zenodo.19574117)
- Zenodo record: [https://zenodo.org/records/19574117](https://zenodo.org/records/19574117)
- PDF: [Ento_Linguistics_DAF_TCC_v1_04-15-2026.pdf](Ento_Linguistics_DAF_TCC_v1_04-15-2026.pdf)
- PDF download: [Ento_Linguistics_v1.1.1_2026-09-22.pdf](https://zenodo.org/api/records/22902510/files/Ento_Linguistics_v1.1.1_2026-09-22.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/19574117)

## Citation

> Daniel Ari Friedman, Tucker Cahill Chambers (2026). *Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology*. Zenodo. DOI: 10.5281/zenodo.19574117. URL: https://doi.org/10.5281/zenodo.19574117.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
