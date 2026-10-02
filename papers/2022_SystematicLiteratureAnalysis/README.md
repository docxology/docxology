<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 The Free Energy Principle & Active Inference: a Systematic Literature Analysis

**Virginia Bleu Knight, RJ Cordes, Daniel Friedman** (2022) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.7449367-blue)](https://doi.org/10.5281/zenodo.7449367)

---

## Abstract

> Here we perform a literature analysis of publications in scientific literature using the term “Free Energy Principle” or “Active Inference”, with an emphasis on works written by Karl J Friston. For a subset of papers with accessible full texts, we performed manual annotation (related to structural, visual, and mathematical features) and automated analyses (related to the terms in the Active Inference Institute’s Active Inference Ontology). The initial analysis here, at the scale of thousands of citations and hundreds of annotated papers, is presented as a first step towards the development of systems which could: Encompass increased scope of relevant works, including non-textual Integrate multiple forms of annotation and participation Facilitate integration of manual and artificial contributions Feature richer interfaces for use in learning & research Address field-specific local questions and provide transferable approaches Speak to broader questions in the history and philosophy of science This project is maintained by the Active Inference Institute. This project has an interactive Coda site and a Github repository .

## Keywords

`systematic literature analysis` · `Free Energy Principle` · `Active Inference` · `Karl Friston` · `history of science` · `bibliometrics` · `ontology`

## Methods

- **Publish or Perish / Google Scholar search for FEP, ActInf and Friston papers** — Citations from 1990–2021 matching the two terms or authored by Karl Friston were collected and de-duplicated manually by title.
- **BioPython query of open-access PubMed papers for full-text subset** — The BioPython API was used to restrict analysis to open-source PubMed papers with the terms in title/abstract.
- **PyPDF2 term-frequency extraction using Active Inference Ontology terms** — A custom PyPDF2 script counted 74 core, 250 supplement and 74 entailed ontology terms in each abstract and PDF.
- **Manual annotation of figures, equations, tables, boxes, supplements** — Each analyzed paper was hand-annotated for structural/mathematical features and estimated citations per year.
- **ResearchRabbit citation network; Coda tables; Orange clustering** — ResearchRabbit built a citation network of the focal papers; Coda merged data into reflexive tables; Orange clustered term usage.

## Key Findings

- From the larger FEP/ActInf citation corpus, the analysis focused on an initial set of 237 open-access papers obtained via PubMed.
- The most highly cited papers in the open-source dataset were from 2013 and all included Karl J. Friston as an author.
- By citations per year, Friston is not in the top five first authors; Sterzer (109.3) and Carhart-Harris (108.5) lead, and top papers by this metric date from 2018–2020.
- All core Active Inference Ontology terms increased in use frequency over time.
- Term frequencies tracked specific publications, e.g. 'Information Geometry' rose after Parr et al. 2019 and 'Cognitivism' after Friston & Allen 2018.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.7449367](https://doi.org/10.5281/zenodo.7449367)
- Zenodo record: [https://zenodo.org/records/7449367](https://zenodo.org/records/7449367)
- PDF: [2022_SystematicLiteratureAnalysis.pdf](2022_SystematicLiteratureAnalysis.pdf)
- PDF download: [KnightCordesFriedman_2022_ActInf_FEP_Literature_v1.pdf](https://zenodo.org/api/records/7449368/files/KnightCordesFriedman_2022_ActInf_FEP_Literature_v1.pdf/content)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/7449367)

## Citation

> Virginia Bleu Knight, RJ Cordes, Daniel Friedman (2022). *The Free Energy Principle & Active Inference: a Systematic Literature Analysis*. Zenodo. DOI: 10.5281/zenodo.7449367. URL: https://doi.org/10.5281/zenodo.7449367.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
