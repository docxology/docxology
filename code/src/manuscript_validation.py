"""Read-only structural checks for the repository-system manuscript.

Validation establishes source/configuration consistency, not publication
readiness, claim truth, renderer availability, or successful figure rendering.
Archived publications under papers/ are outside this module's scope.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

from docxology_tools.generated_outputs import read_generated_output_text

MANUSCRIPT_PATH = Path("docs/manuscript")
SECTION_PATTERN = re.compile(r"^(?:[0-9]{2}|S[0-9]{2})_[a-z0-9_]+\.md$")
LABEL_PATTERN = re.compile(r"\{#((?:sec|fig|tbl):[A-Za-z0-9_-]+)\}")
LINK_PATTERN = re.compile(r"(!?)\[[^\]\n]*\]\((<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)")
CITATION_PATTERN = re.compile(r"(?<![\w/])@([A-Za-z0-9_:.+-]+)")
TOKEN_PATTERN = re.compile(r"\{\{\s*[A-Z][A-Z0-9_]*\s*\}\}")


class UniqueKeyLoader(yaml.SafeLoader):
    """Reject duplicate configuration keys instead of silently overriding them."""

    def construct_mapping(self, node, deep=False):
        self.flatten_mapping(node)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if not isinstance(key, str):
                raise yaml.constructor.ConstructorError(None, None, "configuration keys must be strings", key_node.start_mark)
            if key in mapping:
                raise yaml.constructor.ConstructorError(None, None, f"duplicate configuration key: {key}", key_node.start_mark)
            mapping[key] = self.construct_object(value_node, deep=deep)
        return mapping


def prose_without_fences(text: str) -> str:
    """Ignore code examples and diagrams when checking prose conventions."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence is None and marker:
            fence = marker.group(1)
        elif fence is not None:
            if re.fullmatch(r"\s{0,3}" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
                fence = None
        else:
            lines.append(line)
    if fence is not None:
        raise ValueError("unterminated fenced code block")
    return "\n".join(lines)


def _source_text(root: Path, relative: Path, errors: list[str]) -> str | None:
    try:
        text = read_generated_output_text(root, root / relative)
    except (OSError, ValueError, UnicodeError) as exc:
        errors.append(f"{relative.as_posix()}: cannot read a regular repository source ({type(exc).__name__})")
        return None
    if text is None:
        errors.append(f"{relative.as_posix()}: missing source")
    return text


def _local_path(value: object, root: Path) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        return None
    path = Path(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    try:
        if (root / path).resolve().is_relative_to(root.resolve()):
            return path
    except (OSError, ValueError):
        return None
    return None


def _configuration(text: str, root: Path, errors: list[str]) -> tuple[dict, list[str]]:
    label = "docs/manuscript/config.yaml"
    try:
        config = yaml.load(text, Loader=UniqueKeyLoader)
    except yaml.YAMLError:
        errors.append(f"{label}: invalid safe YAML or duplicate keys")
        return {}, []
    if not isinstance(config, dict):
        errors.append(f"{label}: expected a configuration mapping")
        return {}, []
    for field in ("paper", "publication", "metadata", "render", "bibliography"):
        if not isinstance(config.get(field), dict):
            errors.append(f"{label}: {field} must be a mapping")
    paper = config.get("paper")
    if isinstance(paper, dict) and not isinstance(paper.get("title"), str):
        errors.append(f"{label}: paper.title must be a non-empty string")
    elif isinstance(paper, dict) and not paper["title"].strip():
        errors.append(f"{label}: paper.title must be a non-empty string")
    publication = config.get("publication")
    if isinstance(publication, dict) and publication.get("github_repository") != "docxology/docxology":
        errors.append(f"{label}: publication.github_repository must identify docxology/docxology")
    authors = config.get("authors")
    if not isinstance(authors, list) or not authors or any(
        not isinstance(author, dict) or not isinstance(author.get("name"), str) or not author["name"].strip()
        for author in authors
    ):
        errors.append(f"{label}: authors must contain named author mappings")
    if _local_path(config.get("manuscript_dir"), root) != MANUSCRIPT_PATH:
        errors.append(f"{label}: manuscript_dir must be docs/manuscript, relative to the repository root")
    bibliography = config.get("bibliography")
    if isinstance(bibliography, dict):
        if _local_path(bibliography.get("references_path"), root) != MANUSCRIPT_PATH / "references.bib":
            errors.append(f"{label}: bibliography.references_path must name docs/manuscript/references.bib")
        for key in ("fail_on_missing", "fail_on_unused"):
            if type(bibliography.get(key)) is not bool:
                errors.append(f"{label}: bibliography.{key} must be a YAML boolean")
        if bibliography.get("fail_on_missing") is not True:
            errors.append(f"{label}: unresolved manuscript citations must fail validation")
    render = config.get("render")
    formats = render.get("formats") if isinstance(render, dict) else None
    if not isinstance(formats, dict) or not formats or any(type(enabled) is not bool for enabled in formats.values()):
        errors.append(f"{label}: render.formats must contain YAML boolean values")
        return config, []
    unsupported = sorted(set(formats) - {"pdf", "html", "slides", "docx", "epub"})
    if unsupported:
        errors.append(f"{label}: unsupported render formats: {', '.join(unsupported)}")
    return config, sorted(name for name, enabled in formats.items() if enabled is True)


def bibliography_keys(text: str, errors: list[str]) -> list[str]:
    """Inventory keys while rejecting unclosed entries and stray outer text.

    This is a bounded entry/delimiter check, not evaluation of BibTeX fields,
    string expansion, TeX content, citation styling, or renderer compatibility.
    """
    keys: list[str] = []
    cursor = 0
    label = "docs/manuscript/references.bib"
    while cursor < len(text):
        if text[cursor].isspace():
            cursor += 1
            continue
        if text[cursor] == "%":
            newline = text.find("\n", cursor)
            cursor = len(text) if newline < 0 else newline + 1
            continue
        entry = re.match(r"@([A-Za-z]+)\s*([({])", text[cursor:])
        if entry is None:
            errors.append(f"{label}: unexpected text outside a bibliography entry")
            break
        kind, opening = entry.groups()
        start = cursor + entry.end() - 1
        braces = 1 if opening == "{" else 0
        quoted = False
        escaped = False
        end = None
        for index in range(start + 1, len(text)):
            char = text[index]
            if escaped:
                escaped = False
                continue
            if char == "\\":
                escaped = True
                continue
            if char == '"':
                quoted = not quoted
                continue
            if quoted:
                continue
            if char == "{":
                braces += 1
            elif char == "}":
                braces -= 1
                if braces < 0:
                    break
                if opening == "{" and braces == 0:
                    end = index
                    break
            elif char == ")" and opening == "(" and braces == 0:
                end = index
                break
        if end is None:
            errors.append(f"{label}: unclosed or unbalanced bibliography entry")
            break
        body = text[start + 1:end]
        if kind.lower() not in {"comment", "preamble", "string"}:
            key = re.match(r"\s*([^,\s{}()]+)\s*,", body)
            if key is None:
                errors.append(f"{label}: citation entry must start with a key and comma")
            else:
                keys.append(key.group(1))
        cursor = end + 1
    return keys


def prose_links(prose: str, relative: Path, errors: list[str]) -> list[tuple[str, str]]:
    """Resolve inline, explicit reference, and shortcut image destinations."""
    links = LINK_PATTERN.findall(prose)
    def normalize(value: str) -> str:
        return " ".join(value.split()).casefold()
    definitions = {
        normalize(label): target
        for label, target in re.findall(r"(?m)^\s{0,3}\[([^\]\n]+)\]:\s*(<[^>]+>|[^\s]+)(?:\s+.*)?$", prose)
    }
    for image, text, reference in re.findall(r"(!?)\[([^\]\n]*)\]\[([^\]\n]*)\]", prose):
        key = normalize(reference or text)
        if key not in definitions:
            errors.append(f"{relative}: unresolved reference-style {'figure' if image else 'link'}")
        else:
            links.append((image, definitions[key]))
    for reference in re.findall(r"!\[([^\]\n]*)\](?![\[(])", prose):
        key = normalize(reference)
        if key not in definitions:
            errors.append(f"{relative}: unresolved shortcut figure reference")
        else:
            links.append(("!", definitions[key]))
    return links


def validate_manuscript(root: Path) -> dict:
    """Return deterministic repository-relative diagnostics without writing files."""
    errors: list[str] = []
    config_text = _source_text(root, MANUSCRIPT_PATH / "config.yaml", errors)
    config, formats = _configuration(config_text, root, errors) if config_text is not None else ({}, [])
    references = _source_text(root, MANUSCRIPT_PATH / "references.bib", errors)
    citation_keys = []
    if references is not None:
        citation_keys = bibliography_keys(references, errors)
        if len(citation_keys) != len(set(citation_keys)):
            errors.append("docs/manuscript/references.bib: duplicate citation keys")
    def section_order(path: Path) -> tuple[int, str]:
        group = 1 if path.name.startswith("S") else 2 if path.name[:2] in {"98", "99"} else 0
        return group, path.name

    sections = sorted(
        (path for path in (root / MANUSCRIPT_PATH).glob("*.md") if SECTION_PATTERN.fullmatch(path.name)),
        key=section_order,
    )
    prefixes = [path.name.split("_", 1)[0] for path in sections]
    if len(prefixes) != len(set(prefixes)):
        errors.append("docs/manuscript: duplicate section-number prefixes")
    for required in ("00_abstract.md", "99_references.md"):
        if required not in {path.name for path in sections}:
            errors.append(f"docs/manuscript/{required}: required section is missing")
    labels: set[str] = set()
    cross_references: list[tuple[str, str]] = []
    used_keys: set[str] = set()
    for section in sections:
        relative = section.relative_to(root)
        text = _source_text(root, relative, errors)
        if text is None:
            continue
        try:
            prose = prose_without_fences(text)
        except ValueError as exc:
            errors.append(f"{relative}: {exc}")
            continue
        headings = re.findall(r"(?m)^# (.+)$", prose)
        first_line = next((line for line in prose.splitlines() if line.strip()), "")
        if len(headings) != 1 or not first_line.startswith("# ") or not re.search(r"\{#sec:[A-Za-z0-9_-]+\}$", first_line):
            errors.append(f"{relative}: section must start with exactly one H1 carrying a sec label")
        for label in LABEL_PATTERN.findall(prose):
            if label in labels:
                errors.append(f"{relative}: duplicate label {label}")
            labels.add(label)
        if TOKEN_PATTERN.search(prose):
            errors.append(f"{relative}: unresolved generated-value token")
        for raw_key in CITATION_PATTERN.findall(prose):
            # Sentence punctuation may follow a narrative citation/reference.
            # Preserve an exact bibliography key before trimming punctuation.
            key = raw_key if raw_key in citation_keys else raw_key.rstrip(".:")
            if key.startswith(("sec:", "fig:", "tbl:")):
                cross_references.append((relative.as_posix(), key))
            else:
                used_keys.add(key)
                if key not in citation_keys:
                    errors.append(f"{relative}: unresolved citation {key}")
        for image, raw_target in prose_links(prose, relative, errors):
            target = raw_target.strip("<>")
            if "\0" in target:
                errors.append(f"{relative}: invalid local reference")
                continue
            try:
                parsed = urlsplit(target)
            except ValueError:
                errors.append(f"{relative}: malformed link URL")
                continue
            if parsed.scheme:
                if parsed.scheme not in {"https", "http", "mailto"}:
                    errors.append(f"{relative}: unsupported link scheme")
                elif parsed.scheme in {"https", "http"}:
                    try:
                        valid = bool(parsed.hostname) and parsed.username is None and parsed.password is None
                        parsed.port  # Validate the optional numeric port/range.
                    except ValueError:
                        valid = False
                    if not valid:
                        errors.append(f"{relative}: malformed or credential-bearing external URL")
                continue
            if parsed.netloc:
                errors.append(f"{relative}: protocol-relative links are unsupported")
                continue
            if not parsed.path:
                continue
            decoded = unquote(parsed.path)
            if "\0" in decoded:
                errors.append(f"{relative}: invalid local reference")
                continue
            destination = section.parent / decoded
            try:
                if not destination.resolve().is_relative_to(root.resolve()):
                    errors.append(f"{relative}: local link escapes repository")
                elif not destination.exists():
                    errors.append(f"{relative}: missing local {'figure' if image else 'link'} {parsed.path}")
                elif image and (not destination.is_file() or destination.is_symlink()):
                    errors.append(f"{relative}: figure target must be a regular file")
            except (OSError, ValueError):
                errors.append(f"{relative}: invalid local reference")
    for path, label in cross_references:
        if label not in labels:
            errors.append(f"{path}: unresolved cross-reference {label}")
    if isinstance(config.get("bibliography"), dict) and config["bibliography"].get("fail_on_unused") is True:
        for key in sorted(set(citation_keys) - used_keys):
            errors.append(f"docs/manuscript/references.bib: unused citation {key}")
    return {
        "schema_version": 1,
        "scope": "repository manuscript source structure and local configuration",
        "manuscript_dir": MANUSCRIPT_PATH.as_posix(),
        "sections": [path.name for path in sections],
        "citation_count": len(citation_keys),
        "configured_render_formats": formats,
        "source_valid": not errors,
        "render_performed": False,
        "bibliography_syntax_validated": False,
        "publication_readiness_assessed": False,
        "errors": errors,
    }
