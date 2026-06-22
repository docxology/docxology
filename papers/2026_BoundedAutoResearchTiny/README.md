# Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20417016.svg)](https://doi.org/10.5281/zenodo.20417016)

---

## Abstract

Abstract

This paper presents Deterministic bounded AutoResearch for a small MNIST neural-network task, a public template exemplar that
turns an AutoResearch loop into ordinary reproducible research infrastructure.
The case study is intentionally small but concrete: 2000 training
and 500 test images from MNIST handwritten digit database are evaluated by the
bounded small MNIST neural-network classification loop. The run evaluates
4 of 5 proposed candidates,
including Tiny patch-attention classifier, selects
exp-mlp-tanh-64 (MLP,
50890 parameters), and improves test_accuracy from
82.6% to 89.4%
(6.8% absolute change). The validated diagnostic layer reports
macro F1 89.4%, bootstrap accuracy interval
86.4% to 92.0%, Brier score 0.161,
negative log likelihood 0.361, top-2 accuracy
95.6%, and exact McNemar p-value 0.000.
The same pipeline writes proposal, candidate, run, review, benchmark, evidence,
figure, confusion-matrix, statistical-summary, probability-quality, and
security-integrity artifacts from declared output contracts; uses
0 LLM calls at USD 0.00 cost; and records
7 configured stages, 6 supported
local-artifact claims, and 78 required artifacts.
The local security attestation status is passed,
with 0 checksum mismatch(es). The final
readiness status is passed, with review gates deferred to a
human rather than self-approved by the generated run.

---
Associated artifacts
GitHub release: v0.3.0 (https://github.com/docxology/template_autoresearch_project/releases/tag/v0.3.0)
DOI: https://doi.org/10.5281/zenodo.20417016
Zenodo: https://zenodo.org/records/20417016
PDF SHA-256: f02abeeaba525750c4b3751241711b80b472e11cc2c0f7f34f56b62dbea786ef

## Keywords

autoresearch · reproducible research · machine learning benchmark · artifact readiness · human review · local artifact integrity

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20417016](https://doi.org/10.5281/zenodo.20417016) |
| **Published** | 2026 |
| **Version** | 0.3.0 |
| **Zenodo record** | https://zenodo.org/records/20420357 |
| **GitHub release** | https://github.com/docxology/template_autoresearch_project/releases/tag/v0.3.0 |
| **Source repository** | https://github.com/docxology/template_autoresearch_project |

## Files

- `Friedman_2026_Bounded_f02abeea.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task*. Zenodo. https://doi.org/10.5281/zenodo.20417016

## Related

- GitHub release: https://github.com/docxology/template_autoresearch_project/releases/tag/v0.3.1
- Zenodo record: https://zenodo.org/records/20692993

- Zenodo record: https://zenodo.org/records/20420357
- GitHub release: https://github.com/docxology/template_autoresearch_project/releases/tag/v0.3.0
- Source repository: https://github.com/docxology/template_autoresearch_project
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
