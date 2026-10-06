"""Real-file regression coverage for the Scholar observation recorder.

The recorder is the only writer of ``data/scholar-snapshot.json`` and
``data/scholar-verification-receipt.json``.  These tests run the real script as
a subprocess against a minimal checkout under ``tmp_path`` (the script, the
validator module, and the package ``__init__`` bootstrap), seeded with the
byte-exact pair that was recorded for the 2026-10-02 observation, and assert
the bytes it writes and the bytes it refuses to touch.  The seed is frozen
here, not read from ``data/``, so the cases stay meaningful after the live pair
has moved on; one case still replays the live pair to catch drift between the
tool and the curated history.  Nothing is mocked.  The single exception is the
rollback group at the end of the file: a write that succeeds and then fails
cannot be staged portably from outside the process (no root, no ``chflags``),
so those cases call ``main`` in-process on a ``tmp_path`` pair and make
``os.replace`` fail on a chosen call; the real temp-file, restore and
validation code still runs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

# docxology_tools owns the canonical bootstrap; this locate makes the package importable.
_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))
import docxology_tools  # noqa: E402, F401  (canonical bootstrap: code/src + code/orchestrators onto sys.path)

import record_scholar_observation as recorder  # noqa: E402

from docxology_tools.scholar_verification import (  # noqa: E402
    canonical_json_bytes,
    current_history_note,
    default_observation_source,
    observation_timing_errors,
    parse_verified_at,
    format_verified_at,
    reusable_receipt_verified_at,
    superseded_note,
    supersede_history,
    validate_observation,
    validate_scholar_snapshot_receipt,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
RECORDER_SOURCE = REPO_ROOT / "code" / "orchestrators" / "record_scholar_observation.py"
SYNC_SOURCE = REPO_ROOT / "code" / "orchestrators" / "sync_scholar_metrics.py"
VALIDATOR_SOURCE = REPO_ROOT / "code" / "src" / "scholar_verification.py"
PACKAGE_SOURCE = REPO_ROOT / "code" / "src" / "docxology_tools" / "__init__.py"

# The pair as recorded for the 2026-10-02 observation (JSON text, ASCII-escaped).
_SEED_SNAPSHOT_JSON = r"""{
  "metric": "google_scholar",
  "profile_id": "DXjPFtYAAAAJ",
  "profile_url": "https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en",
  "secondary_profile_id": "Y2bMf3MAAAAJ",
  "secondary_profile_note": "A second Google Scholar profile ID (Y2bMf3MAAAAJ) is linked from the ORCID record. DXjPFtYAAAAJ is the canonical/primary profile used for all public metrics; Y2bMf3MAAAAJ is secondary and should be consolidated or disambiguated to avoid citation-graph fragmentation.",
  "citations": 823,
  "h_index": 14,
  "i10_index": 17,
  "since_2021": {
    "citations": 594,
    "h_index": 14,
    "i10_index": 15
  },
  "as_of": "2026-10-02",
  "method": "Direct Chrome browser observation of the canonical profile on 2026-10-02 in an authenticated Google session (signed-in account control visible). All-time: 823 citations, h-index 14, i10-index 17; Since-2021: 594 / 14 / 15. No anonymous or search-engine cached result was used.",
  "policy": "This file is the single source of truth for Google Scholar metrics. Update ONLY from a direct (non-cached, non-anonymous-stale) Scholar fetch. On update, record the new value, a new as_of date, and the method here, and append the prior value to history. Public anonymous/cached Scholar views may differ; never publish a citation number above the most recent direct-fetch value recorded here. All hand-maintained surfaces are regenerated from this file via code/orchestrators/sync_scholar_metrics.py, and the agent claims ledger derives from it via code/orchestrators/export_agent_data.py.",
  "history": [
    {
      "as_of": "2026-04",
      "citations": 812,
      "h_index": 15,
      "note": "manual sync (SUPERSEDED \u2014 exceeded the live primary source; corrected 2026-05-16)"
    },
    {
      "as_of": "2026-05-12",
      "citations": 758,
      "h_index": 15,
      "note": "maintenance-log audit fetch (AGENTS.md 2026-05-12 row)"
    },
    {
      "as_of": "2026-05-16",
      "citations": 764,
      "h_index": 15,
      "i10_index": 17,
      "note": "independent dual direct-fetch (superseded 2026-06-09)"
    },
    {
      "as_of": "2026-06-09",
      "citations": 777,
      "h_index": 15,
      "i10_index": 17,
      "note": "direct logged-in browser-session fetch (superseded 2026-08-26)"
    },
    {
      "as_of": "2026-08-26",
      "citations": 815,
      "h_index": 14,
      "i10_index": 16,
      "note": "direct authenticated Chrome browser-session fetch (superseded 2026-10-02)"
    },
    {
      "as_of": "2026-10-02",
      "citations": 823,
      "h_index": 14,
      "i10_index": 17,
      "note": "Direct authenticated Chrome browser observation \u2014 current source of truth."
    }
  ]
}"""
_SEED_RECEIPT_JSON = r"""{
  "schema_version": "1.0",
  "receipt_type": "google_scholar_direct_authenticated",
  "profile_id": "DXjPFtYAAAAJ",
  "direct": true,
  "authenticated": true,
  "verified_at": "2026-10-02T14:38:54Z",
  "snapshot_path": "data/scholar-snapshot.json",
  "snapshot_sha256": "d9c4b848ad04238eb731f05748bbb88e473518ffe87a422526cfd9b11651b00d",
  "snapshot_as_of": "2026-10-02",
  "metrics": {
    "citations": 823,
    "h_index": 14,
    "i10_index": 17,
    "since_2021": {
      "citations": 594,
      "h_index": 14,
      "i10_index": 15
    }
  },
  "source": "Direct authenticated browser observation of https://scholar.google.com/citations?user=DXjPFtYAAAAJ&hl=en",
  "method": "Direct Chrome browser observation of the canonical profile on 2026-10-02 in an authenticated Google session (signed-in account control visible). All-time: 823 citations, h-index 14, i10-index 17; Since-2021: 594 / 14 / 15. No anonymous or search-engine cached result was used."
}"""
SEED_SNAPSHOT_SHA256 = "d9c4b848ad04238eb731f05748bbb88e473518ffe87a422526cfd9b11651b00d"

SEED_SNAPSHOT_BYTES = canonical_json_bytes(json.loads(_SEED_SNAPSHOT_JSON))
SEED_RECEIPT_BYTES = canonical_json_bytes(json.loads(_SEED_RECEIPT_JSON))

ATTEST = "--attest-direct-authenticated"
VERIFIED_AT = "2026-10-05T00:30:00Z"
# Any run on or after 2026-10-05 is more than one UTC day past this as_of, so a
# clock-defaulted verified_at is refused for it while an explicit one is not.
LATE_AS_OF = "2026-10-03"
LATE_VERIFIED_AT = "2026-10-03T12:00:00Z"
UNDECODABLE = b"\xff\xfe\x00garbage"
EM_DASH = "—"
EXPECTED_METHOD = (
    "Direct authenticated observation of the canonical profile on 2026-10-05. "
    "All-time: 824 citations, h-index 14, i10-index 17; Since-2021: 595 / 14 / 15. "
    "No anonymous or search-engine cached result was used."
)
RECEIPT_KEY_ORDER = [
    "schema_version",
    "receipt_type",
    "profile_id",
    "direct",
    "authenticated",
    "verified_at",
    "snapshot_path",
    "snapshot_sha256",
    "snapshot_as_of",
    "metrics",
    "source",
    "method",
]


@dataclass(frozen=True)
class Checkout:
    """A minimal runnable checkout: scripts, validator, bootstrap, and the data pair."""

    root: Path
    script: Path
    sync_script: Path
    snapshot: Path
    receipt: Path

    def run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.script), *args],
            cwd=self.root,
            text=True,
            capture_output=True,
        )

    def sync_check(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(self.sync_script), "--check"],
            cwd=self.root,
            text=True,
            capture_output=True,
        )

    def state(self) -> tuple[bytes, bytes | None]:
        receipt = self.receipt.read_bytes() if self.receipt.exists() else None
        return self.snapshot.read_bytes(), receipt

    def data_files(self) -> list[str]:
        return sorted(path.name for path in self.snapshot.parent.iterdir())


def _checkout(
    root: Path,
    *,
    snapshot_bytes: bytes = SEED_SNAPSHOT_BYTES,
    receipt_bytes: bytes = SEED_RECEIPT_BYTES,
) -> Checkout:
    script = root / "code" / "orchestrators" / "record_scholar_observation.py"
    sync_script = root / "code" / "orchestrators" / "sync_scholar_metrics.py"
    validator = root / "code" / "src" / "scholar_verification.py"
    package = root / "code" / "src" / "docxology_tools" / "__init__.py"
    for target in (script, validator, package):
        target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(RECORDER_SOURCE, script)
    shutil.copy2(SYNC_SOURCE, sync_script)
    shutil.copy2(VALIDATOR_SOURCE, validator)
    shutil.copy2(PACKAGE_SOURCE, package)
    snapshot = root / "data" / "scholar-snapshot.json"
    receipt = root / "data" / "scholar-verification-receipt.json"
    snapshot.parent.mkdir(parents=True, exist_ok=True)
    snapshot.write_bytes(snapshot_bytes)
    receipt.write_bytes(receipt_bytes)
    return Checkout(root, script, sync_script, snapshot, receipt)


def _observation_args(**overrides: object) -> list[str]:
    values: dict[str, object] = {
        "as_of": "2026-10-05",
        "citations": 824,
        "h_index": 14,
        "i10_index": 17,
        "since_2021_citations": 595,
        "since_2021_h_index": 14,
        "since_2021_i10_index": 15,
    }
    values.update(overrides)
    arguments: list[str] = []
    for key, value in values.items():
        arguments += ["--" + key.replace("_", "-"), str(value)]
    return arguments


def _record_args(*extra: str, **overrides: object) -> list[str]:
    return [*_observation_args(**overrides), ATTEST, *extra]


def _expected_snapshot() -> dict:
    """Re-derive the recorded snapshot independently of the recorder's helpers."""
    expected = json.loads(SEED_SNAPSHOT_BYTES.decode("utf-8"))
    expected.update(
        citations=824, h_index=14, i10_index=17, as_of="2026-10-05", method=EXPECTED_METHOD
    )
    expected["since_2021"] = {"citations": 595, "h_index": 14, "i10_index": 15}
    expected["history"][-1]["note"] = (
        "Direct authenticated Chrome browser observation (superseded 2026-10-05)"
    )
    expected["history"].append(
        {
            "as_of": "2026-10-05",
            "citations": 824,
            "h_index": 14,
            "i10_index": 17,
            "note": f"Direct authenticated observation {EM_DASH} current source of truth.",
        }
    )
    return expected


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def test_seed_is_the_recorded_pre_observation_pair(tmp_path: Path):
    checkout = _checkout(tmp_path)

    assert _sha256(checkout.snapshot.read_bytes()) == SEED_SNAPSHOT_SHA256
    assert validate_scholar_snapshot_receipt(tmp_path) == []
    assert checkout.sync_check().returncode == 0


