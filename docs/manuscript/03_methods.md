# Methods {#sec:methods}

## Source-to-projection method

The shared [bibliography parser](../../code/src/biblio_table.py) reads the curated works table. [Bibliography export](../../code/orchestrators/export_bibliography.py) produces structured work records and citation-manager formats; downstream commands produce work pages, catalog pages, search indexes, feeds, and sitemaps. Equivalent software and resume flows use their own authored authorities. [GENERATED.md](../../GENERATED.md) maps producers to outputs.

Runnable commands live in `code/orchestrators/`. Reusable parsing, rendering, identity, and validation policies live in `code/src/` and are imported through [docxology_tools](../../code/src/docxology_tools/__init__.py). The [generation plan](../../code/src/generation_plan.py) declares local writers, inputs, ordered dependencies, and exact no-write checks. The driver performs bounded ordered passes and stops on a failed writer. Fingerprint skips optimize local generation; independent checks establish freshness. The [regeneration runbook](../operations/regeneration.md) explains invalidation and interrupted-run behavior.

## Progressive browser discovery

The [search runtime](../../js/search-page.js) starts an unfiltered visit with a compact preview, then loads the full core for a query or scoped selection. Work and video text segments load for relevant nonempty searches. Late responses cannot restore an older query. Missing data exposes fallback or retry behavior instead of implying that a partial result set is complete.

The [gallery runtime](../../js/art-gallery.js) filters a complete compact catalog while rendering a finite batch of cards. Detail data loads for descriptions and lightbox views; native artwork-page links remain usable. The [publication runtime](../../js/publications.js) loads the work catalog and requests abstract/keyword enrichment for nonempty searches. Sorting and filtering act on the matching catalog before row batching. [Runtime guidance](../operations/site-runtime.md) records these contracts and their browser tests.

## Evidence and release method

Local structural, generated-output, and browser checks have distinct scopes. The [release runbook](../operations/settle.md) separates reviewed payload commits from generated control binders. [Deployment verification](../operations/live-verification.md) binds fresh route checks to an expected source commit and a specific successful Pages run. [Release integrity](../operations/release-integrity.md) records the further requirements for human visual review and full release attestation.

## Manuscript construction method

Implementation statements link a source owner or runbook. Volatile catalog totals remain in the [generated count snapshot](../../reports/current_counts.md). The draft contains no unresolved generated-value tokens or new quantitative results. Future measurements require identified inputs, a repeatable method, dated receipts, and an interpretation boundary before they enter manuscript prose.
