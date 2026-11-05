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


## Integrated follow-up — source a69c6bbf, layout v5

This later review applies to committed source `a69c6bbf09c3c7d8d55aebe7c752b73444a44437`, including the scholarly PDF pilot and the final linked-bullet correction. The preceding 137-slide review remains historical evidence for `476fbb85ae30edf499b0742253228c8f5e047b7e`; its counts and artifacts have not been relabeled as this candidate.

Qualified execution `15024-8405211232564f72ae8aa1562950f142` succeeded with **125 manuscript tests passed in 38.49 seconds**, including the real four-format render. Six dependency deprecation warnings were retained. The run did not time out, left no remaining descendants and reported source unchanged. Every named native input matched its exact Git object at the reviewed commit and remained unchanged afterward. The worktree was explicitly recorded as dirty solely for the unrelated `reports/asset_size_2026-11-05.json` control receipt. This is a manuscript gate, not whole-repository acceptance.

### Earlier failures remain evidence

The attempt at `54bf5bc0e7da14dc7abaa850d20502f1445000d9`, receipt `14695-95c4c2ae9c474cbb94b8dbaa22574093`, retained **101 passed / 5 failed**. Its four-format render passed, but ordinary non-Git manuscript fixtures reached a Git-backed PDF lookup before their link checks. The committed repair defers that lookup only when no projection registry is declared; malformed JSON and dangling registry symlinks still refuse. A focused gate passed 82 checks, including those five fixtures and the deployed/projection suites. Those counts overlap other checks and are not added to the manuscript total.

The intermediate `cc33754e68c00bc6ca86eda4a61f3278cd44c160` render, receipt `14755-6e146db651924b398e4602b65a458717`, passed 106 automated checks and produced 141 slides, but **failed independent visual review**: slide 125 overprinted the final Scholar-readiness sentence inside a valid body box. Text-presence and aggregate body bounds did not detect it. The later negative-control measurement `14949-c03ff8f77f93406eb7d37e207bdb00cb` detected **15 substantial word overlaps**, all on that slide, despite preserved extractable words and the original body font. That intermediate artifact is not format-cleared. The integrating assistant separately viewed its full-size slides 40, 41 and 57 and found no issue on those three pages. That limited intermediate observation remains separate from the failed whole-deck visual result and the later full-deck review below.

Private measured variants retained the failed input. Complete sentence continuations within one logical bullet repaired the observed layout. The production rule groups linked-list sentences, retains a short emphasized label with its opening sentence, and accounts for each paragraph gap before packing. Generated nonbullet continuations keep their explicit margins and inherit the original active bullet level's font. No manuscript prose, source URLs, global fonts or allocation budgets were changed. This is observed behavior of this generated deck in the named viewer; no matching upstream defect or universal viewer claim is asserted.

The actual tests-first source gate retained 13 initial failures, followed by a narrow whitespace-only geometry failure. The final core gate passed 122 checks with lint clean; the final native gate above includes those cases and three native checks. The counts describe separate, overlapping scopes.

### Final artifact and receipt identities

| Observed object | SHA-256 |
| --- | --- |
| Render receipt | `df965384a80b9f518227b6ec4cd1f3c33d89c7c5fb64032b96887f9039edb7b8` |
| PowerPoint | `782e3f1f1de91b90f8a9b36a72a543b5f03b9f7248e398e53ad44bd794756fb8` |
| Native PDF | `2ea28625bd51d328512a346c3ddd9a03041d33b0dad52bb61f15d54e601d862f` |
| HTML | `87b1a22924706142d0e9990c4ddce0b50756bb64730d8dc9ebf4a77ea0ae987f` |
| EPUB | `0b7eddb874734ae23418e3213f65e7c9cfba01235a25fc5e34db24e55cd990a5` |
| LibreOffice slide PDF | `efc10b635050316dfdf8ccd3599cbdfa973c0b5ac89c4199d0f0055fc57a25ff` |
| Native source context | `dc171aa0892ab58f62fa4a62ac660fa0de547efe98b4fda91f35ac8a5b4b0d31` |
| Current semantic proof | `c4c843b4242012776fa5469181133cf0860ac75e02c87beb519cf73c0277a004` |
| Viewer body coverage | `9962f4ee046ee6c7348a7e1e4a4182c0c29c133f19fb77a8ba0f3014d013b1f6` |
| Viewer word coverage | `d0dc8200ff0beccaf24215e41c7659c74aeec6a313f6ba3076cecb39ad884a5b` |
| Four-format inspection | `10364b103dd5459f5690266e6728fdd94a2ae63ac2a5474891c8406e6dc95ca8` |

