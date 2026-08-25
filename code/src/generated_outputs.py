"""Safe primitives for deterministic generated-file checks.

The pure :func:`output_drift` comparison is intentionally separate from file
I/O.  A generator can render its complete expected outputs once, then either
compare those bytes without writing (``--check``) or apply the same mapping.
Keeping the comparison independent from rendering prevents a check from
accidentally comparing freshly rendered content with itself.

Generated outputs are a release boundary, rather than ordinary scratch files.
Every I/O helper below requires the trusted repository root and rejects a
target outside that root, a final symlink, any symlinked path component below
the root, or a pre-existing hard-linked output file.  The helpers use
directory file descriptors with
``O_NOFOLLOW`` after the initial validation as well, so an intervening path
swap cannot redirect a read or write outside the checked-out repository.
"""

from __future__ import annotations

from collections.abc import Mapping
from contextlib import contextmanager
import json
import os
from pathlib import Path
import secrets
import stat
from typing import Callable, Iterator


class UnsafeGeneratedOutputPathError(ValueError):
    """A generated output cannot safely be read, written, or removed."""


def _lexical_absolute(path: Path) -> Path:
    """Normalize *path* without resolving any symbolic links."""
    return Path(os.path.abspath(os.fspath(path)))


def _path_entry(path: Path, *, label: str) -> os.stat_result | None:
    """Return an ``lstat`` result, keeping absent output paths distinguishable."""
    try:
        return path.lstat()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise UnsafeGeneratedOutputPathError(
            f"unable to inspect {label}: {path}: {exc}"
        ) from exc


def _reject_link(entry: os.stat_result | None, path: Path, *, label: str) -> None:
    if entry is not None and stat.S_ISLNK(entry.st_mode):
        raise UnsafeGeneratedOutputPathError(
            f"symlinked generated output {label} is not permitted: {path}"
        )


def _trusted_root_and_parts(repo_root: Path, target: Path, *, directory: bool) -> tuple[Path, Path, tuple[str, ...]]:
    """Validate lexical containment and all existing components under a root.

    ``Path.resolve`` must not be used for this boundary: it follows precisely
    the links the release chain must reject.  A trusted, non-symlink root is
    normalized lexically, then every existing component below it is inspected
    with ``lstat`` before any content operation begins.
    """
    root = _lexical_absolute(repo_root)
    candidate = _lexical_absolute(target)
    root_entry = _path_entry(root, label="generated-output root")
    if root_entry is None:
        raise UnsafeGeneratedOutputPathError(f"generated-output root is missing: {root}")
    _reject_link(root_entry, root, label="root")
    if not stat.S_ISDIR(root_entry.st_mode):
        raise UnsafeGeneratedOutputPathError(f"generated-output root is not a directory: {root}")
    try:
        relative = candidate.relative_to(root)
    except ValueError as exc:
        raise UnsafeGeneratedOutputPathError(
            f"generated output must be contained in {root}: {candidate}"
        ) from exc
    if not relative.parts:
        if directory:
            return root, candidate, ()
        raise UnsafeGeneratedOutputPathError(
            f"generated output target must name a file below the repository root: {candidate}"
        )

    current = root
    for index, component in enumerate(relative.parts):
        current = current / component
        entry = _path_entry(current, label="generated output target")
        _reject_link(entry, current, label="target or ancestor")
        if entry is None:
            continue
        is_final = index == len(relative.parts) - 1
        if not is_final and not stat.S_ISDIR(entry.st_mode):
            raise UnsafeGeneratedOutputPathError(
                f"generated output ancestor is not a directory: {current}"
            )
        if is_final:
            required = stat.S_ISDIR if directory else stat.S_ISREG
            if not required(entry.st_mode):
                kind = "directory" if directory else "regular file"
                raise UnsafeGeneratedOutputPathError(
                    f"generated output target is not a {kind}: {current}"
                )
            if not directory and entry.st_nlink > 1:
                raise UnsafeGeneratedOutputPathError(
                    f"hard-linked generated output is not permitted: {current}"
                )
    return root, candidate, relative.parts


def safe_generated_output_path(repo_root: Path, target: Path) -> Path:
    """Return a repository-local generated-file target after safety checks.

    A missing final target is valid: check mode represents it as drift and
    write mode creates it through :func:`write_generated_output_text`.
    """
    _root, candidate, _parts = _trusted_root_and_parts(repo_root, target, directory=False)
    return candidate


