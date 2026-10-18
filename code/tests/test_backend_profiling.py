"""Diagnostic boundaries cannot silently become successful performance claims."""
import json
from pathlib import Path
import subprocess
import sys

import pytest

_DOCXOLOGY_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_DOCXOLOGY_SRC) not in sys.path:
    sys.path.append(str(_DOCXOLOGY_SRC))

from docxology_tools import backend_profiling as profiling  # noqa: E402


def test_reports_are_new_and_external(tmp_path):
    root = tmp_path / 'repo'
    root.mkdir()
    with pytest.raises(ValueError, match='outside'):
        profiling.write_report(root / 'report.json', root, {'ok': True})
    outside = tmp_path / 'report.json'
    profiling.write_report(outside, root, {'ok': True})
    original = outside.read_bytes()
    with pytest.raises(FileExistsError):
        profiling.write_report(outside, root, {'ok': False})
    assert outside.read_bytes() == original
    alias = tmp_path / 'alias'
    alias.symlink_to(root, target_is_directory=True)
    with pytest.raises(ValueError, match='outside'):
        profiling.write_report(alias / 'via-link.json', root, {})


def test_measure_rejects_changed_context(tmp_path, monkeypatch):
    contexts = iter([{'hash': 'before'}, {'hash': 'after'}])
    monkeypatch.setattr(profiling, 'source_context', lambda root: next(contexts))
    monkeypatch.setattr(profiling, 'execute', lambda *_: [])
    with pytest.raises(ValueError, match='changed'):
        profiling.measure('seo', tmp_path, 'timing')


def test_source_context_binds_bytes_with_restored_mtime(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    path = tmp_path / 'source.txt'
    path.write_text('first')
    subprocess.run(['git', '-C', str(tmp_path), 'add', 'source.txt'], check=True)
    subprocess.run(['git', '-C', str(tmp_path), '-c', 'user.name=Fixture', '-c',
                    'user.email=fixture@example.com', 'commit', '-qm', 'fixture'], check=True)
    before = profiling.source_context(tmp_path)
    info = path.stat()
    path.write_text('other')
    import os
    os.utime(path, ns=(info.st_atime_ns, info.st_mtime_ns))
    after = profiling.source_context(tmp_path)
    assert before['head'] == after['head']
    assert before['visible_content_sha256'] != after['visible_content_sha256']
    path.unlink()
    path.symlink_to(tmp_path.parent / 'outside')
    with pytest.raises(ValueError, match='Symlinked'):
        profiling.source_context(tmp_path)


def sample():
    return {'source': {'head': 'a', 'hash': 'b'}, 'runtime': {'python': '3.15.0'},
            'result_sha256': 'c', 'elapsed_seconds': 0.1}


def test_samples_use_exact_fixed_worker_and_explicit_noncertification(tmp_path, monkeypatch):
    calls = []
    def run(argv, **kwargs):
        calls.append((argv, kwargs))
        return subprocess.CompletedProcess(argv, 0, json.dumps({'ok': True, 'sample': sample()}), '')
    monkeypatch.setattr(profiling.subprocess, 'run', run)
    report = profiling.run_samples(tmp_path / 'profile_backend.py', tmp_path, 'seo', 'timing', 2, 7)
    assert len(report['samples']) == 2 and report['contexts_match']
    assert report['validation'] == 'not_run' and report['deployment'] == 'not_checked'
    assert report['timing_includes_tracing_overhead'] is False
    argv, kwargs = calls[0]
    assert argv == [sys.executable, str(tmp_path / 'profile_backend.py'), 'seo', '--mode', 'timing', '--worker']
    assert kwargs['timeout'] == 7 and kwargs['stdin'] == subprocess.DEVNULL
    assert kwargs['env']['PYTHONDONTWRITEBYTECODE'] == '1'
    assert kwargs['env']['GIT_OPTIONAL_LOCKS'] == '0'


@pytest.mark.parametrize('field', ['source', 'runtime', 'result_sha256'])
def test_incompatible_samples_cannot_claim_comparability(tmp_path, monkeypatch, field):
    a, b = sample(), sample()
    b[field] = 'changed'
    samples = iter([a, b])
    monkeypatch.setattr(profiling.subprocess, 'run', lambda argv, **kw: subprocess.CompletedProcess(
        argv, 0, json.dumps({'ok': True, 'sample': next(samples)}), ''))
    with pytest.raises(ValueError, match='differ'):
        profiling.run_samples(tmp_path / 'profile.py', tmp_path, 'seo', 'timing', 2, 7)


def test_nonzero_worker_is_unavailable(tmp_path, monkeypatch):
    monkeypatch.setattr(profiling.subprocess, 'run', lambda argv, **kw:
                        subprocess.CompletedProcess(argv, 1, '{}', 'private stderr'))
    with pytest.raises(ValueError, match='worker failed'):
        profiling.run_samples(tmp_path / 'profile.py', tmp_path, 'seo', 'timing', 1, 7)


def test_timeout_cannot_return_a_sample(tmp_path, monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired('own worker', kwargs['timeout'])
    monkeypatch.setattr(profiling.subprocess, 'run', timeout)
    with pytest.raises(subprocess.TimeoutExpired):
        profiling.run_samples(tmp_path / 'profile.py', tmp_path, 'seo', 'timing', 1, 7)


@pytest.mark.parametrize('workload,mode,repeats,timeout', [
    ('arbitrary', 'timing', 1, 1), ('seo', 'shell', 1, 1),
    ('seo', 'timing', 0, 1), ('seo', 'timing', 11, 1), ('seo', 'timing', 1, 601)])
def test_bounds_reject_before_execution(tmp_path, monkeypatch, workload, mode, repeats, timeout):
    def forbidden(*args, **kwargs):
        pytest.fail('invalid request started a worker')
    monkeypatch.setattr(profiling.subprocess, 'run', forbidden)
    with pytest.raises(ValueError):
        profiling.run_samples(tmp_path / 'profile.py', tmp_path, workload, mode, repeats, timeout)


def test_source_context_observes_index_membership_without_byte_or_head_change(tmp_path):
    subprocess.run(['git', 'init', '-q', str(tmp_path)], check=True)
    (tmp_path / 'base.txt').write_text('base')
    subprocess.run(['git', '-C', str(tmp_path), 'add', 'base.txt'], check=True)
    subprocess.run(['git', '-C', str(tmp_path), '-c', 'user.name=Fixture', '-c',
                    'user.email=fixture@example.com', 'commit', '-qm', 'fixture'], check=True)
    (tmp_path / 'receipt.json').write_text('{}')
    before = profiling.source_context(tmp_path)
    subprocess.run(['git', '-C', str(tmp_path), 'add', 'receipt.json'], check=True)
    staged = profiling.source_context(tmp_path)
    assert before['head'] == staged['head']
    assert before['visible_content_sha256'] == staged['visible_content_sha256']
    assert before['index_membership_sha256'] != staged['index_membership_sha256']
    subprocess.run(['git', '-C', str(tmp_path), 'rm', '--cached', 'receipt.json'], check=True)
    assert profiling.source_context(tmp_path) == before
