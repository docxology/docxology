# Methods {#sec:methods}

## Source-to-projection method

The shared [bibliography parser](../../code/src/biblio_table.py) reads the curated works table. [Bibliography export](../../code/orchestrators/export_bibliography.py) produces structured work records and citation-manager formats; downstream commands produce work pages, catalog pages, search indexes, feeds, and sitemaps. Equivalent software and resume flows use their own authored authorities. [GENERATED.md](../../GENERATED.md) maps producers to outputs.

Runnable commands live in `code/orchestrators/`. Reusable parsing, rendering, identity, and validation policies live in `code/src/` and are imported through [docxology_tools](../../code/src/docxology_tools/__init__.py). The [generation plan](../../code/src/generation_plan.py) declares local writers, inputs, ordered dependencies, and exact no-write checks. The driver performs bounded ordered passes and stops on a failed writer. Fingerprint skips optimize local generation; independent checks establish freshness. The [regeneration runbook](../operations/regeneration.md) explains invalidation and interrupted-run behavior.

## Progressive browser discovery

The [search runtime](../../js/search-page.js) starts an unfiltered visit with a compact preview, then loads the full core for a query or scoped selection. Work and video text segments load for relevant nonempty searches. Late responses cannot restore an older query. Missing data exposes fallback or retry behavior instead of implying that a partial result set is complete.

The [gallery runtime](../../js/art-gallery.js) filters a complete compact catalog while rendering a finite batch of cards. Detail data loads for descriptions and lightbox views; native artwork-page links remain usable. The [publication runtime](../../js/publications.js) loads the work catalog and requests abstract/keyword enrichment for nonempty searches. Sorting and filtering act on the matching catalog before row batching. [Runtime guidance](../operations/site-runtime.md) records these contracts and their browser tests.

![Progressive discovery loads compact entry data first, then retrieves detail for the active query or interaction. Native links and server-rendered content preserve a fallback path.](../output/figures/progressive-discovery.png){#fig:progressive_discovery}

## Evidence and release method

Local structural, generated-output, and browser checks have distinct scopes. The [release runbook](../operations/settle.md) separates reviewed payload commits from generated control binders. [Deployment verification](../operations/live-verification.md) binds fresh route checks to an expected source commit and a specific successful Pages run. [Release integrity](../operations/release-integrity.md) records the further requirements for human visual review and full release attestation.

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
