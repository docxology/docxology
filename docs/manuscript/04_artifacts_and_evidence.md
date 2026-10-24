# Artifacts and Evidence {#sec:artifacts_evidence}

## Evidence inventory

- [Curated bibliography](../../pages/BIBLIOGRAPHY.md), [identity registry](../../data/work-identifiers.json) support reviewed catalog entries and persistent route reservations. It does not establish completeness of all external indexes.

- [Generated manifest](../../data/generated-manifest.json) and producer no-write checks support declared output ownership and current source/projection agreement. It does not establish fresh external observations or deployed bytes.

- [Scholar snapshot](../../data/scholar-snapshot.json) and [verification receipt](../../data/scholar-verification-receipt.json) support a dated directly observed metric bound to exact snapshot bytes. It does not establish a continuously current count or independent assessment of research quality.

- [Browser tests](../../code/tests/) and [QA reports](../../reports/) support behavior in the tested runtime and scenarios. It does not establish every device, network, assistive technology, or human visual approval.

- [Pages artifact manifest](../../data/pages-artifact-manifest.json) supports declared web projection, hashes, omissions, and source binding. It does not establish every live response body or archive licensing.

- [Deployed artifact verifier](../../code/orchestrators/verify_deployed_artifact.py) supports the targeted technical checks listed in its fresh receipt. It does not establish full-site body verification or full release attestation.

- [Visual QA runbook](../operations/accessibility-qa.md) supports separate capture, hash-bound review, and approval procedures. It does not establish review from screenshot generation alone.

- [Manuscript validator](../../code/orchestrators/validate_manuscript.py) supports source/configuration consistency and reference resolution. It does not establish complete BibTeX grammar, rendering, scientific validity, or editorial approval.


![Evidence classes answer different questions. Byte identity, generation agreement, browser behavior, deployed contracts, and named review each retain their own scope.](../output/figures/evidence-boundaries.png){#fig:evidence_boundaries}

## Current evidence status

Visitor state adds a separate evidence class: a saved list records a reader's selection, and a share URL records portable keys and a title. Neither creates authorship, citation support or a new bibliography authority. Selected exports inherit the catalog's metadata limits. A teaching-model trace records computation under its stated assumptions and parameters, without establishing empirical validity.

This draft binds architecture statements to repository sources and gives commands that can be rerun against a chosen candidate. It does not repeat historical test totals or deployment results as current measurements. Dated evidence belongs in the corresponding report and release records; a later reader must inspect the candidate and scope of each receipt.

The architecture diagram in [development.md](../operations/development.md) is a documentation aid. The native PDF cover and body diagrams explain architecture, loading decisions, evidence boundaries, and release verification. They describe source-backed contracts rather than experimental results. Explicit rendering produces external review artifacts with hash-bound receipts.

## Claim discipline

A supporting source must match the kind of claim being made. Deterministic rendering supports source/output agreement; an external citation supports attribution; a browser observation supports its tested behavior. None substitutes for the others. Future benchmark tables must name their runtime, candidate, inputs, measurement procedure, failures, and retained raw observations.
