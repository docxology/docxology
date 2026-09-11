# ADR: Asset strategy for the Pages artifact and art gallery imagery

- **Status:** Accepted (Option C, executed 2026-08-29) / Proposed (Option A, deferred)
- **Date:** 2026-08-29
- **Deciders:** site-upgrade fleet (adr lane), with decision-pinned tests in
  `code/tests/`
- **Related:** [`docs/operations/github-pages-artifact.md`](github-pages-artifact.md),
  [`docs/operations/report-retention.md`](report-retention.md),
  `data/report-retention.json`

## Context

The canonical repository includes paper PDFs, extracted paper figures, and
dated visual-QA screenshot binaries for provenance, while the published site is
the bounded Pages artifact assembled by
`code/orchestrators/build_pages_artifact.py` and deployed from
`.github/workflows/pages.yml`. The artifact builder warns at 880 MiB (raised
from 850 MiB by the 2026-09-11 budget review below) and fails
at the 900 MiB release hard ceiling; GitHub's platform limit is 1 GiB. After
the earlier prune of duplicate paper binaries, the artifact stood at
**826 MiB** — about 24 MiB below the 900 MiB ceiling and just inside the
850 MiB review-warning band, leaving almost no headroom for ordinary content
growth (new papers, new QA sets, new artwork).

Three asset classes drove the pressure and each has a different ownership
model:

1. **Paper images** — 8944 extracted figure images under `papers/**/images/`,
   already omitted from the artifact and served by raw GitHub URLs; versioned
   in Git, not deployable payload.
2. **QA screenshots** — dated visual-QA and browser-smoke screenshot binaries,
   omitted from the artifact but still consuming checkout and artifact-audit
   budget across superseded date-stamped sets.
3. **Art gallery thumbnails** — 942 artwork thumbnails hotlinked from
   `live.staticflickr.com`. Flickr remains the durable origin for the art
   collection, but hotlinking is a third-party dependency: Flickr controls
   availability and terms, and a cross-domain image sitemap built from those
   URLs is inert for indexing (Google does not index image-sitemap URLs on a
   domain the site does not own — see the removed `sitemap-images.xml`,
   decision-pinned by `code/tests/test_regenerate_all.py`).

## Decision

**Option C — prune superseded QA screenshot sets — is Accepted and was
executed on 2026-08-29, freeing 111.5 MB across 4 dated sets** (two
`reports/visual-qa/` sets and two `reports/browser-smoke/` sets). Every
removed path carries a reviewed provenance record in
`data/report-retention.json` with generation time, SHA-256 provenance hash,
durable `git:<commit>` replacement location, and reviewer identity, per the
retention policy. Removal is from the checkout only; no Git history is
rewritten. Screenshot binaries remain retrievable from the recorded commits
and GitHub raw/tree URLs.

**Option A — self-hosting art gallery thumbnails on an origin we control — is
Proposed but deferred.** Deferral is deliberate: 942 thumbnails must be
acquired, normalized, and committed, which would consume artifact headroom and
review capacity now, while the Flickr hotlinking dependency is currently
stable. Self-hosting is the only path that would make an image sitemap
meaningful, so the image sitemap stays removed (pinned by
`code/tests/test_regenerate_all.py`, which asserts the generator is absent from
the generation plan) until Option A lands.

The prune also fixed the reference scanner in
`code/orchestrators/prune_old_reports.py` to skip `_site/` and
`data/report-retention.json` when detecting tracked references, so generated
projections and the retention manifest itself no longer block pruning of
genuinely superseded sets (see the report-retention appendix).

## Consequences

- The artifact drops by 111.5 MB from 826 MiB, restoring real headroom below
  the 850 MiB review band and the 900 MiB hard ceiling.
- Superseded QA evidence remains auditable: manifests with per-file SHA-256
  digests stay in the Pages projection and the working tree; binaries resolve
  to the recorded Git commits.
- Art gallery images remain third-party hosted. This is an accepted
  availability and terms risk, tracked by the triggers below, and it keeps the
  image sitemap unshipped.
- Contributors must add a reviewed retention entry before any further prune;
  the pruner enforces this mechanically.
- The Pages artifact's omission policy for paper images and visual-QA binaries
  is unchanged; this ADR records the budget rationale behind it.

## Triggers for revisiting Option A (self-hosted art thumbnails)

Revisit Option A when **any** of the following becomes true:

1. **Artifact size trigger:** the Pages artifact is projected at more than
   880 MiB in a release check (`build_pages_artifact.py --check-size`), i.e.
   the review-warning band is reached again (the band moved 850 → 880 MiB in
   the 2026-09-11 budget review below).
2. **Flickr dependency trigger:** Flickr changes its hotlinking behavior or
   terms of service such that `live.staticflickr.com` thumbnails become
   unreliable, rate-limited, or disallowed for this use.
