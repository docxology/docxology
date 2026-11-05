# Google Scholar discovery and citation metadata

Each publication retains its bibliography DOI and permanent `works/{citation_key}.html`
URL. Distinct template manuscripts retain separate identities even when they
share a tooling release. Generated work pages expose title, ordered authors,
citation DOI, date, and the selected primary PDF in HTML citation tags, with
matching work identity in JSON-LD. Person/organization author types come from
verified DOI-matching registration records; a comma-free display name alone
does not establish an organization. Unverified literal names remain untyped. They are linked from the static publication
browse interface and included according to the sitemap policy.

`build_work_pages.py` reads reviewed `citation_metadata` from paper metadata
for journal title, volume, issue, ISSN, and page range. Crossref enrichment must
match the curated DOI and title before adoption; Zenodo deposits are not
invented as journal publications. Full citation dates must be valid and agree
with the curated citation year and DOI. Otherwise year-only precision is kept.
`seo_invariants.check_work_citations` verifies title, all authors in order,
DOI, date, journal fields, and the actual eligible primary PDF against sources.

## Bounded same-directory PDF pilot

[Google's inclusion guidance](https://scholar.google.com/intl/en/scholar/inclusion.html)
requires the PDF selected by `citation_pdf_url` to share the abstract page's
subdirectory. The reviewed pilot declares byte-identical, content-addressed
`works/<sha256>.pdf` aliases for selected journal articles in
[`data/scholar-pdf-projections.json`](../../data/scholar-pdf-projections.json).
The [dated source review](../../reports/scholar_pdf_placement_review_2026-11-05.md)
records the five selected documents, rights evidence, searchable first-page
text, ordered bylines, dates and complete author-written abstracts. The two
MDPI abstracts were adopted in full from the retained publisher PDFs.

The shared [projection resolver](../../code/src/scholar_pdf_projection.py)
validates exact work identity, source bytes, review bindings and immutable
destination reservations. The Pages assembler creates aliases only in its
output; no duplicate PDFs are added to the repository. Each file must be at
most 5,000,000 bytes, and all reserved aliases together must stay within a
5 MiB aggregate allowance. Retired reservations remain hosted and budgeted.
Changing a selected edition never reassigns an existing alias to new bytes.
Reviewed remote primaries retain priority over aliases; original `papers/`
PDFs and their public URLs remain available.

The work-page citation tag, download link and structured data use the same
selected resource. The readiness audit binds the selected bytes and checks
that the complete reviewed abstract remains visible in static HTML. Hidden,
collapsed or substituted summaries fail that contract. Declared alias paths
are recognized precisely by link and SEO checks, then copied and hashed by
the artifact builder under the unchanged 930 MiB CI budget and 950 MiB hard
ceiling. The assembled manifest records alias membership and source custody.

Local HTTP route checks must serve the assembled Pages output, for example
after `uv run python3 code/orchestrators/build_pages_artifact.py --output <fresh-output> --check-size`.
The reserved `works/<sha256>.pdf` files are materialized in that output and do
not exist in the source checkout.

The [October proposal](../../reports/scholar_pdf_placement_proposal_2026-10-13.md)
is historical planning evidence. The current registry and dated review own the
implemented pilot. Other works can retain cross-directory archival links or
reviewed remote editions; the pilot does not establish their eligibility.
Google also requires scholarly content, searchable files and freely visible
full text or complete author-written abstracts. Source review, generated-page
agreement, deployment verification and actual indexing are separate checks.
Do not compress or rewrite source PDFs merely to claim inclusion.

The 2026-10-12 source pass populated citation metadata for 22 DOI/title-matched
Crossref records, including 19 journal articles. Ten further requests returned
HTTP 429. A subsequent bounded sequential pass recovered and DOI/title-matched
all ten records, completing enrichment of the 32 Crossref-backed paper folders
(including 29 journal articles). These counts describe the dated source passes,
not a permanent catalog total.

## Repeatable review and local audit

`uv run python3 code/orchestrators/review_citation_metadata.py --output /private/tmp/citation-review.json`
fetches bounded, sequential Crossref proposals without applying metadata. Use
`--citation-key <permanent-key>` repeatedly to narrow a pass. DOI and normalized
title must both match; malformed records, title/DOI mismatches, and HTTP errors
remain explicit non-adoptable results. No source identity or Scholar metrics are
written. Review each proposed field against its linked registration record before
adopting `citation_metadata` in the eligible paper's `metadata.json`, then regenerate.
Unchanged semantic metadata preserves its earlier adoption timestamp. A fresh
request timestamp in the proposal is distinct from that reviewed adoption date.
Report destinations inside the repository must be under `reports/`; symlinks and
hardlinks are rejected. External destinations need an existing real parent
(`/private/tmp` on macOS).

`uv run python3 code/orchestrators/build_scholar_readiness.py` builds the
[per-work audit](../../reports/scholar_readiness.md) and
[JSON dataset](../../data/scholar-readiness.json). The ordered generation plan
and standard validation run its exact `--check` mode. It records real head tags,
selected public PDF hashes, size, and directory placement. The audit uses a
conservative decimal 5,000,000-byte interpretation of Google's 5 MB ceiling.
It preserves source PDFs and permanent URLs. Missing local PDFs are observations
about this archive, not claims that no external full text exists.
Citation evidence excludes template contents and later body head lookalikes;
blank required fields, missing catalogued DOI tags, and duplicate singleton
tags remain local blockers. Repeated ordered author tags are valid. This
lightweight parser is not a complete HTML5 tree builder; the exact source
identity gate and browser QA remain separate checks.

The configured pilot records reviewed searchable text, scholarly suitability
and complete author-written abstracts as prerequisites. Those observations do
not verify every catalog item or actual Scholar indexing. The
catalog includes software, courses, books, and other material; a local blocker
count is not an estimate of how many scholarly articles Google should index.
The dataset is discoverable through the website data catalog and agent schema
registry. It does not replace authenticated Search Console or Scholar review.

## Verification and follow-up

Run `uv run python3 code/orchestrators/regenerate_all.py --validate` and the
repository tests after citation-source changes. If a tracked public-source
snapshot was refreshed before payload landing, use the explicit narrow
`--allow-dirty-prepayload-evidence` mode described in
[settle.md](../operations/settle.md); ordinary clean and release checks stay strict. Run
`uv run python3 code/orchestrators/gsc_followup_preflight.py --check` for local
SEO and live hub readiness. A preflight success does not verify that unpublished
PR content is live, that Google indexed a URL, or that Scholar merged versions.

After the changes land and deploy, verify the new work pages and PDFs directly,
then use the signed-in [Search Console runbook](gsc-followup.md) to submit the
sitemap and inspect selected work URLs. Scholar profile membership and indexing
must be checked separately. The [2026-11-05 signed-in Search Console observation](../../reports/gsc_observations_2026-11-05.md)
records successful sitemap discovery, an initial indexing-request service
failure, and a later live-test attempt with an unconfirmed outcome. No accepted
indexing request was observed. Actual indexing and Scholar review remain
separate checks.
Keep `data/scholar-snapshot.json` and its receipt unchanged until a direct
authenticated observation is recorded through the declared tool.
