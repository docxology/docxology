"""Bounded, read-only performance diagnostics for fixed backend workloads.

Timing samples exclude context hashing and tracing overhead. These observations
never certify generated output, source freshness, deployment or release status.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

from docxology_tools.paper_artifacts import source_file, source_paths

SCHEMA_VERSION = "1.0"
WORKLOADS = ("seo", "fingerprints")


def runtime_context() -> dict:
    packages = {}
    for name in ("pillow", "pypdf", "pytest", "reportlab", "pymupdf"):
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = None
    return {"python": platform.python_version(), "implementation": platform.python_implementation(),
            "platform": platform.system(), "machine": platform.machine(),
            "cpu_count": os.cpu_count(), "packages": packages}


def source_context(root: Path) -> dict:
    """Bind Git-visible source names and bytes, refusing unsafe/changing reads."""
    visible = source_paths(root)
    digest = hashlib.sha256()
    count = size = 0
    for name in sorted(visible):
        path = source_file(root, name, visible)
        if path is None:
            raise ValueError("a Git-visible source file is unavailable")
        before = path.stat()
        digest.update(name.encode("utf-8") + b"\0" + str(before.st_size).encode() + b"\0")
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b""):
                digest.update(chunk)
        after = path.stat()
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns):
            raise ValueError("a source file changed during context capture")
        digest.update(b"\0")
        count += 1
        size += before.st_size
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, check=True,
                            capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=15,
                            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    index = subprocess.run(["git", "ls-files", "--cached", "-z"], cwd=root, check=True,
                           capture_output=True, stdin=subprocess.DEVNULL, timeout=15,
                           env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
    membership = b"\0".join(sorted(set(index.stdout.split(b"\0")) - {b""}))
    return {"head": result.stdout.strip(), "index_membership_sha256": hashlib.sha256(membership).hexdigest(),
            "visible_content_sha256": digest.hexdigest(),
            "files": count, "bytes": size}


def execute(workload: str, root: Path):
    if workload == "seo":
        from docxology_tools import seo_invariants
        seo_invariants.clear_page_cache()
        return seo_invariants.collect_seo_errors(root)
    if workload == "fingerprints":
        from docxology_tools.generation_plan import LOCAL_GENERATION_STEPS, step_input_fingerprint
        return {step.identifier: step_input_fingerprint(step, root)
                for step in LOCAL_GENERATION_STEPS if step.inputs}
    raise ValueError("unknown fixed workload")


def trace_rows(profile, root: Path, limit: int = 30) -> list[dict]:
    rows = []
    for entry in profile.getstats():
        code = entry.code
        if isinstance(code, str):
            name, file, line = code, "<builtin>", 0
        else:
            name, line = code.co_name, code.co_firstlineno
            path = Path(code.co_filename)
            file = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.name
        rows.append({"function": name, "file": file, "line": line, "calls": entry.callcount,
                     "recursive_calls": entry.reccallcount, "self_seconds": entry.inlinetime,
                     "cumulative_seconds": entry.totaltime})
    return sorted(rows, key=lambda row: (-row["cumulative_seconds"], row["file"], row["line"]))[:limit]


def measure(workload: str, root: Path, mode: str) -> dict:
    if workload not in WORKLOADS or mode not in ("timing", "tracing"):
        raise ValueError("unknown workload or profiling mode")
    if sys.version_info < (3, 15):
        raise ValueError("backend profiling requires Python 3.15 or later")
    before = source_context(root)
    profile = None
    if mode == "tracing":
        from profiling.tracing import Profile
        profile = Profile()
    start = time.perf_counter()
    result = profile.runcall(execute, workload, root) if profile else execute(workload, root)
    elapsed = time.perf_counter() - start
    after = source_context(root)
    if before != after:
        raise ValueError("source context changed during the workload; discard this sample")
    return {"source": before, "runtime": runtime_context(), "mode": mode,
            "elapsed_seconds": elapsed,
            "result_sha256": hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest(),
            "result_items": len(result),
            "trace": trace_rows(profile, root) if profile else [],
            "validation": "not_run", "network_freshness": "not_checked"}


def run_samples(script: Path, root: Path, workload: str, mode: str, repeats: int, timeout: int) -> dict:
    if workload not in WORKLOADS or mode not in ("timing", "tracing"):
        raise ValueError("unknown workload or profiling mode")
    if not 1 <= repeats <= 10 or not 1 <= timeout <= 600:
        raise ValueError("repeats must be 1–10 and timeout must be 1–600 seconds per sample")
    samples = []
    for _ in range(repeats):
        result = subprocess.run(
            [sys.executable, str(script), workload, "--mode", mode, "--worker"],
            cwd=root, check=False, capture_output=True, text=True, stdin=subprocess.DEVNULL,
            timeout=timeout, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "GIT_OPTIONAL_LOCKS": "0"})
        if result.returncode:
            raise ValueError("profiling worker failed; no successful comparison is available")
        sample = json.loads(result.stdout)
        if not sample.get("ok"):
            raise ValueError("profiling worker could not produce a stable sample")
        samples.append(sample["sample"])
    contexts_match = all((sample["source"], sample["runtime"], sample["result_sha256"]) ==
                         (samples[0]["source"], samples[0]["runtime"], samples[0]["result_sha256"])
                         for sample in samples)
    if not contexts_match:
        raise ValueError("sample contexts or results differ; discard the comparison")
    return {"schema_version": SCHEMA_VERSION, "ok": True, "workload": workload, "mode": mode,
            "samples": samples, "contexts_match": True,
            "sampling": "not_run", "validation": "not_run", "deployment": "not_checked",
            "timing_includes_tracing_overhead": mode == "tracing"}


def write_report(path: Path, root: Path, payload: dict) -> None:
    """Create a new external diagnostic; never replace a previous observation."""
    destination = path.resolve()
    if destination.is_relative_to(root.resolve()):
        raise ValueError("profiling reports must be outside the repository")
    with destination.open("x", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
