<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Markdown Decision Process: A Framework for Probabilistic Document Analysis

**Daniel Friedman** (2025) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17244386-blue)](https://doi.org/10.5281/zenodo.17244386)

---

## Abstract

> The Markdown Decision Process (MDP) framework treats Markdown documents as stochastic decision processes, enabling intelligent analysis, generation, and optimization through probabilistic modeling. Drawing from Markov Decision Process and POMDP theory, the framework operates at Marr's three levels: computational, algorithmic, and implementational. Key innovations include MarkChain for document...

## Keywords

`Markdown Decision Process` · `document analysis` · `Markov chains` · `reinforcement learning` · `POMDP` · `probabilistic modeling` · `document generation`

## Methods

- **Markdown elements modeled as states in a stochastic decision process** — Treats Markdown documents as stochastic processes drawing on MDP/POMDP theory, with transitions between elements following learned probabilistic patterns.
- **MarkChain, PolicyOptimizer and BeliefUpdater components** — Higher-order Markov chains for generation, reinforcement-learning policy optimization against user reward functions, and Bayesian belief updating over semantic interpretations.
- **Evaluation corpora: technical docs, arXiv papers, blogs, mixed** — Reports four evaluation corpora, e.g. 500 technical documents from 25 open-source projects and 200 arXiv CS papers converted to Markdown.
- **Comparisons against n-gram, GPT-2, BERT and rule-based baselines** — Compares MarkChain orders 1–3 against n-gram and GPT-2 baselines for structure learning, and BeliefUpdater against rule-based and BERT classifiers.
- **Manually annotated 200-document semantic classification test** — BeliefUpdater accuracy and calibration (ECE) assessed on 200 manually annotated documents with an 80/20 train/test split.

## Key Findings

- The paper reports higher structural similarity for MarkChain than baselines, with higher-order chains performing better at the cost of longer generation time.
- BeliefUpdater is reported as more calibrated than rule-based approaches but slightly less accurate than a BERT classifier.
- Reported scalability is approximately linear in document size, with policy optimization the most computationally costly operation.
- In one controlled example, optimization reduced average paragraph length from 16.0 to 14.4 words and the list-to-paragraph ratio from 1.0 to 0.2.
- The paper lists threats to validity, including corpus bias, hyperparameter sensitivity and limited domain diversity in evaluation corpora.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.17244386](https://doi.org/10.5281/zenodo.17244386)
- Zenodo record: [https://zenodo.org/records/17244386](https://zenodo.org/records/17244386)
- PDF: [2025_MarkdownDecisionProcess.pdf](2025_MarkdownDecisionProcess.pdf)
- PDF download: [MarkdownDecisionProcess_DAF_10-02-2025.pdf](https://zenodo.org/api/records/17244387/files/MarkdownDecisionProcess_DAF_10-02-2025.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/17244386)

## Citation

> Daniel Friedman (2025). *Markdown Decision Process: A Framework for Probabilistic Document Analysis*. Zenodo. DOI: 10.5281/zenodo.17244386. URL: https://doi.org/10.5281/zenodo.17244386.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
