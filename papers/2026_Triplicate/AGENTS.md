<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine

**Paper**: The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for Triplicate
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Pure-Python engine rendering YAML content to a print-ready PDF, Hybrid drawn-furniture / ReportLab-flowed-body layout strategy, Nine single-responsibility modules with a deterministic four-step pipeline
- Identifies findings: The engine keeps content and code strictly separate, so producing a new newspaper title is a data edit rather than a code change., Drawing furniture first and starting column frames below it lets spanning headlines, standing boxes and automatic text flow coexist on one page., Rendering is deterministic: the same edition manifest always yields a byte-identical paper.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects The Triplicate: A Data-Driven Large-Format Newspaper Layout Engine to related works in the bibliography
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
- https://github.com/docxology/template_newspaper
