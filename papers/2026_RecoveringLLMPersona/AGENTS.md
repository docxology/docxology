<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — Recovering LLM-Persona Accuracies from Unlabeled Votes

**Paper**: Recovering LLM-Persona Accuracies from Unlabeled Votes (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for RecoveringLLMPersona
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Three system-prompted trader personas as binary judges, Unsupervised NTQR ErrorIndependentEvaluation on vote counts, Deliberately unbalanced 40/24 scenario deck
- Identifies findings: For mistral:latest, unsupervised recovery matched authored-truth accuracies to a mean absolute error of 0.012, within the 0.102 sampling-noise floor., The algebra recovered a poor judge's accuracy without labels: the pessimist's true bullish accuracy of 0.57 was recovered as 0.59., Inter-judge disagreement did not imply evaluability; what gated evaluation was whether every individual judge varied, not ensemble-level disagreement.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects Recovering LLM-Persona Accuracies from Unlabeled Votes to related works in the bibliography
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
- https://github.com/docxology/ntqr_llm
