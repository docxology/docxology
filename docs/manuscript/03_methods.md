# Methods {#sec:methods}

## Source-to-projection method

The shared [bibliography parser](../../code/src/biblio_table.py) reads the curated works table. [Bibliography export](../../code/orchestrators/export_bibliography.py) produces structured work records and citation-manager formats; downstream commands produce work pages, catalog pages, search indexes, feeds, and sitemaps. Equivalent software and resume flows use their own authored authorities. [GENERATED.md](../../GENERATED.md) maps producers to outputs.

Runnable commands live in `code/orchestrators/`. Reusable parsing, rendering, identity, and validation policies live in `code/src/` and are imported through [docxology_tools](../../code/src/docxology_tools/__init__.py). The [generation plan](../../code/src/generation_plan.py) declares local writers, inputs, ordered dependencies, and exact no-write checks. The driver performs bounded ordered passes and stops on a failed writer. Fingerprint skips optimize local generation; independent checks establish freshness. The [regeneration runbook](../operations/regeneration.md) explains invalidation and interrupted-run behavior.

The checkout-local [shared package](../../code/src/README.md) preserves one module object across canonical namespace imports and legacy flat imports. This matters for exception catching, class identity and module state. Registration is explicit and regression checks compare the registry with shared source files. Importing the package does not eagerly load its optional rendering or browser dependencies. The project metadata declares a repository-local application rather than an installable wheel.

## Progressive browser discovery

The [search runtime](../../js/search-page.js) starts an unfiltered visit with a compact preview, then loads the full core for a query or scoped selection. Work and video text segments load for relevant nonempty searches. Late responses cannot restore an older query. Missing data exposes fallback or retry behavior instead of implying that a partial result set is complete.

The [gallery runtime](../../js/art-gallery.js) filters a complete compact catalog while rendering a finite batch of cards. Detail data loads for descriptions and lightbox views; native artwork-page links remain usable. The [publication runtime](../../js/publications.js) loads the work catalog and requests abstract/keyword enrichment for nonempty searches. Sorting and filtering act on the matching catalog before row batching. [Runtime guidance](../operations/site-runtime.md) records these contracts and their browser tests.

![Progressive discovery loads compact entry data first, then retrieves detail for the active query or interaction. Native links and server-rendered content preserve a fallback path.](../output/figures/progressive-discovery.png){#fig:progressive_discovery}

## Local reading state and selected exports

The [research-tools generator](../../code/orchestrators/build_research_tools.py) derives a citation catalog from the bibliography's authoritative export routines. The [reading-list runtime](../../js/collections.js) stores named, ordered citation-key selections in the visitor's browser. Selected BibTeX, RIS and Citation Style Language (CSL) exports retain authoritative records, contributor roles and reading order. Markdown provides a linked reading outline.

Shared URL fragments and imported JavaScript Object Notation (JSON) backups open previews. Explicit saving creates a new list. Malformed stored JSON preserves retrievable original text for recovery, unavailable storage leaves a session draft, and detected cross-tab changes stop overwriting. Unavailable work keys remain visible and block citation export. The [source auditor](../../code/src/content_audit.py) recognizes the bounded collection-state contract only on the collection route and continues to reject missing ordinary anchors.

| Object | Authority and persistence |
| --- | --- |
| Citation catalog | A generated projection of reviewed bibliography records |
| Saved list | Visitor-controlled selection stored in this browser |
| Shared or imported preview | Portable title and ordered keys that require explicit saving |
| Citation export | Selected existing records, with unavailable keys reported as a failure |

The [research-tools guide](../operations/research-tools.md) records input bounds, recovery rules and browser scenarios. These controls preserve the stated application boundaries; they do not make browser storage permanent or encrypted.

## Explained connections and curated trails

[Related-work ranking](../../code/src/research_connections.py) uses recorded method and topic phrases, distinguishing contributors and explicit software associations. Explanations preserve author/editor roles, label domain-only fallback matches and exclude known duplicate work identities. Metadata overlap is neither a citation relation nor evidence that two scientific claims are equivalent.

The [research map](../../js/research-map.js) presents literal catalog, byline and software edges with provenance. The diagram bounds its displayed neighborhood; a complete list and JSON export retain the remaining edges. Exact normalized names may group homonyms and leave spelling variants separate. The [trail source](../../data/research-trails-source.json) declares editorial goals, prerequisites and linked work, software and video identities. Generation rejects unresolved references. Suggested study times are editorial estimates rather than measured completion times.

## Reproducible teaching models

The [probability laboratory](../../js/probability-lab.js) implements binary Bayesian updating with explicit likelihoods and conditionally independent observations. Log weights avoid numerical underflow; impossible evidence is reported without changing accepted history. A seeded reinforced urn records its initial counts, reinforcement, generator seed and every draw. Comma-separated values (CSV) exports retain replay parameters and computed steps.

These are finite teaching processes with declared assumptions and deterministic replay where specified. They do not reproduce an indexed paper, validate physical theories, or model ant physiology and pheromone interactions. The page links mathematical definitions separately from related research.

## Evidence and release method

Local structural, generated-output, and browser checks have distinct scopes. The [release runbook](../operations/settle.md) separates reviewed payload commits from generated control binders. [Deployment verification](../operations/live-verification.md) binds fresh route checks to an expected source commit and a specific successful Pages run. [Release integrity](../operations/release-integrity.md) records the further requirements for human visual review and full release attestation.

The [artifact verifier](../../code/orchestrators/verify_deployed_artifact.py) requires research-desk pages, citation/map/trail datasets and their runtime assets in its declared critical scope. Missing manifest entries and mismatched live bytes fail technical acceptance. This remains a targeted projection check rather than a claim that every archived object was fetched.

## Manuscript construction method

Implementation statements link a source owner or runbook. Volatile catalog totals remain in the [generated count snapshot](../../reports/current_counts.md). The draft contains no unresolved generated-value tokens or new quantitative results. Future measurements require identified inputs, a repeatable method, dated receipts, and an interpretation boundary before they enter manuscript prose.

## Agent inspection and bounded diagnostics

The [agent interface](../operations/agent-interface.md) exposes versioned JSON
status and an ordered generation plan derived from the same registry as the
writers. Inspection does not grant validation or release status. The
[backend profiler](../operations/backend-profiling.md) provides fixed, read-only
timing and tracing workloads under the qualified Python runtime. It binds source
bytes, runtime, results, and index membership; changed inputs invalidate an
observation. Timing comparisons require matched workload and tracing conditions.

Generation cache inputs include the interpreter pin, project metadata, and lock
file as well as declared sources. This allows dependency-only changes to trigger
rebuilding. A cache hit is an execution decision and carries no independent
claim of scientific correctness or deployed freshness.