3. **Strategic trigger:** the art gallery becomes a strategically primary
   surface of the site (indexing, discovery, or editorial priority), at which
   point self-hosted images plus a same-origin image sitemap become the
   correct asset model.

When Option A is executed, self-host every `artworks.json` thumbnail on an
origin this site owns, then (and only then) reintroduce an image sitemap whose
every `<image:loc>` is same-origin — the live pin in
`code/tests/test_regenerate_all.py:20-21` (`build_image_sitemap.py` removed
from the generation chain) encodes exactly this reversal condition and will
fail until the precondition holds.


## Correction (2026-08-29, handoff #3 section 3)

The original ADR overstated what the prune achieved. Measured growth reports:

| Report | Artifact | Files | Omitted QA screenshots |
|---|---|---|---|
| 2026-08-28 07:29 | 814.64 MiB | 4,654 | 78 / 169,341,772 B |
| 2026-08-28 23:37 | 825.23 MiB | 4,690 | 78 / 169,341,772 B |
| 2026-08-29 01:31 | 821.66 MiB | 4,670 | 78 / 169,341,772 B |

The pruned QA screenshot sets were **already excluded** from the Pages artifact
(the artifact builder omits visual-QA screenshots by policy). The prune bought
**repository clone weight only (111.5 MB)**, not artifact budget. The artifact
actually grew ~7 MiB across the round; headroom to the 850 MiB warning line is
~28 MiB, and `omitted_paper_image_count` rose to 8,944 — the exclusion set is
absorbing growth to hold the line.

Consequences: Option A (separate assets origin) is **more urgent than originally
assessed**. The triggers below are modified accordingly — treat trigger (a) as an
active planning item now, not a distant condition. Any image-heavy addition
(per-work OG cards, self-hosted art thumbnails) must wait for the assets-origin
decision. CI should fail when artifact MiB crosses the warning line rather than
discovering it at the ceiling (assigned to the ci-tests lane).

## Budget review (2026-09-11): review-warning band 850 → 880 MiB

The 2026-09-10 publications intake (Skillarum #216 with its versioned PDF,
plus the Cognitive Case Diagrams v2.4.0 versioned PDF — ~19 MiB of permanent
paper-PDF growth) and the 2026-09-11 UTC-rollover double-generation of the
dated evidence families pushed the projected artifact from 844.9 MiB (2026-09-07
baseline) to 870.5 MiB, past the 850 MiB review-warning band. Composition at
review: paper PDFs 681 MiB (78%), extracted paper images 950 MiB (omitted from
the projection by policy), published dated reports ≈ 60 MiB, everything else
small.

Decision: the review-warning band moves to **880 MiB** — 20 MiB of review
headroom below the unchanged 900 MiB release hard ceiling
(`code/src/artifact_budget.py` `BUDGET_MIB`, `build_pages_artifact.py`
`WARNING_ARTIFACT_BYTES` and the manifest `warning_policy` string, the
validate.yml step name, and the size trigger above updated together). The
durable lever — omitting superseded dated reports from the Pages projection
while they remain in the repository (per the DOC-012 retention tiers, with
GitHub tree/raw fallbacks) — is flagged for the principal in TODO.md; without
it, the next intake's ~20 MiB of paper PDFs reaches the hard ceiling.

## Execution (2026-09-11): superseded-report omission class landed

The durable lever from the budget review above landed as the third omission
class in `build_pages_artifact.py` (shared cited-by semantics with
`prune_old_reports` via the new `code/src/report_references.py` scan): any
tracked `reports/` path strictly older than the newest date of its family —
top-level `reports/<family>_<YYYY-MM-DD>` receipts and whole dated
`reports/visual-qa/`, `reports/browser-smoke/`, `reports/browser-qa/` sets —
is omitted from the Pages projection while remaining committed in the
repository. Reports cited from a published page or data file are never
omitted, and a post-assemble 404 guard fails the build if any referenced
repository path was not copied.

Measured against the 2026-09-11 growth receipt (864.17 MiB, 5,184 files): the
omission class newly removes **390 files / 70.9 MiB** that were previously in
the artifact (74.4 MB of non-binary superseded receipts and manifests; the
visual-QA/browser-smoke binaries under the superseded dated sets were already
omitted by the binary class and are not double-counted), projecting the
artifact at **≈793.3 MiB** — about **87 MiB** of review headroom below the
unchanged 880 MiB warning band. Trigger (a) above therefore returns to
dormant: the next evidence wave adds only each family's newest receipt, and
yesterday's drops out automatically, so ordinary dated-evidence growth no
longer moves the artifact toward the ceiling. Option A (self-hosted art
thumbnails) remains deferred under the same triggers; the band stays at
880 MiB with the 900 MiB hard ceiling untouched.
