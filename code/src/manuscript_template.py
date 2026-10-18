"""Pinned docxology/template export and isolated native PDF worker.

The renderer executes reviewed repository code and TeX. Process isolation and
an environment allowlist avoid ambient Python imports/credentials
they are not
an OS sandbox or a network security boundary.
"""
from __future__ import annotations

import hashlib
import io
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tarfile
import tomllib

TEMPLATE = {"repository": "docxology/template", "revision": "3462d19761cc87d09a0b780ef978fa9efc142723", "version": "4.0.2"}
COVER = {"producer": "repository-source-flow-v1", "alt": "Reviewed sources pass through shared identity and parsing policy into generated views and commit-bound release evidence. New observations require review before becoming curated claims."}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def export_template(repository: Path, destination: Path) -> dict:
    """Export one committed tree
    never import a mutable template checkout."""
    result = subprocess.run(["git", "archive", "--format=tar", TEMPLATE["revision"], "infrastructure", "pyproject.toml", "uv.lock"],
                            cwd=repository, capture_output=True, timeout=60, check=False)
    if result.returncode or len(result.stdout) > 100 * 1024 * 1024:
        raise ValueError("Pinned docxology/template source is unavailable or exceeds the export bound")
    destination.mkdir()
    with tarfile.open(fileobj=io.BytesIO(result.stdout)) as archive:
        members = archive.getmembers()
        if len(members) > 5000 or sum(member.size for member in members) > 100 * 1024 * 1024:
            raise ValueError("Template archive exceeds the extraction bound")
        names = set()
        for member in members:
            path = Path(member.name)
            if (path.is_absolute() or ".." in path.parts or "\\" in member.name or member.name in names
                    or not (member.isfile() or member.isdir())
                    or not path.parts or path.parts[0] not in {"infrastructure", "pyproject.toml", "uv.lock"}):
                raise ValueError("Unsafe template archive member")
            names.add(member.name)
        archive.extractall(destination, filter="data")
    metadata = tomllib.loads((destination / "pyproject.toml").read_text())
    if metadata["project"]["version"] != TEMPLATE["version"]:
        raise ValueError("Pinned template version differs from its metadata")
    return {**TEMPLATE, "archive_sha256": hashlib.sha256(result.stdout).hexdigest(),
            "source_sha256": {path.relative_to(destination).as_posix(): sha256(path)
                              for path in sorted(destination.rglob("*")) if path.is_file()}}


def cover_pdf(path: Path, *, version: str, commit: str, license_name: str) -> None:
    """Draw an informative vector figure from the manuscript's qualitative model."""
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor
    c = canvas.Canvas(str(path), pagesize=(960, 510), invariant=1)
    c.setTitle("docxology source authority and release evidence")
    c.setAuthor("Daniel Ari Friedman")
    c.setFillColor(HexColor("#10263b"))
    c.rect(0, 0, 960, 510, fill=1, stroke=0)
    c.setFillColor(HexColor("#eff7f8"))
    c.setFont("Helvetica-Bold", 30)
    c.drawString(38, 455, "From source authority to deployed evidence")
    blocks = [("REVIEWED SOURCES", ["Curated tables", "Original archive"]),
              ("SHARED POLICY", ["Permanent identities", "Parsers and contracts"]),
              ("GENERATED VIEWS", ["HTML and JSON", "Citations and indexes"]),
              ("RELEASE EVIDENCE", ["Independent checks", "Commit-bound deploy"])]
    for i, (title, lines) in enumerate(blocks):
        x = 38 + i * 231
        c.setFillColor(HexColor("#193e56"))
        c.roundRect(x, 204, 206, 184, 12, fill=1, stroke=0)
        c.setFillColor(HexColor("#65d8c4"))
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x + 14, 354, title)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont("Helvetica", 18)
        for j, line in enumerate(lines):
            c.drawString(x + 14, 310 - j * 28, line)
        if i < 3:
            c.setStrokeColor(HexColor("#65d8c4"))
            c.setLineWidth(3)
            c.line(x + 209, 290, x + 224, 290)
            c.line(x + 217, 297, x + 224, 290)
            c.line(x + 217, 283, x + 224, 290)
    c.setFillColor(HexColor("#eff7f8"))
    c.setFont("Helvetica", 19)
    c.drawString(38, 138, "New observations require review before becoming curated claims.")
    c.setFont("Helvetica", 17)
    c.drawString(38, 91, "Hashes bind bytes  |  Tests exercise behavior  |  Human review remains separate")
    c.setFillColor(HexColor("#65d8c4"))
    c.setFont("Helvetica-Bold", 15)
    c.drawString(38, 40, f"docxology / Review draft {version} / {license_name}")
    c.setFont("Helvetica", 12)
    c.drawString(38, 16, f"Source: github.com/docxology/docxology | revision {commit}")
    c.save()


