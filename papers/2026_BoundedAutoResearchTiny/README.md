# Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20417017.svg)](https://doi.org/10.5281/zenodo.20417017)

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
GitHub release: Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task (v0.2.0) (https://github.com/docxology/template_autoresearch_project/releases/tag/v0.2.0)
PDF SHA-256: 922d12425ac8649d214fc38ad24a0379802d3de7b27f7bd2c9ef659b282a5c85

## Keywords

autoresearch · reproducible research · machine learning benchmark · artifact readiness · human review · local artifact integrity

## Publication Details

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.20417017](https://doi.org/10.5281/zenodo.20417017) |
| **Published** | 2026 |
| **Version** | 0.2 |
| **Zenodo record** | https://zenodo.org/records/20417017 |
| **GitHub release** | https://github.com/docxology/template_autoresearch_project/releases/tag/v0.2.0 |
| **Source repository** | https://github.com/docxology/template_autoresearch_project |

## Files

- `Friedman_2026_Bounded_922d1242.pdf` - Zenodo PDF

## Citation

> Friedman, D. A. (2026). *Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task*. Zenodo. https://doi.org/10.5281/zenodo.20417017

## Related

- Zenodo record: https://zenodo.org/records/20417017
- GitHub release: https://github.com/docxology/template_autoresearch_project/releases/tag/v0.2.0
- Source repository: https://github.com/docxology/template_autoresearch_project
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
