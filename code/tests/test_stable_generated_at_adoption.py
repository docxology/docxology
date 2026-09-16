"""Tests for stable_generated_at adoption across the timestamped generators.

Each generator that writes a wall-clock ``generated_at`` must reuse the
on-disk timestamp when its payload body is unchanged (byte-stable output
across two runs), take a fresh timestamp when the body changed, and fall
back to a fresh timestamp when the existing file is missing or unreadable.
The seam under test is the generator's stamping helper, not a subprocess
run: JSON adopters go through ``docxology_tools.report_paths.stable_generated_at``
and HTML adopters go through the equivalent on-disk stamp reuse
(``docxology_tools.build_stamp.reuse_on_disk_stamp``), matching the
build_search_index / build_resume / build_404_page reference pattern.
build_video_pages was already adopted upstream
(``stable_generated_output_timestamp`` + ``reuse_on_disk_stamp``) and is
covered by test_build_video_pages.py.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_orchestrator(name: str):
    spec = importlib.util.spec_from_file_location(
        name, REPO_ROOT / "code" / "orchestrators" / f"{name}.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


current_counts = _load_orchestrator("build_current_counts")
coverage_exceptions = _load_orchestrator("build_coverage_exceptions")
reconciliation = _load_orchestrator("build_reconciliation_report")
ledger = _load_orchestrator("build_reproducibility_ledger")
evidence_page = _load_orchestrator("build_evidence_page")
exports_page = _load_orchestrator("build_exports_page")

from docxology_tools.build_stamp import reuse_on_disk_stamp  # noqa: E402

OLD_TS = "2026-07-17T00:00:00Z"
FRESH_TS = "2026-07-18T12:34:56Z"

ALT_STAMP = (
    '<p class="build-stamp"><a href="https://github.com/docxology/docxology/commit/'
    'fffffffffff">build fffffffffff 2099-01-01</a></p>'
)


def _body() -> dict:
    """A representative generated-at payload body (small, body-agnostic)."""
    return {"schema_version": "1.0", "count": 3, "items": ["a", "b", "c"]}


def _changed_body() -> dict:
    return {"schema_version": "1.0", "count": 4, "items": ["a", "b", "c", "d"]}


# --- JSON adopters: the wrapper reuses the on-disk generated_at ---

GLOBAL_PATH_ADOPTERS = [
    pytest.param(current_counts, "JSON_PATH", "preserve_timestamp_when_unchanged", id="current_counts"),
    pytest.param(coverage_exceptions, "OUT", "preserve_timestamp_when_unchanged", id="coverage_exceptions"),
]

PARAM_PATH_ADOPTERS = [
    pytest.param(reconciliation, "stabilize_payload", id="reconciliation"),
    pytest.param(ledger, "_preserve_generated_at", id="reproducibility_ledger"),
]


@pytest.mark.parametrize(("module", "attr", "seam_name"), GLOBAL_PATH_ADOPTERS)
def test_json_unchanged_body_is_byte_identical_across_two_runs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, module, attr: str, seam_name: str
) -> None:
    out = tmp_path / "payload.json"
    monkeypatch.setattr(module, attr, out)
    out.write_text(
        json.dumps({"generated_at": OLD_TS, **_body()}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    seam = getattr(module, seam_name)

    first = seam({"generated_at": FRESH_TS, **_body()})
    second = seam({"generated_at": FRESH_TS, **_body()})

    assert first["generated_at"] == OLD_TS, "unchanged body must reuse the existing timestamp"
    assert json.dumps(first, indent=2, ensure_ascii=False) == json.dumps(
        second, indent=2, ensure_ascii=False
    ), "two runs over an unchanged body must be byte-identical"


@pytest.mark.parametrize(("module", "seam_name"), PARAM_PATH_ADOPTERS)
def test_json_unchanged_body_is_byte_identical_across_two_runs_param(
    tmp_path: Path, module, seam_name: str
) -> None:
    out = tmp_path / "payload.json"
    seam = getattr(module, seam_name)
    out.write_text(
        json.dumps({"generated_at": OLD_TS, **_body()}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    first = seam({"generated_at": FRESH_TS, **_body()}, json_out=out)
    second = seam({"generated_at": FRESH_TS, **_body()}, json_out=out)

    assert first["generated_at"] == OLD_TS, "unchanged body must reuse the existing timestamp"
    assert json.dumps(first, indent=2, ensure_ascii=False) == json.dumps(
        second, indent=2, ensure_ascii=False
    ), "two runs over an unchanged body must be byte-identical"


@pytest.mark.parametrize(("module", "attr", "seam_name"), GLOBAL_PATH_ADOPTERS)
def test_json_changed_body_takes_fresh_timestamp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, module, attr: str, seam_name: str
) -> None:
    out = tmp_path / "payload.json"
    monkeypatch.setattr(module, attr, out)
    out.write_text(
        json.dumps({"generated_at": OLD_TS, **_body()}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    changed = getattr(module, seam_name)({"generated_at": FRESH_TS, **_changed_body()})

    assert changed["generated_at"] == FRESH_TS, "a changed body must not inherit the stale timestamp"


@pytest.mark.parametrize(("module", "seam_name"), PARAM_PATH_ADOPTERS)
def test_json_changed_body_takes_fresh_timestamp_param(
    tmp_path: Path, module, seam_name: str
) -> None:
    out = tmp_path / "payload.json"
    changed = getattr(module, seam_name)(
        {"generated_at": FRESH_TS, **_changed_body()}, json_out=out
    )

    assert changed["generated_at"] == FRESH_TS, "a changed body must not inherit the stale timestamp"


@pytest.mark.parametrize(("module", "attr", "seam_name"), GLOBAL_PATH_ADOPTERS)
@pytest.mark.parametrize("corrupt", [False, True], ids=["missing", "corrupt"])
def test_json_missing_or_corrupt_existing_takes_fresh_timestamp(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, module, attr: str, seam_name: str, corrupt: bool
) -> None:
    out = tmp_path / "payload.json"
    monkeypatch.setattr(module, attr, out)
    if corrupt:
        out.write_text("{not json", encoding="utf-8")

    payload = getattr(module, seam_name)({"generated_at": FRESH_TS, **_body()})

    assert payload["generated_at"] == FRESH_TS, (
        "a missing or unreadable existing file must yield a fresh timestamp"
    )


@pytest.mark.parametrize(("module", "seam_name"), PARAM_PATH_ADOPTERS)
@pytest.mark.parametrize("corrupt", [False, True], ids=["missing", "corrupt"])
def test_json_missing_or_corrupt_existing_takes_fresh_timestamp_param(
    tmp_path: Path, module, seam_name: str, corrupt: bool
) -> None:
    out = tmp_path / "payload.json"
    if corrupt:
        out.write_text("{not json", encoding="utf-8")

    payload = getattr(module, seam_name)({"generated_at": FRESH_TS, **_body()}, json_out=out)

    assert payload["generated_at"] == FRESH_TS, (
        "a missing or unreadable existing file must yield a fresh timestamp"
    )


# --- HTML adopters: the on-disk footer build stamp is the page's timestamp ---


def _render_with_alt_stamp(module, render, *args) -> str:
    """Render a page as if HEAD had moved (different stamp, same body)."""
    original = module.footer_build_stamp_html
    module.footer_build_stamp_html = lambda: ALT_STAMP
    try:
        return render(*args)
    finally:
        module.footer_build_stamp_html = original


def test_evidence_html_unchanged_body_keeps_existing_stamp() -> None:
    claims = evidence_page.load_claims()
    on_disk = evidence_page.render_html(claims)
    candidate = _render_with_alt_stamp(evidence_page, evidence_page.render_html, claims)

    assert reuse_on_disk_stamp(candidate, on_disk) == on_disk, (
        "an unchanged body must keep the on-disk stamp (byte-identical) rather than re-stamping"
    )


def test_evidence_html_changed_body_is_not_masked_by_stamp_reuse() -> None:
    claims = evidence_page.load_claims()
    on_disk = evidence_page.render_html(claims)
    tampered = on_disk + "<!-- drift -->\n"
    candidate = _render_with_alt_stamp(evidence_page, evidence_page.render_html, claims)

    assert reuse_on_disk_stamp(candidate, tampered) != tampered, (
        "a changed body must be visible to --check even after stamp reuse"
    )


@pytest.mark.parametrize("corrupt", [False, True], ids=["missing", "corrupt"])
def test_evidence_html_missing_or_stampless_existing_re_stamps(corrupt: bool) -> None:
    claims = evidence_page.load_claims()
    candidate = _render_with_alt_stamp(evidence_page, evidence_page.render_html, claims)
    existing = "not a stamped page" if corrupt else None

    assert reuse_on_disk_stamp(candidate, existing) == candidate, (
        "a missing or stampless existing page must fall back to the freshly stamped render"
    )


def test_exports_html_unchanged_body_keeps_existing_stamp() -> None:
    on_disk = exports_page.render()
    candidate = _render_with_alt_stamp(exports_page, exports_page.render)

    assert reuse_on_disk_stamp(candidate, on_disk) == on_disk, (
        "an unchanged body must keep the on-disk stamp (byte-identical) rather than re-stamping"
    )


def test_exports_html_changed_body_is_not_masked_by_stamp_reuse() -> None:
    on_disk = exports_page.render()
    tampered = on_disk + "<!-- drift -->\n"
    candidate = _render_with_alt_stamp(exports_page, exports_page.render)

    assert reuse_on_disk_stamp(candidate, tampered) != tampered, (
        "a changed body must be visible to --check even after stamp reuse"
    )


@pytest.mark.parametrize("corrupt", [False, True], ids=["missing", "corrupt"])
def test_exports_html_missing_or_stampless_existing_re_stamps(corrupt: bool) -> None:
    candidate = _render_with_alt_stamp(exports_page, exports_page.render)
    existing = "not a stamped page" if corrupt else None

    assert reuse_on_disk_stamp(candidate, existing) == candidate, (
        "a missing or stampless existing page must fall back to the freshly stamped render"
    )
