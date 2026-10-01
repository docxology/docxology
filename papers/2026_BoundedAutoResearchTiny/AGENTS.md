<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task

**Paper**: Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for BoundedAutoResearchTiny
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Offline MNIST subset: 2000 train / 500 test images, seed 20260525, Bounded candidate search over MLP, softmax, nearest-centroid, patch-attention, Seven-stage AutoResearch pipeline with file-backed ledgers
- Identifies findings: The loop selected exp-mlp-tanh-64 after evaluating 4 of 5 proposed candidates, raising test accuracy from the 82.6% baseline to 89.4%., Diagnostics report macro F1 of 89.4%, a bootstrap accuracy interval of 86.4% to 92.0%, and top-2 accuracy of 95.6%., The selected candidate was top-ranked in 72.5% of deterministic bootstrap resamples, with exp-mlp-relu-32 as runner-up.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects Bounded AutoResearch for a Tiny Reproducible Machine-Learning Task to related works in the bibliography
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
- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

### Related Software
- https://github.com/docxology/template_autoresearch_project
