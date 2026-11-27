"""Stage the repository-methods draft for the shared Template reader pipeline."""

from __future__ import annotations

import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import quote, unquote, urlsplit

import pymupdf
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import docxology_tools  # noqa: E402,F401
from docxology_tools.manuscript_figures import FIGURES, SOURCE_TARGETS, render_figures  # noqa: E402
from docxology_tools.manuscript_template import cover_pdf  # noqa: E402

LINK = re.compile(r"(?P<open>\]\()(?P<target>[^\s)]+)\)")
SECTIONS = re.compile(r"^(?:[0-9]{2}|S[0-9]{2})_")


def stage(root: Path) -> None:
    """Render owned diagrams and prepare a PDF/HTML view of all source sections."""
    source = root / "docs/manuscript"
    output = root / "output"
    output.mkdir(exist_ok=False)
    commit = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True
    ).strip()
    files = set(
        subprocess.check_output(["git", "ls-files", "-z"], cwd=root, text=True).split(
            "\0"
        )
    )

    def link(match: re.Match[str]) -> str:
        target = match["target"]
        if target in SOURCE_TARGETS:
            return f"](../figures/{SOURCE_TARGETS[target]}.png)"
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            return match[0]
        path = (source / unquote(parsed.path)).resolve().relative_to(root)
        relative = path.as_posix()
        if relative in files:
            kind = "blob"
        elif any(name.startswith(relative + "/") for name in files):
            kind = "tree"
        else:
            raise ValueError(
                f"Manuscript target is absent from the Git index: {relative}"
            )
        fragment = f"#{parsed.fragment}" if parsed.fragment else ""
        return f"](https://github.com/docxology/docxology/{kind}/{commit}/{quote(relative)}{fragment})"

    staged = output / "manuscript"
    staged.mkdir()
    for path in sorted(source.glob("*.md")):
        if SECTIONS.match(path.name):
            (staged / path.name).write_text(
                LINK.sub(link, path.read_text(encoding="utf-8")), encoding="utf-8"
            )
    for name in ("preamble.md", "references.bib"):
        shutil.copyfile(source / name, staged / name)

    config = yaml.safe_load((source / "config.yaml").read_text())
    config["render"]["formats"] = dict(
        pdf=True, html=True, slides=False, docx=False, epub=False
    )
    cover = config["paper"]["cover"]
    cover["image"] = "../figures/docxology-cover.png"
    (staged / "config.yaml").write_text(
        "# Generated manuscript ordering\n" + yaml.safe_dump(config, sort_keys=False)
    )

    figures = output / "figures"
    render_figures(figures)
    cover_source = figures / "docxology-cover.pdf"
    cover_pdf(
        cover_source,
        version=config["paper"]["version"],
        commit=commit,
        license_name=config["metadata"]["license"],
    )
    with pymupdf.open(cover_source) as pdf:
        pdf[0].get_pixmap(matrix=pymupdf.Matrix(1.5, 1.5), alpha=False).save(
            figures / "docxology-cover.png"
        )
    registry = [
        {
            "label": "fig:" + name.replace("-", "_"),
            "filename": name + ".png",
            "alt_text": alt,
        }
        for name, alt in FIGURES.items()
    ]
    (figures / "figure_registry.json").write_text(
        json.dumps({"schema_version": 1, "figures": registry}, indent=2) + "\n"
    )


if __name__ == "__main__":
    stage(Path(__file__).resolve().parents[2])
