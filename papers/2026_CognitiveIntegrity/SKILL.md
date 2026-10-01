---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Cognitive Integrity Framework: Formal Foundations (Part 1 of 3: Theoretical Foundations)"
description: "Multiagent AI systems introduce cognitive attack surfaces absent in single-model inference. When agents delegate to agents, forming beliefs about beliefs through recursive trust hierarchies, manipulation of reasoning processes—rather than mere data c..."
tags: ["cognitive-integrity", "multiagent-security", "cognitive-security", "active-inference", "category-theory", "formal-foundations", "threat-modeling"]
domain: "Cognitive Security"
citation: "Daniel Ari Friedman (2026). *Cognitive Integrity Framework: Formal Foundations (Part 1 of 3: Theoretical Foundations)*. Zenodo."
doi: "10.5281/zenodo.18364118"
---

# Cognitive Integrity Framework: Formal Foundations (Part 1 of 3: Theoretical Foundations)

**Daniel Ari Friedman** (2026) · Cognitive Security

## Context

This work addresses topics in **Cognitive Security**: cognitive integrity, multiagent security, cognitive security, Active Inference.

## Methods

Primary methods and techniques applied in this work:

- **Trust Calculus with bounded, exponentially decaying delegation** — Formalizes delegated trust with decay factor δ per delegation step and proves bounds by induction on chain depth.
- **Defense Composition Algebra (series/parallel detection)** — Derives detection rates for series and parallel composition of defenses, assuming independent detection events.
- **Information-theoretic attack/detection bounds** — Relates attack entropy, mutual information with detector output, and channel capacity to bound detection rate and attack impact.
- **Five-class adversary hierarchy (Ω1–Ω5)** — Defines external, peripheral, agent-level, coordination, and systemic adversary classes and maps them to multiagent architectures and OWASP Agentic Top 10.
- **Operational semantics, invariants, and model-checking configurations** — Specifies operational semantics for message passing and trust updates, belief/goal/trust invariants, and model-checking setups for safety properties.

## Key Findings

Core contributions and results:

- Trust Boundedness theorem: delegated trust over a chain of depth d is at most δ^d, so trust cannot be amplified and vanishes exponentially with depth.
- The paper states a stealth-impact tradeoff as a theorem: high-impact attacks are easier to detect, while stealthy attacks have limited effect.
- The framework formalizes five architectural defenses with composition rules for reasoning about layered security.
- The author notes guarantees depend on assumptions (honest orchestrator, n ≥ 3f+1, authenticated channels) and that the O(n²) trust matrix limits deployment to moderate agent counts.
- Semantic-equivalence attacks, sub-threshold progressive drift, and orchestrator compromise are identified as formally difficult to detect.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2020_EmergentTeams](../2020_EmergentTeams/)
- [2020_FacilitatorsCatechism](../2020_FacilitatorsCatechism/)
- [2020_GreatPreset](../2020_GreatPreset/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.18364118
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-06-30T23:26:08Z

## Prerequisites

- Familiarity with cognitive integrity, multiagent security, cognitive security
- Background in Cognitive Security fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.18364118`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
