#!/usr/bin/env python3
"""Create and synchronize per-paper CFF citation DOI roles.

``pages/BIBLIOGRAPHY.md`` owns a work's canonical citation DOI. The matching
``papers/*/metadata.json`` stores that value in ``doi`` and may store a
version-specific download identifier in ``artifact_doi``. A paper CFF must
therefore expose the canonical DOI in its top-level ``doi`` and ``url``
fields, while retaining a distinct artifact DOI only as explicitly labelled
secondary identifier metadata.

The synchronizer deliberately owns only these DOI-role fields. Existing
non-DOI CFF content, including historical GitHub-release identifiers, remains
untouched. That avoids replacing hand-curated provenance with an incomplete
metadata projection while still making the citation identity deterministic and
checkable.

Usage:
    uv run python3 code/orchestrators/generate_citation_cff.py
        Create CFF files that are missing entirely (legacy behaviour).
    uv run python3 code/orchestrators/generate_citation_cff.py --apply
        Reconcile DOI-role fields in every renderable CFF.
    uv run python3 code/orchestrators/generate_citation_cff.py --check
        Render the same DOI-role mapping without writing and fail on drift.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS_DIR = REPO_ROOT / "papers"
ORCID = "https://orcid.org/0000-0001-6232-9096"
sys.path.insert(0, str(REPO_ROOT / "code" / "src"))

from generated_outputs import stale_output_paths, write_output_texts  # noqa: E402


DOI_RE = re.compile(r"^10\.\d{4,9}/[-._;()/:A-Z0-9]+$", re.IGNORECASE)
TOP_LEVEL_FIELD_RE = re.compile(r"^(?:doi|url):")
IDENTIFIER_TYPE_RE = re.compile(r"^  - type:\s*(.*?)\s*$", re.MULTILINE)
IDENTIFIER_VALUE_RE = re.compile(r"^    value:\s*(.*?)\s*$", re.MULTILINE)
ARTIFACT_LABEL_RE = re.compile(r"\b(?:artifact|version|download)\b", re.IGNORECASE)


def _yaml_quoted(value: str) -> str:
    """Escape a string for safe embedding in a YAML double-quoted scalar."""
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _yaml_unquoted(value: str) -> str:
    """Read the restricted scalar form emitted by this CFF renderer."""
    value = value.strip()
    if len(value) >= 2 and value[:1] == value[-1:] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def normalize_doi(value: object, *, field: str, paper_dir: Path) -> str:
    """Return a strict bare DOI or reject malformed non-empty metadata."""
    doi = str(value or "").strip()
    if doi and not DOI_RE.fullmatch(doi):
        raise ValueError(f"{paper_dir.name}: {field} must be a bare DOI, got {doi!r}")
    return doi


def doi_role_values(meta: dict[str, Any], paper_dir: Path) -> tuple[str, str]:
    """Return canonical and optional artifact DOI values under one field contract."""
    legacy_version_doi = str(meta.get("version_doi") or "").strip()
    if legacy_version_doi:
        raise ValueError(
            f"{paper_dir.name}: version_doi is unsupported; use artifact_doi for a version/download DOI"
        )
    canonical = normalize_doi(meta.get("doi"), field="doi", paper_dir=paper_dir)
    artifact = normalize_doi(meta.get("artifact_doi"), field="artifact_doi", paper_dir=paper_dir)
    if artifact and not canonical:
        raise ValueError(
            f"{paper_dir.name}: artifact_doi requires a canonical doi citation identity"
        )
    return canonical, artifact


def doi_resolver(doi: str) -> str:
    """Return the canonical resolver URL for a validated DOI."""
    return f"https://doi.org/{doi}" if doi else ""


def zenodo_record_url(doi: str) -> str:
    """Return an immutable Zenodo landing URL only for a Zenodo version DOI."""
    match = re.fullmatch(r"10\.5281/zenodo\.(\d+)", doi, re.IGNORECASE)
    return f"https://zenodo.org/records/{match.group(1)}" if match else ""


def parse_author(name: str) -> dict[str, str]:
    """Parse a name string into CFF author format."""
    name = name.strip()
    if "," in name:
        parts = [part.strip() for part in name.split(",", 1)]
        return {"family-names": parts[0], "given-names": parts[1] if len(parts) > 1 else ""}
    parts = name.rsplit(None, 1)
    if len(parts) == 2:
        return {"family-names": parts[1], "given-names": parts[0]}
    return {"family-names": name, "given-names": ""}


def _identifier_entry(identifier_type: str, value: str, description: str) -> list[str]:
    return [
        f"  - type: {identifier_type}\n",
        f'    value: "{_yaml_quoted(value)}"\n',
        f'    description: "{_yaml_quoted(description)}"\n',
    ]


def doi_role_identifier_entries(canonical: str, artifact: str) -> list[str]:
    """Render CFF entries that distinguish citation and artifact DOI roles."""
    entries: list[str] = []
    if canonical:
        entries.extend(_identifier_entry("doi", canonical, "Canonical citation DOI"))
        entries.extend(
            _identifier_entry("url", doi_resolver(canonical), "Canonical citation DOI resolver")
        )
    if artifact and artifact.casefold() != canonical.casefold():
        entries.extend(_identifier_entry("doi", artifact, "Version/download DOI (Zenodo artifact)"))
        entries.extend(
            _identifier_entry(
                "url",
                doi_resolver(artifact),
                "Version/download DOI resolver (Zenodo artifact)",
            )
        )
        artifact_record = zenodo_record_url(artifact)
        if artifact_record:
            entries.extend(
                _identifier_entry(
                    "url", artifact_record, "Version/download landing page (Zenodo artifact)"
                )
            )
    return entries


def _repository_code(meta: dict[str, Any]) -> str:
    for resource in meta.get("related_resources", []):
        url = resource.get("url", "") if isinstance(resource, dict) else ""
        if isinstance(url, str) and url.startswith("https://github.com/"):
            return url
    github_repo = meta.get("github_repo")
    if isinstance(github_repo, str) and github_repo.strip():
        return f"https://github.com/{github_repo.strip()}"
    return ""


def _release_date(meta: dict[str, Any], paper_dir: Path) -> str:
    publication_date = str(meta.get("publication_date") or meta.get("year") or "").strip()
    if publication_date:
        return publication_date
    if paper_dir.name[:4].isdigit():
        return paper_dir.name[:4]
    raise ValueError(f"{paper_dir.name}: metadata needs publication_date or year for CITATION.cff")


def _cff_type(meta: dict[str, Any]) -> str:
    work_type = meta.get("type", meta.get("resource_type", {}).get("title", "Paper"))
    if not isinstance(work_type, str):
        return "article"
    value = work_type.lower()
    if "book" in value:
        return "book"
    if "software" in value or "code" in value:
        return "software"
    if "presentation" in value or "slide" in value:
        return "conference-paper"
    if "report" in value:
        return "report"
    return "article"


def generate_cff(meta: dict[str, Any], paper_dir: Path) -> str | None:
    """Create a complete CFF for a missing paper folder from metadata source."""
    title = str(meta.get("title") or "").strip()
    if not title:
        return None
    canonical, artifact = doi_role_values(meta, paper_dir)
    version = meta.get("version")
    lines = [
        "cff-version: 1.2.0",
        'message: "If you use this work, please cite it as below."',
        f"type: {_cff_type(meta)}",
        f'title: "{_yaml_quoted(title)}"',
    ]
    if version is not None and str(version).strip():
        lines.append(f'version: "{_yaml_quoted(str(version))}"')
    lines.append(f"date-released: {_release_date(meta, paper_dir)}")
    if canonical:
        lines.extend([f"doi: {canonical}", f'url: "{doi_resolver(canonical)}"'])
    repository_code = _repository_code(meta)
    if repository_code:
        lines.append(f'repository-code: "{_yaml_quoted(repository_code)}"')
    lines.append("authors:")
    creators = meta.get("creators") or [{"name": "Daniel A. Friedman"}]
    for creator in creators:
        name = creator.get("name", "") if isinstance(creator, dict) else str(creator)
        if not name:
            continue
        author = parse_author(name)
        lines.append(f'  - family-names: "{_yaml_quoted(author["family-names"])}"')
        lines.append(f'    given-names: "{_yaml_quoted(author["given-names"])}"')
        if "daniel" in name.lower() and "friedman" in name.lower():
            lines.append(f'    orcid: "{ORCID}"')
    identifiers = doi_role_identifier_entries(canonical, artifact)
    github_release_url = str(meta.get("github_release_url") or "").strip()
    if github_release_url:
        identifiers.extend(_identifier_entry("url", github_release_url, "GitHub release"))
    if identifiers:
        lines.append("identifiers:")
        lines.extend(line.rstrip("\n") for line in identifiers)
    return "\n".join(lines) + "\n"


def _top_level_value(text: str, key: str) -> str:
    match = re.search(rf"^{re.escape(key)}:\s*(.*?)\s*$", text, re.MULTILINE)
    return _yaml_unquoted(match.group(1)) if match else ""


def _identifier_entries(text: str) -> tuple[list[str], list[str], list[str]]:
    """Split a CFF around its identifier list while preserving non-managed entries."""
    lines = text.splitlines(keepends=True)
    start = next((index for index, line in enumerate(lines) if line.rstrip("\n") == "identifiers:"), None)
    if start is None:
        return lines, [], []
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.strip() and not line.startswith((" ", "\t")):
            end = index
            break
    entries: list[list[str]] = []
    current: list[str] = []
    for line in lines[start + 1 : end]:
        if line.startswith("  - type:"):
            if current:
                entries.append(current)
            current = [line]
        elif current:
            current.append(line)
        else:
            # Retain unusual content as an opaque entry rather than discarding it.
            current = [line]
    if current:
        entries.append(current)
    return lines[:start], ["".join(entry) for entry in entries], lines[end:]


def _identifier_fields(entry: str) -> tuple[str, str, str]:
    identifier_type = ""
    value = ""
    description = ""
    type_match = IDENTIFIER_TYPE_RE.search(entry)
    value_match = IDENTIFIER_VALUE_RE.search(entry)
    description_match = re.search(r"^    description:\s*(.*?)\s*$", entry, re.MULTILINE)
    if type_match:
        identifier_type = _yaml_unquoted(type_match.group(1))
    if value_match:
        value = _yaml_unquoted(value_match.group(1))
    if description_match:
        description = _yaml_unquoted(description_match.group(1))
    return identifier_type, value, description


def _is_managed_doi_identifier(entry: str) -> bool:
    identifier_type, value, _description = _identifier_fields(entry)
    normalized_type = identifier_type.casefold()
    normalized_value = value.casefold()
    return normalized_type == "doi" or "doi.org/" in normalized_value or "zenodo.org/records/" in normalized_value


def _artifact_identifier_is_explicit(text: str, artifact: str) -> bool:
    _before, entries, _after = _identifier_entries(text)
    for entry in entries:
        identifier_type, value, description = _identifier_fields(entry)
        if identifier_type.casefold() == "doi" and value.casefold() == artifact.casefold():
            return bool(ARTIFACT_LABEL_RE.search(description))
    return False


def cff_doi_role_errors(text: str, meta: dict[str, Any], paper_dir: Path) -> list[str]:
    """Return every citation-identity mismatch without changing the CFF."""
    canonical, artifact = doi_role_values(meta, paper_dir)
    top_doi = _top_level_value(text, "doi")
    top_url = _top_level_value(text, "url")
    errors: list[str] = []
    if canonical:
        if top_doi.casefold() != canonical.casefold():
            errors.append(f"top-level doi must be canonical {canonical}")
        expected_url = doi_resolver(canonical)
        if top_url.casefold() != expected_url.casefold():
            errors.append(f"top-level url must resolve canonical DOI {canonical}")
    elif top_doi:
        errors.append("CFF declares a top-level doi but metadata has no canonical doi")
    if artifact and artifact.casefold() != canonical.casefold() and not _artifact_identifier_is_explicit(text, artifact):
        errors.append(f"artifact DOI {artifact} must be an explicitly labelled secondary identifier")
    return errors


def _replace_top_level_doi_fields(text: str, canonical: str) -> str:
    """Replace CFF primary DOI fields without disturbing other top-level metadata."""
    lines = [line for line in text.splitlines(keepends=True) if not TOP_LEVEL_FIELD_RE.match(line)]
    if not canonical:
        return "".join(lines)
    insert_after = next(
        (index for index, line in enumerate(lines) if line.startswith("date-released:")),
        None,
    )
    if insert_after is None:
        raise ValueError("CITATION.cff is missing date-released; cannot place canonical DOI fields")
    lines[insert_after + 1 : insert_after + 1] = [
        f"doi: {canonical}\n",
        f'url: "{doi_resolver(canonical)}"\n',
    ]
    return "".join(lines)


def _replace_doi_identifier_entries(text: str, canonical: str, artifact: str) -> str:
    before, existing_entries, after = _identifier_entries(text)
    retained = [entry for entry in existing_entries if not _is_managed_doi_identifier(entry)]
    managed = doi_role_identifier_entries(canonical, artifact)
    if not managed and not retained:
        return "".join(before + after)
    rendered = ["identifiers:\n", *managed]
    for entry in retained:
        rendered.append(entry if entry.endswith("\n") else f"{entry}\n")
    return "".join(before + rendered + after)


def reconcile_cff_doi_roles(text: str, meta: dict[str, Any], paper_dir: Path) -> str:
    """Return a CFF with only stale DOI-role fields normalized from metadata."""
    if not cff_doi_role_errors(text, meta, paper_dir):
        return text
    canonical, artifact = doi_role_values(meta, paper_dir)
    return _replace_doi_identifier_entries(
        _replace_top_level_doi_fields(text, canonical), canonical, artifact
    )


def render_outputs(papers_dir: Path = PAPERS_DIR) -> dict[Path, str]:
    """Render every CFF DOI-role output from metadata and existing non-DOI content."""
    outputs: dict[Path, str] = {}
    for paper_dir in sorted(path for path in papers_dir.iterdir() if path.is_dir()):
        metadata_path = paper_dir / "metadata.json"
        if not metadata_path.is_file():
            continue
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{paper_dir.name}: invalid metadata.json: {exc}") from exc
        if not isinstance(metadata, dict):
            raise ValueError(f"{paper_dir.name}: metadata.json must contain a JSON object")
        cff_path = paper_dir / "CITATION.cff"
        if cff_path.is_file():
            existing = cff_path.read_text(encoding="utf-8")
            outputs[cff_path] = reconcile_cff_doi_roles(existing, metadata, paper_dir)
        else:
            generated = generate_cff(metadata, paper_dir)
            if generated is not None:
                outputs[cff_path] = generated
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="fail if any CFF DOI-role fields are stale")
    mode.add_argument("--apply", action="store_true", help="write every stale CFF DOI-role rendering")
    mode.add_argument(
        "--force",
        action="store_true",
        help="legacy alias for --apply; retained for existing maintenance callers",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        outputs = render_outputs()
        stale = stale_output_paths(outputs, repo_root=REPO_ROOT)
        if args.check:
            if stale:
                shown = "\n".join(f"  - {path.relative_to(REPO_ROOT)}" for path in stale)
                raise SystemExit(f"Stale CITATION.cff DOI-role outputs:\n{shown}")
            print(f"Checked {len(outputs)} CFF DOI-role outputs")
            return
        if args.apply or args.force:
            write_output_texts({path: outputs[path] for path in stale}, repo_root=REPO_ROOT)
            print(f"Applied {len(stale)} CFF DOI-role updates")
            return
        missing = {path: content for path, content in outputs.items() if not path.exists()}
        write_output_texts(missing, repo_root=REPO_ROOT)
        print(f"Generated {len(missing)} missing CFF files; use --apply to synchronize existing DOI roles")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"CFF generation failed: {exc}") from exc


if __name__ == "__main__":
    main()
