# Cognitive Integrity Framework: Computational Validation and Empirical Analysis (Part 2 of 3: Implementation, Empirical Analysis, and Adversarial Evaluation)

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22134545.svg)](https://doi.org/10.5281/zenodo.22134545)

---

## Abstract

This paper presents the computational validation of the Cognitive Integrity Framework (CIF) whose formal foundations are established in Part 1 (DOI: 10.5281/zenodo.18364119). We implement the CIF defense suite --- cognitive firewalls, belief sandboxes, tripwires, drift and anomaly scoring, trust calculus with bounded delegation, provenance tracking, and Byzantine-tolerant consensus --- and evaluate it on an integrated 1,475-item attack corpus spanning fifteen categories, together with a 120-item benign corpus whose harder half carries attack-adjacent vocabulary. Multi-tier evaluation. Real pipeline evaluation across 30 seeds yields a mean detection rate of 86.3% (95% CI 85.5%-87.1%) at an 18.5% false-positive rate on the Claude Code architecture, measured on an injection-only 100-sample-per-seed arm. LLM-backed validation (N=10, Gemma 3 4B) reaches 80-100% across two topologies and is reported as preliminary and underpowered. Colony benchmarks at 20-100 agents reach 81-100% on structured adversarial scenarios, with emergent misalignment the hardest case at 74.3% detection and a 25.5% false-positive rate. Parametric simulation (N=3,800) characterises a 96-100% design-level ceiling across four production architectures, and is labelled a simulation rather than a measurement wherever it appears. Ablation on a 100-attack corpus attributes almost all marginal detection to the Invariants module: the full pipeline reaches 89.0% true-positive rate, removing Invariants costs 65 percentage points, removing the Tripwire costs two, and removing any other module costs nothing the corpus can measure. The layered architecture is therefore only partly borne out, and the paper says so. An undefended control arm places the defense's cost at +0.610 ms at the median and +32 KiB peak. Measured as ranked scorers, the drift score and the firewall pattern matcher fall below chance (AUC 0.374 and 0.383, intervals excluding 0.5). Every quantity the three papers share is derived from a single ledger and gated in continuous integration; no reported number is typed by hand. All experiments are deterministically reproducible at seed 42, and the code, corpora and artifacts are at https://github.com/docxology/cognitive_integrity. This is Part 2 of the three-part Cognitive Security for Multiagent Operators series: - Part 1 (DOI: 10.5281/zenodo.18364119): formal foundations and theoretical analysis - Part 2 (this paper): computational validation and implementation - Part 3+4 merged (DOI: 10.5281/zenodo.18364130): unified practitioner guidance and cross-domain applications

## Keywords

cognitive security · multiagent systems · AI safety · prompt injection · trust calculus · defense in depth

## Artifacts

| Field | Value |
|------|-------|
| **DOI** | [10.5281/zenodo.22134545](https://doi.org/10.5281/zenodo.22134545) |
| **Published** | 2026-08-26 |
| **Version** | 2.0 |
| **Zenodo record** | https://zenodo.org/records/22134545 |

## Files

- `cogsec_multiagent_2_computational_combined.pdf` - Zenodo PDF

## Citation

> Daniel Ari Friedman (2026). *Cognitive Integrity Framework: Computational Validation and Empirical Analysis (Part 2 of 3: Implementation, Empirical Analysis, and Adversarial Evaluation)*. Zenodo. DOI: 10.5281/zenodo.22134545. URL: https://doi.org/10.5281/zenodo.22134545.

## Related

- Zenodo record: https://zenodo.org/records/22134545
- [Full Bibliography](../../pages/BIBLIOGRAPHY.md) · [All Papers](../README.md)