def test_records_an_observation_and_binds_the_receipt(tmp_path: Path):
    checkout = _checkout(tmp_path)

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT))

    assert result.returncode == 0, result.stderr
    snapshot_bytes, receipt_bytes = checkout.state()
    assert snapshot_bytes == (
        json.dumps(_expected_snapshot(), indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    snapshot = json.loads(snapshot_bytes)
    seed = json.loads(SEED_SNAPSHOT_BYTES)
    # Only the observation moved: key order, policy, profile and secondary fields stay curated.
    assert list(snapshot) == list(seed)
    for untouched in ("metric", "profile_id", "profile_url", "secondary_profile_id", "secondary_profile_note", "policy"):
        assert snapshot[untouched] == seed[untouched]
    assert snapshot["history"][:-2] == seed["history"][:-1]
    assert snapshot["history"][-2]["note"].endswith("(superseded 2026-10-05)")
    assert all("since_2021" not in entry for entry in snapshot["history"])

    receipt = json.loads(receipt_bytes)
    assert list(receipt) == RECEIPT_KEY_ORDER
    assert receipt["direct"] is True and receipt["authenticated"] is True
    assert receipt["verified_at"] == VERIFIED_AT
    assert receipt["snapshot_sha256"] == _sha256(snapshot_bytes)
    assert receipt["snapshot_as_of"] == "2026-10-05"
    assert receipt["metrics"] == {
        "citations": 824,
        "h_index": 14,
        "i10_index": 17,
        "since_2021": {"citations": 595, "h_index": 14, "i10_index": 15},
    }
    assert receipt["method"] == snapshot["method"] == EXPECTED_METHOD
    assert receipt["source"] == "Direct authenticated observation of " + snapshot["profile_url"]
    assert "browser" not in receipt["source"].lower() and "browser" not in receipt["method"].lower()
    assert receipt_bytes == (json.dumps(receipt, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    assert validate_scholar_snapshot_receipt(tmp_path) == []
    assert checkout.sync_check().returncode == 0
    assert checkout.data_files() == ["scholar-snapshot.json", "scholar-verification-receipt.json"]
    for command in (
        "sync_scholar_metrics.py",
        "regenerate_all.py --validate",
        "settle.py --tier full",
    ):
        assert command in result.stdout


def test_default_verified_at_is_a_timezone_qualified_now(tmp_path: Path):
    checkout = _checkout(tmp_path)
    before = datetime.now(timezone.utc).replace(microsecond=0)

    # The clock default is only accepted within a day of as_of, so observe "today".
    result = checkout.run(*_record_args(as_of=before.date().isoformat()))

    after = datetime.now(timezone.utc)
    assert result.returncode == 0, result.stderr
    stamp = json.loads(checkout.receipt.read_text(encoding="utf-8"))["verified_at"]
    assert stamp.endswith("Z")
    assert before <= parse_verified_at(stamp) <= after
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_non_utc_verified_at_is_normalised_to_utc(tmp_path: Path):
    checkout = _checkout(tmp_path)

    result = checkout.run(*_record_args("--verified-at", "2026-10-04T17:30:00-07:00"))

    assert result.returncode == 0, result.stderr
    assert json.loads(checkout.receipt.read_text(encoding="utf-8"))["verified_at"] == "2026-10-05T00:30:00Z"


@pytest.mark.parametrize(
    ("overrides", "extra", "attest", "returncode", "message"),
    [
        pytest.param({"as_of": "2026-10-02"}, [], True, 1, "strictly later", id="same-day-as-of"),
        pytest.param({"as_of": "2026-09-01"}, [], True, 1, "strictly later", id="older-as-of"),
        pytest.param({"as_of": "2999-01-01"}, [], True, 1, "in the future", id="future-as-of"),
        pytest.param({"as_of": "2026-13-45"}, [], True, 2, "calendar date", id="impossible-date"),
        pytest.param({"as_of": "20261005"}, [], True, 2, "YYYY-MM-DD", id="compact-date"),
        pytest.param({}, ["--verified-at", "2026-10-05T10:00:00"], True, 2, "timezone-qualified", id="naive-verified-at"),
        pytest.param({}, ["--verified-at", "2026-10-05"], True, 2, "timezone-qualified", id="bare-date-verified-at"),
        pytest.param({}, ["--verified-at", "2999-01-01T00:00:00Z"], True, 1, "in the future", id="future-verified-at"),
        pytest.param({}, ["--verified-at", "2026-10-01T00:00:00Z"], True, 1, "precedes as_of", id="verified-at-before-as-of"),
        pytest.param({"citations": -1}, [], True, 2, "non-negative integer", id="negative-metric"),
        pytest.param({"h_index": "true"}, [], True, 2, "non-negative integer", id="boolean-metric"),
        pytest.param({"i10_index": "1.5"}, [], True, 2, "non-negative integer", id="fractional-metric"),
        pytest.param({"since_2021_citations": "+7"}, [], True, 2, "non-negative integer", id="signed-metric"),
        pytest.param({}, [], False, 2, "--attest-direct-authenticated", id="missing-attestation"),
        pytest.param({"as_of": LATE_AS_OF}, [], True, 1, "--verified-at", id="defaulted-verified-at-too-late"),
        pytest.param(
            {
                "citations": 595,
                "h_index": 14,
                "i10_index": 15,
                "since_2021_citations": 824,
                "since_2021_h_index": 14,
                "since_2021_i10_index": 17,
            },
            [],
            True,
            1,
            "transposed",
            id="transposed-columns",
        ),
        pytest.param({"since_2021_citations": 825}, [], True, 1, "exceeds the all-time citations", id="since-citations-above-all-time"),
        pytest.param({"since_2021_h_index": 15}, [], True, 1, "exceeds the all-time h_index", id="since-h-above-all-time"),
        pytest.param({"since_2021_i10_index": 18}, [], True, 1, "exceeds the all-time i10_index", id="since-i10-above-all-time"),
        pytest.param(
            {"citations": 10, "h_index": 14, "i10_index": 5, "since_2021_citations": 9, "since_2021_h_index": 3, "since_2021_i10_index": 0},
            [],
            True,
            1,
            "all-time h_index (14) exceeds all-time citations (10)",
            id="all-time-h-above-citations",
        ),
        pytest.param(
            {"citations": 10, "h_index": 3, "i10_index": 17, "since_2021_citations": 9, "since_2021_h_index": 3, "since_2021_i10_index": 0},
            [],
            True,
            1,
            "all-time i10_index (17) exceeds all-time citations (10)",
            id="all-time-i10-above-citations",
        ),
        pytest.param(
            {"since_2021_citations": 5, "since_2021_h_index": 6, "since_2021_i10_index": 2},
            [],
            True,
            1,
            "since_2021 h_index (6) exceeds since_2021 citations (5)",
            id="since-h-above-since-citations",
        ),
        pytest.param(
            {"since_2021_citations": 5, "since_2021_h_index": 2, "since_2021_i10_index": 6},
            [],
            True,
            1,
            "since_2021 i10_index (6) exceeds since_2021 citations (5)",
            id="since-i10-above-since-citations",
        ),
    ],
)
def test_refusals_leave_both_files_byte_identical(
    tmp_path: Path, overrides: dict, extra: list[str], attest: bool, returncode: int, message: str
):
    checkout = _checkout(tmp_path)
    before = checkout.state()
    arguments = [*_observation_args(**overrides), *([ATTEST] if attest else []), *extra]

    result = checkout.run(*arguments)

    assert result.returncode == returncode, result.stderr
    assert message in result.stderr
    assert checkout.state() == before
    assert checkout.data_files() == ["scholar-snapshot.json", "scholar-verification-receipt.json"]


def test_refuses_when_the_last_history_entry_disagrees_with_the_snapshot(tmp_path: Path):
    drifted = json.loads(SEED_SNAPSHOT_BYTES)
    drifted["history"][-1]["citations"] = 800
    snapshot_bytes = canonical_json_bytes(drifted)
    receipt = json.loads(SEED_RECEIPT_BYTES)
    receipt["snapshot_sha256"] = _sha256(snapshot_bytes)
    checkout = _checkout(tmp_path, snapshot_bytes=snapshot_bytes, receipt_bytes=canonical_json_bytes(receipt))
    before = checkout.state()

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT))

    assert result.returncode == 1
    assert "history" in result.stderr and "citations" in result.stderr
    assert checkout.state() == before


def test_refuses_a_snapshot_without_history(tmp_path: Path):
    bare = json.loads(SEED_SNAPSHOT_BYTES)
    del bare["history"]
    snapshot_bytes = canonical_json_bytes(bare)
    receipt = json.loads(SEED_RECEIPT_BYTES)
    receipt["snapshot_sha256"] = _sha256(snapshot_bytes)
    checkout = _checkout(tmp_path, snapshot_bytes=snapshot_bytes, receipt_bytes=canonical_json_bytes(receipt))
    before = checkout.state()

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT))

    assert result.returncode == 1
    assert "history" in result.stderr
    assert checkout.state() == before


