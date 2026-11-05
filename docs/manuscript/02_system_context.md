# System Context {#sec:system_context}

## Archive and website

The public repository is the curated catalog and retained-local-source archive for the site at `danielarifriedman.com`; selected publication editions and provider media may remain at identified external archives. Python commands maintain checked-in HTML, JSON, citation exports, and reports; GitHub Pages serves static files. The [Pages artifact policy](../operations/github-pages-artifact.md) defines a bounded projection, so repository availability and website availability are separate properties of an object.

The [unified bibliography](../../pages/BIBLIOGRAPHY.md) is the curated works authority. The [software catalog](../../pages/SOFTWARE.md) selects reviewed software entries, while the [cached GitHub inventory](../../data/github-repositories.json) records a broader public inventory. An inventory observation can prompt review without automatically becoming a curated publication or endorsement.

![Authored sources pass through shared contracts into public views. Local source objects and declared external editions retain distinct custody; Pages serves a bounded projection with explicit archival fallbacks.](../output/figures/system-context.png){#fig:system_context}

## Identity and source custody

[Work identity reservations](../../data/work-identifiers.json) preserve permanent citation keys and work-page URLs as titles or years change. [Canonical policy](../seo/canonical-policy.md) connects generated `works/` landing pages with paper-folder routes and redirects. A work page may offer source-PDF and GitHub-folder links when the corresponding archive objects exist; a missing source remains an availability limitation.

Archived PDF bytes and literal extracted text under [papers/](../../papers/) require custody checks when replaced. A digest binds bytes to an identified object. It does not prove that extraction selected every paragraph correctly, that a document is licensed for redistribution, or that its research results were replicated.

## Responsibility and object states

Source providers publish documents or registry observations. A maintainer reviews their relationship to an existing work, records the accepted metadata and evidence, and selects a hosting route. Generators project those decisions; validators check declared contracts; deployment and human reviewers assess their own stated scopes. Automation does not inherit the authority of the document's authors or the maintainer's unresolved judgment.

| State | Required support | Consequence |
| --- | --- | --- |
| Observed candidate | Identified source and dated observation | Review queue; no automatic publication claim |
| Curated work | Reviewed source row and reserved identity | Stable catalog and citation projections |
| Selected edition | Exact local object or declared versioned remote PDF | Edition-specific download and citation metadata |
| Generated candidate | Declared inputs and successful no-write checks | Source/projection agreement in the tested checkout |
| Technically accepted deployment | Expected revision and scoped live checks | Acceptance only for the named deployed contracts |

These states describe responsibilities in existing workflows, not a universal lifecycle enforced by a single state machine. A later metadata change can require a new review without invalidating the historical existence of a prior edition.

## Execution and manuscript boundary

The [development map](../operations/development.md) describes configuration owners and module boundaries. Local generation operates on existing sources; public-source intake, account actions, and deployment are separate operations. This manuscript lives at `docs/manuscript/` in the public repository. Its local validator inspects source structure and configuration without requiring a sibling checkout or rendering a document.
