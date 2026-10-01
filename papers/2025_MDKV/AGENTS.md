<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — MDKV: A Multitrack Markdown Container for Structured, Portable Documents

**Paper**: MDKV: A Multitrack Markdown Container for Structured, Portable Documents (2025)
**Domain**: Computational
**Authors**: Daniel Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for MDKV
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: ZIP container with YAML manifest and tracks/ directory of Markdown files, Seven-type track taxonomy (primary, translation, commentary, code, etc.), Python reference implementation split into core, storage, services, and CLI
- Identifies findings: The paper lists four contributions: a precise model and container format, a modular architecture exposed via CLI and GUI, detailed use cases, and guidance on cryptographic provenance and conformance., Export is designed to be deterministic: order follows the manifest, and identical inputs produce identical outputs., The author lists format limitations, including no built-in encryption or signing and code tracks that are listings rather than runnable notebooks.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects MDKV: A Multitrack Markdown Container for Structured, Portable Documents to related works in the bibliography
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