def test_refuses_a_symlinked_snapshot(tmp_path: Path):
    checkout = _checkout(tmp_path)
    elsewhere = tmp_path / "elsewhere.json"
    elsewhere.write_bytes(SEED_SNAPSHOT_BYTES)
    checkout.snapshot.unlink()
    checkout.snapshot.symlink_to(elsewhere)
    receipt_before = checkout.receipt.read_bytes()

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT))

    assert result.returncode == 1
    assert "symlink" in result.stderr
    assert elsewhere.read_bytes() == SEED_SNAPSHOT_BYTES
    assert checkout.snapshot.is_symlink()
    assert checkout.receipt.read_bytes() == receipt_before


def test_dry_run_writes_nothing_and_predicts_the_real_sha(tmp_path: Path):
    checkout = _checkout(tmp_path)
    before = checkout.state()

    dry = checkout.run(*_record_args("--verified-at", VERIFIED_AT, "--dry-run"))

    assert dry.returncode == 0, dry.stderr
    assert checkout.state() == before
    assert checkout.data_files() == ["scholar-snapshot.json", "scholar-verification-receipt.json"]
    assert "dry run: nothing written" in dry.stdout
    assert "823 -> 824 (+1)" in dry.stdout
    assert "594 -> 595 (+1)" in dry.stdout
    assert "(superseded 2026-10-05)" in dry.stdout
    predicted = next(
        line.split()[-1] for line in dry.stdout.splitlines() if line.strip().startswith("snapshot_sha256")
    )

    real = checkout.run(*_record_args("--verified-at", VERIFIED_AT))

    assert real.returncode == 0, real.stderr
    assert _sha256(checkout.snapshot.read_bytes()) == predicted
    assert json.loads(checkout.receipt.read_text(encoding="utf-8"))["snapshot_sha256"] == predicted


