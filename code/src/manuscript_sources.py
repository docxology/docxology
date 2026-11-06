"""Conservative bounded source custody for explicit manuscript draft renders."""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path

from docxology_tools.generated_outputs import (
    generated_output_directory_exists,
    read_generated_output_text,
)

SOURCE_DIRECTORIES = ("code/src", "code/orchestrators")
MAX_SOURCE_FILES = 2048
MAX_SOURCE_ENTRIES = 10000
MAX_SOURCE_BYTES = 8 * 1024 * 1024
MAX_TOTAL_BYTES = 32 * 1024 * 1024


def production_source_snapshot(root: Path) -> dict:
    """Hash every production Python file, including uncommitted dependencies.

    This is source content custody, not an execution trace or a claim that the
    working tree is clean. Compare snapshots before publishing render outputs.
    Directory links fail rather than silently omitting part of the inventory.
    """
    root = root.absolute()

    def unavailable(error):
        raise ValueError("Production source inventory is unavailable") from error

    hashes = {}
    entries = total = 0
    for relative in SOURCE_DIRECTORIES:
        directory = root / relative
        if not generated_output_directory_exists(root, directory):
            raise ValueError("Required production source directory is missing")
        count_before = len(hashes)
        pending = [directory]
        while pending:
            folder = pending.pop()
            if not generated_output_directory_exists(root, folder):
                raise ValueError("Production source directory disappeared")
            try:
                with os.scandir(folder) as scan:
                    for entry in scan:
                        entries += 1
                        if entries > MAX_SOURCE_ENTRIES:
                            raise ValueError("Production source entry bound exceeded")
                        info = entry.stat(follow_symlinks=False)
                        path = folder / entry.name
                        if stat.S_ISLNK(info.st_mode):
                            raise ValueError(
                                "Production source links are not permitted"
                            )
                        if stat.S_ISDIR(info.st_mode):
                            pending.append(path)
                            continue
                        if not stat.S_ISREG(info.st_mode):
                            raise ValueError(
                                "Production source entry is not a regular file"
                            )
                        if not entry.name.endswith(".py"):
                            continue
                        if len(hashes) >= MAX_SOURCE_FILES:
                            raise ValueError("Production source file bound exceeded")
                        text = read_generated_output_text(
                            root, path, newline="", max_bytes=MAX_SOURCE_BYTES
                        )
                        if text is None:
                            raise ValueError("Production source disappeared")
                        raw = text.encode("utf-8")
                        total += len(raw)
                        if total > MAX_TOTAL_BYTES:
                            raise ValueError(
                                "Production source total byte bound exceeded"
                            )
                        hashes[path.relative_to(root).as_posix()] = hashlib.sha256(
                            raw
                        ).hexdigest()
            except OSError as error:
                unavailable(error)
        if len(hashes) == count_before:
            raise ValueError("Required production source directory has no Python files")
    hashes = dict(sorted(hashes.items()))
    context = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {
        "kind": "working source content snapshot",
        "scope": [name + "/**/*.py" for name in SOURCE_DIRECTORIES],
        "files_sha256": hashes,
        "bytes": total,
        "inventory_sha256": hashlib.sha256(context).hexdigest(),
    }
