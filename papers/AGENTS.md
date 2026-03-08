# AGENTS.md — Papers Directory

**Directory**: [papers/](.)
**Purpose**: Per-paper documentation folders for 99 publications (2015–2026), each containing README.md, AGENTS.md, and Claude Code-compatible SKILL.md.

---

## Agent Roles

### 📖 ARCHIVIST

- Maintains the directory index in [README.md](README.md)
- Tracks PDF availability (95/99 currently present)
- Cross-references with [BIBLIOGRAPHY.md](../BIBLIOGRAPHY.md) entries
- Manages [paper_metadata.json](paper_metadata.json) with structured metadata for all 99 papers

### 🔬 RESEARCHER

- Extracts abstracts, authors, keywords, methods, and contributions from PDFs
- Populates per-paper README.md with accurate paper-specific information
- Identifies research domain classification for each paper

### 🎓 EDUCATOR

- Generates Claude Code-compatible SKILL.md for each paper
- Ensures YAML frontmatter with `name`, `description`, and `tags`
- Populates `## Instructions`, `## Key Concepts`, `## Prerequisites` sections
- Creates learning pathways across the 8 research domains

### 🔗 INTEGRATOR

- Links each paper folder to its BIBLIOGRAPHY.md entry and DOI
- Maps papers to associated software repositories in SOFTWARE.md
- Connects related papers across domains

---

## Documentation Generation Pipeline

| Script | Purpose |
|--------|---------|
| [regenerate_docs.py](regenerate_docs.py) | Rebuild README.md, AGENTS.md, and SKILL.md from metadata |

### Quality Checks (All 99 Pass)

| Check | Status |
|-------|--------|
| README.md present | 99/99 ✅ |
| AGENTS.md present | 99/99 ✅ |
| SKILL.md present | 99/99 ✅ |
| SKILL.md YAML frontmatter (name, description, tags) | 99/99 ✅ |
| SKILL.md `## Instructions` section | 99/99 ✅ |
| SKILL.md `## Key Concepts` section | 99/99 ✅ |
| SKILL.md `## Prerequisites` section | 99/99 ✅ |

---

## Folder Coverage by Domain

| Domain | Papers | Example Folders |
|--------|:------:|-----------------|
| 🐜 Entomology | 20 | `Friedman_2025_AntStack`, `Friedman_2021_ActiveInferants`, `Friedman_2019_PhDDissertation` |
| 🧠 Active Inference | 19 | `Friedman_2025_CEREBRUM`, `Friedman_2024_FederatedInference`, `Friedman_2023_GNN` |
| 🛡️ Cognitive Security | 19 | `Friedman_2026_CognitiveIntegrity`, `Friedman_2022_InformationCommons`, `Friedman_2023_P3IF` |
| 🎨 Art & Synergetics | 13 | `Friedman_2026_DoorsOfPerception`, `Friedman_2023_BlakeFuller`, `Friedman_2025_QuadMath` |
| 🧬 Genetics & Biomedical | 9 | `Friedman_2015_HoneyBeeEvolution`, `Friedman_2016_NuclearStructure` |
| 🎥 Presentations | 8 | `Friedman_2025_5thSymposium`, `Friedman_2024_BioFirm` |
| 💻 Computational | 6 | `Friedman_2025_DiscoveryEngine`, `Friedman_2025_MDKV` |
| 🌍 AII Ecosystem | 5 | `Friedman_2025_AII_v3`, `Friedman_2024_OntologySUMO` |

---

## Maintenance Log

| Date | Agent | Action | Status |
|------|-------|--------|--------|
| 2026-03-08 | ARCHIVIST | Verified all 99 folders have complete docs | ✅ |
| 2026-03-08 | EDUCATOR | Fixed CryptoJews and EhrlichialInfection SKILL.md | ✅ |
| 2026-03-08 | RESEARCHER | Rebuilt paper_metadata.json with 99 entries | ✅ |