def test_check_tracks_whether_the_exact_observation_is_recorded(tmp_path: Path):
    checkout = _checkout(tmp_path)
    arguments = [*_observation_args(), "--check"]
    before = checkout.state()

    assert checkout.run(*arguments).returncode == 1
    assert checkout.state() == before

    assert checkout.run(*_record_args("--verified-at", VERIFIED_AT)).returncode == 0
    recorded = checkout.state()
    assert checkout.run(*arguments).returncode == 0
    # A different observation is not "recorded", even on the same day.
    assert checkout.run(*_observation_args(citations=825), "--check").returncode == 1
    assert checkout.state() == recorded

    receipt = json.loads(checkout.receipt.read_text(encoding="utf-8"))
    receipt["snapshot_sha256"] = "0" * 64
    checkout.receipt.write_bytes(canonical_json_bytes(receipt))
    tampered = checkout.run(*arguments)
    assert tampered.returncode == 1
    assert "snapshot_sha256 does not match" in tampered.stdout


def test_rerunning_a_recorded_observation_is_a_no_op(tmp_path: Path):
    checkout = _checkout(tmp_path)
    assert checkout.run(*_record_args("--verified-at", VERIFIED_AT)).returncode == 0
    recorded = checkout.state()

    again = checkout.run(*_record_args("--verified-at", "2026-10-05T01:00:00Z"))

    assert again.returncode == 0, again.stderr
    assert "already recorded" in again.stdout
    assert checkout.state() == recorded
    assert len(json.loads(recorded[0])["history"]) == len(json.loads(SEED_SNAPSHOT_BYTES)["history"]) + 1


@pytest.mark.parametrize("damage", ["deleted", "wrong-sha", "undecodable"])
def test_a_lost_or_stale_receipt_is_regenerated_without_touching_the_snapshot(tmp_path: Path, damage: str):
    checkout = _checkout(tmp_path)
    assert checkout.run(*_record_args("--verified-at", VERIFIED_AT)).returncode == 0
    snapshot_bytes = checkout.snapshot.read_bytes()
    history_length = len(json.loads(snapshot_bytes)["history"])
    if damage == "deleted":
        checkout.receipt.unlink()
    elif damage == "undecodable":
        checkout.receipt.write_bytes(UNDECODABLE)
    else:
        receipt = json.loads(checkout.receipt.read_text(encoding="utf-8"))
        receipt["snapshot_sha256"] = "0" * 64
        checkout.receipt.write_bytes(canonical_json_bytes(receipt))
    assert recorder._validate_pair(tmp_path) != []

    result = checkout.run(*_record_args("--verified-at", "2026-10-05T13:00:00Z"))

    assert result.returncode == 0, result.stderr
    assert "receipt-only recovery" in result.stdout
    assert checkout.snapshot.read_bytes() == snapshot_bytes
    assert len(json.loads(snapshot_bytes)["history"]) == history_length
    receipt = json.loads(checkout.receipt.read_text(encoding="utf-8"))
    assert receipt["verified_at"] == "2026-10-05T13:00:00Z"
    assert receipt["snapshot_sha256"] == _sha256(snapshot_bytes)
    assert list(receipt) == RECEIPT_KEY_ORDER
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_receipt_only_recovery_refuses_a_method_that_would_diverge(tmp_path: Path):
    checkout = _checkout(tmp_path)
    assert checkout.run(*_record_args("--verified-at", VERIFIED_AT)).returncode == 0
    checkout.receipt.unlink()

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT, "--method", "something else"))

    assert result.returncode == 1
    assert "--method" in result.stderr
    assert not checkout.receipt.exists()


