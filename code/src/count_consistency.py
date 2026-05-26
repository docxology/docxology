"""Cross-check volatile bibliography counts across agent-facing surfaces."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BIBLIO_PATH = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"
PAPERS_README = REPO_ROOT / "papers" / "README.md"


def parse_bibliography_work_count(biblio_path: Path = BIBLIO_PATH) -> int:
    text = biblio_path.read_text(encoding="utf-8")
    m = re.search(r"\*\*(\d+)\*\*\s+works", text)
    if not m:
        raise ValueError(f"Could not parse works count from {biblio_path}")
    return int(m.group(1))


def parse_paper_folder_count(papers_readme: Path = PAPERS_README) -> int:
    text = papers_readme.read_text(encoding="utf-8")
    m = re.search(r"## Papers \((\d+)\)", text)
    if not m:
        raise ValueError(f"Could not parse paper folder count from {papers_readme}")
    return int(m.group(1))


def _find_int(pattern: str, text: str) -> int | None:
    m = re.search(pattern, text, re.I | re.M)
    if not m:
        return None
    return int(m.group(1))


def collect_count_drift() -> list[str]:
    """Return human-readable drift messages; empty if consistent."""
    works = parse_bibliography_work_count()
    folders = parse_paper_folder_count()
    errors: list[str] = []

    llms = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")
    llms_works = _find_int(r"-\s*(\d+)\s+works in the curated bibliography", llms)
    llms_folders = _find_int(r"-\s*(\d+)\s+per-paper folders", llms)
    if llms_works is not None and llms_works != works:
        errors.append(f"llms.txt bibliography works: {llms_works} (expected {works})")
    if llms_folders is not None and llms_folders != folders:
        errors.append(f"llms.txt paper folders: {llms_folders} (expected {folders})")

    pub_html = (REPO_ROOT / "publications.html").read_text(encoding="utf-8")
    title_works = _find_int(r"<title>[^<]*\|\s*(\d+)\s+Works", pub_html)
    if title_works is not None and title_works != works:
        errors.append(f"publications.html title works: {title_works} (expected {works})")

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    readme_works = _find_int(r">\s*\*\*(\d+)\s+works\*\* in the unified bibliography", readme)
    if readme_works is not None and readme_works != works:
        errors.append(f"README.md blockquote works: {readme_works} (expected {works})")

    works_json = REPO_ROOT / "data" / "works.json"
    if works_json.is_file():
        import json

        data = json.loads(works_json.read_text(encoding="utf-8"))
        json_count = data.get("count")
        json_len = len(data.get("works", []))
        if json_count != works:
            errors.append(f"data/works.json count field: {json_count} (expected {works})")
        if json_len != works:
            errors.append(f"data/works.json works length: {json_len} (expected {works})")

    ld_json = REPO_ROOT / "data" / "publications-ld.json"
    if ld_json.is_file():
        import json

        ld = json.loads(ld_json.read_text(encoding="utf-8"))
        me_len = len(ld.get("mainEntity", []))
        if me_len != works:
            errors.append(f"data/publications-ld.json mainEntity length: {me_len} (expected {works})")

    return errors
