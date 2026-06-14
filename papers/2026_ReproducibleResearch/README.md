# 📦 A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication

**Daniel Ari Friedman** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20669283-blue)](https://doi.org/10.5281/zenodo.20669283)

---
<!-- Schema.org structured data for search engines -->
<!--
{"@context":"https://schema.org","@type":"ScholarlyArticle","headline":"A template/ approach to Reproducible Generative Research","abstract":"template/ applies the principle of Infrastructure as Code to the research lifecycle, making the manuscript, test suite, and provenance chain version-controlled, deterministically buildable, and independently verifiable. Built on a Two-Layer Architecture separating 12 reusable infrastructure subpackages from self-contained project workspaces, connected by an eight-stage build pipeline.","keywords":["reproducible research","infrastructure as code","build pipeline","Zero-Mock testing","steganographic watermarking","AI-agent documentation","Model Context Protocol","cryptographic provenance","literate programming","open science"],"author":{"@type":"Person","name":"Daniel Ari Friedman","url":"https://docxology.github.io/docxology/"}}
-->

## Abstract

> The reproducibility crisis in computational research is fundamentally structural: research artifacts are scattered across disconnected tools—LaTeX editors, Jupyter notebooks, ad-hoc shell scripts—with no enforced mechanism to keep code, data, and manuscript synchronized. `template/` applies the principle of Infrastructure as Code to the research lifecycle, making the manuscript, test suite, and provenance chain version-controlled, deterministically buildable, and independently verifiable. It is built on a Two-Layer Architecture that separates 12 reusable infrastructure subpackages (~150 Python modules, validated by ~3,083 tests) from self-contained project workspaces, connected by an eight-stage build pipeline progressing from environment sanitization through test execution (with a Zero-Mock testing policy enforcing 90% project-level and 60% infrastructure-level coverage via real filesystem operations and subprocess invocations), analysis script invocation, Pandoc/XeLaTeX rendering, SHA-256 cryptographic hashing with steganographic watermarking, structural PDF validation, and LLM-assisted review. A Documentation Duality standard equips every directory with both human-readable `README.md` and machine-readable `AGENTS.md` files, while each infrastructure module additionally carries a `SKILL.md`—a structured skill descriptor aligned with the Model Context Protocol—enabling AI agents to locate and invoke module capabilities without hallucinating API signatures. Scalability is demonstrated across three heterogeneous projects achieving 100% pipeline success with zero mock violations. A comparative feature analysis against nine peer tools across fourteen dimensions confirms that `template/` uniquely integrates all eleven distinctive capabilities within a single enforced pipeline.

## Keywords

`reproducible research` · `infrastructure as code` · `build pipeline` · `Zero-Mock testing` · `steganographic watermarking` · `AI-agent documentation` · `Model Context Protocol` · `cryptographic provenance` · `literate programming` · `open science`

## Key Contributions

- Introduces a Two-Layer Architecture separating reusable infrastructure (~150 modules, ~3,083 tests) from self-contained project workspaces
- Defines an eight-stage build pipeline from environment sanitization through LLM-assisted review
- Enforces a Zero-Mock testing policy (90% project / 60% infrastructure coverage) using real filesystem operations
- Implements SHA-256 cryptographic hashing with steganographic watermarking for provenance
- Introduces Documentation Duality (README.md + AGENTS.md) and SKILL.md aligned with Model Context Protocol
- Demonstrates self-referential architecture: the manuscript is rendered by the pipeline it describes
- Provides comparative analysis against 9 peer tools across 14 dimensions

## Methods

- Two-Layer Architecture: infrastructure subpackages vs. project workspaces
- Eight-stage build pipeline: sanitization → tests → analysis → Pandoc/XeLaTeX → SHA-256 → steganographic watermarking → PDF validation → LLM review
- Zero-Mock testing policy enforcing real filesystem and subprocess operations
- Documentation Duality standard with MCP-aligned SKILL.md files
- Comparative feature analysis against Snakemake, Nextflow, CWL, Quarto, Jupyter Book, R Markdown, Overleaf, DVC, OpenAI Prism

## 🎯 Consulting & Tutoring

**Available for AI Research Consulting and Tutoring.** [Contact Daniel Ari Friedman, PhD](https://docxology.github.io/docxology/) for collaboration on reproducible research, build pipelines, and AI-agent documentation.

## Citation

```bibtex
@article{2026_ReproducibleResearch,
  author = {Daniel Ari Friedman},
  title = {{A template/ approach to Reproducible Generative Research: Architecture and Ergonomics from Configuration through Publication}},
  journal = {Zenodo},
  year = {2026},
  doi = {10.5281/zenodo.20669283},
  url = {https://zenodo.org/records/20669283},
}
```

## File Inventory

- `AGENTS.md` (2,924 bytes)
- `README.md` (5,480 bytes)
- `SKILL.md` (3,696 bytes)
- `template_daf_v1_03202026.pdf` (1,153,790 bytes)

## Links

- **Repository**: [github.com/docxology/template](https://github.com/docxology/template)
- **Zenodo**: [zenodo.org/records/20669283](https://zenodo.org/records/20669283)
