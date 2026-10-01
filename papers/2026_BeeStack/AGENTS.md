<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation

**Paper**: BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman, Tucker Cahill Chambers

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for BeeStack
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Five typed Python modules (Body, Brain, Mind, Swarm, Niche) with contracts, BeeBody: FlyBody walking/flight tasks on a generated honeybee MJCF in MuJoCo, BeeBrain ingestion of curated public Apis mellifera datasets
- Identifies findings: The empirical run integrates 48 response panels, 7 anatomy inventories and 24 odor templates, with a parseable-source fraction of 0.800., All module contract self-tests pass (rate 1.000) alongside 11 catalogued open gaps; the authors stress this is contract conformance, not biological validation., BeeBody visual scores (0.980 visual, 1.000 silhouette) certify that renders look like a bee, not that kinetics match; masses, adhesion and aerodynamics are FlyBody defaults.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation to related works in the bibliography
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
- https://github.com/docxology/BeeStack