def generated_output_directory_exists(repo_root: Path, directory: Path) -> bool:
    """Check a generated-output directory without following symlinks.

    Missing directories are ordinary drift in a no-write check.  Existing
    directories must be real directories beneath the trusted root.
    """
    _root, candidate, _parts = _trusted_root_and_parts(repo_root, directory, directory=True)
    return _path_entry(candidate, label="generated-output directory") is not None


def _nofollow_flag() -> int:
    """Return ``O_NOFOLLOW`` or fail closed on platforms that lack it."""
    try:
        return os.O_NOFOLLOW
    except AttributeError as exc:  # pragma: no cover - only unsupported platforms
        raise UnsafeGeneratedOutputPathError(
            "platform lacks O_NOFOLLOW; refusing generated-output I/O"
        ) from exc


def _open_flags(*, directory: bool = False) -> int:
    """Return platform features required for fail-closed descriptor traversal."""
    try:
        flags = os.O_RDONLY | _nofollow_flag()
        if directory:
            flags |= os.O_DIRECTORY
    except AttributeError as exc:  # pragma: no cover - only unsupported platforms
        raise UnsafeGeneratedOutputPathError(
            "platform lacks O_NOFOLLOW/O_DIRECTORY; refusing generated-output I/O"
        ) from exc
    if os.open not in os.supports_dir_fd:  # pragma: no cover - only unsupported platforms
        raise UnsafeGeneratedOutputPathError(
            "platform lacks directory-descriptor support; refusing generated-output I/O"
        )
    return flags


def _open_directory(path: Path) -> int:
    try:
        return os.open(path, _open_flags(directory=True))
    except OSError as exc:
        raise UnsafeGeneratedOutputPathError(
            f"unable to open generated-output directory safely: {path}: {exc}"
        ) from exc


def _open_child_directory(parent_fd: int, component: str, *, create: bool) -> int:
    """Open one direct child directory without following a link."""
    try:
        return os.open(component, _open_flags(directory=True), dir_fd=parent_fd)
    except FileNotFoundError:
        if not create:
            raise
        try:
            os.mkdir(component, mode=0o777, dir_fd=parent_fd)
        except FileExistsError:
            # A concurrent creator is safe only if the no-follow open below
            # confirms it became a real directory rather than a link.
            pass
        try:
            return os.open(component, _open_flags(directory=True), dir_fd=parent_fd)
        except OSError as exc:
            raise UnsafeGeneratedOutputPathError(
                f"unable to create generated-output directory safely: {component}: {exc}"
            ) from exc
    except OSError as exc:
        raise UnsafeGeneratedOutputPathError(
            f"unsafe generated-output ancestor {component!r}: {exc}"
        ) from exc


@contextmanager
def _parent_directory_fd(repo_root: Path, target: Path, *, create: bool) -> Iterator[tuple[int, str]]:
    """Yield a no-follow directory descriptor for *target*'s parent.

    The upfront lexical/lstat validation gives clear errors; descriptor
    traversal repeats the important boundary at use time and prevents an
    ancestor-link race from redirecting an operation.
    """
    root, _candidate, parts = _trusted_root_and_parts(repo_root, target, directory=False)
    fd = _open_directory(root)
    try:
        for component in parts[:-1]:
            next_fd = _open_child_directory(fd, component, create=create)
            os.close(fd)
            fd = next_fd
        yield fd, parts[-1]
    finally:
        os.close(fd)


def _ensure_unlinked_regular_file_descriptor(fd: int, target: Path) -> None:
    entry = os.fstat(fd)
    if not stat.S_ISREG(entry.st_mode):
        raise UnsafeGeneratedOutputPathError(
            f"generated output target is not a regular file: {target}"
        )
    if entry.st_nlink > 1:
        raise UnsafeGeneratedOutputPathError(
            f"hard-linked generated output is not permitted: {target}"
        )


