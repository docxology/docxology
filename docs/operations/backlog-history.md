# Historical backlog notes

These completed review and session notes were previously kept in `TODO.md`.
The active backlog is [TODO.md](../../TODO.md); the public change record is
[CHANGELOG.md](../../CHANGELOG.md). Dates, measurements, and verification claims
below describe those historical passes rather than current repository state.

## Completed / Closed (2026-08-01)

Implemented and verified (validated against source; the 231-test suite and the
affected orchestrators' `--check` gates pass):

Review-pass fixes:
- `code/orchestrators/submit_indexnow.py` — catch `URLError` (exit 1, no traceback).
- `code/orchestrators/ensure_social_meta.py` — HTML-escape injected og/twitter values.
- `code/orchestrators/build_evidence_page.py` — guard empty `claim["sources"]`.
- `code/orchestrators/build_catalog.py` — remove fabricated stale fallback counts
  (works/software are required inputs).
- `code/orchestrators/generate_feed.py` — guard non-numeric `year` in the sort key.
- `code/orchestrators/build_paper_pages.py` — fail loudly on per-work render errors.
- `code/orchestrators/migrate_inline_handlers.py` — correct the `data-nav-toggle` docstring.
- `code/orchestrators/generate_citation_cff.py` — YAML-escape title/version/names;
  grant the DAF ORCID only to Daniel Friedman.
- `code/src/youtube_fetcher.py` — reject impossible `upload_date` values.
- `GENERATED.md` — matrix rows for `build_reproducibility_ledger.py` and
  `fetch_work_authors.py`; relabel `deploy_seo_security.py`.
- `code/AGENTS.md` — stale "~20 orchestrators" → "~26".

Comprehensive follow-up pass:
- **SEC-001 (path traversal):** `add_zenodo_only.py` and
  `sync_paired_publications.py` now sanitize the Zenodo file `key` to its
  basename and verify the resolved target stays inside the paper folder
  (`_pdf_target` helper). + `code/tests/test_zenodo_pdf_safety.py` (4 tests).
- **Test-mock removal:** `youtube_fetcher.fetch_tab`/`fetch_channel` accept an
  injectable `runner`; `submit_bulk` accepts an injectable `opener`. Rewrote
  `test_youtube_fetcher.py` and `test_submit_indexnow.py` to use real injected
  fakes and to assert the constructed request — no `unittest.mock` left in the
  fetch/indexnow tests.
- **Tautological test:** `test_search_utils.py` now executes the real `esc()`
  through Node on concrete inputs (skips if node absent).
- **Negative-fixture coverage:** `test_seo_invariants.py` now proves
  `check_social_meta`, `check_work_descriptions`, `check_sitemap_policy`, and
  `check_paper_pages` each flag a constructed violation (tmp_path).
- **`errors="ignore"` → `errors="replace"`:** `fetch_video_transcripts.py`,
  `audit_publication_skills.py` (refresh_public_source_inventory already used
  replace/strict).
- **Stale dated-report fallbacks removed:** `build_catalog.py`,
  `build_evidence_page.py`, `build_generated_manifest.py`, `build_agent_index.py`,
  `build_search_index.py`, `export_agent_data.py` now fail cleanly when a report
  is missing instead of emitting a hardcoded 2026-05/06 path.
- **`export_agent_data.py`:** claim `sources` now cite the computed latest
  snapshot path (`_SNAPSHOT_SOURCE`) instead of a hardcoded 2026-06-09 file.
- **Hardcoded `dateModified`:** `build_evidence_page.py` and
  `build_exports_page.py` derive it from `data/current-counts.json` generated_at.
- **Misc robustness:** `build_video_pages.py` skips id-less records and makes
  `iso_date` safe; `verify_live_site.py` guards malformed `.get("datasets")` /
  `.get("items")` shapes; `build_image_sitemap.py` warns when the 1000-image cap
  truncates; `build_domain_pages.py` guards non-numeric `year` in the sort key.
- **Test brittleness:** `test_resume_data.py` asserts Scholar citations against
  `data/scholar-snapshot.json` instead of the hardcoded `777`.

## Session findings (2026-09-08)

Live-verification repair pass (PRs #16/#17) plus a CI-robustness PR:

- **MINOR (fixed in the 2026-09-08 PRs #16/#17):** the `Verify live site`
  workflow had failed on every run since it shipped (2026-09-05): (a) the
  deploy-freshness step truncated main's HEAD to 7 chars while deployed
  stamps are git's auto-lengthened short form (`8ecdaa07`, 8 chars), so
  `8ecdaa07 != 8ecdaa0` retried through the whole grace window; (b) the
  expectation target itself was unsatisfiable — page stamps are deliberately
  reused across non-rendering commits (`build_stamp.reuse_or_current`), so
  "stamp == main HEAD" can stay stale for weeks on a fresh deploy. Fixed with
  prefix stamp semantics plus an artifact-stamp expectation (the committed
  `index.html`), and — once the freshness step passed for the first time — a
  stale raw-serialization marker pin in `verify_live_site.py` (spaced
  `"@type": "CollectionPage"` vs the compact emission), now replaced by
  structural JSON-LD parsing (`jsonld_types_in_html`) asserting `@type`
  values, immune to generator re-serialization. The workflow has been green
  end-to-end since.
- **MINOR (observed, fixed in the 2026-09-08 robustness PR):** the
  Lighthouse budget gate tripped on shared-runner variance — main's
  browser-tests failed with `index.html performance=52 < baseline floor 55`
  on a byte-identical homepage that had passed four PR runs and re-passed
  green on rerun (the file's own baseline comment records ±20 swings, 76/75/57,
  on identical content). Per-page scoring now takes the **median of 3 runs**
  when the first run lands below a floor; a single noisy dip no longer fails
  the gate while a genuine regression stays below the median. Floor values
  are unchanged (integrator-owned).

## Session findings (2026-09-07)

Reconciliation pass findings; resolved-in-PR items are recorded here with
evidence and belong in `CHANGELOG.md` at merge time:

- **MEDIUM (fixed in the 2026-09-07 PR):** `build_search_index.py` stamped the
  main `search-index.json` and its three split companions with *different*
  `generated_at` timestamps whenever the rendered body changed —
  `stable_generated_at` returned `None`, and `render()` / `render_split()` each
  called the clock again. Every content-changing regeneration therefore
  committed a self-inconsistent tree that failed `validate_repo.py --check`
  (observed as the 2 s skew in f58f0be9 and the 3 s skew in 71506b8b; the
  committed tree failed the gate until the next idempotent re-run). Fixed by
  resolving one timestamp before rendering all four surfaces, with a
  regression test (`code/tests/test_build_search_index.py`) that fails under
  the old writer.
- **MINOR (no action):** the `check_external_links` 2026-09-05 triage shows no
  hard 404s — all 129 warnings are bot-protected/rate-limited (403/429),
  timeout, or transient-outage classifications; `wiki.santafe.edu` (connection
  failure) and `dfri.people.stanford.edu` (503) remain the only two
  manually-verifiable candidates and both are already visible in the dated
  triage.
- **MEDIUM (fixed in the 2026-09-07 PR):** the `pull_request` event of
  `.github/workflows/validate.yml` checked out the synthetic merge ref, whose
  first parent is the base branch — so its first-parent diff is the entire PR
  and `source_payload_commit` resolved to the merge commit, failing
  `build_pages_artifact.py --check-manifest` ("stale Pages artifact manifest:
  source_commit_at_generation") for every content PR since commit-bound
  provenance landed. The last green PR validate runs predate the pattern
  (2026-05-29). Fixed by pinning the checkout to
  `github.event.pull_request.head.sha`.
- **DOC-004 advance (2026-09-07):** recorded R73 (Codomyrmex
  `untagged-ce7d…` v1.3.0) and R74 (GNN v3.2.0) as `superseded` /
  `bibliography-folder version-history-only` in
  `data/paired-publication-decisions.json`, verified against the regenerated
  `reports/paired_publications_2026-09-07.json` (full-scope queue 5 → 4
  unreviewed actions; an intermediate docxology-only rescan showed 2 but used
  a narrower owner scope than the 2026-09-04 baseline — see DOC-004). The
  cluster was fully resolved later the same day — see the DOC-004 closure.
- **MINOR (observed, then fixed in the 2026-09-07 PR):** pairing candidates
  whose GitHub release is a *draft* carry rotating `untagged-*` URLs, so
  per-fingerprint decisions (R71/R73/R75) cannot permanently clear them — each
  scan requeued the release under a new fingerprint. Fixed the same day: draft
  releases are skipped from pairing entirely (see the DOC-004 closure below).
- **DOC-004 CLOSED (2026-09-07 principal session):** the principal classified
  `docxology/cognitive_integrity` as curated (added to `pages/SOFTWARE.md`),
  confirmed superseded dispositions for the rotating Codomyrmex drafts
  (R75/R76) and the ActiveInferAnts/CEREBRUM version-specific artifacts
  (R77/R78), and directed that draft (`untagged-*`) releases be skipped from
  pairing entirely. The refreshed full-scope report has **zero unreviewed
  candidates** (447 pairs; 450 → 447 reflects the three skipped draft pairs),
  meeting DOC-004's acceptance; the row is removed per the
  completed-rows-deleted convention (evidence: this entry + CHANGELOG).
- **MEDIUM (fixed in the 2026-09-07 PR):** draft releases are now skipped at
  pairing time (`is_draft_release` in `code/src/publication_pairing.py`);
  provenance binding is merge-aware (`latest_payload_commit` steps through a
  merge commit whose tree matches a parent, resolving the branch payload on
  PR-shaped merge refs) with regression tests; the merge-ref test was
  mutation-verified to fail under the old walk.
- **MAJOR: none found.** All 48-gate-equivalent checks visible from a clean
  checkout pass; the two environment-bound items (browser QA under
  `browser-qa` extra, signed-in Search Console follow-up) remain tracked by
  DOC-008 and DOC-010.

## Session findings (2026-09-10)

Intake/republication pass findings. All five decision items were resolved on
2026-09-11 (dispositions recorded in-line and in the cited ledgers); the
remaining entries are records of mechanized or resolved state:

- **EvoJump `needs_review` cluster (12 pairs): RESOLVED (2026-09-11).** The
  12 `needs_review` actions in the 2026-09-10 pairing report were the
  cross-product of two Zenodo concepts — 10.5281/zenodo.22664645 (auto-archive
  upload, zip only) and 10.5281/zenodo.22664675 (source archive + paper PDF
  `evojump_paper.pdf`) — against six `docxology/EvoJump` releases. Decisions
  recorded in `data/paired-publication-decisions.json`: R80 accepts the six
  22664675 pairs as software-catalog (canonical curated deposit — the README
  citation links it and it carries the only github_release_mentions_doi
  cross-link; the citable paper remains bibliography row #12, concept
  10.5281/zenodo.17229924; no new bibliography row, R02 precedent), and R81
  supersedes the six 22664645 pairs as the GitHub-Zenodo automated integration
  archive. The next pairing report should show zero `needs_review`.
- **CCD title divergence (curation call, not applied): RESOLVED (2026-09-11).**
  Bibliography row #112 adopted the Zenodo v2.4.0 self-title "Cognitive
  Diagrams: Reviewing Categorical Accounts of Linguistic Case" (concept DOI
  10.5281/zenodo.19695259 unchanged); this also clears the
  `fetch_work_authors.py` title_mismatch flag.
- **On Time version-DOI exception: RESOLVED (2026-09-11).** Record 15168382
  (row #17, commit `d086e7a3`) is registered in
  `VERSION_SPECIFIC_CITATION_EXCEPTIONS` (`code/orchestrators/check_zenodo_uncatalogued.py`)
  with full identity (title, concept 10.5281/zenodo.15168381, version DOI
  10.5281/zenodo.15168382); the next report's `non_canonical_doi` count drops
  to zero.
- **Uncatalogued Zenodo supplement: RESOLVED (2026-09-11).** Record 22666981
  (software-only supplement to the CCD paper; the paper row cites concept
  10.5281/zenodo.19695259) is registered in `KNOWN_STALE_RECORD_IDS` by bare
  record id — the matcher compares record ids, so the concept id in the
  original note would never have matched.
- **Fork registered:** `docxology/oh-my-pi` was registered under the standing
  fork policy (DOC-005 mechanized path), matching the RGMs precedent.
- **Pages artifact budget review (DOC-009/DOC-012; threshold 850 → 880 MiB):**
  the 2026-09-10 intake evidence plus the 2026-09-11 UTC-rollover
  double-generation grew the bounded Pages projection to 870.5 MiB,
  tripping CI's artifact-budget gate. Composition at review: paper PDFs
  681 MiB, published dated reports ≈ 60 MiB, extracted paper images 950
  MiB (omitted by policy). The review threshold moved to 880 MiB
  (documented in CHANGELOG 2026-09-10). RESOLVED (2026-09-11): the omission
  class landed — `build_pages_artifact.py` now omits superseded dated reports
  from the Pages projection (top-level receipts strictly older than their
  family's newest, plus whole dated visual-qa/browser-smoke/browser-qa sets),
  with cited-by protection so a report referenced from a published surface
  stays published; reports remain in the repository per the DOC-012 retention
  tiers (projection-only omission needs no retention entry), and the shared
  `code/src/report_references.py` scan keeps the pruner's safety net in
  lockstep. Measured: 390 files / 70.9 MiB newly out of the artifact,
  projecting ≈793.3 MiB with ≈87 MiB of headroom under the unchanged
  880 MiB band (see `docs/operations/asset-strategy-adr.md`, "Execution
  (2026-09-11)").

## Session findings (2026-09-12)

Pipeline-streamlining and docs-accuracy pass (PRs #27/#28 and follow-ups):

- **Unified settle driver landed (PR #27):** `code/orchestrators/settle.py` +
  `code/src/change_classifier.py` classify dirty paths into surfaces
  (reports/site/code/tests/ci/docs/other) and run the tiered battery — fast
  (sitemap `--check`, artifact budget, ruff), full (+ pytest + standard
  `validate_repo.py`, CI-equivalent), release (+ `--release --strict-reports`
  with the conventional deployment attestation) — then land the payload +
  control-tail commit split (`release_controls.is_control_path` is the single
  control predicate) with optional push/PR. Runbook:
  `docs/operations/settle.md`, signposted from `AGENT_START.md`.
- **Gate-latency fixes (PR #27; PERF-001 acceptance met):** build-stamp
  memoization (video-pages check 55s → 5.7s) and the sitemap batch walk
  cached end-to-end (sitemap `--check` 0.8s vs 19s per-path; the 2026-09-06
  attempt's timeout-swallow trap is closed — the failure path now caches the
  fallback explicitly).
- **Binder-ordering recipe (PR #28):** `docs/operations/settle.md` Notes
  carries the land-then-confirm cycle: render binders only after the payload
  commit (the Pages manifest binds `source_commit_at_generation` to the last
  payload-content commit) and only after dated receipts are tracked
  (`build_agent_index.py` resolves receipt paths among tracked files);
  dependency order is `build_pages_artifact --write-manifest
  --allow-dirty-prepayload-evidence` (fails closed on dirty post-deploy
  Pages inputs without a valid prepayload snapshot) → generated manifest →
  agent-index → release integrity → final generated manifest, with
  `build_public_source_review.py` a deliberate manual last render; commit
  payload churn from the consumer renders (`sync_site_facts`,
  `build_catalog`, `build_search_index`) before the final manifest render;
  commit the live-site receipt together with its binder rebind (a
  receipt-only push turned main validate red once, fixed by rebind
  `c7de4a4a`).
- **DOC-013:** the root docs alignment was reviewed in the 2026-09-12
  docs-accuracy wave; findings landed with the settle-driver pointers.
