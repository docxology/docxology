"""Pure helpers for conservative private-versus-public release reconciliation.

The public ``origin/main`` history is the release baseline.  A private branch
can be useful evidence, but it is not an authority to merge wholesale: binary
intake, generated artifacts, and unrelated source changes must stay out of a
public release until they have their own verification path.
"""

from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
import re
from typing import Any, Iterable, Mapping


DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)
FOLDER_RE = re.compile(r"\.\./papers/([^/]+)/")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")

SOURCE_METADATA_PATHS = frozenset(
    {
        "pages/BIBLIOGRAPHY.md",
        "pages/SOFTWARE.md",
        "resume/source.json",
        "data/scholar-snapshot.json",
        "data/repository-exclusions.json",
        "data/paired-publication-decisions.json",
        "papers/paper_metadata.json",
    }
)
PAPER_GENERATED_NAMES = frozenset({"README.md", "AGENTS.md", "SKILL.md", "CITATION.cff", "index.html", "full_text.md"})
PAPER_BINARY_SUFFIXES = frozenset({".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".tif", ".tiff", ".svg"})
GENERIC_BINARY_SUFFIXES = PAPER_BINARY_SUFFIXES | frozenset({".zip", ".gz", ".tar", ".mp4", ".mov", ".mp3", ".wav"})
DERIVED_EXACT_PATHS = frozenset(
    {
        "GENERATED.md",
        "bibliography.bib",
        "bibliography.csl.json",
        "bibliography.ris",
        "feed.xml",
        "search-index.json",
        "sitemap.xml",
        "sitemap-images.xml",
        "uv.lock",
    }
)


@dataclass(frozen=True)
class ChangedPath:
    """A single path-level change from ``git diff --name-status -z``."""

    status: str
    path: str
    previous_path: str | None = None


def parse_name_status_z(raw: bytes) -> list[ChangedPath]:
    """Parse Git's NUL-delimited name-status format, including renames."""
    fields = raw.split(b"\0")
    changes: list[ChangedPath] = []
    index = 0
    while index < len(fields):
        if not fields[index]:
            break
        status = fields[index].decode("utf-8", "surrogateescape")
        index += 1
        if status[0] in {"R", "C"}:
            if index + 1 >= len(fields):
                raise ValueError(f"incomplete {status!r} name-status record")
            previous = fields[index].decode("utf-8", "surrogateescape")
            path = fields[index + 1].decode("utf-8", "surrogateescape")
            index += 2
            changes.append(ChangedPath(status=status, path=path, previous_path=previous))
            continue
        if index >= len(fields):
            raise ValueError(f"incomplete {status!r} name-status record")
        path = fields[index].decode("utf-8", "surrogateescape")
        index += 1
        changes.append(ChangedPath(status=status, path=path))
    return changes


def manifest_output_patterns(manifest: Mapping[str, Any]) -> tuple[str, ...]:
    """Return real output path/glob patterns from a generated-manifest payload."""
    patterns: set[str] = set()
    artifacts = manifest.get("artifacts", [])
    if not isinstance(artifacts, list):
        return ()
    for artifact in artifacts:
        if not isinstance(artifact, Mapping):
            continue
        outputs = artifact.get("outputs", [])
        if not isinstance(outputs, list):
            continue
        for output in outputs:
            if not isinstance(output, str):
                continue
            # A few manifest entries annotate a path in parentheses; others
            # are prose descriptions and must not become a false path match.
            candidate = output.split(" (", 1)[0].strip()
            if "/" not in candidate and not candidate.startswith("*") and "." not in candidate:
                continue
            patterns.add(candidate)
    return tuple(sorted(patterns))


def _matches_manifest(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatchcase(path, pattern) for pattern in patterns)


def classify_path(path: str, manifest_patterns: Iterable[str] = ()) -> str:
    """Classify a changed path for a conservative release reconciliation."""
    normalized = path.removeprefix("./")
    filename = normalized.rsplit("/", 1)[-1]
    suffix = "." + filename.rsplit(".", 1)[1].lower() if "." in filename else ""

    # Metadata sources have precedence over the older manifest's broad
    # enrichment entries. They require corroboration, not a blind regeneration.
    if normalized in SOURCE_METADATA_PATHS or (
        normalized.startswith("papers/") and normalized.endswith("/metadata.json")
    ):
        return "source_metadata"

    # Paper PDFs and extracted images are intake material.  The release plan
    # explicitly defers them rather than treating a private binary refresh as
    # an automatically reproducible generated output.
    if normalized.startswith("papers/") and (
        "/images/" in normalized or suffix in PAPER_BINARY_SUFFIXES
    ):
        return "binary_intake"

    if normalized in DERIVED_EXACT_PATHS or _matches_manifest(normalized, manifest_patterns):
        return "derived_output"
    if normalized.startswith("reports/") or normalized.startswith("works/") or normalized.startswith("videos/"):
        return "derived_output"
    if normalized.startswith("data/"):
        return "derived_output"
    if normalized.startswith("papers/") and filename in PAPER_GENERATED_NAMES:
        return "derived_output"
    if suffix in GENERIC_BINARY_SUFFIXES:
        return "binary_intake"
    return "other_source"


def default_decision(classification: str) -> tuple[str, str]:
    """Return the release disposition for a path without specific evidence."""
    decisions = {
        "source_metadata": (
            "defer",
            "Source metadata needs canonical-source corroboration before it can be ported.",
        ),
        "derived_output": (
            "regenerate",
            "Do not port a private derived artifact; rebuild it from reconciled public sources.",
        ),
        "binary_intake": (
            "defer",
            "Unverified PDF, extracted image, or other binary intake is out of scope for this release.",
        ),
        "other_source": (
            "defer",
            "Unrelated private source change is not part of the public-main release reconciliation.",
        ),
    }
    try:
        return decisions[classification]
    except KeyError as exc:  # pragma: no cover - defensive API boundary
        raise ValueError(f"unknown reconciliation classification: {classification}") from exc


def extract_doi(value: object) -> str:
    """Extract a normalized DOI from a markdown or metadata value."""
    match = DOI_RE.search(str(value or ""))
    return match.group(0).rstrip(".,;:)]}") if match else ""


def clean_markdown(value: str) -> str:
    """Make a bibliography title suitable for exact, conservative matching."""
    value = MARKDOWN_LINK_RE.sub(r"\1", value)
    return re.sub(r"[*_`]", "", value).strip()


def bibliography_rows(markdown: str) -> dict[str, dict[str, str]]:
    """Map bibliography paper folders to their title and canonical DOI."""
    rows: dict[str, dict[str, str]] = {}
    for line in markdown.splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 8 or cells[0].lower() in {"#", "---"}:
            continue
        folder_match = FOLDER_RE.search(cells[7])
        if not folder_match:
            continue
        rows[folder_match.group(1)] = {
            "title": clean_markdown(cells[4]),
            "doi": extract_doi(cells[6]),
        }
    return rows


def changed_top_level_fields(public: Mapping[str, Any], private: Mapping[str, Any]) -> list[str]:
    """Return sorted JSON fields that differ without serializing their values."""
    return sorted(key for key in set(public) | set(private) if public.get(key) != private.get(key))


def source_backed_metadata_fields(
    folder: str,
    public_metadata: Mapping[str, Any],
    private_metadata: Mapping[str, Any],
    private_bibliography: Mapping[str, Mapping[str, str]],
) -> list[dict[str, str]]:
    """Return private identity candidates, never independently verified ports.

    An exact match between a private metadata field and a private bibliography
    row proves only internal private consistency.  It is useful for a review
    queue, but the public bibliography or an external primary authority must
    independently support any source edit.  Every result is therefore
    deferred rather than automatically portable.
    """
    canonical = private_bibliography.get(folder)
    if not canonical:
        return []
    findings: list[dict[str, str]] = []
    public_doi = extract_doi(public_metadata.get("doi"))
    private_doi = extract_doi(private_metadata.get("doi"))
    canonical_doi = extract_doi(canonical.get("doi"))
    if public_doi.casefold() != private_doi.casefold() and private_doi and private_doi.casefold() == canonical_doi.casefold():
        findings.append(
            {
                "folder": folder,
                "field": "doi",
                "baseline_value": public_doi,
                "private_value": private_doi,
                "canonical_value": canonical_doi,
                "decision": "defer",
                "implementation": "Private metadata and private bibliography agree, but this is candidate-only until the public canonical source or an external DOI authority is reviewed.",
            }
        )

    public_title = clean_markdown(str(public_metadata.get("title", "")))
    private_title = clean_markdown(str(private_metadata.get("title", "")))
    canonical_title = clean_markdown(canonical.get("title", ""))
    if public_title != private_title and private_title and private_title == canonical_title:
        findings.append(
            {
                "folder": folder,
                "field": "title",
                "baseline_value": public_title,
                "private_value": private_title,
                "canonical_value": canonical_title,
                "decision": "defer",
                "implementation": "Private metadata and private bibliography agree, but this title remains candidate-only pending an independent public authority.",
            }
        )
    return findings


def render_markdown(payload: Mapping[str, Any]) -> str:
    """Render a deterministic, review-friendly reconciliation report."""
    summary = payload["summary"]
    lines = [
        "# Private-versus-Public Release Reconciliation",
        "",
        f"Report date: {payload['report_date']}",
        "",
        f"Public baseline: `{payload['baseline']['requested']}` → `{payload['baseline']['resolved']}`",
        f"Private reference: `{payload['private_ref']['requested']}` → `{payload['private_ref']['resolved']}`",
        "",
        "This is a read-only comparison. It neither merges nor cherry-picks private history.",
        "",
        "## Disposition Summary",
        "",
        "| Classification | Changed paths | Release disposition |",
        "| --- | ---: | --- |",
    ]
    for classification in ("source_metadata", "derived_output", "binary_intake", "other_source"):
        item = summary["classifications"].get(classification, {"count": 0, "decision": "defer"})
        lines.append(f"| {classification.replace('_', ' ')} | {item['count']} | {item['decision']} |")
    lines.extend(
        [
            "",
            "## Required Release Treatment",
            "",
            "- Treat private metadata/bibliography agreement as a review candidate, not independent corroboration or an automatic source port.",
            "- Regenerate every derived output from reconciled public sources; do not copy private rendered files or reports.",
            "- Defer all PDFs, extracted text, and paper-image binaries pending separately verified intake provenance.",
            "- Defer all private-only source changes until a public canonical source or external primary authority is recorded.",
            "",
            "## Private Identity Candidates (Deferred)",
            "",
        ]
    )
    findings = payload["private_identity_candidates"]
    if not findings:
        lines.append("No private metadata/bibliography identity candidate was found.")
    else:
        lines.extend(
            [
                "| Folder | Field | Baseline | Canonical/private | Decision | Local release status |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for finding in findings:
            lines.append(
                "| {folder} | {field} | {baseline_value} | {private_value} | {decision} | {release_status} |".format(
                    **finding
                )
            )
    lines.extend(
        [
            "",
            "## Deferred Source Metadata",
            "",
            f"{summary['deferred_metadata_fields']} metadata fields across {summary['metadata_files_reviewed']} paper metadata files remain deferred pending independent public-source verification.",
            "",
            "## Evidence Boundary",
            "",
            "The report records an internal source comparison only. It does not verify private Zenodo, PDF, image, Scholar, biographical, repository-classification, or generated-claim changes against their external authorities.",
            "",
        ]
    )
    return "\n".join(lines)
