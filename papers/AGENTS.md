# AGENTS.md — Papers Directory

**Directory**: [papers/](.)
**Purpose**: Per-paper documentation folders for 108 publications (2015–2026), each containing README.md, AGENTS.md, and Claude Code-compatible SKILL.md.

---

## Agent Roles

### 📖 ARCHIVIST

- Maintains the directory index in [README.md](README.md)
- Tracks PDF availability using the **PDF** column in the [README](README.md) index (per-folder ✅/❌)
- Cross-references with [BIBLIOGRAPHY.md](../pages/BIBLIOGRAPHY.md) entries
- Manages [paper_metadata.json](paper_metadata.json) with structured metadata for all paper folders (108 entries as of 2026-05-15)

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
- When the unified bibliography count or table order changes, run [`sync_publications_html.py`](sync_publications_html.py) so `publications.html` **PUBS** and JSON-LD **mainEntity** stay aligned with [`pages/BIBLIOGRAPHY.md`](../pages/BIBLIOGRAPHY.md).

---

## Documentation Generation Pipeline

| Script | Purpose |
|--------|---------|
| [regenerate_docs.py](regenerate_docs.py) | Rebuild README.md, AGENTS.md, and SKILL.md from metadata |
| [sync_publications_html.py](sync_publications_html.py) | Rebuild `publications.html` **PUBS** and JSON-LD **mainEntity** from the unified bibliography table (`pages/BIBLIOGRAPHY.md`); run after adds/reorders in that table |

### Quality Checks (spot-check after adds)

| Check | Status |
|-------|--------|
| README.md present | 108/108 folders (last verified 2026-05-15) |
| AGENTS.md present | 108/108 |
| SKILL.md present | 108/108 |
| SKILL.md YAML frontmatter (name, description, tags) | required per folder |
| SKILL.md `## Instructions` section | required |
| SKILL.md `## Key Concepts` section | required |
| SKILL.md `## Prerequisites` section | required |

---

## Folder Coverage by Domain

| Domain | Works | Example Folders |
|--------|:-----:|-----------------|
| 🐜 Entomology | 21 | `2026_EntoLinguistics`, `2025_AntStack`, `2021_ActiveInferants`, `2019_PhDDissertation` |
| 🧠 Active Inference | 23 | `2026_FEPLean`, `2026_CognitiveCaseDiagrams`, `2026_FocusedAttentionMeditation`, `2026_ActInfMetaAnalysis`, `2025_CEREBRUM` |
| 🛡️ Cognitive Security | 20 | `2026_CognitiveIntegrity`, `2022_InformationCommons`, `2023_P3IF`, `2020_FacilitatorsCatechism` |
| 🎨 Art & Synergetics | 15 | `2026_BlakeJiang`, `2026_DoorsOfPerception`, `2026_BeforePragmatism`, `2023_BlakeFuller`, `2025_QuadMath` |
| 🧬 Genetics & Biomedical | 9 | `2015_HoneyBeeEvolution`, `2016_NuclearStructure` |
| 💻 Computational | 7 | `2026_ReproducibleResearch`, `2025_DiscoveryEngine`, `2025_MDKV` |
| 🌍 AII Ecosystem | 5 | `2025_AII_v3`, `2024_OntologySUMO` |
| 🎥 Presentations & Media | 15 | `2025_5thSymposium`, `2024_BioFirm`; rows with Domain 🎥 also include courses, series, and playbooks in the unified table |

Counts follow the **Domain** column in [`pages/BIBLIOGRAPHY.md`](../pages/BIBLIOGRAPHY.md) (one row per indexed work, 115 total as of the table header).

---

## Maintenance Log

| Date | Agent | Action | Status |
|------|-------|--------|--------|
| 2026-03-08 | ARCHIVIST | Verified paper folders have complete docs (initial index) | ✅ |
| 2026-03-08 | EDUCATOR | Fixed CryptoJews and EhrlichialInfection SKILL.md | ✅ |
| 2026-03-08 | RESEARCHER | Rebuilt paper_metadata.json (initial unified entries) | ✅ |
| 2026-04-15 | ARCHIVIST | Indexed 102 paper folders in README; Entomology domain +1 (Ento-Linguistics); bibliography row in pages/BIBLIOGRAPHY.md | ✅ |
| 2026-04-19 | ARCHIVIST | Added 2026_ActInfMetaAnalysis (DOI 10.5281/zenodo.19461934); Active Inference domain 19→20; paper count 102→103; bibliography row 108; metadata.json; publications.html; index.html counts 109→110 | ✅ |
| 2026-04-19 | ARCHIVIST | Added 2026_FocusedAttentionMeditation (DOI 10.1007/978-3-032-16955-6_11, Springer CSCIS vol 2857); Active Inference domain 20→21; paper count 103→104; bibliography row 109; all counts 110→111 | ✅ |
| 2026-04-23 | ARCHIVIST | Added 2026_CognitiveCaseDiagrams (DOI 10.5281/zenodo.19695260, Active Inference Journal v1); README.md, AGENTS.md, SKILL.md; bibliography row 110; Active Inference domain 21→22; paper_metadata; publications.html + index counts 111→112; papers/README index; SOFTWARE + software.html 47→48 | ✅ |
| 2026-04-24 | ARCHIVIST | Added 2026_FEPLean (DOI 10.5281/zenodo.19699234, Active Inference Journal v1); README.md, AGENTS.md, SKILL.md; BIBLIOGRAPHY row 111; Active Inference domain 22→23; paper_metadata; publications.html + index counts 112→113; papers/README 106; SOFTWARE AII 31→32 + FEP_Lean | ✅ |
| 2026-04-25 | MAINTAINER | AGENTS: PDF tracking defers to README index column; log aligned with root doc sync (teaching / hub counts) | ✅ |
| 2026-05-04 | INTEGRATOR | Domain **Works** table + `sync_publications_html.py` in pipeline; PUBS/mainEntity sync script landed | ✅ |
| 2026-05-12 | MAINTAINER | Repo-wide doc audit; this AGENTS.md domain breakdown matches `pages/BIBLIOGRAPHY.md` ground truth (21/23/20/14/9/7/5/15 = 114); spot-checked `2026_FocusedAttentionMeditation` per-paper docs (README/AGENTS/SKILL present, no PDF as expected) | ✅ |
| 2026-05-13 | ARCHIVIST | Added `2026_BlakeJiang` (DOI 10.5281/zenodo.20144984); Art & Synergetics 14→15; bibliography 114→115; paper folders and metadata 107→108 | ✅ |
| 2026-05-15 | ARCHIVIST | Updated AII v2/v3 rows to version-specific Zenodo DOIs and ActInfMetaAnalysis to current v2 DOI/title; retained concept/v1 DOIs only as version-chain context | ✅ |
