"""Source-backed author entity types without guessing personal name structure."""
from __future__ import annotations

import json
from pathlib import Path

from docxology_tools.paper_artifacts import source_file


def load_author_records(root: Path) -> dict:
    """Read the eligible reviewed registry once per renderer invocation."""
    path = source_file(root, "data/work-authors.json")
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("works"), dict):
        raise ValueError("work-authors registry must contain a works object")
    return payload["works"]


def verified_author_types(work: dict, records: dict) -> dict[str, str]:
    """Accept explicit types only from verified, exact DOI-bound author records."""
    record = records.get(work.get("citation_key"))
    doi = work.get("doi")
    if not isinstance(record, dict) or record.get("status") != "verified" or not isinstance(doi, str) or not doi.strip():
        return {}
    source_doi = record.get("doi")
    if not isinstance(source_doi, str) or source_doi.strip().casefold() != doi.strip().casefold():
        return {}
    authors = record.get("authors")
    if not isinstance(authors, list):
        return {}
    types: dict[str, set[str]] = {}
    for author in authors:
        if not isinstance(author, dict):
            continue
        literal = author.get("literal")
        if isinstance(literal, str) and literal.strip():
            display, typ = literal.strip(), "Organization"
        else:
            family, given = author.get("family", ""), author.get("given", "")
            if not isinstance(family, str) or not isinstance(given, str):
                continue
            if family.strip():
                display = f"{family.strip()}, {given.strip()}" if given.strip() else family.strip()
            elif given.strip():
                display = given.strip()
            else:
                continue
            typ = "Person"
        types.setdefault(display, set()).add(typ)
    # Conflicting source representations remain unknown, rather than guessing.
    return {name: next(iter(values)) for name, values in types.items() if len(values) == 1}


def author_entity(display_name: str, principal: dict, source_type: str | None = None) -> dict:
    """Preserve author order/name and the established principal identity node."""
    family, separator, given = display_name.partition(",")
    if family.strip() == "Friedman" and given.strip().startswith("Daniel"):
        return principal
    if source_type == "Organization":
        return {"@type": "Organization", "name": display_name}
    name = f"{given.strip()} {family.strip()}".strip() if separator else display_name
    entity = {"name": name}
    if source_type == "Person" or separator:
        entity["@type"] = "Person"
    return entity


def reviewed_contributor_role(work: dict, records: dict) -> str:
    record = records.get(work["citation_key"], {})
    role = record.get("contributor_role", "author")
    if role not in {"author", "editor"}:
        raise ValueError(f"Unsupported contributor role for {work['citation_key']}: {role}")
    if role == "editor":
        names = [f'{a["family"]}, {a["given"]}' for a in record.get("authors", [])]
        if (record.get("status") != "document_verified" or record.get("num") != work["num"]
                or record.get("title") != work["title"] or names != work.get("authors")
                or not record.get("evidence", "").startswith("EDITED BY ")):
            raise ValueError(f"Editor role lacks matching document evidence for {work['citation_key']}")
    return role