The producer is `coherent-list-paragraph-pagination-v5`, renderer source SHA-256 `d62a7f0a8e870916303bc7214f43ef8bf9e6bf8cc488bfe245f992d19014e7d4`. The declared 450-character indivisible/table/code budget, 600-character prose budget, 60-character line estimate, nine-line envelope and 457200-EMU bullet inset remain unchanged. Native tools and template remain pinned as above. Actual viewing used LibreOffice 26.8.1.1, executable SHA-256 `ddd0f0491a12ca2bec285ecf4b1244c3618fc6cb51f529769424c86d956283c3`, and PyMuPDF 1.28.2.

### Final preservation and layout result

The actual deck has **148 slides**. A private observational wrapper called the unchanged paginator and captured the resolved current manuscript and its unchanged returned projection. The check retained **34,752 non-table body characters**, **151 link occurrences**, all **42 table body rows**, code, document metadata, every source heading and all four image bindings. Original logical list boundaries and ordered starting/style attributes were preserved: **31 logical items remained 31 display fragments**. Repeated table headers matched their original column/header/footer structures. Internal link remapping resolved to actual output anchors; other link labels, targets and occurrences remained exact. Complete figure captions remain present, while the existing presentation policy uses shorter image labels.

The actual PowerPoint non-heading body matched projected prose, tables and code after whitespace normalization. All embedded figure payloads matched their fresh render hashes. Complete PowerPoint text was then found in the actual LibreOffice PDF in order, allowing automatic list labels and normalized punctuation/whitespace. Source/projection custody and viewer verification are separate checks.

All **119 text body placeholder pages** were measured against actual inherited slide/layout/master geometry, with **zero outside-body text**, **zero body/body or body/title overlap**, and no text beyond page edges. The new bounded word-box helper also found **zero substantial word overlaps across all 148 pages**. It refuses malformed, nonfinite, nonpositive or unbounded geometry and flags overlap greater than 40% of the smaller rectangle for words with at least two alphanumeric characters. Isolated symbols and one-character words are outside this detector; it supplements visual reading rather than certifying universal typography.

The repaired Scholar bullet is now slide **132**. Its indexing caveat retains the contiguous expected word sequence, and its body font measures **24.01 points**, matching the original observed size. All 19 slide contact sheets were produced. The native PDF remains **16 physical pages** without detected page-edge text overflow; HTML loaded all four figures without horizontal overflow; EPUB retained **13 valid XHTML documents**. Reader-specific EPUB visual review remains pending.

A separate Codex reviewer independently verified all 26 inspected source hashes against exact Git objects and all 13 output hashes, viewed **all 19 contact sheets covering 148 slides**, final full-size slide **132**, both native PDF contact sheets covering **16 pages**, and the full HTML capture. The reviewer found the repaired bullet clearly readable at the preserved 24.01-point size, with all three sentences and linked labels retained, and observed no other clipping or overprint in that scope. The reviewer also read the source/projection, body and word coverage scopes and cleared the final format evidence with the limits stated here. A second independent Codex reviewer, who had also cleared the exact source hashes statically, separately viewed all 19 final slide contact sheets, both native PDF contact sheets, the full HTML, repaired slide 132, method slides 40/41/57 and former-orphan slides 10/18/32/37/62. That reviewer verified six supplied JSON/receipt/viewer-PDF hashes and found no clipping or overlap blocker in that technical format scope. These overlapping review scopes are not additional test counts.

This assistant technical/format evidence does not supply named human, editorial or scientific approval. Render receipts keep those review fields pending and do not assess scientific validity or publication readiness. Deployment, indexing and the complete-profile release binder remain separate gates. Later publication commits may retain this review only after verifying that every named native input hash still matches this reviewed source; changed inputs require the applicable checks again.


## Fresh regeneration — source 75e89661

This follow-up records a fresh native render at committed source `75e896616b3c6e60994672ca7523cd51d549cf7a`. The earlier `a69c6bbf09c3c7d8d55aebe7c752b73444a44437` review and the failed intermediate attempts above remain historical observations with their original hashes. The earlier a69c6bbf raw execution artifacts were unavailable for rechecking when this follow-up began; this fresh artifact set does not recreate their custody or replace those historical records.

Qualified execution `15880-02685613871a461a9aa3899e3ddb354b` completed successfully with **125 manuscript tests passed in 47.36 seconds** and **six retained dependency deprecation warnings**. The worktree was clean before and after the run, the backend reported source unchanged, no timeout occurred, and no descendants remained. The pytest selection covered the two manuscript test files, including real four-format rendering. Subsequent checks covered the scoped semantic/viewer inspections. This was not a full repository, site-browser or Lighthouse run.