def _replacement_target_mode(parent_fd: int, name: str, target: Path) -> tuple[int, bool]:
    """Return the replacement mode after rechecking the live final entry.

    A replacement never mutates the old inode.  This live check still rejects
    a link or non-file that appeared after mapping-level preflight, while the
    returned mode keeps ordinary replacement behavior compatible with
    ``Path.write_text`` for an existing generated file.
    """
    try:
        entry = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return 0o666, False
    except OSError as exc:
        raise UnsafeGeneratedOutputPathError(
            f"unable to inspect generated output for replacement: {target}: {exc}"
        ) from exc
    if stat.S_ISLNK(entry.st_mode):
        raise UnsafeGeneratedOutputPathError(
            f"symlinked generated output replacement target is not permitted: {target}"
        )
    if not stat.S_ISREG(entry.st_mode):
        raise UnsafeGeneratedOutputPathError(
            f"generated output replacement target is not a regular file: {target}"
        )
    if entry.st_nlink > 1:
        raise UnsafeGeneratedOutputPathError(
            f"hard-linked generated output replacement target is not permitted: {target}"
        )
    return stat.S_IMODE(entry.st_mode), True


def _new_staged_name() -> str:
    """Return an unguessable direct child name for one staged replacement."""
    return f".docxology-generated-{secrets.token_hex(16)}.tmp"


def _remove_staged_output(parent_fd: int, name: str) -> None:
    """Best-effort cleanup of a staging directory entry without path traversal."""
    try:
        os.unlink(name, dir_fd=parent_fd)
    except FileNotFoundError:
        return
    except OSError:
        # The primary output error is more useful than a cleanup failure.  The
        # stage has a random dotfile name and is never a published artifact.
        return


