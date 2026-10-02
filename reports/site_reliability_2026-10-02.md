# Site and repository reliability review — 2026-10-02

This implementation follows the authorized repository and website improvement
pass. The baseline is public main commit
`1badb9884253e4a1109e64b8fa27269c88685758`. The commit that publishes this report,
its bounded control tail, and the Actions deployment receipt identify the final
candidate; a source report cannot predict its own future Git SHA.

## Acceptance criteria and failure boundaries

- Preserve all 219 existing work keys and reserve retired keys independently of
  editable titles and years. Reject duplicate, unsafe, missing, retired, or
  orphaned identities. Validate intake before source mutation and preserve
  concurrent edits when a failed update needs rollback.
- Reclaim Pages headroom through a narrow projection policy while retaining all
  paper PDFs and manuscript files. Legacy QA captures remain in Git custody with
  manifest fallbacks; nested, invalid-date, and non-image report paths stay hosted.
- Share progressive search loading, retain full search text for every record
  family, and recover from mixed deployment revisions without silently reporting
  a successful empty result.
- Make mobile navigation usable at 320px without JavaScript, contain and restore
  modal focus, and report actual clipboard outcomes with a usable link fallback.
- Keep the offline shell small and runtime cache bounded. Protect good cached
  responses from HTTP errors, storage failures, update churn, and stalled or
  oversized network bodies. Exercise these boundaries in real Chromium.
- Fail required hosted browser/Lighthouse checks when tools, complete reports,
  or qualifying category scores are unavailable. Preserve diagnostics as Actions
  artifacts instead of treating missing execution as a pass.
- Bind deployed manifest bytes to the committed candidate, check every work page
  and critical shared asset by SHA-256, check every archived PDF's HEAD contract,
  and check three deterministic PDF samples by SHA-256. Preserve the receipt
  outside the source tree with bounded retries and complete-response deadlines.
- Invalidate cached generation when an owning script, shared source library,
  or declared imported orchestrator changes. Missing source inputs require a
  rebuild; always-run steps retain their explicit fixed-point behavior.
- Regenerate source-dependent outputs in the declared order, confirm byte
  stability, run the repository suite and validation, and obtain fresh independent
  review of shared infrastructure changes before publication.

## Reviewed source changes

[Bibliography metadata decisions](bibliography_metadata_review_2026-10-02.json)
bind three full titles to archived title pages and the Active Blockference
publication year to Crossref. Existing citation keys remain unchanged, including
the historically named 2022 key for the chapter published in 2023. The Discovery
Engine abstract is corrected against its archived source instead of perpetuating
an unsupported free-energy synopsis. Human-facing search summaries and abstract
search text also use the reviewed inert-prose normalization; raw enrichment and
archived source bytes remain intact, including literal mathematical notation.

[Repository catalog decisions](repository_catalog_review_2026-10-02.json) record
five canonical URL migrations with matching immutable GitHub repository IDs and
the pinned README source for OmniLatticeTextbook. The catalog description preserves
the project's no-DOI status and does not adopt unsupported scientific-validation
claims from repository prose.

The canonical Scholar profile was observed directly in an authenticated browser
on 2026-10-02: 823 citations, h-index 14, and i10-index 17; the corresponding
since-2021 values are 594, 14, and 15. The snapshot and receipt bind the exact
snapshot bytes and observation method. Independent review verified the binding
against a sanitized observation excerpt; that reviewer did not independently
operate the browser. Public artifacts exclude account identity and screenshots.

## Verification and provenance

Local acceptance on 2026-10-02:

