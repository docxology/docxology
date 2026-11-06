# Manuscript status — docxology

Source version 0.7.0-draft, dated 2026-11-05, is a repository-methods draft about the public research, software and citation index. It describes implemented mechanisms and documented maintenance cases. It has no assigned venue, manuscript DOI, comparative experiment, or new empirical research results. Archived research publications under [papers/](../../papers/) retain their separate identities and bytes.

This revision expands the source-to-projection method with complete-or-error intake, document-byline review, selected-edition custody, bounded hosting, search-engine readiness, explicit responsibility states, a claim-to-evidence map, failure controls and a reproducibility protocol. Primary external references provide provenance context and official hosting/indexing requirements; they do not validate this implementation or establish standards conformance. The supplement maps claims to source owners and regression tests.

The [structural validator](../../code/orchestrators/validate_manuscript.py) checks manuscript inputs; it does not render or assess publication readiness. The [rendering guide](README.md) pins the committed docxology/template 4.0.2 API, Pandoc/crossref pair, XeTeX, BibTeX, external dependency interpreter, cover and body-diagram producers. Explicit rendering writes a new external review directory and binds source, runtime, tools, transformations, figures and output hashes. Prior attempts are preserved. Trusted template code and TeX execute; process controls alone are not an OS sandbox.

## Current production-source custody

The [clean-source follow-up](../../reports/software_quality_followup_2026-11-06.md)
records current checkpoint `cdca4d9056033532c2cefda2167034008d736e53`. Its core
suite passed 2,598 tests and 13 subtests; a separate fresh four-format build
passed 128 manuscript cases. Both actually ran at that clean commit, retained
six dependency warnings, and reported unchanged source.

The canonical receipt SHA-256 is
`edd567c53ec386adc9ce04d2c60a2f8213a5c84e55937ebe49fb33f3a056c60c`;
139 production Python members independently match committed Git bytes and the
working tree. The follow-up binds all 17 direct inputs, output hashes and
automated semantic/viewer checks. This is a working-source content snapshot,
not a runtime execution trace or proof about an arbitrary dirty checkout.

Later documentation/control commits may reuse this proof only with unchanged
production membership/bytes, direct render inputs and pinned template identity.
They are not new renders of a later commit. Human/editorial approval and
reader-specific EPUB review remain pending.

## Earlier source-bound formats

The earlier [C82 production-custody build](../../reports/software_quality_followup_2026-11-05.md)
at `c82dd2dd0d8ef59ab7149b072b03f418d93b3234` passed 128 manuscript tests and
recorded receipt `3dda11333d1d5fdf025a8e040ba82671e5732ce922e514166066083948993152`.
It remains evidence for that earlier source, followed by the separate fresh
checkpoint above after the reproducibility generator changed.

The [2026-11-05 format review](../../reports/manuscript_format_review_2026-11-05.md) preserves the historical a69c6bbf and 75e89661 renders and failed intermediate attempts. Following three groups of hosted-core failures, 192 related tests and whole-code Ruff passed on the installed corrections; the report distinguishes that selected dirty-source gate from clean-source or full-suite acceptance. The corrected source was committed as `3a445fed495d6f692254f698d227605edb65de87`.

Fresh four-format regeneration at that clean C3 source passed 125 manuscript tests in 19.74 seconds with six retained dependency warnings, followed by scoped semantic/viewer checks and independent assistant format review. The fresh render receipt SHA-256 is `2ca700132a6e199244a8c45764be88d35df3a303baa8b1a19888b597d25abe75`. The report records the separate artifact hashes, full 138-file production Python archive/member binding, all 17 direct render inputs and selected private custody. The production archive SHA-256 is `edd4256781703a8916fba3b9ae0e1ccf1a921caf55d2eb7ab3d8bc3f7d651fe2`; template and renderer pins remain unchanged.

Later status/report/control commits may reuse the C3 proof only after rechecking the complete production-source member map, all 17 direct render inputs and the pinned template identity. They are not new renders of a later candidate. Reader-specific EPUB visual review, named human approval, editorial/scientific assessment and publication readiness remain separate and pending.

Manuscript text and original figures use CC BY 4.0. Archived papers and provider material retain their own terms. Review outputs are not new bibliography entries or archival deposits.
