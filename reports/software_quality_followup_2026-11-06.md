# Deterministic regeneration and clean-source verification — 2026-11-06

This follows the [November 5 software-quality review](software_quality_followup_2026-11-05.md).
That review's C82 render and earlier dirty-source core test identities remain
historical observations. The current production checkpoint is
`cdca4d9056033532c2cefda2167034008d736e53`.

## Reproducibility-page repair

Comparing two complete canonical generation passes exposed one payload difference:
`reproducibility.html` changed only its generated footer timestamp. All 53 steps
returned zero in each pass; their success alone did not establish byte stability.
The strict comparison retained this failure instead of ignoring timestamp changes.

The source owner, `build_reproducibility_ledger.outputs()`, now uses the existing
shared `reuse_on_disk_stamp` policy during apply as well as check mode. Unchanged
substantive HTML preserves its complete earlier footer; changed visible ledger
content receives a new footer and JSON timestamp. Explicit output paths and
public command interfaces are unchanged.

Disposable persisted-output regressions produced one intended failure and one
passing changed-content control before the repair. The final focused ledger and
build-stamp gate passed all 36 cases and exact-path Ruff. The first broader
focused attempt exposed a fixture cache-isolation error, which was corrected
without changing stamp policy; that failed observation is retained separately.
The final fixture restores its process-cache monkeypatch on teardown.

## Fresh clean-commit gates

Both following runs actually executed at clean
`cdca4d9056033532c2cefda2167034008d736e53`; neither is an earlier run relabeled
as a later commit:

| Gate | Actual result |
| --- | --- |
| Core site suite, excluding explicit browser/native groups | 2,598 passed and 13 subtests passed; six retained dependency warnings; 56.00 seconds. |
| Manuscript rendering and validation, including native four-format build | 128 passed; six retained dependency warnings; 10.10 seconds. |

The qualified runs finished without timeout or remaining owned descendants and
reported unchanged source. The native build created fresh PDF, HTML, EPUB and
PowerPoint outputs, with all 139 production Python members independently bound
to committed Git bytes and current working files. It binds 17 direct manuscript
inputs and 13 generated artifacts. No historical review files were reused.

| Evidence | SHA-256 |
| --- | --- |
| Canonical render receipt | `edd567c53ec386adc9ce04d2c60a2f8213a5c84e55937ebe49fb33f3a056c60c` |
| Production file/hash inventory | `24042be6c751d4f3816cac6837fb9fc85b5d4da0276a5a7fb44c635bababfa8f` |
| Production Git archive at the clean checkpoint | `97f2c1016fbe40a8b6fedd554d245c34b8c3938378318a1d6551f58e6835c596` |

Automated source/projection checks retained 34,752 non-table body characters,
151 link occurrences, 42 table rows, 31 logical list items and four registered
figures. Actual LibreOffice conversion produced 148 slide pages. All 119 body
placeholders had zero reported outside-body text or body/title overlap; the
bounded substantial-word-overlap detector reported zero. The PDF has 16 pages,
and the EPUB has 13 valid XHTML documents.

These are source, software and automated format observations. Human editorial,
visual, scientific and EPUB-reader-specific review remain separate and pending.
Later documentation/control commits can reuse this production evidence only
with unchanged production membership/bytes, direct inputs and pinned template
identity; they are not new renders of those later commits. Final generated-output
convergence and deployed-byte acceptance are separate checks.
