<!-- docxology:generated-document README.md; ownership=explicit-manifest -->

# 💻 BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · *Zenodo*

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20420556-blue)](https://doi.org/10.5281/zenodo.20420556)

---

## Abstract

> BeeStack is an executable, evidence-typed research scaffold for whole-colony simulation of the Western honey bee (Apis mellifera), organized as five layers (Body, Brain, Mind, Swarm, Niche). It pairs FlyBody/MuJoCo body and small-scene swarm renders with curated empirical BeeBrain datasets and reduced deterministic kernels, keeping fidelity a declared per-module property: every quoted number is traceable from configuration to artifact to manuscript, gaps are catalogued rather than hidden, and the validation rate is a config-band self-test measure, not a biological-realism score. This 1.0 release accompanies the manuscript 'BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation' and includes the combined PDF and the full source archive. Source: https://github.com/docxology/BeeStack

## Keywords

`honeybee` · `Apis mellifera` · `active inference` · `simulation scaffold` · `swarm intelligence` · `niche construction` · `FlyBody` · `MuJoCo` · `antennal lobe` · `mushroom body` · `central complex` · `waggle dance`

## Methods

- **Five typed Python modules (Body, Brain, Mind, Swarm, Niche) with contracts** — A five-layer honeybee specification is converted into five typed Python modules with explicit contracts, deterministic seeding and a hydrated manuscript.
- **BeeBody: FlyBody walking/flight tasks on a generated honeybee MJCF in MuJoCo** — Body renders use FlyBody walking and wing-beat flight tasks through a generated honeybee MJCF body plan in MuJoCo; strict swarm scenes use scripted poses with real contact detection.
- **BeeBrain ingestion of curated public Apis mellifera datasets** — Public anatomy and activity datasets (Honey-Bee Standard Brain, glomerular odor codes, calcium imaging, etc.) are parsed into anatomy inventories, response panels and dance templates.
- **Reduced deterministic kernels for BeeMind, BeeSwarm and BeeNiche** — Active-inference-style policy scoring, dance recruitment and comb/thermal stepping are implemented as reduced, hand-calibrated deterministic kernels with diagnostics.
- **Claim ledger and manuscript hydration from run-time JSON** — A claim ledger maps each claim class to evidence and what it does not prove; manuscript numbers are read from pipeline-generated JSON, and tests use no mocks.

## Key Findings

- The empirical run integrates 48 response panels, 7 anatomy inventories and 24 odor templates, with a parseable-source fraction of 0.800.
- All module contract self-tests pass (rate 1.000) alongside 11 catalogued open gaps; the authors stress this is contract conformance, not biological validation.
- BeeBody visual scores (0.980 visual, 1.000 silhouette) certify that renders look like a bee, not that kinetics match; masses, adhesion and aerodynamics are FlyBody defaults.
- Strict swarm scenes are small scripted-pose contact scenes (3 scenes, 15 unique contact pairs); colony dynamics use reduced kernels with 50 agents representing 20,000 workers.
- The authors state the results do not show BeeStack can yet predict colony survival, pesticide response, full dance-language use, or field foraging success.

_Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`)._

## Artifacts

- GitHub repository: [docxology/BeeStack](https://github.com/docxology/BeeStack)
- GitHub release: [v1.0.0](https://github.com/docxology/BeeStack/releases/tag/v1.0.0)
- DOI: [10.5281/zenodo.20420556](https://doi.org/10.5281/zenodo.20420556)
- Zenodo record: [https://zenodo.org/records/20420556](https://zenodo.org/records/20420556)
- PDF: [BeeStack_combined.pdf](BeeStack_combined.pdf)
- PDF SHA-256: [See Zenodo record](https://zenodo.org/records/20420556)

## Citation

> Daniel Ari Friedman, Tucker Cahill Chambers (2026). *BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation*. Zenodo. DOI: 10.5281/zenodo.20420556. URL: https://doi.org/10.5281/zenodo.20420556.

## Related

- [Full Bibliography](../../pages/BIBLIOGRAPHY.md)
- [All Papers](../README.md)
