"""Privacy projection for owned-repository links.

Only the observed public inventory authorizes owned-repository links.
Literal historical documents and their extraction evidence remain unchanged.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
URL_RX = re.compile('(?:https?://|(?:ssh://)?git@github\\.com[:/]|//(?=(?:www\\.)?(?:github\\.com|raw\\.githubusercontent\\.com|api\\.github\\.com)/)|(?<![\\w@])(?=(?:www\\.)?(?:github\\.com|raw\\.githubusercontent\\.com|api\\.github\\.com)/))[^\\s<>"\'()\\[\\]]+', re.I)
POLICY = "public-owned-repositories-v1"


def evidence_entries(root: Path = ROOT) -> list[dict]:
    """Read the closed, byte-bound ledger of retained literal evidence."""
    path = root / "data/public-link-evidence.json"
    entries = json.loads(path.read_text())["entries"] if path.is_file() else []
    seen = set()
    for entry in entries:
        name = entry["path"]
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or name != relative.as_posix() or name in seen:
            raise ValueError("Invalid retained evidence path")
        seen.add(name)
        if entry["class"] == "superseded-report":
            valid = name.startswith("reports/")
        else:
            valid = entry["class"] == "archived-document-extraction" and name.startswith("papers/") and relative.name.startswith("full_text")
        if not valid or not re.fullmatch(r"[a-f0-9]{64}", entry["sha256"]):
            raise ValueError("Invalid retained evidence binding")
        if "projection" in entry and not re.fullmatch(r"reports/public_projection_[A-Za-z0-9_.-]+", entry["projection"]):
            raise ValueError("Invalid public report projection path")
    return entries


def projected_report(path: Path, root: Path = ROOT) -> Path:
    """Resolve a reviewed public copy while retaining the original observation."""
    name = path.relative_to(root).as_posix()
    for entry in evidence_entries(root):
        if entry["path"] != name or "projection" not in entry:
            continue
        target = root / entry["projection"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"] or hashlib.sha256(target.read_bytes()).hexdigest() != entry["projection_sha256"]:
            raise ValueError("Stale public report projection")
        return target
    return path


def owned_repository(url: str) -> str:
    normalized = re.sub(r"(?i)^(?:ssh://)?git@github\.com[:/]", "https://github.com/", url)
    if normalized.startswith("//"):
        normalized = "https:" + normalized
    elif not re.match(r"https?://", normalized, re.I):
        normalized = "https://" + normalized
    parsed = urlsplit(normalized.rstrip(".,;:!?"))
    parts = unquote(parsed.path).strip("/").split("/")
    if parsed.hostname and parsed.hostname.casefold() in {"github.com", "www.github.com", "raw.githubusercontent.com", "api.github.com"}:
        if parsed.hostname.casefold() == "api.github.com" and parts[0].casefold() == "repos":
            parts = parts[1:]
    else:
        return ""
    if len(parts) >= 2 and parts[0].casefold() in {"docxology", "activeinferenceinstitute"}:
        slug = re.match(r"[A-Za-z0-9_.-]+", parts[1])
        return (parts[0] + "/" + slug.group().casefold().rstrip(".").removesuffix(".git")).casefold() if slug else ""
    return ""


def public_repositories(root: Path = ROOT) -> frozenset[str]:
    payload = json.loads((root / "data/github-repositories.json").read_text())
    public = [row for row in payload["repositories"] if row.get("private") is False]
    names = {row["full_name"].casefold() for row in public}
    redirect_path = root / "data/public-repository-redirects.json"
    if redirect_path.is_file():
        ids = {row.get("github_id") for row in public}
        for redirect in json.loads(redirect_path.read_text())["redirects"]:
            if redirect["github_id"] not in ids:
                raise ValueError("Public repository redirect target is absent from the public inventory")
            names.add(redirect["alias"].casefold())
    return frozenset(names)


def project_public_links(value, allowed: frozenset[str], *, preserve_records: bool = False):
    """Return a public projection without mutating the raw observation."""
    def blocked(text):
        return any(owned_repository(m.group()) and owned_repository(m.group()) not in allowed for m in URL_RX.finditer(text))
    if isinstance(value, dict):
        return {key: project_public_links(item, allowed, preserve_records=preserve_records) for key, item in value.items()}
    if isinstance(value, list):
        return [project_public_links(item, allowed, preserve_records=preserve_records) for item in value if preserve_records or not (isinstance(item, dict) and any(isinstance(item.get(key), str) and blocked(item[key]) for key in ("identifier", "url")))]
    if isinstance(value, str):
        return URL_RX.sub(lambda m: "[non-public repository]" if owned_repository(m.group()) and owned_repository(m.group()) not in allowed else m.group(), value)
    return value


def project_pairing_report(payload: dict, allowed: frozenset[str], *, preserve_records: bool = False) -> dict:
    projected = project_public_links(payload, allowed, preserve_records=preserve_records)
    if projected != payload:
        original = json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()
        provenance = {"policy": POLICY, "original_observation_sha256": hashlib.sha256(original).hexdigest(), "scope": "Public projection only; does not refresh or approve upstream observations."}
        if "source_observations" in projected:
            provenance["upstream_source_observations"] = projected.pop("source_observations")
        projected["public_link_projection"] = provenance
    return projected


def source_link_outputs(root: Path = ROOT) -> dict[Path, str]:
    """Project new registry refresh sidecars and the latest pairing report."""
    allowed = public_repositories(root)
    outputs = {}
    reports = sorted((root / "reports").glob("paired_publications_*.json"))
    if reports:
        path = reports[-1]
        payload = json.loads(path.read_text())
        projected = project_pairing_report(payload, allowed)
        if projected != payload:
            outputs[path] = json.dumps(projected, indent=2, ensure_ascii=False) + "\n"
            original_digest = hashlib.sha256(path.read_bytes()).hexdigest()
            projected_digest = hashlib.sha256(outputs[path].encode()).hexdigest()
            for metadata_path in (root / "papers").glob("*/metadata.json"):
                metadata = json.loads(metadata_path.read_text())
                release = metadata.get("latest_software_release", {})
                if release.get("source_report") == path.relative_to(root).as_posix() and release.get("source_report_sha256") == original_digest:
                    release["source_report_sha256"] = projected_digest
                    release["source_report_projection"] = {"policy": POLICY, "original_report_sha256": original_digest}
                    outputs[metadata_path] = json.dumps(metadata, indent=2, ensure_ascii=False) + "\n"
    for path in (root / "papers").glob("*/source_evidence.json"):
        payload = json.loads(path.read_text())
        projected = {key: project_pairing_report(value, allowed) if key.startswith("registry_refresh") else value for key, value in payload.items()}
        if projected != payload:
            outputs[path] = json.dumps(projected, indent=2, ensure_ascii=False) + "\n"
    curated = [root / "data/publishing-status.json", root / "README.md"]
    curated.extend((root / "pages").glob("*.md"))
    for name in ("metadata.json", "README.md", "AGENTS.md", "SKILL.md"):
        curated.extend((root / "papers").glob("*/" + name))
    for path in curated:
        if not path.is_file():
            continue
        original = outputs.get(path, path.read_text())
        if path.suffix == ".json":
            payload = json.loads(original)
            projected = project_public_links(payload, allowed, preserve_records=True)
            if projected != payload:
                outputs[path] = json.dumps(projected, indent=2, ensure_ascii=False) + "\n"
        else:
            projected = project_public_links(original, allowed)
            if projected != original:
                outputs[path] = projected
    return outputs
