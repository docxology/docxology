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
from site_facts import counts, generated_date, generated_month_year
TARGETS = [REPO_ROOT / "index.html", REPO_ROOT / "publications.html", REPO_ROOT / "discovery.html", REPO_ROOT / "pages" / "DISCOVERY.md"]


def latest_report(prefix: str, suffix: str) -> str | None:
    paths = sorted((REPO_ROOT / "reports").glob(f"{prefix}_*.{suffix}"))
    return paths[-1].name if paths else None


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
    github = c.get("github_inventory", {})
    public_facts = c.get("public_source_snapshot", {})
    replacements = {
        r"Last updated: (?:May|June|July) 2026": f"Data refreshed {month}",
        r"Data refreshed (?:May|June|July) 2026": f"Data refreshed {month}",
    }
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    if path.name == "index.html":
        text = re.sub(r'<meta name="revised" content="[^"]+">', f'<meta name="revised" content="{date}">', text)
        text = re.sub(r'<meta name="date" content="[^"]+">', f'<meta name="date" content="{date}">', text)
        text = re.sub(r'("dateModified":\s*")[^"]+(")', rf"\g<1>{date}\g<2>", text, count=1)
        text = re.sub(r"Paper Documentation \(\d+ folders, \d+ with full text, [\d,]+ extracted images\)", f"Paper Documentation ({folders} folders, {full_text} with full text, {images:,} extracted images)", text)
        text = re.sub(r"Highlights from the catalog across \d+ research domains", "Highlights from the catalog across 8 research domains", text)
    elif path.name == "publications.html":
        text = re.sub(r"<p class=\"sub\">\d+ works spanning", f"<p class=\"sub\">{works} works spanning", text, count=1)
        text = re.sub(r"as of (?:May|June|July) 2026", f"as of {month}", text, count=1)
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
    if path.name in {"discovery.html", "DISCOVERY.md"}:
        for prefix, suffix in (
            ("reconciliation", "md"),
            ("asset_size", "json"),
            ("accessibility_static", "json"),
        ):
            name = latest_report(prefix, suffix)
            if name:
                text = re.sub(rf"{prefix}_\d{{4}}-\d{{2}}-\d{{2}}\.{suffix}", name, text)
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if public facts are stale")
    args = parser.parse_args()
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
