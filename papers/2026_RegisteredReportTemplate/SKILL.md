---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Registered Report Template: Preregistration, Deviations, and Claim Boundaries"
description: "This document is a template, not an empirical study. It demonstrates the registered-report workflow end to end: locking a preregistration, validating its completeness, executing the registered analysis plan against deterministic demonstration data, a..."
tags: ["registered-report", "preregistration", "replication", "deviation-ledger"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Registered Report Template: Preregistration, Deviations, and Claim Boundaries*. Zenodo."
doi: "10.5281/zenodo.21298892"
---

# Registered Report Template: Preregistration, Deviations, and Claim Boundaries

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: registered report, preregistration, replication, deviation ledger.

## Methods

Primary methods and techniques applied in this work:

- **Content-hashed registration freeze plus completeness validation** — The registration is deep-copied and stamped with a SHA-256 hash over sorted-key JSON, then checked for required sections such as hypotheses, outcomes, exclusion rules, and analysis plan.
- **Seeded synthetic two-group dataset (n = 24 per group)** — Instead of real data, a seeded generator draws control values from Normal(0, 1) and treatment values from Normal(0.8, 1) to demonstrate the workflow.
- **Two-sided label-permutation test with 2000 shuffles and add-one correction** — The registered primary model tests the group mean difference at alpha = 0.05 using 2000 seeded label shuffles.
- **Deviation ledger classifying executed elements as ok, warning, or error** — build_deviation_ledger records each executed outcome and model and grades unregistered elements by whether a documented rationale exists.
- **Deliberately plan-divergent demo analysis to exercise the ledger** — The demo adds a secondary_score endpoint and swaps the permutation test for a linear model, each with a rationale, to show how deviations are recorded.

## Key Findings

Core contributions and results:

- On the synthetic data the registered test gives an observed mean difference of 1.003 and a two-sided permutation p-value of 0.0005, with 0 of 2000 shuffles at least as extreme.
- With both documented deviations, the review packet stays valid, keeps primary_score as the only confirmatory outcome, and reports an integrity score of 0.9.
- The author states that the result says nothing about any real-world phenomenon, because the data are synthetic and the effect is injected by construction.
- The template turns registered-report discipline into code checks, such as a content hash that makes silent edits to the locked plan detectable.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21298892
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-10T19:31:16Z

## Prerequisites

- Familiarity with registered report, preregistration, replication
- Background in Computational fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21298892`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
