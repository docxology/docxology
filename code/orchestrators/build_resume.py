#!/usr/bin/env python3
"""Build structured resume/CV JSON, plaintext variants, and PDF output."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
from io import BytesIO
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "code" / "src"
sys.path.insert(0, str(SRC_DIR))

from site_nav import HEAD_EXTRAS  # noqa: E402
from resume_data import (  # noqa: E402
    SOURCE_FILES,
    VARIANTS,
    build_resume_payload,
    date_range,
    filter_items,
    filtered_software,
    filtered_works,
    json_dumps,
    render_text,
    source_manifest as resume_source_manifest,
)

try:
    from report_paths import generated_timestamp
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp

JSON_OUT = REPO_ROOT / "data" / "resume.json"
RESUME_DIR = REPO_ROOT / "resume"
FULL_PDF = RESUME_DIR / "resume.pdf"
FULL_HTML = RESUME_DIR / "resume.html"
VERIFY_OUT = RESUME_DIR / "verify.html"
RESUME_HTML_URL = "https://danielarifriedman.com/resume/resume.html"
VERIFY_URL = "https://danielarifriedman.com/resume/verify.html"
RESUME_JSON_URL = "https://danielarifriedman.com/data/resume.json"
RESUME_PDF_URL = "https://danielarifriedman.com/resume/resume.pdf"
TXT_OUTPUTS = {
    "full": RESUME_DIR / "full.txt",
    "academic": RESUME_DIR / "academic.txt",
    "software-consulting": RESUME_DIR / "software-consulting.txt",
    "teaching-service": RESUME_DIR / "teaching-service.txt",
}
PDF_FONT_REGULAR = "ResumeVera"
PDF_FONT_BOLD = "ResumeVeraBold"
_PDF_FONTS_REGISTERED = False
PDF_RED = "#A6192E"
PDF_RED_DARK = "#7F101F"
PDF_RED_PALE = "#FFF1F3"
PDF_BLACK = "#111111"
PDF_BODY = "#151515"
LINK_TOKEN_RE = re.compile(
    r"(?P<url>https?://[^\s<]+)|"
    r"(?P<doi>10\.\d{4,9}/[^\s<]+)|"
    r"(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})"
)
TRAILING_LINK_PUNCT = ".,;:)]}"


def _sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _source_manifest() -> dict:
    return resume_source_manifest(REPO_ROOT)


def _provenance_base(payload: dict, json_bytes: bytes) -> dict:
    source = _source_manifest()
    try:
        import reportlab

        reportlab_version = getattr(reportlab, "Version", "unknown")
    except ImportError:  # pragma: no cover - exercised only in minimal environments
        reportlab_version = "not-installed"
    return {
        "generator": {
            "name": "code/orchestrators/build_resume.py",
            "schema_version": 2,
            "reportlab_version": reportlab_version,
        },
        "generated_at": payload["generated_at"],
        "resume_html_url": RESUME_HTML_URL,
        "verification_url": VERIFY_URL,
        "resume_json_url": RESUME_JSON_URL,
        "resume_pdf_url": RESUME_PDF_URL,
        "source_manifest": source,
        "resume_json": {"bytes": len(json_bytes), "sha256": _sha256_bytes(json_bytes)},
        "source_manifest_matches_payload": payload.get("integrity", {}).get("source_manifest") == source,
    }


def existing_generated_at() -> str | None:
    if not JSON_OUT.exists():
        return None
    try:
        return json.loads(JSON_OUT.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def _link_markup(label: str, target: str) -> str:
    label_escaped = html.escape(label)
    target_escaped = html.escape(target, quote=True)
    return (
        f'<link href="{target_escaped}" color="{PDF_RED_DARK}">'
        f'<font color="{PDF_RED_DARK}" backColor="{PDF_RED_PALE}"><u>{label_escaped}</u></font>'
        "</link>"
    )


def _paragraph_markup(text: str, *, linkify: bool = True) -> str:
    if not linkify:
        return html.escape(text).replace("\n", "<br/>")

    parts: list[str] = []
    cursor = 0
    for match in LINK_TOKEN_RE.finditer(text):
        parts.append(html.escape(text[cursor : match.start()]))
        token = match.group(0)
        trailing = ""
        while token and token[-1] in TRAILING_LINK_PUNCT:
            trailing = token[-1] + trailing
            token = token[:-1]
        if match.group("email"):
            target = f"mailto:{token}"
        elif match.group("doi"):
            target = f"https://doi.org/{token}"
        else:
            target = token
        parts.append(_link_markup(token, target))
        parts.append(html.escape(trailing))
        cursor = match.end()
    parts.append(html.escape(text[cursor:]))
    return "".join(parts).replace("\n", "<br/>")


def _paragraph(text: str, style, *, linkify: bool = True):
    from reportlab.platypus import Paragraph

    return Paragraph(_paragraph_markup(text, linkify=linkify), style)


def _markup_paragraph(markup: str, style):
    from reportlab.platypus import Paragraph

    return Paragraph(markup, style)


def _bold_markup(text: str, *, color: str = PDF_RED_DARK) -> str:
    return f'<font name="{PDF_FONT_BOLD}" color="{color}">{html.escape(text)}</font>'


def _label_value(label: str, value, style):
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value)
    return _markup_paragraph(f"{_bold_markup(label)} {_paragraph_markup(str(value))}", style)


def _link_paragraph(label: str, target: str, style):
    return _markup_paragraph(_link_markup(label, target), style)


def _draw_qr(canvas, value: str, x: float, y: float, size: float) -> None:
    from reportlab.lib import colors
    from reportlab.graphics import renderPDF
    from reportlab.graphics.barcode.qr import QrCodeWidget
    from reportlab.graphics.shapes import Drawing

    canvas.saveState()
    canvas.setFillColor(colors.white)
    canvas.rect(x, y, size, size, stroke=0, fill=1)
    canvas.restoreState()
    qr = QrCodeWidget(value)
    bounds = qr.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(size, size, transform=[size / width, 0, 0, size / height, 0, 0])
    drawing.add(qr)
    renderPDF.draw(drawing, canvas, x, y)
    canvas.linkURL(value, (x, y, x + size, y + size), relative=0)


def _qr_flowable(value: str, size: float):
    from reportlab.platypus import Flowable

    class QRFlowable(Flowable):
        def __init__(self, url: str, width: float) -> None:
            super().__init__()
            self.value = url
            self.width = width
            self.height = width

        def draw(self) -> None:
            _draw_qr(self.canv, self.value, 0, 0, self.width)

    return QRFlowable(value, size)


def _page_footer_factory(provenance: dict):
    from reportlab.lib import colors

    short_hash = provenance["source_manifest"]["sha256"][:12]
    generated_at = provenance["generated_at"]

    def _page_footer(canvas, doc) -> None:
        canvas.saveState()
        canvas.setTitle("Daniel Ari Friedman - Public Structured CV")
        canvas.setAuthor("Daniel Ari Friedman")
        canvas.setSubject("Accessible, source-verified structured curriculum vitae")
        canvas.setKeywords("Daniel Ari Friedman, CV, resume, publications, software, verification")
        canvas.setCreator("docxology build_resume.py")
        if hasattr(canvas, "setLang"):
            canvas.setLang("en-US")
        page_width = doc.pagesize[0]
        qr_size = 28
        qr_x = page_width - doc.rightMargin - qr_size
        qr_y = 11
        canvas.setStrokeColor(colors.HexColor(PDF_RED))
        canvas.setLineWidth(0.8)
        canvas.line(doc.leftMargin, 47, page_width - doc.rightMargin, 47)
        canvas.setFont(PDF_FONT_BOLD, 6.6)
        canvas.setFillColor(colors.HexColor(PDF_RED_DARK))
        canvas.drawString(doc.leftMargin, 34, f"Build {generated_at} | source sha256 {short_hash}")
        canvas.setFont(PDF_FONT_REGULAR, 6.4)
        canvas.setFillColor(colors.HexColor(PDF_BODY))
        canvas.drawString(doc.leftMargin, 23, f"Verify: {VERIFY_URL}")
        canvas.setFont(PDF_FONT_BOLD, 6.7)
        canvas.setFillColor(colors.HexColor(PDF_RED_DARK))
        canvas.drawRightString(qr_x - 7, 25, f"Page {doc.page}")
        _draw_qr(canvas, VERIFY_URL, qr_x, qr_y, qr_size)
        canvas.restoreState()

    return _page_footer


def _register_pdf_fonts() -> None:
    """Register embedded TrueType fonts so Poppler renders text on all platforms."""
    global _PDF_FONTS_REGISTERED
    if _PDF_FONTS_REGISTERED:
        return
    import reportlab
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_dir = Path(reportlab.__file__).resolve().parent / "fonts"
    pdfmetrics.registerFont(TTFont(PDF_FONT_REGULAR, str(font_dir / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont(PDF_FONT_BOLD, str(font_dir / "VeraBd.ttf")))
    _PDF_FONTS_REGISTERED = True


def _styles():
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet

    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "ResumeTitle",
            parent=base["Title"],
            fontName=PDF_FONT_BOLD,
            fontSize=20,
            leading=24,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_BLACK),
            spaceAfter=5,
        ),
        "cover_title": ParagraphStyle(
            "ResumeCoverTitle",
            parent=base["Title"],
            fontName=PDF_FONT_BOLD,
            fontSize=25,
            leading=29,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_BLACK),
            spaceAfter=4,
        ),
        "cover_kicker": ParagraphStyle(
            "ResumeCoverKicker",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=8.2,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_RED_DARK),
            spaceAfter=5,
        ),
        "cover_hash": ParagraphStyle(
            "ResumeCoverHash",
            parent=base["Normal"],
            fontName=PDF_FONT_REGULAR,
            fontSize=6.05,
            leading=7.1,
            textColor=colors.HexColor(PDF_BODY),
            splitLongWords=True,
        ),
        "subtitle": ParagraphStyle(
            "ResumeSubtitle",
            parent=base["Normal"],
            fontName=PDF_FONT_REGULAR,
            fontSize=8.6,
            leading=10.6,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_BODY),
            spaceAfter=6,
        ),
        "contact": ParagraphStyle(
            "ResumeContact",
            parent=base["Normal"],
            fontName=PDF_FONT_REGULAR,
            fontSize=7.2,
            leading=9.0,
            textColor=colors.HexColor(PDF_BODY),
        ),
        "metric_label": ParagraphStyle(
            "ResumeMetricLabel",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=6.5,
            leading=7.8,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_RED_DARK),
        ),
        "metric_value": ParagraphStyle(
            "ResumeMetricValue",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=12,
            leading=13.5,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_BLACK),
        ),
        "metric_note": ParagraphStyle(
            "ResumeMetricNote",
            parent=base["Normal"],
            fontName=PDF_FONT_REGULAR,
            fontSize=6.3,
            leading=7.4,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PDF_BODY),
        ),
        "section": ParagraphStyle(
            "ResumeSection",
            parent=base["Heading2"],
            fontName=PDF_FONT_BOLD,
            fontSize=11.2,
            leading=13.2,
            textColor=colors.HexColor(PDF_RED_DARK),
            spaceBefore=8,
            spaceAfter=2,
        ),
        "table_header": ParagraphStyle(
            "ResumeTableHeader",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=6.5,
            leading=7.5,
            textColor=colors.white,
            alignment=TA_CENTER,
        ),
        "date": ParagraphStyle(
            "ResumeDate",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=7.2,
            leading=8.6,
            textColor=colors.HexColor(PDF_RED_DARK),
            alignment=TA_RIGHT,
        ),
        "record_title": ParagraphStyle(
            "ResumeRecordTitle",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=7.8,
            leading=9.1,
            textColor=colors.HexColor(PDF_BLACK),
        ),
        "repo": ParagraphStyle(
            "ResumeRepo",
            parent=base["Normal"],
            fontName=PDF_FONT_BOLD,
            fontSize=6.8,
            leading=8.0,
            textColor=colors.HexColor(PDF_BLACK),
            splitLongWords=True,
        ),
        "body": ParagraphStyle(
            "ResumeBody",
            parent=base["BodyText"],
            fontName=PDF_FONT_REGULAR,
            fontSize=7.2,
            leading=8.6,
            textColor=colors.HexColor(PDF_BODY),
            spaceAfter=1.8,
            splitLongWords=True,
        ),
        "small": ParagraphStyle(
            "ResumeSmall",
            parent=base["BodyText"],
            fontName=PDF_FONT_REGULAR,
            fontSize=6.35,
            leading=7.4,
            textColor=colors.HexColor(PDF_BODY),
            spaceAfter=1.2,
            splitLongWords=True,
        ),
        "tiny": ParagraphStyle(
            "ResumeTiny",
            parent=base["BodyText"],
            fontName=PDF_FONT_REGULAR,
            fontSize=5.9,
            leading=6.8,
            textColor=colors.HexColor(PDF_BODY),
            splitLongWords=True,
        ),
    }


def _table(data, col_widths, *, header: bool = False, zebra: bool = True):
    from reportlab.lib import colors
    from reportlab.platypus import LongTable

    table = LongTable(data, colWidths=col_widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#F0B7BF")),
    ]
    if header:
        commands.extend(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(PDF_RED_DARK)),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, colors.HexColor(PDF_RED_DARK)),
            ]
        )
        if zebra and len(data) > 1:
            commands.append(("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FFF8F9")]))
    elif zebra:
        commands.append(("ROWBACKGROUNDS", (0, 0), (-1, -1), [colors.white, colors.HexColor("#FFF8F9")]))
    table.setStyle(commands)
    return table


def _section(story: list, title: str, styles: dict, *, count: int | None = None) -> None:
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import HRFlowable, KeepTogether, Spacer

    label = title if count is None else f"{title} ({count})"
    story.append(
        KeepTogether(
            [
                _paragraph(label, styles["section"], linkify=False),
                HRFlowable(
                    width="100%",
                    thickness=0.7,
                    color=colors.HexColor(PDF_RED),
                    spaceBefore=0,
                    spaceAfter=0.05 * inch,
                ),
            ]
        )
    )
    story.append(Spacer(1, 0.015 * inch))


def _record_flow(title: str, styles: dict, details: list[str] | None = None, *, note: str | None = None):
    flow = [_paragraph(title, styles["record_title"])]
    if note:
        flow.append(_paragraph(note, styles["small"]))
    for detail in details or []:
        flow.append(_paragraph(f"- {detail}", styles["body"]))
    return flow


def _links_text(item: dict, *, prefix: str = "Source") -> str:
    links = item.get("links", [])
    if not links:
        return ""
    return f"{prefix}: " + " | ".join(f"{link['label']} {link['url']}" for link in links)


def _record_flow_with_links(
    title: str,
    styles: dict,
    item: dict,
    details: list[str] | None = None,
    *,
    note: str | None = None,
):
    flow = _record_flow(title, styles, details, note=note)
    links = _links_text(item)
    if links:
        flow.append(_paragraph(links, styles["tiny"]))
    return flow


def _metric_card(label: str, value: str, note: str, styles: dict, *, note_url: str | None = None) -> list:
    return [
        _paragraph(label, styles["metric_label"], linkify=False),
        _paragraph(value, styles["metric_value"], linkify=False),
        _link_paragraph(note, note_url, styles["metric_note"]) if note_url else _paragraph(note, styles["metric_note"], linkify=False),
    ]


def _cover_page(story: list, payload: dict, styles: dict, provenance: dict) -> None:
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import HRFlowable, PageBreak, Spacer, TableStyle

    profile = payload["profile"]
    metrics = payload["metrics"]
    source_hash = provenance["source_manifest"]["sha256"]
    json_hash = provenance["resume_json"]["sha256"]
    resume_source_count = sum(
        len(payload[key])
        for key in ["education", "experience", "awards", "conferences", "media_outreach", "service", "art_uses"]
    )

    story.append(_paragraph("PUBLIC STRUCTURED CV", styles["cover_kicker"], linkify=False))
    story.append(_paragraph(f"{profile['name']}, {profile['credential']}", styles["cover_title"], linkify=False))
    story.append(_paragraph(f"{profile['headline']} | {profile['location']}", styles["subtitle"], linkify=False))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.5,
            color=colors.HexColor(PDF_RED),
            spaceBefore=0.05 * inch,
            spaceAfter=0.09 * inch,
        )
    )

    verify_rows = [
        [
            _paragraph("Verify", styles["table_header"], linkify=False),
            [
                _link_paragraph("resume/verify.html", VERIFY_URL, styles["repo"]),
                _paragraph("QR target, public hashes, source files, and artifact sizes.", styles["small"], linkify=False),
            ],
        ],
        [
            _paragraph("Source", styles["table_header"], linkify=False),
            [
                _paragraph(f"manifest sha256 {source_hash[:16]}", styles["repo"], linkify=False),
                _paragraph("resume/source.json + canonical data exports", styles["small"], linkify=False),
            ],
        ],
        [
            _paragraph("Output", styles["table_header"], linkify=False),
            [
                _paragraph(f"json sha256 {json_hash[:16]}", styles["repo"], linkify=False),
                _link_paragraph("data/resume.json", RESUME_JSON_URL, styles["small"]),
                _link_paragraph("resume/resume.pdf", RESUME_PDF_URL, styles["small"]),
            ],
        ],
    ]
    verify_table = _table(verify_rows, [0.82 * inch, 4.08 * inch], header=False, zebra=False)
    verify_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor(PDF_RED)),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor(PDF_RED_DARK)),
                ("BACKGROUND", (1, 0), (1, -1), colors.HexColor("#FFFDFD")),
                ("LINEBELOW", (0, 0), (-1, -1), 0.35, colors.HexColor("#F6CBD1")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    qr_panel = _table(
        [
            [_paragraph("Scan / Click", styles["metric_label"], linkify=False)],
            [_qr_flowable(VERIFY_URL, 1.78 * inch)],
            [_paragraph("resume/verify.html", styles["metric_note"], linkify=False)],
        ],
        [1.96 * inch],
        zebra=False,
    )
    qr_panel.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 1.0, colors.HexColor(PDF_RED)),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(PDF_RED_PALE)),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    dashboard = _table([[verify_table, qr_panel]], [5.0 * inch, 2.1 * inch], zebra=False)
    dashboard.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("INNERGRID", (0, 0), (-1, -1), 0, colors.white)]))
    story.append(dashboard)
    story.append(Spacer(1, 0.09 * inch))

    metric_table = _table(
        [
            [
                _metric_card("Curated Works", str(metrics["works"]), "data/works.json", styles, note_url="https://danielarifriedman.com/data/works.json"),
                _metric_card(
                    "Software Rows",
                    str(metrics["software_catalogued"]),
                    "data/software.json",
                    styles,
                    note_url="https://danielarifriedman.com/data/software.json",
                ),
                _metric_card(
                    "Scholar Metrics",
                    str(metrics["google_scholar"]["citations"]),
                    "Scholar profile",
                    styles,
                    note_url=metrics["google_scholar"]["profile_url"],
                ),
                _metric_card("Resume Records", str(resume_source_count), "verify page", styles, note_url=VERIFY_URL),
            ],
            [
                _metric_card("Source Hash", source_hash[:12], "source manifest", styles),
                _metric_card("JSON Hash", json_hash[:12], "data/resume.json", styles, note_url=RESUME_JSON_URL),
                _metric_card(
                    "PDF Hash",
                    "verify page",
                    "resume/verify.html",
                    styles,
                    note_url=VERIFY_URL,
                ),
                _metric_card("Footer QR", "every page", "resume/verify.html", styles, note_url=VERIFY_URL),
            ]
        ],
        [1.78 * inch, 1.78 * inch, 1.78 * inch, 1.76 * inch],
        zebra=False,
    )
    metric_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor(PDF_RED)),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor(PDF_RED)),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(PDF_RED_PALE)),
            ]
        )
    )
    story.append(metric_table)
    story.append(Spacer(1, 0.1 * inch))

    _section(story, "Source-to-Output Flow", styles)
    flow_rows = [
        [
            _paragraph("Inputs", styles["table_header"], linkify=False),
            _paragraph("Generated JSON", styles["table_header"], linkify=False),
            _paragraph("Public PDF + Verification", styles["table_header"], linkify=False),
        ],
        [
            [
                _link_paragraph("resume/source.json", "https://github.com/docxology/docxology/blob/main/resume/source.json", styles["repo"]),
                _link_paragraph("data/works.json", "https://danielarifriedman.com/data/works.json", styles["small"]),
                _link_paragraph("data/software.json", "https://danielarifriedman.com/data/software.json", styles["small"]),
                _paragraph(f"source sha256 {source_hash[:16]}", styles["cover_hash"], linkify=False),
            ],
            [
                _link_paragraph("data/resume.json", RESUME_JSON_URL, styles["repo"]),
                _paragraph(f"{provenance['resume_json']['bytes']:,} bytes", styles["small"], linkify=False),
                _paragraph(f"json sha256 {json_hash[:16]}", styles["cover_hash"], linkify=False),
            ],
            [
                _link_paragraph("resume/resume.pdf", RESUME_PDF_URL, styles["repo"]),
                _link_paragraph("resume/verify.html", VERIFY_URL, styles["small"]),
                _paragraph("PDF hash posted on verification page", styles["cover_hash"], linkify=False),
            ],
        ],
    ]
    story.append(_table(flow_rows, [2.45 * inch, 2.2 * inch, 2.45 * inch], header=True))
    story.append(Spacer(1, 0.08 * inch))

    _section(story, "Section Counts", styles)
    counts = [
        ("Education", len(payload["education"])),
        ("Experience", len(payload["experience"])),
        ("Awards", len(payload["awards"])),
        ("Conferences", len(payload["conferences"])),
        ("Media / Outreach", len(payload["media_outreach"])),
        ("Service", len(payload["service"])),
        ("Art Uses", len(payload["art_uses"])),
    ]
    story.append(
        _table(
            [
                [_paragraph(name, styles["record_title"], linkify=False), _paragraph(str(count), styles["date"], linkify=False)]
                for name, count in counts
            ],
            [5.95 * inch, 1.15 * inch],
        )
    )
    story.append(PageBreak())


def render_pdf(payload: dict, variant: str = "full", provenance: dict | None = None) -> bytes:
    from reportlab import rl_config
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.platypus import HRFlowable, PageBreak, SimpleDocTemplate, Spacer, TableStyle

    rl_config.invariant = 1
    _register_pdf_fonts()
    styles = _styles()
    story = []
    profile = payload["profile"]
    contact = payload["contact"]
    metrics = payload["metrics"]
    provenance = provenance or _provenance_base(payload, json_dumps(payload).encode("utf-8"))

    _cover_page(story, payload, styles, provenance)

    story.append(_paragraph(f"{profile['name']}, {profile['credential']}", styles["title"], linkify=False))
    story.append(_paragraph(f"{profile['headline']} | {profile['location']}", styles["subtitle"], linkify=False))

    contact_rows = [
        [
            _label_value("Email", contact["email"], styles["contact"]),
            _label_value("Sites", contact["personal_sites"], styles["contact"]),
        ],
        [
            _label_value("GitHub", contact["github"], styles["contact"]),
            _label_value("LinkedIn", contact["linkedin"], styles["contact"]),
        ],
        [
            _label_value("Scholar", contact["google_scholar"], styles["contact"]),
            _label_value("ORCID", contact["orcid"], styles["contact"]),
        ],
        [
            _label_value("Keybase / ENS", f"{contact['keybase']} / {contact['ens']}", styles["contact"]),
            _label_value("Art", contact["art_portfolio"], styles["contact"]),
        ],
    ]
    contact_table = _table(contact_rows, [3.65 * inch, 3.65 * inch], zebra=False)
    contact_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor(PDF_RED)),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FFFDFD")),
                ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#F6CBD1")),
            ]
        )
    )
    story.append(contact_table)
    story.append(
        HRFlowable(
            width="100%",
            thickness=1.1,
            color=colors.HexColor(PDF_RED),
            spaceBefore=0.08 * inch,
            spaceAfter=0.08 * inch,
        )
    )

    metric_rows = [
        [
            [
                _paragraph("Curated Works", styles["metric_label"], linkify=False),
                _paragraph(str(metrics["works"]), styles["metric_value"], linkify=False),
                _paragraph("from data/works.json", styles["metric_note"], linkify=False),
            ],
            [
                _paragraph("Software Rows", styles["metric_label"], linkify=False),
                _paragraph(str(metrics["software_catalogued"]), styles["metric_value"], linkify=False),
                _paragraph(
                    f"{metrics['owned_software_catalogued']} owned + {metrics['aii_software_catalogued']} AII",
                    styles["metric_note"],
                    linkify=False,
                ),
            ],
            [
                _paragraph("Scholar Citations", styles["metric_label"], linkify=False),
                _paragraph(str(metrics["google_scholar"]["citations"]), styles["metric_value"], linkify=False),
                _paragraph(
                    f"h {metrics['google_scholar']['h_index']} / i10 {metrics['google_scholar']['i10_index']} as of {metrics['google_scholar']['as_of']}",
                    styles["metric_note"],
                    linkify=False,
                ),
            ],
        ]
    ]
    metric_table = _table(metric_rows, [2.4 * inch, 2.45 * inch, 2.45 * inch], zebra=False)
    metric_table.setStyle(
        TableStyle(
            [
                ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor(PDF_RED)),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor(PDF_RED)),
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(PDF_RED_PALE)),
            ]
        )
    )
    story.append(metric_table)
    story.append(Spacer(1, 0.06 * inch))
    story.append(
        _paragraph(
            f"Variant: {variant}. Generated: {payload['generated_at']}. Current public metrics: "
            f"{metrics['works']} curated works; {metrics['software_catalogued']} catalogued software repositories "
            f"({metrics['owned_software_catalogued']} owned + {metrics['aii_software_catalogued']} AII); "
            f"{metrics['google_scholar']['citations']} Google Scholar citations, "
            f"h-index {metrics['google_scholar']['h_index']}, i10-index {metrics['google_scholar']['i10_index']} "
            f"as of {metrics['google_scholar']['as_of']}. GitHub inventory: "
            f"{metrics['github_inventory']['docxology']} docxology + "
            f"{metrics['github_inventory']['ActiveInferenceInstitute']} AII public repositories "
            f"({metrics['github_inventory']['primary_total']} primary, {metrics['github_inventory']['forks']} forks).",
            styles["body"],
        )
    )

    _section(story, "Summary", styles)
    story.append(_paragraph(profile["summary"], styles["body"], linkify=False))

    education = filter_items(payload["education"], variant)
    _section(story, "Education", styles, count=len(education))
    story.append(
        _table(
            [
                [
                    _paragraph(date_range(item), styles["date"], linkify=False),
                    _record_flow_with_links(
                        f"{item['degree']} | {item['institution']} | {item['location']}",
                        styles,
                        item,
                        item.get("details", []),
                    ),
                ]
                for item in education
            ],
            [1.08 * inch, 6.22 * inch],
        )
    )

    experience = filter_items(payload["experience"], variant)
    _section(story, "Experience", styles, count=len(experience))
    story.append(
        _table(
            [
                [
                    _paragraph(date_range(item), styles["date"], linkify=False),
                    _record_flow_with_links(
                        f"{item['workplace']} | {', '.join(item['roles'])}",
                        styles,
                        item,
                        [item["description"]],
                        note=item["category"],
                    ),
                ]
                for item in experience
            ],
            [1.08 * inch, 6.22 * inch],
        )
    )

    awards = filter_items(payload["awards"], variant)
    _section(story, "Awards and Fellowships", styles, count=len(awards))
    story.append(
        _table(
            [
                [_paragraph("Year", styles["table_header"], linkify=False), _paragraph("Award", styles["table_header"], linkify=False), _paragraph("Details", styles["table_header"], linkify=False)]
            ]
            + [
                [
                    _paragraph(str(item["year"]), styles["date"], linkify=False),
                    _record_flow_with_links(item["name"], styles, item),
                    _paragraph(item["details"], styles["body"]),
                ]
                for item in awards
            ],
            [0.55 * inch, 2.25 * inch, 4.5 * inch],
            header=True,
        )
    )

    works = filtered_works(payload["works"], variant)
    story.append(PageBreak())
    _section(story, "Works and Publications", styles, count=len(works))
    story.append(
        _table(
            [
                [
                    _paragraph("#", styles["table_header"], linkify=False),
                    _paragraph("Year", styles["table_header"], linkify=False),
                    _paragraph("Type", styles["table_header"], linkify=False),
                    _paragraph("Title and Venue", styles["table_header"], linkify=False),
                    _paragraph("Link", styles["table_header"], linkify=False),
                ]
            ]
            + [
                [
                    _paragraph(f"{work['num']:03d}", styles["tiny"], linkify=False),
                    _paragraph(str(work["year"]), styles["tiny"], linkify=False),
                    _paragraph(work["type"], styles["tiny"], linkify=False),
                    _record_flow(f"{work['title']} | {work['venue']}", styles),
                    _paragraph(work.get("doi") or work.get("url") or "", styles["tiny"]),
                ]
                for work in works
            ],
            [0.35 * inch, 0.42 * inch, 0.68 * inch, 4.3 * inch, 1.55 * inch],
            header=True,
        )
    )

    software = filtered_software(payload["software"], variant)
    story.append(PageBreak())
    _section(story, "Software", styles, count=len(software))
    story.append(
        _table(
            [
                [
                    _paragraph("Repository", styles["table_header"], linkify=False),
                    _paragraph("Stack", styles["table_header"], linkify=False),
                    _paragraph("Description and Source Links", styles["table_header"], linkify=False),
                ]
            ]
            + [
                [
                    [
                        _paragraph(f"{row['owner']}/{row['name']}", styles["repo"], linkify=False),
                        _paragraph(row["url"], styles["tiny"]),
                    ],
                    _paragraph(row.get("language") or "unspecified", styles["tiny"], linkify=False),
                    [
                        _paragraph(row.get("description", ""), styles["body"]),
                        *(
                            [
                                _paragraph(
                                    " | ".join(
                                        part
                                        for part in [
                                            f"paper: {row['paper_path']}" if row.get("paper_path") else "",
                                            f"zenodo: {row['zenodo_url']}" if row.get("zenodo_url") else "",
                                        ]
                                        if part
                                    ),
                                    styles["small"],
                                )
                            ]
                            if row.get("paper_path") or row.get("zenodo_url")
                            else []
                        ),
                    ],
                ]
                for row in software
            ],
            [2.1 * inch, 0.58 * inch, 4.62 * inch],
            header=True,
        )
    )

    conferences = filter_items(payload["conferences"], variant)
    _section(story, "Conferences, Posters, Seminars, Workshops", styles, count=len(conferences))
    story.append(
        _table(
            [
                [
                    _paragraph(str(item["year"]), styles["date"], linkify=False),
                    _record_flow_with_links(
                        f"{item['title']} | {item['event']}",
                        styles,
                        item,
                        [" ".join(part for part in [item["type"], item.get("details", ""), item.get("date", "")] if part)],
                    ),
                ]
                for item in conferences
            ],
            [0.62 * inch, 6.68 * inch],
        )
    )

    media = filter_items(payload["media_outreach"], variant)
    _section(story, "Science Engagement, Outreach, Quotes, Articles", styles, count=len(media))
    story.append(
        _table(
            [
                [
                    _paragraph(str(item["year"]), styles["date"], linkify=False),
                    _record_flow_with_links(
                        item["name"],
                        styles,
                        item,
                        [" | ".join(part for part in [item["type"], item.get("source", ""), item.get("details", "")] if part)],
                    ),
                ]
                for item in media
            ],
            [0.62 * inch, 6.68 * inch],
        )
    )

    service = filter_items(payload["service"], variant)
    _section(story, "Professional Participation, Engagement, and Service", styles, count=len(service))
    story.append(
        _table(
            [
                [
                    _paragraph(date_range(item), styles["date"], linkify=False),
                    _record_flow_with_links(f"{item['group']} | {item['type']}", styles, item, [item["description"]]),
                ]
                for item in service
            ],
            [1.08 * inch, 6.22 * inch],
        )
    )

    if variant == "full":
        _section(story, "Art Portfolio and Uses", styles, count=len(payload["art_uses"]))
        story.append(
            _table(
                [
                    [
                        _paragraph(str(item["year"]) if item["year"] is not None else "All", styles["date"], linkify=False),
                        _record_flow_with_links(item["name"], styles, item, [item["description"]]),
                    ]
                    for item in payload["art_uses"]
                ],
                [0.62 * inch, 6.68 * inch],
            )
        )

    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.7 * inch,
        title=f"Daniel Ari Friedman {variant} CV",
        author="Daniel Ari Friedman",
        subject="Structured resume generated from docxology repository data",
    )
    footer = _page_footer_factory(provenance)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return buf.getvalue()


def _html_escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def _html_href(value: object) -> str:
    """Allow only links appropriate for generated public CV HTML."""
    target = str(value or "").strip()
    if re.match(r"^(?:https?://|mailto:|/)", target):
        return _html_escape(target)
    return ""


def _html_link(label: object, target: object) -> str:
    href = _html_href(target)
    label_html = _html_escape(label)
    return f'<a href="{href}">{label_html}</a>' if href else label_html


def _html_links(item: dict) -> str:
    rendered = []
    for link in item.get("links", []):
        if not isinstance(link, dict):
            continue
        label = str(link.get("label") or "Source")
        target = str(link.get("url") or "")
        if target.startswith("10."):
            target = f"https://doi.org/{target}"
        if _html_href(target):
            rendered.append(_html_link(label, target))
    return " <span aria-hidden=\"true\">·</span> ".join(rendered)


def _html_contact_value(value: object, *, mailto: bool = False) -> str:
    values = value if isinstance(value, list) else [value]
    rendered = []
    for raw in values:
        text = str(raw or "")
        target = f"mailto:{text}" if mailto else text
        rendered.append(_html_link(text, target))
    return " <span aria-hidden=\"true\">·</span> ".join(rendered)


def _html_record(title: object, details: list[object], links: str = "", *, date: object = "") -> str:
    detail_html = "".join(f"<p>{_html_escape(detail)}</p>" for detail in details if str(detail or "").strip())
    date_html = f'<p class="record-date">{_html_escape(date)}</p>' if str(date or "").strip() else ""
    links_html = f'<p class="record-links">{links}</p>' if links else ""
    return f"<li><article>{date_html}<h3>{_html_escape(title)}</h3>{detail_html}{links_html}</article></li>"


def render_resume_html(payload: dict, variant: str = "full") -> bytes:
    """Render a no-JavaScript, semantic CV view for screen readers and crawlers."""
    if variant not in VARIANTS:
        raise ValueError(f"unknown variant: {variant}")
    profile = payload["profile"]
    contact = payload["contact"]
    metrics = payload["metrics"]
    sections: list[str] = []

    education = filter_items(payload["education"], variant)
    education_rows = []
    for item in education:
        title = f"{item['degree']} — {item['institution']} — {item['location']}"
        education_rows.append(_html_record(title, item.get("details", []), _html_links(item), date=date_range(item)))
    sections.append(
        f'<section aria-labelledby="education"><h2 id="education">Education <span>({len(education)})</span></h2>'
        f'<ol class="record-list">{"".join(education_rows)}</ol></section>'
    )
    experience = filter_items(payload["experience"], variant)
    experience_rows = []
    for item in experience:
        title = f"{item['workplace']} — {', '.join(item['roles'])}"
        details = [item.get("description", ""), item.get("category", "")]
        experience_rows.append(_html_record(title, details, _html_links(item), date=date_range(item)))
    sections.append(
        f'<section aria-labelledby="experience"><h2 id="experience">Experience <span>({len(experience)})</span></h2>'
        f'<ol class="record-list">{"".join(experience_rows)}</ol></section>'
    )
    awards = filter_items(payload["awards"], variant)
    award_rows = [
        _html_record(item["name"], [item.get("details", "")], _html_links(item), date=item.get("year"))
        for item in awards
    ]
    sections.append(
        f'<section aria-labelledby="awards"><h2 id="awards">Awards and Fellowships <span>({len(awards)})</span></h2>'
        f'<ol class="record-list">{"".join(award_rows)}</ol></section>'
    )
    works = filtered_works(payload["works"], variant)
    work_items = []
    for work in works:
        target = work.get("doi") or work.get("url") or ""
        if str(target).startswith("10."):
            target = f"https://doi.org/{target}"
        title = _html_link(work.get("title", "Untitled work"), target)
        venue = f" <span class=\"muted\">· {_html_escape(work.get('venue', ''))}</span>" if work.get("venue") else ""
        work_items.append(
            f'<li><span class="record-date">[{_html_escape(work.get("num", ""))}] {_html_escape(work.get("year", ""))}</span> '
            f'<span class="work-type">{_html_escape(work.get("type", "Work"))}</span> {title}{venue}</li>'
        )
    sections.append(
        f'<section aria-labelledby="works"><h2 id="works">Works and Publications <span>({len(works)})</span></h2>'
        f'<ol class="works-list">{"".join(work_items)}</ol></section>'
    )
    software = filtered_software(payload["software"], variant)
    software_items = []
    link_separator = ' <span aria-hidden="true">·</span> '
    for row in software:
        links = [_html_link(row.get("owner", "") + "/" + row.get("name", ""), row.get("url", ""))]
        if row.get("paper_path"):
            links.append(_html_link("paper", f"/{row['paper_path']}"))
        if row.get("zenodo_url"):
            links.append(_html_link("Zenodo", row["zenodo_url"]))
        software_items.append(
            f'<li><article><h3>{link_separator.join(links)}</h3>'
            f'<p>{_html_escape(row.get("description", ""))}</p><p class="record-links">'
            f'{_html_escape(row.get("language") or "Unspecified")}</p></article></li>'
        )
    sections.append(
        f'<section aria-labelledby="software"><h2 id="software">Software <span>({len(software)})</span></h2>'
        f'<ul class="record-list">{"".join(software_items)}</ul></section>'
    )
    for key, heading in (
        ("conferences", "Conferences, Posters, Seminars, and Workshops"),
        ("media_outreach", "Science Engagement, Outreach, Quotes, and Articles"),
        ("service", "Professional Participation, Engagement, and Service"),
    ):
        items = filter_items(payload[key], variant)
        rows = []
        for item in items:
            title = item.get("title") or item.get("name") or item.get("description") or "Record"
            details = [item.get("event", ""), item.get("source", ""), item.get("type", ""), item.get("details", ""), item.get("description", "")]
            group = item.get("group", "")
            if group:
                title = f"{group} — {title}"
            rows.append(_html_record(title, details, _html_links(item), date=item.get("year") or date_range(item)))
        sections.append(
            f'<section aria-labelledby="{key}"><h2 id="{key}">{_html_escape(heading)} <span>({len(items)})</span></h2>'
            f'<ol class="record-list">{"".join(rows)}</ol></section>'
        )
    if variant == "full":
        items = payload["art_uses"]
        art_rows = [
            _html_record(item.get("name", ""), [item.get("description", "")], _html_links(item), date=item.get("year") or "All")
            for item in items
        ]
        sections.append(
            f'<section aria-labelledby="art"><h2 id="art">Art Portfolio and Uses <span>({len(items)})</span></h2>'
            f'<ol class="record-list">{"".join(art_rows)}</ol></section>'
        )

    structured_data = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "ProfilePage",
            "name": f"{profile['name']} — Public Structured CV",
            "url": RESUME_HTML_URL,
            "dateModified": payload["generated_at"],
            "mainEntity": {"@type": "Person", "name": profile["name"], "url": "https://danielarifriedman.com/"},
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{_html_escape(profile['name'])} — Public Structured CV</title>
    <meta name="description" content="Accessible, source-verified public curriculum vitae for {_html_escape(profile['name'])}.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{RESUME_HTML_URL}">
    <meta property="og:type" content="profile">
    <meta property="og:title" content="{_html_escape(profile['name'])} — Public Structured CV">
    <meta property="og:description" content="Accessible, source-verified public curriculum vitae.">
    <meta property="og:url" content="{RESUME_HTML_URL}">
    <meta property="og:site_name" content="Daniel Ari Friedman">
    <meta property="og:image" content="https://danielarifriedman.com/og-image.jpg">
    <meta property="og:image:alt" content="Daniel Ari Friedman public profile">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="https://danielarifriedman.com/og-image.jpg">
    <meta name="twitter:image:alt" content="Daniel Ari Friedman public profile">
{HEAD_EXTRAS}
    <link rel="stylesheet" href="/style.css?v=newspaper-glitch-20260530c">
    <script type="application/ld+json">{structured_data}</script>
    <style>
        :root {{ color-scheme: dark; }}
        .cv-shell {{ width: min(1120px, calc(100% - 2rem)); margin: 0 auto; padding: 2rem 0 4rem; }}
        .cv-hero {{ border-block: 4px double var(--border-color, #555); padding: 2rem 0 1.25rem; }}
        .cv-hero h1 {{ margin: 0; font-size: clamp(2.2rem, 7vw, 5rem); line-height: .95; }}
        .cv-hero p {{ max-width: 820px; color: var(--text-secondary, #bbb); }}
        .cv-tools, .cv-contact, .cv-metrics {{ display: grid; gap: .75rem; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); margin: 1rem 0; }}
        .cv-card {{ border: 1px solid var(--border-color, #555); padding: 1rem; background: rgba(255,255,255,.03); }}
        .cv-card h2, .cv-card h3 {{ margin-top: 0; }}
        .cv-card a, .record-links a {{ overflow-wrap: anywhere; }}
        .cv-metric {{ font-size: 1.7rem; font-weight: 700; display: block; }}
        .record-list, .works-list {{ padding-left: 1.5rem; }}
        .record-list > li, .works-list > li {{ margin: 0 0 1rem; }}
        .record-list article {{ border-left: 2px solid var(--accent-color, #e33); padding-left: .8rem; }}
        .record-list h3 {{ margin: 0 0 .25rem; }}
        .record-list p {{ margin: .25rem 0; }}
        .record-date, .work-type {{ color: var(--accent-color, #f66); font-weight: 700; }}
        .muted {{ color: var(--text-secondary, #aaa); }}
        .cv-footer {{ border-top: 1px solid var(--border-color, #555); margin-top: 2rem; padding-top: 1rem; color: var(--text-secondary, #bbb); }}
        @media (prefers-reduced-motion: reduce) {{ *, *::before, *::after {{ scroll-behavior: auto !important; transition: none !important; }} }}
    </style>
</head>
<body>
    <a class="skip-link" href="#main">Skip to main content</a>
    <nav aria-label="Main navigation"><a class="nav-logo" href="/">Daniel Ari Friedman</a><div class="nav-links"><a href="/publications.html">Publications</a><a href="/software.html">Software</a><a href="/resume/resume.pdf">PDF</a><a href="/resume/verify.html">Verify</a></div></nav>
    <main id="main" class="cv-shell">
        <header class="cv-hero">
            <p><strong>PUBLIC STRUCTURED CV · { _html_escape(variant) }</strong></p>
            <h1>{_html_escape(profile['name'])}, {_html_escape(profile['credential'])}</h1>
            <p>{_html_escape(profile['headline'])} · {_html_escape(profile['location'])}</p>
            <p>{_html_escape(profile['summary'])}</p>
        </header>
        <section aria-labelledby="cv-links"><h2 id="cv-links">CV formats and verification</h2><div class="cv-tools">
            <p class="cv-card"><a href="/resume/resume.pdf">Download accessible-text PDF</a></p><p class="cv-card"><a href="/data/resume.json">Structured JSON</a></p><p class="cv-card"><a href="/resume/full.txt">Plain-text CV</a></p><p class="cv-card"><a href="/resume/verify.html">Verify source and artifact hashes</a></p>
        </div></section>
        <section aria-labelledby="contact"><h2 id="contact">Contact and identifiers</h2><div class="cv-contact">
            <p class="cv-card"><strong>Email</strong><br>{_html_contact_value(contact.get('email', []), mailto=True)}</p>
            <p class="cv-card"><strong>Sites</strong><br>{_html_contact_value(contact.get('personal_sites', []))}</p>
            <p class="cv-card"><strong>Profiles</strong><br>{_html_link('GitHub', contact.get('github'))}<br>{_html_link('ORCID', 'https://orcid.org/' + str(contact.get('orcid', '')))}<br>{_html_link('Google Scholar', contact.get('google_scholar'))}</p>
        </div></section>
        <section aria-labelledby="metrics"><h2 id="metrics">Current public metrics</h2><div class="cv-metrics">
            <p class="cv-card"><span class="cv-metric">{metrics['works']}</span>curated works</p><p class="cv-card"><span class="cv-metric">{metrics['software_catalogued']}</span>catalogued software rows</p><p class="cv-card"><span class="cv-metric">{metrics['github_inventory']['docxology']} + {metrics['github_inventory']['ActiveInferenceInstitute']}</span>public GitHub repositories by account</p><p class="cv-card"><span class="cv-metric">{metrics['google_scholar']['citations']}</span>Google Scholar citations <small>(as of {_html_escape(metrics['google_scholar']['as_of'])})</small></p>
        </div><p>Counts are generated from canonical exports. GitHub inventory generated {_html_escape(metrics['github_inventory']['generated_at'])}; Scholar metrics remain explicitly dated.</p></section>
        {''.join(sections)}
        <footer class="cv-footer"><p>Generated {_html_escape(payload['generated_at'])}. Source manifest: <code>{_html_escape(payload['integrity']['source_manifest']['sha256'])}</code>.</p><p>PDF rendering provides selectable text, embedded fonts, link annotations, language metadata, and deterministic hashes. It does not claim a fully tagged PDF/UA structure; use this semantic HTML view or plain text for maximum assistive-technology compatibility.</p></footer>
    </main>
</body>
</html>
"""
    return content.encode("utf-8")


