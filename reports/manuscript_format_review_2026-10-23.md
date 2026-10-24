# Manuscript format inspection — 2026-10-23

Status: assistant inspection of a frozen working-tree draft. Named human visual
approval, editorial review, scientific validity and publication readiness remain
unassessed or pending.

The inspected source is version 0.6.0-draft. Its repository-link base is
82e358abbe2469ab02f841ecb66dd2a3383fe725; the render receipt separately binds hashes of the source files.
This is prelanding layout evidence, not a clean-commit or deployment receipt.
A later candidate needs its own source-bound render.

## Observed surfaces

- Native template PDF: every page of the 12-page document, including the cover,
  four diagrams, table, references and section transitions.
- HTML: the complete desktop rendering and a 390-pixel mobile viewport;
  diagrams loaded and the measured document did not overflow horizontally.
- EPUB: ZIP/XML/internal-reference checks and browser inspection of every one
  of its 12 XHTML documents. The qualified rerender retained identical XHTML
  and image bytes; only package identifier metadata changed. This is not native
  ebook-reader acceptance.
- PowerPoint: all 129 slides rendered through LibreOffice 26.8.1.1, captured at
  90 dpi and inspected across the complete 11-sheet capture manifest. All four
  figure frames were also inspected at full capture size. No remaining clipping
  or overlapping content was observed in this runtime. The deck retains the
  complete manuscript for review; it is not an abridged talk.

## Corrections and retained failures

The initial presentation clipped long prose and captions and overlapped tables.
A supplementary visible-text comparison found missing long runs on 21 of 43
slides. Its green successor did not detect remaining automatic image-caption
clipping; full-size inspection rejected that intermediate layout.

The corrected presentation producer is bounded-block-pagination-v2. It separates
bounded prose, list items, table segments, images and full captions; image frames
use short descriptive labels. Generic container content reaches the presentation
writer, and internal subsection/container links resolve to the corresponding
slide. Real Pandoc/PPTX relationship regressions cover the previously missing
subsection target.

One native PDF attempt reached its 180-second worker deadline and published no
review directory. A fresh four-format run passed without changing that deadline.
The failed attempt and earlier failed captures remain retained outside the
source tree. Some Chrome capture calls reported a saved-path error after
writing valid PNGs; inspection used the decoded files and their recorded hashes,
not a claim that those CLI calls exited successfully.

The current long-text comparison found no missing long runs on the 129-slide
presentation. Text comparison supplements visual inspection and does not prove
all glyphs, objects or presentation-viewer behavior.

## Frozen artifact binding

| Format | Artifact | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| pdf | docxology-methods.pdf | 165362 | 770632059aca0d96e62e279f8e756557d48507dbd1dff167467a3f335710eeb1 |
| html | docxology-methods.html | 59557 | 68ae4916d0e10d799f2567923503e32b2bbf8017e0e9c22115d8d3997d0aacb2 |
| epub | docxology-methods.epub | 406338 | c1cac953a79528495bb6394dd43be585f31498105e53e802ae80564ad5eb1191 |
| slides | docxology-methods.pptx | 544811 | d7d50ffb5ea37a3e33c2c3d0a1c08a45cd1e0e3ec74aa5eac9cadd1c09f61357 |

Render receipt SHA-256: 36f96296b53f6716afeab7974d2254ba9903b290fe1b427673f1ff9fd6092a33

Renderer SHA-256: 7b0478a577c2a9860bccf51d9915a997c1db33fd837cb4fdacab2d48780df338

The receipt also binds the configuration, section sources, bibliography, pinned
template export, external Python runtime, tools, figures and output hashes.
Review artifacts and capture manifests remain outside normal site generation.

## Reproduction and limits

Use the declared [render command](../docs/manuscript/README.md), its pinned
template and qualified external interpreter, and a new review directory.
Rasterize the native PDF, render the presentation in the named viewer, inspect
every capture and verify the receipt hashes. Other readers and presentation
applications require their own inspection.

This observation does not replace the complete selected test suite,
regeneration, standard validation, source landing, hosted CI or deployment
acceptance. It grants no human/editorial approval or new scientific claim.
