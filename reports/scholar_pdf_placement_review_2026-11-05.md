# Scholar PDF placement source review — 2026-11-05

Review scope: five already-public journal articles and the bounded Pages-only PDF projection pilot at source commit `7ea51f5bf18d841df5bd3b33d5d1827351d49e72`. This is a source-prerequisite and local implementation review. Deployment, crawler retrieval and actual Google Scholar indexing remain unverified.

The reviewed authority is [data/scholar-pdf-projections.json](../data/scholar-pdf-projections.json), schema `ScholarPDFProjectionRegistry.v1`, SHA-256 `21ae02d3ab2c8cf5b039722149a57b956adb6968e3b84d287fbc61d15a342567`. Its exact PDF hashes, work identities, reviewed bylines/dates, rights and abstract bindings are separate from whether a route is currently selected.

## Source membership and byte cost

| Work | DOI | Citation date | PDF bytes | Pages |
| --- | --- | --- | ---: | ---: |
| [Shared Protentions in Multi-Agent Active Inference](https://danielarifriedman.com/papers/2024_SharedProtentions/2024_SharedProtentions.pdf) | [10.3390/e26040303](https://doi.org/10.3390/e26040303) | 2024-03-29 | 325,880 | 17 |
| [A variational synthesis of evolutionary and developmental dynamics](https://danielarifriedman.com/papers/2023_VariationalSynthesis/2023_VariationalSynthesis.pdf) | [10.3390/e25070964](https://doi.org/10.3390/e25070964) | 2023-06-21 | 1,488,327 | 24 |
| [Active Inferants: An Active Inference Framework for Ant Colony Behavior](https://danielarifriedman.com/papers/2021_ActiveInferants/2021_ActiveInferants.pdf) | [10.3389/fnbeh.2021.647732](https://doi.org/10.3389/fnbeh.2021.647732) | 2021-06-24 | 1,004,293 | 14 |
| [Gene expression variation in the brains of harvester ant foragers is associated with collective behavior](https://danielarifriedman.com/papers/2020_GeneExpressionForagers/2020_GeneExpressionForagers.pdf) | [10.1038/s42003-020-0813-8](https://doi.org/10.1038/s42003-020-0813-8) | 2020-03-05 | 1,115,979 | 9 |
| [Context-dependent expression of the foraging gene in field colonies of ants: the interacting roles of age, environment and task](https://danielarifriedman.com/papers/2016_ForagingGene/2016_ForagingGene.pdf) | [10.1098/rspb.2016.0841](https://doi.org/10.1098/rspb.2016.0841) | 2016-08-31 | 536,684 | 9 |

The five additional projected copies total **4,471,163 bytes (4.264 MiB)**. Each individual PDF is below the conservative 5,000,000-byte limit. The independent reservation budget is 5 MiB across **active and retired** aliases; retirement does not free an alias or its budget. This review does not increase the hosting artifact limits or claim a current artifact headroom value.

| Work number | Exact retained PDF SHA-256 | Complete author abstract SHA-256 |
| --- | --- | --- |
| 40 | `0b40c6a4bc0d1dd0d2a9a4597b557132b01187327389c05c5455df713905f7d3` | `666d4ac466b142c3c56b3254f60320ef6409c8fefd49bb72dbc3620dc5619fc2` |
| 48 | `665cb03933df668fdc11286d2c973c6ca4cf2300f4bb716c1e8130996832f364` | `dd5ac31aed6742d6c141542f7b8259ab333b82a5175cb76084a92800f6bc16cc` |
| 75 | `6debf52e3c4fdce8330e5601ce3efb7f2c1d9ca3bbaddaf31cfb824ee96d30e4` | `7d59786352876c8f80678727d89ef16573f591f1ba8c956b424aeac39bd67f54` |
| 86 | `91160c7b340ea9fbd7740a18f968243546ca4dbc95dcfe27b411439fb5a93683` | `eb638271960db10990120e8538b870d123e6af5e59a0179b6385d97d6a4a438c` |
| 104 | `80b790681900c4f9d71b95057711e574664f17dfb9024a315bd28d4ab22530f6` | `f29ea47cad3b3655d1fe534b9c13941f52186676e7351f0e2b3ac9b5e15e90be` |

All five originals retain their existing `papers/` URLs. Each reserved alias is exactly `works/<PDF SHA-256>.pdf`, using the full hash above. It is an additional byte-identical Pages projection, beside the existing `works/<citation_key>.html` abstract page. Original source PDFs are neither rewritten nor moved into `works/` in Git.

## Byline, date, abstract and rights review

The ordered citation bylines agree with the reviewed publisher PDFs:

- **Work 40**: Mahault Albarracin; Riddhi J. Pitliya; Toby St. Clere Smithe; Daniel Ari Friedman; Karl Friston; Maxwell J. D. Ramstead.
- **Work 48**: Karl Friston; Daniel A. Friedman; Axel Constant; V. Bleu Knight; Chris Fields; Thomas Parr; John O. Campbell.
- **Work 75**: Daniel Ari Friedman; Alec Tschantz; Maxwell J. D. Ramstead; Karl Friston; Axel Constant.
- **Work 86**: Daniel Ari Friedman; Ryan Alexander York; Austin Travis Hilliard; Deborah M. Gordon.
- **Work 104**: Krista K. Ingram; Deborah M. Gordon; Daniel A. Friedman; Michael Greene; John Kahler; Swetha Peteru.

The two MDPI dates and the Frontiers date are also printed as publication dates in the reviewed PDFs. The Nature and Royal Society citation dates come from the existing DOI/title-matched registration records, rather than an accepted/received date on the first page. Each exact registration URL is retained in the registry.

All five PDFs yielded substantial nonblank text on their first two pages. Complete current abstract passages match the source PDFs after NFKC and punctuation/whitespace normalization, including removal of extraction line-break hyphenation. This is bounded text/passage evidence, not visual approval of every PDF page.

The initial Shared Protentions and Variational Synthesis fields were shortened curated summaries. Their complete author-written PDF abstracts are now adopted in both the master and per-paper metadata, with explicit source PDF/hash, abstract hash and dated provenance. The other three complete abstracts and their existing provenance remain unchanged. Canonical Active Inferants citation tags and the reviewed PDF use **Alec Tschantz**; the legacy `metadata.creators` spelling “Alexander” is not the byline authority for this pilot.

| Work | Rights observed in retained publisher PDF | Scope |
| --- | --- | --- |
| Shared Protentions | CC BY 4.0, page 1 | Preserve author/source attribution and license link. |
| Variational Synthesis | CC BY 4.0, page 1 | Preserve author/source attribution and license link. |
| Active Inferants | CC BY, page 14 | The reviewed PDF wording does not specify a version; do not invent one. Preserve attribution and cite the original journal publication. |
| Gene Expression Foragers | CC BY 4.0, page 9 | The publisher explicitly reserves separately credited third-party material; those exceptions are not relicensed by this review. |
| Foraging Gene | CC BY 4.0, page 1 | Preserve author/source attribution and license link. |

These findings apply to the identified article bytes. Repository/site licenses do not replace an article's own license or third-party credit lines. The bounded publisher-page check returned HTTP 429 for both MDPI pages, an unavailable identity redirect for Nature, and HTTP 403 for Royal Society; Frontiers full text was available. Retained publisher PDFs supplied the direct byline/abstract/license evidence. No access failure was treated as evidence of absent content or permission.

## Retained aliases and current selection

Reservations bind immutable work identity, exact source PDF bytes and exact hash-derived alias. They are retained when a work is no longer selected, and an old alias cannot be reassigned to different bytes or another identity. Current selections remain independently mutable. A valid remote primary continues to take priority; retiring a local pilot selection preserves its old reserved alias and original URL.

[Google's inclusion guidance](https://scholar.google.com/intl/en/scholar/inclusion.html) informs the placement contract: unique scholarly work pages, visible complete author abstracts or full text, appropriate citation metadata and searchable PDFs in the same directory as the abstract, within the individual size limit. Matching these source/local conditions does not establish that Google fetched or indexed a work.

## Local validation and remaining acceptance

The focused projection suite passed 35 tests. A broader compatibility run passed 329 tests, with three generated-output checks explicitly deferred to owning regeneration; namespace checks passed 18 tests. These runs overlap and are not a cumulative test count. Disposable fixture assembly checked exact alias/original copy bytes, hashes and reservation budgeting. A separate source reviewer checked all five actual PDF hashes, bylines, dates and abstract evidence.

The deferred checks concern generated SEO output and agent-index consistency. Full canonical generation, real artifact assembly/budget checks and final integrated-source validation belong to the integration pass. They are not inferred from the fixture tests or this source review.

After publication and deployment, verify the five original URLs, five retained aliases, selected citation PDF targets and complete visible abstract pages. Record deployed byte/hash and route evidence against the integrated candidate. Actual Scholar inclusion/profile membership and authenticated metrics require separate direct observation. The readiness flags `network_checked` and `indexing_verified` remain false; no sitemap submission, crawler fetch, indexing result or metrics update is asserted here.
