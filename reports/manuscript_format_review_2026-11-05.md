# Manuscript format review — 2026-11-05

Reviewed source: `476fbb85ae30edf499b0742253228c8f5e047b7e`, including parent `c780cc6ca7485f95db6e08f1229ba48c71a013f8`. This is an intermediate source- and artifact-bound format review. A later integrated manuscript/pilot candidate requires its own committed render and inspection; these observations must not be relabeled as that later candidate's proof.

Reviewed owners: [renderer](https://github.com/docxology/docxology/blob/476fbb85ae30edf499b0742253228c8f5e047b7e/code/src/manuscript_rendering.py), [direct regressions](https://github.com/docxology/docxology/blob/476fbb85ae30edf499b0742253228c8f5e047b7e/code/tests/test_manuscript_rendering.py), and [rendering contract](https://github.com/docxology/docxology/blob/476fbb85ae30edf499b0742253228c8f5e047b7e/docs/manuscript/README.md).

## Problem and bounded correction

The frozen review deck had 172 slides. A 450-character greedy split could put a final word or short phrase on its own continuation slide: Motivation ended before “uncertainty.” despite available space. Every display unit also received a separate slide.

The corrected deck remains an unabridged review artifact. It prefers sentence boundaries, balances unavoidable short tails and packs adjacent text within subsection boundaries. Prose uses a separate 600-character/nine-estimated-line envelope at 60 characters per line, narrowed recursively for list indentation and counting block gaps. The existing 450-character indivisible-inline/table/code rules, figure/caption separation, simple table restrictions and hard failure for unsupported units remain.

Actual LibreOffice body-box inspection also exposed a linked bullet extending past its inherited right edge. Bullet body text now reserves a measured 0.5-inch right inset, without widening the body or budgets. A bounded comparison found that 0.4 inches still failed and both 0.5 and 0.6 passed; the smallest tested passing value was selected. Only the relevant OOXML inset attribute changes. Tests verify namespace/text/link/media preservation, idempotence, valid quote forms and refusal before replacing malformed input.

## Exact source and artifacts

Renderer SHA-256: `e6f79b48123fcf7c9f8f981a4b4f8e0ea0a4087bb22ab4814bf219978fbd38f6`.

The final render receipt SHA-256 is `4efa9fff9e53ae3de05e5bec66afc59ee0367bacf1f4dd805f56d71098262e7a`. Its source-link commit is exactly the reviewed 476fbb85 revision. Compared with the earlier frozen render, manuscript body/configuration/bibliography/figure inputs are unchanged; the renderer source hash changes.

| Review artifact | SHA-256 |
| --- | --- |
| PowerPoint | `22c9f802a543bccf923a2c2ca8a043b904783d06726b906fb7b336c46bd2f839` |
| Native PDF | `90e7c4d8a05f2678e640530eeb366ed6869c51db58a54b5e5a5c170514498407` |
| HTML | `81b8bf469155774efaebe2e40fa0bc732a0aa755b252df4fe931f3a55e71534f` |
| EPUB | `a8ebf49acc3766b081c1a4505b0f16d80ca87e27ca2405d38a071073de4d7cea` |
| LibreOffice slide PDF | `dedce43b311983efeab5c568fb4647a6c5ee50453021c667807f58cae7924c04` |

These hashes identify observed manual-review outputs; they do not declare a new deposited edition or an available public download route.

## Automated and format evidence

Qualified execution receipt `14206-ba6a7c6d85054f419f0753d2b4b104c1` finished successfully at the exact reviewed commit, with source unchanged, no timeout and no remaining descendants. **106 manuscript tests passed**, including real four-format rendering, internal slide-link targets and table semantics. Focused lint and the actual manuscript structural validator also passed in the source gate.

The declared template revision remains `3462d19761cc87d09a0b780ef978fa9efc142723` (4.0.2). The renderer uses pinned Pandoc 3.12.1, pandoc-crossref 0.3.26 built against that Pandoc, XeTeX 3.141592653-2.6-0.999998 and BibTeX 0.99e. Viewer inspection used LibreOffice 26.8.1.1 and PyMuPDF 1.28.2; tool/runtime and artifact bindings remain in the receipts.

The resulting PowerPoint/LibreOffice deck has **137 slides**, versus 172 before. Non-heading visible text matches in order after whitespace normalization; separate AST regressions preserve inline identity. External-link occurrences, paths and fragments are preserved, normalizing only the deliberate source-link commit rebind. Other historical pinned URLs stay exact. All four embedded figure byte payloads are unchanged.

All 137 viewer pages retain the expected text in order. **108 actual text body placeholders** were measured against inherited slide/layout/master geometry: **zero outside-body text and zero text/body/title overlaps**. Title-only, image and graphic-table layouts retain their separate visual checks; this count is not a claim that every slide uses the same body layout. The native PDF remains 16 physical pages; HTML images loaded without horizontal page overflow, and EPUB package/XHTML checks passed.

| Former tiny continuation | Corrected slide |
| --- | --- |
| 11: “uncertainty.” | 10: complete Motivation paragraph |
| 21: “properties of an object.” | 18 |
| 37: “an installable wheel.” | 32 |
| 43: “new edition’s extraction.” | 37 |
| 69: “tracing conditions.” | 58 |
| 119: “together.” | 103 |

## Independent disposition and limits

A separate Codex reviewer cleared the final source statically, reviewed all 137 preliminary slides and the 16-page native PDF/HTML/figures, then inspected final full-size slides 10, 18, 32, 37, 58, 103 and repaired 113 plus final slides 105–128. The reviewer verified the final receipt/artifact bindings and successful body-box/text coverage evidence, finding no observed clipping, overlap or remaining prose-pagination blocker in that scope.

This is assistant source/format review, not named human/editorial/scientific approval. Reader-specific EPUB visual review and other presentation viewers remain pending. Artifact receipts retain their pending human/editorial review fields and do not assess scientific validity or publication readiness. Full-profile generation, deployment, release and the later integrated candidate's format proof remain separate acceptance steps. Original manuscript prose and retained publication sources were not edited by this layout correction.
