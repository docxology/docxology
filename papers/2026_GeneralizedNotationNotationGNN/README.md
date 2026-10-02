<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 GeneralizedNotationNotation (GNN)

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.7803313-blue)](https://doi.org/10.5281/zenodo.7803313)

---

## Abstract

> Active Inference offers a unifying account of perception, learning, and action under the free energy principle, yet the generative models at its core are still communicated ad hoc: scattered across prose descriptions, bespoke notebooks, and framework-specific code that rarely agree. This fragmentation makes published models hard to reproduce, compare, or port between tools, and it raises the barrier for newcomers learning the formalism. GeneralizedNotationNotation (GNN) addresses this gap with a standardized, human- and machine-readable text language for specifying Active Inference generative models, paired with a 25-step processing pipeline that transforms a single specification into validation, visualization, simulation, and analysis artifacts. A GNN file denotes a generative model, and the language lets that model take the several shapes the field actually uses: the notation blocks a file declares — categorical A/B/C/D[/E] tensors, linear-Gaussian system matrices F/H/Q/R with a Gaussian prior, per-agent and per-level compositions — fix its model kind, which the pipeline classifies structurally and carries through rendering and execution, recording explicitly which registered backends can render and run a model of each kind and which report it unsupported. GNN's "Triple Play" treats each model as three coordinated views — a textual specification, graphical visualizations, and executable cognitive models — so that one source yields consistent outputs across modalities. The framework spans 32 exemplar specifications (27 discrete-state and 5 continuous linear-Gaussian) across 9 model families and 10 registered rendering backends, with explicit gates for cross-format semantic fidelity and cross-framework reliability. GNN 3.0.0 layered safe-by-design long-running orchestration on top of this language and pipeline — durable observation streams, resumable run sessions, and auditable container plans that generate, validate, and replay data only, with no live infrastructure mutation. We describe the language, the model kinds it denotes, the pipeline architecture, and the validation that confirms specifications round-trip faithfully across formats and execute across multiple simulation backends — with coverage gaps recorded as explicit profiled-unsupported statuses rather than silently omitted — establishing GNN as reproducible, interoperable infrastructure for communicating Active Inference models.

## Keywords

`active inference` · `generative models` · `cognitive modeling` · `notation system` · `reproducibility` · `computational neuroscience` · `bayesian inference` · `standards` · `gnn` · `python`

## Methods

- **Parsing and structured export** — Parses plain-text model specifications into an internal representation and structured export formats, retaining declared model vocabulary.
- **Model-kind type checking and validation** — Checks state spaces, observation modalities, control factors, matrix dimensions, and kind-specific shape contracts before code generation.
- **Kind-aware model rendering** — Carries structurally determined model kinds into rendering and execution, recording which backends can handle each kind and which report it unsupported.
- **Semantic fidelity and cross-framework gates** — Provides reproducible commands for testing semantic preservation in round trips and comparing generated model structure across backend implementations.

## Key Findings

- The manuscript presents the Triple Play as text, graphical, and executable views derived from a shared model specification.
- At the manuscript snapshot, the framework covers 32 exemplar specifications across nine model families and ten registered rendering backends.
- The manuscript reports profiled execution gaps for continuous and hierarchical models, and a deliberate render-only scope for structural models; it does not claim that every model executes on every backend.
- The manuscript specifies reproducible validation commands and explicitly avoids asserting a fixed passing-check count.
- The manuscript describes long-running orchestration contracts that generate, validate, and replay data without mutating live infrastructure.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [ActiveInferenceInstitute/Generalized_Notation_Notation](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation)
- DOI: [10.5281/zenodo.7803313](https://doi.org/10.5281/zenodo.7803313)
- Artifact DOI: [10.5281/zenodo.22985529](https://doi.org/10.5281/zenodo.22985529)
- Zenodo record: [https://zenodo.org/records/22985529](https://zenodo.org/records/22985529)
- PDF: [GeneralizedNotationNotation_v3.6.0.pdf](GeneralizedNotationNotation_v3.6.0.pdf)
- PDF SHA-256: acb7749c561b26562064421ca2f7fbca68c8b0e8a955082e5d5a3e28b50bd784

## Citation

> Daniel Ari Friedman (2026). *GeneralizedNotationNotation (GNN)*. Zenodo. DOI: 10.5281/zenodo.7803313. URL: https://doi.org/10.5281/zenodo.7803313.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
