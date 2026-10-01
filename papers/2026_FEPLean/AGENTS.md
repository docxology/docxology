<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics

**Paper**: Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics (2026)
**Domain**: Active Inference
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for FEPLean
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Curated catalog of 50 FEP topics as namespaced Lean 4 sketches against Mathlib4, Native lake env lean verification on a pinned Lean/Mathlib v4.29.0 stack, LLM-assisted commentary pipeline (Hermes/OpenGauss, kimi-k2.6 via OpenRouter)
- Identifies findings: On the pinned Lean 4 / Mathlib4 v4.29.0 stack, the shipped catalog compiles 50/50 sorry-free., The Hermes-assisted Gauss run run_20260424_064334 achieved 50/50 clean compiles with 0 sorry and 0 errors., Constructions that already typecheck in today's Mathlib4 include finite-set probability, Bayesian updating, finite-space KL divergence and variational free-energy bounds.
- Maps contributions to Active Inference literature

### 🎓 EDUCATOR
- Creates learning pathways for Active Inference concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics to related works in the bibliography
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

### Related Software
- https://github.com/ActiveInferenceInstitute/fep_lean
