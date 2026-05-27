"""Resume/CV data loading, validation, variant filtering, and text rendering."""

from __future__ import annotations

import json
import re
import textwrap
import unicodedata
from collections.abc import Iterable
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
VARIANTS = ("full", "academic", "software-consulting", "teaching-service")
SOURCE_FILES = (
    "resume/source.json",
    "data/works.json",
    "data/software.json",
    "data/scholar-snapshot.json",
    "data/claims.json",
)

CODA_GLYPH_RE = re.compile(r"[\ue000-\uf8ff\u200b-\u200f\u2028\u2029\u2060\ufeff]")
DOI_WRAP_RE = re.compile(r"10\.\d{4,9}/[^\s]+")
URL_RE = re.compile(r"^https?://")


class ResumeDataError(ValueError):
    """Raised when resume source data is incomplete or inconsistent."""


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ResumeDataError(f"{path} must contain a JSON object")
    return data


def strip_coda_glyphs(value: str) -> str:
    """Remove Coda-export private glyphs and zero-width controls from text."""
    cleaned = unicodedata.normalize("NFKC", CODA_GLYPH_RE.sub("", value))
    cleaned = cleaned.replace("\r\n", "\n").replace("\r", "\n")
    return re.sub(r"[ \t]+", " ", cleaned).strip()


def clean_value(value: Any) -> Any:
    if isinstance(value, str):
        return strip_coda_glyphs(value)
    if isinstance(value, list):
        return [clean_value(item) for item in value]
    if isinstance(value, dict):
        return {str(key): clean_value(item) for key, item in value.items()}
    return value


def _ids(items: Iterable[dict[str, Any]]) -> list[str]:
    return [str(item.get("id", "")) for item in items]


def _require_unique_ids(source: dict[str, Any], section: str) -> None:
    ids = _ids(source.get(section, []))
    if not ids or any(not item for item in ids):
        raise ResumeDataError(f"{section} records must have ids")
    dupes = sorted({item for item in ids if ids.count(item) > 1})
    if dupes:
        raise ResumeDataError(f"{section} duplicate ids: {', '.join(dupes)}")


def _validate_dates(section: str, item: dict[str, Any]) -> None:
    if "start_year" in item and not isinstance(item["start_year"], int):
        raise ResumeDataError(f"{section}:{item.get('id')} start_year must be int")
    if "end_year" in item and item["end_year"] is not None and not isinstance(item["end_year"], int):
        raise ResumeDataError(f"{section}:{item.get('id')} end_year must be int or null")
    if item.get("status") == "ongoing" and item.get("end_year") is not None:
        raise ResumeDataError(f"{section}:{item.get('id')} ongoing records must have end_year null")


def _validate_variants(section: str, item: dict[str, Any]) -> None:
    variants = item.get("variants")
    if not isinstance(variants, list) or "full" not in variants:
        raise ResumeDataError(f"{section}:{item.get('id')} must include full variant")
    invalid = sorted(set(variants) - set(VARIANTS))
    if invalid:
        raise ResumeDataError(f"{section}:{item.get('id')} invalid variants: {', '.join(invalid)}")


def _validate_links(section: str, item: dict[str, Any]) -> None:
    links = item.get("links")
    if not isinstance(links, list) or not links:
        raise ResumeDataError(f"{section}:{item.get('id')} must include at least one source link")
    for link in links:
        if not isinstance(link, dict):
            raise ResumeDataError(f"{section}:{item.get('id')} links must be objects")
        label = str(link.get("label", "")).strip()
        url = str(link.get("url", "")).strip()
        if not label or not URL_RE.search(url):
            raise ResumeDataError(f"{section}:{item.get('id')} invalid source link")