def native_pdf(template_root: Path, template_python: Path, project: Path, worker: Path) -> dict:
    snapshot = project / "template-source"
    receipt = export_template(template_root, snapshot)
    # The existing interpreter supplies dependencies. This command does not
    # install packages or change either repository working tree.
    environment = {key: os.environ[key] for key in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR", "SYSTEMROOT") if key in os.environ}
    environment.update(SOURCE_DATE_EPOCH="0", PYTHONDONTWRITEBYTECODE="1", LATEX_TIMEOUT="60")
    command = [str(template_python.absolute()), "-I", "-B", str(worker), str(project)]
    with subprocess.Popen(command, cwd=project, env=environment, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          start_new_session=True) as process:
        try:
            output, _ = process.communicate(timeout=180)
        except subprocess.TimeoutExpired as exc:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
            raise ValueError("Native template PDF render timed out; no review outputs published") from exc
    (project / "native-render.log").write_bytes(output)
    if process.returncode:
        raise ValueError("Native template PDF render failed; no review outputs published: " + output.decode("utf-8", errors="replace")[-3000:])
    log_text = output.decode("utf-8", errors="replace")
    if re.search(r"undefined (?:references|citations)|(?:Citation|Reference) .+ undefined|bibliography processing failed|crossref.*(?:not found|unavailable)", log_text, re.I):
        raise ValueError("Native render has unresolved references or unavailable bibliography tools")
    current = {path.relative_to(snapshot).as_posix(): sha256(path)
               for path in sorted(snapshot.rglob("*")) if path.is_file()}
    if current != receipt["source_sha256"]:
        raise ValueError("Committed template export changed during rendering")
    result = json.loads((project / "worker-result.json").read_text())
    receipt["runtime"] = result
    return receipt


def native_diagnostics(text: str) -> list[str]:
    """Recognize actual diagnostics without matching package descriptions."""
    pattern = re.compile(r"undefined (?:references|citations)|(?:Citation|Reference) .+ undefined|Warning--|I couldn't open|There (?:was|were) [1-9][0-9]* error message|^! ", re.I)
    return [line for line in text.splitlines() if pattern.search(line)]


def worker_main(project: Path) -> None:
    """Standalone -I entry point
    import only the frozen template source."""
    snapshot = project / "template-source"
    sys.path.insert(0, str(snapshot))
    import infrastructure.rendering.pdf_renderer as implementation
    from infrastructure.rendering.config import RenderingConfig
    if not Path(implementation.__file__).resolve().is_relative_to(snapshot.resolve()):
        raise ValueError("Template import escaped its committed export")
    folder = project / "docs/manuscript"
    output = project / "output"
    renderer = implementation.PDFRenderer(RenderingConfig(
        manuscript_dir=str(folder), figures_dir=str(project / "docs/output/figures"),
        output_dir=str(output), pdf_dir=str(output / "pdf"), latex_compiler="xelatex",
        enable_pdf=True, enable_html=False, enable_slides=False, enable_docx=False, enable_epub=False))
    pdf = renderer.render_combined([folder / "00_body.md"], folder, project_name="docxology-methods")
    if Path(pdf).resolve() != (output / "pdf/docxology-methods_combined.pdf").resolve():
        raise ValueError("Unexpected native PDF result")
    # TeX's final log and BibTeX output are authoritative even if the template
    # logs only a generic success message after a tolerated warning.
    for path in output.rglob("*"):
        if path.suffix in {".log", ".blg"}:
            text = path.read_text(errors="replace")
            diagnostics = native_diagnostics(text)
            if diagnostics:
                raise ValueError("Unresolved native bibliography/reference diagnostic: " + path.name + " " + " | ".join(diagnostics))
    from importlib.metadata import version
    result = {"python": sys.version.split()[0], "python_binary_sha256": sha256(Path(sys.executable).resolve()),
              "dependencies": {name: version(name) for name in ("pypdf", "matplotlib", "PyYAML")}}
    (project / "worker-result.json").write_text(json.dumps(result))


if __name__ == "__main__":
    worker_main(Path(sys.argv[1]).resolve())