def test_a_decrease_is_recorded_with_a_warning(tmp_path: Path):
    checkout = _checkout(tmp_path)

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT, citations=800))

    assert result.returncode == 0, result.stderr
    assert "citations decreased (823 -> 800)" in result.stderr
    assert json.loads(checkout.snapshot.read_text(encoding="utf-8"))["citations"] == 800
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_operator_supplied_method_source_and_history_note(tmp_path: Path):
    checkout = _checkout(tmp_path)

    result = checkout.run(
        *_record_args(
            "--verified-at",
            VERIFIED_AT,
            "--method",
            "Operator-written method.",
            "--source",
            "Operator-written source.",
            "--history-note",
            "Operator observation.",
        )
    )

    assert result.returncode == 0, result.stderr
    snapshot = json.loads(checkout.snapshot.read_text(encoding="utf-8"))
    receipt = json.loads(checkout.receipt.read_text(encoding="utf-8"))
    assert snapshot["method"] == receipt["method"] == "Operator-written method."
    assert receipt["source"] == "Operator-written source."
    assert snapshot["history"][-1]["note"] == f"Operator observation {EM_DASH} current source of truth."
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_successor_observation_applies_to_the_live_pair(tmp_path: Path):
    """Replay the tool over the curated pair so it cannot drift from the live history shape."""
    live_snapshot = (REPO_ROOT / "data" / "scholar-snapshot.json").read_bytes()
    live_receipt = (REPO_ROOT / "data" / "scholar-verification-receipt.json").read_bytes()
    live = json.loads(live_snapshot)
    successor = date.fromisoformat(live["as_of"]) + timedelta(days=1)
    if successor > datetime.now(timezone.utc).date() + timedelta(days=1):
        pytest.skip("the live snapshot is already as recent as the recorder allows")
    checkout = _checkout(tmp_path, snapshot_bytes=live_snapshot, receipt_bytes=live_receipt)
    assert validate_scholar_snapshot_receipt(tmp_path) == []

    result = checkout.run(
        *_record_args(
            "--verified-at",
            format_verified_at(datetime.now(timezone.utc)),
            as_of=successor.isoformat(),
            citations=live["citations"] + 1,
            h_index=live["h_index"],
            i10_index=live["i10_index"],
            since_2021_citations=live["since_2021"]["citations"] + 1,
            since_2021_h_index=live["since_2021"]["h_index"],
            since_2021_i10_index=live["since_2021"]["i10_index"],
        )
    )

    assert result.returncode == 0, result.stderr
    updated = json.loads(checkout.snapshot.read_text(encoding="utf-8"))
    assert list(updated) == list(live)
    assert len(updated["history"]) == len(live["history"]) + 1
    assert updated["history"][-2]["note"].endswith(f"(superseded {successor.isoformat()})")
    assert updated["history"][-1]["as_of"] == successor.isoformat()
    assert validate_scholar_snapshot_receipt(tmp_path) == []
    assert checkout.sync_check().returncode == 0


@pytest.mark.skipif(os.geteuid() == 0, reason="root ignores directory permissions")
def test_an_unwritable_data_directory_is_refused_and_leaves_both_files_alone(tmp_path: Path):
    checkout = _checkout(tmp_path)
    before = checkout.state()
    data_dir = checkout.snapshot.parent
    data_dir.chmod(0o555)
    try:
        result = checkout.run(*_record_args("--verified-at", VERIFIED_AT))
    finally:
        data_dir.chmod(0o755)

    assert result.returncode == 1
    assert "write failed" in result.stderr
    assert "CRITICAL" not in result.stderr
    assert checkout.state() == before
    assert checkout.data_files() == ["scholar-snapshot.json", "scholar-verification-receipt.json"]


def test_atomic_write_replaces_bytes_keeps_the_mode_and_leaves_no_temp_files(tmp_path: Path):
    target = tmp_path / "data" / "file.json"
    target.parent.mkdir()
    target.write_bytes(b"old")
    target.chmod(0o640)

    recorder._atomic_write(target, b"new\r\n\xe2\x80\x94")

    assert target.read_bytes() == b"new\r\n\xe2\x80\x94"
    assert target.stat().st_mode & 0o777 == 0o640
    assert sorted(path.name for path in target.parent.iterdir()) == ["file.json"]
    fresh = tmp_path / "data" / "fresh.json"
    recorder._atomic_write(fresh, b"{}")
    assert fresh.stat().st_mode & 0o777 == 0o644


def test_atomic_write_refuses_a_symlink_target(tmp_path: Path):
    real = tmp_path / "real.json"
    real.write_bytes(b"keep")
    link = tmp_path / "link.json"
    link.symlink_to(real)

    with pytest.raises(OSError, match="symlink"):
        recorder._atomic_write(link, b"overwrite")

    assert real.read_bytes() == b"keep"
    assert sorted(path.name for path in tmp_path.iterdir()) == ["link.json", "real.json"]


def test_restore_returns_original_bytes_and_removes_files_that_did_not_exist(tmp_path: Path):
    changed = tmp_path / "changed.json"
    changed.write_bytes(b"after")
    created = tmp_path / "created.json"
    created.write_bytes(b"new file")

    failures = recorder._restore({changed: b"before", created: None})

    assert failures == []
    assert changed.read_bytes() == b"before"
    assert not created.exists()


def test_canonical_json_bytes_keep_order_and_literal_unicode():
    assert canonical_json_bytes({"b": EM_DASH, "a": [1]}) == (
        b'{\n  "b": "\xe2\x80\x94",\n  "a": [\n    1\n  ]\n}\n'
    )


@pytest.mark.parametrize(
    ("note", "expected"),
    [
        (f"Direct authenticated Chrome browser observation {EM_DASH} current source of truth.", "Direct authenticated Chrome browser observation (superseded 2026-10-05)"),
        (f"manual sync {EM_DASH} CURRENT source of truth", "manual sync (superseded 2026-10-05)"),
        ("plain note.", "plain note (superseded 2026-10-05)"),
        ("already done (superseded 2026-01-01)", "already done (superseded 2026-01-01)"),
    ],
)
def test_superseded_note_matches_the_established_history_pattern(note: str, expected: str):
    assert superseded_note(note, "2026-10-05") == expected


def test_current_history_note_never_doubles_the_suffix():
    default = f"Direct authenticated observation {EM_DASH} current source of truth."
    assert current_history_note() == default
    assert current_history_note("Operator note.") == f"Operator note {EM_DASH} current source of truth."
    assert current_history_note(f"Operator note {EM_DASH} current source of truth.") == (
        f"Operator note {EM_DASH} current source of truth."
    )


def test_supersede_history_refuses_drift_and_leaves_its_input_alone():
    snapshot = json.loads(SEED_SNAPSHOT_BYTES)
    history = snapshot["history"]
    before = json.dumps(history)

    updated = supersede_history(history, snapshot, "2026-10-05")

    assert json.dumps(history) == before
    assert updated[-1]["note"].endswith("(superseded 2026-10-05)")
    assert updated[:-1] == history[:-1]
    for bad in (None, [], ["not-an-entry"]):
        with pytest.raises(ValueError, match="history"):
            supersede_history(bad, snapshot, "2026-10-05")
    drifted = json.loads(before)
    drifted[-1]["h_index"] = 99
    with pytest.raises(ValueError, match="h_index"):
        supersede_history(drifted, snapshot, "2026-10-05")


def test_verified_at_parsing_accepts_z_and_offsets_and_refuses_naive_values():
    utc = parse_verified_at("2026-10-05T12:00:00Z")
    assert utc == datetime(2026, 10, 5, 12, 0, tzinfo=timezone.utc)
    assert parse_verified_at("2026-10-05T14:00:00+02:00") == utc
    assert format_verified_at(parse_verified_at("2026-10-05T05:00:00-07:00")) == "2026-10-05T12:00:00Z"
    for naive in ("2026-10-05T12:00:00", "2026-10-05", "not a time", ""):
        with pytest.raises(ValueError):
            parse_verified_at(naive)


