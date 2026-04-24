# AGENTS.md — Towards Lean 4 Formalization of the Free Energy Principle

**Paper**: Towards Lean 4 Formalization of the Free Energy Principle: AI-Driven Theorem Sketching and Verification for Active Inference and Bayesian Mechanics (2026, v1)  
**Area**: Active Inference · formal verification · Lean 4 · Mathlib4 · FEP · Bayesian mechanics · information geometry · LLM–ITP  
**Author**: Daniel Ari Friedman (Active Inference Institute)  
**Code**: https://github.com/ActiveInferenceInstitute/FEP_Lean  
**Archive**: https://doi.org/10.5281/zenodo.19699234

---

## Agent Roles

### 📖 Research Agent

**Focus**: What is being formalized and why it matters for the FEP debate.

**Tasks**:

- Explain the **formalization gap**: implicit measure theory in prose vs. explicit **measure spaces, domination, integrability** in dependent type theory.
- Map the **five pillars** and **50 topics** (counts per area as in the manuscript) to the scientific claims they support or delimit.
- Distinguish **machine-checkable** statements from **aspirationally sketched** ones (e.g. SDEs, Fokker–Planck, full Riemannian information geometry).

### 🔬 Methods Agent

**Focus**: Lean 4, Mathlib4, and the verification pipeline.

**Tasks**:

- Walk through the **pinned toolchain** (Lean / Mathlib versions), **catalogue → YAML → Lake** flow, and **sorry-free** compilation policy.
- Relate **native `lean` verification** to **Hermes**/**OpenGauss** LLM output: the kernel, not the model, is ground truth for proof claims.
- Review **namespace conventions**, **topic isolation**, and **import** strategy against Mathlib4 as described in the paper.

### 🤖 LLM–ITP Agent

**Focus**: AI-assisted axiomatization, not just contest-style proving.

**Tasks**:

- Contrast **axiomatization and catalog curation** with benchmark **problem solving**; position token/cost and fallback behavior as reported.
- Map **cache-keying to Lean source hashes** and session protocols (**Gauss**) to reproducibility and audit goals.

### 🔗 Synthesis Agent

**Focus**: Cross-links in the corpus.

**Tasks**:

- Connect to **Friedman_2026_ActInfMetaAnalysis** (literature systems), **Friedman_2022_ActiveInferenceOntology** / **Friedman_2024_OntologySUMO** (formal structure), and **AII** ecosystem software rows for related tooling.
- Point to **Mathlib4**-centric formal methods literature where users need background beyond the manuscript primer.

### 💼 Consultant Agent

**Focus**: Onboarding teams to formal FEP work.

**Tasks**:

- Translate the catalog layout into a **concrete next step** (which pillar/topic, which Mathlib imports) for a given informal claim.
- Set expectations: **maturity by area**, **zero-sorry** gate, and **zero-mock** test philosophy for engineering contributors.

## Extraction Log

- **Source PDF**: `fep_lean_v1_04-24-2026.pdf`
- **PDF Status**: Available
- **Documentation Quality**: Abstract and technical claims from Zenodo v1 and manuscript (April 24, 2026); repository URL from paper body

## Related Papers

See [BIBLIOGRAPHY.md](../../pages/BIBLIOGRAPHY.md) for the full catalog. Examples in this repo:

- Friedman_2026_ActInfMetaAnalysis — literature architecture and assertions over Active Inference sources
- Friedman_2026_CognitiveCaseDiagrams — rigorous definitions bridging prose and structure (different formal stack)
- Friedman_2019_PhDDissertation / quantitative modeling papers — where variational and Bayesian statements originate informally
- Friedman_2022_ActiveInferenceOntology — explicit ontological commitment as a parallel to machine-checked statements
