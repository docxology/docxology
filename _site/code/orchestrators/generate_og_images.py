#!/usr/bin/env python3
"""Generate tailored Open Graph preview images."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_COUNTS = REPO_ROOT / "data" / "current-counts.json"
W, H = 1200, 630


def _live_counts() -> tuple[int, int]:
    """Return (work_count, software_count) from the generated counts snapshot
    so og-publications.jpg/og-software.jpg never drift from the real totals."""
    payload = json.loads(CURRENT_COUNTS.read_text(encoding="utf-8"))
    counts = payload.get("counts", {})
    work_count = counts.get("bibliography_works")
    software_count = counts.get("generated_exports", {}).get("data_software_json")
    if not isinstance(work_count, int) or not isinstance(software_count, int):
        raise ValueError(f"{CURRENT_COUNTS} is missing bibliography_works or generated_exports.data_software_json")
    return work_count, software_count


def _assets() -> list[tuple[str, str, str]]:
    work_count, software_count = _live_counts()
    return [
        ("og-image.jpg", "Daniel Ari Friedman", "Research, software, art, and public-source discovery"),
        (
            "og-publications.jpg",
            "Publications",
            f"{work_count} curated works across Active Inference, biology, security, and art",
        ),
        (
            "og-software.jpg",
            "Software",
            f"{software_count} catalogued repositories plus public-source software release anchors",
        ),
        ("og-discovery.jpg", "Discovery Map", "Canonical identifiers, APIs, query recipes, and verification notes"),
        ("og-domains.jpg", "Research Domains", "Pathways through works, software, collaborators, and learning"),
        ("og-biomedicine.jpg", "Genetics & Biomedicine", "Bee evolution, gene expression, nuclear structure, and population genetics"),
        ("og-entomology.jpg", "Entomology", "Ant colonies, collective behavior, transcriptomics, and cognition"),
        ("og-active-inference.jpg", "Active Inference", "Free Energy Principle, generative models, formalization, and GNN"),
        ("og-cognitive-security.jpg", "Cognitive Security", "Narrative ecosystems, information commons, and multiagent security"),
        ("og-art-synergetics.jpg", "Art & Synergetics", "William Blake, Buckminster Fuller, Curio Cards, and quadray geometry"),
        ("og-computational.jpg", "Computational Methods", "Research templates, markdown containers, and reproducible workflows"),
        ("og-art.jpg", "Art Gallery", "Pen-and-ink drawings, Curio Cards, and visual research"),
        ("og-media.jpg", "Media & Talks", "Talks, podcasts, livestreams, courses, and interviews"),
        ("og-cite-verify.jpg", "Cite & Verify", "Citation exports, source-of-truth rules, and evidence ledger"),
    ]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Helvetica.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size=size)
        except Exception:
            continue
    return ImageFont.load_default()


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textbbox((0, 0), trial, font=fnt)[2] <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_image(path: str, title: str, subtitle: str) -> None:
    img = Image.new("RGB", (W, H), (12, 12, 14))
    draw = ImageDraw.Draw(img)

    # Layered dark field with restrained gold/red geometry.
    for y in range(H):
        r = 12 + int(22 * y / H)
        g = 12 + int(14 * y / H)
        b = 14 + int(10 * y / H)
        draw.line([(0, y), (W, y)], fill=(r, g, b))
    for i in range(0, W, 80):
        draw.line([(i, 0), (i - 260, H)], fill=(34, 31, 29), width=1)
    for i in range(-400, W, 120):
        draw.line([(i, H), (i + 380, 0)], fill=(42, 32, 27), width=1)
    draw.ellipse((780, -130, 1330, 420), outline=(201, 168, 76), width=3)
    draw.ellipse((-120, 330, 430, 850), outline=(126, 42, 34), width=3)
    draw.line([(760, 78), (1080, 265), (905, 485), (760, 78)], fill=(201, 168, 76), width=4)
    draw.line([(120, 510), (330, 390), (480, 540), (120, 510)], fill=(126, 42, 34), width=4)

    title_font = font(72, bold=True)
    sub_font = font(32)
    small_font = font(25)

    x = 78
    y = 108
    draw.text((x, y), title, font=title_font, fill=(245, 240, 230))
    y += 104
    for line in wrap(draw, subtitle, sub_font, 850)[:3]:
        draw.text((x, y), line, font=sub_font, fill=(216, 210, 200))
        y += 44

    draw.rounded_rectangle((78, 480, 610, 548), radius=10, outline=(201, 168, 76), width=2, fill=(24, 23, 24))
    draw.text((102, 498), "danielarifriedman.com", font=small_font, fill=(240, 201, 106))
    draw.text((78, 570), "docxology/docxology · ORCID 0000-0001-6232-9096", font=small_font, fill=(168, 160, 152))

    img.save(REPO_ROOT / path, quality=92, optimize=True)


COUNTS_SIDECAR = REPO_ROOT / "data" / "og-image-counts.json"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the OG images' baked-in counts are stale")
    args = parser.parse_args()

    work_count, software_count = _live_counts()

    if args.check:
        if not COUNTS_SIDECAR.exists():
            raise SystemExit("Stale OG images: no og-image-counts.json sidecar; run generate_og_images.py")
        recorded = json.loads(COUNTS_SIDECAR.read_text(encoding="utf-8"))
        if recorded.get("work_count") != work_count or recorded.get("software_count") != software_count:
            raise SystemExit(
                "Stale OG images: og-publications.jpg/og-software.jpg were generated with "
                f"work_count={recorded.get('work_count')}, software_count={recorded.get('software_count')}, "
                f"but current-counts.json now reports work_count={work_count}, software_count={software_count}. "
                "Re-run generate_og_images.py."
            )
        print(f"checked OG images (work_count={work_count}, software_count={software_count})")
        return

    for path, title, subtitle in _assets():
        draw_image(path, title, subtitle)
    COUNTS_SIDECAR.write_text(
        json.dumps({"work_count": work_count, "software_count": software_count}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(_assets())} Open Graph images")


if __name__ == "__main__":
    main()