def test_observation_timing_errors_bound_both_dates_against_the_supplied_clock():
    now = datetime(2026, 10, 5, 22, 0, tzinfo=timezone.utc)
    ok = datetime(2026, 10, 5, 21, 0, tzinfo=timezone.utc)

    assert observation_timing_errors(date(2026, 10, 5), ok, now, current_as_of=date(2026, 10, 2)) == []
    # An evening observation west of UTC is already "tomorrow" in UTC.
    assert observation_timing_errors(date(2026, 10, 6), ok, now) == []
    assert observation_timing_errors(date(2026, 10, 7), ok, now) != []
    assert observation_timing_errors(date(2026, 10, 5), ok, now, current_as_of=date(2026, 10, 5)) != []
    assert observation_timing_errors(date(2026, 10, 5), now + timedelta(minutes=6), now) != []
    assert observation_timing_errors(date(2026, 10, 5), now + timedelta(minutes=4), now) == []
    assert observation_timing_errors(date(2026, 10, 5), datetime(2026, 10, 3, 23, 0, tzinfo=timezone.utc), now) != []
    assert observation_timing_errors(date(2026, 10, 5), datetime(2026, 10, 4, 0, 0, tzinfo=timezone.utc), now) == []


# ---------------------------------------------------------------------------
# Attestation is required only for the mode that writes
# ---------------------------------------------------------------------------


def test_read_only_modes_need_no_attestation_and_a_write_still_does(tmp_path: Path):
    checkout = _checkout(tmp_path)
    before = checkout.state()

    dry = checkout.run(*_observation_args(), "--verified-at", VERIFIED_AT, "--dry-run")

    assert dry.returncode == 0, dry.stderr
    assert "dry run: nothing written" in dry.stdout
    assert "a real run requires --attest-direct-authenticated" in dry.stdout
    assert checkout.run(*_observation_args(), "--check").returncode == 1
    assert checkout.state() == before

    unattested_write = checkout.run(*_observation_args(), "--verified-at", VERIFIED_AT)
    assert unattested_write.returncode == 2
    assert "required to write" in unattested_write.stderr
    assert checkout.state() == before

    assert checkout.run(*_record_args("--verified-at", VERIFIED_AT)).returncode == 0
    assert checkout.run(*_observation_args(), "--check").returncode == 0


def test_the_help_text_scopes_the_attestation_and_the_interface_detail_rule(tmp_path: Path):
    checkout = _checkout(tmp_path)

    help_text = " ".join(checkout.run("--help").stdout.split())

    assert "required to write (not for --dry-run or --check)" in help_text
    assert help_text.count("only if you attest them") == 2
    assert "Direct authenticated observation of <profile URL>" in help_text


def test_default_source_names_the_profile_without_asserting_an_interface():
    snapshot = json.loads(SEED_SNAPSHOT_BYTES)

    source = default_observation_source(snapshot)

    assert source == "Direct authenticated observation of " + snapshot["profile_url"]
    assert "browser" not in source.lower()
    with pytest.raises(ValueError, match="profile_url"):
        default_observation_source({})


# ---------------------------------------------------------------------------
# The six typed numbers must be mutually consistent
# ---------------------------------------------------------------------------


def _observation(**overrides: int) -> dict:
    values = {
        "citations": 824,
        "h_index": 14,
        "i10_index": 17,
        "since_2021": {"citations": 595, "h_index": 14, "i10_index": 15},
        "as_of": "2026-10-05",
    }
    since = overrides.pop("since_2021", None)
    values.update(overrides)
    if since is not None:
        values["since_2021"] = since
    return values


def test_validate_observation_accepts_consistent_and_boundary_values():
    assert validate_observation(_observation()) == []
    # Equal values are possible (a profile whose every citation is recent) and so are zeros.
    assert validate_observation(_observation(since_2021={"citations": 824, "h_index": 14, "i10_index": 17})) == []
    zero = {"citations": 0, "h_index": 0, "i10_index": 0}
    assert validate_observation(_observation(since_2021=dict(zero), **zero)) == []


@pytest.mark.parametrize(
    ("observation", "fragments"),
    [
        pytest.param(
            _observation(citations=595, i10_index=15, since_2021={"citations": 824, "h_index": 14, "i10_index": 17}),
            ["since_2021 citations (824) exceeds the all-time citations (595)", "since_2021 i10_index (17) exceeds the all-time i10_index (15)", "transposed"],
            id="transposed-columns",
        ),
        pytest.param(_observation(h_index=900), ["all-time h_index (900) exceeds all-time citations (824)"], id="all-time-h-above-citations"),
        pytest.param(
            _observation(since_2021={"citations": 10, "h_index": 11, "i10_index": 0}),
            ["since_2021 h_index (11) exceeds since_2021 citations (10)"],
            id="since-h-above-since-citations",
        ),
    ],
)
def test_validate_observation_refuses_impossible_combinations(observation: dict, fragments: list[str]):
    errors = " | ".join(validate_observation(observation))

    for fragment in fragments:
        assert fragment in errors


def test_validate_observation_reports_type_errors_without_raising_on_the_comparison():
    errors = validate_observation(_observation(citations=True, since_2021={"citations": "9", "h_index": 1, "i10_index": 1}))

    assert errors and all("non-negative integer" in error for error in errors)


def test_dry_run_and_check_refuse_an_inconsistent_observation_too(tmp_path: Path):
    checkout = _checkout(tmp_path)
    before = checkout.state()
    transposed = _observation_args(
        citations=595, i10_index=15, since_2021_citations=824, since_2021_i10_index=17
    )

    for mode in ("--dry-run", "--check"):
        result = checkout.run(*transposed, mode)
        assert result.returncode == 1
        assert "transposed" in result.stderr
    assert checkout.state() == before


# ---------------------------------------------------------------------------
# Undecodable on-disk bytes are an invalid pair, not a traceback
# ---------------------------------------------------------------------------


def test_an_undecodable_receipt_is_reported_by_check_and_overwritten_by_a_new_observation(tmp_path: Path):
    checkout = _checkout(tmp_path)
    checkout.receipt.write_bytes(UNDECODABLE)

    check = checkout.run(*_observation_args(), "--check")

    assert check.returncode == 1
    assert "Traceback" not in check.stderr
    assert "not recorded" in check.stdout
    assert "invalid Scholar verification receipt" in check.stdout and "not valid UTF-8" in check.stdout
    assert checkout.receipt.read_bytes() == UNDECODABLE

    # A genuinely new observation replaces the broken receipt along with the snapshot.
    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT))

    assert result.returncode == 0, result.stderr
    assert "Traceback" not in result.stderr
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_check_on_a_recorded_snapshot_with_an_undecodable_receipt_points_at_the_receipt(tmp_path: Path):
    checkout = _checkout(tmp_path)
    assert checkout.run(*_record_args("--verified-at", VERIFIED_AT)).returncode == 0
    checkout.receipt.write_bytes(UNDECODABLE)

    check = checkout.run(*_observation_args(), "--check")

    assert check.returncode == 1
    assert "Traceback" not in check.stderr
    assert "Scholar verification receipt" in check.stdout and "not valid UTF-8" in check.stdout
    assert "Scholar snapshot data" not in check.stdout


