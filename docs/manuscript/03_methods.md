# Methods {#sec:methods}

## Source-to-projection method

The shared [bibliography parser](../../code/src/biblio_table.py) reads the curated works table. [Bibliography export](../../code/orchestrators/export_bibliography.py) produces structured work records and citation-manager formats; downstream commands produce work pages, catalog pages, search indexes, feeds, and sitemaps. Equivalent software and resume flows use their own authored authorities. [GENERATED.md](../../GENERATED.md) maps producers to outputs.

Runnable commands live in `code/orchestrators/`. Reusable parsing, rendering, identity, and validation policies live in `code/src/` and are imported through [docxology_tools](../../code/src/docxology_tools/__init__.py). The [generation plan](../../code/src/generation_plan.py) declares local writers, inputs, ordered dependencies, and exact no-write checks. The driver performs bounded ordered passes and stops on a failed writer. Fingerprint skips optimize local generation; independent checks establish freshness. The [regeneration runbook](../operations/regeneration.md) explains invalidation and interrupted-run behavior.

The checkout-local [shared package](../../code/src/README.md) preserves one module object across canonical namespace imports and legacy flat imports. This matters for exception catching, class identity and module state. Registration is explicit and regression checks compare the registry with shared source files. Importing the package does not eagerly load its optional rendering or browser dependencies. The project metadata declares a repository-local application rather than an installable wheel.

## Complete intake and reviewed bylines

The shared [Zenodo reader](../../code/src/zenodo_pagination.py) supplies complete-or-error pagination to its callers while leaving transport and report ownership with them. It requires bounded page shapes, a consistent exact total and distinct numeric record identities; an early short page, duplicate identity, changed total or exhausted bound raises an error instead of returning a partial catalog. Its [regressions](../../code/tests/test_zenodo_pagination.py) include the failure paths. These checks establish the reader's completion contract for the returned observation; they do not create a transactional snapshot of a remote service or prove that a query found every relevant work.

The [paired intake command](../../code/orchestrators/sync_paired_publications.py) also admits a bounded list of explicit immutable records, because author queries can omit institutional or grouped-credit works. Requested identities and normalized manifests must agree with any already observed record. GitHub readers reject malformed pages, duplicate identities and a full final page at the request bound. These controls preserve finite observation scope rather than guaranteeing universal publication discovery.

Publication intake remains a separate review. A DOI identifies a registry record; a versioned PDF identifies a document edition. Their creator lists may differ. The [document-byline regressions](../../code/tests/test_doi_document_authors.py) require reviewed document evidence and frozen registry/document baselines before applying a document-order decision. A later registry refresh reports drift or unavailability while preserving a valid reviewed byline. It cannot silently substitute an unreviewed creator order. Editors, contributors, representative lists and depositors retain their declared roles instead of being inferred to be document authors.

Reviewed literal credits retain ordered institutional and unstructured display labels through [author authority](../../code/src/author_entities.py) and citation exports. Established organizations keep their type; unspecified labels produce name-only structured data. The review binds the work, catalogue byline, document sidecar and raw creator baseline. Registry refresh records a separate observation rather than rewriting that baseline. A person's identifier is not assigned to a composite label.

## Edition selection and bounded hosting

The shared [paper-resource resolver](../../code/src/paper_artifacts.py) selects either an available local PDF or an explicitly reviewed remote primary. The remote declaration binds filename, exact versioned Zenodo file URL, version, record identity, byte count and SHA-256. A separate source-evidence record identifies what was actually fetched or extracted. Declaring a digest does not itself verify remote bytes, and text extracted from an older local PDF cannot be presented as the new edition's extraction.

[Pair review](../../code/src/publication_pairing.py) keeps the stable concept/release key separate from an exact record and complete normalized manifest hash. A changed edition returns to review; conflicting editions cannot be selected by input order. Historical decisions retain their actors, times and rationales. Compact evidence may reference the exact original committed report without republishing its full bytes. A new current-edition decision is separately attributed. Paper-index updates preserve curated extensions and require review before replacing provenance-bearing abstract or keyword fields.

A software archive and its manuscript retain distinct identities. [Software exports](../../code/src/software_table.py) preserve the paper's citation DOI while the software structured-data view prefers an explicitly labelled software archive DOI. Linking an event book to a repository does not make the book's DOI an identifier for that software.

The [artifact builder](../../code/orchestrators/build_pages_artifact.py) constructs a finite web projection under local budgets. GitHub documents an independent published-site limit [@githubPagesLimits]; local headroom is a project policy. Existing hosted PDFs and permanent work routes remain preserved. Reviewed supporting Office files can use an exact committed Git object after local/object byte agreement and reference checks, implemented by [archive projection](../../code/src/archive_projection.py). Historical report selection also protects referenced evidence. A capacity change therefore needs both object custody and consumer-link verification; moving a folder name alone does not establish a working archive route.

A bounded [scholarly PDF projection](../../code/src/scholar_pdf_projection.py) reserves content-addressed aliases beside selected work abstracts. Its [registry](../../data/scholar-pdf-projections.json) binds exact work identity, source hash, byte count, rights evidence and reviewed abstract. Aliases are assembled into the web output without adding duplicate PDFs to Git. Immutable reservations remain hosted and budgeted after a selection retires; a reviewed remote primary retains precedence. Per-file and aggregate limits apply alongside the whole-site budget. Existing archive URLs keep their source objects.

