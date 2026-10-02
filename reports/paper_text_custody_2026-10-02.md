# Paper-text source custody — 2026-10-02

Forty-three archived-paper text extractions contained an unintended directory-migration edit: quoted `manuscript/` paths had become `docs/manuscript/`. The archived PDFs retain the original paths. The text files now match their exact pre-migration Git blobs, and one affected literal evidence quotation in the Refinement Gold metadata has been restored to the PDF's wording.

The [machine-readable receipt](paper_text_custody_2026-10-02.json) records every affected relative path, source-PDF SHA-256, previous and restored text SHA-256, and recovered Git blob. Recovery used commit `5c25de204170cdf03c2f341f0fdc10f399aebaa4`; the archive comparison used published baseline `cf368af238de371865d9876afd5321314eb03406`.

Acceptance checks:

- Each of the 43 files matched the historical migration blob before replacement. Every changed hunk consisted only of inserting `docs/` before `manuscript/`.
- Every recovered file's header-selected PDF and every PDF already present in its folder at the recovery commit match that commit's bytes. Newer PDFs are covered by the separate comparison of all 222 current archived PDFs with the published baseline.
- All 1,723 grounded method and finding quotations still occur in their own paper texts, including 419 quotations in the affected folders, with only whitespace and ligature normalization.
- Direct PDF text extraction confirmed the original paths in Fourfold Vision, ENTO, and both archived FEP Lean PDFs. The repaired Refinement Gold quotation was separately checked against its source PDF.
- The focused bibliography-authority, work-enrichment, and paper-text-extraction suites passed all 53 tests.
- The newer Template Pitch Deck extraction was retained: its historical short-deck text has been superseded by the current manuscript extraction.

This pass restores source wording and preserves existing research qualifications. It does not independently re-extract every character of every recovered text, replicate research results, or attest hosted deployment. The machine receipt distinguishes these limits from the checks actually performed.
