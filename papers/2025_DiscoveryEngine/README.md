<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 The Discovery Engine: A Framework for AI-Driven Synthesis and Navigation of Scientific Knowledge Landscapes

**Vladimir Baulin, Austin Cook, Daniel Friedman, Janna Lumiruusu, Andrew Pashea, Shagor Rahman, Benedikt Waldeck** (2025) · *ArXiv*

[![DOI](https://img.shields.io/badge/DOI-10.48550%2FarXiv.2505.17500-blue)](https://doi.org/10.48550/arXiv.2505.17500)

---

## Abstract

> The prevailing model for disseminating scientific knowledge relies on individual publications dispersed across numerous journals and archives. This legacy system is ill suited to the recent exponential proliferation of publications, contributing to insurmountable information overload, issues surrounding reproducibility and retractions. We introduce the Discovery Engine, a framework to address these challenges by transforming an array of disconnected literature into a unified, computationally tractable representation of a scientific domain. Central to our approach is the LLM-driven distillation of publications into structured "knowledge artifacts," instances of a universal conceptual schema, complete with verifiable links to source evidence. These artifacts are then encoded into a high-dimensional Conceptual Tensor. This tensor serves as the primary, compressed representation of the synthesized field, where its labeled modes index scientific components (concepts, methods, parameters, relations) and its entries quantify their interdependencies. The Discovery Engine allows dynamic "unrolling" of this tensor into human-interpretable views, such as explicit knowledge graphs (the CNM graph) or semantic vector spaces, for targeted exploration. Crucially, AI agents operate directly on the graph using abstract mathematical and learned operations to navigate the knowledge landscape, identify non-obvious connections, pinpoint gaps, and assist researchers in generating novel knowledge artifacts (hypotheses, designs). By converting literature into a structured tensor and enabling agent-based interaction with this compact representation, the Discovery Engine offers a new paradigm for AI-augmented scientific inquiry and accelerated discovery.

## Keywords

`Discovery Engine` · `scientific knowledge synthesis` · `LLM-driven distillation` · `knowledge artifacts` · `Conceptual Tensor` · `knowledge graphs` · `AI-assisted scientific inquiry`

## Methods

- **Template-guided LLM distillation of papers into knowledge artifacts** — LLMs, guided by field-specific templates based on a universal conceptual schema, extract structured components linked to source evidence.
- **Encoding artifacts into a high-dimensional Conceptual Tensor** — Knowledge artifacts are encoded into a tensor whose modes index concepts, methods, parameters and relations, from which graphs or vector spaces are unrolled.
- **Case study: intelligent soft matter corpus with expert template refinement** — A soft-matter publication corpus was distilled, the template refined via researcher feedback cycles, and AI agents analyzed the resulting CNM for themes and gaps.
- **Case study: DE pipeline meta-applied to HCI and KG interaction literature** — HCI, knowledge-graph visualization and XAI papers were distilled into a CNM used to derive design principles and AI-assisted UI concepts for the DE platform.
- **React/TypeScript frontend building a client-side CNM graph from Markdown** — The open-source frontend parses Markdown files via a cnmBuilder.ts utility and visualizes the CNM with 3d-force-graph.

## Key Findings

- Introduces the Discovery Engine as a methodology and conceptual platform for moving from document-centric literature to synthesized, structured knowledge repositories.
- Proposes that human-interpretable views such as the CNM knowledge graph and semantic vector spaces can be generated from the central tensor representation.
- In the soft matter case study, the synthesized CNM served as the basis for a collaborative expert-AI perspective outlining challenges and a research roadmap.
- In the platform design case study, AI-assisted synthesis yielded conceptual designs for modules such as Knowledge Card summaries and a Hypothesis Workbench.
- The authors state that effectiveness depends on continued LLM advances and template governance, and that scaling to very large disciplines is an engineering hurdle.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.48550/arXiv.2505.17500](https://doi.org/10.48550/arXiv.2505.17500)
- PDF: [2025_DiscoveryEngine.pdf](2025_DiscoveryEngine.pdf)
- PDF SHA-256: Not recorded

## Citation

> Vladimir Baulin, Austin Cook, Daniel Friedman, Janna Lumiruusu, Andrew Pashea, Shagor Rahman, Benedikt Waldeck (2025). *The Discovery Engine: A Framework for AI-Driven Synthesis and Navigation of Scientific Knowledge Landscapes*. ArXiv. DOI: 10.48550/arXiv.2505.17500. URL: https://doi.org/10.48550/arXiv.2505.17500.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
