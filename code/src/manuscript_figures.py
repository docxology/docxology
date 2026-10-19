"""Declared, offline explanatory diagrams for the repository-methods draft.

These diagrams describe source-backed contracts, not measured results. Assets
exist only in an explicit external render; the website generator writes none.
"""

from __future__ import annotations

import io
from pathlib import Path

FIGURES = {
    "system-context": "Source authority, generated views, and the bounded website.",
    "progressive-discovery": "Loading decisions for search, gallery, and publications.",
    "evidence-boundaries": "Different evidence supports different kinds of claims.",
    "release-path": "Payload, control metadata, deployment, and human review.",
}
PRODUCER = "repository-method-diagrams-v1"
SOURCE_TARGETS = {f"../output/figures/{name}.png": name for name in FIGURES}


def _draw(name: str) -> bytes:
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(1000, 570), invariant=1)
    navy, teal, pale, ink = "#123047", "#147d80", "#eaf4f4", "#213c4b"

    def text(x, y, value, size=17, color=ink, bold=False):
        c.setFillColor(HexColor(color))
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(x, y, value)

    def box(x, y, width, height, title, lines, fill=pale):
        c.setFillColor(HexColor(fill))
        c.roundRect(x, y, width, height, 10, fill=1, stroke=0)
        text(x + 16, y + height - 29, title, 18, teal, True)
        for i, line in enumerate(lines):
            text(x + 16, y + height - 61 - i * 25, line, 16)

    def arrow(x, y, x2, y2):
        c.setStrokeColor(HexColor(teal))
        c.setFillColor(HexColor(teal))
        c.setLineWidth(2.5)
        c.line(x, y, x2, y2)
        if x2 == x:
            c.line(x2 - 5, y2 + 8, x2, y2)
            c.line(x2 + 5, y2 + 8, x2, y2)
        else:
            c.line(x2 - 8, y2 - 5, x2, y2)
            c.line(x2 - 8, y2 + 5, x2, y2)

    c.setFillColor(HexColor("#ffffff"))
    c.rect(0, 0, 1000, 570, fill=1, stroke=0)
    c.setFillColor(HexColor(navy))
    c.rect(0, 478, 1000, 92, fill=1, stroke=0)
    titles = {
        "system-context": "A research archive with several public views",
        "progressive-discovery": "Load what the current interaction needs",
        "evidence-boundaries": "Evidence has a scope; checks are not interchangeable",
        "release-path": "Bind each published candidate to its own evidence",
    }
    text(28, 522, titles[name], 25, "#ffffff", True)
    text(28, 494, FIGURES[name], 16, "#a8e4df")
    if name == "system-context":
        box(
            28,
            264,
            286,
            177,
            "AUTHORED AUTHORITIES",
            [
                "Bibliography + work identities",
                "Software + resume sources",
                "Reviewed source observations",
            ],
        )
        box(
            359,
            264,
            282,
            177,
            "SHARED CONTRACTS",
            [
                "Parsers + permanent keys",
                "Ordered generation plan",
                "Independent no-write checks",
            ],
        )
        box(
            686,
            264,
            286,
            177,
            "PUBLIC VIEWS",
            [
                "Work + software landing pages",
                "Search + citation exports",
                "Human and agent interfaces",
            ],
        )
        arrow(320, 353, 352, 353)
        arrow(647, 353, 679, 353)
        box(
            28,
            83,
            454,
            133,
            "REPOSITORY ARCHIVE",
            [
                "Original documents and dated evidence",
                "Source custody and historical revisions",
            ],
        )
        box(
            518,
            83,
            454,
            133,
            "BOUNDED PAGES PROJECTION",
            [
                "Navigable current site and selected assets",
                "Pinned GitHub fallback for omitted objects",
            ],
        )
        arrow(500, 267, 500, 235)
        arrow(488, 150, 511, 150)
        text(
            28,
            45,
            "Observation -> review -> curated claim. Inventory alone is not endorsement.",
            16,
        )
    elif name == "progressive-discovery":
        text(28, 445, "SURFACE", 16, teal, True)
        text(205, 445, "INITIAL VIEW", 16, teal, True)
        text(480, 445, "TRIGGER", 16, teal, True)
        text(730, 445, "ADDITIONAL DATA", 16, teal, True)
        rows = [
            (
                "SEARCH",
                ["Compact preview"],
                ["Query or scope"],
                ["Core index; relevant text"],
            ),
            (
                "GALLERY",
                ["Compact full catalog", "Finite card batch"],
                ["Description / lightbox"],
                ["Artwork detail records"],
            ),
            (
                "PUBLICATIONS",
                ["Crawlable work rows", "Work catalog"],
                ["Nonempty search"],
                ["Abstract / keyword detail"],
            ),
        ]
        for i, (label, initial, trigger, detail) in enumerate(rows):
            y = 325 - i * 111
            text(28, y + 52, label, 17, navy, True)
            for x, width, title, lines in [
                (190, 235, "", initial),
                (465, 225, "", trigger),
                (730, 242, "", detail),
            ]:
                c.setFillColor(HexColor(pale))
                c.roundRect(x, y, width, 86, 8, fill=1, stroke=0)
                for j, line in enumerate(lines):
                    text(x + 12, y + 52 - j * 23, line, 16)
            arrow(430, y + 43, 458, y + 43)
            arrow(696, y + 43, 723, y + 43)
        text(
            28,
            58,
            "Late responses cannot restore an older query. Missing data exposes retry/fallback.",
            16,
        )
        text(
            28,
            30,
            "Native links and server-rendered content preserve discovery without JavaScript.",
            16,
        )
    elif name == "evidence-boundaries":
        text(28, 444, "EVIDENCE", 16, teal, True)
        text(302, 444, "SUPPORTS", 16, teal, True)
        text(658, 444, "DOES NOT ESTABLISH", 16, teal, True)
        rows = [
            (
                "Source identity + hashes",
                "Which bytes and revision",
                "Truth or complete extraction",
            ),
            (
                "Generation checks",
                "Source / projection agreement",
                "Fresh external observations",
            ),
            (
                "Browser tests",
                "Tested scenarios and runtime",
                "Every device or human approval",
            ),
            (
                "Deployment verification",
                "Listed routes and artifact contracts",
                "Every live response body",
            ),
            (
                "Human / editorial review",
                "Named review of stated scope",
                "Independent scientific replication",
            ),
        ]
        for i, (a, b, d) in enumerate(rows):
            y = 365 - i * 65
            c.setFillColor(HexColor(pale if i % 2 == 0 else "#f6f9fa"))
            c.roundRect(22, y, 956, 57, 6, fill=1, stroke=0)
            text(35, y + 22, a, 16, navy, True)
            text(302, y + 22, b, 16)
            text(658, y + 22, d, 16)
        text(
            28,
            48,
            "A claim must name the evidence kind, candidate revision, and interpretation boundary.",
            16,
        )
    else:
        steps = [
            ("REVIEW SOURCES", ["Inspect scoped changes", "Preserve unrelated work"]),
            ("PAYLOAD COMMIT", ["Commit authored changes", "Anchor published content"]),
            ("CONTROL TAIL", ["Refresh hashes + indexes", "Converge bounded binders"]),
        ]
        for i, (title, lines) in enumerate(steps):
            x = 28 + i * 327
            box(x, 284, 290, 154, title, lines)
            if i < 2:
                arrow(x + 297, 360, x + 320, 360)
        box(
            28,
            99,
            454,
            139,
            "AUTOMATED ACCEPTANCE",
            [
                "Repository + rendered-browser checks",
                "Pages deploy -> exact-candidate verification",
            ],
        )
        box(
            518,
            99,
            454,
            139,
            "HUMAN REVIEW / RELEASE",
            [
                "Named review of current captures and draft",
                "Revision-bound attestation when complete",
            ],
        )
        # Route the control tail into automated acceptance before human review.
        c.setStrokeColor(HexColor(teal))
        c.setLineWidth(2.5)
        c.lines([(829, 280, 829, 260), (829, 260, 255, 260)])
        arrow(255, 260, 255, 242)
        arrow(489, 170, 511, 170)
        text(
            28,
            52,
            "A new payload invalidates older bindings. Technical checks remain distinct from approval.",
            16,
        )
    c.showPage()
    c.save()
    return buffer.getvalue()


def render_figures(destination: Path) -> dict:
    """Produce only the fixed registry, as vector PDF plus offline PNG."""
    import pymupdf

    destination.mkdir()
    for name in FIGURES:
        pdf = _draw(name)
        (destination / f"{name}.pdf").write_bytes(pdf)
        with pymupdf.open(stream=pdf, filetype="pdf") as document:
            document[0].get_pixmap(matrix=pymupdf.Matrix(1.8, 1.8), alpha=False).save(
                destination / f"{name}.png"
            )
    from importlib.metadata import version

    return {
        "producer": PRODUCER,
        "runtime": {name: version(name) for name in ("reportlab", "pymupdf")},
        "interpretation": "Source-backed explanatory diagrams; no experimental results.",
    }
