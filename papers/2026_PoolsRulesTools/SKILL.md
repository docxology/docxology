---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "Pools, Rules, and Tools: A Template-Integrated Resource Architecture"
description: "No abstract is recorded for this work yet; see the DOI or bibliography link."
tags: ["poolsrulestools"]
domain: "Active Inference"
citation: "Daniel Ari Friedman (2026). *Pools, Rules, and Tools: A Template-Integrated Resource Architecture*. Zenodo."
doi: "10.5281/zenodo.21298888"
---

# Pools, Rules, and Tools: A Template-Integrated Resource Architecture

**Daniel Ari Friedman** (2026) · Active Inference

## Context

This work addresses topics in **Active Inference**: PoolsRulesTools.

## Methods

Primary methods and techniques applied in this work:

- **Four-module reader architecture: fonds_reader, rules_applier, tools_invoker, integration** — One Python reader module per resource category (data pools, governance rules, executable tools) plus an orchestrator that runs all three.
- **Typed YAML manifests (fonds.yaml, rules.yaml, tools.yaml) for discovery** — Each shared resource exposes a typed manifest that its reader uses for discovery and validation; consumers never modify resources.
- **Repo-root-relative path resolution and graceful-degradation readers** — Paths resolve via pathlib parents[N]; readers check existence, catch yaml.YAMLError, log warnings and return empty values rather than raising.
- **{{TOKEN}} injection of runtime statistics into the manuscript** — A script hydrates manuscript tokens from integration-run JSON just before pandoc renders, so counts in the prose come from the pipeline.
- **Real-file tests (no mocks), property-based tests and a negative control** — Nine test files exercise the eight src/ modules with real YAML/BibTeX files; one test monkeypatches the source to prove tokens are live-wired.

## Key Findings

Core contributions and results:

- In a representative run, the integration demo loaded 3 fonds, validated 2 rule sets, discovered 3 tools and processed 8 bibliography entries.
- The paper claims typed manifests shift failure detection from runtime to pipeline startup, which it frames as an improvement for reproducibility.
- It proposes a three-level resilience design (resource absence, schema malformation, script absence) so the pipeline reports failures informatively instead of crashing.
- The authors argue a manifest-and-reader pattern avoids the packaging overhead of shared libraries, the lost validation of symlinks, and the setup burden of environment variables.
- Stated limitations include structural-only validation by default, no concurrency handling against parallel writers, and a small-scale design assumption.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for related publications.

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.21298888
- PDF SHA-256: See zenodo_record
- Pairing confidence: unknown
- Last checked: 2026-07-10T19:31:22Z

## Prerequisites

- Familiarity with PoolsRulesTools
- Background in Active Inference fundamentals
- Access to source repository: N/A

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.21298888`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
