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

from docxology_tools.manuscript_figures import (
    FIGURES,
    PRODUCER,
    SOURCE_TARGETS,
    render_figures,
)
from docxology_tools.manuscript_template import COVER, TEMPLATE, cover_pdf, native_pdf
from docxology_tools.generated_outputs import read_generated_output_text
from docxology_tools.manuscript_validation import (
    MANUSCRIPT_PATH,
    UniqueKeyLoader,
    validate_manuscript,
)

TOOLS = {
    "pandoc": "3.12.1",
    "pandoc-crossref": "0.3.26",
    "xelatex": "3.141592653-2.6-0.999998",
    "bibtex": "0.99e",
}
OUTPUTS = {
    "html": "docxology-methods.html",
    "pdf": "docxology-methods.pdf",
    "epub": "docxology-methods.epub",
    "slides": "docxology-methods.pptx",
}
TIMEOUT = 90
MAX_OUTPUT_BYTES = 20 * 1024 * 1024

SLIDE_TEXT_LIMIT = 450
# The pinned 16:9 PPTX body is 9in x 3.71in at 24pt. The frozen viewer showed
# eight-line paragraphs split solely at 450 characters. Prose may use the
# remaining area, bounded independently by conservative wrapping and line count.
# Indivisible inlines, code, tables and figures retain their separate limits.
SLIDE_PROSE_LIMIT = 600
SLIDE_LINE_WIDTH = 60
SLIDE_LINE_LIMIT = 9
SLIDE_MIN_CONTINUATION = 120
SLIDE_LAYOUT = "coherent-bounded-pagination-v3"


def _slide_text_size(node) -> int:
    """Conservative visible-text budget; link targets and attributes are not text."""
    if isinstance(node, list):
        return sum(_slide_text_size(value) for value in node)
    if not isinstance(node, dict):
        return 0
    kind, content = node.get("t"), node.get("c")
    if kind == "Str":
        return len(content)
    if kind in {"Space", "SoftBreak"}:
        return 1
    if kind == "LineBreak":
        return 70
    if kind in {"Code", "Math"}:
        return len(content[-1])
    if kind in {"Link", "Image"}:
        return _slide_text_size(content[1])
    return _slide_text_size(content)


def _slide_visible_text(node) -> str:
    if isinstance(node, list):
        return "".join(_slide_visible_text(value) for value in node)
    if not isinstance(node, dict):
        return ""
    kind, content = node.get("t"), node.get("c")
    if kind == "Str":
        return content
    if kind in {"Space", "SoftBreak"}:
        return " "
    if kind == "LineBreak":
        return "\n"
    if kind in {"Code", "Math"}:
        return content[-1]
    if kind in {"Link", "Image"}:
        return _slide_visible_text(content[1])
    return _slide_visible_text(content)


def _slide_text_unit(block) -> bool:
    if isinstance(block, list):
        return all(_slide_text_unit(value) for value in block)
    if not isinstance(block, dict):
        return True
    if block.get("t") in {"Image", "Table", "CodeBlock", "Figure"}:
        return False
    return _slide_text_unit(block.get("c"))


def _slide_text_lines(block, width):
    import textwrap

    if width < 12:
        raise ValueError("Slide list nesting exceeds its line budget")
    if block["t"] in {"BulletList", "OrderedList"}:
        items = block["c"] if block["t"] == "BulletList" else block["c"][1]
        return max(0, len(items) - 1) + sum(
            max(0, len(item) - 1) + sum(_slide_text_lines(child, width - 6) for child in item)
            for item in items
        )
    return sum(
        max(1, len(textwrap.wrap(line, width=width, break_on_hyphens=False)))
        for line in _slide_visible_text(block).split("\n")
    )


def _slide_text_fits(blocks, text_width=SLIDE_LINE_WIDTH) -> bool:
    """Input envelope, not a claim that every presentation viewer lays out alike."""
    if sum(_slide_text_size(block) for block in blocks) > SLIDE_PROSE_LIMIT:
        return False
    lines = max(0, len(blocks) - 1)  # conservative gap between display blocks
    lines += sum(_slide_text_lines(block, text_width) for block in blocks)
    return lines <= SLIDE_LINE_LIMIT