All **17 named render inputs** matched their exact Git objects at both the historical a69c6bbf source and the fresh 75e89661 source, and matched the checked-out bytes at independent review. The renderer remains `coherent-list-paragraph-pagination-v5`, SHA-256 `d62a7f0a8e870916303bc7214f43ef8bf9e6bf8cc488bfe245f992d19014e7d4`. The template remains version 4.0.2 at `3462d19761cc87d09a0b780ef978fa9efc142723`, with archive SHA-256 `b51a26aa354d31a627c730cb644a288aab240aaeb7877d6ed6e64dc1a5d70f21`; declared native tool pins are unchanged. The fresh inspection records Python 3.15.2, LibreOffice 26.8.1.1 and PyMuPDF 1.28.2.

### Fresh artifact identities

These hashes belong to the new 75e89661 render and its source-link binding. They must not be substituted for the a69c6bbf artifact hashes above.

| Fresh object | SHA-256 |
| --- | --- |
| Render receipt | `e566fdbb553aff2f7d5e035de5e6dd607efe309abbf8fd299a94698f5ad1adc2` |
| PowerPoint | `020cec272d58bb3d07a47c2810b7d983678aed41eccd37fe40478ede64ac83c8` |
| Native PDF | `db5d5a8f84e9defee994b758d9978531426bea32aa5e2ab4f0a900a1f063ce06` |
| HTML | `2e9d95a1948b17398885faf4f229cfb98f7abf9f072317af86e38219906df646` |
| EPUB | `36e1f64c5b8be99e4289f83734dca9e616c3d637102abb3a40a71eb7559756b5` |
| LibreOffice slide PDF | `73c91d922114c216cbe86367fc6df26f166463515390bc3bd0ed6988d01baf83` |
| Native source context | `40657ebd14b193627c10d0a8a7bb728caf6cd9995e98ef75aa15e6a19b812944` |
| Current semantic proof | `a97e00fe0c0902d3120d22fff4b14aab7a2f5cd94f8e3025f3536212dbc20902` |
| Viewer body coverage | `74972bac3b1a944ab210b91d8ad7baf05d8c8fc3c5b619985031259bef579548` |
| Viewer word coverage | `15f1c599064bd94d4891a4761d6672877f6f7c3eb65e448ef44976b42b7959e4` |
| Four-format inspection | `729d8cd4f955d76541b15c7d8c47af59aab452884dc1aebcab81c049f690cb27` |

### Fresh inspection and independent disposition

The new deck has **148 slides**. The current source/projection proof preserves **34,752 non-table body characters**, **151 link occurrences**, **42 table body rows**, all **four image bindings**, and **31 logical list items as 31 display fragments**, with internal anchors and other link targets checked separately. All 13 render-receipt artifacts matched their recorded sizes and hashes at independent review.

Actual LibreOffice inspection found **119 text body placeholder pages**, **zero outside-body text**, **zero body/body or body/title overlap**, and no detected page-edge text overflow. The unchanged bounded word-box detector found **zero substantial word overlaps across all 148 pages**, with the known-negative mode disabled. Its previously stated exclusions and geometry limits still apply; it is not a universal readability proof. Repaired slide **132** retains its contiguous indexing-caveat word sequence and **24.01-point** body font.

A separate Codex reviewer freshly viewed **all 19 slide contact sheets**, the full-size repaired slide **132**, both native PDF contact sheets covering **16 physical pages**, and the full HTML capture. No clipping, overprint or remaining layout blocker was observed within that coverage. The HTML inspection loaded all **four figures** with a 1280-pixel document width matching its viewport. The EPUB contained **13 valid XHTML documents**; reader-specific EPUB visual review remains pending.

An independent private custody copy retains 71 selected evidence files totaling 16,131,165 bytes; every file was rehashed against custody manifest SHA-256 `2491c8878b0dc4ca07b77331eaa9ca27c329ae19c3abd20a990e5b328f8f02dc`. This records selected artifact custody, not a whole-repository backup, public download route or archival deposit.

This is fresh assistant technical/format review of source 75e89661, not named human, editorial or scientific approval. The draft remains unpublished, without an assigned venue or manuscript DOI. Later report, cached-evidence or control-only commits are not new native renders: they may reuse this proof only after checking every named input and the pinned template identity. Changed render inputs require fresh applicable rendering and review. Whole-site acceptance, deployment, indexing and publication readiness remain separate gates.
