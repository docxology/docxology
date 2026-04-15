# 🐜 Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology

**Daniel Ari Friedman** · **Tucker Cahill Chambers** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19574118-blue)](https://doi.org/10.5281/zenodo.19574118)

---

<!-- Schema.org structured data for search engines -->
<!--
{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"EntoLinguistics","abstract":"Scientific language constitutes the generative models through which researchers parse complex systems. This paper introduces a six-domain Ento-Linguistic framework, an open-source computational pipeline for term extraction and terminology networks, and CACE meta-standards (Clarity, Appropriateness, Consistency, Evolvability) for lexical engineering in entomology.","keywords":["entomology","scientific communication","terminology networks","Active Inference","corpus linguistics","CACE","semantic entropy","myrmecology"],"author":[{"@type":"Person","name":"Daniel Ari Friedman","url":"https://docxology.github.io/docxology/"},{"@type":"Person","name":"Tucker Cahill Chambers"}]}
-->

*How Terminology Networks Shape Understanding of Insect Biology (And Vice-Versa)*

## Abstract

> Scientific language does not merely describe biological phenomena; it actively constitutes the generative models through which researchers parse complex systems. This paper makes three core contributions to understanding—and correcting—the epistemic consequences of this constitutive role. First, we introduce a six-domain Ento-Linguistic framework that decomposes the terminological landscape of insect research into analytically tractable themes, isolating domains where anthropomorphic language most severely distorts causal modeling. Second, we develop an open-source computational pipeline that integrates automated term extraction, co-occurrence network construction, and information-theoretic ambiguity scoring with principles from Active Inference and Complex Systems Theory. Third, we propose and validate four evidence-based meta-standards—Clarity, Appropriateness, Consistency, and Evolvability (CACE)—as a formalized protocol for lexical engineering. Analysis of a corpus encompassing 369 entomological publications (48787 tokens; 7105 unique token types; Type–Token Ratio 0.1456) extracts 888 candidate terms (with 261 assigned to specific semantic domains across 6 conceptual clusters linked by 9 weighted relationships). The resulting terminology networks display strong modularity alongside systematic cross-domain bridging—most prominently in the Power and Labor domain, where 43 bridging terms generate extensive semantic bleed-over into adjacent domains. Terms such as “queen” (241 occurrences), “worker” (269), and “caste” (121) implicitly impose hierarchical control topologies onto biological structures that are fundamentally stigmergic and decentralized. Across all 261 domain-assigned terms, 16.9% exhibit context-dependent semantic drift, demonstrating how conceptual constructs like “individuality” span multiple biological scales and consequently blur the formal systemic boundaries (Markov Blankets) required for mathematically rigorous modeling. The accompanying fully reproducible computational pipeline provides the quantitative analytical tools necessary for a more self-aware and epistemically rigorous scientific practice. All code and data are available at https://github.com/docxology/ento_linguistics.

## Keywords

`entomology` · `scientific communication` · `terminology networks` · `Active Inference` · `corpus linguistics` · `CACE` · `semantic entropy` · `myrmecology`

## Key Contributions

- A six-domain Ento-Linguistic framework (Unit of Individuality; Power & Labor; Behavior & Identity; Sex & Reproduction; Kin & Relatedness; Economics) for analyzing terminological friction in insect research.
- An open-source, reproducible pipeline: literature mining (PubMed, arXiv), text processing, term extraction and domain assignment, semantic entropy, statistical tests, conceptual network and rhetorical analysis, and CACE scoring.
- CACE meta-standards (Clarity, Appropriateness, Consistency, Evolvability) as a protocol for lexical engineering and term evaluation.

## Methods

- Corpus construction via PubMed and arXiv queries; deduplication and preprocessing (tokenization, lemmatization, n-grams) as specified in the paper and supplemental methods.
- Term extraction and domain classification via seed lexicons and co-occurrence expansion; semantic entropy via clustered context vectors; pairwise and ANOVA tests with Benjamini–Hochberg correction where applicable.
- Conceptual overlap networks, bridging-term identification, rhetorical and framing analysis, and per-term CACE scoring.

## 🎯 Consulting & Tutoring

**Available for AI Research Consulting and Tutoring.** [Contact Daniel Ari Friedman, PhD](https://docxology.github.io/docxology/) for collaboration on Active Inference, Bayesian modeling, and computational biology.

## Citation

```bibtex
@article{Friedman_2026_EntoLinguistics,
  author = {Daniel Ari Friedman and Tucker Cahill Chambers},
  title = {{Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology}},
  journal = {Zenodo},
  year = {2026},
  doi = {10.5281/zenodo.19574118},
}
```

## File Inventory

- `AGENTS.md` (3,129 bytes)
- `Ento_Linguistics_DAF_TCC_v1_04-15-2026.pdf` (5,889,924 bytes)
- `README.md` (5,519 bytes)
- `SKILL.md` (3,288 bytes)
