"""Cross-check volatile counts across agent-facing surfaces."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BIBLIO_PATH = REPO_ROOT / "pages" / "BIBLIOGRAPHY.md"
PAPERS_README = REPO_ROOT / "papers" / "README.md"
SOFTWARE_PATH = REPO_ROOT / "pages" / "SOFTWARE.md"

DOMAIN_COUNTS = {
    "Entomology": "\U0001f41c",
    "Active Inference": "\U0001f9e0",
    "Cognitive Security": "\U0001f6e1\ufe0f",
    "Art & Synergetics": "\U0001f3a8",
    "Computational": "\U0001f4bb",
    "AII Ecosystem": "\U0001f30d",
    "Presentations & Media": "\U0001f3a5",
    "Genetics & Biomedical": "\U0001f9ec",
}

TYPE_LABELS = {
    "Paper": "Papers",
    "Presentation": "Presentations",
    "Book": "Books",
    "Course": "Courses",
    "Playbook": "Playbooks",
    "Series": "Series",
}


def parse_bibliography_rows(biblio_path: Path = BIBLIO_PATH) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in biblio_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or not cells[0].isdigit():
            continue
        rows.append(
            {
                "num": cells[0],
                "year": cells[1],
                "domain": cells[2],
                "type": cells[3],
                "title": cells[4],
                "docs": cells[7],
            }
        )
    return rows


def parse_bibliography_work_count(biblio_path: Path = BIBLIO_PATH) -> int:
    text = biblio_path.read_text(encoding="utf-8")
    m = re.search(r"\*\*(\d+)\*\*\s+works", text)
    if m:
        return int(m.group(1))
    counts = _load_current_counts_payload().get("counts", {})
    if isinstance(counts.get("bibliography_works"), int):
        return int(counts["bibliography_works"])
    raise ValueError(f"Could not parse works count from {biblio_path}")


def parse_paper_folder_count(papers_readme: Path = PAPERS_README) -> int:
    text = papers_readme.read_text(encoding="utf-8")
    m = re.search(r"## Papers \((\d+)\)", text)
    if m:
        return int(m.group(1))
    counts = _load_current_counts_payload().get("counts", {})
    if isinstance(counts.get("paper_folder_docs"), int):
        return int(counts["paper_folder_docs"])
    raise ValueError(f"Could not parse paper folder count from {papers_readme}")


def parse_software_catalog_counts(software_path: Path = SOFTWARE_PATH) -> tuple[int, int]:
    docxology = 0
    aii = 0
    for line in software_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| ["):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 5:
            continue
        if "https://github.com/docxology/" in cells[0]:
            docxology += 1
        elif "https://github.com/ActiveInferenceInstitute/" in cells[0]:
            aii += 1
    return docxology, aii


def canonical_bibliography_snapshot(
    biblio_path: Path = BIBLIO_PATH,
    papers_readme: Path = PAPERS_README,
) -> dict[str, int | Counter[str]]:
    """Ground-truth bibliography counts parsed from canonical source tables."""
    rows = parse_bibliography_rows(biblio_path)
    return {
        "works": len(rows),
        "header_works": parse_bibliography_work_count(biblio_path),
        "paper_folders": parse_paper_folder_count(papers_readme),
        "docs_links": _folder_links_in_bibliography(rows),
        "type_counts": _type_counts(rows),
        "domain_counts": _domain_counts(rows),
    }


def canonical_software_snapshot(software_path: Path = SOFTWARE_PATH) -> dict[str, int]:
    """Ground-truth software catalog counts parsed from pages/SOFTWARE.md rows."""
    docxology, aii = parse_software_catalog_counts(software_path)
    return {
        "docxology": docxology,
        "aii": aii,
        "total": docxology + aii,
    }


CURRENT_COUNTS_SIGNPOST = "reports/current_counts.md"


def _load_current_counts_payload() -> dict:
    payload_path = REPO_ROOT / "data" / "current-counts.json"
    if not payload_path.exists():
        return {}
    try:
        return json.loads(payload_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _find_int(pattern: str, text: str) -> int | None:
    m = re.search(pattern, text, re.I | re.M)
    if not m:
        return None
    return int(m.group(1))


def _append_if_mismatch(errors: list[str], label: str, value: int | None, expected: int) -> None:
    if value is not None and value != expected:
        errors.append(f"{label}: {value} (expected {expected})")


def _require_contains(errors: list[str], label: str, text: str, needle: str) -> None:
    if needle not in text:
        errors.append(f"{label}: missing {needle}")


def _domain_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row["domain"] for row in rows)


def _type_counts(rows: list[dict[str, str]]) -> Counter[str]:
    return Counter(row["type"] for row in rows)


def _folder_links_in_bibliography(rows: list[dict[str, str]]) -> int:
    return sum(1 for row in rows if "../papers/" in row["docs"])


def _software_json_counts(errors: list[str], expected_docx: int, expected_aii: int) -> None:
    path = REPO_ROOT / "data" / "software.json"
    if not path.is_file():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    repos = data.get("repositories", [])
    docx = sum(1 for repo in repos if repo.get("owner") == "docxology")
    aii = sum(1 for repo in repos if repo.get("owner") == "ActiveInferenceInstitute")
    _append_if_mismatch(errors, "data/software.json count field", data.get("count"), expected_docx + expected_aii)
    _append_if_mismatch(errors, "data/software.json repositories length", len(repos), expected_docx + expected_aii)
    _append_if_mismatch(errors, "data/software.json docxology rows", docx, expected_docx)
    _append_if_mismatch(errors, "data/software.json AII rows", aii, expected_aii)

    ld_path = REPO_ROOT / "data" / "software-ld.json"
    if ld_path.is_file():
        ld = json.loads(ld_path.read_text(encoding="utf-8"))
        _append_if_mismatch(
            errors,
            "data/software-ld.json mainEntity length",
            len(ld.get("mainEntity", [])),
            expected_docx + expected_aii,
        )


def _github_inventory_counts(errors: list[str]) -> tuple[int | None, int | None, int | None]:
    path = REPO_ROOT / "data" / "github-repositories.json"
    if not path.is_file():
        return None, None, None
    payload = json.loads(path.read_text(encoding="utf-8"))
    counts = payload.get("counts", {})
    profiles = payload.get("profiles", {})
    docx = counts.get("docxology")
    aii = counts.get("ActiveInferenceInstitute")
    total = counts.get("total")
    _append_if_mismatch(
        errors,
        "data/github-repositories.json docxology profile count",
        profiles.get("docxology", {}).get("public_repos"),
        docx,
    )
    _append_if_mismatch(
        errors,
        "data/github-repositories.json AII profile count",
        profiles.get("ActiveInferenceInstitute", {}).get("public_repos"),
        aii,
    )
    return docx, aii, total


def _current_counts_report(errors: list[str], works: int, folders: int, software_docx: int, software_aii: int) -> None:
    json_path = REPO_ROOT / "data" / "current-counts.json"
    report_path = REPO_ROOT / "reports" / "current_counts.md"
    if not json_path.is_file():
        errors.append("data/current-counts.json: missing generated volatile-count report")
        return
    if not report_path.is_file():
        errors.append("reports/current_counts.md: missing generated volatile-count report")
        return

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    counts = payload.get("counts", {})
    software = counts.get("software", {})
    generated_exports = counts.get("generated_exports", {})
    _append_if_mismatch(errors, "data/current-counts.json bibliography works", counts.get("bibliography_works"), works)
    _append_if_mismatch(errors, "data/current-counts.json paper-folder docs", counts.get("paper_folder_docs"), folders)
    _append_if_mismatch(
        errors,
        "data/current-counts.json bibliography docs links",
        counts.get("bibliography_docs_links"),
        folders,
    )
    _append_if_mismatch(errors, "data/current-counts.json docxology software", software.get("docxology_owned"), software_docx)
    _append_if_mismatch(
        errors,
        "data/current-counts.json AII software",
        software.get("active_inference_institute"),
        software_aii,
    )
    _append_if_mismatch(
        errors,
        "data/current-counts.json software total",
        software.get("curated_total"),
        software_docx + software_aii,
    )
    _append_if_mismatch(errors, "data/current-counts.json data/works.json", generated_exports.get("data_works_json"), works)
    _append_if_mismatch(
        errors,
        "data/current-counts.json data/publications-ld.json",
        generated_exports.get("data_publications_ld_main_entity"),
        works,
    )
    _append_if_mismatch(
        errors,
        "data/current-counts.json data/software.json",
        generated_exports.get("data_software_json"),
        software_docx + software_aii,
    )
    _append_if_mismatch(
        errors,
        "data/current-counts.json data/software-ld.json",
        generated_exports.get("data_software_ld_main_entity"),
        software_docx + software_aii,
    )


def _bibliography_prose_counts(errors: list[str], works: int, folders: int) -> None:
    text = BIBLIO_PATH.read_text(encoding="utf-8")
    works_match = re.search(r"\*\*(\d+)\s+works\*\*", text)
    folders_match = re.search(r"\*\*(\d+)\*\*\s+indexed paper folders", text)
    type_counts = _type_counts(parse_bibliography_rows())
    _append_if_mismatch(
        errors,
        "pages/BIBLIOGRAPHY.md hero works",
        int(works_match.group(1)) if works_match else None,
        works,
    )
    _append_if_mismatch(
        errors,
        "pages/BIBLIOGRAPHY.md indexed paper folders",
        int(folders_match.group(1)) if folders_match else None,
        folders,
    )
    for typ, label in TYPE_LABELS.items():
        match = re.search(rf"\*\*(\d+)\*\*\s+{re.escape(label)}", text)
        _append_if_mismatch(
            errors,
            f"pages/BIBLIOGRAPHY.md type summary {label}",
            int(match.group(1)) if match else None,
            type_counts.get(typ, 0),
        )
    _require_contains(
        errors,
        "pages/BIBLIOGRAPHY.md current-count signpost",
        text,
        "../reports/current_counts.md",
    )
    if re.search(r"\.\.\.and \d+ more in the table above", text):
        errors.append("pages/BIBLIOGRAPHY.md: residual domain counts should signpost current totals")


def _software_prose_counts(errors: list[str], software_docx: int, software_aii: int) -> None:
    text = SOFTWARE_PATH.read_text(encoding="utf-8")
    hero_match = re.search(
        r"\*(\d+)\s+original repositories · (\d+)\s+catalogued Active Inference Institute contributions",
        text,
    )
    if hero_match:
        _append_if_mismatch(
            errors,
            "pages/SOFTWARE.md hero docxology repositories",
            int(hero_match.group(1)),
            software_docx,
        )
        _append_if_mismatch(
            errors,
            "pages/SOFTWARE.md hero AII repositories",
            int(hero_match.group(2)),
            software_aii,
        )
    else:
        errors.append("pages/SOFTWARE.md: missing repository-count hero")
    docx_summary = re.search(r"\| \*\*docxology subtotal\*\* \| \*\*(\d+)\*\*", text)
    aii_summary = re.search(r"\| AII Contributions \(non-fork\) \| (\d+) \|", text)
    grand_summary = re.search(r"\| \*\*Grand Total\*\* \| \*\*(\d+)\*\*", text)
    _append_if_mismatch(
        errors,
        "pages/SOFTWARE.md docxology subtotal",
        int(docx_summary.group(1)) if docx_summary else None,
        software_docx,
    )
    _append_if_mismatch(
        errors,
        "pages/SOFTWARE.md AII subtotal",
        int(aii_summary.group(1)) if aii_summary else None,
        software_aii,
    )
    _append_if_mismatch(
        errors,
        "pages/SOFTWARE.md grand total",
        int(grand_summary.group(1)) if grand_summary else None,
        software_docx + software_aii,
    )
    _require_contains(
        errors,
        "pages/SOFTWARE.md current-count signpost",
        text,
        "../reports/current_counts.md",
    )


def collect_count_drift() -> list[str]:
    """Return human-readable drift messages; empty if consistent."""
    rows = parse_bibliography_rows()
    software_docx, software_aii = parse_software_catalog_counts()
    software_total = software_docx + software_aii
    works = len(rows)
    folders = _folder_links_in_bibliography(rows)
    errors: list[str] = []

    payload = _load_current_counts_payload()
    counts = payload.get("counts", {}) if isinstance(payload, dict) else {}
    if not isinstance(counts, dict):
        return ["data/current-counts.json: missing or invalid counts block"]

    software = counts.get("software", {}) or {}
    generated_exports = counts.get("generated_exports", {}) or {}
    type_payload = counts.get("types", {}) or {}
    domain_payload = counts.get("domains", {}) or {}
    generated_counts = canonical_bibliography_snapshot()

    _append_if_mismatch(errors, "data/current-counts.json bibliography works", counts.get("bibliography_works"), works)
    _append_if_mismatch(errors, "data/current-counts.json paper-folder docs", counts.get("paper_folder_docs"), folders)
    _append_if_mismatch(
        errors,
        "data/current-counts.json bibliography docs links",
        counts.get("bibliography_docs_links"),
        folders,
    )
    _append_if_mismatch(errors, "data/current-counts.json docxology software", software.get("docxology_owned"), software_docx)
    _append_if_mismatch(
        errors,
        "data/current-counts.json AII software",
        software.get("active_inference_institute"),
        software_aii,
    )
    _append_if_mismatch(errors, "data/current-counts.json software total", software.get("curated_total"), software_total)
    _append_if_mismatch(errors, "data/current-counts.json data/works.json", generated_exports.get("data_works_json"), works)
    _append_if_mismatch(
        errors,
        "data/current-counts.json data/publications-ld.json",
        generated_exports.get("data_publications_ld_main_entity"),
        works,
    )
    _append_if_mismatch(
        errors,
        "data/current-counts.json data/software.json",
        generated_exports.get("data_software_json"),
        software_total,
    )
    _append_if_mismatch(
        errors,
        "data/current-counts.json data/software-ld.json",
        generated_exports.get("data_software_ld_main_entity"),
        software_total,
    )

    for typ, label in TYPE_LABELS.items():
        expected = generated_counts["type_counts"].get(typ, 0)
        _append_if_mismatch(
            errors,
            f"data/current-counts.json type count {label}",
            type_payload.get(label),
            expected,
        )

    for label, emoji in DOMAIN_COUNTS.items():
        expected = generated_counts["domain_counts"].get(emoji, 0)
        _append_if_mismatch(
            errors,
            f"data/current-counts.json domain count {label}",
            domain_payload.get(label),
            expected,
        )

    _current_counts_report(errors, works, folders, software_docx, software_aii)
    _bibliography_prose_counts(errors, works, folders)
    _software_prose_counts(errors, software_docx, software_aii)
    _software_json_counts(errors, software_docx, software_aii)
    _github_inventory_counts(errors)

    if parse_bibliography_work_count() != works:
        errors.append(
            f"Bibliography header count does not match parsed rows: {parse_bibliography_work_count()} != {works}"
        )
    if parse_paper_folder_count() != folders:
        errors.append(
            f"Paper-folder count does not match parsed docs links: {parse_paper_folder_count()} != {folders}"
        )

    works_json = REPO_ROOT / "data" / "works.json"
    if works_json.is_file():
        data = json.loads(works_json.read_text(encoding="utf-8"))
        _append_if_mismatch(errors, "data/works.json count field", data.get("count"), works)
        _append_if_mismatch(errors, "data/works.json works length", len(data.get("works", [])), works)

    publications_ld = REPO_ROOT / "data" / "publications-ld.json"
    if publications_ld.is_file():
        ld_payload = json.loads(publications_ld.read_text(encoding="utf-8"))
        _append_if_mismatch(errors, "data/publications-ld.json mainEntity length", len(ld_payload.get("mainEntity", [])), works)

    software_ld = REPO_ROOT / "data" / "software-ld.json"
    if software_ld.is_file():
        ld_payload = json.loads(software_ld.read_text(encoding="utf-8"))
        _append_if_mismatch(
            errors,
            "data/software-ld.json mainEntity length",
            len(ld_payload.get("mainEntity", [])),
            software_total,
        )

    prose_targets = [
        ("README.md", "README.md volatile-count signpost", "reports/current_counts.md"),
        ("README.md", "README.md Scholar snapshot signpost", "data/scholar-snapshot.json"),
        ("pages/README.md", "pages/README.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("AGENTS.md", "AGENTS.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("docs/AGENTS.md", "docs/AGENTS.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("papers/AGENTS.md", "papers/AGENTS.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/DISCOVERY.md", "pages/DISCOVERY.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/LINKS.md", "pages/LINKS.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/PROFILE.md", "pages/PROFILE.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/WIKIPEDIA.md", "pages/WIKIPEDIA.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/COLLABORATORS.md", "pages/COLLABORATORS.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/MEDIA.md", "pages/MEDIA.md volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("discovery.html", "discovery.html volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("cite-verify.html", "cite-verify.html volatile-count signpost", CURRENT_COUNTS_SIGNPOST),
        ("pages/SOFTWARE.md", "pages/SOFTWARE.md software hero", "Open-Source Repositories"),
        ("llms.txt", "llms.txt shape", "Current volatile totals"),
        ("publications.html", "publications.html shape", "<title>"),
        ("index.html", "index.html shape", "<title>"),
        ("software.html", "software.html shape", "<title>"),
    ]
    for rel, label, needle in prose_targets:
        text = (REPO_ROOT / rel).read_text(encoding="utf-8")
        _require_contains(errors, label, text, needle)

    return errors
