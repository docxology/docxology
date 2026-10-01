<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19574117-blue)](https://doi.org/10.5281/zenodo.19574117)

---

## Abstract

> Scientific language does not merely describe biological phenomena; it actively constitutes the generative models through which researchers parse complex systems. This paper makes three core contributions to understanding—and correcting—the epistemic consequences of this constitutive role. First, we introduce a six-domain Ento-Linguistic framework that decomposes the terminological landscape of...

## Keywords

`EntoLinguistics`

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