def validate_source(source: dict[str, Any]) -> None:
    required_sections = [
        "profile",
        "contact",
        "education",
        "experience",
        "awards",
        "conferences",
        "media_outreach",
        "service",
        "art_uses",
    ]
    missing = [section for section in required_sections if section not in source]
    if missing:
        raise ResumeDataError("resume/source.json missing sections: " + ", ".join(missing))
    contact = source["contact"]
    for key in ["email", "github", "linkedin", "orcid", "google_scholar", "keybase", "ens", "art_portfolio"]:
        if key not in contact or not contact[key]:
            raise ResumeDataError(f"contact missing required field: {key}")
    if len(source["education"]) < 4:
        raise ResumeDataError("education must include at least 4 records")
    if len(source["experience"]) < 16:
        raise ResumeDataError("experience must include imported work/teaching records")
    if len(source["conferences"]) < 13:
        raise ResumeDataError("conferences must include imported conference records")
    if len(source["media_outreach"]) < 20:
        raise ResumeDataError("media_outreach must include imported media/outreach records")
    if len(source["service"]) < 20:
        raise ResumeDataError("service must include imported service records")
    if len(source["art_uses"]) < 10:
        raise ResumeDataError("art_uses must include imported art-use records")
    for section in ["education", "experience", "awards", "conferences", "media_outreach", "service", "art_uses"]:
        _require_unique_ids(source, section)
        for item in source[section]:
            _validate_dates(section, item)
            _validate_variants(section, item)
            _validate_links(section, item)


def load_resume_inputs(repo_root: Path = REPO_ROOT) -> dict[str, dict[str, Any]]:
    data = {rel: clean_value(load_json(repo_root / rel)) for rel in SOURCE_FILES}
    validate_source(data["resume/source.json"])
    return data


def _claim_by_id(claims: list[dict[str, Any]], claim_id: str) -> dict[str, Any] | None:
    for claim in claims:
        if claim.get("id") == claim_id:
            return claim
    return None


def _metrics(works: dict[str, Any], software: dict[str, Any], scholar: dict[str, Any], claims: dict[str, Any]) -> dict[str, Any]:
    claim_rows = claims.get("claims", [])
    github_claim = _claim_by_id(claim_rows, "docxology-github-public-repos")
    aii_claim = _claim_by_id(claim_rows, "aii-github-public-repos")
    return {
        "works": works["count"],
        "software_catalogued": software["count"],
        "owned_software_catalogued": sum(1 for row in software["repositories"] if row.get("owner") == "docxology"),
        "aii_software_catalogued": sum(
            1 for row in software["repositories"] if row.get("owner") == "ActiveInferenceInstitute"
        ),
        "google_scholar": {
            "citations": scholar["citations"],
            "h_index": scholar["h_index"],
            "i10_index": scholar["i10_index"],
            "as_of": scholar["as_of"],
            "profile_url": scholar["profile_url"],
        },
        "docxology_public_repositories_claim": github_claim,
        "aii_public_repositories_claim": aii_claim,
    }


