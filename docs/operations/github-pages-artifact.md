# GitHub Pages artifact

GitHub Pages is the public web projection of this repository, not the complete
archive. GitHub documents a 1 GB maximum for a published Pages site. Existing
paper PDFs and extracted figures remain in the repository for provenance;
reviewed versioned Zenodo deposits can hold new primary PDF editions.

`.github/workflows/pages.yml` therefore assembles a bounded artifact with
`code/orchestrators/build_pages_artifact.py` and deploys it with the official
Pages artifact workflow. Deployment waits for both repository validation and
the reusable required browser acceptance job in
`.github/workflows/browser-qa.yml`; a failure in either blocks publication.
The validation workflow calls that same browser job. It retains the public HTML, data exports, generated
work/paper pages, available full-text files, CV outputs, existing local PDFs, artwork assets, report
manifests, and agent documentation. It omits duplicate binary files under
`papers/**/images/`, dated visual-QA screenshot binaries under
`reports/visual-qa/*/` and the legacy `reports/YYYY-MM-DD/*` capture layout,
and superseded dated reports: a top-level
`reports/<family>_<YYYY-MM-DD>` receipt strictly older than the newest receipt
of its family, and whole dated screenshot directories under
`reports/visual-qa/`, `reports/browser-smoke/`, and `reports/browser-qa/`
older than that parent's newest date, leave the projection. A report
referenced from a published page or data file is never omitted. Every omitted
file remains versioned in GitHub.

Generated paper pages link extracted-image galleries to the canonical GitHub
tree and use raw GitHub image URLs for previews. The retired image sitemap is not recreated or submitted. Current sitemap
entries describe hosted routes; extracted-image previews and archival fallbacks
are checked separately, so a sitemap must not advertise an omitted Pages asset.

The artifact builder emits a review warning at 930 MiB; ordinary CI enforces
that 930 MiB budget. The projection growth target is at most 890 MiB, preserving
40 MiB of ordinary-CI headroom. The builder separately fails at the
950 MiB release hard ceiling, and records a 1 GiB configured outer bound separately from GitHub's published
1 GB limit. (Raised from the 850/890/900 MiB tiers on
2026-10-31 after the versioned publication intake pushed the measured
projection to 911.45 MiB; the owner retained the existing hosted PDFs and
widened the tiers. New intake follows the PDF hosting policy below. The measured
artifact must still stay below the ceiling before every deploy.) The current full server-rendered
`publications.html` is allowed a 600 KB page-budget exception because it
retains crawlable bibliography rows and inline collection JSON-LD; the asset
audit records the exception and its reason. Run the artifact check locally with:

```sh
uv run python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size
```

`data/pages-artifact-manifest.json` anchors its
`source_commit_at_generation` to the latest commit containing published payload
content. A final, control-only commit may then add the Pages manifest, agent
index, release-integrity envelope, generated manifest, dated public-source
review, and growth receipt without making that SHA self-referential. The
shared `code/src/release_controls.py` policy recognizes only exact, valid
date-stamped control-report names at the top-level `reports/` directory; a
nested or ad hoc report remains payload. A commit that changes only CI
configuration (`.github/workflows/*.yml` or `.github/dependabot.yml`, both
under the excluded `.github` root and read by no generator) is
payload-neutral: the walk passes over it, so a Dependabot action bump needs no
control tail and validates as-is. Any other path in the same commit, including
the generated `.github/README.md`, keeps it a payload commit
(`code/tests/test_payload_neutral_ci.py`). After committing any payload change,
regenerate these control artifacts and commit them separately (ordering
rules: [settle.md](settle.md) Notes, binder ordering);
`--check-manifest` rejects a manifest that still names an older payload commit
after a later content change.

The repository remains the source of truth for its omitted committed files. The public
site's `data/agent-index.json` and `GENERATED.md` describe the canonical
repository datasets and the generated web projection separately.

