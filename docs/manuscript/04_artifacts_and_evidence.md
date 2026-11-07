# Artifacts and Evidence {#sec:artifacts_evidence}

## Claim-to-evidence map

A verification result is useful only with the question it addresses. The repository records the following separate classes; passing one class does not promote an observation into a stronger claim.

| Claim and source owner | Evidence to inspect | Interpretation limit |
| --- | --- | --- |
| Reviewed identity: [bibliography](../../pages/BIBLIOGRAPHY.md) and [reservations](../../data/work-identifiers.json) | Curated row, stable key and explicit review history | No complete external-index or scientific-quality claim |
| Selected PDF edition: [resolver](../../code/src/paper_artifacts.py) | Exact object fields and independent per-paper source evidence | A declaration is not a remote fetch, extraction audit or rights determination |
| Exact pair review: [pairing policy](../../code/src/publication_pairing.py) | Immutable record, complete normalized manifest hash and original review evidence | Concept identity or a cached status alone cannot approve a changed edition |
| Literal credits: [author authority](../../code/src/author_entities.py) | Ordered labels, frozen registry/document evidence and separate refresh observation | A grouped label does not establish individual identity or an inferred contributor role |
| Source/projection agreement: [generation plan](../../code/src/generation_plan.py) | Declared writer, inputs and independent no-write check | No fresh remote observation or live-byte proof |
| Dated metrics: [Scholar snapshot](../../data/scholar-snapshot.json) and [receipt](../../data/scholar-verification-receipt.json) | Direct authenticated observation bound to exact snapshot bytes | No continuously current metric or research-quality assessment |
| Tested behavior: [tests](../../code/tests/) and [QA](../../reports/) | Runtime, selected scenarios, source binding and failures | No coverage of every device, network or assistive technology |
| Hosted projection: [Pages manifest](../../data/pages-artifact-manifest.json) | Included objects, hashes, explicit omissions and source anchor | No availability guarantee for omitted or external objects |
| Targeted live acceptance: [artifact verifier](../../code/orchestrators/verify_deployed_artifact.py) | Expected candidate, deployment run and fetched/HEAD contracts | No full-site body verification or human sign-off |
| Review: [visual QA procedure](../operations/accessibility-qa.md) | Identified captures, hashes, reviewer and review scope | Capture alone is not approval; layout approval is not scientific replication |
| Manuscript structure: [validator](../../code/orchestrators/validate_manuscript.py) | Configuration, references, section structure and resolved tokens | No rendering, full citation grammar, editorial approval or publication readiness |

![Evidence classes answer different questions. Byte identity, generation agreement, browser behavior, deployed contracts, and named review each retain their own scope.](../output/figures/evidence-boundaries.png){#fig:evidence_boundaries}

## Evaluation protocol

The implemented design is evaluated through contract tests and candidate-bound gates, rather than a new comparative experiment. For a changed mechanism, identify its source owner, valid fixture, invalid fixture and expected refusal before editing the implementation. Exercise the same public entry point used by its callers where practical. Temporary fixtures avoid changing tracked evidence. A failure produced by unavailable tools or network access must remain distinct from an assertion failure.

| Mechanism | Positive check | Negative control |
| --- | --- | --- |
| Paginated intake | Distinct records exactly satisfy the observed total | Truncated, duplicate, malformed or changing pages refuse |
| Edition/byline binding | Reviewed edition and evidence hashes agree | Changed evidence or mismatched document/registry baseline refuses |
| Cached pair review | The durable ledger agrees with the exact observed edition | Changed record, manifest or ambiguous concept observations refuse |
| Literal exports and DOI roles | Ordered credits and distinct paper/software identifiers agree | Drifted authority or substitution of a paper DOI for an explicit software archive fails |
| Research credit consumers | Selected CSL and work-specific map types preserve reviewed credits | Invalid authority, unknown explicit type or ambiguous legacy identity refuses |
| Generation invalidation | A warm cache rebuilds after an authority-only input change | A stale output cannot retain a cache hit when its declared authority changes |
| Archive routing | Local bytes agree with the pinned committed object | Source drift or a surviving local download reference refuses |
| Stable discovery | Reserved work identity resolves in generated exports | Missing identity or unresolved trail/citation reference fails |
| Deployment acceptance | Expected source/run and declared object contracts agree | Stale revision, absent critical entry or mismatched fetched bytes fails |

Use the focused regressions named in @sec:source_surface, then the declared generation checks and relevant full selections. Deterministic generation is assessed by repeat execution and unchanged substantive outputs. Runtime performance is assessed separately with matched workloads and conditions; a faster cached pass alone is not a comparative result. Reports must identify deselection, missing capabilities and pending manual review. This draft does not report fresh test counts or timing estimates as manuscript results.

## Maintenance cases and unresolved evidence

The [publication consistency review](../../reports/publication_consistency_review_2026-10-13.json) and [corrected-source review](../../reports/publication_source_corrections_2026-10-19.json) document why an active manuscript, archived edition and implementation check can disagree. MarkdownDecisionProcess's corrected evaluation is prospective because original empirical provenance was unavailable. PopulationSearch's new seeded protocol does not reconstruct a historical table denominator. Blake's identified current epoch must be distinguished from unrecovered historical membership. These are documented correction cases, not a replication study or a representative sample of research reliability.

A current source correction should identify an immutable originating revision and its scoped verification, retain the prior correction history, and update the profile's interpretation boundary. It must not rewrite an archived PDF or imply a new archival deposit. Recovering an old observation requires the actual identified records; a new run cannot silently take its place.

Visitor state is a different evidence class again. A saved reading list records a reader's selection; a share URL carries keys and a title. Selected exports inherit the catalog's metadata limits. A teaching-model trace records computation under stated assumptions and parameters. Neither source creates new authorship, citation support, or empirical validity.

## Current evidence status

This draft binds architecture statements to source owners and provides commands against a chosen candidate. Dated implementation or deployment results remain in their corresponding reports, where a reader can inspect revision, runtime and scope. A later source candidate needs its own applicable acceptance. The architecture diagram in [development.md](../operations/development.md), the cover and the body figures explain the system; their successful production does not constitute an experiment or human visual approval.
