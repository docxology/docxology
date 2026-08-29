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
`.github/workflows/pages.yml`. The artifact builder warns at 850 MiB and fails
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
   decision-pinned by `code/tests/test_build_image_sitemap.py`).

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
`code/tests/test_build_image_sitemap.py`) until Option A lands.

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
   850 MiB in a release check (`build_pages_artifact.py --check-size`), i.e.
   the review-warning band is reached again.
2. **Flickr dependency trigger:** Flickr changes its hotlinking behavior or
   terms of service such that `live.staticflickr.com` thumbnails become
   unreliable, rate-limited, or disallowed for this use.
3. **Strategic trigger:** the art gallery becomes a strategically primary
   surface of the site (indexing, discovery, or editorial priority), at which
   point self-hosted images plus a same-origin image sitemap become the
   correct asset model.

When Option A is executed, self-host every `artworks.json` thumbnail on an
origin this site owns, then (and only then) reintroduce an image sitemap whose
every `<image:loc>` is same-origin — the pinned tests in
`code/tests/test_build_image_sitemap.py` encode exactly this reversal
condition and will fail until the precondition holds.


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
