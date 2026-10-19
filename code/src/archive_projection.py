"""Explicit, byte-verified archive routing for supporting Office documents.

PDFs, work URLs and source files are preserved. No deletion is performed.
"""

from __future__ import annotations

import hashlib
from html import unescape
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote, unquote

REGISTRY = "data/pages-archive-documents.json"
SKIP = {
    REGISTRY,
    "data/pages-artifact-manifest.json",
    "data/generated-manifest.json",
    "data/report-retention.json",
}
URL = re.compile(r"(?<![A-Za-z0-9_=:/?&%.-])https://[^\s\"'<>()[\]]+")


def declared_archives(root: Path) -> dict[str, dict]:
    path = root / REGISTRY
    if not path.exists():
        return {}
    from docxology_tools.generated_outputs import read_generated_output_text

    payload = json.loads(read_generated_output_text(root, path))
    if payload.get("schema_version") != "1.0" or not isinstance(
        payload.get("entries"), list
    ):
        raise ValueError("Invalid Office archive projection registry")
    result = {}
    for item in payload["entries"]:
        name = item.get("path", "")
        if (
            not re.fullmatch(
                r"papers/[0-9]{4}_[A-Za-z0-9_-]+/[A-Za-z0-9_.-]+\.(?:docx|odt)", name
            )
            or name in result
            or not re.fullmatch(r"[0-9a-f]{40}", item.get("commit", ""))
            or not re.fullmatch(r"[0-9a-f]{64}", item.get("sha256", ""))
            or type(item.get("bytes")) is not int
            or not 0 < item["bytes"] <= 64 * 1024 * 1024
            or not item.get("reason")
            or not item.get("reviewed_by")
        ):
            raise ValueError("Unreviewed or invalid Office archive projection entry")
        result[name] = {
            **item,
            "url": f"https://github.com/docxology/docxology/blob/{item['commit']}/{quote(name, safe='/')}",
        }
    return result


def verified_archives(root: Path) -> dict[str, dict]:
    entries = declared_archives(root)
    if not entries:
        return entries
    from docxology_tools.paper_artifacts import source_file, source_paths

    visible = source_paths(root)
    for name, item in entries.items():
        path = source_file(root, name, visible)
        if (
            path is None
            or path.stat().st_size != item["bytes"]
            or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]
        ):
            raise ValueError(f"Office archive source bytes changed: {name}")
        subprocess.run(
            ["git", "merge-base", "--is-ancestor", item["commit"], "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            timeout=30,
        )
        spec = f"{item['commit']}:{name}"
        size = subprocess.check_output(
            ["git", "cat-file", "-s", spec], cwd=root, timeout=30, text=True
        )
        if int(size) != item["bytes"]:
            raise ValueError("Office archive object size differs")
        original = subprocess.check_output(
            ["git", "cat-file", "blob", spec], cwd=root, timeout=30
        )
        if hashlib.sha256(original).hexdigest() != item["sha256"]:
            raise ValueError("Office archive object bytes differ")
    inventory = (
        subprocess.check_output(
            ["git", "ls-files", "-co", "--exclude-standard", "-z"], cwd=root, timeout=30
        )
        .decode()
        .split("\0")
    )
    allowed_urls = {item["url"] for item in entries.values()}
    for name in inventory:
        if not name or name in SKIP or name.split("/")[0] in {".github", "_site"}:
            continue
        path = root / name
        if path.suffix.lower() not in {
            ".html",
            ".json",
            ".md",
            ".txt",
            ".xml",
            ".css",
            ".js",
            ".svg",
            ".csv",
            ".yaml",
            ".yml",
            ".cff",
            ".py",
        }:
            continue
        from docxology_tools.generated_outputs import read_generated_output_text

        text = read_generated_output_text(root, path)
        if text is None:
            raise ValueError("Office archive reference inventory is incomplete")
        text = URL.sub(
            lambda match: " " if match[0] in allowed_urls else match[0], text
        )
        # Remove only exact approved URL spans before conservatively decoding
        # local references. Encoded/nested archive URLs stay protective.
        for _ in range(16):
            decoded = unquote(unescape(text))
            decoded = re.sub(
                r"\\u([0-9a-fA-F]{4})", lambda m: chr(int(m[1], 16)), decoded
            )
            if decoded == text:
                break
            text = decoded
        else:
            raise ValueError("Office archive reference encoding is too deeply nested")
        for target in entries:
            if Path(target).name in text:
                raise ValueError(
                    f"Office archive still has a local or unreviewed reference: {name}"
                )
    return entries
