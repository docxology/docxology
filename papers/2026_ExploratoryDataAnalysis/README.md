<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 Exploratory Data Analysis: A Reproducible Notebook Template

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21086292-blue)](https://doi.org/10.5281/zenodo.21086292)

---

## Abstract

> Exploratory data analysis (EDA) is the most common entry point in applied research, yet it is also where reproducibility most often breaks down: logic accumulates in notebook cells that are never tested and quietly drift from the prose describing them. This paper presents the computational-notebook exemplar of the Research Project Template (https://github.com/docxology/template): an interactive walkthrough notebook (projects/templates/template_eda_notebook/notebooks/eda_walkthrough.ipynb) that imports a small, fully-tested EDA library rather than carrying logic in its cells. We ship a deterministic dataset (data/measurements.csv) with a designed correlation structure and a handful of missing values, then load, clean, summarize, correlate, and visualize it entirely through tested functions in src/eda/. The library is side-effect-free — no plotting and no file I/O — and standalone (numpy and pandas only), so it is covered above the 90% project gate and reused identically from the notebook, the thin analysis script (scripts/eda_analysis.py), and this manuscript. Contributions are methodological and architectural. On the methods side, we walk the canonical first EDA pass: surface missingness explicitly rather than imputing it, compute per-column descriptive statistics and per-group means, and rank features by Pearson correlation. On the architecture side, we demonstrate the notebook-to-tested-source extraction workflow — explore fast in a cell, and the moment a computation matters, move it into the library behind a failing test — verified by a zero-mock suite and a structural notebook-binding check ().

## Keywords

`exploratory data analysis` · `computational notebook` · `reproducible research` · `pandas` · `data cleaning` · `correlation analysis`

## Methods

- **Synthetic 120-record measurement cohort with a fixed seed** — Analyzes a shipped deterministic CSV of height, weight and resting heart rate across three groups, with designed correlations and a few blank cells.
- **Listwise deletion with a reported CleaningReport, no imputation** — clean_dataset() drops rows missing any numeric feature and records rows in, remaining and dropped, rather than imputing.
- **Descriptive statistics, group means and Pearson correlation ranking** — Computes per-column summaries and per-group means, then ranks distinct feature pairs by absolute Pearson correlation via strongest_pairs().
- **Side-effect-free src/eda library with figure-data preparers** — Library functions return plot-ready frozen dataclasses (histogram bins, heatmap grid, category counts); only the thin script and notebook call matplotlib.
- **Zero-mock pytest suite, notebook-binding check and >=90% coverage gate** — Tests exercise real data with exact expected statistics, parse the .ipynb to check imports and absence of cell-defined logic, and enforce coverage.

## Key Findings

- With the shipped data, four rows with missing values are removed, leaving a complete-case dataset.
- The correlation ranking recovers the designed strong positive height–weight relationship, with resting heart rate only weakly related.
- All tests pass with coverage above the 90% project gate and no mocks.
- The paper states its contribution is procedural: the same tested functions back the notebook, the headless script and the manuscript.
- Stated limitations: a single small synthetic cohort, listwise deletion only, Pearson correlation only, and static outputs only.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/template_eda_notebook](https://github.com/docxology/template_eda_notebook)
- GitHub release: [v1.0.0](https://github.com/docxology/template_eda_notebook/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.21086292](https://doi.org/10.5281/zenodo.21086292)
- Zenodo record: [https://zenodo.org/records/21086292](https://zenodo.org/records/21086292)
- PDF: [Friedman_2026_Exploratory_0b10852b.pdf](Friedman_2026_Exploratory_0b10852b.pdf)
- PDF SHA-256: 0b10852bda89361cd71063867b55d9aed942881476867813facd549a961b0c1d

## Citation

> Daniel Ari Friedman (2026). *Exploratory Data Analysis: A Reproducible Notebook Template*. Zenodo. DOI: 10.5281/zenodo.21086292. URL: https://doi.org/10.5281/zenodo.21086292.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
