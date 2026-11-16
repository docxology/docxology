# Wave 2A hardening — 2026-11-16

Candidate base: `d9a4d674e3efa1a8789e259e9172a30f1ee62b7f`.

The metadata audit uses codepoint comparisons instead of supplementary-plane regex ranges. Unit tests cover all specified endpoints, adjacent values, ordinary text, malformed dates, and paper validation.

Public repository links require the public inventory or a separately observed GitHub redirect to the same numeric public repository ID. The redirect observation is dated in `data/public-repository-redirects.json`; redirects do not add repositories to canonical counts.

`data/public-link-evidence.json` records exact retained evidence paths and SHA-256 values. Historical reports and archived document extractions retain their literal bytes. Eight current report consumers use sanitized copies under the existing `public-owned-repositories-v1` policy. Historical decision citations point to immutable GitHub blobs with original hashes. Projection copies retain records and counts, substituting unavailable URL text; they do not renew observation dates or establish new upstream facts. Source observations remain publicly retrievable in the repository archive. This change makes no history-erasure claim.

COGSEC works 071, 079 and 089 explicitly say “EDITED BY” in their verified source records. Their `citation_editor` tags remain accurate. The advisory to emit `citation_author` is evidence-limited and was not adopted: editor-only volumes may not receive Scholar author-profile attribution. Work 237's reviewed registry and document baseline preserves 53 institutional, individual and grouped credit units. Comma-joined credits and its existing versioned PDF URL remain unchanged.

Counts on the publications and evidence pages already derive from canonical source data. The start page now participates in the same synchronization. Scholar citation metrics were not refreshed.

This is a pre-integration engineering record, not a release attestation. Validation receipts, hosted checks and the independent reviewer gate must be assessed for the final candidate SHA. No merge or deployment is authorized by this report.

## Profile, security and feed behavior

The profile README uses absolute published-site or GitHub source links so the same document works in both GitHub rendering contexts. Security contacts point at the repository's vulnerability-reporting policy. The agent manifest reports pending post-deploy attestation rather than promoting an older live report into verification of the current candidate; the release envelope retains the same boundary.

RSS maintenance and publication entries share one deterministic descending date order, with stable identifier tie-breaks. Year-only publication dates retain the existing January 1 convention; genuinely undated records do not acquire an invented publication date. Redacted repository markers cannot become platform hyperlinks.
