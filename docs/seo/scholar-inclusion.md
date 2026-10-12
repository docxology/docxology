# Google Scholar discovery and citation metadata

Each publication retains its bibliography DOI and permanent `works/{citation_key}.html`
URL. Distinct template manuscripts retain separate identities even when they
share a tooling release. Generated work pages expose title, ordered authors,
citation DOI, date, and the selected primary PDF in HTML citation tags, with
matching work identity in JSON-LD. They are linked from the static publication
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
HTTP 429; those records retain their prior metadata. Refresh those missing
fields in a later bounded source pass, then regenerate and validate. These
counts describe that dated pass, not a permanent catalog total.

## Verification and follow-up

Run `uv run python3 code/orchestrators/regenerate_all.py --validate` and the
repository tests after citation-source changes. Run
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
