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

## Remaining Scholar requirements

[Google's inclusion guidance](https://scholar.google.com/intl/en/scholar/inclusion.html)
requires the PDF specified by `citation_pdf_url` to be in the same subdirectory
as its HTML abstract. This site currently serves canonical abstracts under
`works/` and archival PDFs under `papers/`. The cross-directory links are
valid site links but do not meet that placement requirement. Keep the existing
permanent URLs and Pages artifact ceiling; do not copy the entire PDF archive
into `works/` or claim this gap is resolved. A future proposal must preserve
inbound links, bind projected files to source hashes, and pass the unchanged
artifact budget before changing placement.

The guidance also requires searchable PDFs no larger than 5 MB, scholarly
content, and freely visible full text or complete author-written abstracts.
Those requirements are separate from valid HTML metadata. A generated summary,
book, editorial, or oversized document is not automatically eligible. Do not
compress or rewrite source PDFs merely to claim inclusion.

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

Searchable PDF text, scholarly suitability, complete author-written abstracts
or full text, and actual Scholar indexing remain explicitly unverified. The
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
must be checked separately. The available browser on 2026-10-12 was signed out;
no property submission or authenticated Scholar metrics refresh was performed.
Keep `data/scholar-snapshot.json` and its receipt unchanged until a direct
authenticated observation is recorded through the declared tool.
