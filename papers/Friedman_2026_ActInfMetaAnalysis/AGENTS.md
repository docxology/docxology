# AGENTS.md — A Living Meta-Analysis Architecture for Active Inference

**Paper**: A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring (2026) · Zenodo **v2**  
**Area**: Active Inference · computational meta-analysis · nanopublications · living literature review  
**Authors**: Daniel Ari Friedman, Joel Dietz  
**Canonical DOI (v2)**: `10.5281/zenodo.19897664` · [Zenodo record](https://zenodo.org/records/19897664)  
**Prior deposit (v1)**: `10.5281/zenodo.19461934`  
**Repository**: https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis

---

## Agent Roles

### 📖 Research Agent

**Focus**: Deep analysis of the living meta-analysis architecture and how extraction, nanopublications, and scoring interact.

**Tasks**:

- Analyze the pipeline: multi-source retrieval and deduplication, three-tier (A/B/C) taxonomy, LLM-driven assertion extraction against eight core hypotheses, RDF-compatible nanopublications, and citation-weighted evidence scoring over the knowledge graph.
- Evaluate scalability and reproducibility for a corpus on the order of hundreds of deduplicated papers (v2: *N* = 819) spanning 2005–2026 growth dynamics in the Active Inference / FEP literature.
- Map connections to the Free Energy Principle, predictive processing, and falsifiability debates that motivate hypothesis-level evidence profiling.
- Interpret hypothesis score tiers and rankings as *relative* signals (publication bias and linguistic asymmetry caution in v2), not as validated point estimates without human ground truth.

### 🔬 Methods Agent

**Focus**: Methodological rigor and replication.

**Tasks**:

- Document retrieval from arXiv, Semantic Scholar, and OpenAlex; canonical identifier hierarchy (DOI > arXiv ID > Semantic Scholar ID > OpenAlex ID); deduplication outputs.
- Document the eight-category A/B/C taxonomy (core theory, tools & translation, application domains) and cross-cutting topic / citation-network analyses (NMF topics, intra-corpus citation structure).
- Evaluate LLM-based abstract-level extraction: directionality, confidence, natural-language reasoning encoded per nanopublication; limitations (no manual validation of every assertion in v2).
- Verify citation-weighted scoring over the graph and how results are reported (consensus tiers, debate tiers).
- Confirm reproducibility via https://github.com/ActiveInferenceInstitute/act_inf_metaanalysis

### 📚 Citation Agent

**Focus**: Citation context and scholarly impact.

**Tasks**:

- Track citations and impact using DOI `10.5281/zenodo.19897664` (v2); retain `10.5281/zenodo.19461934` for version-chain and early citations to v1.
- Map connections to related works in the Friedman corpus — systematic reviews, ontology work (OntologySUMO), and Active Inference Institute ecosystem papers.
- Identify citing papers and downstream use of the architecture, nanopublication pattern, or open codebase.

### 🔗 Synthesis Agent

**Focus**: Cross-paper and cross-domain connections.

**Tasks**:

- Connect to the broader docxology corpus: Active Inference ecosystem papers (AII_v1–v3), CEREBRUM, FederatedInference, DistributedScience, DiscoveryEngine, and ReproducibleResearch.
- Identify synergies with cognitive security (P3IF, ATLAS, StigmergicAnnotation) and sensemaking where structured knowledge representation matters.
- Link nanopublications and living graphs to open science and FAIR practice.

### 💼 Consultant Agent

**Focus**: Practical application and knowledge transfer.

**Tasks**:

- Support teams porting the architecture to other fast-moving literatures.
- Relate findings to systematic review methods, knowledge graphs, and continuous evidence synthesis.
- Emphasize human validation workflows when LLM extractions feed high-stakes decisions.

## Extraction Log

- **Source PDF (current)**: `act_inf_metaanalysis_v2_04-30-2026.pdf` (Zenodo v2, 2026-04-30)
- **Prior PDF**: `act_inf_metaanalysis_v1_04-19-2026.pdf` (v1 deposit)
- **PDF Status**: Available
- **Documentation Quality**: Aligned to Zenodo v2 metadata and abstract-level description; hand-curated cross-check with repository

## Related Papers

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for the full catalog. Key related entries:

- Friedman_2025_CEREBRUM — Active Inference modeling architecture
- Friedman_2025_DiscoveryEngine — AI-driven synthesis of scientific knowledge landscapes
- Friedman_2026_ReproducibleResearch — Reproducible research pipeline architecture
- Friedman_2024_OntologySUMO — Aligning Active Inference ontology
- Friedman_2023_DistributedScience — Scientific process as multi-scale Active Inference
