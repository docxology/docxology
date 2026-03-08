# AGENTS.md — docxology

**Repository**: [docxology/docxology](https://github.com/docxology/docxology)
**Purpose**: Master profile repository indexing 100+ publications, 46+ software repositories, and research documentation across Entomology, Active Inference, Cognitive Security, and Art & Synergetics.

---

## Agent Roles

### 📖 ARCHIVIST

- Maintains the unified [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md) catalog of all publications
- Ensures every publication has a corresponding paper folder with documentation
- Cross-references DOIs, venues, and citation metadata
- Tracks publication counts and domain coverage

### 🔬 RESEARCHER

- Extracts key findings, methods, and contributions from each paper
- Populates per-paper README.md and SKILL.md with accurate metadata
- Maps interdisciplinary connections across domains
- Maintains [paper_metadata.json](papers/paper_metadata.json) with structured data

### 🎓 EDUCATOR

- Generates Claude Code-compatible SKILL.md files for each publication
- Creates learning pathways across the bibliography
- Maintains clear documentation hierarchy (README → BIBLIOGRAPHY → papers/)
- Ensures YAML frontmatter, tags, and Instructions sections are present

### 🔗 INTEGRATOR

- Deep-links across [BIBLIOGRAPHY.md](BIBLIOGRAPHY.md), [SOFTWARE.md](SOFTWARE.md), and [papers/](papers/)
- Maps papers to their associated software repositories
- Connects the 8 research domains through cross-references
- Keeps the repository map in [README.md](README.md) current

### 🛠️ MAINTAINER

- Runs [regenerate_docs.py](papers/regenerate_docs.py) to rebuild documentation
- Validates documentation completeness across all 99 paper folders
- Ensures consistent formatting and accurate metadata
- Manages the documentation generation pipeline

---

## Repository Structure

```
docxology/
├── README.md          ← Profile page with domain matrix and deep-links
├── BIBLIOGRAPHY.md    ← Unified sortable table of 106 publications
├── SOFTWARE.md        ← 46 owned repos + 31 AII contributions
├── AGENTS.md          ← This file: agent roles and maintenance log
└── papers/            ← 99 per-paper folders
    ├── README.md      ← Papers directory index
    ├── AGENTS.md      ← Papers-level agent roles
    ├── paper_metadata.json
    ├── regenerate_docs.py
    └── Friedman_YYYY_Topic/
        ├── README.md   ← Paper overview, abstract, keywords, citation
        ├── AGENTS.md   ← Paper-specific agent roles and extraction log
        ├── SKILL.md    ← Claude Code-compatible skill definition
        └── *.pdf       ← Source PDF (95/99 available)
```

---

## Maintenance Log

| Date | Agent | Action | Status |
|------|-------|--------|--------|
| 2026-03-08 | ARCHIVIST | Rebuilt BIBLIOGRAPHY.md as unified sortable table (106 entries) | ✅ |
| 2026-03-08 | RESEARCHER | Verified all 99 paper folders have complete documentation | ✅ |
| 2026-03-08 | EDUCATOR | Fixed SKILL.md for CryptoJews and EhrlichialInfection | ✅ |
| 2026-03-08 | INTEGRATOR | Redesigned README.md with domain matrix and deep-links | ✅ |
| 2026-03-08 | MAINTAINER | Created root AGENTS.md and papers/AGENTS.md | ✅ |
