# Release integrity and retention

The repository is the complete archival source; GitHub Pages is the bounded
navigable projection. A public release is not complete until the source,
generated layer, artifact, deployment, and live verification records agree.

## Ordered release gate

1. Refresh public sources deliberately (`refresh_public_sources.py`,
   `refresh_public_source_inventory.py`, and GitHub/Zenodo pairing), then write
   the dated review report. Queue new Zenodo candidates, ambiguous DOI changes,
   repository classifications, and Scholar or biographical changes for explicit
   review. Scholar metrics may change only after a direct authenticated profile
   verification is recorded; a cached or anonymous result is not evidence. Bind
   each curated snapshot revision to
   `data/scholar-verification-receipt.json`; its SHA-256 must match
   `data/scholar-snapshot.json`, and `sync_scholar_metrics.py --check` rejects
   a missing, stale, or non-direct/authenticated receipt.
2. Apply only approved source changes, preserve permanent citation keys, and
   use `pages/BIBLIOGRAPHY.md` as the canonical citation DOI surface. Preserve a
   version/download DOI in `metadata.json` as `artifact_doi` rather than
   replacing the citation DOI.
3. Run `uv run python3 code/orchestrators/regenerate_all.py`, then run it a
   second time and require no tracked-file content changes.  During this
   pre-payload phase, the writer may incorporate only a current
   `public_source_snapshot` that explicitly records
   `source_worktree_clean: false`; that snapshot is reviewed source evidence
   to commit with the payload, not an attestation receipt.  Commit the payload,
   regenerate the control tail in a clean worktree, and only then run strict
   `validate_repo.py --strict-reports`.
4. Run `uv run python3 code/orchestrators/build_pages_artifact.py --output /tmp/docxology-pages --check-size --check-manifest`.
5. Run `uv run --extra browser-qa python3 code/orchestrators/browser_smoke.py`,
   the progressive `browser_qa.py` suite with the cached Playwright runtime,
   visual QA, and `uv run python3 code/orchestrators/gsc_followup_preflight.py`
   after SEO or sitemap changes. Visual QA creates a pending capture; it cannot
   be reviewer-stamped while capturing.
6. Verify the deployed site with `verify_live_site.py` after the Pages deployment
   for the source commit being released; require all checked routes, current
   JSON-level counts, Pages status `built`, and a successful deployment run.
7. After Pages reports the candidate SHA as built, re-run the affected browser,
   visual, raw-link, and live-site evidence against that exact SHA. Inspect the
   pending `reports/visual-qa/<date>/*.png` set, then approve that same set with
   `uv run --extra browser-qa python3 code/orchestrators/visual_qa.py
   --approve-existing --reviewed-by <reviewer>`; approval verifies the recorded
   PNG hashes and coverage before it changes only the review record. A confirmed
   external-link 404 blocks attestation; bot-protected, rate-limited, and
   transient results remain explicit review warnings. Do not regenerate the
   external-link triage derivative at this point: it is a pre-deploy cache/review
   queue, while the exact fresh raw-link report is the attested evidence. In the
   source-clean primary candidate checkout (apart from declared fresh receipts),
   re-render the public-source review with `uv run python3
   code/orchestrators/build_public_source_review.py --exact-source-revision`,
   then create a receipt with `uv run python3
   code/orchestrators/attest_release.py --apply --commit <deployment-sha>`, then
   run `uv run python3 code/orchestrators/validate_repo.py --release
   --release-commit <deployment-sha> --deployment-attestation
   reports/deployment-attestations/<deployment-sha>.json`. A release-ready
   claim is prohibited until this final command passes.

## Managed security-scan boundary

`codex-security:deep-security-scan` has not run in this environment because its
required managed filesystem permission profile is unavailable. Its absence is
not a passing result and does not contribute to a release-ready claim. When
that profile is available, run the scan against the clean candidate, retain its
evidence and limitations, and triage validated findings under
[`SEC-002`](../../TODO.md) before a security-sensitive release.

The final release gate permits only `_site/` and the narrowly defined fresh
post-commit evidence/attestation paths to appear in the checkout. Those files
are evidence generated for an already committed candidate, not source changes;
every other tracked or untracked source path still fails the clean-worktree
check. To preserve normal generator semantics, `validate_repo.py --release`
runs its full strict source validation in a disposable detached worktree at the
exact committed candidate, then validates fresh deployed-SHA receipts only in
the real checkout. This is isolation, not a path-based bypass: the outer
worktree still rejects every non-evidence change and the attestation still
hashes and validates each fresh receipt.

The Pages manifest is deliberately non-self-referential: after committing the
payload/generator candidate, regenerate the control artifacts and commit that
control-only tail. Its `source_commit_at_generation` remains the candidate
payload SHA. The Pages check permits only that narrow tail and fails if any
later commit changes published content while the manifest still names the old
SHA.

The dated pre-deploy public-source review follows the same control-tail policy:
its default renderer records the last payload revision and tree so the report
can be committed with other controls without becoming permanently stale. This
is distinct from post-deploy evidence. Regenerate it with
`build_public_source_review.py --exact-source-revision` in the clean deployed
candidate checkout before attestation; only that mode can satisfy the release
gate's exact deployed-SHA provenance requirement.

`data/release-integrity.json` is a pre-deploy envelope: it records source and
generator hashes, the Pages artifact summary, CV privacy status, and the
required post-deploy attestation path. It deliberately does not ingest mutable
live-site reports, so a fresh deployed-SHA verification cannot make a tracked
pre-deploy artifact stale. Only `attest_release.py` and
`validate_repo.py --release` may establish deployment readiness.

The post-deploy attestation validates the exact report paths and their hashes,
not merely the newest files matching a glob. It requires completed public-source
snapshot/review, link, browser smoke/QA, visual-review, and live-site receipts
that all name the candidate SHA. The review report must also name the exact
public-source snapshot hash it assessed.
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
  in and available through Pages and the agent manifest. Browser and visual QA
  manifests also remain public, with exact screenshot paths and SHA-256 values.
- Visual-QA screenshot binaries remain in GitHub as canonical evidence but are
  omitted from the bounded Pages projection; use a GitHub raw/tree template
  with the commit that contains the evidence path to retrieve them. Historical
  visual-QA screenshots, public-source snapshots, and pairing reports remain in
  GitHub or a release archive when they are removed from the Pages projection.
- Any deletion or pruning requires a dated manifest entry that preserves the
  original report path, generation date, source hash, and replacement location.

Never delete source evidence or rewrite history as a substitute for retention
policy. The executable policy and review-record format are in
[`report-retention.md`](report-retention.md). Use `TODO.md` for unresolved
review work.
