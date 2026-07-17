# Release integrity and retention

The repository is the complete archival source; GitHub Pages is the bounded
navigable projection. A public release is not complete until the source,
generated layer, artifact, deployment, and live verification records agree.

## Ordered release gate

1. Refresh public sources deliberately (`refresh_public_sources.py`,
   `refresh_public_source_inventory.py`, GitHub/Zenodo pairing, and Scholar only
   when directly verified).
2. Apply only reviewed source changes and preserve permanent citation keys.
3. Run `uv run python3 code/orchestrators/regenerate_all.py --validate`.
4. Run `python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size --check-manifest`.
5. Run browser smoke, visual QA, and `gsc_followup_preflight.py` after SEO or
   sitemap changes.
6. Verify the deployed site with `verify_live_site.py`; require 17/17 routes,
   current JSON-level counts, Pages status `built`, and a successful deployment
   run.

`data/release-integrity.json` records source and generator hashes, the Pages
artifact summary, deployment metadata, live verification, and CV privacy status.
`data/pages-artifact-manifest.json` records included files and SHA-256 values,
omitted extracted paper-image policy, byte/file budgets, and GitHub fallback URL
templates.

## Retention tiers

- Current accessibility, asset, live, source, and growth reports remain checked
  in and available through Pages and the agent manifest.
- Historical visual-QA screenshots, public-source snapshots, and pairing reports
  remain in GitHub or a release archive when they are removed from the Pages
  projection.
- Any deletion or pruning requires a dated manifest entry that preserves the
  original report path, generation date, source hash, and replacement location.

Never delete source evidence or rewrite history as a substitute for retention
policy. Use `TODO.md` for unresolved review work.