@pytest.mark.parametrize("mode", [[], ["--check"], ["--dry-run"]])
def test_an_undecodable_snapshot_is_a_clean_refusal(tmp_path: Path, mode: list[str]):
    checkout = _checkout(tmp_path)
    checkout.snapshot.write_bytes(UNDECODABLE)
    before = checkout.state()

    result = checkout.run(*_record_args("--verified-at", VERIFIED_AT, *mode))

    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert result.stderr.startswith("refused:") and "scholar-snapshot.json" in result.stderr
    assert checkout.state() == before


# ---------------------------------------------------------------------------
# verified_at is bounded above by as_of unless the operator states it
# ---------------------------------------------------------------------------


def test_a_clock_default_far_after_as_of_is_refused_and_an_explicit_value_is_not(tmp_path: Path):
    checkout = _checkout(tmp_path)
    before = checkout.state()

    refused = checkout.run(*_record_args(as_of=LATE_AS_OF))

    assert refused.returncode == 1
    assert "more than one day after as_of 2026-10-03" in refused.stderr
    assert "pass --verified-at" in refused.stderr
    assert checkout.state() == before
    dry = checkout.run(*_record_args("--dry-run", as_of=LATE_AS_OF))
    assert dry.returncode == 1 and "pass --verified-at" in dry.stderr

    # Stating the instant lifts the bound, even for an instant well after as_of.
    stated = checkout.run(*_record_args("--verified-at", "2026-10-05T00:30:00Z", as_of=LATE_AS_OF))

    assert stated.returncode == 0, stated.stderr
    assert json.loads(checkout.receipt.read_text(encoding="utf-8"))["verified_at"] == "2026-10-05T00:30:00Z"
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def _record_late_observation(checkout: Checkout) -> bytes:
    result = checkout.run(*_record_args("--verified-at", LATE_VERIFIED_AT, as_of=LATE_AS_OF))
    assert result.returncode == 0, result.stderr
    return checkout.snapshot.read_bytes()


def test_receipt_only_recovery_reuses_the_existing_verified_at(tmp_path: Path):
    checkout = _checkout(tmp_path)
    snapshot_bytes = _record_late_observation(checkout)
    receipt = json.loads(checkout.receipt.read_text(encoding="utf-8"))
    receipt["snapshot_sha256"] = "0" * 64
    checkout.receipt.write_bytes(canonical_json_bytes(receipt))

    # The clock default would be refused for this as_of, so success proves the stamp was reused.
    result = checkout.run(*_record_args(as_of=LATE_AS_OF))

    assert result.returncode == 0, result.stderr
    assert "receipt-only recovery" in result.stdout and "reused from the existing receipt" in result.stdout
    assert checkout.snapshot.read_bytes() == snapshot_bytes
    assert json.loads(checkout.receipt.read_text(encoding="utf-8"))["verified_at"] == LATE_VERIFIED_AT
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_receipt_only_recovery_prefers_an_explicit_verified_at(tmp_path: Path):
    checkout = _checkout(tmp_path)
    _record_late_observation(checkout)
    receipt = json.loads(checkout.receipt.read_text(encoding="utf-8"))
    receipt["snapshot_sha256"] = "0" * 64
    checkout.receipt.write_bytes(canonical_json_bytes(receipt))

    result = checkout.run(*_record_args("--verified-at", "2026-10-03T18:00:00Z", as_of=LATE_AS_OF))

    assert result.returncode == 0, result.stderr
    assert "reused" not in result.stdout
    assert json.loads(checkout.receipt.read_text(encoding="utf-8"))["verified_at"] == "2026-10-03T18:00:00Z"


def _damage_receipt(path: Path, damage: str) -> None:
    receipt = json.loads(path.read_text(encoding="utf-8"))
    receipt["snapshot_sha256"] = "0" * 64
    if damage == "binary":
        path.write_bytes(UNDECODABLE)
        return
    if damage == "deleted":
        path.unlink()
        return
    if damage == "naive-verified-at":
        receipt["verified_at"] = "2026-10-03T12:00:00"
    elif damage == "verified-at-too-early":
        receipt["verified_at"] = "2026-10-01T00:00:00Z"
    elif damage == "verified-at-too-late":
        receipt["verified_at"] = "2026-10-05T00:30:00Z"
    elif damage == "other-observation":
        receipt["snapshot_as_of"] = "2026-10-02"
    elif damage == "no-verified-at":
        del receipt["verified_at"]
    else:  # pragma: no cover - guards the parametrization
        raise AssertionError(damage)
    path.write_bytes(canonical_json_bytes(receipt))


@pytest.mark.parametrize(
    "damage",
    ["deleted", "binary", "naive-verified-at", "verified-at-too-early", "verified-at-too-late", "other-observation", "no-verified-at"],
)
def test_recovery_falls_back_to_the_defaulted_rule_when_the_old_stamp_cannot_be_reused(tmp_path: Path, damage: str):
    checkout = _checkout(tmp_path)
    snapshot_bytes = _record_late_observation(checkout)
    _damage_receipt(checkout.receipt, damage)
    broken = checkout.receipt.read_bytes() if checkout.receipt.exists() else None

    refused = checkout.run(*_record_args(as_of=LATE_AS_OF))

    assert refused.returncode == 1
    assert "pass --verified-at" in refused.stderr
    assert checkout.snapshot.read_bytes() == snapshot_bytes
    assert (checkout.receipt.read_bytes() if checkout.receipt.exists() else None) == broken

    stated = checkout.run(*_record_args("--verified-at", LATE_VERIFIED_AT, as_of=LATE_AS_OF))

    assert stated.returncode == 0, stated.stderr
    assert json.loads(checkout.receipt.read_text(encoding="utf-8"))["verified_at"] == LATE_VERIFIED_AT
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_timing_bound_on_a_defaulted_verified_at_is_one_utc_day_after_as_of():
    as_of = date(2026, 10, 3)
    now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)
    next_day_end = datetime(2026, 10, 4, 23, 59, 59, tzinfo=timezone.utc)
    two_days = datetime(2026, 10, 5, 0, 0, 0, tzinfo=timezone.utc)

    assert observation_timing_errors(as_of, next_day_end, now, verified_at_defaulted=True) == []
    errors = observation_timing_errors(as_of, two_days, now, verified_at_defaulted=True)
    assert len(errors) == 1 and "--verified-at" in errors[0]
    # A stated instant is not bounded above (the operator vouches for it).
    assert observation_timing_errors(as_of, two_days, now) == []
    assert observation_timing_errors(as_of, two_days, now, verified_at_defaulted=False) == []


