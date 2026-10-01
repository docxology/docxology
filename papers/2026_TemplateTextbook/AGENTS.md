<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — The Template Textbook

**Paper**: The Template Textbook (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for TemplateTextbook
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Single config.yaml source of truth for book structure, Tested Python backbone (textbook.models) and deterministic figures, Pandoc + pandoc-crossref rendering pipeline
- Identifies findings: The book is explicitly a scaffold rather than a finished work: every structural element is present and author-specific passages are marked stubs., It provides twelve chapter shells across four parts, each with a matching lab and question bank., Claims building the book reproduces byte-identical figures and numbers, since nothing in the prose is computed by hand.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects The Template Textbook to related works in the bibliography
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
- https://github.com/docxology/template_textbook
