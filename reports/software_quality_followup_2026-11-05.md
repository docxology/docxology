# Software quality follow-up — November 5, 2026

This follow-up addresses reproducible software defects in the profile and three
publication-linked projects. Commands completed on November 6 UTC / November 5
Pacific. It supplements the [publication source review](publication_source_corrections_2026-11-05.json);
it does not replace historical observations or reconstruct missing experiments.

## Reviewed source and behavior

| Repository and reviewed commit | Correction | Verification |
| --- | --- | --- |
| [docxology](https://github.com/docxology/docxology/commit/c82dd2dd0d8ef59ab7149b072b03f418d93b3234) | Explicit manuscript renders bind every production Python source and reject changed bytes or membership; safe reads enforce an optional byte limit before decoding. | 2,596 core tests and 13 subtests passed; independent source review; 128 manuscript rendering/validation tests passed, including a fresh four-format native build. |
| [Blake](https://github.com/docxology/blake/commit/9b4d5d88b02f5cfdc8fddaaf4bed3bed4872702f) | Preserve occupied release destinations, bind the canonical rights matrix and selected analytical epoch, reject source/data overlap, and keep unreviewed secondary-source leads pending. | 97 release/corpus regression tests passed, including real destination sentinels, conflicting analytical epochs, source identity and pending-evidence cases. |
| [Markdown Decision Process](https://github.com/docxology/markdown_decision_process/commit/df81d4ac83dd13f289d9e4767500e3d2a1c033ed) | Share fence-aware heading membership across extraction and transformations; preserve skipped heading levels; replace unsupported MarkChain API examples with executable current examples. | Locked Python 3.11 suite: 307 passed, five existing unfinished performance cases skipped; ten console compatibility tests and fatal lint/type/new-file format gates passed. |
| [ActiveACO](https://github.com/docxology/ActiveACO/commit/80b4e4016a6cc0061c432827997da6e2e3bf05dd) | Restore caller Python and NumPy random state on comparison success or failure. | 76 tests passed; the 7,942-byte seeded regression payload retained SHA-256 `5a29c9921f7f43d77cf6c44227d413c250e94f3aaef4467c318648fe8c94c1d7`; historical result/receipt bytes were unchanged. |

The exact MDP main commit also passed [all seven hosted test/security jobs](https://github.com/docxology/markdown_decision_process/actions/runs/42138992191) and its [documentation build](https://github.com/docxology/markdown_decision_process/actions/runs/42138992203); the optional documentation deployment remained skipped.

The 2,596-test core gate ran on the dirty `f62460d503c63c260afa0e0fee95faf4824d403a` checkout; its six declared input hashes match the later clean `c82dd2dd0d8ef59ab7149b072b03f418d93b3234` checkpoint. The separate 128-test native gate actually ran at clean `c82dd2dd0d8ef59ab7149b072b03f418d93b3234`. These run identities are retained separately.

Focused failing tests preceded the repairs. Profile review additionally exposed
and corrected incomplete-directory enumeration and a recursive-scope mismatch.
Incremental enumeration counts entries before buffering them, rejects unavailable
classification and links, and includes `.py` files regardless of directory name.
Binary bytecode does not enter the Python-source hash map. No shared cross-project
runtime dependency or new inference algorithm was introduced.

## Canonical manuscript source custody

The [render guide](../docs/manuscript/README.md) documents the additive
`production_source` field. A fresh build at clean commit
`c82dd2dd0d8ef59ab7149b072b03f418d93b3234` recorded all **139** committed
production Python files. The canonical map independently matched Git tree
membership, archived committed bytes and current working files before/after
rendering. The inventory digest is independent of archive commit metadata.

| Evidence | SHA-256 |
| --- | --- |
| Canonical render receipt | `3dda11333d1d5fdf025a8e040ba82671e5732ce922e514166066083948993152` |
| Production file/hash inventory | `e4199299aaafea56b13b39452aa98c61d78b79d75f86c1a318d28086ae7baa75` |
| Production Git archive at the rendered commit | `4227fa308d7d30d46c589b82dde30e439f06c7f5c2dd2d813f59ce805fefb654` |

The native run created new PDF, HTML, EPUB and PowerPoint review files. Semantic
checks retained 34,752 non-table body characters, 151 link occurrences, 42 table
rows, 31 logical list items and four registered figures. Actual LibreOffice
conversion produced 148 slide pages; all 119 body-placeholder pages had zero
reported body-bound overflow or body/title overlaps, and the bounded word check
reported zero substantial overlaps. The PDF has 16 pages; the EPUB has 13 valid
XHTML documents. These automated format checks are distinct from human review.

The receipt is a working-source content snapshot. It does not assert that an
arbitrary dirty working tree equals HEAD or trace every runtime import. The
native verification above used an independently checked clean commit and pinned
tool/template inputs. Later documentation/control commits must retain identical
production bytes to reuse that source evidence; an archive hash from a later
commit is not substituted for this frozen archive hash.

## Evidence and capacity limits

No new empirical result, manuscript deposit, DOI, release version, human editorial
approval, or search-engine indexing acceptance is asserted. Blake's historical
156/162 discrepancy and ActiveACO's original Table 1 membership remain unresolved.
Contextual archive identity is not an independent text transcription; candidate
source leads do not acquire reviewer approval through packaging. MarkChain's
unused order/smoothing/temperature parameters are documented as implementation
limits. ActiveACO's random-state restoration is for serial use; concurrent global
random consumers require process isolation.

Human editorial/visual review and EPUB-reader-specific review remain pending.
[TODO.md](../TODO.md) retains the unfinished work. The
[Pages policy](../docs/operations/github-pages-artifact.md) still preserves
repository originals and uses reviewed exact versioned Zenodo files for large
new/current PDF editions. Existing public PDF routes and same-directory scholarly
reservations remain intact. No repository split, original deletion, migration,
or budget increase was performed. The existing 890 MiB growth target remains a
review target, not an achieved claim. The [November 5 baseline](https://github.com/docxology/docxology/blob/c82dd2dd0d8ef59ab7149b072b03f418d93b3234/reports/pages_artifact_growth_2026-11-05.json)
is an immutable source snapshot; the current [Pages artifact manifest](../data/pages-artifact-manifest.json)
supplies projection counts and bytes.
