# AGENTS.md — Papers Directory

**Directory**: [papers/](.)
**Purpose**: Per-paper documentation folders for 105 publications (2015–2026), each containing README.md, AGENTS.md, and Claude Code-compatible SKILL.md.

---

## Agent Roles

### 📖 ARCHIVIST

- Maintains the directory index in [README.md](README.md)
- Tracks PDF availability (95/99 currently present)
- Cross-references with [BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md) entries
- Manages [paper_metadata.json](paper_metadata.json) with structured metadata for all paper folders (105 entries as of 2026-04-23)

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

### Quality Checks (spot-check after adds)

| Check | Status |
|-------|--------|
| README.md present | 105/105 folders (last verified 2026-04-23) |
| AGENTS.md present | 105/105 |
| SKILL.md present | 105/105 |
| SKILL.md YAML frontmatter (name, description, tags) | required per folder |
| SKILL.md `## Instructions` section | required |
| SKILL.md `## Key Concepts` section | required |
| SKILL.md `## Prerequisites` section | required |

---

## Folder Coverage by Domain

| Domain | Papers | Example Folders |
|--------|:------:|-----------------|
| 🐜 Entomology | 21 | `Friedman_2026_EntoLinguistics`, `Friedman_2025_AntStack`, `Friedman_2021_ActiveInferants`, `Friedman_2019_PhDDissertation` |
| 🧠 Active Inference | 22 | `Friedman_2026_CognitiveCaseDiagrams`, `Friedman_2026_FocusedAttentionMeditation`, `Friedman_2026_ActInfMetaAnalysis`, `Friedman_2025_CEREBRUM`, `Friedman_2024_FederatedInference` |
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
| 2026-04-15 | ARCHIVIST | Indexed 102 paper folders in README; Entomology domain +1 (Ento-Linguistics); bibliography row in pages/BIBLIOGRAPHY.md | ✅ |
| 2026-04-19 | ARCHIVIST | Added Friedman_2026_ActInfMetaAnalysis (DOI 10.5281/zenodo.19461934); Active Inference domain 19→20; paper count 102→103; bibliography row 108; metadata.json; publications.html; index.html counts 109→110 | ✅ |
| 2026-04-19 | ARCHIVIST | Added Friedman_2026_FocusedAttentionMeditation (DOI 10.1007/978-3-032-16955-6_11, Springer CSCIS vol 2857); Active Inference domain 20→21; paper count 103→104; bibliography row 109; all counts 110→111 | ✅ |
| 2026-04-23 | ARCHIVIST | Added Friedman_2026_CognitiveCaseDiagrams (DOI 10.5281/zenodo.19695260, Active Inference Journal v1); README.md, AGENTS.md, SKILL.md; bibliography row 110; Active Inference domain 21→22; paper_metadata; publications.html + index counts 111→112; papers/README index; SOFTWARE + software.html 47→48 | ✅ |
