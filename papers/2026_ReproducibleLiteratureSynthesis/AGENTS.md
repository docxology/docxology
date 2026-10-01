<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference

**Paper**: Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for ReproducibleLiteratureSynthesis
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Multi-backend literature search with DOI/arXiv/title deduplication, Deterministic SHA-256-keyed JSON search cache, Abstract and PDF full-text enrichment with on-disk caching
- Identifies findings: In the reported run, the query "reproducible research optimization" against the local backend returned 6 deduplicated papers (4 with a DOI, 6 with an abstract) and no backend errors., A second run with identical config produces byte-identical artifacts apart from cache timestamps, which the paper calls the property it exists to demonstrate., Results from live arXiv and Crossref are not reproducible across weeks; strict reproducibility requires pinning a local corpus, committing the cache, and pinning the LLM seed.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects Reproducible Literature Synthesis with infrastructure/search and infrastructure/reference to related works in the bibliography
- Maps paper-to-software relationships
- Updates cross-domain connections

---

## Extraction Log

| Source | Agent | Action | Status |
|--------|-------|--------|--------|
| Metadata | ARCHIVIST | Cataloged metadata | ✅ |
| Metadata | RESEARCHER | Extracted methods/findings | ✅ |
| Metadata | EDUCATOR | Generated documentation | ✅ |