def _slide_prose_chunks(kind, inlines, text_width=SLIDE_LINE_WIDTH):
    """Prefer sentences, then rebalance an unavoidable short continuation."""
    for inline in inlines:
        if _slide_text_size(inline) > SLIDE_TEXT_LIMIT:
            raise ValueError("Slide contains an indivisible inline exceeding its text budget")
    if not inlines:
        return
    sentence_ends = {index + 1 for index, inline in enumerate(inlines)
                     if re.search(r'[.!?][\u201d\u2019"\')\]]?$', _slide_visible_text(inline).rstrip())}
    parts, start = [], 0
    def fits(left, right):
        return _slide_text_fits([{"t": kind, "c": inlines[left:right]}], text_width)
    while start < len(inlines):
        stop = start
        while stop < len(inlines) and fits(start, stop + 1):
            stop += 1
        if stop == start:
            raise ValueError("Slide contains an indivisible inline exceeding its line budget")
        if stop < len(inlines):
            sentences = [end for end in sentence_ends if start < end <= stop]
            if sentences:
                stop = max(sentences)
        parts.append((start, stop))
        start = stop
    if len(parts) > 1 and _slide_text_size(inlines[parts[-1][0]:]) < SLIDE_MIN_CONTINUATION:
        left, end = parts[-2][0], parts[-1][1]
        choices = [middle for middle in range(left + 1, end)
                   if _slide_text_size(inlines[left:middle]) >= SLIDE_MIN_CONTINUATION
                   and _slide_text_size(inlines[middle:end]) >= SLIDE_MIN_CONTINUATION
                   and fits(left, middle) and fits(middle, end)]
        if choices:
            middle = min(choices, key=lambda value: (value not in sentence_ends,
                         abs(_slide_text_size(inlines[left:value]) - _slide_text_size(inlines[value:end]))))
            parts[-2:] = [(left, middle), (middle, end)]
    for left, right in parts:
        yield {"t": kind, "c": inlines[left:right]}


