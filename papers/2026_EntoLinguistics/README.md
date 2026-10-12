<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🐜 Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19574117-blue)](https://doi.org/10.5281/zenodo.19574117)

---

## Abstract

> Ento-Linguistics v1.3.1 is a corpus-custody patch to the v1.3.0 complexity edition. A second exact-text PubMed reconciliation links 59 more archived abstracts to their source records (7,599 of 7,609 now identified; the 10 unreconciled strings stay excluded from headline results), and PMC records titled as corrections, errata, retraction notices or retracted items are excluded from full-text analysis (6,997 of 7,073 stored records analyzed). All analysis layers, both fixed-margin protocols and the vocabulary/threshold diagnostic were regenerated; the paper reports every value from those exports. Six overlapping terminology domains and four source layers retain their descriptive scope; fixed-margin comparisons and heuristic entropy/CACE measures remain distinct from biological interactions, validated meaning or causal reader effects. The 20-minute lecture remains the v1.3.0 GitHub release asset matched to the v1.3.0 paper. Paper figures are CC BY 4.0; software is MIT; source corpus materials retain their providers' terms. Previous version DOIs preserve earlier artifact identities.

## Keywords

`entomology` · `scientific terminology` · `language analysis` · `discourse analysis` · `ant biology` · `eusociality` · `conceptual frameworks` · `active inference` · `terminology networks` · `computational linguistics` · `complex systems` · `complexity`

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
- GitHub release: [v1.3.1](https://github.com/docxology/ento_linguistics/releases/tag/v1.3.1)
- DOI: [10.5281/zenodo.19574117](https://doi.org/10.5281/zenodo.19574117)
- Zenodo record: [https://zenodo.org/records/19574117](https://zenodo.org/records/19574117)
- PDF: [Ento_Linguistics_DAF_TCC_v1_04-15-2026.pdf](Ento_Linguistics_DAF_TCC_v1_04-15-2026.pdf)
- PDF: [Ento_Linguistics_manuscript.pdf](Ento_Linguistics_manuscript.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/19574117)

## Citation

> Daniel Ari Friedman, Tucker Cahill Chambers (2026). *Ento-Linguistics: Language, Ambiguity, and Scientific Communication in Entomology*. Zenodo. DOI: 10.5281/zenodo.19574117. URL: https://doi.org/10.5281/zenodo.19574117.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
