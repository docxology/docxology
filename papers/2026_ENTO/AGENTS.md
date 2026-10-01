<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data

**Paper**: ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for ENTO
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Flat ZIP layout: manifest.json, one encrypted member per track, optional proof, Per-track AES-256-GCM envelopes with HKDF-derived keys, Four graded observability levels for export-time manifest redaction
- Identifies findings: Tamper detection succeeded on all 2400 benchmark rows (rate 1.0)., Mean pack throughput was 78.9296 MiB/s on the medium-track condition at observability level 3 (n = 150, CV 15.3%); the paper makes no superiority claim., Ciphertext expansion on fixture tracks was an exact, zero-variance 1.7113.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects ENTO: an ENcrypted, Typed, Omnitrack container format for multimodal research data to related works in the bibliography
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
- https://github.com/docxology/entofile
