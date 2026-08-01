#!/usr/bin/env python3
"""Generate CITATION.cff for papers that don't have one, using metadata.json.

For each paper folder under papers/ that lacks a CITATION.cff:
  - Read metadata.json for title, authors, DOI, date, version
  - Generate a CFF 1.2.0 file following the existing pattern
  - Skip if metadata.json is missing or has no title
"""

import json
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
ORCID = "https://orcid.org/0000-0001-6232-9096"


def _yaml_quoted(value: str) -> str:
    """Escape a string for safe embedding in a YAML double-quoted scalar."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def parse_author(name: str) -> dict:
    """Parse a name string into CFF author format."""
    name = name.strip()
    if "," in name:
        parts = [p.strip() for p in name.split(",", 1)]
        return {"family-names": parts[0], "given-names": parts[1] if len(parts) > 1 else ""}
    parts = name.rsplit(None, 1)
    if len(parts) == 2:
        return {"family-names": parts[1], "given-names": parts[0]}
    return {"family-names": name, "given-names": ""}


def generate_cff(meta: dict, paper_dir: Path) -> Optional[str]:
    """Generate CFF content from metadata.json."""
    title = meta.get("title", "")
    if not title:
        return None

    # Determine type
    work_type = meta.get("type", meta.get("resource_type", {}).get("title", "Paper"))
    cff_type = "article"
    if isinstance(work_type, str):
        wt = work_type.lower()
        if "book" in wt:
            cff_type = "book"
        elif "software" in wt or "code" in wt:
            cff_type = "software"
        elif "presentation" in wt or "slide" in wt:
            cff_type = "conference-paper"
        elif "report" in wt:
            cff_type = "report"

    # Date — extract from folder name (YYYY_Topic) if not in metadata
    pub_date = meta.get("publication_date", "")
    if not pub_date:
        year = meta.get("year", "")
        if year:
            pub_date = str(year)
    if not pub_date:
        # Extract year from folder name (e.g. "2015_EhrlichialInfection" -> "2015")
        folder_name = paper_dir.name
        if folder_name[:4].isdigit():
            pub_date = folder_name[:4]
        else:
            pub_date = "2026"

    # DOI
    doi = meta.get("doi", "")
    doi_url = meta.get("doi_url", f"https://doi.org/{doi}" if doi else "")

    # Version
    version = meta.get("version", "")
    if version is None:
        version = ""

    # Authors
    creators = meta.get("creators", [])
    if not creators:
        creators = [{"name": "Daniel A. Friedman"}]

    authors = []
    for creator in creators:
        name = creator.get("name", "") if isinstance(creator, dict) else str(creator)
        if not name:
            continue
        author = parse_author(name)
        # Add ORCID for Daniel Ari Friedman specifically, not any co-author
        # whose surname merely contains "friedman".
        if "daniel" in name.lower() and "friedman" in name.lower():
            author["orcid"] = ORCID
        authors.append(author)

    # Zenodo record
    record_id = meta.get("record_id", "")
    zenodo_url = meta.get("zenodo_record", f"https://zenodo.org/records/{record_id}" if record_id else "")

    # Repository code
    repo_url = ""
    for res in meta.get("related_resources", []):
        url = res.get("url", "") if isinstance(res, dict) else ""
        if "github.com" in url and "docxology" in url:
            repo_url = url
            break

    lines = [
        "cff-version: 1.2.0",
        'message: "If you use this work, please cite it as below."',
        f"type: {cff_type}",
        f'title: "{_yaml_quoted(title)}"',
    ]
    if version:
        lines.append(f'version: "{_yaml_quoted(version)}"')
    lines.append(f"date-released: {pub_date}")
    if doi:
        lines.append(f"doi: {doi}")
        lines.append(f'url: "{doi_url}"')
    if repo_url:
        lines.append(f'repository-code: "{repo_url}"')
    lines.append("authors:")
    for author in authors:
        lines.append(f'  - family-names: "{_yaml_quoted(author.get("family-names", ""))}"')
        lines.append(f'    given-names: "{_yaml_quoted(author.get("given-names", ""))}"')
        if "orcid" in author:
            lines.append(f'    orcid: "{author["orcid"]}"')
    if doi:
        lines.append("identifiers:")
        lines.append(f"  - type: doi")
        lines.append(f"    value: {doi}")
        lines.append(f'    description: "Zenodo DOI"')
        if zenodo_url:
            lines.append(f"  - type: url")
            lines.append(f'    value: "{zenodo_url}"')
            lines.append(f'    description: "Zenodo landing page"')

    return "\n".join(lines) + "\n"


def main():
    force = "--force" in sys.argv
    generated = 0
    skipped = 0

    for paper_dir in sorted(PAPERS_DIR.iterdir()):
        if not paper_dir.is_dir():
            continue

        cff_path = paper_dir / "CITATION.cff"
        if cff_path.exists() and not force:
            skipped += 1
            continue

        meta_path = paper_dir / "metadata.json"
        if not meta_path.is_file():
            skipped += 1
            continue

        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"  ERROR: {paper_dir.name}: invalid metadata.json")
            skipped += 1
            continue

        cff_content = generate_cff(meta, paper_dir)
        if not cff_content:
            print(f"  SKIP: {paper_dir.name}: no title in metadata")
            skipped += 1
            continue

        cff_path.write_text(cff_content, encoding="utf-8")
        generated += 1
        print(f"  WROTE: {paper_dir.name}/CITATION.cff")

    print(f"\n=== Summary ===")
    print(f"  Generated: {generated}")
    print(f"  Skipped (already exists or no data): {skipped}")


if __name__ == "__main__":
    main()
