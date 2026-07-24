# Release integrity and retention

The repository is the complete archival source; GitHub Pages is the bounded
navigable projection. A public release is not complete until the source,
generated layer, artifact, deployment, and live verification records agree.

## Ordered release gate

1. Refresh public sources deliberately (`refresh_public_sources.py`,
   `refresh_public_source_inventory.py`, GitHub/Zenodo pairing, and Scholar only
   when directly verified).
2. Apply only reviewed source changes and preserve permanent citation keys.
3. Run `uv run python3 code/orchestrators/regenerate_all.py --validate`, then
   run it a second time and require no tracked-file content changes.
4. Run `python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size --check-manifest`.
5. Run `browser_smoke.py`, the progressive `browser_qa.py` suite with the
   cached Playwright runtime, visual QA, and `gsc_followup_preflight.py` after SEO or
   sitemap changes.
6. Verify the deployed site with `verify_live_site.py` after the Pages deployment
   for the source commit being released; require all checked routes, current
   JSON-level counts, Pages status `built`, and a successful deployment run.
7. Confirm the release worktree is clean (the preserved local `_site/` output is
   ignored by this check), then run `uv run python3
   code/orchestrators/build_release_integrity.py --check --require-deployed`.
   The ordinary `--check` gate may pass only when the envelope explicitly
   records `deployment_pending: true`; the strict release gate must pass before
   calling the release deployed.

`data/release-integrity.json` records source and generator hashes, the Pages
artifact summary, deployment metadata, live verification, CV privacy status,
and explicit `deployment_pending_reasons` whenever tracked release content does
not match the recorded deployed commit. Control manifests and dated evidence
are excluded from that content comparison because they are refreshed after
deployment. This prevents stale live evidence from being described as a
completed release.
`data/pages-artifact-manifest.json` records included files and SHA-256 values,
omitted extracted paper-image policy, byte/file budgets, and GitHub fallback URL
templates.

The gallery uses `data/artworks-index.json` for its initial grid and search
metadata. The complete `data/artworks.json` record, including resolution maps,
is loaded only for description search or an opened lightbox. Rebuild the compact
projection through `regenerate_all.py`; never hand-edit either export.

The video timeline uses `data/videos-index.json` for its initial chronology,
channel, and display metadata. The complete `data/videos.json` export remains
available for agents and downloads; topic, relationship, and transcript detail
is not loaded by the timeline until a visitor opens a stable video page.

`browser_qa.py` records the known Chromium warning that meta-delivered CSP
cannot enforce `frame-ancestors`. It is retained as a warning because GitHub
Pages does not expose response-header control; any other console or page error
fails the browser report.

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
