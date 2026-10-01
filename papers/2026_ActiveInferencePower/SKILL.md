---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Active Inference Power Suite: Conditional Statistical Power under Controlled Generative Settings"
description: "<p class=\"p1\">Statistical power is an investigator-facing operating characteristic of an adaptive-study design. Before simulation, the investigator fixes an agent-side model, evaluator-side process, testing setting, policy, and replication plan. Each..."
tags: ["multiple-testing", "false-discovery-rate", "benjamini-hochberg", "statistical-power", "active-inference", "pymdp", "sequential-hypothesis-testing", "reproducible-research"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2026). *Active Inference Power Suite: Conditional Statistical Power under Controlled Generative Settings*. Zenodo."
doi: "10.5281/zenodo.21695160"
---

# Active Inference Power Suite: Conditional Statistical Power under Controlled Generative Settings

**Daniel Ari Friedman** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: multiple testing, false discovery rate, Benjamini-Hochberg, statistical power.

## Methods

Primary methods and techniques applied in this work:

- **Power estimated as an operating characteristic of an investigator-declared design** — Defines power over replications of a declared model/process/setting/policy design, scoring traces against evaluator-only hidden truth.
- **Seeded Monte Carlo comparison of 9 FWER/FDR correction procedures** — Compares Bonferroni, Šidák, Holm, Hochberg, BH, BY, Storey, adaptive BH and weighted BH on a seeded two-groups design with MC SE bands.
- **Dependence-regime stress grid for BH and BY** — Evaluates BH and BY FDR and power under negative equicorrelation, independence, positive-factor and block covariance regimes.
- **Discrete-state active-inference agent: posterior threshold vs BH on calibrated p-values** — Runs identical streams through a posterior-threshold decision and a BH-calibrated evidence rule under strong and weak evidence regimes.
- **Action-in-the-loop policies with sensing reliability, cost and stopping** — Compares fixed-horizon, posterior-cutoff, information-gain, cost-aware, posterior-sampling and e-process stopping policies in a synthetic action loop.

## Key Findings

Core contributions and results:

- In the configured design, FWER-oriented procedures reached power 0.315–0.321 while FDR-oriented procedures reached 0.430–0.749, framed as the expected trade-off, not dominance.
- Storey's paired power gain over BH was about 0.073, which the paper stresses is an operating-characteristic comparison, not a validity certificate.
- Under weak evidence the posterior-threshold policy had FDR 0.153 and FWER 0.366, while the calibrated BH policy made no rejections, illustrating a calibration gap.
- Across the dependence grid, BH estimates stayed within the finite-simulation band and BY stayed more conservative; the paper states this is not a new PRDS proof.
- The paper concludes power numbers should not be carried into a new design; adaptive actions change data path, cost and evidence contract together.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21695160
- PDF SHA-256: 24fa25a4f29affcfd92c8c001ff6487a0c36960c6b4f38ed4419984fc8743cbf
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:58Z

## Prerequisites

- Familiarity with multiple testing, false discovery rate, Benjamini-Hochberg
- Background in Active Inference fundamentals
- Access to source repository: ActiveInferenceInstitute/active_inference_power

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21695160`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
