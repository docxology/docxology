"""Deterministic local Scholar prerequisites, never an indexing attestation."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

from docxology_tools.citation_metadata import CitationHead
from docxology_tools.paper_artifacts import PaperResources, SITE_URL, source_file, source_paths

PDF_BYTE_LIMIT = 5_000_000


def fingerprint(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def assess_work(root: Path, work: dict, visible: frozenset[str]) -> dict:
    key = work["citation_key"]
    page_rel = f"works/{key}.html"
    page = source_file(root, page_rel, visible)
    resources = PaperResources.load(root, work.get("docs_path", ""), visible)
    parser = CitationHead()
    if page:
        parser.feed(page.read_text(encoding="utf-8"))
    tags = parser.tags
    blockers = []
    for field in ("citation_title", "citation_author", "citation_publication_date"):
        if not tags.get(field) or not all(value.strip() for value in tags[field]):
            blockers.append(f"missing_{field}")
    if work.get("doi") and not all(value.strip() for value in tags.get("citation_doi", [""])):
        blockers.append("missing_citation_doi")
    for field in ("citation_title", "citation_publication_date", "citation_doi", "citation_pdf_url"):
        if len(tags.get(field, [])) > 1:
            blockers.append(f"duplicate_{field}")
    pdf = resources.primary_pdf
    pdf_info = None
    if pdf is None:
        blockers.append("no_selected_local_pdf")
    else:
        url = resources.absolute_url(pdf)
        size = pdf.stat().st_size
        same_directory = PurePosixPath(urlsplit(url).path).parent == PurePosixPath("/" + page_rel).parent
        if not same_directory:
            blockers.append("pdf_directory_differs_from_abstract")
        if size > PDF_BYTE_LIMIT:
            blockers.append("pdf_exceeds_byte_limit")
        if tags.get("citation_pdf_url") != [url]:
            blockers.append("citation_pdf_url_differs_from_selected_source")
        pdf_info = {
            "path": pdf.relative_to(root).as_posix(), "url": url,
            "selection_basis": resources.primary_basis, "bytes": size,
            "sha256": fingerprint(pdf), "within_byte_limit": size <= PDF_BYTE_LIMIT,
            "same_directory_as_abstract": same_directory,
        }
    if page is None:
        blockers.append("missing_abstract_page")
    return {
        "citation_key": key, "title": work["title"], "type": work["type"],
        "abstract_url": SITE_URL + page_rel,
        "page_sha256": fingerprint(page) if page else None,
        "citation_tags": tags, "primary_pdf": pdf_info,
        "selection_issue": resources.selection_issue,
        "local_status": "blocked" if blockers else "requires_review",
        "blockers": blockers,
        "unverified_requirements": ["searchable_pdf", "scholarly_content",
                                    "complete_author_written_abstract_or_full_text", "actual_scholar_indexing"],
    }


def build_report(root: Path) -> dict:
    visible = source_paths(root)
    works_path = source_file(root, "data/works.json", visible)
    if works_path is None:
        raise ValueError("Public works dataset is missing")
    works = json.loads(works_path.read_text(encoding="utf-8"))["works"]
    rows = [assess_work(root, work, visible) for work in works]
    return {
        "schema_version": "1.0", "evidence_kind": "offline Scholar prerequisite audit",
        "inclusion_guidance": "https://scholar.google.com/intl/en/scholar/inclusion.html",
        "pdf_byte_limit": PDF_BYTE_LIMIT,
        "limit_interpretation": "Conservative decimal 5 MB; archived PDFs are never rewritten by this audit.",
        "works_sha256": fingerprint(works_path), "network_checked": False,
        "indexing_verified": False,
        "summary": {
            "works": len(rows), "local_status": dict(sorted(Counter(row["local_status"] for row in rows).items())),
            "blockers": dict(sorted(Counter(item for row in rows for item in row["blockers"]).items())),
        },
        "works": rows,
    }


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    lines = ["# Scholar prerequisite audit", "", "Offline measurements only. Citation metadata, PDF placement, and size do not establish Scholar inclusion.",
             "Searchability, scholarly content, complete author-written abstracts/full text, and actual indexing require separate review.",
             "", "Source: [Google Scholar inclusion guidance](" + report["inclusion_guidance"] + ").",
             "See [the placement policy](../docs/seo/scholar-inclusion.md) and [machine-readable results](../data/scholar-readiness.json).",
             "", f"Audited works: {summary['works']}. PDF limit: {report['pdf_byte_limit']:,} bytes (conservative decimal 5 MB).", "", "| Local blocker | Works |", "| --- | ---: |"]
    lines.extend(f"| {name} | {count} |" for name, count in summary["blockers"].items())
    lines.extend(["", "## Work-level findings", "", "| Work | PDF bytes | Local blockers |", "| --- | ---: | --- |"])
    for row in report["works"]:
        title = row["title"].replace("|", "\\|").replace("\n", " ")
        size = row["primary_pdf"]["bytes"] if row["primary_pdf"] else "—"
        findings = ", ".join(row["blockers"]) or "Separate content and indexing review required"
        lines.append(f"| [{title}](../works/{row['citation_key']}.html) | {size} | {findings} |")
    return "\n".join(lines) + "\n"
