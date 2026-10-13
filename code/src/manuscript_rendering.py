"""Explicit, offline draft rendering into a new external review directory."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import quote, unquote, urlsplit
import zipfile

import yaml

from docxology_tools.generated_outputs import read_generated_output_text
from docxology_tools.manuscript_validation import MANUSCRIPT_PATH, UniqueKeyLoader, validate_manuscript

TOOLS = {"pandoc": "3.12.1", "pandoc-crossref": "0.3.25", "typst": "0.15.1"}
OUTPUTS = {"html": "docxology-methods.html", "pdf": "docxology-methods.pdf",
           "epub": "docxology-methods.epub", "slides": "docxology-methods.pptx"}
TIMEOUT = 90
MAX_OUTPUT_BYTES = 20 * 1024 * 1024


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run(arguments: list[str], *, root: Path, data: str | None = None) -> str:
    environment = dict(os.environ, SOURCE_DATE_EPOCH="0")
    result = subprocess.run(arguments, input=data, capture_output=True, text=True,
                            cwd=root, timeout=TIMEOUT, env=environment, check=False)
    if result.returncode:
        raise ValueError(f"{Path(arguments[0]).name} failed (exit {result.returncode}); previous review outputs were not changed")
    return result.stdout


def toolchain(root: Path) -> dict:
    result = {}
    for name, version in TOOLS.items():
        executable = shutil.which(name)
        if executable is None:
            raise ValueError(f"Required renderer is missing: {name} {version}")
        lines = run([executable, "--version"], root=root).splitlines()
        if not lines:
            raise ValueError(f"Renderer version banner is missing: {name}")
        banner = lines[0]
        if not re.search(r"\bv?" + re.escape(version) + r"(?:\s|$)", banner):
            raise ValueError(f"Renderer version mismatch: {name} requires {version}")
        if name == "pandoc-crossref" and f"Pandoc v{TOOLS['pandoc']}" not in banner:
            raise ValueError("pandoc-crossref must match the pinned Pandoc build")
        result[name] = {"version": version, "binary_sha256": digest(Path(executable).resolve())}
    return result


def new_review_directory(root: Path, output: Path) -> Path:
    """Require an absent external destination with real existing ancestors."""
    output = Path(os.path.abspath(output))
    if output.is_relative_to(root.resolve()):
        raise ValueError("Review outputs must be outside the repository")
    for parent in (output, *output.parents):
        if parent.is_symlink():
            raise ValueError("Review destination and ancestors must not be symlinks")
    if output.exists() or not output.parent.is_dir():
        raise ValueError("Use a new review directory under an existing real parent")
    return output


def rebase_links(node, root: Path, commit: str):
    """Bind source links to one public revision; keep figures local/offline."""
    if isinstance(node, list):
        return [rebase_links(value, root, commit) for value in node]
    if not isinstance(node, dict):
        return node
    node = {key: rebase_links(value, root, commit) for key, value in node.items()}
    if node.get("t") in {"RawBlock", "RawInline"}:
        raise ValueError("Raw renderer markup requires an explicit rendering integration")
    if node.get("t") == "CodeBlock" and "mermaid" in node["c"][0][1]:
        raise ValueError("Mermaid figures need an explicit renderer")
    if node.get("t") not in {"Link", "Image"}:
        return node
    target = node["c"][-1][0]
    parsed = urlsplit(target)
    if node["t"] == "Image":
        # Figure rendering needs a separate declared producer/inspection.
        # Current sources have no figures; never fetch remote images silently.
        raise ValueError("Manuscript figures require an explicit offline rendering integration")
    if parsed.scheme or parsed.netloc or not parsed.path:
        return node
    path = (root / MANUSCRIPT_PATH / unquote(parsed.path)).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Manuscript link escapes repository")
    relative = path.relative_to(root.resolve()).as_posix()
    kind = "tree" if path.is_dir() else "blob"
    node["c"][-1][0] = f"https://github.com/docxology/docxology/{kind}/{commit}/{quote(relative, safe='/')}"
    if parsed.fragment:
        node["c"][-1][0] += "#" + parsed.fragment
    return node


def validate_artifacts(directory: Path, formats: list[str]) -> dict:
    artifacts = {}
    for format_name in formats:
        path = directory / OUTPUTS[format_name]
        size = path.stat().st_size
        if not 0 < size <= MAX_OUTPUT_BYTES:
            raise ValueError(f"Invalid rendered artifact size: {path.name}")
        if format_name == "pdf":
            from pypdf import PdfReader
            reader = PdfReader(path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            if not reader.pages or "docxology" not in text or "References" not in text or "@sec:" in text:
                raise ValueError("PDF text or references did not render")
        elif format_name in {"epub", "slides"}:
            with zipfile.ZipFile(path) as package:
                if package.testzip() is not None:
                    raise ValueError("Corrupt rendered package")
                required = "META-INF/container.xml" if format_name == "epub" else "ppt/presentation.xml"
                if required not in package.namelist():
                    raise ValueError("Rendered package is missing its document")
        else:
            text = path.read_text(encoding="utf-8")
            if 'id="refs"' not in text or "@sec:" in text or "@docxologyIndex" in text:
                raise ValueError("HTML references did not render")
        artifacts[path.name] = {"format": format_name, "bytes": size, "sha256": digest(path)}
    return artifacts


def render_manuscript(root: Path, output: Path) -> dict:
    root = root.absolute()
    output = new_review_directory(root, output)
    validation = validate_manuscript(root)
    if not validation["source_valid"]:
        raise ValueError("Manuscript structural source checks failed")
    config_path = root / MANUSCRIPT_PATH / "config.yaml"
    inputs = [config_path, root / MANUSCRIPT_PATH / "references.bib"]
    inputs.extend(root / MANUSCRIPT_PATH / name for name in validation["sections"])
    inputs.extend([root / "code/src/manuscript_rendering.py", root / "code/orchestrators/render_manuscript.py"])
    frozen = {path: read_generated_output_text(root, path, newline="") for path in inputs}
    if any(text is None for text in frozen.values()):
        raise ValueError("Required rendering source is missing")
    source_hashes = {path.relative_to(root).as_posix(): hashlib.sha256(text.encode("utf-8")).hexdigest()
                     for path, text in frozen.items()}
    config = yaml.load(frozen[config_path], Loader=UniqueKeyLoader)
    if config["render"].get("toolchain") != TOOLS:
        raise ValueError("Manuscript configuration must declare the pinned toolchain")
    formats = validation["configured_render_formats"]
    if not formats or any(name not in OUTPUTS for name in formats):
        raise ValueError("Configured formats are not supported by the declared renderer")
    tools = toolchain(root)
    commit = run(["git", "rev-parse", "HEAD"], root=root).strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("Public source-link revision must be a full Git commit")
    sections = []
    for name in validation["sections"]:
        path = root / MANUSCRIPT_PATH / name
        text = frozen[path]
        if re.search(r"(?m)^\s*```\s*mermaid\b", text):
            raise ValueError("Mermaid figures need an explicit renderer")
        sections.append(text)
    with tempfile.TemporaryDirectory(prefix=".docxology-render-", dir=output.parent) as scratch_name:
        scratch = Path(scratch_name)
        data_dir = scratch / "pandoc-data"
        data_dir.mkdir()
        pandoc = ["pandoc", "--data-dir", str(data_dir)]
        references = scratch / "references.bib"
        references.write_text(frozen[inputs[1]], encoding="utf-8")
        bibliography = json.loads(run([*pandoc, "--from=biblatex", "--to=csljson", "--fail-if-warnings", str(references)], root=root))
        if len(bibliography) != validation["citation_count"]:
            raise ValueError("Parsed bibliography count differs from structural inventory")
        document = json.loads(run([*pandoc, "--from=markdown", "--to=json"], root=root, data="\n\n".join(sections)))
        document = rebase_links(document, root, commit)
        document["blocks"].insert(0, {"t": "Para", "c": [{"t": "Str", "c":
            f"Review draft {config['paper']['version']}. Manuscript text and original figures: {config['metadata']['license']}. Human and editorial reviews pending."}]})
        metadata = document["meta"]
        for name, value in {"title": config["paper"]["title"], "subtitle": config["paper"]["subtitle"],
                            "date": config["paper"]["date"], "lang": config["metadata"]["language"],
                            "rights": config["metadata"]["license"], "version": config["paper"]["version"]}.items():
            metadata[name] = {"t": "MetaString", "c": value}
        metadata["author"] = {"t": "MetaList", "c": [{"t": "MetaString", "c": author["name"]} for author in config["authors"]]}
        data = json.dumps(document, ensure_ascii=False)
        common = [*pandoc, "--from=json", "--standalone", "--number-sections", "--filter=pandoc-crossref",
                  "--citeproc", "--bibliography", str(references), "--fail-if-warnings"]
        for format_name in formats:
            arguments = [*common, "--output", str(scratch / OUTPUTS[format_name])]
            if format_name == "pdf":
                arguments += ["--to=typst", "--pdf-engine=typst", "--pdf-engine-opt=--ignore-system-fonts",
                              "--pdf-engine-opt=--creation-timestamp=0", "-V", "fontsize=10pt"]
            else:
                arguments += ["--to=" + {"html": "html5", "epub": "epub3", "slides": "pptx"}[format_name]]
                if format_name == "slides":
                    arguments += ["--slide-level=2"]
            run(arguments, root=root, data=data)
        artifacts = validate_artifacts(scratch, formats)
        if any(digest(path) != source_hashes[path.relative_to(root).as_posix()] for path in inputs):
            raise ValueError("Rendering sources changed; no review outputs were published")
        receipt = {"schema_version": "1.0", "evidence_kind": "offline manuscript draft render",
                   "source_sha256": source_hashes,
                   "source_link_commit": commit, "toolchain": tools, "artifacts": artifacts,
                   "bibliography_parser": "Pandoc biblatex reader", "bibliography_entries": len(bibliography),
                   "license": config["metadata"]["license"], "editorial_review": "pending",
                   "human_visual_review": "pending", "scientific_validity_assessed": False,
                   "publication_readiness_assessed": False, "network_fetches_requested": False}
        (scratch / "render-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
        new_review_directory(root, output)
        shutil.rmtree(data_dir)
        references.unlink()
        scratch.rename(output)
    return receipt