def _stage_text_replacement(
    parent_fd: int,
    content: str,
    *,
    mode: int,
    preserve_mode: bool,
    target: Path,
    encoding: str,
) -> tuple[str, tuple[int, int]]:
    """Write one new regular file in the already-open parent directory."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | _nofollow_flag()
    flags |= getattr(os, "O_NONBLOCK", 0)
    for _ in range(8):
        staged_name = _new_staged_name()
        try:
            fd = os.open(staged_name, flags, mode, dir_fd=parent_fd)
        except FileExistsError:
            # Cryptographic-name collisions are implausible, but retrying is
            # deterministic and avoids ever opening an existing staged file.
            continue
        except OSError as exc:
            raise UnsafeGeneratedOutputPathError(
                f"unable to stage generated output safely: {target}: {exc}"
            ) from exc
        try:
            _ensure_unlinked_regular_file_descriptor(fd, target)
            if preserve_mode:
                os.fchmod(fd, mode)
            with os.fdopen(fd, "w", encoding=encoding) as handle:
                fd = -1
                handle.write(content)
                handle.flush()
                os.fsync(handle.fileno())
            entry = os.stat(staged_name, dir_fd=parent_fd, follow_symlinks=False)
            if (
                stat.S_ISLNK(entry.st_mode)
                or not stat.S_ISREG(entry.st_mode)
                or entry.st_nlink > 1
            ):
                raise UnsafeGeneratedOutputPathError(
                    f"staged generated output is not a singly linked regular file: {target}"
                )
            return staged_name, (entry.st_dev, entry.st_ino)
        except BaseException:
            _remove_staged_output(parent_fd, staged_name)
            raise
        finally:
            if fd >= 0:
                os.close(fd)
    raise UnsafeGeneratedOutputPathError(
        f"unable to allocate a unique staged generated output for: {target}"
    )


def _replace_staged_output(
    parent_fd: int,
    staged_name: str,
    staged_identity: tuple[int, int],
    target_name: str,
    target: Path,
    *,
    _before_atomic_replace: Callable[[], None] | None = None,
) -> None:
    """Atomically install a verified staged file without mutating the old inode.

    ``_before_atomic_replace`` is an internal, deterministic interleaving seam
    for the real-filesystem regression test.  It runs only after the live
    target and staged inode have been checked, precisely where a concurrent
    process could otherwise add a hard-link alias to the old target.  Atomic
    replacement must leave that alias on the old inode rather than mutate it.
    """
    def verify_staged_output() -> None:
        try:
            staged = os.stat(staged_name, dir_fd=parent_fd, follow_symlinks=False)
        except OSError as exc:
            raise UnsafeGeneratedOutputPathError(
                f"unable to inspect staged generated output before replacement: {target}: {exc}"
            ) from exc
        if (
            (staged.st_dev, staged.st_ino) != staged_identity
            or stat.S_ISLNK(staged.st_mode)
            or not stat.S_ISREG(staged.st_mode)
            or staged.st_nlink > 1
        ):
            raise UnsafeGeneratedOutputPathError(
                f"staged generated output changed before replacement: {target}"
            )

    verify_staged_output()
    if os.rename not in os.supports_dir_fd:  # pragma: no cover - unsupported platforms
        raise UnsafeGeneratedOutputPathError(
            "platform lacks descriptor-relative atomic replacement; refusing generated-output write"
        )
    if _before_atomic_replace is not None:
        _before_atomic_replace()
        # The deterministic test seam must not weaken the staging contract.
        verify_staged_output()
    try:
        os.replace(
            staged_name,
            target_name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
    except (NotImplementedError, TypeError) as exc:  # pragma: no cover - unsupported platforms
        raise UnsafeGeneratedOutputPathError(
            "platform lacks descriptor-relative atomic replacement; refusing generated-output write"
        ) from exc
    except OSError as exc:
        raise UnsafeGeneratedOutputPathError(
            f"unable to replace generated output safely: {target}: {exc}"
        ) from exc


def read_generated_output_text(
    repo_root: Path,
    target: Path,
    *,
    encoding: str = "utf-8",
    errors: str | None = None,
) -> str | None:
    """Read a generated output safely, returning ``None`` only when missing."""
    candidate = safe_generated_output_path(repo_root, target)
    try:
        with _parent_directory_fd(repo_root, candidate, create=False) as (parent_fd, name):
            flags = os.O_RDONLY | _nofollow_flag() | getattr(os, "O_NONBLOCK", 0)
            try:
                fd = os.open(name, flags, dir_fd=parent_fd)
            except FileNotFoundError:
                return None
            except OSError as exc:
                raise UnsafeGeneratedOutputPathError(
                    f"unable to read generated output safely: {candidate}: {exc}"
                ) from exc
            try:
                _ensure_unlinked_regular_file_descriptor(fd, candidate)
                with os.fdopen(fd, "r", encoding=encoding, errors=errors) as handle:
                    fd = -1
                    return handle.read()
            finally:
                if fd >= 0:
                    os.close(fd)
    except FileNotFoundError:
        # A missing ancestor is equivalent to a missing generated output in
        # check mode.  Any symlink or non-directory ancestor already raises.
        return None


def write_generated_output_text(
    repo_root: Path,
    target: Path,
    content: str,
    *,
    encoding: str = "utf-8",
    _before_replace: Callable[[], None] | None = None,
    _before_atomic_replace: Callable[[], None] | None = None,
) -> None:
    """Atomically replace one repository-local generated text file safely.

    The old output inode is never truncated or otherwise mutated.  Therefore
    even a hard link added after validation remains an unchanged alias to the
    old content; the final output name atomically moves to a new staged inode.
    ``_before_replace`` and ``_before_atomic_replace`` are internal
    deterministic interleaving seams used by the real-filesystem hard-link
    regression tests.  The latter runs after the final target check, proving
    that a late alias cannot cause an external file to be mutated.
    """
    candidate = safe_generated_output_path(repo_root, target)
    with _parent_directory_fd(repo_root, candidate, create=True) as (parent_fd, name):
        mode, preserve_mode = _replacement_target_mode(parent_fd, name, candidate)
        staged_name: str | None = None
        try:
            staged_name, staged_identity = _stage_text_replacement(
                parent_fd,
                content,
                mode=mode,
                preserve_mode=preserve_mode,
                target=candidate,
                encoding=encoding,
            )
            if _before_replace is not None:
                _before_replace()
            # Recheck the live final entry after any external interleaving.
            # A hard link or symlink that appears here fails closed; a link
            # added immediately after this check remains harmless because the
            # atomic replacement never mutates the old inode.
            _replacement_target_mode(parent_fd, name, candidate)
            _replace_staged_output(
                parent_fd,
                staged_name,
                staged_identity,
                name,
                candidate,
                _before_atomic_replace=_before_atomic_replace,
            )
            staged_name = None
        finally:
            if staged_name is not None:
                _remove_staged_output(parent_fd, staged_name)


def remove_generated_output(repo_root: Path, target: Path) -> None:
    """Remove an explicitly owned generated output without following links."""
    candidate = safe_generated_output_path(repo_root, target)
    with _parent_directory_fd(repo_root, candidate, create=False) as (parent_fd, name):
        try:
            entry = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return
        except OSError as exc:
            raise UnsafeGeneratedOutputPathError(
                f"unable to inspect generated output for removal: {candidate}: {exc}"
            ) from exc
        if (
            stat.S_ISLNK(entry.st_mode)
            or not stat.S_ISREG(entry.st_mode)
            or entry.st_nlink > 1
        ):
            raise UnsafeGeneratedOutputPathError(
                "generated output removal target is not a singly linked regular file: "
                f"{candidate}"
            )
        try:
            os.unlink(name, dir_fd=parent_fd)
        except OSError as exc:
            raise UnsafeGeneratedOutputPathError(
                f"unable to remove generated output safely: {candidate}: {exc}"
            ) from exc


def generated_output_files(repo_root: Path, directory: Path, pattern: str) -> tuple[Path, ...]:
    """List real generated-output candidates, rejecting links before callers read.

    This intentionally does not claim ownership: callers remain responsible
    for their own markers/manifests and may leave hand-authored regular files
    untouched.  It only prevents a scan used by ``--check`` or explicit
    cleanup from following a symlinked directory or file.
    """
    if not generated_output_directory_exists(repo_root, directory):
        return ()
    candidate_dir = _lexical_absolute(directory)
    paths: list[Path] = []
    for path in candidate_dir.rglob(pattern):
        paths.append(safe_generated_output_path(repo_root, path))
    return tuple(sorted(paths, key=lambda path: path.as_posix()))


def stable_generated_output_timestamp(
    repo_root: Path, target: Path, payload: Mapping[str, object]
) -> str | None:
    """Reuse an unchanged generated payload timestamp through the safe reader.

    Several renderers intentionally retain ``generated_at`` when their JSON
    body is byte-for-byte semantically unchanged.  They must not use an
    ordinary ``Path.read_text`` for that optimization, because it executes in
    write mode immediately before the output is rewritten.
    """
    content = read_generated_output_text(repo_root, target)
    if content is None:
        return None
    try:
        existing = json.loads(content)
    except json.JSONDecodeError:
        return None
    if not isinstance(existing, dict):
        return None
    current_body = {key: value for key, value in payload.items() if key != "generated_at"}
    existing_body = {key: value for key, value in existing.items() if key != "generated_at"}
    timestamp = existing.get("generated_at")
    return str(timestamp) if current_body == existing_body and timestamp else None


def output_drift(
    expected: Mapping[Path, str], observed: Mapping[Path, str | None]
) -> tuple[Path, ...]:
    """Return every target whose observed text is absent or differs exactly.

    This is pure: callers provide both the source-rendered expected values and
    the on-disk observations.  Target iteration follows ``expected`` order so
    CLI failures remain deterministic and concise.
    """
    return tuple(
        path
        for path, expected_text in expected.items()
        if observed.get(path) != expected_text
    )


def read_output_texts(
    paths: Mapping[Path, str], *, repo_root: Path
) -> dict[Path, str | None]:
    """Read candidate generated outputs, representing a missing file as ``None``."""
    # Reject the complete target set before opening even the first output.
    # This keeps a malformed multi-output check from quietly inspecting a
    # partial set while another target already violates the release boundary.
    for path in paths:
        safe_generated_output_path(repo_root, path)
    observed: dict[Path, str | None] = {}
    for path in paths:
        observed[path] = read_generated_output_text(repo_root, path)
    return observed


def stale_output_paths(
    expected: Mapping[Path, str], *, repo_root: Path
) -> tuple[Path, ...]:
    """Return source-rendered targets that do not exactly match on disk."""
    return output_drift(expected, read_output_texts(expected, repo_root=repo_root))


def write_output_texts(outputs: Mapping[Path, str], *, repo_root: Path) -> None:
    """Write a complete rendered-output mapping using UTF-8 text files."""
    # Validate every output first so a bad later target cannot leave an
    # earlier generated file partially refreshed.  Individual writes repeat
    # descriptor-relative validation to protect against a path-swap race.
    for path in outputs:
        safe_generated_output_path(repo_root, path)
    for path, content in outputs.items():
        write_generated_output_text(repo_root, path, content)
