# Scholar PDF placement proposal — 2026-10-13

This is a measured proposal, not an applied migration or Scholar indexing claim.
The [hash-bound plan](scholar_pdf_placement_proposal_2026-10-13.json) uses the
[prerequisite audit](../data/scholar-readiness.json) and the main revision
`6eaa02173ea8c6bfa46d510784235934f1cde7be` artifact manifest. Its measurements are
historic inputs; re-measure the candidate before implementing any copy.

## Proposal

Keep every permanent work page and archival PDF URL. A future explicit web
projection could copy reviewed, byte-identical PDFs under `/works/<sha256>.pdf`,
beside the abstract pages, and point `citation_pdf_url` at that projection.
Content-addressed names bind copies to the preserved archive. Old PDF URLs
continue to serve the source; no recompression or archive rewriting is proposed.

| Measurement | Value |
| --- | ---: |
| Current artifact (MiB) | 864.93 |
| All size/tag-qualified copies (MiB) | 209.89 |
| Illustrative pilot PDF count | 69.00 |
| Pilot copies (MiB) | 19.85 |
| Metadata reserve (MiB) | 1.00 |
| Projected pilot plus reserve (MiB) | 885.77 |
| Unchanged CI ceiling (MiB) | 890.00 |
| Growth target (MiB) | 850.00 |

## Gates and tradeoffs

The pilot fits the unchanged hard ceiling, but the existing artifact already
exceeds the growth target. Prefer a deliberate report-provenance projection
migration before adding PDF copies. Historical pairing receipts may be served
through immutable commit/hash-bound archive locators; their current local
provenance consumers must migrate first. URL string replacement alone does not
release their bytes under the current reference scanner. Never omit evidence
while projected consumers still require a local path, and never silently delete
archived reports or screenshots.

The smallest-first list demonstrates capacity; it does not select eligible
scholarly articles. Each PDF still needs searchable-text, scholarly-content,
and author-written abstract/full-text review. Oversized PDFs and works without a
selected local PDF remain outside this illustration.

Before applying: declare the projection/source mapping and its writer/check;
validate selected source hashes, generated citation URLs, exact artifact file
membership, and the fresh unchanged byte ceiling; exercise preserved old URLs
and deployed new URLs. Human review and actual Scholar indexing are separate.
No files have been copied and no citation URLs have changed.
