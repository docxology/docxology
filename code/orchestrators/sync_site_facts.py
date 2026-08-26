#!/usr/bin/env python3
"""Propagate generated counts and freshness into hand-authored public surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))
from site_facts import SiteFactsError, counts, generated_date, generated_month_year  # noqa: E402
from report_paths import latest_source_report, latest_source_subdir_file  # noqa: E402
TARGETS = [
    REPO_ROOT / "index.html",
    REPO_ROOT / "publications.html",
    REPO_ROOT / "discovery.html",
    REPO_ROOT / "pages" / "DISCOVERY.md",
    REPO_ROOT / "llms.txt",
    REPO_ROOT / "art.html",
    REPO_ROOT / "videos.html",
]

MONTH_NAMES = (
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
)
MONTH_YEAR_PATTERN = rf"(?:{'|'.join(MONTH_NAMES)})\s+\d{{4}}"


def latest_report(prefix: str, suffix: str) -> str | None:
    path = latest_source_report(f"{prefix}_*.{suffix}", required=False)
    return path.name if path else None


def dataset_count(filename: str, key: str) -> int:
    try:
        payload = json.loads((REPO_ROOT / "data" / filename).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return 0
    value = payload.get(key)
    return int(value) if isinstance(value, int) else 0


def render(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    c = counts()
    date = generated_date()
    month = generated_month_year()
    works = c.get("bibliography_works", 0)
    folders = c.get("paper_folder_docs", 0)
    full_text = c.get("full_text_papers", 0)
    images = c.get("extracted_images", 0)
    galleries = c.get("papers_with_images", 0)
    artworks = dataset_count("artworks.json", "count")
    videos = dataset_count("videos.json", "count")
    github = c.get("github_inventory", {})
    public_facts = c.get("public_source_snapshot", {})
    replacements = {
        rf"Last updated:\s*{MONTH_YEAR_PATTERN}": f"Data refreshed {month}",
        rf"Data refreshed\s+{MONTH_YEAR_PATTERN}": f"Data refreshed {month}",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    if path.name == "index.html":
        text = re.sub(r'<meta name="revised" content="[^"]+">', f'<meta name="revised" content="{date}">', text)
        text = re.sub(r'<meta name="date" content="[^"]+">', f'<meta name="date" content="{date}">', text)
        text = re.sub(r'("dateModified":\s*")[^"]+(")', rf"\g<1>{date}\g<2>", text, count=1)
        text = re.sub(r"Paper Documentation \(\d+ folders, \d+ with full text, [\d,]+ extracted images\)", f"Paper Documentation ({folders} folders, {full_text} with full text, {images:,} extracted images)", text)
        text = re.sub(r"Highlights from the catalog across \d+ research domains", "Highlights from the catalog across 8 research domains", text)
    elif path.name == "publications.html":
        text = re.sub(r"<p class=\"sub\">\d+ works spanning", f"<p class=\"sub\">{works} works spanning", text, count=1)
        text = re.sub(rf"as of {MONTH_YEAR_PATTERN}", f"as of {month}", text, count=1, flags=re.IGNORECASE)
        text = re.sub(r"<meta name=\"revised\" content=\"[^\"]+\">", f'<meta name="revised" content="{date}">', text)
    elif path.name == "discovery.html":
        text = re.sub(r'("dateModified":\s*")[^"]+(")', rf"\g<1>{date}\g<2>", text, count=1)
        text = re.sub(r'<meta name="revised" content="[^"]+">', f'<meta name="revised" content="{date}">', text)
        text = re.sub(r"checked on \d{4}-\d{2}-\d{2}", f"checked on {date}", text)
        text = re.sub(r"Returned \d+ exact-name records", f"Returned {public_facts.get('Zenodo exact-name creator records', 0)} exact-name records", text)
        text = re.sub(r"Returned \d+ records, including versioned deposits", f"Returned {public_facts.get('Zenodo ORCID-linked records', 0)} records, including versioned deposits", text)
        text = re.sub(
            r'(<tr><td>GitHub API — docxology</td>.*?<td>Returned )\d+( public repositories on )\d{4}-\d{2}-\d{2}',
            rf"\g<1>{public_facts.get('GitHub user docxology', github.get('docxology', 0))}\g<2>{date}",
            text,
            flags=re.S,
        )
        text = re.sub(
            r'(<tr><td>GitHub API — AII</td>.*?<td>Returned )\d+( public repositories on )\d{4}-\d{2}-\d{2}',
            rf"\g<1>{public_facts.get('GitHub user ActiveInferenceInstitute', github.get('ActiveInferenceInstitute', 0))}\g<2>{date}",
            text,
            flags=re.S,
        )
        text = re.sub(
            r'(<div class="stat"><div class="num">)\d+/\d+(</div><div class="lbl">Zenodo exact / ORCID</div>)',
            rf"\g<1>{public_facts.get('Zenodo exact-name creator records', 0)}/{public_facts.get('Zenodo ORCID-linked records', 0)}\g<2>",
            text,
        )
        for prefix, suffix in (("public_source_snapshot", "json"), ("public_source_inventory", "json")):
            name = latest_report(prefix, suffix)
            if name:
                text = re.sub(rf"{prefix}_\d{{4}}-\d{{2}}-\d{{2}}\.json", name, text)
    elif path.name == "DISCOVERY.md":
        # Keep the Scholar snapshot's own provenance date intact. The other
        # source rows are refreshed from the latest public-source report below.
        text = re.sub(r"checked on \d{4}-\d{2}-\d{2}", f"checked on {date}", text)
        text = re.sub(r"Zenodo returned \d+ exact-name records on \d{4}-\d{2}-\d{2}", f"Zenodo returned {public_facts.get('Zenodo exact-name creator records', 0)} exact-name records on {date}", text)
        text = re.sub(r"ORCID-linked query returned \d+ records on \d{4}-\d{2}-\d{2}", f"ORCID-linked query returned {public_facts.get('Zenodo ORCID-linked records', 0)} records on {date}", text)
        text = re.sub(r"NCBI E-utilities returned \d+ records for the exact author query on \d{4}-\d{2}-\d{2}", f"NCBI E-utilities returned {public_facts.get('PubMed exact author records', 0)} records for the exact author query on {date}", text)
        text = re.sub(r"Europe PMC returned \d+ exact-author results, including preprints, on \d{4}-\d{2}-\d{2}", f"Europe PMC returned {public_facts.get('Europe PMC exact author records', 0)} exact-author results, including preprints, on {date}", text)
        text = re.sub(r"Crossref returned \d+ DOI records attached to the ORCID on \d{4}-\d{2}-\d{2}", f"Crossref returned {public_facts.get('Crossref ORCID DOI records', 0)} DOI records attached to the ORCID on {date}", text)
        for prefix, suffix in (("public_source_snapshot", "json"), ("public_source_inventory", "json")):
            name = latest_report(prefix, suffix)
            if name:
                text = re.sub(rf"{prefix}_\d{{4}}-\d{{2}}-\d{{2}}\.json", name, text)
    elif path.name == "llms.txt":
        text = re.sub(
            r"latest snapshot records \d+ paper folders, \d+ full-text extractions, \d+ image galleries, and [\d,]+ extracted images",
            f"latest snapshot records {folders} paper folders, {full_text} full-text extractions, {galleries} image galleries, and {images:,} extracted images",
            text,
        )
    elif path.name == "art.html":
        # The gallery is client-rendered, but crawler/social metadata and the
        # visible heading must agree with the generated artwork export.
        count = f"{artworks:,}"
        text = re.sub(r"\b[\d,]+(?=\s+ink-on-paper drawings)", count, text, flags=re.I)
        text = re.sub(r"\b[\d,]+(?=\s+pen(?:-|\s+)and ink drawings)", count, text, flags=re.I)
        text = re.sub(r"\b[\d,]+(?=\s+Pen Drawings)", count, text)
        text = re.sub(r"\b[\d,]+(?=\s+artworks\b)", count, text, flags=re.I)
        text = re.sub(r'("numberOfItems"\s*:\s*)\d+', rf"\g<1>{artworks}", text)
    elif path.name == "videos.html":
        # The timeline derives cards from data/videos.json; keep metadata useful
        # with JavaScript unavailable and for social/crawler previews as well.
        text = re.sub(r"\b[\d,]+\+", f"{videos:,}", text)
    else:
        text = re.sub(r"Last updated: \d{4}-\d{2}-\d{2}", f"Last updated: {date}", text)
        text = re.sub(r"as of \d{4}-\d{2}-\d{2}", f"as of {date}", text)
        text = re.sub(r"\b\d+ exact-name records", f"{public_facts.get('Zenodo exact-name creator records', 0)} exact-name records", text)
        text = re.sub(r"\b\d+ versioned records", f"{public_facts.get('Zenodo ORCID-linked records', 0)} versioned records", text)
        for prefix, suffix in (("public_source_snapshot", "json"), ("public_source_inventory", "json")):
            name = latest_report(prefix, suffix)
            if name:
                text = re.sub(rf"{prefix}_\d{{4}}-\d{{2}}-\d{{2}}\.json", name, text)
    # Discovery pages also link dated generated reports; keep those pointers
    # aligned with the newest report artifacts in the same rebuild.
    if path.name in {"discovery.html", "DISCOVERY.md", "llms.txt"}:
        for prefix, suffix in (
            ("reconciliation", "md"),
            ("asset_size", "json"),
            ("accessibility_static", "json"),
        ):
            name = latest_report(prefix, suffix)
            if name:
                text = re.sub(rf"{prefix}_\d{{4}}-\d{{2}}-\d{{2}}\.{suffix}", name, text)
        # The two QA screenshot manifests live in per-date SUBDIRECTORIES
        # (reports/<prefix>/YYYY-MM-DD/manifest.json), not flat suffixed files,
        # so they need their own rewrite. prune_old_reports.py keeps only the
        # latest set, so these hand-authored links must track that latest date
        # or they rot AND pin the superseded set against pruning.
        for prefix in ("visual-qa", "browser-smoke"):
            latest = latest_source_subdir_file(prefix, "manifest.json", required=False)
            if latest is not None:
                snap_date = latest.parent.name
                text = re.sub(
                    rf"reports/{prefix}/\d{{4}}-\d{{2}}-\d{{2}}/manifest\.json",
                    f"reports/{prefix}/{snap_date}/manifest.json",
                    text,
                )
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if public facts are stale")
    args = parser.parse_args()
    # Do this before examining or writing targets.  A wall-clock fallback would
    # make an invalid/missing revision source appear freshly synchronized;
    # release-facing metadata must instead stop until the generated count
    # snapshot is repaired.
    try:
        counts()
        generated_date()
        generated_month_year()
    except (OSError, SiteFactsError) as exc:
        raise SystemExit(f"site-facts source validation failed: {exc}") from exc
    stale = []
    for path in TARGETS:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = render(path)
        if original != updated:
            stale.append(str(path.relative_to(REPO_ROOT)))
            if not args.check:
                path.write_text(updated, encoding="utf-8")
    if stale and args.check:
        raise SystemExit("stale site facts: " + ", ".join(stale))
    print(("checked" if args.check else "synced") + " site facts for " + ", ".join(stale or ["all targets"]))


if __name__ == "__main__":
    main()
