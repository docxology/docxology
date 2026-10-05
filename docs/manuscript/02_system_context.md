# System Context {#sec:system_context}

## Archive and website

The public repository is the source archive for the site at `danielarifriedman.com`. Python commands maintain checked-in HTML, JSON, citation exports, and reports; GitHub Pages serves static files. The [Pages artifact policy](../operations/github-pages-artifact.md) defines a bounded projection, so repository availability and website availability are separate properties of an object.

The [unified bibliography](../../pages/BIBLIOGRAPHY.md) is the curated works authority. The [software catalog](../../pages/SOFTWARE.md) selects reviewed software entries, while the [cached GitHub inventory](../../data/github-repositories.json) records a broader public inventory. An inventory observation can prompt review without automatically becoming a curated publication or endorsement.

## Identity and source custody

[Work identity reservations](../../data/work-identifiers.json) preserve permanent citation keys and work-page URLs as titles or years change. [Canonical policy](../seo/canonical-policy.md) connects generated `works/` landing pages with paper-folder routes and redirects. A work page may offer source-PDF and GitHub-folder links when the corresponding archive objects exist; a missing source remains an availability limitation.

Archived PDF bytes and literal extracted text under [papers/](../../papers/) require custody checks when replaced. A digest binds bytes to an identified object. It does not prove that extraction selected every paragraph correctly, that a document is licensed for redistribution, or that its research results were replicated.

## Execution and manuscript boundary

The [development map](../operations/development.md) describes configuration owners and module boundaries. Local generation operates on existing sources; public-source intake, account actions, and deployment are separate operations. This manuscript lives at `docs/manuscript/` in the public repository. Its local validator inspects source structure and configuration without requiring a sibling checkout or rendering a document.
