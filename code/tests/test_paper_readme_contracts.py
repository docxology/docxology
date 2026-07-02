from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def paper_readmes() -> list[Path]:
    return sorted(PAPERS_DIR.glob("20*/README.md"))


def doi_for_readme(path: Path, metadata: dict[str, dict]) -> str:
    folder = path.parent.name
    doi = str(metadata.get(folder, {}).get("doi") or "")
    if doi:
        match = DOI_RE.search(doi)
        return match.group(0).rstrip(".,;:)]}`'\"") if match else doi.rstrip(".,;:)]}`'\"")
    match = DOI_RE.search(path.read_text())
    return match.group(0).rstrip(".,;:)]}`'\"") if match else ""


def test_all_paper_readme_doi_citations_include_explicit_doi_and_url():
    metadata = json.loads((PAPERS_DIR / "paper_metadata.json").read_text())
    failures = []
    for path in paper_readmes():
        doi = doi_for_readme(path, metadata)
        if not doi:
            continue
        text = path.read_text()
        resolver = f"https://doi.org/{doi}"
        citation = text.split("## Citation", 1)[1].split("## ", 1)[0] if "## Citation" in text else ""
        if "[![DOI]" not in text or resolver not in text:
            failures.append(f"{path.relative_to(REPO_ROOT)} missing DOI badge/resolver")
        if doi not in citation or resolver not in citation or "DOI:" not in citation or "URL:" not in citation:
            failures.append(f"{path.relative_to(REPO_ROOT)} missing DOI/URL in citation")
    assert not failures, "\n".join(failures)


def test_all_paper_readme_local_links_resolve():
    failures = []
    for path in paper_readmes():
        text = path.read_text()
        for raw_target in MARKDOWN_LINK_RE.findall(text):
            target = raw_target.strip().strip("<>")
            if not target or re.match(r"^(https?://|mailto:|tel:|#)", target):
                continue
            local = unquote(target.split("#", 1)[0].split("?", 1)[0])
            if not local:
                continue
            if not (path.parent / local).exists():
                failures.append(f"{path.relative_to(REPO_ROOT)}: {target}")
    assert not failures, "\n".join(failures)


def test_all_paper_readmes_avoid_broken_visible_link_fragments():
    patterns = [
        r"doi\.org/None",
        r"zenodo\.org/records/None",
        r"https?://\S*\.\.\.",
        r"&[A-Za-z]+\.\.\.",
        r"<\/?(?:p|div)\b",
    ]
    failures = []
    for path in paper_readmes():
        text = path.read_text()
        for pattern in patterns:
            if re.search(pattern, text):
                failures.append(f"{path.relative_to(REPO_ROOT)}: {pattern}")
    assert not failures, "\n".join(failures)
