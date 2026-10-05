# Artifacts and Evidence {#sec:artifacts_evidence}

## Evidence inventory

| Artifact or check | Supports | Does not establish |
| --- | --- | --- |
| [Curated bibliography](../../pages/BIBLIOGRAPHY.md), [identity registry](../../data/work-identifiers.json) | Reviewed catalog entries and persistent route reservations | Completeness of all external indexes |
| [Generated manifest](../../data/generated-manifest.json) and producer no-write checks | Declared output ownership and current source/projection agreement | Fresh external observations or deployed bytes |
| [Scholar snapshot](../../data/scholar-snapshot.json) and [verification receipt](../../data/scholar-verification-receipt.json) | A dated directly observed metric bound to exact snapshot bytes | A continuously current count or independent assessment of research quality |
| [Browser tests](../../code/tests/) and [QA reports](../../reports/) | Behavior in the tested runtime and scenarios | Every device, network, assistive technology, or human visual approval |
| [Pages artifact manifest](../../data/pages-artifact-manifest.json) | Declared web projection, hashes, omissions, and source binding | Every live response body or archive licensing |
| [Deployed artifact verifier](../../code/orchestrators/verify_deployed_artifact.py) | The targeted technical checks listed in its fresh receipt | Full-site body verification or full release attestation |
| [Visual QA runbook](../operations/accessibility-qa.md) | Separate capture, hash-bound review, and approval procedures | Review from screenshot generation alone |
| [Manuscript validator](../../code/orchestrators/validate_manuscript.py) | Source/configuration consistency and reference resolution | Complete BibTeX grammar, rendering, scientific validity, or editorial approval |

## Current evidence status

This draft binds architecture statements to repository sources and gives commands that can be rerun against a chosen candidate. It does not repeat historical test totals or deployment results as current measurements. Dated evidence belongs in the corresponding report and release records; a later reader must inspect the candidate and scope of each receipt.

The architecture diagram in [development.md](../operations/development.md) is a documentation aid. No experimental figures or manuscript-rendered outputs are attached to this draft.

## Claim discipline

A supporting source must match the kind of claim being made. Deterministic rendering supports source/output agreement; an external citation supports attribution; a browser observation supports its tested behavior. None substitutes for the others. Future benchmark tables must name their runtime, candidate, inputs, measurement procedure, failures, and retained raw observations.