def render_verify_html(payload: dict, provenance: dict) -> bytes:
    metrics = payload["metrics"]
    github_metrics = metrics["github_inventory"]
    generator = provenance.get("generator", {})
    source_rows = "\n".join(
        f"""                    <tr>
                        <td>{_html_escape(row["path"])}</td>
                        <td>{row["bytes"]:,}</td>
                        <td><code>{_html_escape(row["sha256"])}</code></td>
                    </tr>"""
        for row in provenance["source_manifest"]["files"]
    )
    section_counts = [
        ("Education", len(payload["education"])),
        ("Experience", len(payload["experience"])),
        ("Awards", len(payload["awards"])),
        ("Conferences", len(payload["conferences"])),
        ("Media / Outreach", len(payload["media_outreach"])),
        ("Service", len(payload["service"])),
        ("Art Uses", len(payload["art_uses"])),
    ]
    count_cards = "\n".join(
        f"""                <article class="metric-card">
                    <span>{_html_escape(label)}</span>
                    <strong>{count}</strong>
                </article>"""
        for label, count in [
            ("Curated works", metrics["works"]),
            ("Software rows", metrics["software_catalogued"]),
            ("Scholar citations", metrics["google_scholar"]["citations"]),
            ("Public GitHub repositories", github_metrics["public"]),
            *section_counts,
        ]
    )
    source_hash = provenance["source_manifest"]["sha256"]
    json_hash = provenance["resume_json"]["sha256"]
    pdf_hash = provenance.get("resume_pdf", {}).get("sha256", "N/A (reportlab not installed)")
    content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Resume Verification - Daniel Ari Friedman</title>
    <meta name="description" content="Hashes, source manifest, file sizes, and public links for Daniel Ari Friedman's generated structured resume/CV.">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="{VERIFY_URL}">
    <meta property="og:type" content="website">
    <meta property="og:title" content="Resume Verification - Daniel Ari Friedman">
    <meta property="og:description" content="Hashes, source manifest, file sizes, and public links for Daniel Ari Friedman's generated structured resume/CV.">
    <meta property="og:url" content="{VERIFY_URL}">
    <meta property="og:site_name" content="Daniel Ari Friedman">
    <meta property="og:image" content="https://danielarifriedman.com/og-image.jpg">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
{HEAD_EXTRAS}
    <link rel="stylesheet" href="/style.css?v=newspaper-glitch-20260530c">
    <style>
        :root {{
            --resume-red: #ff0000;
            --resume-red-dark: #ff0000;
            --resume-paper: #0b0b0b;
            --resume-panel: #111111;
            --resume-ink: #f2f2f2;
            --resume-muted: #b8b8b8;
            --resume-rule: rgba(255,255,255,.22);
        }}
        body {{ background: var(--bg-primary, #050505); color: var(--resume-ink); }}
        .verify-shell {{ width: min(1120px, calc(100% - 2rem)); margin: 0 auto; padding: 2rem 0 3rem; }}
        .verify-hero {{ border-top: 4px double var(--resume-rule); border-bottom: 4px double var(--resume-rule); padding: 2rem 0 1rem; }}
        .verify-hero h1 {{ color: var(--resume-ink); font-size: clamp(2rem, 6vw, 4.5rem); line-height: .95; margin: 0; }}
        .verify-hero p {{ color: var(--resume-muted); max-width: 760px; font-size: 1rem; }}
        .hash-grid, .metric-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: .8rem; margin: 1rem 0; }}
        .hash-card, .metric-card, .flow-card {{ border: 1px solid var(--resume-rule); background: var(--resume-panel); padding: .85rem; border-radius: 3px; box-shadow: none; }}
        .hash-card span, .metric-card span {{ color: var(--resume-red); display: block; font-size: .76rem; font-weight: 700; text-transform: uppercase; }}
        .hash-card code {{ color: var(--resume-ink); overflow-wrap: anywhere; font-size: .78rem; }}
        .metric-card strong {{ display: block; font-size: 2rem; line-height: 1.1; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 1rem; }}
        th {{ background: #141414; color: var(--resume-ink); text-align: left; border-bottom: 2px solid var(--resume-red); }}
        th, td {{ border: 1px solid var(--resume-rule); padding: .55rem; vertical-align: top; }}
        td code {{ overflow-wrap: anywhere; }}
        .flow-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: .8rem; }}
        .flow-card h3 {{ margin: 0 0 .3rem; color: var(--resume-ink); }}
        a {{ color: var(--resume-red); text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 2px; }}
    </style>
</head>
<body>
    <a class="skip-link" href="#main">Skip to main content</a>
    <nav role="navigation" aria-label="Main navigation"><a href="/" class="nav-logo">Daniel Ari Friedman</a><div class="nav-links"><a href="/publications.html">Publications</a><a href="/resume/resume.pdf">Resume PDF</a><a href="/data/agent-index.json">Agent Map</a></div></nav>
    <main id="main" class="verify-shell">
        <header class="verify-hero">
            <p><strong>Public Structured CV Verification</strong></p>
            <h1>Resume Verification</h1>
            <p>Generated {payload["generated_at"]}. This page records the input source manifest, generated JSON hash, final PDF hash, counts, sizes, and public artifact links. The accessible HTML CV is available at <a href="/resume/resume.html">/resume/resume.html</a>.</p>
        </header>

        <section aria-labelledby="artifacts">
            <h2 id="artifacts">Artifacts</h2>
            <div class="flow-grid">
                <article class="flow-card"><h3>Structured JSON</h3><p><a href="/data/resume.json">/data/resume.json</a></p><p>{provenance["resume_json"]["bytes"]:,} bytes</p></article>
                <article class="flow-card"><h3>Accessible HTML CV</h3><p><a href="/resume/resume.html">/resume/resume.html</a></p><p>No JavaScript required</p></article>
                <article class="flow-card"><h3>Public PDF</h3><p><a href="/resume/resume.pdf">/resume/resume.pdf</a></p><p>{provenance.get("resume_pdf", {}).get("bytes", 0):,} bytes</p></article>
                <article class="flow-card"><h3>Verification URL</h3><p><a href="/resume/verify.html">/resume/verify.html</a></p><p>{VERIFY_URL}</p></article>
            </div>
        </section>

        <section aria-labelledby="hashes">
            <h2 id="hashes">Hashes</h2>
            <div class="hash-grid">
                <article class="hash-card"><span>Source Manifest SHA-256</span><code>{_html_escape(source_hash)}</code></article>
                <article class="hash-card"><span>data/resume.json SHA-256</span><code>{_html_escape(json_hash)}</code></article>
                <article class="hash-card"><span>resume/resume.pdf SHA-256</span><code>{_html_escape(pdf_hash)}</code></article>
            </div>
        </section>

        <section aria-labelledby="counts">
            <h2 id="counts">Structured Counts</h2>
            <div class="metric-grid">
{count_cards}
            </div>
        </section>

        <section aria-labelledby="flow">
            <h2 id="flow">Source-to-Output Flow</h2>
            <div class="flow-grid">
                <article class="flow-card"><h3>Inputs</h3><p>resume/source.json + canonical public data exports.</p><p><code>{_html_escape(source_hash[:16])}</code></p></article>
                <article class="flow-card"><h3>Merged Payload</h3><p>data/resume.json</p><p><code>{_html_escape(json_hash[:16])}</code></p></article>
                <article class="flow-card"><h3>Rendered Artifacts</h3><p>resume/resume.html + resume/resume.pdf + verification.</p><p><code>{_html_escape(pdf_hash[:16])}</code></p></article>
            </div>
            <p>Generator: <code>{_html_escape(generator.get("name", "unknown"))}</code>, schema {_html_escape(generator.get("schema_version", "unknown"))}; ReportLab {_html_escape(generator.get("reportlab_version", "unknown"))}. Source manifest matches the payload: <strong>{"yes" if provenance.get("source_manifest_matches_payload") else "no"}</strong>.</p>
            <p>Accessibility: the HTML CV is semantic, keyboard-navigable, and JavaScript-free. The PDF provides selectable text, embedded fonts, link annotations, and language metadata; it does not claim fully tagged PDF/UA structure.</p>
        </section>

        <section aria-labelledby="sources">
            <h2 id="sources">Source Files</h2>
            <table>
                <caption>Every file hashed into the CV source manifest</caption>
                <thead><tr><th scope="col">Path</th><th scope="col">Bytes</th><th scope="col">SHA-256</th></tr></thead>
                <tbody>
{source_rows}
                </tbody>
            </table>
        </section>
    </main>
</body>
</html>
"""
    return content.encode("utf-8")


def tracked_outputs(payload: dict) -> dict[Path, bytes]:
    json_bytes = json_dumps(payload).encode("utf-8")
    provenance = _provenance_base(payload, json_bytes)
    outputs: dict[Path, bytes] = {JSON_OUT: json_bytes}
    for variant, path in TXT_OUTPUTS.items():
        outputs[path] = render_text(payload, variant).encode("utf-8")
    try:
        pdf_bytes = render_pdf(payload, "full", provenance)
        provenance = {**provenance, "resume_pdf": {"bytes": len(pdf_bytes), "sha256": _sha256_bytes(pdf_bytes)}}
        outputs[FULL_PDF] = pdf_bytes
    except ImportError:
        import sys
        print("warning: reportlab not installed, skipping PDF check", file=sys.stderr)
    outputs[FULL_HTML] = render_resume_html(payload, "full")
    outputs[VERIFY_OUT] = render_verify_html(payload, provenance)
    return outputs


def selected_outputs(payload: dict, variant: str, fmt: str) -> dict[Path, bytes]:
    if fmt == "all":
        return tracked_outputs(payload)
    if fmt == "json":
        return {JSON_OUT: json_dumps(payload).encode("utf-8")}
    if fmt == "txt":
        return {TXT_OUTPUTS[variant]: render_text(payload, variant).encode("utf-8")}
    if fmt == "pdf":
        target = FULL_PDF if variant == "full" else RESUME_DIR / f"{variant}.pdf"
        json_bytes = json_dumps(payload).encode("utf-8")
        return {target: render_pdf(payload, variant, _provenance_base(payload, json_bytes))}
    if fmt == "html":
        return {FULL_HTML: render_resume_html(payload, variant)}
    raise ValueError(f"unknown format: {fmt}")


def check_outputs(outputs: dict[Path, bytes]) -> list[str]:
    stale = []
    for path, content in outputs.items():
        if not path.exists() or path.read_bytes() != content:
            stale.append(str(path.relative_to(REPO_ROOT)))
    return stale


def write_outputs(outputs: dict[Path, bytes]) -> None:
    for path, content in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Regenerate all tracked resume outputs")
    parser.add_argument("--check", action="store_true", help="Fail if tracked resume outputs are stale")
    parser.add_argument("--variant", choices=VARIANTS, default="full")
    parser.add_argument("--format", choices=("json", "txt", "pdf", "html", "all"), default="all")
    args = parser.parse_args()

    generated_at = existing_generated_at() if args.check else None
    payload = build_resume_payload(generated_at or generated_timestamp(), REPO_ROOT)
    outputs = tracked_outputs(payload) if args.all or args.check else selected_outputs(payload, args.variant, args.format)

    if args.check:
        stale = check_outputs(outputs)
        if stale:
            raise SystemExit("Stale resume outputs: " + ", ".join(stale))
        print(f"checked resume outputs ({len(outputs)} files)")
        return

    write_outputs(outputs)
    print(f"wrote resume outputs ({len(outputs)} files)")


if __name__ == "__main__":
    main()
