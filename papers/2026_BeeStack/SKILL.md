---
# docxology:generated-document SKILL.md; ownership=explicit-manifest
name: "BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation"
description: "BeeStack is an executable, evidence-typed research scaffold for whole-colony simulation of the Western honey bee (Apis mellifera), organized as five layers (Body, Brain, Mind, Swarm, Niche). It pairs FlyBody/MuJoCo body and small-scene swarm renders ..."
tags: ["honeybee", "apis-mellifera", "active-inference", "simulation-scaffold", "swarm-intelligence", "niche-construction", "flybody", "mujoco", "antennal-lobe", "mushroom-body"]
domain: "Computational"
citation: "Daniel Ari Friedman, Tucker Cahill Chambers (2026). *BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation*. Zenodo."
doi: "10.5281/zenodo.20420556"
---

# BeeStack: An Evidence-Typed Scaffold for Whole-Colony Honeybee Simulation

**Daniel Ari Friedman, Tucker Cahill Chambers** (2026) · Computational

## Context

This work addresses topics in **Computational**: honeybee, Apis mellifera, active inference, simulation scaffold.

## Methods

Primary methods and techniques applied in this work:

- **Five typed Python modules (Body, Brain, Mind, Swarm, Niche) with contracts** — A five-layer honeybee specification is converted into five typed Python modules with explicit contracts, deterministic seeding and a hydrated manuscript.
- **BeeBody: FlyBody walking/flight tasks on a generated honeybee MJCF in MuJoCo** — Body renders use FlyBody walking and wing-beat flight tasks through a generated honeybee MJCF body plan in MuJoCo; strict swarm scenes use scripted poses with real contact detection.
- **BeeBrain ingestion of curated public Apis mellifera datasets** — Public anatomy and activity datasets (Honey-Bee Standard Brain, glomerular odor codes, calcium imaging, etc.) are parsed into anatomy inventories, response panels and dance templates.
- **Reduced deterministic kernels for BeeMind, BeeSwarm and BeeNiche** — Active-inference-style policy scoring, dance recruitment and comb/thermal stepping are implemented as reduced, hand-calibrated deterministic kernels with diagnostics.
- **Claim ledger and manuscript hydration from run-time JSON** — A claim ledger maps each claim class to evidence and what it does not prove; manuscript numbers are read from pipeline-generated JSON, and tests use no mocks.

## Key Findings

Core contributions and results:

- The empirical run integrates 48 response panels, 7 anatomy inventories and 24 odor templates, with a parseable-source fraction of 0.800.
- All module contract self-tests pass (rate 1.000) alongside 11 catalogued open gaps; the authors stress this is contract conformance, not biological validation.
- BeeBody visual scores (0.980 visual, 1.000 silhouette) certify that renders look like a bee, not that kinetics match; masses, adhesion and aerodynamics are FlyBody defaults.
- Strict swarm scenes are small scripted-pose contact scenes (3 scenes, 15 unique contact pairs); colony dynamics use reduced kernels with 50 agents representing 20,000 workers.
- The authors state the results do not show BeeStack can yet predict colony survival, pesticide response, full dance-language use, or field foraging success.

Methods and findings are summarized from the full text; each item is backed by a verbatim quote recorded in `metadata.json` (`evidence`, `key_findings_evidence`).

## Related Works

- [2023_NSFReporting](../2023_NSFReporting/)
- [2023_NaturalAIBased](../2023_NaturalAIBased/)
- [2025_AuBI](../2025_AuBI/)

## Validation

Verification points for this work:

- Canonical DOI: 10.5281/zenodo.20420556
- PDF SHA-256: See zenodo_record
- Pairing confidence: strong
- Last checked: 2026-09-24T18:29:54Z

## Prerequisites

- Familiarity with honeybee, Apis mellifera, active inference
- Background in Computational fundamentals
- Access to source repository: docxology/BeeStack

## Instructions

When working with this paper:

1. Reference the DOI for citation: `10.5281/zenodo.20420556`
2. Apply methods listed in the Methods section for related analysis.
3. Validate findings against the original PDF and metadata.