def _slide_units(block, text_width=SLIDE_LINE_WIDTH):
    """Yield bounded display units without discarding authored content."""
    kind, content = block["t"], block.get("c")
    if kind in {"Para", "Plain"}:
        if _slide_text_unit(block):
            yield from _slide_prose_chunks(kind, content, text_width)
        else:
            yield block
    elif kind in {"BulletList", "OrderedList"}:
        items = content if kind == "BulletList" else content[1]
        for index, item in enumerate(items):
            for child in item:
                for unit in _slide_units(child, max(12, text_width - 6)):
                    if kind == "BulletList":
                        yield {"t": kind, "c": [[unit]]}
                    else:
                        attributes = [content[0][0] + index, *content[0][1:]]
                        yield {"t": kind, "c": [attributes, [[unit]]]}
    elif kind == "Figure":
        attributes, caption, body = content
        if (
            len(body) != 1
            or body[0]["t"] not in {"Plain", "Para"}
            or len(body[0]["c"]) != 1
            or body[0]["c"][0]["t"] != "Image"
        ):
            raise ValueError("Slides require a single registered image per figure")
        # PPTX also renders a standalone image's alt text as its caption.
        # Keep that label short and descriptive; the complete figure caption
        # follows on its own slide.
        original = body[0]["c"][0]
        label = (
            Path(original["c"][-1][0]).stem.replace("-", " ").capitalize() + " diagram"
        )
        image = {
            "t": "Image",
            "c": [original["c"][0], [{"t": "Str", "c": label}], original["c"][-1]],
        }
        yield {"t": "Div", "c": [attributes, [{"t": "Para", "c": [image]}]]}
        for child in caption[1]:
            yield from _slide_units(child)
    elif kind == "Table":
        attributes, caption, columns, head, bodies, foot = content
        if (
            len(columns) > 3
            or len(bodies) != 1
            or bodies[0][2]
            or foot[1]
            or any(
                cell[2:4] != [1, 1] for row in head[1] + bodies[0][3] for cell in row[1]
            )
        ):
            raise ValueError(
                "Slide table requires simple rows without spanning cells or footers"
            )
        for child in caption[1]:
            yield from _slide_units(child)
        rows = bodies[0][3]
        groups, group, size = [], [], _slide_text_size(head)
        for row in rows:
            cost = _slide_text_size(row)
            if cost + _slide_text_size(head) > SLIDE_TEXT_LIMIT:
                raise ValueError("Slide table row exceeds its text budget")
            if group and (len(group) == 3 or size + cost > SLIDE_TEXT_LIMIT):
                groups.append(group)
                group, size = [], _slide_text_size(head)
            group.append(row)
            size += cost
        if group or not groups:
            groups.append(group)
        for index, group in enumerate(groups):
            attr = attributes if index == 0 else ["", attributes[1], attributes[2]]
            body = [bodies[0][0], bodies[0][1], [], group]
            yield {"t": kind, "c": [attr, [None, []], columns, head, [body], foot]}
    elif kind == "Div":
        for index, unit in enumerate(
            unit for child in content[1] for unit in _slide_units(child, text_width)
        ):
            attributes = (
                content[0] if index == 0 else ["", content[0][1], content[0][2]]
            )
            yield {"t": kind, "c": [attributes, [unit]]}
    elif kind == "CodeBlock":
        if len(content[1]) > SLIDE_TEXT_LIMIT or any(
            len(line) > 80 for line in content[1].splitlines()
        ):
            raise ValueError("Slide code block exceeds its text or line budget")
        yield block
    else:
        raise ValueError(f"Unsupported slide display block: {kind}")


def paginate_slides(document: dict) -> dict:
    """Pack coherent text within an explicit envelope; preserve display barriers."""
    output = dict(document, blocks=[])
    title, attributes, count = [{"t": "Str", "c": "Review draft"}], ["", [], []], 0
    pending_header, packed = None, []
    aliases = {}

    def flush():
        nonlocal count, packed
        if not packed:
            return
        count += 1
        heading = title if count == 1 else [*title, {"t": "Space"}, {"t": "Str", "c": f"({count})"}]
        attr = attributes if count == 1 else ["", [], []]
        anchors = [anchor for _, values in packed for anchor in values]
        if not attr[0] and anchors:
            attr = [anchors[-1], [], []]
        for anchor in anchors:
            if anchor != attr[0]:
                aliases[anchor] = attr[0]
        output["blocks"].append({"t": "Header", "c": [2, attr, heading]})
        output["blocks"].extend(unit for unit, _ in packed)
        packed = []

    for block in document["blocks"]:
        if block["t"] == "Header":
            flush()
            if pending_header is not None:
                output["blocks"].append(pending_header)
            level, attributes, title = block["c"]
            if _slide_text_size(title) > 80:
                raise ValueError("Slide heading exceeds its text budget")
            count = 0
            pending_header = {"t": "Header", "c": [2, attributes, title]} if level > 1 else None
            if level == 1:
                output["blocks"].append(block)
                attributes = ["", [], []]
            continue
        for unit in _slide_units(block):
            pending_header = None
            anchors = []
            while unit["t"] == "Div":
                if unit["c"][0][0]:
                    anchors.append(unit["c"][0][0])
                unit = unit["c"][1][0]
            isolated = block["t"] in {"Figure", "Table", "CodeBlock"} or not _slide_text_unit(unit)
            if isolated:
                flush()
                packed.append((unit, anchors))
                flush()
            else:
                if packed and not _slide_text_fits([*(value for value, _ in packed), unit]):
                    flush()
                if not _slide_text_fits([unit]):
                    raise ValueError("Slide text unit exceeds its line or text budget")
                packed.append((unit, anchors))
    flush()
    if pending_header is not None:
        output["blocks"].append(pending_header)

    def remap(node):
        if isinstance(node, list):
            return [remap(value) for value in node]
        if not isinstance(node, dict):
            return node
        node = {key: remap(value) for key, value in node.items()}
        if node.get("t") == "Link":
            target = node["c"][-1][0]
            if target.startswith("#") and unquote(target[1:]) in aliases:
                node["c"][-1][0] = "#" + aliases[unquote(target[1:])]
        return node

    return remap(output)