| Check | Observed result |
| --- | --- |
| Initial forced ordered regeneration | Two passes; 100 local surfaces run, none skipped |
| Final source follow-up regeneration | Two ordered passes; 69 surfaces run, 31 skipped with unchanged complete inputs |
| `DOCXOLOGY_REQUIRE_BROWSER_QA=1 uv run python3 -m pytest code/tests -q` | 1,204 passed; zero failures, errors, or skips; 346.471 seconds |
| `uv run python3 code/orchestrators/validate_repo.py` | Repository validation completed |
| `uv run --group lint ruff check code` | Passed |
| Workflow lint and `git diff --check` | Passed |
| Static accessibility | 2,535 of 2,535 checked pages passed |
| Artifact budget | 834.35 MiB against the 890 MiB gate; Pages projection 835.5 MiB |
| Fresh external links | 853 observed: 699 OK, 146 rate-limited/bot-protected, one connection failure, three timeouts, four transient responses, zero HTTP 404s |
| Independent cache review | 139 focused cases passed; no missing imported helpers across 31 cached stages |
| Independent shared writer review | 70 focused cases passed; full-page stamp reuse and descriptor-safe, complete-map reads verified |

The full test run included real Chromium lifecycle, progressive search,
mobile/no-JavaScript navigation, focus, clipboard, first-paint geometry, and
all eight real Lighthouse 13.4.1 reports. Thirty-two runtime/source hashes
remained unchanged during the run. An earlier local Lighthouse process failed
with a Puppeteer connection closure on Videos; its unchanged retry succeeded.
That failure remains recorded separately; the final full run above passed
cleanly without retries or runtime errors. All eight pages passed their existing
floors with one Lighthouse run each:

| Page | Performance | Accessibility | SEO | CLS |
| --- | ---: | ---: | ---: | ---: |
| Homepage | 75 | 100 | 100 | 0 |
| Publications | 69 | 100 | 100 | 0.001407 |
| Art | 74 | 100 | 100 | 0 |
| Videos | 88 | 93 | 100 | 0.021526 |
| Search | 72 | 100 | 100 | 0.110704 |
| 404 | 99 | 100 | 100 | 0 |
| Representative work | 97 | 100 | 100 | 0 |
| Representative video detail | 95 | 100 | 100 | 0 |

These scores do not establish the aspirational 85/95/95 targets on every
page. Search's remaining initialization shift comes from wrapped type filters
appearing after the core index loads; the footer shift was repaired. This
measured follow-up remains under DOC-009.

An extra ordered pass and clean post-landing validation are final publication
gates. Hosted jobs and live acceptance belong to their candidate-SHA Actions
receipts; local tests alone do not establish successful deployment. The fresh
external-link capture records its dirty worktree honestly and is an outbound
observation, rather than clean candidate release evidence.

A pre-publication hosted run caught an ambiguous clipboard-test selector after
asynchronous search results added more headings. The regression tests now scope
clicks and completion assertions to the intended Research heading while keeping
the real search rendering, pending clipboard promise, query-preservation, and
unavailable/denied clipboard checks. The failed run is retained in Actions;
the replacement candidate must pass the complete hosted gate before publication.

Independent source review checked the title pages, Crossref publication year,
GitHub repository identities, pinned README hash, public-text privacy, all active
work keys, retired reservations, and Scholar snapshot binding. Independent code
review exercised shared search, service-worker, intake, and deployment-verifier
failure cases; its findings were repaired before landing.

Footer stamps record rendering provenance and retain their date only when the
complete page is unchanged except for the stamp. Shared writers and checks now
use the same rule, validate the complete output mapping before reads, and finish
all descriptor-safe reuse reads before writes. They do not prove that a future
publication commit contains the rendering. Exact deployment SHA and live bytes
are separately bound in the retained technical acceptance receipt. That receipt
does not claim all artifact files were downloaded, human visual review occurred,
or the complete release attestation passed.

## Remaining source and access work

The [active backlog](../TODO.md) retains recurring maintenance and concrete
external dependencies. Licensed full text remains unavailable for ToComment,
Paleolithic Rockstars, and Focused Attention Meditation. Digital Twins and
Aligning AIO to SUMO author discrepancies require depositor reconciliation;
registered creators are preserved. Contradictions inside originating manuscripts
require source publication changes before archived summaries can adopt them.

The available signed-in browser could not access the site's Search Console
property. Owner-granted property access is required for sitemap and indexing
follow-up; no DNS, ownership, or account settings were changed. Flickr-side
enrichment remains an account editing task. A managed-profile deep security
scan is a separate evidence requirement and is never inferred from ordinary
tests or independent code review.
