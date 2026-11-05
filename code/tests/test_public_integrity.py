"""Regression tests for public CV/source privacy and URL safety."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

REPO_ROOT = Path(__file__).resolve().parents[2]

from docxology_tools.public_integrity import (  # noqa: E402
    INSECURE_HTTP_URL_RE,
    LOCAL_PATH_RE,
    redact_local_paths,
    scan_public_files,
)


def test_current_public_cv_surfaces_have_no_privacy_violations():
    assert scan_public_files(REPO_ROOT) == []


def test_local_path_detector_catches_user_home_paths():
    assert LOCAL_PATH_RE.search("source: /Users/example/Downloads/CV.pdf")
    assert LOCAL_PATH_RE.search("source: /home/example/private.json")


def test_public_integrity_checks_can_scan_a_narrow_fixture(tmp_path):
    fixture = tmp_path / "fixture.json"
    fixture.write_text('{"url":"javascript:alert(1)"}', encoding="utf-8")
    errors = scan_public_files(tmp_path, ("fixture.json",))
    assert "unsafe URL scheme" in errors[0]


def test_windows_home_paths_are_detected_without_matching_json_newline_escapes():
    import json

    assert LOCAL_PATH_RE.search(r"C:\Users\example\private.txt")
    assert LOCAL_PATH_RE.search(json.dumps({"path": r"C:\Users\example\private.txt"}))
    assert not LOCAL_PATH_RE.search(json.dumps({"note": "A:\nB:\n"}))
    assert not LOCAL_PATH_RE.search("https://example.org/Users/example/public.txt")


def test_csp_data_source_is_not_treated_as_an_unsafe_link_scheme(tmp_path):
    fixture = tmp_path / "fixture.html"
    fixture.write_text('<meta content="img-src self data: https:">', encoding="utf-8")
    assert scan_public_files(tmp_path, ("fixture.html",)) == []


def test_insecure_http_detector_flags_plain_http_but_accepts_https(tmp_path):
    assert INSECURE_HTTP_URL_RE.search('"url": "http://example.org/page"')
    assert not INSECURE_HTTP_URL_RE.search('"url": "https://example.org/page"')
    fixture = tmp_path / "fixture.json"
    fixture.write_text('{"url":"http://example.org/page"}', encoding="utf-8")
    errors = scan_public_files(tmp_path, ("fixture.json",))
    assert any("insecure http://" in error for error in errors)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("source:/Users/example/private.txt", "source:[local path redacted]"),
        ("label:/home/example/private.txt", "label:[local path redacted]"),
        ("label:/Volumes/Example/private.txt", "label:[local path redacted]"),
        ("file:/Users/example/private.txt", "file:[local path redacted]"),
        ("file:///Users/example/private.txt", "file:[local path redacted]"),
        ("label:~/private.txt", "label:[local path redacted]"),
        (r"label:C:\Users\example\private.txt", "label:[local path redacted]"),
    ],
)
def test_colon_prefixed_local_paths_are_detected_and_redacted(text, expected):
    assert redact_local_paths(text) == expected
    assert redact_local_paths(expected) == expected


@pytest.mark.parametrize(
    "url",
    [
        "https://example.org/Users/example/public.txt",
        "http://example.org/Volumes/Example/public.txt",
        "https://example.org/docs:/Users/example/public.txt",
        "https://example.org/?next=label:/Volumes/Example/public.txt#file:/home/example/public.txt",
        "HTTPS://example.org/file:/Users/example/public.txt",
        "https://[2001:db8::1]/Users/example/public.txt",
        "https://example.org/(docs):/Users/example/public.txt",
    ],
)
def test_public_http_urls_are_preserved_as_complete_tokens(url):
    assert redact_local_paths(url) == url
    body = f"Public: {url}\nPrivate source:/Users/example/private.txt"
    assert redact_local_paths(body) == (
        f"Public: {url}\nPrivate source:[local path redacted]"
    )


def test_public_integrity_uses_url_aware_detection_for_colon_paths(tmp_path):
    fixture = tmp_path / "fixture.txt"
    fixture.write_text(
        "Source: https://example.org/docs:/Users/example/public.txt", encoding="utf-8"
    )
    assert scan_public_files(tmp_path, ("fixture.txt",)) == []
    fixture.write_text("Source label:/Volumes/Example/private.txt", encoding="utf-8")
    assert scan_public_files(tmp_path, ("fixture.txt",)) == [
        "fixture.txt: local filesystem path detected"
    ]


def test_json_escaped_newline_does_not_extend_a_public_url_exemption():
    import json

    text = json.dumps({
        "note": "https://example.org/public\nsource:/Users/example/private.txt"
    })
    assert "/Users/example/private.txt" not in redact_local_paths(text)
    assert "https://example.org/public" in redact_local_paths(text)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        (
            "[public](https://example.org/page)source:/Users/example/private.txt",
            "[public](https://example.org/page)source:[local path redacted]",
        ),
        (
            "[public](https://example.org/(docs):/Users/example/public.txt)"
            "source:/Users/example/private.txt",
            "[public](https://example.org/(docs):/Users/example/public.txt)"
            "source:[local path redacted]",
        ),
        (
            "[public](https://example.org/(outer(inner)):/Users/example/public.txt)"
            "file:/Volumes/Example/private.txt",
            "[public](https://example.org/(outer(inner)):/Users/example/public.txt)"
            "file:[local path redacted]",
        ),
        (
            "(https://[2001:db8::1]/Users/example/public.txt)"
            "source:/Users/example/private.txt",
            "(https://[2001:db8::1]/Users/example/public.txt)"
            "source:[local path redacted]",
        ),
        (
            "[public](\nhttps://example.org/page)source:/Users/example/private.txt",
            "[public](\nhttps://example.org/page)source:[local path redacted]",
        ),
        (
            "[first](https://example.org/page)source:/Users/example/private.txt"
            "[second](https://example.org/(docs):/Users/example/public.txt)",
            "[first](https://example.org/page)source:[local path redacted]"
            "[second](https://example.org/(docs):/Users/example/public.txt)",
        ),
        (
            "[https://example.org/[docs]:/Users/example/public.txt]"
            "label:/Users/example/private.txt",
            "[https://example.org/[docs]:/Users/example/public.txt]"
            "label:[local path redacted]",
        ),
    ],
)
def test_markdown_url_boundary_cannot_hide_a_following_local_path(
    tmp_path, text, expected
):
    assert redact_local_paths(text) == expected
    assert redact_local_paths(expected) == expected
    fixture = tmp_path / "fixture.txt"
    fixture.write_text(text, encoding="utf-8")
    assert scan_public_files(tmp_path, ("fixture.txt",)) == [
        "fixture.txt: local filesystem path detected"
    ]
    fixture.write_text(expected, encoding="utf-8")
    assert scan_public_files(tmp_path, ("fixture.txt",)) == []
