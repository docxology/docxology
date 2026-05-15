#!/usr/bin/env python3
"""Export the unified bibliography to citation-manager and agent-friendly formats.

Outputs:
  - bibliography.bib
  - bibliography.ris
  - bibliography.csl.json
  - data/works.json

Run with --check to verify the generated files are current without writing them.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
sys.path.insert(0, str(PAPERS_DIR))

from biblio_table import BiblioRow, iter_bibliography_rows  # noqa: E402
from sync_publications_html import canonical_link_url  # noqa: E402

try:
    from report_paths import generated_timestamp
except ImportError:  # pragma: no cover - package import path
    from .report_paths import generated_timestamp


DOMAIN_NAMES = {
    "🐜": "Entomology",
    "🧠": "Active Inference",
    "🛡️": "Cognitive Security",
    "🛡": "Cognitive Security",
    "🎨": "Art & Synergetics",
    "💻": "Computational",
    "🌍": "AII Ecosystem",
    "🎥": "Media & Teaching",
    "🧬": "Genetics & Biomedical",
}

TYPE_TO_BIBTEX = {
    "Book": "book",
    "Book Chapter": "incollection",
    "Course": "misc",
    "Paper": "article",
    "Playbook": "misc",
    "Presentation": "misc",
    "Series": "misc",
}

TYPE_TO_CSL = {
    "Book": "book",
    "Book Chapter": "chapter",
    "Course": "webpage",
    "Paper": "article-journal",
    "Playbook": "webpage",
    "Presentation": "speech",
    "Series": "webpage",
}

TYPE_TO_RIS = {
    "Book": "BOOK",
    "Book Chapter": "CHAP",
    "Course": "ELEC",
    "Paper": "JOUR",
    "Playbook": "GEN",
    "Presentation": "CONF",
    "Series": "GEN",
}


@dataclass(frozen=True)
class Work:
    num: int
    citation_key: str
    year: int | str
    domain: str
    domain_name: str
    type: str
    title: str
    venue: str
    url: str
    doi: str
    docs_path: str
    has_paper_folder: bool


def clean_text(value: str) -> str:
    """Remove Markdown and presentation-only glyphs from a field."""
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"<[^>]+>", "", value)
    return value.replace("📄", "").replace("📁", "").strip()


def doi_from_url(url: str) -> str:
    m = re.search(r"https?://(?:dx\.)?doi\.org/(10\.\S+)", url)
    return m.group(1).rstrip(").,") if m else ""


def slug_words(title: str) -> list[str]:
    words = re.findall(r"[A-Za-z0-9]+", title)
    stop = {"a", "an", "and", "for", "in", "of", "on", "the", "to", "with"}
    return [w for w in words if w.lower() not in stop][:4]


def citation_key(row: BiblioRow) -> str:
    words = slug_words(row.title)
    suffix = "".join(w[:1].upper() + w[1:] for w in words) or "Work"
    return f"Friedman{row.year}{suffix}{row.num:03d}"


def docs_path(row: BiblioRow) -> str:
    return f"papers/{row.folder}/" if row.folder else ""


def row_to_work(row: BiblioRow) -> Work:
    url = canonical_link_url(row.link_cell, row.venue)
    domain = row.domain.strip()
    return Work(
        num=row.num,
        citation_key=citation_key(row),
        year=int(row.year) if row.year.isdigit() else row.year,
        domain=domain,
        domain_name=DOMAIN_NAMES.get(domain, DOMAIN_NAMES.get(domain.rstrip("️"), "Other")),
        type=row.typ,
        title=clean_text(row.title),
        venue=clean_text(row.venue),
        url=url,
        doi=doi_from_url(url),
        docs_path=docs_path(row),
        has_paper_folder=bool(row.folder),
    )


def bib_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def bibtex_entry(work: Work) -> str:
    entry_type = TYPE_TO_BIBTEX.get(work.type, "misc")
    fields = [
        ("title", work.title),
        ("author", "Friedman, Daniel Ari"),
        ("year", str(work.year)),
    ]
    if entry_type in {"article", "incollection"} and work.venue:
        fields.append(("journal" if entry_type == "article" else "booktitle", work.venue))
    elif work.venue:
        fields.append(("howpublished", work.venue))
    if work.doi:
        fields.append(("doi", work.doi))
    if work.url:
        fields.append(("url", work.url))
    fields.extend(
        [
            ("keywords", f"{work.domain_name}; {work.type}"),
            ("note", f"Catalog row {work.num}; docs: {work.docs_path or 'not available'}"),
        ]
    )
    body = ",\n".join(f"  {k} = {{{bib_escape(v)}}}" for k, v in fields if v)
    return f"@{entry_type}{{{work.citation_key},\n{body}\n}}"


def csl_item(work: Work) -> dict:
    item = {
        "id": work.citation_key,
        "type": TYPE_TO_CSL.get(work.type, "article-journal"),
        "title": work.title,
        "author": [{"family": "Friedman", "given": "Daniel Ari"}],
        "issued": {"date-parts": [[work.year]]},
        "genre": work.type,
        "keyword": f"{work.domain_name}; {work.type}",
        "note": f"Catalog row {work.num}; docs: {work.docs_path or 'not available'}",
    }
    if work.venue:
        item["container-title"] = work.venue
        item["publisher"] = work.venue
    if work.doi:
        item["DOI"] = work.doi
    if work.url:
        item["URL"] = work.url
    return item


def ris_record(work: Work) -> str:
    lines = [
        f"TY  - {TYPE_TO_RIS.get(work.type, 'GEN')}",
        "AU  - Friedman, Daniel Ari",
        f"PY  - {work.year}",
        f"TI  - {work.title}",
    ]
    if work.venue:
        lines.append(f"T2  - {work.venue}")
    if work.doi:
        lines.append(f"DO  - {work.doi}")
    if work.url:
        lines.append(f"UR  - {work.url}")
    lines.extend(
        [
            f"KW  - {work.domain_name}",
            f"KW  - {work.type}",
            f"N1  - Catalog row {work.num}; docs: {work.docs_path or 'not available'}",
            "ER  -",
        ]
    )
    return "\n".join(lines)


def existing_generated_at(path: Path) -> str | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("generated_at")
    except json.JSONDecodeError:
        return None


def render_outputs(works: list[Work], generated_at: str | None = None) -> dict[Path, str]:
    data_dir = REPO_ROOT / "data"
    works_json = {
        "generated_at": generated_at or generated_timestamp(),
        "source": "pages/BIBLIOGRAPHY.md",
        "count": len(works),
        "works": [asdict(w) for w in works],
    }
    return {
        REPO_ROOT / "bibliography.bib": "\n\n".join(bibtex_entry(w) for w in works) + "\n",
        REPO_ROOT / "bibliography.ris": "\n\n".join(ris_record(w) for w in works) + "\n",
        REPO_ROOT / "bibliography.csl.json": json.dumps(
            [csl_item(w) for w in works], indent=2, ensure_ascii=False
        )
        + "\n",
        data_dir / "works.json": json.dumps(works_json, indent=2, ensure_ascii=False) + "\n",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated files are stale")
    args = parser.parse_args()

    works = [row_to_work(r) for r in iter_bibliography_rows()]
    generated_at = existing_generated_at(REPO_ROOT / "data" / "works.json") if args.check else None
    outputs = render_outputs(works, generated_at)

    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(REPO_ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if stale:
        raise SystemExit("Stale generated bibliography files: " + ", ".join(stale))

    action = "checked" if args.check else "wrote"
    print(f"{action} {len(outputs)} bibliography export files from {len(works)} works")


if __name__ == "__main__":
    main()
