---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Codomyrmex: An Artificial Ecology for Agentic Software Development"
description: "Agentic software can preserve task state while still forgetting the consequences of prior actions. Codomyrmex studies a narrow control-plane question: after a caller reports a failed action at one software location, can the system deterministically i..."
tags: ["ai-agents", "model-context-protocol", "mcp", "multi-agent", "orchestration", "colony-control-plane", "stigmergy", "artificial-ecology", "agentic-software-engineering", "falsification-worker"]
domain: "Computational"
citation: "Daniel Ari Friedman (2026). *Codomyrmex: An Artificial Ecology for Agentic Software Development*. Zenodo."
doi: "10.5281/zenodo.21750800"
artifact_doi: "10.5281/zenodo.21750801"
---

# Codomyrmex: An Artificial Ecology for Agentic Software Development

**Daniel Ari Friedman** (2026) · Computational

## Context

This work addresses topics in **Computational**: ai-agents, model-context-protocol, mcp, multi-agent.

## Methods

Primary methods and techniques applied in this work:

- **Colony Control Plane with 8 named subsystems** — The implementation separates signal storage, resource accounting, actuation gating, consequence records, role inference, pruning, deterministic falsification, and integration.
- **Ternary EXECUTE/HOLD/REFUSE gate with weighted bounded score** — Budget, effective local hazard, trust credit, and proposal completeness are combined into a weighted score with hard overrides that route each proposal.
- **Stigmergic signal field with FAILURE and RISK pressure at target locations** — Reported failures and prospective risks are stored separately in a process-local field, and the gate uses their maximum as the local hazard.
- **Contract test suite using real subsystem instances** — Tests check same-target inhibition, cross-target isolation, linear decay recovery, score bounds, trust updates, and interface behavior.
- **Paired deterministic replay of same-target vs. unrelated-target proposals** — Identical proposals are evaluated with and without a reported failure at the target location to test failure-to-gate coupling.

## Key Findings

Core contributions and results:

- The scoped Colony Kernel surface has 819 passing tests with 76.6% branch coverage, 0 Ruff errors, and 0 ty diagnostics.
- After a reported failure, the paired replay moves the same-target proposal from 0.875/EXECUTE to 0.725/HOLD while an unrelated target is unchanged.
- The author states these results support reproducible software contracts, not ecological optimality, calibrated risk, production harm reduction, or generalization to external workloads.
- The proposed comparative benchmark has not been run, and no raw trial traces are included in this release.
- Default state is in memory, so the artifact does not support claims that pressure, trust, or gate state survive process restarts, model swaps, or deployment across machines.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21750800
- PDF SHA-256: eda76ad12a50bce01b113894c785e0915b6ba367f5bf67d17c8f586416102b93
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:58Z
- Artifact DOI: 10.5281/zenodo.21750801

## Prerequisites

- Familiarity with ai-agents, model-context-protocol, mcp
- Background in Computational fundamentals
- Access to source repository: docxology/codomyrmex

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21750800`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
