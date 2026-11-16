"""Privacy projection for newly imported owned-repository links.

Only the observed public inventory authorizes new owned-repository links.
Literal historical documents and their extraction evidence remain unchanged.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
URL_RX = re.compile(r"https?://[^\s<>\"'()\[\]]+", re.I)
POLICY = "public-owned-repositories-v1"


def owned_repository(url: str) -> str:
    parsed = urlsplit(url.rstrip(".,;:!?"))
    parts = unquote(parsed.path).strip("/").split("/")
    if parsed.hostname and parsed.hostname.casefold() in {"github.com", "www.github.com"} and len(parts) >= 2 and parts[0].casefold() == "docxology":
        slug = re.match(r"[A-Za-z0-9_.-]+", parts[1])
        return (parts[0] + "/" + slug.group().casefold().rstrip(".").removesuffix(".git")).casefold() if slug else ""
    return ""


def public_repositories(root: Path = ROOT) -> frozenset[str]:
    payload = json.loads((root / "data/github-repositories.json").read_text())
    return frozenset(row["full_name"].casefold() for row in payload["repositories"] if row.get("private") is False)


def project_public_links(value, allowed: frozenset[str]):
    """Return a public projection without mutating the raw observation."""
    def blocked(text):
        return any(owned_repository(m.group()) and owned_repository(m.group()) not in allowed for m in URL_RX.finditer(text))
    if isinstance(value, dict):
        return {key: project_public_links(item, allowed) for key, item in value.items()}
    if isinstance(value, list):
        return [project_public_links(item, allowed) for item in value if not (isinstance(item, dict) and any(isinstance(item.get(key), str) and blocked(item[key]) for key in ("identifier", "url")))]
    if isinstance(value, str):
        return URL_RX.sub(lambda m: "[non-public repository]" if owned_repository(m.group()) and owned_repository(m.group()) not in allowed else m.group(), value)
    return value


def project_pairing_report(payload: dict, allowed: frozenset[str]) -> dict:
    projected = project_public_links(payload, allowed)
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
    return outputs
