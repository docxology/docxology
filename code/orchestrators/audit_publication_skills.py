#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
LEGACY_HOST = "docxology.github.io/docxology"
MAX_DESCRIPTION_CHARS = 1024


def _load_works(repo_root: Path) -> list[dict[str, Any]]:
    path = repo_root / "data" / "works.json"
    return json.loads(path.read_text(encoding="utf-8"))["works"]


def _doc_paths(repo_root: Path) -> set[str]:
    return {
        str(work.get("docs_path") or "").rstrip("/")
        for work in _load_works(repo_root)
        if str(work.get("docs_path") or "").strip()
    }


def _skill_dirs(repo_root: Path) -> set[str]:
    return {
        str(path.parent.relative_to(repo_root))
        for path in sorted((repo_root / "papers").glob("*/SKILL.md"))
        if re.match(r"\d{4}_", path.parent.name)
    }


def _frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    if not text.startswith("---\n"):
        return {}, "missing opening frontmatter delimiter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, "missing closing frontmatter delimiter"
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields, None


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _validate_tags(raw: str) -> str | None:
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        return f"tags must be a JSON list: {exc.msg}"
    if not isinstance(parsed, list) or not parsed:
        return "tags must be a non-empty JSON list"
    bad = [tag for tag in parsed if not isinstance(tag, str) or not tag.strip()]
    if bad:
        return "tags must contain only non-empty strings"
    return None


def collect_skill_errors(repo_root: Path = REPO_ROOT) -> list[str]:
    errors: list[str] = []
    docs = _doc_paths(repo_root)
    skills = _skill_dirs(repo_root)

    for missing in sorted(docs - skills):
        errors.append(f"{missing}/SKILL.md missing for data/works.json docs_path")
    for extra in sorted(skills - docs):
        errors.append(f"{extra}/SKILL.md is not referenced by data/works.json docs_path")

    for folder in sorted(docs & skills):
        path = repo_root / folder / "SKILL.md"
        text = path.read_text(encoding="utf-8", errors="ignore")
        rel = str(path.relative_to(repo_root))
        if LEGACY_HOST in text:
            errors.append(f"{rel}: legacy GitHub Pages host found; use https://danielarifriedman.com/")
        fields, frontmatter_error = _frontmatter(text)
        if frontmatter_error:
            errors.append(f"{rel}: {frontmatter_error}")
            continue
        for key in ("name", "description", "tags"):
            if not fields.get(key):
                errors.append(f"{rel}: frontmatter missing {key}")
        description = _unquote(fields.get("description", ""))
        if len(description) > MAX_DESCRIPTION_CHARS:
            errors.append(f"{rel}: description exceeds {MAX_DESCRIPTION_CHARS} characters")
        if fields.get("tags"):
            tag_error = _validate_tags(fields["tags"])
            if tag_error:
                errors.append(f"{rel}: {tag_error}")
        if not re.search(r"^##\s+Instructions\s*$", text, re.MULTILINE):
            errors.append(f"{rel}: missing ## Instructions section")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate publication SKILL.md files for agent-facing operability.")
    parser.add_argument("--check", action="store_true", help="Validate publication skills and exit")
    args = parser.parse_args()
    errors = collect_skill_errors()
    if errors:
        raise SystemExit("Publication skill audit failed:\n" + "\n".join(errors[:120]))
    print(f"checked {len(_skill_dirs(REPO_ROOT))} publication skills")


if __name__ == "__main__":
    main()
