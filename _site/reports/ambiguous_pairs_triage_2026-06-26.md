# Ambiguous Paired-Publication Triage (2026-06-26)

183 needs_review pairs from reports/paired_publications_2026-06-26.json.
All map to **existing** paper folders. Collapsed to the decisions that matter:

## TIER 1 — Real decisions (4 items)

### A. Folder has NO DOI — decide whether to add the proposed one
- **2026_ReproducibleResearch** — proposed DOI `10.5281/zenodo.16903351` from docxology/template (11 release pairs collapse here)

### B. Folder DOI differs from proposed DOI — check concept-vs-version
- **2023_TranscriptActiveInference**
    - folder DOI: `10.5281/zenodo.8229512`
    - proposed:   `10.5281/zenodo.8228934`  (ActiveInferenceInstitute/ActiveInferAnts)
    - release: https://github.com/ActiveInferenceInstitute/ActiveInferAnts/releases/tag/1
    - zenodo:  https://zenodo.org/records/8229512
- **2026_FEPLean**
    - folder DOI: `10.5281/zenodo.19699234`
    - proposed:   `10.5281/zenodo.19699233`  (ActiveInferenceInstitute/fep_lean)
    - release: https://github.com/ActiveInferenceInstitute/fep_lean/releases/tag/v1.0.0
    - zenodo:  https://zenodo.org/records/19699234
- **2026_ITrace**
    - folder DOI: `10.5281/zenodo.20614909`
    - proposed:   `10.5281/zenodo.20614908`  (docxology/itrace)
    - release: https://github.com/docxology/itrace/releases/tag/v0.4.1
    - zenodo:  https://zenodo.org/records/20614909

## TIER 2 — Already represented, same DOI (169 pairs) — noise
These folders already cite the exact proposed concept DOI. No action except optionally
recording an already_reviewed decision in data/paired-publication-decisions.json to
stop them reappearing. Folders:

- 2025_AntStack
- 2026_ActiveInferenceMulti  (x14)
- 2026_BoundedAutoResearchTiny  (x14)
- 2026_CogSecSkills
- 2026_ConvergenceAnalysisGradient  (x18)
- 2026_DeterministicTestbedSelf  (x13)
- 2026_EditorialQualityAt  (x15)
- 2026_GeneralizedNotationNotationGNN  (x7)
- 2026_LivingMetaAnalysis  (x11)
- 2026_RefinementGold  (x11)
- 2026_SelfImprovementAgent  (x12)
- 2026_TemplateApproachReproducible  (x16)
- 2026_TemplateMadlib  (x11)
- 2026_TemplateTextbook  (x12)
- 2026_Triplicate  (x13)
