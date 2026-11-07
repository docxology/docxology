"""Source-backed author entity types without guessing personal name structure."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from docxology_tools.paper_artifacts import source_file


def load_author_records(root: Path) -> dict:
    """Read the eligible reviewed registry once per renderer invocation."""
    path = source_file(root, "data/work-authors.json")
    if path is None:
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("works"), dict):
        raise ValueError("work-authors registry must contain a works object")
    for key, record in payload["works"].items():
        if isinstance(record, dict) and "literal_credit_review" in record:
            validate_literal_credit_review(root, key, record)
    return payload["works"]


def _credit_names(record: dict) -> list[str]:
    authors = record.get("authors")
    if not isinstance(authors, list) or not authors:
        raise ValueError("Reviewed literal credits require an ordered authors list")
    names = []
    for author in authors:
        if (
            not isinstance(author, dict)
            or not isinstance(author.get("literal"), str)
            or not author["literal"].strip()
            or author["literal"] != author["literal"].strip()
            or author.get("entity_type", "Organization")
            not in {"Organization", "Unspecified"}
            or "family" in author
            or "given" in author
        ):
            raise ValueError(
                "Reviewed credits must retain literal names and supported entity types"
            )
        names.append(author["literal"])
    return names


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate literal-credit evidence field")
        result[key] = value
    return result


def validate_literal_credit_review(root: Path, key: str, record: dict) -> None:
    """Validate a frozen, attributed credit review; this is not a live lookup."""
    review = record.get("literal_credit_review")
    if (
        not isinstance(review, dict)
        or type(review.get("schema_version")) is not int
        or review["schema_version"] != 1
    ):
        raise ValueError(f"{key}: invalid literal-credit review")
    if (
        record.get("status") != "verified"
        or type(record.get("num")) is not int
        or record["num"] < 1
        or not isinstance(record.get("doi"), str)
        or not record["doi"]
        or not isinstance(record.get("title"), str)
        or not record["title"]
    ):
        raise ValueError(
            f"{key}: literal-credit authority requires a verified work identity"
        )
    for field in ("reviewed_by", "reason"):
        if not isinstance(review.get(field), str) or not review[field].strip():
            raise ValueError(f"{key}: missing literal-credit {field}")
    when = review.get("reviewed_at")
    if not isinstance(when, str):
        raise ValueError(f"{key}: literal-credit review requires a timestamp")
    parsed = datetime.fromisoformat(when.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed > datetime.now(timezone.utc):
        raise ValueError(
            f"{key}: literal-credit timestamp is unqualified or future-dated"
        )
    name = review.get("source")
    if not isinstance(name, str):
        raise ValueError(f"{key}: missing literal-credit source")
    rel = PurePosixPath(name)
    if (
        len(rel.parts) != 3
        or rel.parts[0] != "papers"
        or rel.parts[2] != "source_evidence.json"
        or rel.is_absolute()
        or ".." in rel.parts
        or "\\" in name
        or any(
            (root / Path(*rel.parts[:i])).is_symlink()
            for i in range(1, len(rel.parts) + 1)
        )
    ):
        raise ValueError(
            f"{key}: literal-credit source must be an independent paper sidecar"
        )
    path = root / name
    if not path.is_file() or path.stat().st_nlink != 1:
        raise ValueError(f"{key}: literal-credit source is unavailable or linked")
    with path.open("rb") as stream:
        raw = stream.read(1_048_577)
    if len(raw) > 1_048_576 or hashlib.sha256(raw).hexdigest() != review.get(
        "source_sha256"
    ):
        raise ValueError(
            f"{key}: literal-credit source hash mismatch or excessive size"
        )
    evidence = json.loads(raw, object_pairs_hook=_unique_object)
    registry = (
        evidence.get("registry_observation") if isinstance(evidence, dict) else None
    )
    if not isinstance(registry, dict):
        raise ValueError(
            f"{key}: literal-credit source requires raw registry observation"
        )
    creators = registry.get("creators")
    if (
        not isinstance(creators, list)
        or not creators
        or any(
            not isinstance(c, dict)
            or not isinstance(c.get("name"), str)
            or not c["name"].strip()
            for c in creators
        )
    ):
        raise ValueError(f"{key}: invalid frozen creator list")
    creators_sha = hashlib.sha256(
        json.dumps(
            creators, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    ).hexdigest()
    names = _credit_names(record)
    document = evidence.get("document_observation")
    if (
        not isinstance(review.get("record_id"), str)
        or not review["record_id"].isdigit()
        or registry.get("record_id") != review["record_id"]
        or registry.get("version") != review.get("version")
        or creators_sha != review.get("creators_sha256")
        or registry.get("title") != record["title"]
        or record["doi"].casefold()
        not in {
            str(registry.get("doi", "")).casefold(),
            str(registry.get("conceptdoi", "")).casefold(),
        }
        or names != [c["name"] for c in creators]
        or not isinstance(document, dict)
        or document.get("credit_labels") != names
        or record.get("registry_baseline")
        != {"creators": creators, "title": record["title"]}
    ):
        raise ValueError(
            f"{key}: literal-credit source/registry/document binding mismatch"
        )


def reviewed_literal_authors(work: dict, records: dict) -> list[dict] | None:
    """Use reviewed structure only for the exact current citation and byline."""
    key = work.get("citation_key")
    record = records.get(key)
    if not isinstance(record, dict) or "literal_credit_review" not in record:
        return None
    names = _credit_names(record)
    doi = work.get("doi")
    if (
        type(work.get("num")) is not int
        or work["num"] != record.get("num")
        or work.get("title") != record.get("title")
        or not isinstance(doi, str)
        or doi.casefold() != str(record.get("doi", "")).casefold()
        or work.get("authors") != names
    ):
        raise ValueError(
            f"{key}: literal-credit authority does not match current bibliography"
        )
    folder = work.get("docs_path")
    if folder and not record["literal_credit_review"]["source"].startswith(
        folder.rstrip("/") + "/"
    ):
        raise ValueError(
            f"{key}: literal-credit source does not match current paper folder"
        )
    return record["authors"]


def verified_author_types(work: dict, records: dict) -> dict[str, str]:
    """Accept explicit types only from verified, exact DOI-bound author records."""
    record = records.get(work.get("citation_key"))
    reviewed_literal_authors(work, records)
    doi = work.get("doi")
    if (
        not isinstance(record, dict)
        or record.get("status") != "verified"
        or not isinstance(doi, str)
        or not doi.strip()
    ):
        return {}
    source_doi = record.get("doi")
    if (
        not isinstance(source_doi, str)
        or source_doi.strip().casefold() != doi.strip().casefold()
    ):
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
            display = literal.strip()
            typ = (
                author.get("entity_type", "Organization")
                if "literal_credit_review" in record
                else "Organization"
            )
        else:
            family, given = author.get("family", ""), author.get("given", "")
            if not isinstance(family, str) or not isinstance(given, str):
                continue
            if family.strip():
                display = (
                    f"{family.strip()}, {given.strip()}"
                    if given.strip()
                    else family.strip()
                )
            elif given.strip():
                display = given.strip()
            else:
                continue
            typ = "Person"
        types.setdefault(display, set()).add(typ)
    # Conflicting source representations remain unknown, rather than guessing.
    return {
        name: next(iter(values)) for name, values in types.items() if len(values) == 1
    }


def author_entity(
    display_name: str, principal: dict, source_type: str | None = None
) -> dict:
    """Preserve author order/name and the established principal identity node."""
    if source_type == "Unspecified":
        return {"name": display_name}
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
        raise ValueError(
            f"Unsupported contributor role for {work['citation_key']}: {role}"
        )
    if role == "editor":
        names = [f"{a['family']}, {a['given']}" for a in record.get("authors", [])]
        if (
            record.get("status") != "document_verified"
            or record.get("num") != work["num"]
            or record.get("title") != work["title"]
            or names != work.get("authors")
            or not record.get("evidence", "").startswith("EDITED BY ")
        ):
            raise ValueError(
                f"Editor role lacks matching document evidence for {work['citation_key']}"
            )
    return role


def bibliography_contributor_role(
    num: int, title: str, authors: list[str], records: dict, identifiers: dict | None
) -> str:
    """Bind roles through permanent identities rather than mutable record numbers."""
    if not records:
        return "author"
    if identifiers is None:
        raise ValueError("Contributor roles require permanent work identifiers")
    from docxology_tools.work_identifiers import key_for_num

    key = key_for_num(num, identifiers)
    if not isinstance(records.get(key, {}), dict):
        raise ValueError(f"Invalid contributor record for {key}")
    return reviewed_contributor_role(
        {"citation_key": key, "num": num, "title": title, "authors": authors}, records
    )
