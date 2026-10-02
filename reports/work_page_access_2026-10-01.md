# Work-page access and reliability review — 2026-10-01

This pass improves the shared public work and paper-folder pages without changing
permanent citation keys or publication identities. The starting public revision
was `4d2f388ec797f08a5d5134f5b6c605c4a666328a`.

## Access and source boundaries

The catalog contains 219 work pages and 202 documentation folders. Of those,
194 folders contain 222 archived PDFs; 16 folders contain multiple PDFs.
The work pages provide a direct download and a GitHub paper-folder link near
the title wherever the corresponding public source exists. Additional documents
retain their filenames and sizes. Associated software repositories are separately
labeled.

Selection follows an explicit `primary_pdf`, then the named extracted-text
source, then a sole archived PDF. Filename ordering, file size, and modification
time do not establish a latest edition. Ambiguous files are listed without a
primary designation. A declared missing primary fails generation. Extracted text
that names a different primary document remains separately labeled and is not
represented as an encoding of that primary PDF.

The shared resolver admits Git-visible regular files, excludes ignored local
artifacts, rejects escaping paths, symlinks and hardlinks, and encodes URL path
segments. Repository and deployment manifests remain the publication boundary.
Paper-folder pages retain `noindex, follow` and their canonical work URL.

## Content and citations

Work pages render the entire stored curated abstract rather than a shortened
README excerpt. Managed READMEs also preserve the stored abstract. Empty or
unavailable abstracts do not become machine-readable scientific abstracts;
generated folder-topic tokens do not become keywords. Per-field source records
separate concepts from findings and point readers to summary evidence.
The meditation chapter retains an explicitly labeled abridged publisher synopsis.
This pass does not supply missing licensed full text or resolve the originating
publications' outstanding judgment calls in `TODO.md` (DOC-016).

The ten rows without recorded authors omit author fields consistently from
visible citations, JSON-LD, BibTeX, CSL and RIS. Verified names and collective
credits retain their order. Copy BibTeX uses a safe JSON string and copies the
canonical entry exactly, including ampersands, quotes and angle brackets.
Embedded work and breadcrumb JSON escape script terminators without changing
the parsed data.

## Maintenance

Repeated work and folder styles now live in the shared stylesheet. Source
actions use accessible groups rather than inheriting the fixed site navigation.
Generator input declarations include the actual metadata, artifacts and shared
code. The active backlog retains its fifteen unfinished items; public completed
history is archived separately and obsolete private-checkout rules are corrected.

The landing driver commits only selected paths, preserves other staged work,
handles deletion and rename sources, and refuses concurrent payload changes or
HEAD movement. It replays the existing public-source review with its recorded
inputs, guards input/output custody, and bounds control convergence to four
passes. A fresh landed-tree check precedes push. Local regeneration defaults to
two ordered passes for known cross-pass dependencies; validation remains the
final authority.

## Verification

Fresh independent reviews cover the source resolver, citation payloads, content
provenance, dependency declarations and publication-driver changes. Focused
regressions use disposable Git repositories and source sentinels.

Real Chromium acceptance passed for the Fourfold Vision work and folder pages:
the downloaded PDF matches the local source bytes, clipboard text matches the
canonical BibTeX entry, both pages fit at 320px and 768px and with enlarged text,
and axe reports no serious or critical violations. The test retains the site's
CSP and serves its audit library from the same origin. It is included in hosted
browser QA.

All 219 generated work pages passed the catalog access invariants. Local
regeneration completed 100 generator-step executions across two ordered passes.
Repository validation passed; 2,535 pages passed static accessibility checks,
and the Pages artifact stayed within its review budget at that validation.
The full test suite and post-commit validation are required by the landing driver;
the separate hosted browser job exercises the rendered-page acceptance test.
Published commit IDs and workflow results remain directly inspectable in the
public repository history and its Actions runs.