def digest(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def run(arguments: list[str], *, root: Path, data: str | None = None) -> str:
    environment = dict(os.environ, SOURCE_DATE_EPOCH="0")
    result = subprocess.run(
        arguments,
        input=data,
        capture_output=True,
        text=True,
        cwd=root,
        timeout=TIMEOUT,
        env=environment,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            f"{Path(arguments[0]).name} failed (exit {result.returncode}); previous review outputs were not changed"
        )
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
        if name == "pandoc-crossref" and not re.search(
            r"\bPandoc v" + re.escape(TOOLS["pandoc"]) + r"(?:\s|,|$)", banner
        ):
            raise ValueError("pandoc-crossref must match the pinned Pandoc build")
        result[name] = {
            "version": version,
            "binary_sha256": digest(Path(executable).resolve()),
        }
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


def rebase_links(node, root: Path, commit: str, figure_targets: dict | None = None):
    """Bind source links to one public revision; keep figures local/offline."""
    if isinstance(node, list):
        return [rebase_links(value, root, commit, figure_targets) for value in node]
    if not isinstance(node, dict):
        return node
    node = {
        key: rebase_links(value, root, commit, figure_targets)
        for key, value in node.items()
    }
    if node.get("t") in {"RawBlock", "RawInline"}:
        raise ValueError(
            "Raw renderer markup requires an explicit rendering integration"
        )
    if node.get("t") == "CodeBlock" and "mermaid" in node["c"][0][1]:
        raise ValueError("Mermaid figures need an explicit renderer")
    if node.get("t") not in {"Link", "Image"}:
        return node
    target = node["c"][-1][0]
    parsed = urlsplit(target)
    if node["t"] == "Image":
        if figure_targets is None or target not in figure_targets:
            raise ValueError(
                "Manuscript figures require an explicit offline rendering integration"
            )
        node["c"][-1][0] = figure_targets[target]
        return node
    if parsed.scheme or parsed.netloc or not parsed.path:
        return node
    path = (root / MANUSCRIPT_PATH / unquote(parsed.path)).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError("Manuscript link escapes repository")
    relative = path.relative_to(root.resolve()).as_posix()
    kind = "tree" if path.is_dir() else "blob"
    node["c"][-1][0] = (
        f"https://github.com/docxology/docxology/{kind}/{commit}/{quote(relative, safe='/')}"
    )
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
            if (
                not reader.pages
                or "docxology" not in text
                or "References" not in text
                or "@sec:" in text
            ):
                raise ValueError("PDF text or references did not render")
        elif format_name in {"epub", "slides"}:
            with zipfile.ZipFile(path) as package:
                if package.testzip() is not None:
                    raise ValueError("Corrupt rendered package")
                required = (
                    "META-INF/container.xml"
                    if format_name == "epub"
                    else "ppt/presentation.xml"
                )
                if required not in package.namelist():
                    raise ValueError("Rendered package is missing its document")
        else:
            text = path.read_text(encoding="utf-8")
            if 'id="refs"' not in text or "@sec:" in text or "@docxologyIndex" in text:
                raise ValueError("HTML references did not render")
        artifacts[path.name] = {
            "format": format_name,
            "bytes": size,
            "sha256": digest(path),
        }
    return artifacts


def render_manuscript(
    root: Path,
    output: Path,
    *,
    template_root: Path | None = None,
    template_python: Path | None = None,
) -> dict:
    root = root.absolute()
    output = new_review_directory(root, output)
    validation = validate_manuscript(root)
    if not validation["source_valid"]:
        raise ValueError("Manuscript structural source checks failed")
    config_path = root / MANUSCRIPT_PATH / "config.yaml"
    inputs = [config_path, root / MANUSCRIPT_PATH / "references.bib"]
    inputs.extend(root / MANUSCRIPT_PATH / name for name in validation["sections"])
    inputs.extend(
        [
            root / "code/src/manuscript_rendering.py",
            root / "code/orchestrators/render_manuscript.py",
        ]
    )
    frozen = {
        path: read_generated_output_text(root, path, newline="") for path in inputs
    }
    if any(text is None for text in frozen.values()):
        raise ValueError("Required rendering source is missing")
    source_hashes = {
        path.relative_to(root).as_posix(): hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()
        for path, text in frozen.items()
    }
    config = yaml.load(frozen[config_path], Loader=UniqueKeyLoader)
    if config["render"].get("toolchain") != TOOLS:
        raise ValueError("Manuscript configuration must declare the pinned toolchain")
    formats = validation["configured_render_formats"]
    if not formats or any(name not in OUTPUTS for name in formats):
        raise ValueError(
            "Configured formats are not supported by the declared renderer"
        )
    template_receipt = None
    if "pdf" in formats:
        if template_root is None or template_python is None:
            raise ValueError(
                "PDF requires explicit --template-root and --template-python"
            )
        if (
            config["render"].get("template") != TEMPLATE
            or config["paper"].get("cover") != COVER
        ):
            raise ValueError(
                "PDF requires the pinned template and declared cover producer"
            )
        for relative in (
            "docs/manuscript/preamble.md",
            "code/src/manuscript_template.py",
        ):
            path = root / relative
            inputs.append(path)
            frozen[path] = read_generated_output_text(root, path, newline="")
            if frozen[path] is None:
                raise ValueError("Declared native rendering source is missing")
            source_hashes[relative] = hashlib.sha256(
                frozen[path].encode("utf-8")
            ).hexdigest()
    figure_config = config["render"].get("figures")
    if figure_config is not None and figure_config != {
        "producer": PRODUCER,
        "ids": list(FIGURES),
    }:
        raise ValueError("Unknown manuscript figure producer or registry")
    if figure_config:
        path = root / "code/src/manuscript_figures.py"
        inputs.append(path)
        frozen[path] = read_generated_output_text(root, path, newline="")
        if frozen[path] is None:
            raise ValueError("Declared figure producer source is missing")
        source_hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
            frozen[path].encode()
        ).hexdigest()
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
    with tempfile.TemporaryDirectory(
        prefix=".docxology-render-", dir=output.parent
    ) as scratch_name:
        scratch = Path(scratch_name)
        data_dir = scratch / "pandoc-data"
        data_dir.mkdir()
        pandoc = ["pandoc", "--data-dir", str(data_dir)]
        references = scratch / "references.bib"
        references.write_text(frozen[inputs[1]], encoding="utf-8")
        bibliography = json.loads(
            run(
                [
                    *pandoc,
                    "--from=biblatex",
                    "--to=csljson",
                    "--fail-if-warnings",
                    str(references),
                ],
                root=root,
            )
        )
        if len(bibliography) != validation["citation_count"]:
            raise ValueError(
                "Parsed bibliography count differs from structural inventory"
            )
        document = json.loads(
            run(
                [*pandoc, "--from=markdown", "--to=json"],
                root=root,
                data="\n\n".join(sections),
            )
        )
        figure_receipt = render_figures(scratch / "figures") if figure_config else None
        targets = (
            {target: f"figures/{name}.png" for target, name in SOURCE_TARGETS.items()}
            if figure_config
            else None
        )
        document = rebase_links(document, root, commit, targets)
        document["blocks"].insert(
            0,
            {
                "t": "Para",
                "c": [
                    {
                        "t": "Str",
                        "c": f"Review draft {config['paper']['version']}. Manuscript text and original figures: {config['metadata']['license']}. Human and editorial reviews pending.",
                    }
                ],
            },
        )
        metadata = document["meta"]
        for name, value in {
            "title": config["paper"]["title"],
            "subtitle": config["paper"]["subtitle"],
            "date": config["paper"]["date"],
            "lang": config["metadata"]["language"],
            "rights": config["metadata"]["license"],
            "version": config["paper"]["version"],
        }.items():
            metadata[name] = {"t": "MetaString", "c": value}
        metadata["author"] = {
            "t": "MetaList",
            "c": [
                {"t": "MetaString", "c": author["name"]} for author in config["authors"]
            ],
        }
        data = json.dumps(document, ensure_ascii=False)
        common = [
            *pandoc,
            "--from=json",
            "--standalone",
            "--number-sections",
            "--filter=pandoc-crossref",
            "--citeproc",
            "--bibliography",
            str(references),
            "--resource-path",
            str(scratch),
            "--fail-if-warnings",
        ]
        for format_name in formats:
            arguments = [*common, "--output", str(scratch / OUTPUTS[format_name])]
            if format_name == "pdf":
                project = scratch / "native-project"
                folder = project / "docs/manuscript"
                folder.mkdir(parents=True)
                figures = project / "docs/output/figures"
                figures.mkdir(parents=True)
                if figure_config:
                    compiled_figures = project / "output/figures"
                    compiled_figures.mkdir(parents=True)
                    for asset in (scratch / "figures").iterdir():
                        shutil.copyfile(asset, figures / asset.name)
                        shutil.copyfile(asset, compiled_figures / asset.name)
                cover_pdf(
                    figures / "docxology-cover.pdf",
                    version=config["paper"]["version"],
                    commit=commit,
                    license_name=config["metadata"]["license"],
                )
                staged = {
                    key: config[key]
                    for key in (
                        "paper",
                        "authors",
                        "publication",
                        "metadata",
                        "keywords",
                    )
                    if key in config
                }
                staged = json.loads(json.dumps(staged))
                staged["paper"]["cover"] = {
                    "image": "../output/figures/docxology-cover.pdf",
                    "alt": COVER["alt"],
                }
                staged["rendering"] = {
                    "section_breaks": False,
                    "cover_height_fraction": 0.42,
                }
                staged["metadata"].update(fontsize="10pt", geometry="margin=0.85in")
                staged["publication"]["publisher"] = "Daniel Ari Friedman"
                staged["publication"]["suggested_citation"] = (
                    "Friedman, D. A. (2026). docxology: Research, Software, and Citation Index. Repository-methods draft; editorial review pending."
                )
                (folder / "config.yaml").write_text(
                    yaml.safe_dump(staged, sort_keys=False), encoding="utf-8"
                )
                (folder / "references.bib").write_text(
                    frozen[inputs[1]], encoding="utf-8"
                )
                (folder / "preamble.md").write_text(
                    frozen[root / "docs/manuscript/preamble.md"], encoding="utf-8"
                )
                # The AST has already rejected raw markup/images and bound local
                # evidence links to the exact repository revision.
                native_document = json.loads(data)
                if figure_config:
                    native_targets = {
                        f"figures/{name}.png": f"../output/figures/{name}.pdf"
                        for name in FIGURES
                    }
                    native_document = rebase_links(
                        native_document, root, commit, native_targets
                    )
                body = run(
                    [*pandoc, "--from=json", "--to=markdown", "--wrap=none"],
                    root=root,
                    data=json.dumps(native_document),
                )
                (folder / "00_body.md").write_text(body, encoding="utf-8")
                worker = project / "native-worker.py"
                worker.write_text(
                    frozen[root / "code/src/manuscript_template.py"], encoding="utf-8"
                )
                staged_hashes = {
                    path.relative_to(project).as_posix(): digest(path)
                    for path in sorted(
                        [
                            *(project / "docs").rglob("*"),
                            *(project / "output/figures").rglob("*"),
                        ]
                    )
                    if path.is_file()
                }
                worker_hash = digest(worker)
                template_receipt = native_pdf(
                    template_root, template_python, project, worker
                )
                after_hashes = {
                    path.relative_to(project).as_posix(): digest(path)
                    for path in sorted(
                        [
                            *(project / "docs").rglob("*"),
                            *(project / "output/figures").rglob("*"),
                        ]
                    )
                    if path.is_file()
                }
                if after_hashes != staged_hashes or digest(worker) != worker_hash:
                    raise ValueError(
                        "Staged rendering sources changed; no review outputs were published"
                    )
                template_receipt["staged_source_sha256"] = staged_hashes
                shutil.copyfile(
                    project / "output/pdf/docxology-methods_combined.pdf",
                    scratch / OUTPUTS["pdf"],
                )
                shutil.copyfile(
                    figures / "docxology-cover.pdf", scratch / "docxology-cover.pdf"
                )
                shutil.copyfile(
                    project / "native-render.log", scratch / "native-render.log"
                )
                shutil.rmtree(project)
                continue
            else:
                arguments += [
                    "--to="
                    + {"html": "html5", "epub": "epub3", "slides": "pptx"}[format_name]
                ]
                if format_name == "slides":
                    resolved = json.loads(
                        run([*common, "--to=json"], root=root, data=data)
                    )
                    slides = paginate_slides(resolved)
                    arguments = [
                        *pandoc,
                        "--from=json",
                        "--standalone",
                        "--to=pptx",
                        "--slide-level=2",
                        "--resource-path",
                        str(scratch),
                        "--fail-if-warnings",
                        "--output",
                        str(scratch / OUTPUTS[format_name]),
                    ]
                    run(
                        arguments,
                        root=root,
                        data=json.dumps(slides, ensure_ascii=False),
                    )
                    continue
            run(arguments, root=root, data=data)
        artifacts = validate_artifacts(scratch, formats)
        if figure_config:
            for name, alt in FIGURES.items():
                for suffix in ("pdf", "png"):
                    asset = scratch / "figures" / f"{name}.{suffix}"
                    artifacts[f"figures/{asset.name}"] = {
                        "format": "figure",
                        "figure_id": name,
                        "bytes": asset.stat().st_size,
                        "sha256": digest(asset),
                        "alt": alt,
                    }
        if template_receipt is not None:
            artifacts["docxology-cover.pdf"] = {
                "format": "cover",
                "bytes": (scratch / "docxology-cover.pdf").stat().st_size,
                "sha256": digest(scratch / "docxology-cover.pdf"),
                "alt": COVER["alt"],
            }
        if any(
            digest(path) != source_hashes[path.relative_to(root).as_posix()]
            for path in inputs
        ):
            raise ValueError(
                "Rendering sources changed; no review outputs were published"
            )
        receipt = {
            "schema_version": "1.0",
            "evidence_kind": "offline manuscript draft render",
            "source_sha256": source_hashes,
            "source_link_commit": commit,
            "toolchain": tools,
            "template": template_receipt,
            "artifacts": artifacts,
            "slide_layout": {"producer": SLIDE_LAYOUT, "text_budget": SLIDE_TEXT_LIMIT, "prose_budget": SLIDE_PROSE_LIMIT, "line_width": SLIDE_LINE_WIDTH, "line_limit": SLIDE_LINE_LIMIT}
            if "slides" in formats
            else None,
            "figures": figure_receipt,
            "bibliography_parser": "Pandoc biblatex reader",
            "bibliography_entries": len(bibliography),
            "license": config["metadata"]["license"],
            "editorial_review": "pending",
            "human_visual_review": "pending",
            "scientific_validity_assessed": False,
            "publication_readiness_assessed": False,
            "network_fetches_requested": False,
        }
        (scratch / "render-receipt.json").write_text(
            json.dumps(receipt, indent=2) + "\n", encoding="utf-8"
        )
        new_review_directory(root, output)
        shutil.rmtree(data_dir)
        references.unlink()
        scratch.rename(output)
    return receipt
