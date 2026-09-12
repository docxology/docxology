# GitHub Pages artifact

GitHub Pages is the public web projection of this repository, not the complete
archive. GitHub documents a 1 GiB maximum for a published Pages site, while the
canonical repository includes paper PDFs and extracted figure images for
provenance and reproducibility.

`.github/workflows/pages.yml` therefore assembles a bounded artifact with
`code/orchestrators/build_pages_artifact.py` and deploys it with the official
Pages artifact workflow. It retains the public HTML, data exports, generated
work/paper pages, full-text files, CV outputs, PDFs, artwork assets, report
manifests, and agent documentation. It omits duplicate binary files under
`papers/**/images/`, dated visual-QA screenshot binaries under
`reports/visual-qa/*/`, and superseded dated reports: a top-level
`reports/<family>_<YYYY-MM-DD>` receipt strictly older than the newest receipt
of its family, and whole dated screenshot directories under
`reports/visual-qa/`, `reports/browser-smoke/`, and `reports/browser-qa/`
older than that parent's newest date, leave the projection. A report
referenced from a published page or data file is never omitted. Every omitted
file remains versioned in GitHub.

Generated paper pages link extracted-image galleries to the canonical GitHub
tree and use raw GitHub image URLs for previews. The image sitemap describes
only images actually hosted by the site (the artwork gallery and its supported
remote image sources), so no published sitemap entry points at an omitted
Pages asset.

The artifact builder emits a documented review warning at 880 MiB, fails at the
900 MiB release hard ceiling, and records GitHub's 1 GiB platform limit as a
separate physical constraint. The current full server-rendered
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
nested or ad hoc report remains payload. After committing any payload change,
regenerate these control artifacts and commit them separately (ordering
rules: [settle.md](settle.md) Notes, binder ordering);
`--check-manifest` rejects a manifest that still names an older payload commit
after a later content change.

The repository remains the source of truth for all omitted files. The public
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
