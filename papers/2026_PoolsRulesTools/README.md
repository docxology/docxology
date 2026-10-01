<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 Pools, Rules, and Tools: A Template-Integrated Resource Architecture

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.21298888-blue)](https://doi.org/10.5281/zenodo.21298888)

---

## Abstract

> Research software repositories in monorepo configurations accumulate three categories of shared resources that individual projects must consume without re-implementing discovery logic: data pools (bibliographies, contacts, datasets), governance rules (style guides, coverage thresholds, citation schemas), and executable tools (code executors, validators, skill invocations). Without a canonical...

## Keywords

`PoolsRulesTools`

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
