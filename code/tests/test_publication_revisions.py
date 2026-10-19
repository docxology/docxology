"""Historical publication notices are explicit, pinned and safely rendered."""

import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from docxology_tools.publication_revisions import (
    revision_notice,
    revision_notice_html,
    revision_notice_markdown,
)  # noqa: E402


def metadata():
    return {
        "source_revision_review": {
            "repository": "docxology/ActiveACO",
            "commit": "a" * 40,
            "document": "PAPER_REVISION.md",
            "reviewed_at": "2026-10-19",
            "summary": "Corrected <scoring>; historical denominator is unavailable.",
        }
    }


def test_pinned_source_and_archive_boundary_are_visible():
    data = metadata()
    assert "/blob/" + "a" * 40 + "/PAPER_REVISION.md" in revision_notice(data)["url"]
    for rendered in (revision_notice_html(data), revision_notice_markdown(data)):
        assert "&lt;scoring&gt;" in rendered
        assert "historical archive" in rendered
        assert "new publication or DOI" in rendered
    assert revision_notice_html({}) == ""


@pytest.mark.parametrize(
    "key,value",
    [
        ("commit", "main"),
        ("repository", "private/repo"),
        ("document", "../secret.md"),
        ("reviewed_at", "2026-02-31"),
        ("summary", ""),
        ("commit", None),
    ],
)
def test_invalid_correction_identity_fails_closed(key, value):
    data = metadata()
    data["source_revision_review"][key] = value
    with pytest.raises(ValueError):
        revision_notice_html(data)
