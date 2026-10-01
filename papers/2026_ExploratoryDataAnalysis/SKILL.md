---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Exploratory Data Analysis: A Reproducible Notebook Template"
description: "Exploratory data analysis (EDA) is the most common entry point in applied research, yet it is also where reproducibility most often breaks down: logic accumulates in notebook cells that are never tested and quietly drift from the prose describing the..."
tags: ["exploratory-data-analysis", "computational-notebook", "reproducible-research", "pandas", "data-cleaning", "correlation-analysis"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Exploratory Data Analysis: A Reproducible Notebook Template*. Zenodo."
doi: "10.5281/zenodo.21086292"
---

# Exploratory Data Analysis: A Reproducible Notebook Template

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: exploratory data analysis, computational notebook, reproducible research, pandas.

## Methods

Primary methods and techniques applied in this work:

- **Synthetic 120-record measurement cohort with a fixed seed** — Analyzes a shipped deterministic CSV of height, weight and resting heart rate across three groups, with designed correlations and a few blank cells.
- **Listwise deletion with a reported CleaningReport, no imputation** — clean_dataset() drops rows missing any numeric feature and records rows in, remaining and dropped, rather than imputing.
- **Descriptive statistics, group means and Pearson correlation ranking** — Computes per-column summaries and per-group means, then ranks distinct feature pairs by absolute Pearson correlation via strongest_pairs().
- **Side-effect-free src/eda library with figure-data preparers** — Library functions return plot-ready frozen dataclasses (histogram bins, heatmap grid, category counts); only the thin script and notebook call matplotlib.
- **Zero-mock pytest suite, notebook-binding check and >=90% coverage gate** — Tests exercise real data with exact expected statistics, parse the .ipynb to check imports and absence of cell-defined logic, and enforce coverage.

## Key Findings

Core contributions and results:

- With the shipped data, four rows with missing values are removed, leaving a complete-case dataset.
- The correlation ranking recovers the designed strong positive height–weight relationship, with resting heart rate only weakly related.
- All tests pass with coverage above the 90% project gate and no mocks.
- The paper states its contribution is procedural: the same tested functions back the notebook, the headless script and the manuscript.
- Stated limitations: a single small synthetic cohort, listwise deletion only, Pearson correlation only, and static outputs only.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21086292
- PDF SHA-256: 0b10852bda89361cd71063867b55d9aed942881476867813facd549a961b0c1d
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:57Z

## Prerequisites

- Familiarity with exploratory data analysis, computational notebook, reproducible research
- Background in Computational fundamentals
- Access to source repository: docxology/template_eda_notebook

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21086292`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
