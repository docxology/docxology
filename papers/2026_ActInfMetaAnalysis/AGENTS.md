<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring

**Paper**: A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring (2026)
**Domain**: Active Inference
**Authors**: Daniel Ari Friedman, Joel Dietz

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for ActInfMetaAnalysis
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Multi-source retrieval (arXiv, Semantic Scholar, OpenAlex) with ID-hierarchy dedup, Keyword-based A/B/C domain taxonomy (200+ indicators, 8 categories), Abstract-only LLM assertion extraction with gemma3:4b on local Ollama
- Identifies findings: Application domains dominated the corpus (Domain C 64.0%), with tools (B) at 20.8% and core theory (A) at 15.2%., The citation network was sparse: 2,176 intra-corpus edges out of 29,323 outgoing references (7.4% resolution), anchored by hub papers., LLM-derived hypothesis scores clustered into tiers, with H1 FEP Universality in a diffuse tier (about +0.48) where a large neutral plurality reflects broad invocation of the principle without explicit empirical test.
- Maps contributions to Active Inference literature

### 🎓 EDUCATOR
- Creates learning pathways for Active Inference concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects A Living Meta-Analysis Architecture for Active Inference: Assertion Extraction, Nanopublications, and Hypothesis Scoring to related works in the bibliography
- Maps paper-to-software relationships
- Updates cross-domain connections

---

## Extraction Log

| Source | Agent | Action | Status |
|--------|-------|--------|--------|
| Metadata | ARCHIVIST | Cataloged metadata | ✅ |
| Metadata | RESEARCHER | Extracted methods/findings | ✅ |
| Metadata | EDUCATOR | Generated documentation | ✅ |

## Cross-References

### Related Papers
- [2018_WoodliceAndMen](../2018_WoodliceAndMen/)
- [2020_BehaviorEngineering](../2020_BehaviorEngineering/)
- [2021_ModelingConflict](../2021_ModelingConflict/)