def build_resume_payload(generated_at: str, repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    inputs = load_resume_inputs(repo_root)
    source = inputs["resume/source.json"]
    works = inputs["data/works.json"]
    software = inputs["data/software.json"]
    scholar = inputs["data/scholar-snapshot.json"]
    claims = inputs["data/claims.json"]
    return {
        "generated_at": generated_at,
        "source_files": list(SOURCE_FILES),
        "profile": source["profile"],
        "contact": source["contact"],
        "metrics": _metrics(works, software, scholar, claims),
        "education": source["education"],
        "experience": source["experience"],
        "awards": source["awards"],
        "conferences": source["conferences"],
        "media_outreach": source["media_outreach"],
        "service": source["service"],
        "art_uses": source["art_uses"],
        "works": works["works"],
        "software": software["repositories"],
        "claims": claims["claims"],
        "variants": {
            "full": "Complete CV with all structured resume sections, works, and software.",
            "academic": "Academic CV variant emphasizing education, research, works, awards, conferences, and service.",
            "software-consulting": "Software and consulting variant emphasizing systems work, software, and applied Active Inference.",
            "teaching-service": "Teaching and service variant emphasizing education, courses, media, outreach, and community work.",
        },
    }


def item_in_variant(item: dict[str, Any], variant: str) -> bool:
    if variant == "full":
        return True
    return variant in item.get("variants", [])


def filter_items(items: list[dict[str, Any]], variant: str) -> list[dict[str, Any]]:
    return [item for item in items if item_in_variant(item, variant)]


def filtered_works(works: list[dict[str, Any]], variant: str) -> list[dict[str, Any]]:
    if variant in ("full", "academic"):
        return works
    if variant == "software-consulting":
        return [
            work
            for work in works
            if work.get("domain_name") in {"Computational", "Active Inference", "Cognitive Security"}
            or work.get("type") in {"Paper", "Book", "Presentation"}
        ]
    if variant == "teaching-service":
        return [
            work
            for work in works
            if work.get("domain_name") in {"Media & Teaching", "Active Inference", "Entomology"}
            or work.get("type") in {"Course", "Series", "Playbook"}
        ]
    raise ResumeDataError(f"unknown variant: {variant}")


def filtered_software(software: list[dict[str, Any]], variant: str) -> list[dict[str, Any]]:
    if variant in ("full", "software-consulting"):
        return software
    if variant == "academic":
        return [row for row in software if row.get("paper_path") or row.get("zenodo_url")]
    if variant == "teaching-service":
        needles = ("biology", "course", "education", "journal", "textbook", "video")
        return [
            row
            for row in software
            if any(needle in " ".join([row.get("name", ""), row.get("description", "")]).lower() for needle in needles)
        ]
    raise ResumeDataError(f"unknown variant: {variant}")


def date_range(item: dict[str, Any]) -> str:
    start = item.get("start_year")
    end = item.get("end_year")
    if start is None and item.get("year") is not None:
        return str(item["year"])
    if start is None:
        return "All"
    if item.get("status") == "ongoing" or end is None:
        return f"{start}-ongoing"
    if start == end:
        return str(start)
    return f"{start}-{end}"


def _line(label: str, value: Any) -> str:
    if isinstance(value, list):
        value = "; ".join(str(item) for item in value)
    return f"{label}: {value}"


def _append_wrapped(lines: list[str], text: str, *, indent: str = "  ", width: int = 100) -> None:
    if DOI_WRAP_RE.search(text):
        lines.append(indent + text)
        return
    lines.extend(textwrap.wrap(text, width=width, initial_indent=indent, subsequent_indent=indent))


def _section(lines: list[str], title: str) -> None:
    lines.extend(["", title.upper(), "-" * len(title)])


def _render_record(lines: list[str], heading: str, details: list[str] | None = None) -> None:
    lines.append(heading)
    for detail in details or []:
        _append_wrapped(lines, f"- {detail}", indent="  ")


def _links_text(item: dict[str, Any]) -> str:
    links = item.get("links", [])
    if not links:
        return ""
    return "Sources: " + "; ".join(f"{link['label']}: {link['url']}" for link in links)


def _details_with_links(item: dict[str, Any], details: list[str] | None = None) -> list[str]:
    rendered = list(details or [])
    links = _links_text(item)
    if links:
        rendered.append(links)
    return rendered


def render_text(payload: dict[str, Any], variant: str) -> str:
    if variant not in VARIANTS:
        raise ResumeDataError(f"unknown variant: {variant}")
    profile = payload["profile"]
    contact = payload["contact"]
    metrics = payload["metrics"]
    lines = [
        f"{profile['name']}, {profile['credential']}",
        profile["headline"],
        profile["location"],
        "",
        _line("Email", contact["email"]),
        _line("Sites", contact["personal_sites"]),
        _line("GitHub", contact["github"]),
        _line("LinkedIn", contact["linkedin"]),
        _line("Google Scholar", contact["google_scholar"]),
        _line("ORCID", contact["orcid"]),
        _line("Keybase", contact["keybase"]),
        _line("ENS", contact["ens"]),
        _line("Art portfolio", contact["art_portfolio"]),
        _line("Voice/Text", contact["voice_text"]),
        "",
        f"Variant: {variant}",
        f"Generated: {payload['generated_at']}",
        "",
        f"Current public metrics: {metrics['works']} curated works; {metrics['software_catalogued']} catalogued software repositories "
        f"({metrics['owned_software_catalogued']} owned + {metrics['aii_software_catalogued']} AII); "
        f"{metrics['google_scholar']['citations']} Google Scholar citations, h-index {metrics['google_scholar']['h_index']}, "
        f"i10-index {metrics['google_scholar']['i10_index']} as of {metrics['google_scholar']['as_of']}.",
    ]
    _section(lines, "Summary")
    _append_wrapped(lines, profile["summary"], indent="")

    _section(lines, "Education")
    for item in filter_items(payload["education"], variant):
        _render_record(
            lines,
            f"{date_range(item)} | {item['degree']} | {item['institution']} | {item['location']}",
            _details_with_links(item, item.get("details", [])),
        )

    _section(lines, "Experience")
    for item in filter_items(payload["experience"], variant):
        roles = ", ".join(item["roles"])
        _render_record(
            lines,
            f"{date_range(item)} | {item['category']} | {item['workplace']} | {roles}",
            _details_with_links(item, [item["description"]]),
        )

    _section(lines, "Awards and Fellowships")
    for item in filter_items(payload["awards"], variant):
        _render_record(lines, f"{item['year']} | {item['name']}", _details_with_links(item, [item["details"]]))

    works = filtered_works(payload["works"], variant)
    _section(lines, f"Works and Publications ({len(works)})")
    for work in works:
        link = work.get("doi") or work.get("url") or ""
        link_text = f" | {link}" if link else ""
        lines.append(f"[{work['num']:03d}] {work['year']} | {work['type']} | {work['title']} | {work['venue']}{link_text}")

    software = filtered_software(payload["software"], variant)
    _section(lines, f"Software ({len(software)})")
    for row in software:
        desc = row.get("description", "")
        paper = f" | paper: {row['paper_path']}" if row.get("paper_path") else ""
        zenodo = f" | zenodo: {row['zenodo_url']}" if row.get("zenodo_url") else ""
        lines.append(f"{row['owner']}/{row['name']} | {row.get('language') or 'unspecified'} | {row['url']} | {desc}{paper}{zenodo}")

    _section(lines, "Conferences, Posters, Seminars, Workshops")
    for item in filter_items(payload["conferences"], variant):
        detail = " ".join(part for part in [item.get("details", ""), item.get("date", "")] if part)
        links = _links_text(item)
        suffix = f" | {detail}" if detail else ""
        source_suffix = f" | {links}" if links else ""
        lines.append(f"{item['year']} | {item['type']} | {item['event']} | {item['title']}{suffix}{source_suffix}")

    _section(lines, "Science Engagement, Outreach, Quotes, Articles")
    for item in filter_items(payload["media_outreach"], variant):
        source = f" | {item['source']}" if item.get("source") else ""
        detail = f" | {item['details']}" if item.get("details") else ""
        links = _links_text(item)
        source_links = f" | {links}" if links else ""
        lines.append(f"{item['year']} | {item['type']} | {item['name']}{source}{detail}{source_links}")

    _section(lines, "Professional Participation, Engagement, and Service")
    for item in filter_items(payload["service"], variant):
        links = _links_text(item)
        source_suffix = f" | {links}" if links else ""
        lines.append(f"{date_range(item)} | {item['group']} | {item['type']} | {item['description']}{source_suffix}")

    if variant == "full":
        _section(lines, "Art Portfolio and Uses")
        for item in payload["art_uses"]:
            year = item["year"] if item["year"] is not None else "All"
            links = _links_text(item)
            source_suffix = f" | {links}" if links else ""
            lines.append(f"{year} | {item['name']} | {item['description']}{source_suffix}")

    text = "\n".join(lines).rstrip() + "\n"
    if CODA_GLYPH_RE.search(text):
        raise ResumeDataError("rendered text contains Coda export glyphs")
    return text


def json_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
