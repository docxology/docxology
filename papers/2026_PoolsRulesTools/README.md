<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Pools, Rules, and Tools: A Template-Integrated Resource Architecture

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298888-blue)](https://doi.org/10.5281/zenodo.21298888)

---

## Abstract

> Research software repositories in monorepo configurations accumulate three categories of shared resources that individual projects must consume without re-implementing discovery logic: data pools (bibliographies, contacts, datasets), governance rules (style guides, coverage thresholds, citation schemas), and executable tools (code executors, validators, skill invocations). Without a canonical integration pattern, projects either duplicate discovery logic or silently ignore resources that fail to load — both outcomes degrade reproducibility and collaborative cohesion [Wilson et al., 2014, Taschuk and Wilson, 2017]. This paper presents template_pools_rules_tools, a meta-project exemplar that demonstrates how a single project can programmatically discover, validate, and exercise all three resource categories with zero tight coupling to any specific resource instance. The exemplar comprises eight Python modules — three resource readers (fonds_reader, rules_applier, tools_invoker), an orchestrator (integration), a semantic rule evaluator (strong_rule_evaluator), a figure generator (figures), a manuscript-token generator (manuscript_variables), and shared type definitions (type_defs) — plus six thin orchestration scripts and a fully token-injected manuscript pipeline. The architecture (fig. 1) separates resource ownership from resource consumption. Resources live in top-level fonds/, rules/, and tools/ directories and are never modified by consumers. Each resource exposes a typed manifest (fonds.yaml, rules.yaml, tools.yaml) that the corresponding reader module uses for discovery and validation. All readers implement graceful fallbacks: they return None or empty collections when a resource is absent, log a warning via the standard library logging module, and allow the integration pipeline to continue. This revision extends the original three-figure presentation to eight content figures plus a cover illustration — a fond taxonomy (fig. 2), a rule hierarchy (fig. 3), a tool invocation contract (fig. 4), a three-level resilience diagram (fig. 8), and a script pipeline flow (fig. 6) — so that every structural claim in the prose has a corresponding visual. In a representative pipeline run, the integration demo loaded 3 fonds, validated 2 rule sets, discovered 3 tools, and processed 8 bibliography entries — all reported as structured JSON that populates manuscript variable tokens at render time. Tests covering the eight src/ modules (across nine test files) achieve well above the required &gt;=90% combined line coverage and use real file paths rather than mocks, ensuring that reported counts are genuine — run uv run pytest … --cov-report=term for the current test count and coverage percentage rather than trusting a number printed here. The template_pools_rules_tools exemplar provides a reference implementation that any project in the template repository can consult when designing its own resource-consumption layer.

## Methods

- **Four-module reader architecture: fonds_reader, rules_applier, tools_invoker, integration** — One Python reader module per resource category (data pools, governance rules, executable tools) plus an orchestrator that runs all three.
- **Typed YAML manifests (fonds.yaml, rules.yaml, tools.yaml) for discovery** — Each shared resource exposes a typed manifest that its reader uses for discovery and validation; consumers never modify resources.
- **Repo-root-relative path resolution and graceful-degradation readers** — Paths resolve via pathlib parents[N]; readers check existence, catch yaml.YAMLError, log warnings and return empty values rather than raising.
- **{{TOKEN}} injection of runtime statistics into the manuscript** — A script hydrates manuscript tokens from integration-run JSON just before pandoc renders, so counts in the prose come from the pipeline.
- **Real-file tests (no mocks), property-based tests and a negative control** — Nine test files exercise the eight src/ modules with real YAML/BibTeX files; one test monkeypatches the source to prove tokens are live-wired.

## Key Findings

- In a representative run, the integration demo loaded 3 fonds, validated 2 rule sets, discovered 3 tools and processed 8 bibliography entries.
- The paper claims typed manifests shift failure detection from runtime to pipeline startup, which it frames as an improvement for reproducibility.
- It proposes a three-level resilience design (resource absence, schema malformation, script absence) so the pipeline reports failures informatively instead of crashing.
- The authors argue a manifest-and-reader pattern avoids the packaging overhead of shared libraries, the lost validation of symlinks, and the setup burden of environment variables.
- Stated limitations include structural-only validation by default, no concurrency handling against parallel writers, and a small-scale design assumption.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.21298888](https://doi.org/10.5281/zenodo.21298888)
- Zenodo record: [https://zenodo.org/records/21298888](https://zenodo.org/records/21298888)
- PDF: [Friedman_2026_Pools_6908c1a0.pdf](Friedman_2026_Pools_6908c1a0.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/21298888)

## Citation

> Daniel Ari Friedman (2026). *Pools, Rules, and Tools: A Template-Integrated Resource Architecture*. Zenodo. DOI: 10.5281/zenodo.21298888. URL: https://doi.org/10.5281/zenodo.21298888.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
