#!/usr/bin/env python3
"""Extract full text and images from all paper PDFs.

For each paper folder under papers/ that contains at least one PDF:
  - Extract full text to full_text.md
  - Extract embedded images to images/ subfolder
  - Use PyMuPDF (fitz) for text + image extraction
  - Fall back to pdftotext for text if PyMuPDF fails
  - OCR with tesseract for scanned/image-only PDFs

Usage:
    python3 extract_paper_texts.py [--force] [--ocr-only-image-pdfs]
"""

import sys
import os
import json
import hashlib
import subprocess
import shutil
from pathlib import Path

try:
    import fitz  # PyMuPDF
    HAVE_PYMUPDF = True
except ImportError:
    fitz = None
    HAVE_PYMUPDF = False

try:
    import pypdf
    HAVE_PYPDF = True
except ImportError:
    pypdf = None
    HAVE_PYPDF = False

REPO_ROOT = Path(__file__).resolve().parents[2]  # docxology/
PAPERS_DIR = REPO_ROOT / "papers"
TESSERACT = shutil.which("tesseract")
PDFTOTEXT = shutil.which("pdftotext")

def is_scanned_pdf(pdf_path):
    """Check if a PDF is likely scanned (image-only) by checking text coverage on first few pages."""
    if HAVE_PYMUPDF:
        doc = fitz.open(str(pdf_path))
        text_chars = 0
        for i in range(min(5, len(doc))):
            text_chars += len(doc[i].get_text().strip())
        doc.close()
        return text_chars < 100
    if HAVE_PYPDF:
        reader = pypdf.PdfReader(str(pdf_path))
        text_chars = 0
        for i in range(min(5, len(reader.pages))):
            text_chars += len((reader.pages[i].extract_text() or "").strip())
        return text_chars < 100
    return False

def extract_text_pymupdf(pdf_path):
    """Extract text using PyMuPDF."""
    if not HAVE_PYMUPDF:
        return []
    doc = fitz.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append((i + 1, text))
    doc.close()
    return pages