def test_reusable_receipt_verified_at_applies_every_condition():
    as_of = date(2026, 10, 3)
    now = datetime(2026, 10, 9, 12, 0, tzinfo=timezone.utc)

    def receipt(**fields: object) -> bytes:
        payload = {"snapshot_as_of": "2026-10-03", "verified_at": "2026-10-03T12:00:00Z", **fields}
        return json.dumps(payload).encode("utf-8")

    assert reusable_receipt_verified_at(receipt(), as_of, now) == datetime(2026, 10, 3, 12, 0, tzinfo=timezone.utc)
    assert reusable_receipt_verified_at(receipt(verified_at="2026-10-03T05:00:00-07:00"), as_of, now) == datetime(
        2026, 10, 3, 12, 0, tzinfo=timezone.utc
    )
    for unusable in (
        None,
        UNDECODABLE,
        b"not json",
        b"[]",
        receipt(snapshot_as_of="2026-10-02"),
        receipt(verified_at="2026-10-03T12:00:00"),
        receipt(verified_at="2026-10-03"),
        receipt(verified_at=7),
        receipt(verified_at="2026-10-01T00:00:00Z"),
        receipt(verified_at="2026-10-05T00:00:00Z"),
        receipt(verified_at="2026-10-10T00:00:00Z"),
    ):
        assert reusable_receipt_verified_at(unusable, as_of, now) is None


# ---------------------------------------------------------------------------
# Rollback: the second write fails after the first succeeded
# ---------------------------------------------------------------------------


class ReplaceFailures:
    """Fail ``os.replace`` on chosen calls; every other call is the real thing."""

    def __init__(self, failing: set[int] | None = None, *, from_call: int | None = None):
        self.failing = failing or set()
        self.from_call = from_call
        self.armed = True
        self.calls: list[str] = []
        self._real = os.replace

    def __call__(self, source, destination):
        self.calls.append(Path(destination).name)
        number = len(self.calls)
        if self.armed and (number in self.failing or (self.from_call is not None and number >= self.from_call)):
            raise OSError(f"simulated os.replace failure on call {number}")
        return self._real(source, destination)


def _in_process_pair(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> tuple[Path, Path]:
    """Seed ``tmp_path/data`` and point the recorder's module-level paths at it."""
    data = tmp_path / "data"
    data.mkdir()
    snapshot = data / "scholar-snapshot.json"
    receipt = data / "scholar-verification-receipt.json"
    snapshot.write_bytes(SEED_SNAPSHOT_BYTES)
    receipt.write_bytes(SEED_RECEIPT_BYTES)
    monkeypatch.setattr(recorder, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(recorder, "SNAPSHOT", snapshot)
    monkeypatch.setattr(recorder, "RECEIPT", receipt)
    return snapshot, receipt


def test_a_failed_receipt_replace_restores_the_snapshot_and_leaves_no_temp_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    snapshot, receipt = _in_process_pair(tmp_path, monkeypatch)
    replace = ReplaceFailures({2})  # 1 = snapshot (succeeds), 2 = receipt (fails), 3 = snapshot restore
    monkeypatch.setattr(os, "replace", replace)

    code = recorder.main(_record_args("--verified-at", VERIFIED_AT))

    captured = capsys.readouterr()
    assert code == 1
    assert replace.calls == [snapshot.name, receipt.name, snapshot.name]
    assert "every replaced file was restored" in captured.err
    assert "simulated os.replace failure on call 2" in captured.err
    assert "FAILED" not in captured.err and "CRITICAL" not in captured.err
    assert snapshot.read_bytes() == SEED_SNAPSHOT_BYTES
    assert receipt.read_bytes() == SEED_RECEIPT_BYTES
    assert sorted(path.name for path in snapshot.parent.iterdir()) == sorted([receipt.name, snapshot.name])
    monkeypatch.setattr(os, "replace", replace._real)
    assert validate_scholar_snapshot_receipt(tmp_path) == []


def test_a_failed_restore_is_reported_as_failed_and_the_same_command_repairs_the_pair(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    snapshot, receipt = _in_process_pair(tmp_path, monkeypatch)
    replace = ReplaceFailures(from_call=2)  # the receipt write fails and so does restoring the snapshot
    monkeypatch.setattr(os, "replace", replace)

    code = recorder.main(_record_args("--verified-at", VERIFIED_AT))

    captured = capsys.readouterr()
    assert code == 1
    assert "restoration FAILED" in captured.err
    assert "every replaced file was restored" not in captured.err
    assert "CRITICAL: could not restore data/scholar-snapshot.json" in captured.err
    assert "Not restored: data/scholar-snapshot.json" in captured.err
    assert "re-run this exact command" in captured.err
    assert "git restore data/scholar-snapshot.json data/scholar-verification-receipt.json" in captured.err
    # The snapshot kept the new observation while the receipt is the old one: fail-closed, not silently wrong.
    assert snapshot.read_bytes() != SEED_SNAPSHOT_BYTES
    assert receipt.read_bytes() == SEED_RECEIPT_BYTES
    assert recorder._validate_pair(tmp_path) != []
    assert sorted(path.name for path in snapshot.parent.iterdir()) == sorted([receipt.name, snapshot.name])

    replace.armed = False
    repaired = recorder.main(_record_args("--verified-at", VERIFIED_AT))

    assert repaired == 0
    assert "receipt-only recovery" in capsys.readouterr().out
    assert validate_scholar_snapshot_receipt(tmp_path) == []
    assert json.loads(snapshot.read_text(encoding="utf-8"))["as_of"] == "2026-10-05"


def test_a_failed_first_write_says_nothing_was_replaced(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    snapshot, receipt = _in_process_pair(tmp_path, monkeypatch)
    monkeypatch.setattr(os, "replace", ReplaceFailures({1}))

    code = recorder.main(_record_args("--verified-at", VERIFIED_AT))

    captured = capsys.readouterr()
    assert code == 1
    assert "before any file was replaced" in captured.err and "unchanged" in captured.err
    assert "restored" not in captured.err
    assert (snapshot.read_bytes(), receipt.read_bytes()) == (SEED_SNAPSHOT_BYTES, SEED_RECEIPT_BYTES)
    assert sorted(path.name for path in snapshot.parent.iterdir()) == sorted([receipt.name, snapshot.name])
