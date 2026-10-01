<!-- docxology:generated-document AGENTS.md; ownership=explicit-manifest -->

# AGENTS.md — template_pitch_deck: Reproducible, Validated Pitch-Deck Generation

**Paper**: template_pitch_deck: Reproducible, Validated Pitch-Deck Generation (2026)
**Domain**: Computational
**Authors**: Daniel Ari Friedman

---

## Agent Roles

### 📖 ARCHIVIST
- Maintains bibliographic metadata and cross-references
- Tracks citation links and DOI consistency for TemplatePitchDeck
- Updates related_papers links when new connections are identified

### 🔬 RESEARCHER
- Extracts methods: Shared format-agnostic DeckContent/Slide content model with slide budgets, Dual PDF (ReportLab) and PPTX (python-pptx) renderers with a parity test, {{TOKEN}} resolution against deck_tokens.yaml with fail-loud checks
- Identifies findings: The tool generates six artifacts (short, medium and long decks, each as PDF and PPTX) from one token-resolved content source., PDF and PPTX decks built from identical content carry identical slide counts and text, verified by reading back both file formats rather than by inspection., Rendering is deterministic: given the same repository state, two consecutive runs produce byte-identical PDF and PPTX output, with generation time kept only in deck metadata.
- Maps contributions to Computational literature

### 🎓 EDUCATOR
- Creates learning pathways for Computational concepts
- Develops SKILL.md with executable instructions
- Maintains prerequisite knowledge mapping

### 🔗 INTEGRATOR
- Connects template_pitch_deck: Reproducible, Validated Pitch-Deck Generation to related works in the bibliography
- Maps paper-to-software relationships
- Updates cross-domain connections

---

## Extraction Log

| Source | Agent | Action | Status |
|--------|-------|--------|--------|
| Metadata | ARCHIVIST | Cataloged metadata | ✅ |
| Metadata | RESEARCHER | Extracted methods/findings | ✅ |
| Metadata | EDUCATOR | Generated documentation | ✅ |