The repository, its Git history, the deployed projection, and external providers have different availability properties. Each manifest must state its own scope. Neither a small deployment nor a successful local hash check demonstrates the durability of every external source.

## Progressive browser discovery

The [search runtime](../../js/search-page.js) starts an unfiltered visit with a compact preview, then loads the full core for a query or scoped selection. Work and video text segments load for relevant nonempty searches. Late responses cannot restore an older query. Missing data exposes fallback or retry behavior instead of implying that a partial result set is complete.

The [gallery runtime](../../js/art-gallery.js) filters a complete compact catalog while rendering a finite batch of cards. Detail data loads for descriptions and lightbox views; native artwork-page links remain usable. The [publication runtime](../../js/publications.js) loads the work catalog and requests abstract/keyword enrichment for nonempty searches. Sorting and filtering act on the matching catalog before row batching. [Runtime guidance](../operations/site-runtime.md) records these contracts and their browser tests.

![Progressive discovery loads compact entry data first, then retrieves detail for the active query or interaction. Native links and server-rendered content preserve a fallback path.](../output/figures/progressive-discovery.png){#fig:progressive_discovery}

## Local reading state and selected exports

The [research-tools generator](../../code/orchestrators/build_research_tools.py) derives a citation catalog from the bibliography's authoritative export routines. The [reading-list runtime](../../js/collections.js) stores named, ordered citation-key selections in the visitor's browser. Selected BibTeX, RIS and Citation Style Language (CSL) exports retain authoritative records, contributor roles and reading order. Selected CSL uses the same work-bound literal-credit authority as the complete bibliography; invalid authority fails generation before catalog bytes change. Markdown provides a linked reading outline.

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

The [research map](../../js/research-map.js) presents literal catalog, byline and software edges with provenance. The diagram bounds its displayed neighborhood; a complete list and JSON export retain the remaining edges. Reviewed work-specific types distinguish people, organizations and unspecified contributor labels without propagating a label's type to unrelated works. Exact normalized names within a type may group homonyms and leave spelling variants separate. Saved links prefer an existing exact identity; a missing legacy person identity resolves only to a sole typed successor, while ambiguity requires an explicit selection. The [trail source](../../data/research-trails-source.json) declares editorial goals, prerequisites and linked work, software and video identities. Generation rejects unresolved references. Suggested study times are editorial estimates rather than measured completion times.

## Reproducible teaching models

The [probability laboratory](../../js/probability-lab.js) implements binary Bayesian updating with explicit likelihoods and conditionally independent observations. Log weights avoid numerical underflow; impossible evidence is reported without changing accepted history. A seeded reinforced urn records its initial counts, reinforcement, generator seed and every draw. Comma-separated values (CSV) exports retain replay parameters and computed steps.

These are finite teaching processes with declared assumptions and deterministic replay where specified. They do not reproduce an indexed paper, validate physical theories, or model ant physiology and pheromone interactions. The page links mathematical definitions separately from related research.

## Evidence and release method

Local structural, generated-output, and browser checks have distinct scopes. The [release runbook](../operations/settle.md) separates reviewed payload commits from generated control binders. [Deployment verification](../operations/live-verification.md) binds fresh route checks to an expected source commit and a specific successful Pages run. [Release integrity](../operations/release-integrity.md) records the further requirements for human visual review and full release attestation.

The [artifact verifier](../../code/orchestrators/verify_deployed_artifact.py) requires research-desk pages, citation/map/trail datasets and their runtime assets in its declared critical scope. The same bounded verifier requires every reserved scholarly PDF alias's exact body hash and PDF media type, with matching included original/copy contracts. Missing manifest entries and mismatched live bytes fail technical acceptance. This remains a targeted projection check rather than a claim that every archived object was fetched.

## Search-engine discovery boundary

Work landing pages, sitemaps and citation metadata expose reviewed records to crawlers. Google Scholar's inclusion guidance distinguishes scholarly content, immediately available full text or complete author-written abstracts, searchable PDF files, and compatible article metadata [@scholarInclusion]. A local readiness check can identify missing inputs and inconsistent links. It cannot establish actual indexing, resolve crawler scheduling, or turn a generated synopsis into an author-written abstract.

The [readiness policy](../../code/src/scholar_readiness.py) and [follow-up guide](../seo/gsc-followup.md) keep technical readiness separate from observations in a signed-in search console. The [dated pilot review](../../reports/scholar_pdf_placement_review_2026-11-05.md) records reviewed document prerequisites. The resolver checks that the canonical full abstract still matches its reviewed digest and is visible in static HTML. Copying a PDF requires rights evidence, a source hash, a reserved destination and a measured budget; successful source checks do not certify deployed bytes or indexing. The size or host eligibility of one edition must not be generalized to another. Authenticated Scholar metric observations use their own snapshot-and-receipt process and do not measure index completeness.

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
file as well as declared sources. Citation and document consumers also declare
the author records and source-evidence sidecars they actually read. This allows
dependency-only or reviewed-authority changes to trigger rebuilding. A cache hit is an execution decision and carries no independent
claim of scientific correctness or deployed freshness.
