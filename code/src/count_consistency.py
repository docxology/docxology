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
    if not m:
        raise ValueError(f"Could not parse works count from {biblio_path}")
    return int(m.group(1))


def parse_paper_folder_count(papers_readme: Path = PAPERS_README) -> int:
    text = papers_readme.read_text(encoding="utf-8")
    m = re.search(r"## Papers \((\d+)\)", text)
    if not m:
        raise ValueError(f"Could not parse paper folder count from {papers_readme}")
    return int(m.group(1))


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


def collect_count_drift() -> list[str]:
    """Return human-readable drift messages; empty if consistent."""
    rows = parse_bibliography_rows()
    table_works = len(rows)
    works = parse_bibliography_work_count()
    folders = parse_paper_folder_count()
    folder_links = _folder_links_in_bibliography(rows)
    type_counts = _type_counts(rows)
    domain_counts = _domain_counts(rows)
    software_docx, software_aii = parse_software_catalog_counts()
    software_total = software_docx + software_aii
    errors: list[str] = []

    if works != table_works:
        errors.append(f"pages/BIBLIOGRAPHY.md header works: {works} (expected {table_works})")
    works = table_works

    if folder_links != folders:
        errors.append(f"pages/BIBLIOGRAPHY.md Docs links: {folder_links} (expected {folders})")

    biblio = BIBLIO_PATH.read_text(encoding="utf-8")
    biblio_folders = _find_int(r"\*\*(\d+)\*\*\s+indexed paper folders", biblio)
    _append_if_mismatch(errors, "pages/BIBLIOGRAPHY.md paper folders", biblio_folders, folders)
    biblio_types = {
        label: int(count)
        for count, label in re.findall(
            r"\*\*(\d+)\*\*\s+(Papers|Presentations|Books|Courses|Playbooks|Series)",
            biblio,
        )
    }
    for typ, label in TYPE_LABELS.items():
        expected = type_counts.get(typ, 0)
        if expected:
            _append_if_mismatch(errors, f"pages/BIBLIOGRAPHY.md type count {label}", biblio_types.get(label), expected)
    for label, symbol in DOMAIN_COUNTS.items():
        domain_value = _find_int(rf"###\s+.*{re.escape(label)}\s*\n\n>\s+(\d+)\s+works", biblio)
        _append_if_mismatch(errors, f"pages/BIBLIOGRAPHY.md domain count {label}", domain_value, domain_counts.get(symbol, 0))

    llms = (REPO_ROOT / "llms.txt").read_text(encoding="utf-8")
    llms_works = _find_int(r"-\s*(\d+)\s+works in the curated bibliography", llms)
    llms_folders = _find_int(r"-\s*(\d+)\s+per-paper folders", llms)
    llms_docx = _find_int(r"-\s*(\d+)\s+owned repositories catalogued", llms)
    llms_aii = _find_int(r"-\s*(\d+)\s+Active Inference Institute repositories catalogued", llms)
    _append_if_mismatch(errors, "llms.txt bibliography works", llms_works, works)
    _append_if_mismatch(errors, "llms.txt paper folders", llms_folders, folders)
    _append_if_mismatch(errors, "llms.txt owned repositories", llms_docx, software_docx)
    _append_if_mismatch(errors, "llms.txt AII repositories", llms_aii, software_aii)

    pub_html = (REPO_ROOT / "publications.html").read_text(encoding="utf-8")
    title_works = _find_int(r"<title>[^<]*\|\s*(\d+)\s+Works", pub_html)
    _append_if_mismatch(errors, "publications.html title works", title_works, works)

    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")
    _require_contains(errors, "README.md volatile-count signpost", readme, "reports/current_counts.md")
    _require_contains(errors, "README.md Scholar snapshot signpost", readme, "data/scholar-snapshot.json")
    readme_works = _find_int(r">\s*\*\*(\d+)\s+works\*\* in the unified bibliography", readme)
    readme_profile_repos = _find_int(r"·\s+\*\*(\d+)\*\*\s+public GitHub repositories on the primary profile", readme)
    readme_software_total = _find_int(r"·\s+\*\*(\d+)\*\*\s+catalogued software repos", readme)
    readme_full_catalog = _find_int(r">\s+\*\*Full catalog\*\*:\s+(\d+)\s+works", readme)
    readme_owned = _find_int(r">\s+\*\*Full catalog\*\*:.*?·\s+(\d+)\s+owned repos", readme)
    readme_aii = _find_int(r">\s+\*\*Full catalog\*\*:.*?·\s+\d+\s+owned repos\s+·\s+(\d+)\s+AII contributions", readme)
    readme_papers = _find_int(r"\|\s*[^|]*papers/\]\([^)]*\)\s*\|\s+\*\*(\d+)\s+per-paper folders\*\*", readme)
    _append_if_mismatch(errors, "README.md blockquote works", readme_works, works)
    _append_if_mismatch(errors, "README.md software total", readme_software_total, software_total)
    _append_if_mismatch(errors, "README.md full catalog works", readme_full_catalog, works)
    _append_if_mismatch(errors, "README.md full catalog owned repos", readme_owned, software_docx)
    _append_if_mismatch(errors, "README.md full catalog AII repos", readme_aii, software_aii)
    _append_if_mismatch(errors, "README.md paper folders", readme_papers, folders)
    for label, symbol in DOMAIN_COUNTS.items():
        value = _find_int(rf"\|\s*.*{re.escape(label)}\s*\|\s+\[(\d+)\s+(?:works|papers)\]", readme)
        _append_if_mismatch(errors, f"README.md domain count {label}", value, domain_counts.get(symbol, 0))

    pages_readme = (REPO_ROOT / "pages" / "README.md").read_text(encoding="utf-8")
    _require_contains(errors, "pages/README.md volatile-count signpost", pages_readme, "reports/current_counts.md")
    pages_hub_works = _find_int(r"table of \*\*(\d+) works\*\*", pages_readme)
    pages_hub_folders = _find_int(r"\*\*(\d+) per-paper folders\*\*", pages_readme)
    pages_hub_owned = _find_int(r"\|\s*[^|]*SOFTWARE[^|]*\|\s+\*\*(\d+)\s+owned repos\*\*", pages_readme)
    pages_hub_aii = _find_int(r"\|\s*[^|]*SOFTWARE[^|]*\|.*?\+\s+\*\*(\d+)\s+Active Inference Institute", pages_readme)
    _append_if_mismatch(errors, "pages/README.md bibliography works", pages_hub_works, works)
    _append_if_mismatch(errors, "pages/README.md paper folders", pages_hub_folders, folders)
    _append_if_mismatch(errors, "pages/README.md owned repositories", pages_hub_owned, software_docx)
    _append_if_mismatch(errors, "pages/README.md AII repositories", pages_hub_aii, software_aii)

    root_agents = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    _require_contains(errors, "AGENTS.md volatile-count signpost", root_agents, "reports/current_counts.md")
    _append_if_mismatch(
        errors,
        "AGENTS.md purpose works",
        _find_int(r"unified bibliography \((\d+) works\)", root_agents),
        works,
    )
    _append_if_mismatch(
        errors,
        "AGENTS.md purpose owned software",
        _find_int(r"(\d+) owned software repositories", root_agents),
        software_docx,
    )
    _append_if_mismatch(
        errors,
        "AGENTS.md structure paper folders",
        _find_int(r"papers/\s+.*?(\d+) per-paper folders", root_agents),
        folders,
    )

    docs_agents = (REPO_ROOT / "docs" / "AGENTS.md").read_text(encoding="utf-8")
    _require_contains(errors, "docs/AGENTS.md volatile-count signpost", docs_agents, "reports/current_counts.md")
    _append_if_mismatch(errors, "docs/AGENTS.md bibliography rows", _find_int(r"is the \*\*(\d+)-row\*\* unified table", docs_agents), works)
    _append_if_mismatch(errors, "docs/AGENTS.md paper folders", _find_int(r"has \*\*(\d+)\*\* per-work folders", docs_agents), folders)

    papers_agents = (REPO_ROOT / "papers" / "AGENTS.md").read_text(encoding="utf-8")
    _require_contains(errors, "papers/AGENTS.md volatile-count signpost", papers_agents, "reports/current_counts.md")
    _append_if_mismatch(errors, "papers/AGENTS.md purpose publications", _find_int(r"folders for (\d+) publications", papers_agents), folders)
    _append_if_mismatch(errors, "papers/AGENTS.md metadata entries", _find_int(r"all paper folders \((\d+) entries", papers_agents), folders)
    _append_if_mismatch(errors, "papers/AGENTS.md total works note", _find_int(r"one row per indexed work, (\d+) total", papers_agents), works)
    for label, symbol in DOMAIN_COUNTS.items():
        value = _find_int(rf"\|\s*.*{re.escape(label)}\s*\|\s+(\d+)\s+\|", papers_agents)
        _append_if_mismatch(errors, f"papers/AGENTS.md domain count {label}", value, domain_counts.get(symbol, 0))

    discovery = (REPO_ROOT / "pages" / "DISCOVERY.md").read_text(encoding="utf-8")
    _require_contains(errors, "pages/DISCOVERY.md volatile-count signpost", discovery, "reports/current_counts.md")
    _append_if_mismatch(errors, "pages/DISCOVERY.md Works JSON count", _find_int(r"Structured export of the (\d+)-work bibliography", discovery), works)
    _append_if_mismatch(errors, "pages/DISCOVERY.md Software JSON count", _find_int(r"Structured export of the (\d+)-row curated software catalog", discovery), software_total)

    software_text = SOFTWARE_PATH.read_text(encoding="utf-8")
    _append_if_mismatch(errors, "pages/SOFTWARE.md original repositories", _find_int(r"\*(\d+) original repositories", software_text), software_docx)
    _append_if_mismatch(errors, "pages/SOFTWARE.md AII contributions", _find_int(r"(\d+) catalogued Active Inference Institute contributions", software_text), software_aii)
    _append_if_mismatch(errors, "pages/SOFTWARE.md docxology subtotal", _find_int(r"\|\s+\*\*docxology subtotal\*\*\s+\|\s+\*\*(\d+)\*\*", software_text), software_docx)
    _append_if_mismatch(errors, "pages/SOFTWARE.md grand total", _find_int(r"\|\s+\*\*Grand Total\*\*\s+\|\s+\*\*(\d+)\*\*", software_text), software_total)

    _software_json_counts(errors, software_docx, software_aii)
    _current_counts_report(errors, works, folders, software_docx, software_aii)
    github_docx, github_aii, github_total = _github_inventory_counts(errors)
    if github_docx is not None:
        _append_if_mismatch(errors, "README.md public GitHub repositories", readme_profile_repos, github_docx)
        _append_if_mismatch(errors, "llms.txt public repositories", _find_int(r"-\s*(\d+)\s+public repositories on the primary GitHub profile", llms), github_docx)
        _append_if_mismatch(errors, "pages/DISCOVERY.md GitHub profile public repositories", _find_int(r"GitHub API returned (\d+) public repositories", discovery), github_docx)
        _append_if_mismatch(errors, "pages/SOFTWARE.md public repositories", _find_int(r"For (\d+) total public repos", software_text), github_docx)
        _append_if_mismatch(errors, "pages/DISCOVERY.md repository inventory docxology count", _find_int(r"inventory for (\d+) docxology and", discovery), github_docx)
    if github_aii is not None:
        _append_if_mismatch(
            errors,
            "pages/DISCOVERY.md AII public repositories",
            _find_int(r"GitHub API \S* AII[^\n]*\|\s+Returned (\d+) public repositories on", discovery),
            github_aii,
        )
        _append_if_mismatch(errors, "pages/SOFTWARE.md AII public repositories", _find_int(r"AII account:\s+(\d+) public repositories", software_text), github_aii)
    if github_total is not None:
        _append_if_mismatch(errors, "repositories.html total inventory", _find_int(r"<strong>(\d+)</strong>Total public repos", (REPO_ROOT / "repositories.html").read_text(encoding="utf-8")), github_total)

    index = (REPO_ROOT / "index.html").read_text(encoding="utf-8")
    index_hero_works = _find_int(r'class="btn btn-outline">(\d+)\s+Works</a>', index)
    index_stat_works = _find_int(r'<div class="stat"><div class="num">(\d+)</div><div class="lbl">Works</div></div>', index)
    index_sidebar_works = _find_int(r"<strong>(\d+)</strong>\s+works in the unified bibliography", index)
    index_bibliography_works = _find_int(r"Full bibliography \((\d+) works\)", index)
    for label, value in {
        "index.html hero works": index_hero_works,
        "index.html stat works": index_stat_works,
        "index.html sidebar works": index_sidebar_works,
        "index.html bibliography CTA works": index_bibliography_works,
    }.items():
        _append_if_mismatch(errors, label, value, works)

    works_json = REPO_ROOT / "data" / "works.json"
    if works_json.is_file():
        data = json.loads(works_json.read_text(encoding="utf-8"))
        json_count = data.get("count")
        json_len = len(data.get("works", []))
        _append_if_mismatch(errors, "data/works.json count field", json_count, works)
        _append_if_mismatch(errors, "data/works.json works length", json_len, works)

    ld_json = REPO_ROOT / "data" / "publications-ld.json"
    if ld_json.is_file():
        ld = json.loads(ld_json.read_text(encoding="utf-8"))
        me_len = len(ld.get("mainEntity", []))
        _append_if_mismatch(errors, "data/publications-ld.json mainEntity length", me_len, works)

    # Hand-maintained narrative pages that quote the work/folder count in prose. These
    # have no generator, so nothing keeps them current — guard them here so they cannot
    # silently rot (they had drifted to 125/154 before being reconciled 2026-06-14).
    links = (REPO_ROOT / "pages" / "LINKS.md").read_text(encoding="utf-8")
    _append_if_mismatch(errors, "pages/LINKS.md bibliography works", _find_int(r"table of all (\d+) works", links), works)
    _append_if_mismatch(errors, "pages/LINKS.md paper folders", _find_int(r"(\d+) per-paper folders with documentation", links), folders)

    profile = (REPO_ROOT / "pages" / "PROFILE.md").read_text(encoding="utf-8")
    _append_if_mismatch(errors, "pages/PROFILE.md prose works", _find_int(r"lists \*\*(\d+)\*\* works", profile), works)
    _append_if_mismatch(errors, "pages/PROFILE.md metrics table works", _find_int(r"Works \(unified bibliography\)\s*\|\s*\[(\d+)\]", profile), works)

    wikipedia = (REPO_ROOT / "pages" / "WIKIPEDIA.md").read_text(encoding="utf-8")
    _append_if_mismatch(errors, "pages/WIKIPEDIA.md lead catalog works", _find_int(r"catalogs (\d+) works", wikipedia), works)
    _append_if_mismatch(errors, "pages/WIKIPEDIA.md full catalog note", _find_int(r"full (\d+)-work catalog", wikipedia), works)

    for page in ("COLLABORATORS.md", "MEDIA.md"):
        text = (REPO_ROOT / "pages" / page).read_text(encoding="utf-8")
        _append_if_mismatch(errors, f"pages/{page} footer works", _find_int(r"the full bibliography \((\d+) works\)", text), works)

    # Hand-maintained HTML pages that quote the work count in prose (not count-derived
    # like publications.html). They had drifted to 154/125 before 2026-06-14.
    discovery_html = (REPO_ROOT / "discovery.html").read_text(encoding="utf-8")
    _append_if_mismatch(errors, "discovery.html works-json export", _find_int(r"export of the (\d+)-work bibliography", discovery_html), works)
    cite_verify_html = (REPO_ROOT / "cite-verify.html").read_text(encoding="utf-8")
    _append_if_mismatch(errors, "cite-verify.html works-json export", _find_int(r"Structured (\d+)-work bibliography export", cite_verify_html), works)

    return errors