def extract_text_pypdf(pdf_path):
    """Extract text using pypdf."""
    if not HAVE_PYPDF:
        return []
    reader = pypdf.PdfReader(str(pdf_path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append((i + 1, text))
    return pages

def extract_text_pdftotext(pdf_path):
    """Extract text using pdftotext as fallback."""
    if not PDFTOTEXT:
        return []
    result = subprocess.run(
        [PDFTOTEXT, "-layout", str(pdf_path), "-"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return []
    text = result.stdout
    # pdftotext uses form feed between pages
    parts = text.split("\f")
    return [(i + 1, p) for i, p in enumerate(parts) if p.strip()]

def ocr_pdf(pdf_path, max_pages=None):
    """OCR a PDF using pdftoppm + tesseract."""
    if not TESSERACT:
        return []
    
    # Convert PDF pages to images and OCR them
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # Use pdftoppm to convert to images
        cmd = ["pdftoppm", "-r", "300", "-png", str(pdf_path), os.path.join(tmpdir, "page")]
        result = subprocess.run(cmd, capture_output=True, timeout=300)
        if result.returncode != 0:
            return []
        
        # Find all generated images
        images = sorted(Path(tmpdir).glob("page-*.png"))
        if max_pages:
            images = images[:max_pages]
        
        pages = []
        for img_path in images:
            # Extract page number from filename
            stem = img_path.stem
            page_num = int(stem.split("-")[-1])
            
            # OCR with tesseract
            result = subprocess.run(
                [TESSERACT, str(img_path), "-", "--psm", "3"],
                capture_output=True, text=True, timeout=60
            )
            if result.returncode == 0:
                pages.append((page_num, result.stdout))
        
        return pages

def extract_images(pdf_path, output_dir):
    """Extract embedded images from a PDF using PyMuPDF.

    Returns a list of (page_num, filename) tuples so the caller can
    embed image references in the markdown at the correct page position.
    """
    if not HAVE_PYMUPDF:
        return []
    doc = fitz.open(str(pdf_path))
    extracted = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list):
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]

                # Skip tiny images (likely icons, bullets, etc.)
                if len(image_bytes) < 1000:
                    continue

                # Skip very small dimensions
                width = base_image.get("width", 0)
                height = base_image.get("height", 0)
                if width < 50 or height < 50:
                    continue

                filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                filepath = output_dir / filename

                # Only write if not already exists
                if not filepath.exists():
                    filepath.write_bytes(image_bytes)
                extracted.append((page_num + 1, filename))
            except Exception as exc:
                print(f"  WARNING: image extraction failed on page {page_num + 1}, image {img_index + 1} of {pdf_path.name}: {exc}", file=sys.stderr)
                continue

    doc.close()
    return extracted

def format_markdown(pages, title, pdf_name, images=None):
    """Format extracted pages as markdown.

    If images (list of (page_num, filename)) is provided, embed image
    references at the end of each page's text so readers and crawlers
    can discover extracted figures in context.
    """
    # Group images by page
    from collections import defaultdict
    images_by_page = defaultdict(list)
    if images:
        for page_num, filename in images:
            images_by_page[page_num].append(filename)

    total_images = sum(len(v) for v in images_by_page.values())

    lines = [
        f"# Full Text: {title}",
        "",
        f"> Extracted from `{pdf_name}`",
        "",
    ]
    if total_images:
        lines.append(f"> {total_images} figures extracted to `images/`")
        lines.append("")
    lines += ["---", ""]

    for page_num, text in pages:
        if not text.strip():
            text = f"*[Page {page_num} appears to be blank or image-only]*"
        lines.append(f"## Page {page_num}")
        lines.append("")
        lines.append(text.strip())
        lines.append("")

        # Embed image references for this page
        page_imgs = images_by_page.get(page_num, [])
        for img_filename in page_imgs:
            lines.append(f"![{img_filename}](images/{img_filename})")
            lines.append("")

    return "\n".join(lines)

def process_paper(paper_dir, force=False):
    """Process a single paper folder."""
    # Find PDFs
    pdfs = sorted(paper_dir.glob("*.pdf"))
    if not pdfs:
        return None
    
    # Use the largest PDF (likely the main manuscript)
    main_pdf = max(pdfs, key=lambda p: p.stat().st_size)
    
    # Check if full_text.md already exists
    full_text_path = paper_dir / "full_text.md"
    if full_text_path.exists() and not force:
        return "skipped"
    
    # Load metadata for title
    meta_path = paper_dir / "metadata.json"
    title = paper_dir.name
    if meta_path.exists():
        with open(meta_path) as f:
            meta = json.load(f)
        title = meta.get("title", title)
    
    # Create images directory
    images_dir = paper_dir / "images"
    images_dir.mkdir(exist_ok=True)
    
    # Extract text
    pages = []
    method = "pymupdf" if HAVE_PYMUPDF else "pypdf"
    try:
        scanned = is_scanned_pdf(main_pdf)
        
        if scanned and TESSERACT:
            # OCR for scanned PDFs
            method = "ocr"
            pages = ocr_pdf(main_pdf)
            if not pages:
                if HAVE_PYMUPDF:
                    method = "pymupdf_fallback"
                    pages = extract_text_pymupdf(main_pdf)
                else:
                    method = "pypdf_fallback"
                    pages = extract_text_pypdf(main_pdf)
        else:
            if HAVE_PYMUPDF:
                pages = extract_text_pymupdf(main_pdf)
            else:
                pages = extract_text_pypdf(main_pdf)
            if not pages and PDFTOTEXT:
                method = "pdftotext"
                pages = extract_text_pdftotext(main_pdf)
    except Exception as e:
        if PDFTOTEXT:
            method = "pdftotext"
            pages = extract_text_pdftotext(main_pdf)
        else:
            return f"error: {e}"
    
    # Extract images first so we can embed references in the markdown
    images = extract_images(main_pdf, images_dir)

    if not pages:
        return "error: no text extracted"

    # Write full_text.md with inline image references
    md_content = format_markdown(pages, title, main_pdf.name, images=images)
    md_content += f"\n\n---\n*Extraction method: {method}*\n"
    full_text_path.write_text(md_content, encoding="utf-8")

    return f"ok ({len(pages)} pages, {len(images)} images, {method})"

def main():
    if not HAVE_PYMUPDF and not HAVE_PYPDF and not PDFTOTEXT:
        print("ERROR: Neither PyMuPDF, pypdf, nor pdftotext is available. Install pypdf with: pip3 install pypdf")
        sys.exit(1)
    force = "--force" in sys.argv
    
    papers = sorted(d for d in PAPERS_DIR.iterdir() if d.is_dir())
    stats = {"ok": 0, "skipped": 0, "no_pdf": 0, "error": 0}
    
    for paper_dir in papers:
        pdfs = list(paper_dir.glob("*.pdf"))
        if not pdfs:
            stats["no_pdf"] += 1
            continue
        
        result = process_paper(paper_dir, force=force)
        if result is None:
            stats["no_pdf"] += 1
        elif result == "skipped":
            stats["skipped"] += 1
        elif result.startswith("ok"):
            stats["ok"] += 1
        elif result.startswith("error"):
            stats["error"] += 1
            print(f"  ERROR: {paper_dir.name}: {result}")
        else:
            stats["ok"] += 1
        
        if result and result != "skipped":
            print(f"  {paper_dir.name}: {result}")
    
    print(f"\n=== Summary ===")
    print(f"  OK: {stats['ok']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  No PDF: {stats['no_pdf']}")
    print(f"  Errors: {stats['error']}")
    print(f"  Total: {sum(stats.values())}")

if __name__ == "__main__":
    main()
