"""Regeneration root, mutation, and restart contracts in disposable trees."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import generation_plan  # noqa: E402
import regenerate_all  # noqa: E402


@pytest.fixture
def fixture_step(tmp_path):
    for relative, content in (
        ("data/source.txt", "before\n"),
        ("code/src/fixture.py", "# shared fixture\n"),
        ("code/orchestrators/root_contract_fixture.py", "# writer fixture\n"),
    ):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return generation_plan.GenerationStep(
        "fixture", "root_contract_fixture.py", (), ("--check",),
        "Disposable writer", ("data/source.txt",),
    )


def test_default_runner_and_cache_use_the_same_injected_root(tmp_path, fixture_step):
    """Execute the real child process; the working checkout is never its cwd."""
    writer = tmp_path / "code/orchestrators/root_contract_fixture.py"
    writer.write_text(
        "from pathlib import Path\n"
        "Path('output.txt').write_text(Path('data/source.txt').read_text())\n"
        "Path('observed-root.txt').write_text(str(Path.cwd()))\n",
        encoding="utf-8",
    )
    assert regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(fixture_step,), emit=lambda _message: None,
    ) == (1, 0)
    assert (tmp_path / "output.txt").read_text() == "before\n"
    assert (tmp_path / "observed-root.txt").read_text() == str(tmp_path)
    assert generation_plan.load_regeneration_state(tmp_path)["fixture"]
    assert regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(fixture_step,), emit=lambda _message: None,
    ) == (0, 1)


def test_real_writer_input_change_cannot_cache_old_output_as_fresh(tmp_path, fixture_step):
    writer = tmp_path / "code/orchestrators/root_contract_fixture.py"
    writer.write_text(
        "from pathlib import Path\n"
        "source = Path('data/source.txt')\n"
        "Path('output.txt').write_text(source.read_text())\n"
        "if source.read_text() == 'before\\n':\n"
        "    source.write_text('after\\n')\n",
        encoding="utf-8",
    )
    messages = []
    assert regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(fixture_step,), emit=messages.append,
    ) == (1, 0)
    assert (tmp_path / "output.txt").read_text() == "before\n"
    assert "fixture" not in generation_plan.load_regeneration_state(tmp_path)
    assert messages == [
        "cache invalidated fixture: declared inputs changed during writer",
    ]
    assert regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(fixture_step,), emit=messages.append,
    ) == (1, 0)
    assert (tmp_path / "output.txt").read_text() == "after\n"
    assert regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(fixture_step,), emit=messages.append,
    ) == (0, 1)


def test_failed_forced_writer_cannot_leave_partial_output_eligible_to_skip(
    tmp_path, fixture_step,
):
    writer = tmp_path / "code/orchestrators/root_contract_fixture.py"
    writer.write_text(
        "from pathlib import Path\n"
        "if Path('fail-next').exists():\n"
        "    Path('fail-next').unlink()\n"
        "    Path('output.txt').write_text('partial output\\n')\n"
        "    raise SystemExit(3)\n"
        "Path('output.txt').write_text(Path('data/source.txt').read_text())\n",
        encoding="utf-8",
    )
    options = dict(repo_root=tmp_path, steps=(fixture_step,), emit=lambda _message: None)
    assert regenerate_all.run_regeneration(**options) == (1, 0)
    assert "fixture" in generation_plan.load_regeneration_state(tmp_path)
    (tmp_path / "fail-next").touch()
    with pytest.raises(subprocess.CalledProcessError) as caught:
        regenerate_all.run_regeneration(force=True, **options)
    assert caught.value.returncode == 3
    assert (tmp_path / "output.txt").read_text() == "partial output\n"
    assert "fixture" not in generation_plan.load_regeneration_state(tmp_path)
    assert regenerate_all.run_regeneration(**options) == (1, 0)
    assert (tmp_path / "output.txt").read_text() == "before\n"
    assert regenerate_all.run_regeneration(**options) == (0, 1)


@pytest.mark.parametrize("change", ["delete", "create"])
def test_missing_inputs_at_either_writer_boundary_invalidate_cache(
    tmp_path, fixture_step, change,
):
    source = tmp_path / "data/source.txt"
    initial = generation_plan.step_input_fingerprint(fixture_step, tmp_path)
    generation_plan.save_regeneration_state({"fixture": initial}, tmp_path)
    if change == "create":
        source.unlink()

    def runner(_script, _args):
        if change == "delete":
            source.unlink()
        else:
            source.write_text("after\n")

    assert regenerate_all.run_regeneration(
        repo_root=tmp_path, steps=(fixture_step,), force=True, runner=runner,
        emit=lambda _message: None,
    ) == (1, 0)
    assert "fixture" not in generation_plan.load_regeneration_state(tmp_path)


@pytest.mark.parametrize("payload", [
    {"steps": {}},
    {"schema_version": 2, "steps": {}},
    {"schema_version": True, "steps": {}},
    {"schema_version": 1.0, "steps": {}},
    {"schema_version": 1, "steps": {"fixture": 123}},
    {"schema_version": 1, "steps": {"fixture": None}},
    {"schema_version": 1, "steps": {"fixture": "not-a-fingerprint"}},
    {"schema_version": 1, "steps": {"": "a" * 64}},
])
def test_unknown_or_malformed_cache_is_cold_state(tmp_path, payload):
    path = generation_plan.regeneration_state_path(tmp_path)
    path.parent.mkdir()
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert generation_plan.load_regeneration_state(tmp_path) == {}


def test_valid_cache_round_trip_is_deterministic(tmp_path):
    state = {"z": "b" * 64, "a": "a" * 64}
    generation_plan.save_regeneration_state(state, tmp_path)
    path = generation_plan.regeneration_state_path(tmp_path)
    before = path.read_bytes()
    assert generation_plan.load_regeneration_state(tmp_path) == state
    generation_plan.save_regeneration_state(dict(reversed(list(state.items()))), tmp_path)
    assert path.read_bytes() == before
    assert list(path.parent.glob(".regeneration-state-*.tmp")) == []


def test_failed_atomic_cache_replace_preserves_previous_receipt(tmp_path, monkeypatch):
    generation_plan.save_regeneration_state({"fixture": "a" * 64}, tmp_path)
    path = generation_plan.regeneration_state_path(tmp_path)
    before = path.read_bytes()

    def fail_replace(_source, _destination):
        raise OSError("fixture replace failure")

    monkeypatch.setattr(generation_plan.os, "replace", fail_replace)
    with pytest.raises(OSError, match="fixture replace failure"):
        generation_plan.save_regeneration_state({"fixture": "b" * 64}, tmp_path)
    assert path.read_bytes() == before
    assert list(path.parent.glob(".regeneration-state-*.tmp")) == []


def test_input_vanishing_between_discovery_and_stat_is_not_cached(tmp_path, monkeypatch):
    source = tmp_path / "source.txt"
    source.write_text("fixture\n")
    original_stat = Path.stat
    calls = 0

    def stat(path, *args, **kwargs):
        nonlocal calls
        if path == source:
            calls += 1
            if calls == 2:
                raise FileNotFoundError("fixture vanished after discovery")
        return original_stat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "stat", stat)
    assert generation_plan.input_fingerprint(tmp_path, ("source.txt",)) is None
    assert calls == 2


@pytest.fixture
def process_driver(tmp_path, fixture_step):
    """Independent interpreters run the production driver in a disposable tree."""
    repository = Path(__file__).resolve().parents[2]
    for relative in (
        "code/orchestrators/regenerate_all.py", "code/src/generation_plan.py",
        "code/src/docxology_tools/__init__.py",
    ):
        destination = tmp_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(repository / relative, destination)
    writer = tmp_path / "code/orchestrators/root_contract_fixture.py"
    writer.write_text(
        "import os, time\n"
        "from pathlib import Path\n"
        "mode = os.environ['DOCXOLOGY_FIXTURE_MODE']\n"
        "Path('writer-started-' + mode).touch()\n"
        "Path('output.txt').write_text('partial output\\n' if mode == 'failure' "
        "else Path('data/source.txt').read_text())\n"
        "if mode in ('success', 'failure'):\n"
        "    deadline = time.monotonic() + 15\n"
        "    while not Path('release-writer').exists():\n"
        "        if time.monotonic() > deadline: raise SystemExit(99)\n"
        "        time.sleep(0.01)\n"
        "if mode == 'failure': raise SystemExit(3)\n",
        encoding="utf-8",
    )
    driver = tmp_path / "code/orchestrators/driver.py"
    driver.write_text(
        "import os, sys, time\n"
        "from pathlib import Path\n"
        "import regenerate_all\n"
        "from docxology_tools.generation_plan import GenerationStep\n"
        "step = GenerationStep('fixture', 'root_contract_fixture.py', (), "
        "('--check',), 'writer', ('data/source.txt',))\n"
        "def emit(message):\n"
        "    if os.environ['DOCXOLOGY_FIXTURE_MODE'] == 'between-passes' "
        "and message == 'Local regeneration pass 2/2':\n"
        "        Path('between-passes').touch()\n"
        "        deadline = time.monotonic() + 15\n"
        "        while not Path('release-passes').exists():\n"
        "            if time.monotonic() > deadline: raise SystemExit(99)\n"
        "            time.sleep(0.01)\n"
        "    print(message, flush=True)\n"
        "operation = regenerate_all.run_regeneration_passes "
        "if len(sys.argv) > 1 else regenerate_all.run_regeneration\n"
        "try:\n"
        "    print(operation(steps=(step,), emit=emit), flush=True)\n"
        "except regenerate_all.RegenerationLockError as exc:\n"
        "    print(str(exc), file=sys.stderr)\n"
        "    raise SystemExit(75)\n",
        encoding="utf-8",
    )
    return driver


def _process_command(driver, *, passes=False):
    return [sys.executable, str(driver), *(["passes"] if passes else [])]


def _process_environment(mode):
    return {**os.environ, "DOCXOLOGY_FIXTURE_MODE": mode}


def _wait_for_signal(path, process):
    deadline = time.monotonic() + 8
    while not path.exists():
        assert process.poll() is None, "fixture driver exited before reaching its write boundary"
        assert time.monotonic() < deadline, "fixture driver did not reach its bounded write boundary"
        time.sleep(0.01)


@pytest.mark.parametrize("mode", ["success", "failure"])
@pytest.mark.parametrize("passes", [False, True])
def test_independent_overlapping_run_rejected_before_writer_and_cache(
    tmp_path, process_driver, mode, passes,
):
    first = subprocess.Popen(
        _process_command(process_driver, passes=passes), cwd=tmp_path,
        env=_process_environment(mode), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    try:
        _wait_for_signal(tmp_path / f"writer-started-{mode}", first)
        cache = generation_plan.regeneration_state_path(tmp_path)
        before = cache.read_bytes() if cache.exists() else None
        contender = subprocess.run(
            _process_command(process_driver), cwd=tmp_path,
            env=_process_environment("contender"), capture_output=True,
            text=True, timeout=5,
        )
        assert contender.returncode == 75
        assert "another regeneration is active" in contender.stderr
        assert not (tmp_path / "writer-started-contender").exists()
        assert (cache.read_bytes() if cache.exists() else None) == before
        lock = tmp_path / ".docxology/regeneration.lock"
        inode = lock.stat().st_ino
        assert lock.stat().st_mode & 0o777 == 0o600
        (tmp_path / "release-writer").touch()
        stdout, stderr = first.communicate(timeout=8)
        assert first.returncode == (0 if mode == "success" else 1), (stdout, stderr)
        assert ("fixture" in generation_plan.load_regeneration_state(tmp_path)) == (mode == "success")

        recovery = subprocess.run(
            _process_command(process_driver), cwd=tmp_path,
            env=_process_environment("recovery"), capture_output=True,
            text=True, timeout=5,
        )
        assert recovery.returncode == 0, recovery.stderr
        assert (tmp_path / "output.txt").read_text() == "before\n"
        assert lock.stat().st_ino == inode  # Never unlink and split the lock domain.
        assert ("(0, 1)" if mode == "success" else "(1, 0)") in recovery.stdout
        assert "fixture" in generation_plan.load_regeneration_state(tmp_path)
    finally:
        (tmp_path / "release-writer").touch()
        if first.poll() is None:
            first.kill()
        first.communicate(timeout=8)


def test_independent_run_is_rejected_between_passes(tmp_path, process_driver):
    first = subprocess.Popen(
        _process_command(process_driver, passes=True), cwd=tmp_path,
        env=_process_environment("between-passes"), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    try:
        _wait_for_signal(tmp_path / "between-passes", first)
        assert "fixture" in generation_plan.load_regeneration_state(tmp_path)
        contender = subprocess.run(
            _process_command(process_driver), cwd=tmp_path,
            env=_process_environment("contender"), capture_output=True,
            text=True, timeout=5,
        )
        assert contender.returncode == 75
        assert "another regeneration is active" in contender.stderr
        assert not (tmp_path / "writer-started-contender").exists()
        (tmp_path / "release-passes").touch()
        stdout, stderr = first.communicate(timeout=8)
        assert first.returncode == 0, (stdout, stderr)
        assert "(1, 1)" in stdout
    finally:
        (tmp_path / "release-passes").touch()
        if first.poll() is None:
            first.kill()
        first.communicate(timeout=8)


def test_writer_keeps_lock_if_driver_is_terminated(tmp_path, process_driver):
    first = subprocess.Popen(
        _process_command(process_driver), cwd=tmp_path,
        env=_process_environment("success"), stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_signal(tmp_path / "writer-started-success", first)
        first.kill()
        first.wait(timeout=5)
        contender = subprocess.run(
            _process_command(process_driver), cwd=tmp_path,
            env=_process_environment("contender"), capture_output=True,
            text=True, timeout=5,
        )
        assert contender.returncode == 75
        assert not (tmp_path / "writer-started-contender").exists()
        (tmp_path / "release-writer").touch()
        # Wait for the real writer to exit and release its inherited descriptor.
        deadline = time.monotonic() + 8
        while True:
            try:
                with regenerate_all._regeneration_lock(tmp_path):
                    break
            except regenerate_all.RegenerationLockError:
                assert time.monotonic() < deadline, "orphan writer did not release its lock"
                time.sleep(0.01)
        recovery = subprocess.run(
            _process_command(process_driver), cwd=tmp_path,
            env=_process_environment("recovery"), capture_output=True,
            text=True, timeout=5,
        )
        assert recovery.returncode == 0, recovery.stderr
        assert "(1, 0)" in recovery.stdout
    finally:
        (tmp_path / "release-writer").touch()
        if first.poll() is None:
            first.kill()
        first.wait(timeout=5)


def test_cli_validation_keeps_same_lock(tmp_path, process_driver):
    validator = tmp_path / "code/orchestrators/validate_repo.py"
    validator.write_text(
        "import time\n"
        "from pathlib import Path\n"
        "Path('validation-started').touch()\n"
        "deadline = time.monotonic() + 15\n"
        "while not Path('release-validation').exists():\n"
        "    if time.monotonic() > deadline: raise SystemExit(99)\n"
        "    time.sleep(0.01)\n",
        encoding="utf-8",
    )
    # Change only the disposable entry-point plan; main itself and its child
    # validation invocation are production code, not a mock of subprocess.run.
    process_driver.write_text(
        process_driver.read_text().split("operation =", 1)[0]
        + "regenerate_all.LOCAL_GENERATION_STEPS = (step,)\n"
        + "regenerate_all.validate_generation_plan = lambda: None\n"
        + "raise SystemExit(regenerate_all.main())\n",
        encoding="utf-8",
    )
    first = subprocess.Popen(
        [sys.executable, str(process_driver), "--validate"], cwd=tmp_path,
        env=_process_environment("validation"), stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    )
    try:
        _wait_for_signal(tmp_path / "validation-started", first)
        assert "fixture" in generation_plan.load_regeneration_state(tmp_path)
        contender = subprocess.run(
            [sys.executable, str(process_driver)], cwd=tmp_path,
            env=_process_environment("contender"), capture_output=True,
            text=True, timeout=5,
        )
        assert contender.returncode == 1
        assert "regeneration refused: another regeneration is active" in contender.stderr
        assert not (tmp_path / "writer-started-contender").exists()
        (tmp_path / "release-validation").touch()
        stdout, stderr = first.communicate(timeout=8)
        assert first.returncode == 0, (stdout, stderr)
    finally:
        (tmp_path / "release-validation").touch()
        if first.poll() is None:
            first.kill()
        first.communicate(timeout=8)


def test_unsupported_lock_platform_fails_before_cache_or_writer(tmp_path, monkeypatch):
    monkeypatch.setattr(regenerate_all, "fcntl", None)
    with pytest.raises(regenerate_all.RegenerationLockError, match="requires POSIX flock"):
        regenerate_all.run_regeneration(repo_root=tmp_path, steps=())
    assert not (tmp_path / ".docxology").exists()
    assert not generation_plan.regeneration_state_path(tmp_path).exists()


@pytest.mark.parametrize("unsafe", [
    "directory-symlink", "file-symlink", "file-hardlink", "file-fifo",
])
def test_lock_refuses_unsafe_file_aliases(tmp_path, unsafe):
    private = tmp_path / ".docxology"
    external = tmp_path / "unrelated"
    external.mkdir()
    target = external / "retain.txt"
    target.write_text("keep these bytes\n")
    if unsafe == "directory-symlink":
        private.symlink_to(external, target_is_directory=True)
    else:
        private.mkdir()
        if unsafe == "file-symlink":
            (private / "regeneration.lock").symlink_to(target)
        elif unsafe == "file-fifo":
            os.mkfifo(private / "regeneration.lock")
        else:
            os.link(target, private / "regeneration.lock")
    with pytest.raises(regenerate_all.RegenerationLockError):
        regenerate_all.run_regeneration(repo_root=tmp_path, steps=())
    assert target.read_text() == "keep these bytes\n"
    assert not generation_plan.regeneration_state_path(tmp_path).exists()


def test_regeneration_lock_is_ignored_by_git():
    repository = Path(__file__).resolve().parents[2]
    result = subprocess.run(
        ["git", "check-ignore", ".docxology/regeneration.lock"], cwd=repository,
        capture_output=True, text=True, timeout=5,
    )
    assert result.returncode == 0
