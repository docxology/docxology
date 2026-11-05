# Limitations and Next Steps {#sec:limitations_next_steps}

## Current limitations

The draft describes an implemented repository design using local source evidence. It has no comparative study, controlled usability evaluation, independent scientific replication, or new performance measurements. The repository citation identifies the described system; it is not external validation of its design.

Cached public-source observations have a date and scope. External indexes can contain duplicates, split identities, incomplete metadata, or access restrictions. Provider-hosted media may fail independently of a valid native page. Source custody, licenses, and depositor/author reconciliation remain separate from generated-page correctness.

Automated browser acceptance and screenshot capture cannot grant human visual sign-off. Structural manuscript validation cannot verify complete BibTeX grammar, execute a renderer, or assess publication readiness. Manuscript text and original manuscript figures use CC BY 4.0; that declaration does not assign rights to archived papers or third-party artwork.

## Custody, scale and discovery

Versioned external PDF delivery reduces growth in the site's own payload but adds an availability dependency. An immutable-looking URL and a locally stored digest are insufficient evidence that a future remote response is available or unchanged. Retained source receipts, explicit edition links and scoped remote rechecks support diagnosis. Existing repository files and public routes need their own migration review before any hosting change.

Capacity planning must measure the actual projected bytes and their growth drivers. An art subdirectory can contain only small metadata while the images already live at a provider; moving that directory would not solve PDF or report growth. Conversely, moving referenced reports without migrating their consumers can preserve bytes in Git while breaking public evidence navigation. The project must test omission rules and immutable fallbacks together.

Search-engine inclusion remains an external outcome. Technical metadata, crawl accessibility and content readiness are prerequisites, not proof of acceptance by Google or Scholar. Search-console access, exact observations and source rights can remain unresolved even when local checks pass. No crawler index completeness or ranking improvement is claimed here.

## Visitor state and model boundaries

Local reading lists have no server-side synchronization guarantee. Export and recovery controls cannot prevent browser eviction, user deletion or unrelated software from changing local state. A syntactically valid share link supports navigation and selection, not the truth of the selected work's claims.

Relationship ranking depends on recorded metadata and editorial choices. Common topics, incomplete bylines and normalized names can make a suggested connection broad or ambiguous. The map is not a verified identity registry, citation graph or causal network. Curated trails and finite teaching models are learning aids whose usefulness has not been established by a controlled usability or scientific evaluation.

## Next steps

1. Keep architecture and source references synchronized with implementation changes, using the local manuscript gate.
2. Run the declared pinned rendering integration and inspect every requested format before external publication.
3. Add literature when relevant primary references and complete citation metadata have been checked.
4. Add quantitative findings only after an explicit measurement design and retained candidate-bound observations exist; use a generated-value producer for volatile results.
5. Obtain editorial and human visual review before considering publication.

The active implementation backlog remains [TODO.md](../../TODO.md). This section records manuscript requirements without replacing repository ownership, account access, or source-review decisions.
