"""Real draft rendering is separate from structural and human-review evidence."""

from pathlib import Path
import hashlib
import json
import os
import sys

import pytest


@pytest.mark.manuscript_render
def test_slide_link_targets_survive_real_pptx(tmp_path):
    import subprocess
    import zipfile
    import xml.etree.ElementTree as ET

    source = "## Target {#target}\n\n::: {#inner}\nPayload\n:::\n\n[Jump target](#target) and [Jump inner](#inner)\n"
    document = json.loads(
        subprocess.run(
            ["pandoc", "--from=markdown", "--to=json"],
            input=source,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    output = tmp_path / "links.pptx"
    subprocess.run(
        [
            "pandoc",
            "--from=json",
            "--to=pptx",
            "--slide-level=2",
            "--fail-if-warnings",
            "--output",
            str(output),
        ],
        input=json.dumps(rendering.paginate_slides(document)),
        text=True,
        capture_output=True,
        check=True,
    )
    links = []
    with zipfile.ZipFile(output) as package:
        for name in package.namelist():
            if name.startswith("ppt/slides/slide") and name.endswith(".xml"):
                tree = ET.fromstring(package.read(name))
                relations_name = "ppt/slides/_rels/" + Path(name).name + ".rels"
                relations = {
                    item.attrib["Id"]: item.attrib
                    for item in ET.fromstring(package.read(relations_name))
                }
                for link in tree.iter(
                    "{http://schemas.openxmlformats.org/drawingml/2006/main}hlinkClick"
                ):
                    target = relations[
                        link.attrib[
                            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
                        ]
                    ]
                    assert target["Type"].endswith("/slide")
                    links.append(target["Target"])
    assert len(links) == 2
    assert len(set(links)) == 1


def test_slide_link_targets_keep_nested_container_aliases():
    text = {"t": "Para", "c": [{"t": "Str", "c": "Payload"}]}
    nested = {
        "t": "Div",
        "c": [["outer", [], []], [{"t": "Div", "c": [["inner", [], []], [text]]}]],
    }
    jumps = {
        "t": "Para",
        "c": [
            {
                "t": "Link",
                "c": [["", [], []], [{"t": "Str", "c": name}], ["#" + name, ""]],
            }
            for name in ("target", "outer", "inner")
        ],
    }
    header = {
        "t": "Header",
        "c": [2, ["target", [], []], [{"t": "Str", "c": "Target"}]],
    }
    document = {"meta": {}, "blocks": [header, nested, jumps]}
    output = rendering.paginate_slides(document)
    assert output["blocks"][0]["c"][1][0] == "target"
    assert [inline["c"][-1][0] for inline in output["blocks"][-1]["c"]] == [
        "#target"
    ] * 3
    assert jumps["c"][1]["c"][-1][0] == "#outer"


def test_slide_pagination_preserves_long_prose_and_links():
    link = {
        "t": "Link",
        "c": [
            ["", [], []],
            [{"t": "Str", "c": "source"}],
            ["https://example.org/evidence", ""],
        ],
    }
    inlines = [{"t": "Str", "c": "retained"}, {"t": "Space"}] * 140 + [link]
    document = {
        "meta": {},
        "blocks": [
            {
                "t": "Header",
                "c": [2, ["methods", [], []], [{"t": "Str", "c": "Methods"}]],
            },
            {"t": "Para", "c": inlines},
        ],
    }
    output = rendering.paginate_slides(document)
    paragraphs = [block for block in output["blocks"] if block["t"] == "Para"]
    assert len(paragraphs) >= 3
    assert [inline for block in paragraphs for inline in block["c"]] == inlines
    assert all(
        rendering._slide_text_size(block) <= rendering.SLIDE_PROSE_LIMIT
        and rendering._slide_text_fits([block])
        for block in paragraphs
    )
    headers = [block for block in output["blocks"] if block["t"] == "Header"]
    assert headers[0]["c"][1][0] == "methods"
    assert all(header["c"][1][0] == "" for header in headers[1:])
    assert document["blocks"][1]["c"] == inlines


@pytest.mark.parametrize("kind", ["BulletList", "OrderedList"])
def test_slide_pagination_keeps_list_order_and_numbering(kind):
    items = [
        [{"t": "Para", "c": [{"t": "Str", "c": f"item-{index}"}]}]
        for index in range(12)
    ]
    content = (
        items
        if kind == "BulletList"
        else [[4, {"t": "Decimal"}, {"t": "Period"}], items]
    )
    output = rendering.paginate_slides(
        {"meta": {}, "blocks": [{"t": kind, "c": content}]}
    )
    lists = [block for block in output["blocks"] if block["t"] == kind]
    actual = [
        block["c"][0] if kind == "BulletList" else block["c"][1][0] for block in lists
    ]
    assert actual == items
    if kind == "OrderedList":
        assert [block["c"][0][0] for block in lists] == list(range(4, 16))


def test_slide_pagination_separates_figure_caption():
    image = {
        "t": "Image",
        "c": [["", [], []], [{"t": "Str", "c": "description"}], ["figure.png", ""]],
    }
    caption = {"t": "Plain", "c": [{"t": "Str", "c": "Full caption retained"}]}
    figure = {
        "t": "Figure",
        "c": [
            ["fig:example", [], []],
            [None, [caption]],
            [{"t": "Plain", "c": [image]}],
        ],
    }
    output = rendering.paginate_slides({"meta": {}, "blocks": [figure]})
    assert output["blocks"][0]["c"][1][0] == "fig:example"
    rendered_image = output["blocks"][1]["c"][0]
    assert rendered_image["c"][1] == [{"t": "Str", "c": "Figure diagram"}]
    assert image["c"][1] == [{"t": "Str", "c": "description"}]
    assert output["blocks"][3] == caption


@pytest.mark.manuscript_render
def test_slide_pagination_splits_real_pandoc_table(tmp_path):
    import subprocess

    source = "| Term | Meaning |\n| --- | --- |\n" + "\n".join(
        f"| Key {i} | Definition {i} |" for i in range(11)
    )
    document = json.loads(
        subprocess.run(
            ["pandoc", "--from=markdown", "--to=json"],
            input=source,
            text=True,
            capture_output=True,
            check=True,
        ).stdout
    )
    original = document["blocks"][0]
    output = rendering.paginate_slides(document)
    tables = [block for block in output["blocks"] if block["t"] == "Table"]
    assert len(tables) == 4
    assert [row for table in tables for row in table["c"][4][0][3]] == original["c"][4][
        0
    ][3]
    assert all(table["c"][3] == original["c"][3] for table in tables)
    assert all(len(table["c"][4][0][3]) <= 3 for table in tables)
    oversized = json.loads(json.dumps(document))
    oversized["blocks"][0]["c"][4][0][3][0][1][0][4] = [
        {"t": "Plain", "c": [{"t": "Str", "c": "x" * 451}]}
    ]
    with pytest.raises(ValueError, match="row exceeds"):
        rendering.paginate_slides(oversized)
    original["c"][4][0][3][0][1][0][2] = 2
    with pytest.raises(ValueError, match="spanning"):
        rendering.paginate_slides(document)


@pytest.mark.parametrize(
    "block,message",
    [
        ({"t": "Para", "c": [{"t": "Str", "c": "x" * 451}]}, "indivisible"),
        ({"t": "CodeBlock", "c": [["", [], []], "x" * 81]}, "code block"),
        ({"t": "BlockQuote", "c": []}, "Unsupported"),
        (
            {"t": "Header", "c": [2, ["", [], []], [{"t": "Str", "c": "x" * 81}]]},
            "heading",
        ),
        ({"t": "Figure", "c": [["", [], []], [None, []], []]}, "single registered"),
    ],
)
def test_slide_pagination_refuses_unbounded_or_unsupported_content(block, message):
    with pytest.raises(ValueError, match=message):
        rendering.paginate_slides({"meta": {}, "blocks": [block]})


def test_slide_pagination_emits_reference_content_and_target():
    paragraph = {"t": "Para", "c": [{"t": "Str", "c": "Full bibliographic entry"}]}
    nested = {
        "t": "Div",
        "c": [
            ["refs", [], []],
            [{"t": "Div", "c": [["ref-source", [], []], [paragraph]]}],
        ],
    }
    output = rendering.paginate_slides({"meta": {}, "blocks": [nested]})
    assert output["blocks"][0]["c"][1][0] == "ref-source"
    assert output["blocks"][1] == paragraph


def test_slide_pagination_retains_empty_headings():
    headers = [
        {"t": "Header", "c": [2, [name, [], []], [{"t": "Str", "c": name}]]}
        for name in ("First", "Last")
    ]
    assert (
        rendering.paginate_slides({"meta": {}, "blocks": headers})["blocks"] == headers
    )


_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import manuscript_rendering as rendering  # noqa: E402


def test_destination_must_be_new_external_and_real(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    existing = tmp_path / "existing"
    existing.mkdir()
    (existing / "keep.txt").write_text("Preserve me")
    for target in (root / "output", existing, tmp_path / "missing" / "output"):
        with pytest.raises(ValueError):
            rendering.new_review_directory(root, target)
    alias = tmp_path / "alias"
    alias.symlink_to(existing, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        rendering.new_review_directory(root, alias / "output")
    assert (existing / "keep.txt").read_text() == "Preserve me"
    with pytest.raises(ValueError, match="outside"):
        rendering.new_review_directory(
            root, tmp_path / "outside" / ".." / "repo" / "review"
        )


@pytest.mark.parametrize(
    "node",
    [
        {"t": "Image", "c": [["", [], []], [], ["https://example.com/figure.png", ""]]},
        {"t": "CodeBlock", "c": [["", ["mermaid"], []], "graph LR"]},
        {
            "t": "RawBlock",
            "c": ["html", "<script>fetch('https://example.com')</script>"],
        },
    ],
)
def test_unsupported_figures_or_renderer_markup_never_fetch_silently(tmp_path, node):
    with pytest.raises(ValueError):
        rendering.rebase_links(node, tmp_path, "a" * 40)


def test_repository_evidence_links_bind_revision_and_fragments(tmp_path):
    (tmp_path / "pages").mkdir()
    path = tmp_path / "pages/A file.md"
    path.write_text("source")
    node = {
        "t": "Link",
        "c": [
            ["", [], []],
            [{"t": "Str", "c": "Source"}],
            ["../../pages/A%20file.md#section", ""],
        ],
    }
    rewritten = rendering.rebase_links(node, tmp_path, "a" * 40)
    assert (
        rewritten["c"][-1][0]
        == "https://github.com/docxology/docxology/blob/"
        + "a" * 40
        + "/pages/A%20file.md#section"
    )
    node["c"][-1][0] = "../../../private.txt"
    with pytest.raises(ValueError, match="escapes"):
        rendering.rebase_links(node, tmp_path, "a" * 40)


def test_missing_or_wrong_tool_versions_fail(monkeypatch, tmp_path):
    monkeypatch.setattr(rendering.shutil, "which", lambda name: None)
    with pytest.raises(ValueError, match="missing"):
        rendering.toolchain(tmp_path)
    monkeypatch.setattr(rendering.shutil, "which", lambda name: "/unused/tool")
    monkeypatch.setattr(rendering, "run", lambda *args, **kwargs: "pandoc 0.0.1\n")
    with pytest.raises(ValueError, match="version mismatch"):
        rendering.toolchain(tmp_path)


def test_failed_tool_preserves_existing_review_output(tmp_path):
    root = Path(__file__).resolve().parents[2]
    existing = tmp_path / "review"
    existing.mkdir()
    document = existing / rendering.OUTPUTS["pdf"]
    document.write_bytes(b"previous")
    with pytest.raises(ValueError, match="new review directory"):
        rendering.render_manuscript(root, existing)
    assert document.read_bytes() == b"previous"


@pytest.mark.parametrize(
    "failure", ["renderer", "source_mutation", "crlf_source", "staged_mutation", "production_mutation", "production_added", "production_removed"]
)
def test_failure_during_render_never_publishes_misbound_outputs(
    tmp_path, monkeypatch, failure
):
    import yaml

    root = tmp_path / "repo"
    folder = root / "docs/manuscript"
    folder.mkdir(parents=True)
    config = {
        "paper": {
            "title": "docxology",
            "subtitle": "Draft",
            "date": "2026-10-13",
            "version": "draft",
        },
        "publication": {"github_repository": "docxology/docxology"},
        "authors": [{"name": "Public Example"}],
        "metadata": {"language": "en", "license": "CC-BY-4.0"},
        "manuscript_dir": "docs/manuscript",
        "bibliography": {
            "references_path": "docs/manuscript/references.bib",
            "fail_on_missing": True,
            "fail_on_unused": False,
        },
        "render": {"toolchain": rendering.TOOLS, "formats": {"html": True}},
    }
    if failure == "staged_mutation":
        config["paper"]["cover"] = rendering.COVER
        config["render"].update(template=rendering.TEMPLATE, formats={"pdf": True})
    (folder / "config.yaml").write_text(yaml.safe_dump(config))
    (folder / "references.bib").write_text("@misc{example,title={A draft},year={2026}}")
    source = folder / "00_abstract.md"
    source.write_text("# Abstract {#sec:abstract}\n\nDraft [@example].\n")
    if failure == "crlf_source":
        source.write_bytes(source.read_bytes().replace(b"\n", b"\r\n"))
    (folder / "99_references.md").write_text("# References {#sec:references}\n")
    for relative in (
        "code/src/manuscript_rendering.py",
        "code/orchestrators/render_manuscript.py",
        "code/src/manuscript_template.py",
        "docs/manuscript/preamble.md",
    ):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Public renderer source\n")
    monkeypatch.setattr(rendering, "toolchain", lambda root: {})

    def runner(arguments, *, root, data=None):
        if arguments[0] == "git":
            return "a" * 40
        assert "--data-dir" in arguments
        if "--from=biblatex" in arguments:
            return '[{"id":"example"}]'
        if "--from=markdown" in arguments:
            return json.dumps({"meta": {}, "blocks": []})
        assert "--from=json" in arguments
        if "--to=markdown" in arguments:
            return "Prevalidated draft body"
        if failure == "renderer":
            raise ValueError("renderer failed")
        Path(arguments[arguments.index("--output") + 1]).write_text(
            '<html><div id="refs">Reference</div></html>'
        )
        dependency = root / "code/src/manuscript_template.py"
        if failure == "production_mutation":
            dependency.write_text("# Changed transitive source\n")
        elif failure == "production_added":
            (root / "code/src/new_policy.py").write_text("# New dependency\n")
        elif failure == "production_removed":
            dependency.unlink()
        if failure == "source_mutation":
            source.write_text(source.read_text() + "\nChanged during render.\n")
        return ""

    monkeypatch.setattr(rendering, "run", runner)

    def mutate_native(template_root, template_python, project, worker):
        body = project / "docs/manuscript/00_body.md"
        body.write_text(body.read_text() + "Changed during native render")
        return {}

    monkeypatch.setattr(rendering, "native_pdf", mutate_native)
    destination = tmp_path / "new-review"
    kwargs = (
        {"template_root": tmp_path, "template_python": tmp_path / "python"}
        if failure == "staged_mutation"
        else {}
    )
    if failure == "crlf_source":
        receipt = rendering.render_manuscript(root, destination, **kwargs)
        production = receipt["production_source"]
        assert production["files_sha256"]["code/src/manuscript_template.py"] == hashlib.sha256(
            (root / "code/src/manuscript_template.py").read_bytes()
        ).hexdigest()
        assert production["scope"] == ["code/src/**/*.py", "code/orchestrators/**/*.py"]
        assert production["kind"] == "working source content snapshot"
        assert (
            receipt["source_sha256"]["docs/manuscript/00_abstract.md"]
            == hashlib.sha256(source.read_bytes()).hexdigest()
        )
    else:
        with pytest.raises(ValueError, match="renderer failed|sources changed"):
            rendering.render_manuscript(root, destination, **kwargs)
        assert not destination.exists()
    assert not list(tmp_path.glob(".docxology-render-*"))


@pytest.mark.manuscript_render
def test_real_four_format_render_and_receipt(tmp_path):
    root = Path(__file__).resolve().parents[2]
    for name in ("DOCXOLOGY_TEMPLATE_ROOT", "DOCXOLOGY_TEMPLATE_PYTHON"):
        if not os.environ.get(name):
            pytest.fail(
                f"{name} is required for selected manuscript_render tests; see docs/manuscript/README.md"
            )
    receipt = rendering.render_manuscript(
        root,
        tmp_path / "review",
        template_root=Path(os.environ["DOCXOLOGY_TEMPLATE_ROOT"]),
        template_python=Path(os.environ["DOCXOLOGY_TEMPLATE_PYTHON"]),
    )
    assert {item["format"] for item in receipt["artifacts"].values()} == {
        "html",
        "pdf",
        "epub",
        "slides",
        "cover",
        "figure",
    }
    from docxology_tools.manuscript_validation import validate_manuscript

    assert receipt["bibliography_entries"] == validate_manuscript(root)["citation_count"]
    assert receipt["license"] == "CC-BY-4.0"
    assert receipt["human_visual_review"] == "pending"
    assert receipt["editorial_review"] == "pending"
    assert not receipt["publication_readiness_assessed"]
    assert str(tmp_path) not in str(receipt)
    assert receipt["slide_layout"] == {
        "producer": rendering.SLIDE_LAYOUT,
        "text_budget": rendering.SLIDE_TEXT_LIMIT,
        "prose_budget": rendering.SLIDE_PROSE_LIMIT,
        "line_width": rendering.SLIDE_LINE_WIDTH,
        "line_limit": rendering.SLIDE_LINE_LIMIT,
        "bullet_right_inset_emu": rendering.SLIDE_BULLET_RIGHT_INSET,
    }
    import zipfile
    import xml.etree.ElementTree as ET

    with zipfile.ZipFile(tmp_path / "review" / rendering.OUTPUTS["slides"]) as package:
        media = [name for name in package.namelist() if name.startswith("ppt/media/")]
        assert len(media) == len(rendering.FIGURES)
        padded_bodies = 0
        ns = {"p": "http://schemas.openxmlformats.org/presentationml/2006/main", "a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
        for name in package.namelist():
            if not (name.startswith("ppt/slides/slide") and name.endswith(".xml")):
                continue
            for shape in ET.fromstring(package.read(name)).findall(".//p:sp", ns):
                ph = shape.find(".//p:ph", ns)
                if ph is None or ph.get("idx") != "1":
                    continue
                if any((style := paragraph.find("a:pPr", ns)) is None or style.find("a:buNone", ns) is None for paragraph in shape.findall(".//a:p", ns)):
                    assert int(shape.find("p:txBody/a:bodyPr", ns).get("rIns")) >= rendering.SLIDE_BULLET_RIGHT_INSET
                    padded_bodies += 1
        assert padded_bodies > 0

        runs = [
            node.text or ""
            for name in package.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
            for node in ET.fromstring(package.read(name)).iter(
                "{http://schemas.openxmlformats.org/drawingml/2006/main}t"
            )
        ]
    assert (
        "docxology: daniel ari friedman public research and software index"
        in " ".join(runs).casefold()
    )


def test_exact_toolchain_and_crossref_build_are_required(monkeypatch, tmp_path):
    binary = tmp_path / "renderer"
    binary.write_bytes(b"synthetic renderer")
    monkeypatch.setattr(rendering.shutil, "which", lambda name: str(binary))
    banners = {
        "pandoc": "pandoc 3.12.1",
        "pandoc-crossref": "pandoc-crossref v0.3.26 built with Pandoc v3.12.1,",
        "xelatex": "XeTeX 3.141592653-2.6-0.999998 (TeX Live 2026)",
        "bibtex": "BibTeX 0.99e (TeX Live 2026)",
    }
    calls = iter(banners.values())
    monkeypatch.setattr(rendering, "run", lambda *args, **kwargs: next(calls))
    result = rendering.toolchain(tmp_path)
    assert {name: data["version"] for name, data in result.items()} == rendering.TOOLS
    assert all(
        data["binary_sha256"] == hashlib.sha256(binary.read_bytes()).hexdigest()
        for data in result.values()
    )
    for pandoc_version in ("3.10.1", "3.12.10"):
        banners["pandoc-crossref"] = (
            f"pandoc-crossref v0.3.26 built with Pandoc v{pandoc_version},"
        )
        calls = iter(banners.values())
        with pytest.raises(ValueError, match="pinned Pandoc build"):
            rendering.toolchain(tmp_path)
    banners["pandoc-crossref"] = "pandoc-crossref v0.3.260 built with Pandoc v3.12.1,"
    calls = iter(banners.values())
    with pytest.raises(ValueError, match="version mismatch"):
        rendering.toolchain(tmp_path)


def test_native_diagnostics_distinguish_errors_from_package_metadata():
    from docxology_tools.manuscript_template import native_diagnostics

    assert not native_diagnostics(
        "Package: infwarerr Providing info/warning/error messages\nThere were 0 error messages"
    )
    for text in (
        "LaTeX Warning: There were undefined references.",
        "Package natbib Warning: Citation `absent' undefined",
        "Warning--I didn't find a database entry for absent",
        "I couldn't open database file",
        "There were 2 error messages",
    ):
        assert native_diagnostics(text)


def test_native_pdf_requires_explicit_template_inputs(tmp_path):
    root = Path(__file__).resolve().parents[2]
    with pytest.raises(ValueError, match="explicit --template-root"):
        rendering.render_manuscript(root, tmp_path / "missing-template")
    assert not (tmp_path / "missing-template").exists()


def test_pinned_template_export_ignores_worktree_and_binds_source(
    tmp_path, monkeypatch
):
    from docxology_tools import manuscript_template as native
    import io
    import subprocess
    import tarfile

    archive_bytes = io.BytesIO()
    with tarfile.open(fileobj=archive_bytes, mode="w") as archive:
        for name, value in {
            "pyproject.toml": b'[project]\nversion = "4.0.2"\n',
            "uv.lock": b"locked\n",
            "infrastructure/renderer.py": b"committed\n",
        }.items():
            info = tarfile.TarInfo(name)
            info.size = len(value)
            archive.addfile(info, io.BytesIO(value))

    def runner(arguments, **kwargs):
        assert arguments[:4] == [
            "git",
            "archive",
            "--format=tar",
            native.TEMPLATE["revision"],
        ]
        return subprocess.CompletedProcess(
            arguments, 0, stdout=archive_bytes.getvalue()
        )

    monkeypatch.setattr(native.subprocess, "run", runner)
    repository = tmp_path / "mutable"
    repository.mkdir()
    (repository / "unrelated.txt").write_text("Do not touch")
    receipt = native.export_template(repository, tmp_path / "snapshot")
    assert (
        receipt["source_sha256"]["infrastructure/renderer.py"]
        == hashlib.sha256(b"committed\n").hexdigest()
    )
    assert not (tmp_path / "snapshot/unrelated.txt").exists()
    assert (repository / "unrelated.txt").read_text() == "Do not touch"


@pytest.mark.parametrize("member", ["../escape", "/absolute", "infrastructure/link"])
def test_template_export_rejects_escaping_paths_and_links(
    tmp_path, monkeypatch, member
):
    from docxology_tools import manuscript_template as native
    import io
    import subprocess
    import tarfile

    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode="w") as archive:
        info = tarfile.TarInfo(member)
        if member.endswith("link"):
            info.type = tarfile.SYMTYPE
            info.linkname = "/private"
        archive.addfile(info)
    monkeypatch.setattr(
        native.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args, 0, stdout=data.getvalue()
        ),
    )
    with pytest.raises(ValueError, match="Unsafe"):
        native.export_template(tmp_path, tmp_path / "export")
    assert not (tmp_path / "escape").exists()


def test_native_timeout_kills_own_process_group(tmp_path, monkeypatch):
    from docxology_tools import manuscript_template as native
    import subprocess

    monkeypatch.setattr(native, "export_template", lambda *args: {})
    killed = []
    monkeypatch.setattr(native.os, "killpg", lambda pid, sig: killed.append(pid))

    class HungWorker:
        pid = 12345
        calls = 0

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def communicate(self, **kwargs):
            self.calls += 1
            if self.calls == 1:
                raise subprocess.TimeoutExpired("worker", 180)
            return b"", None

    monkeypatch.setattr(
        native.subprocess, "Popen", lambda *args, **kwargs: HungWorker()
    )
    with pytest.raises(ValueError, match="timed out"):
        native.native_pdf(
            tmp_path, tmp_path / "python", tmp_path, tmp_path / "worker.py"
        )
    assert killed == [12345]


def test_unknown_cover_producer_fails_before_template_execution(tmp_path, monkeypatch):
    root = Path(__file__).resolve().parents[2]
    monkeypatch.setattr(rendering, "COVER", {"producer": "unreviewed"})
    with pytest.raises(ValueError, match="declared cover producer"):
        rendering.render_manuscript(
            root,
            tmp_path / "unknown-cover",
            template_root=tmp_path,
            template_python=tmp_path / "python",
        )
    assert not (tmp_path / "unknown-cover").exists()


def test_only_declared_diagram_targets_reach_rendered_images(tmp_path):
    from docxology_tools.manuscript_figures import SOURCE_TARGETS

    target = next(iter(SOURCE_TARGETS))
    node = {
        "t": "Image",
        "c": [["fig:diagram", [], []], [{"t": "Str", "c": "Diagram"}], [target, ""]],
    }
    mapped = rendering.rebase_links(
        node, tmp_path, "a" * 40, {target: "figures/diagram.png"}
    )
    assert mapped["c"][-1][0] == "figures/diagram.png"
    node["c"][-1][0] = "https://example.org/remote.png"
    with pytest.raises(ValueError, match="explicit offline"):
        rendering.rebase_links(
            node, tmp_path, "a" * 40, {target: "figures/diagram.png"}
        )


def _layout_prose(text):
    import re
    return {"t": "Para", "c": [
        {"t": "Space"} if token.isspace() else {"t": "Str", "c": token}
        for token in re.findall(r"\s+|\S+", text)
    ]}


def _layout_pages(document):
    pages = []
    for block in rendering.paginate_slides(document)["blocks"]:
        if block["t"] == "Header":
            pages.append([])
        else:
            pages[-1].append(block)
    return [page for page in pages if page]


@pytest.mark.parametrize("filename,needle", [
    ("01_introduction.md", "A scholarly profile"),
    ("02_system_context.md", "The public repository"),
    ("03_methods.md", "The checkout-local"),
    ("03_methods.md", "The shared [paper-resource"),
    ("03_methods.md", "timing and tracing workloads"),
    ("06_limitations_and_next_steps.md", "Capacity planning"),
])
def test_actual_manuscript_paragraphs_do_not_orphan_their_final_words(filename, needle):
    """These paragraphs produced the observed 1–5-word frozen LO slides."""
    import re
    root = Path(__file__).resolve().parents[2]
    source = (root / "docs/manuscript" / filename).read_text()
    paragraph = next(value for value in source.split("\n\n") if needle in value)
    # Isolate visible prose for this allocation regression. Rich inline identity
    # and resolved link/citation retention have separate AST/native regressions.
    paragraph = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", paragraph)
    paragraph = paragraph.replace("[@docxologyIndex]", "(Friedman 2026)").replace("`", "")
    paragraph = " ".join(paragraph.split())
    original = _layout_prose(paragraph)
    pages = _layout_pages({"meta": {}, "blocks": [original]})
    assert len(pages) == 1, filename
    assert pages[0] == [original]


def test_long_prose_prefers_complete_sentence_boundaries_and_retains_every_inline():
    sentences = [" ".join([word] * 24) + "." for word in ("Alpha", "Bravo", "Charlie", "Delta")]
    original = _layout_prose(" ".join(sentences))
    pages = _layout_pages({"meta": {}, "blocks": [original]})
    paragraphs = [block for page in pages for block in page]
    assert [inline for block in paragraphs for inline in block["c"]] == original["c"]
    assert all("".join(node.get("c", " ") for node in block["c"]).rstrip().endswith(".") for block in paragraphs)
    assert all(rendering._slide_text_size(block) >= 120 for block in paragraphs)


def test_long_single_sentence_balances_tiny_tail_without_discarding_words():
    original = _layout_prose(" ".join(["retained"] * 61) + ".")
    pages = _layout_pages({"meta": {}, "blocks": [original]})
    paragraphs = [block for page in pages for block in page]
    assert len(pages) >= 2
    assert [inline for block in paragraphs for inline in block["c"]] == original["c"]
    assert min(rendering._slide_text_size(block) for block in paragraphs) >= 120


def test_short_adjacent_paragraphs_pack_in_order_within_one_section():
    originals = [_layout_prose(f"Paragraph {index} retains its own complete authored sentence.") for index in range(6)]
    document = {"meta": {}, "blocks": [{"t": "Header", "c": [2, ["section", [], []], [{"t": "Str", "c": "Section"}]]}, *originals]}
    pages = _layout_pages(document)
    assert len(pages) < len(originals)
    assert any(len(page) > 1 for page in pages)
    assert [block for page in pages for block in page] == originals


def test_packing_keeps_section_boundaries_and_co_located_anchor_aliases():
    def header(identity):
        return {"t": "Header", "c": [2, [identity, [], []], [{"t": "Str", "c": identity}]]}
    first, second = _layout_prose("First complete paragraph."), _layout_prose("Second complete paragraph.")
    nested = {"t": "Div", "c": [["inner", [], []], [second]]}
    jumps = {"t": "Para", "c": [{"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "Jump"}], ["#inner", ""]]}]}
    output = rendering.paginate_slides({"meta": {}, "blocks": [header("one"), first, nested, header("two"), jumps]})
    assert [block["c"][1][0] for block in output["blocks"] if block["t"] == "Header"] == ["one", "two"]
    assert output["blocks"][1:3] == [first, second]
    assert output["blocks"][-1]["c"][0]["c"][-1][0] == "#one"
    assert jumps["c"][0]["c"][-1][0] == "#inner"


def test_explicit_line_breaks_prevent_false_compact_packing():
    originals = [{"t": "Para", "c": [{"t": "Str", "c": "line"}, {"t": "LineBreak"}] * 6} for _ in range(2)]
    pages = _layout_pages({"meta": {}, "blocks": originals})
    assert len(pages) >= 2
    assert [inline for page in pages for block in page for inline in block["c"]] == [inline for block in originals for inline in block["c"]]


def test_nested_list_packing_accounts_for_every_indentation_level():
    body = _layout_prose(" ".join(["word"] * 37) + ".")
    nested = {"t": "BulletList", "c": [[{"t": "BulletList", "c": [[body]]}]]}
    originals = [nested, nested]
    pages = _layout_pages({"meta": {}, "blocks": originals})
    assert len(pages) == 2
    assert [block for page in pages for block in page] == originals


def test_bullet_body_inset_preserves_text_links_media_and_nonbullet_geometry(tmp_path):
    import zipfile
    from xml.etree import ElementTree as ET
    source = b'''<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr><p:txBody><a:bodyPr/><a:p><a:pPr lvl="0"/><a:r><a:t>Static navigation and progressive search. Source: nav-toggle.js</a:t></a:r></a:p></p:txBody></p:sp><p:sp><p:nvSpPr><p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr><p:txBody><a:bodyPr rIns="91440"/><a:p><a:pPr><a:buNone/></a:pPr><a:r><a:t>Ordinary prose remains unchanged.</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>'''
    path = tmp_path / "review.pptx"
    untouched = {"ppt/slides/_rels/slide1.xml.rels": b"exact link relationship bytes", "ppt/media/figure.png": b"exact image bytes"}
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("ppt/slides/slide1.xml", source)
        for name, raw in untouched.items():
            package.writestr(name, raw)
    assert rendering.pad_slide_bullet_bodies(path) == 1
    with zipfile.ZipFile(path) as package:
        actual = package.read("ppt/slides/slide1.xml")
        for name, raw in untouched.items():
            assert package.read(name) == raw
    assert actual == source.replace(b"<a:bodyPr/>", b'<a:bodyPr rIns="457200"/>', 1)
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    assert [node.text for node in ET.fromstring(actual).findall(".//a:t", ns)] == [node.text for node in ET.fromstring(source).findall(".//a:t", ns)]
    once = path.read_bytes()
    assert rendering.pad_slide_bullet_bodies(path) == 0
    assert path.read_bytes() == once


def test_bullet_inset_refuses_malformed_package_without_replacing_original(tmp_path):
    import zipfile
    path = tmp_path / "bad.pptx"
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("ppt/slides/slide1.xml", b"<broken")
    before = path.read_bytes()
    with pytest.raises(ValueError):
        rendering.pad_slide_bullet_bodies(path)
    assert path.read_bytes() == before


@pytest.mark.parametrize("attribute", [b"rIns='91440'", b"rIns = '91440'", b'rIns = "91440"'])
def test_bullet_inset_preserves_valid_xml_quote_and_spacing_forms(tmp_path, attribute):
    import zipfile
    from xml.etree import ElementTree as ET
    source = b'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr><p:txBody><a:bodyPr '+attribute+b'/><a:p><a:pPr/><a:r><a:t>Reviewed bullet.</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>'
    path = tmp_path / "quoted.pptx"
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("ppt/slides/slide1.xml", source)
    assert rendering.pad_slide_bullet_bodies(path) == 1
    with zipfile.ZipFile(path) as package:
        actual = package.read("ppt/slides/slide1.xml")
    assert actual == source.replace(attribute, attribute.replace(b"91440", b"457200"))
    assert ET.fromstring(actual) is not None


def _actual_linked_scholar_bullet():
    import re
    source = (Path(__file__).resolve().parents[2] / "docs/manuscript/S01_source_surface.md").read_text()
    text = next(line[2:] for line in source.splitlines() if line.startswith("- **Scholar technical readiness."))
    inlines = []
    for token in re.split(r"(\*\*[^*]+\*\*|\[[^]]+\]\([^)]+\))", text):
        if token.startswith("**"):
            inlines.append({"t": "Strong", "c": _layout_prose(token[2:-2])["c"]})
        elif match := re.fullmatch(r"\[([^]]+)\]\(([^)]+)\)", token):
            inlines.append({"t": "Link", "c": [["", [], []], _layout_prose(match[1])["c"], [match[2], ""]]})
        else:
            inlines.extend(_layout_prose(token)["c"])
    return {"t": "Para", "c": inlines}


@pytest.mark.parametrize("kind", ["BulletList", "OrderedList"])
def test_actual_linked_bullet_keeps_complete_sentence_continuations_in_one_item(kind):
    original = _actual_linked_scholar_bullet()
    attributes = [7, {"t": "UpperRoman"}, {"t": "TwoParens"}]
    content = [[original]] if kind == "BulletList" else [attributes, [[original]]]
    source = {"t": kind, "c": content}
    pages = _layout_pages({"meta": {}, "blocks": [source]})
    assert len(pages) == 1
    assert len(pages[0]) == 1
    result = pages[0][0]
    items = result["c"] if kind == "BulletList" else result["c"][1]
    assert len(items) == 1
    paragraphs = items[0]
    assert len(paragraphs) == 3
    assert [inline for part in paragraphs for inline in part["c"]] == original["c"]
    assert rendering._slide_visible_text(paragraphs[0]).startswith("Scholar technical readiness. Source:")
    assert rendering._slide_visible_text(paragraphs[1]).startswith("Verification:")
    assert rendering._slide_visible_text(paragraphs[2]) == "Actual indexing requires an independent observation."
    assert rendering._slide_text_fits([result])
    if kind == "OrderedList":
        assert result["c"][0] == attributes
    assert original == _actual_linked_scholar_bullet()


def test_linked_sentence_paragraph_gaps_are_budgeted_before_list_packing():
    original = _layout_prose(" ".join([" ".join(["Retained"] * 20) + "."] * 5))
    original["c"][:0] = [{"t": "Link", "c": [["", [], []], [{"t": "Str", "c": "Source"}], ["https://example.org/source", ""]]}, {"t": "Space"}]
    pages = _layout_pages({"meta": {}, "blocks": [{"t": "BulletList", "c": [[original]]}]})
    assert len(pages) >= 2
    paragraphs = [child for page in pages for block in page for item in block["c"] for child in item]
    assert len(paragraphs) == 5
    assert [inline for child in paragraphs for inline in child["c"]] == original["c"]
    assert all(rendering._slide_text_fits(page) for page in pages)


@pytest.mark.parametrize("attribute", [b'lvl="1"', b"lvl='1'", b"lvl = '1'"])
def test_bullet_continuations_inherit_active_level_without_changing_text_or_indents(tmp_path, attribute):
    import zipfile
    from xml.etree import ElementTree as ET
    source = b'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr><p:txBody><a:bodyPr rIns="457200"/><a:p><a:pPr lvl="0"/><a:r><a:t>First sentence. </a:t></a:r></a:p><a:p><a:pPr lvl="1" indent="0" marL="342900"><a:buNone/></a:pPr><a:r><a:t xml:space="preserve">Verification sentence. </a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>'
    source = source.replace(b'lvl="1"', attribute)
    path = tmp_path / "continuation.pptx"
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("ppt/slides/slide1.xml", source)
        package.writestr("ppt/slides/_rels/slide1.xml.rels", b"unchanged relationships")
    assert rendering.pad_slide_bullet_bodies(path) == 1
    with zipfile.ZipFile(path) as package:
        actual = package.read("ppt/slides/slide1.xml")
        assert package.read("ppt/slides/_rels/slide1.xml.rels") == b"unchanged relationships"
    assert actual == source.replace(attribute, attribute.replace(b"1", b"0"))
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    assert "".join(node.text or "" for node in ET.fromstring(actual).findall(".//a:t", ns)) == "First sentence. Verification sentence. "
    once = path.read_bytes()
    assert rendering.pad_slide_bullet_bodies(path) == 0
    assert path.read_bytes() == once


def test_viewer_word_overlap_catches_same_origin_words_and_tolerates_small_kerning():
    # A worked geometry version of observed slide125: several complete words
    # were drawn at the same origin, although its enclosing block stayed inside.
    words = [(70, 176, 120, 200, "Actual"), (70, 176, 140, 200, "indexing")]
    result = rendering.slide_word_overlaps(words)
    assert [(row["left"], row["right"], row["words"]) for row in result] == [(0, 1, ["Actual", "indexing"])]
    assert result[0]["fraction"] == 1.0
    assert rendering.slide_word_overlaps([(0, 0, 10, 20, "normal"), (9, 0, 20, 20, "kerning")]) == []


@pytest.mark.parametrize("words", [
    [(0, 0, float("nan"), 20, "invalid")],
    [(0, 0, float("inf"), 20, "invalid")],
    [(10, 0, 0, 20, "reversed")],
    [(0, 0, 0, 20, "empty")],
    [(0, 0, 10, 20, "")],
    [(0, 0, 10, 20, " ")],
    [(0, 0, 10**1000, 20, "overflow")],
    [(0, 0, 10, 20)],
    [(0, 0, 10, 20, "bounded")] * 1001,
])
def test_viewer_word_overlap_refuses_invalid_or_unbounded_geometry(words):
    with pytest.raises(ValueError):
        rendering.slide_word_overlaps(words)


@pytest.mark.parametrize("mutation", ["non_numeric", "outside_level", "alias_prefix"])
def test_malformed_bullet_paragraph_refuses_before_replacing_package(tmp_path, mutation):
    import zipfile
    source = b'<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:q="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:nvSpPr><p:nvPr><p:ph idx="1"/></p:nvPr></p:nvSpPr><p:txBody><a:bodyPr rIns="457200"/><a:p><a:pPr lvl="0"/><a:r><a:t>Retained bullet.</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>'
    if mutation == "non_numeric":
        source = source.replace(b'lvl="0"', b'lvl="invalid"')
    elif mutation == "outside_level":
        source = source.replace(b'lvl="0"', b'lvl="9"')
    else:
        source = source.replace(b'<a:pPr ', b'<q:pPr ')
    path = tmp_path / "unsupported.pptx"
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("ppt/slides/slide1.xml", source)
    original = path.read_bytes()
    with pytest.raises(ValueError):
        rendering.pad_slide_bullet_bodies(path)
    assert path.read_bytes() == original