Browser and visual QA manifests remain in the Pages projection. Visual QA
manifests retain repository-relative screenshot paths and SHA-256 digests,
while their PNG or other screenshot binaries are retrieved from the Git commit
that contains the evidence path. The Pages artifact manifest records the
omitted visual-QA screenshot count, byte total, examples, and GitHub raw/tree
URL templates. The manifest also records the `omitted_superseded_reports`
summary (count, bytes, examples) next to the paper-image and visual-QA
summaries; the growth receipt mirrors its count and byte total. The GitHub
tree/raw fallback templates apply unchanged because omitted reports remain at
the source commit. As a durable 404 guard, the builder scans the assembled
projection for repository-relative `reports/` references and fails the build
if any referenced repository path was not copied (GitHub raw/tree fallback
URLs do not count as local references); this is an artifact-boundary decision,
not deletion or report pruning.

The legacy dated capture layout is matched only for real calendar dates and
direct child image files; arbitrary report images and nested directories do
not inherit the omission rule. Existing local PDFs and available full text remain
hosted. Reviewed supporting Office
documents may instead use pinned GitHub source downloads, declared in
`data/pages-archive-documents.json`. The transcript has both a hosted PDF and
a visible link to its original Office source archive. Archive routing requires
exact source/committed-object byte agreement and rejects any surviving local
download reference; it never deletes repository source bytes. No source evidence is deleted by this policy.

## Scholarly discovery aliases

The [reviewed projection registry](../../data/scholar-pdf-projections.json)
reserves content-addressed `works/<sha256>.pdf` aliases beside selected abstract
pages. The shared resolver verifies source hashes, exact identities, rights
evidence and complete abstracts before the assembler copies bytes into its
output. These are additional web routes, with no duplicate source PDFs in Git.
All reservations, including retired associations, consume a 5 MiB aggregate
allowance; each document is at most 5,000,000 bytes. Original download routes
remain hosted and selected remote editions retain priority. Alias growth must
also pass the unchanged whole-site budget. The manifest records each alias,
source, hash, bytes and license evidence. See [Scholar inclusion](../seo/scholar-inclusion.md)
for source review, exact local checks and separate deployed/indexing acceptance.

## Primary PDF hosting and source custody

For new publications and editions, prefer an existing versioned Zenodo PDF
archive. Keep curated metadata, stable work/paper pages, available extracted text,
and previews in this site. Existing local originals and their public URLs remain
hosted; a reviewed remote primary selects the current edition while older local
PDFs remain historical attachments. This policy does not authorize bulk migration,
repository creation, deletion, or a budget increase.

Declare a remote primary in the paper's `metadata.json` as `remote_primary_pdf`
with `name`, `url`, `version`, `record_id`, `bytes`, and `sha256`. The shared
[`PaperResources` resolver](../../code/src/paper_artifacts.py) owns validation and
primary selection. Its current remote backend accepts only an exact versioned
Zenodo file URL for the named record and file; a concept DOI or mutable latest
link cannot select the bytes. GitHub Releases may be considered as a future
backend, but are not accepted by this contract.

Record the independent source observation in `source_evidence.json`: its
`source_pdf` names the exact record, filename, URL, version, byte count, and
SHA-256. An `extraction` names its text file and SHA-256 and binds
`source_pdf_sha256` to the source PDF, with the tool and method; `review_scope`
states what was checked, and `historical_sources` preserves prior editions.
A declaration alone does not fetch the PDF or verify its remote bytes. Preserve
historical originals and extraction provenance, and do not present text from a
previous edition as the current remote PDF's extraction.

Generated download links, citation PDF metadata, and JSON-LD use the selected
primary through the shared resolver. The Pages manifest and deployed-artifact
checks describe files hosted by this site; source evidence and remote availability
remain separate from that deployed-byte scope. Follow
[publication-sync.md](publication-sync.md#pdf-hosting-decision) for intake.

After deployment, the Pages workflow runs `verify_deployed_artifact.py` and
retains `deployment-acceptance-<full SHA>` as an Actions artifact for 90 days.
It checks exact manifest and critical-asset/work-page hashes, all locally hosted
paper PDF HEAD contracts, and three deterministic hosted PDF content hashes. Failed
checks fail the workflow and retain diagnostics. This technical receipt is
bounded to 12 minutes across requests and propagation retries, with a separate
15-minute hosted step limit so an exhausted deadline can still retain its
failure receipt. Queued checks after the deadline are explicitly unattempted.
The receipt is
separate from the human-reviewed full release attestation in
[release-integrity.md](release-integrity.md).
