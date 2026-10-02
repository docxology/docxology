<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 🧠 A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring

**Daniel Ari Friedman, Joel Dietz** (2026) · *Active Inference Journal*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.19461933-blue)](https://doi.org/10.5281/zenodo.19461933)

---

## Abstract

> No prior automated system tracks hypothesis-level evidence across the full Active Inference and Free Energy Principle (FEP) literature. Manual synthesis cannot keep pace with a field that has grown at a compound annual rate of 20.36% across 2005–2026, and the FEP’s theoretical generality has invited falsifiability critiques that only hypothesis-specific evidence profiling can address. Building on pioneering systematic manual annotation paired with ontology-based anal- ysis at the scale of hundreds of papers, we present a computational meta-analysis framework that automates and scales this approach. The pipeline retrieves literature from arXiv, Semantic Scholar, and OpenAlex, deduplicating 𝑁 = 819 papers via a canonical identifier hierarchy (DOI > arXiv ID > Semantic Scholar ID > OpenAlex ID). It classifies papers into a three-tier taxonomy spanning eight categories: A (Core Theory), B (Tools & Translation), and C (Application Domains). An LLM-powered extraction system then evaluates each abstract against eight core hypotheses, producing structured nanopublications—each encoding directionality, a confidence score, and natural-language reasoning—that populate an RDF-compatible knowledge graph scored by a citation-weighted evidence function. All extracted assertions are automatically generated and have not been manually validated; hypothesis scores should be considered preliminary. The resulting evidence landscape reveals a field where application domains (Domain C, 64.0%) collectively dominate the corpus, with tools development (Domain B, 20.8%)—including pymdp, RxInfer.jl, and interpretable alternatives such as Free Energy Projective Simulation—and core theory (Domain A, 15.2%) rounding out the taxonomy. Non-negative matrix factorization identifies 5 latent topics that cross-cut the keyword taxonomy, and citation network analysis exposes a sparse yet structured graph (2,176 intra-corpus edges out of 29,323 total outgoing references—only 7.4% reference resolution, reflecting the corpus’s specialised scope rather than the underlying citation density of any single paper) anchored by pronounced hub papers. Hypothesis scores cluster into three tiers: a broad consensus tier (score > 0.83) covering five hypotheses—H7 Morphogenesis, H2 AIF Optimality, H4 Predictive Coding, H6 Clinical Utility, and H5 Scalability; a near-consensus boundary (H8 Language AIF, score ≈+0.83); a moderate debate tier (H3 Markov Blanket Realism, ≈+0.78); and a diffuse tier (H1 FEP Universality, ≈+0.48) where a large neutral plurality reflects the principle’s broad invocation without explicit empirical test—though absolute score magnitudes are inflated by publication bias and linguistic asymmetry in academic writing, making relative rankings and temporal trajectories more reliable than point estimates. By demonstrating that automated LLM-driven assertion extraction—operating without human-validated ground truth—can generate scalable, queryable representations of scientific evidence, this work provides a reusable architecture for living literature reviews—continuously updated knowledge graphs that track hypothesis-level consensus across rapidly evolving fields. All code, results, and methods to reproduce this manuscript are open source at https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis/ .

## Keywords

`Active Inference` · `meta-analysis` · `nanopublications` · `assertion extraction` · `citation-weighted scoring` · `literature review architecture` · `Free Energy Principle` · `computational bibliography`

## Methods

- **Multi-source retrieval (arXiv, Semantic Scholar, OpenAlex) with ID-hierarchy dedup** — Literature was retrieved from three databases and deduplicated to 819 papers using a DOI > arXiv > Semantic Scholar > OpenAlex identifier hierarchy.
- **Keyword-based A/B/C domain taxonomy (200+ indicators, 8 categories)** — Papers were classified into Core Theory, Tools & Translation and Application Domains by keyword matching rather than expert annotation.
- **Abstract-only LLM assertion extraction with gemma3:4b on local Ollama** — Each abstract was assessed against eight hypotheses via a JSON-schema prompt returning direction, confidence and reasoning.
- **Nanopublication knowledge graph with citation-weighted hypothesis scoring** — Extracted assertions became structured nanopublications in an RDF-compatible knowledge graph scored by a citation-weighted evidence function.
- **NMF topic modelling and intra-corpus citation network analysis** — Non-negative matrix factorization was used to find latent topics, and citation edges among corpus papers were analyzed for network topology.

## Key Findings

- Application domains dominated the corpus (Domain C 64.0%), with tools (B) at 20.8% and core theory (A) at 15.2%.
- The citation network was sparse: 2,176 intra-corpus edges out of 29,323 outgoing references (7.4% resolution), anchored by hub papers.
- LLM-derived hypothesis scores clustered into tiers, with H1 FEP Universality in a diffuse tier (about +0.48) where a large neutral plurality reflects broad invocation of the principle without explicit empirical test.
- The authors caution that all assertions are automatically generated and not manually validated, so hypothesis scores are preliminary.
- Preliminary experiments indicated about 15-20% over-extraction, and error rates for the 819-paper run were not quantified.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- DOI: [10.5281/zenodo.19461933](https://doi.org/10.5281/zenodo.19461933)
- Zenodo record: [https://zenodo.org/records/19461933](https://zenodo.org/records/19461933)
- PDF: [act_inf_metaanalysis_v2_04-30-2026.pdf](act_inf_metaanalysis_v2_04-30-2026.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/19461933)

## Citation

> Daniel Ari Friedman, Joel Dietz (2026). *A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring*. Active Inference Journal. DOI: 10.5281/zenodo.19461933. URL: https://doi.org/10.5281/zenodo.19461933.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
