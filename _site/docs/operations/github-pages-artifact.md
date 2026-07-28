# GitHub Pages artifact

GitHub Pages is the public web projection of this repository, not the complete
archive. GitHub documents a 1 GiB maximum for a published Pages site, while the
canonical repository includes paper PDFs and extracted figure images for
provenance and reproducibility.

`.github/workflows/pages.yml` therefore assembles a bounded artifact with
`code/orchestrators/build_pages_artifact.py` and deploys it with the official
Pages artifact workflow. It retains the public HTML, data exports, generated
work/paper pages, full-text files, CV outputs, PDFs, artwork assets, reports,
and agent documentation. It omits only duplicate binary files under
`papers/**/images/`; those source images remain versioned in GitHub.

Generated paper pages link extracted-image galleries to the canonical GitHub
tree and use raw GitHub image URLs for previews. The image sitemap describes
only images actually hosted by the site (the artwork gallery and its supported
remote image sources), so no published sitemap entry points at an omitted
Pages asset.

The artifact builder fails above a 900 MiB safety ceiling, leaving margin below
the Pages limit. Run it locally with:

```sh
python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size
```

The repository remains the source of truth for all omitted files. The public
site's `data/agent-index.json` and `GENERATED.md` describe the canonical
repository datasets and the generated web projection separately.
