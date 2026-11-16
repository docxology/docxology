"""Unicode and paper-validation regressions for the metadata audit."""
import importlib.util
import json
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "audit_metadata", Path(__file__).resolve().parents[1] / "audit_metadata.py"
)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


@pytest.mark.parametrize("low,high", [
    (0x1F600, 0x1F64F), (0x1F300, 0x1F5FF), (0x1F680, 0x1F6FF),
    (0x1F1E0, 0x1F1FF), (0x2702, 0x27B0), (0x24C2, 0x24C2),
    (0x1F170, 0x1F1DF), (0x1F200, 0x1F251),
])
def test_unicode_boundaries(low, high):
    assert audit.contains_emoji("domain " + chr(low))
    assert audit.contains_emoji(chr(high) + " domain")
    # Adjacent ranges deliberately touch at the flag boundary.
    for point in (low - 1, high + 1):
        expected = point in {0x1F1DF, 0x1F1E0, 0x1F1FF, 0x1F200, 0x1F5FF, 0x1F600}
        assert audit.contains_emoji(chr(point)) is expected


@pytest.mark.parametrize("text", ["", "Active Inference", "Entomology", "\ufffd", "\ud800", "\U0010ffff"])
def test_plain_text_and_nonemoji_scalars(text):
    assert not audit.contains_emoji(text)
    assert not audit.has_emoji(text)


@pytest.mark.parametrize("value", [None, 12, "2026-02-30T00:00:00Z", "2026-01-01", ""])
def test_invalid_iso(value):
    assert not audit.is_valid_iso(value)


def test_paper_audit_rejects_emoji_domain(tmp_path, monkeypatch):
    monkeypatch.setattr(audit, "PAPERS_DIR", str(tmp_path))
    folder = tmp_path / "paper"
    folder.mkdir()
    metadata = {
        "domain": "Entomology", "type": "Paper",
        "methods": [{"name": "Observation"}, {"name": "Analysis"}],
        "key_findings": ["A finding"], "checked_at": "2026-11-16T00:00:00Z",
    }
    (folder / "metadata.json").write_text(json.dumps(metadata))
    assert audit.check_paper("paper", {"paper"}) == ("paper", {}, True)
    metadata["domain"] += "\U0001f600"
    (folder / "metadata.json").write_text(json.dumps(metadata))
    assert "domain" in audit.check_paper("paper", {"paper"})[1]
    assert audit.check_paper("missing", set())[1] == {"exists": "metadata.json not found"}
