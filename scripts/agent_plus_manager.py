#!/usr/bin/env python3
"""Manage Agent+ installations through one descriptor-anchored transaction workspace."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import stat
import subprocess
import sys
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from types import TracebackType
from typing import Any, Literal, Self

SCHEMA = "agent-plus-install/v1"
TRANSACTION_SCHEMA = "agent-plus-upgrade-transaction/v2"
JOURNAL_NAME = "upgrade-transaction.json"
JOURNAL_PENDING_NAME = "upgrade-transaction.pending"
SOURCE_REPOSITORY = "https://github.com/traftonobrien/agent-plus"
ALLOWED_PROFILES = frozenset({"research", "product", "scouting"})
MANIFEST_KEYS = frozenset(
    {"schema_version", "agent_plus_version", "profile", "source_repository", "managed_files"}
)
JOURNAL_KEYS = frozenset(
    {
        "schema_version",
        "transaction_id",
        "profile",
        "state",
        "managed_files",
        "recovery_files",
        "recovery_digests",
        "candidate_managed_files",
        "candidate_version",
        "prior_manifest_sha256",
        "candidate_manifest_sha256",
        "snapshot_complete",
        "stage_complete",
        "commit_files",
        "committed_files",
        "restored_files",
        "last_error",
    }
)
SNAPSHOT_REQUIRED_STATES = frozenset(
    {"STAGING", "READY", "COMMITTING", "RECOVERY_REQUIRED", "RECOVERING", "COMMITTED", "RECOVERED"}
)


class ManagerError(RuntimeError):
    """Expected, user-actionable filesystem, integrity, or concurrency failure."""


def _source_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _managed_sources(source: Path, profile: str) -> dict[str, Path]:
    if profile not in ALLOWED_PROFILES:
        raise ManagerError(f"Unknown profile: {profile}")
    base = source / "bootstrap" / "base"
    return {
        "AGENTS.md": base / "AGENTS.md",
        "CLAUDE.md": base / "CLAUDE.md",
        "AI_WORKFLOW.md": base / "AI_WORKFLOW.md",
        "AI_AGENT_OUTPUT_POLICY.md": base / "AI_AGENT_OUTPUT_POLICY.md",
        "ESSENTIAL_WORK_PROTOCOL.md": base / "ESSENTIAL_WORK_PROTOCOL.md",
        ".cursor/rules/agent-plus-output.mdc": base / ".cursor" / "rules" / "agent-plus-output.mdc",
        ".agent-plus/PROFILE.md": source / "bootstrap" / "profiles" / profile / "PROFILE.md",
        ".planning/templates/ESSENTIAL-TASK.md": base / ".planning" / "templates" / "ESSENTIAL-TASK.md",
        "scripts/ai-context.sh": base / "scripts" / "ai-context.sh",
        "scripts/anti_loop_guard.py": base / "scripts" / "anti_loop_guard.py",
        "scripts/interface_consumer_guard.py": base / "scripts" / "interface_consumer_guard.py",
        "scripts/agent-plus-doctor.sh": source / "scripts" / "agent-plus-doctor.sh",
        "tests/test_interface_consumer_guard.py": base / "tests" / "test_interface_consumer_guard.py",
    }


def _require_platform() -> None:
    required = (os.open, os.mkdir, os.rename, os.unlink, os.stat, os.rmdir)
    if os.name != "posix" or not all(function in os.supports_dir_fd for function in required):
        raise ManagerError(
            "Agent+ transaction filesystem requires POSIX descriptor-relative operations"
        )
    if not hasattr(os, "O_NOFOLLOW") or not hasattr(os, "O_DIRECTORY"):
        raise ManagerError("Agent+ transaction filesystem requires O_NOFOLLOW and O_DIRECTORY")


def _safe_parts(relative: str) -> list[str]:
    if type(relative) is not str or not relative:
        raise ManagerError("Relative transaction path is invalid")
    path = PurePosixPath(relative)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ManagerError(f"Unsafe relative transaction path: {relative}")
    return list(path.parts)


def _os_failure(action: str, exc: OSError) -> ManagerError:
    return ManagerError(f"{action}: {exc.strerror or exc}")


def _fsync(fd: int, action: str) -> None:
    try:
        os.fsync(fd)
    except OSError as exc:
        raise _os_failure(action, exc) from exc


def _open_root(path: Path, label: str) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(path, flags)
        details = os.fstat(fd)
    except OSError as exc:
        raise _os_failure(f"Cannot open {label} root", exc) from exc
    if not stat.S_ISDIR(details.st_mode):
        os.close(fd)
        raise ManagerError(f"{label} root is not a directory")
    return fd


def _open_dir_at(parent_fd: int, name: str, *, create: bool = False) -> int:
    _safe_parts(name)
    if "/" in name:
        raise ManagerError(f"Directory component is not singular: {name}")
    if create:
        try:
            os.mkdir(name, dir_fd=parent_fd)
        except FileExistsError:
            pass
        except OSError as exc:
            raise _os_failure(f"Cannot create directory {name}", exc) from exc
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    try:
        fd = os.open(name, flags, dir_fd=parent_fd)
        details = os.fstat(fd)
    except OSError as exc:
        raise _os_failure(f"Cannot securely open directory {name}", exc) from exc
    if not stat.S_ISDIR(details.st_mode):
        os.close(fd)
        raise ManagerError(f"Directory component is not a directory: {name}")
    return fd


def _walk_dir(root_fd: int, relative: str, *, create: bool = False) -> int:
    parts = _safe_parts(relative)
    current = os.dup(root_fd)
    try:
        for part in parts:
            next_fd = _open_dir_at(current, part, create=create)
            os.close(current)
            current = next_fd
        return current
    except (ManagerError, OSError):
        os.close(current)
        raise


def _walk_parent(root_fd: int, relative: str, *, create: bool = False) -> tuple[int, str]:
    parts = _safe_parts(relative)
    leaf = parts.pop()
    current = os.dup(root_fd)
    try:
        for part in parts:
            next_fd = _open_dir_at(current, part, create=create)
            os.close(current)
            current = next_fd
        return current, leaf
    except (ManagerError, OSError):
        os.close(current)
        raise


def _open_regular(parent_fd: int, name: str, *, writable: bool = False, create: bool = False) -> int:
    _safe_parts(name)
    if "/" in name:
        raise ManagerError(f"File component is not singular: {name}")
    flags = (os.O_RDWR if writable else os.O_RDONLY) | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
    if create:
        flags |= os.O_CREAT | os.O_EXCL
    try:
        fd = os.open(name, flags, 0o644, dir_fd=parent_fd) if create else os.open(name, flags, dir_fd=parent_fd)
        details = os.fstat(fd)
    except OSError as exc:
        raise _os_failure(f"Cannot securely open file {name}", exc) from exc
    if not stat.S_ISREG(details.st_mode):
        os.close(fd)
        raise ManagerError(f"Expected regular file: {name}")
    return fd


def _read_fd(fd: int, label: str) -> bytes:
    chunks: list[bytes] = []
    try:
        while True:
            chunk = os.read(fd, 1024 * 1024)
            if not chunk:
                return b"".join(chunks)
            chunks.append(chunk)
    except OSError as exc:
        raise _os_failure(f"Cannot read {label}", exc) from exc


def _write_all(fd: int, data: bytes, label: str) -> None:
    offset = 0
    try:
        while offset < len(data):
            offset += os.write(fd, data[offset:])
    except OSError as exc:
        raise _os_failure(f"Cannot write {label}", exc) from exc


def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hash_fd(fd: int, label: str) -> str:
    try:
        os.lseek(fd, 0, os.SEEK_SET)
    except OSError as exc:
        raise _os_failure(f"Cannot seek {label}", exc) from exc
    return _hash_bytes(_read_fd(fd, label))


def _check_destination_leaf(parent_fd: int, name: str, phase: str) -> None:
    try:
        details = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    except OSError as exc:
        raise _os_failure(f"Cannot inspect {phase} destination {name}", exc) from exc
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
        raise ManagerError(f"Unsafe {phase} destination: {name}")


def _copy_fd_to_atomic_destination(
    source_fd: int,
    destination_parent_fd: int,
    destination_name: str,
    expected: str | None,
    phase: str,
) -> str:
    source_details = os.fstat(source_fd)
    if not stat.S_ISREG(source_details.st_mode):
        raise ManagerError(f"{phase} source is not a regular file")
    temporary = f".agent-plus-{uuid.uuid4().hex}.tmp"
    output_fd: int | None = None
    try:
        output_fd = _open_regular(destination_parent_fd, temporary, writable=True, create=True)
        try:
            os.lseek(source_fd, 0, os.SEEK_SET)
        except OSError as exc:
            raise _os_failure(f"Cannot seek {phase} source", exc) from exc
        digest = hashlib.sha256()
        while True:
            try:
                chunk = os.read(source_fd, 1024 * 1024)
            except OSError as exc:
                raise _os_failure(f"Cannot read {phase} source", exc) from exc
            if not chunk:
                break
            digest.update(chunk)
            _write_all(output_fd, chunk, f"{phase} temporary")
        actual = digest.hexdigest()
        if expected is not None and actual != expected:
            raise ManagerError(f"{phase} source integrity mismatch: {destination_name}")
        _fsync(output_fd, f"{phase} temporary")
        _check_destination_leaf(destination_parent_fd, destination_name, phase)
        try:
            os.rename(
                temporary,
                destination_name,
                src_dir_fd=destination_parent_fd,
                dst_dir_fd=destination_parent_fd,
            )
        except OSError as exc:
            raise _os_failure(f"Cannot atomically {phase} {destination_name}", exc) from exc
        _fsync(destination_parent_fd, f"{phase} destination directory")
        return actual
    finally:
        if output_fd is not None:
            os.close(output_fd)
        try:
            os.unlink(temporary, dir_fd=destination_parent_fd)
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise _os_failure(f"Cannot remove {phase} temporary", exc) from exc


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ManagerError("Duplicate JSON object key")
        result[key] = value
    return result


class TransactionFilesystem:
    """One command-lifetime boundary for all transaction and target I/O."""

    def __init__(self, target: Path) -> None:
        _require_platform()
        try:
            self.target_path = target.expanduser().resolve(strict=True)
            self.source_path = _source_root().resolve(strict=True)
        except OSError as exc:
            raise _os_failure("Cannot resolve Agent+ filesystem root", exc) from exc
        self.target_fd = _open_root(self.target_path, "target")
        try:
            self.source_fd = _open_root(self.source_path, "source")
        except (ManagerError, OSError):
            os.close(self.target_fd)
            raise
        self.agent_fd: int | None = None

    def close(self) -> None:
        if self.agent_fd is not None:
            os.close(self.agent_fd)
            self.agent_fd = None
        os.close(self.source_fd)
        os.close(self.target_fd)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        self.close()

    def open_agent(self, *, create: bool = False) -> int:
        if self.agent_fd is None:
            self.agent_fd = _open_dir_at(self.target_fd, ".agent-plus", create=create)
        return self.agent_fd

    def target_parent(self, relative: str, *, create: bool = False) -> tuple[int, str]:
        return _walk_parent(self.target_fd, relative, create=create)

    def target_file(self, relative: str) -> int:
        parent, leaf = _walk_parent(self.target_fd, relative)
        try:
            return _open_regular(parent, leaf)
        finally:
            os.close(parent)

    def source_relative(self, source: Path) -> str:
        try:
            return source.relative_to(self.source_path).as_posix()
        except ValueError as exc:
            raise ManagerError(f"Canonical source escapes source root: {source}") from exc

    def source_file(self, source: Path) -> int:
        parent, leaf = _walk_parent(self.source_fd, self.source_relative(source))
        try:
            return _open_regular(parent, leaf)
        finally:
            os.close(parent)

    def workspace(self, transaction_id: str, *, create: bool = False) -> TransactionWorkspace:
        _safe_parts(transaction_id)
        agent_fd = self.open_agent()
        transactions_fd = _open_dir_at(agent_fd, ".transactions", create=create)
        try:
            root_fd = _open_dir_at(transactions_fd, transaction_id, create=create)
        finally:
            os.close(transactions_fd)
        snapshot_fd: int | None = None
        try:
            snapshot_fd = _open_dir_at(root_fd, "snapshot", create=create)
            stage_fd = _open_dir_at(root_fd, "stage", create=create)
        except (ManagerError, OSError):
            if snapshot_fd is not None:
                os.close(snapshot_fd)
            os.close(root_fd)
            raise
        return TransactionWorkspace(self, transaction_id, root_fd, snapshot_fd, stage_fd)

    def transaction_parent(self) -> int:
        return _open_dir_at(self.open_agent(), ".transactions", create=True)

    def transaction_workspace_exists(self, transaction_id: str) -> bool:
        _safe_parts(transaction_id)
        transactions_fd = self.transaction_parent()
        try:
            try:
                details = os.stat(transaction_id, dir_fd=transactions_fd, follow_symlinks=False)
            except FileNotFoundError:
                return False
            except OSError as exc:
                raise _os_failure("Cannot inspect transaction workspace", exc) from exc
            if stat.S_ISLNK(details.st_mode) or not stat.S_ISDIR(details.st_mode):
                raise ManagerError("Transaction workspace is not a directory")
            return True
        finally:
            os.close(transactions_fd)

    def _journal_entry_exists(self, name: str, label: str) -> bool:
        try:
            details = os.stat(name, dir_fd=self.open_agent(), follow_symlinks=False)
        except FileNotFoundError:
            return False
        except OSError as exc:
            raise _os_failure(f"Cannot inspect {label}", exc) from exc
        if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
            raise ManagerError(f"{label.capitalize()} is not a regular file")
        return True

    def journal_bytes(self) -> bytes:
        fd = _open_regular(self.open_agent(), JOURNAL_NAME)
        try:
            return _read_fd(fd, "transaction journal")
        finally:
            os.close(fd)

    def journal_exists(self) -> bool:
        return self._journal_entry_exists(JOURNAL_NAME, "transaction journal")

    def transaction_record_exists(self) -> bool:
        journal = self.journal_exists()
        pending = self._journal_entry_exists(JOURNAL_PENDING_NAME, "pending transaction journal")
        return journal or pending

    def prepare_journal_recovery(self) -> bool:
        journal = self.journal_exists()
        pending = self._journal_entry_exists(JOURNAL_PENDING_NAME, "pending transaction journal")
        if pending:
            try:
                os.unlink(JOURNAL_PENDING_NAME, dir_fd=self.open_agent())
                _fsync(self.open_agent(), "pending transaction journal directory")
            except OSError as exc:
                raise _os_failure("Cannot remove pending transaction journal", exc) from exc
        return journal

    def write_journal(self, journal: dict[str, Any]) -> None:
        data = json.dumps(journal, indent=2, sort_keys=True) + "\n"
        _publish_journal_at(self.open_agent(), data.encode())

    def remove_journal(self) -> None:
        try:
            os.unlink(JOURNAL_NAME, dir_fd=self.open_agent())
            _fsync(self.open_agent(), "transaction journal directory")
        except FileNotFoundError:
            return
        except OSError as exc:
            raise _os_failure("Cannot remove transaction journal", exc) from exc

    @contextmanager
    def lock(self, *, allow_stale: bool) -> Iterator[None]:
        """Hold one kernel-owned lease without deleting a shared lock path."""
        del allow_stale
        agent_fd = self.open_agent()
        token = uuid.uuid4().hex
        name = "upgrade.lock"
        flags = os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | getattr(os, "O_CLOEXEC", 0)
        try:
            lock_fd = os.open(name, flags, 0o600, dir_fd=agent_fd)
            details = os.fstat(lock_fd)
            if not stat.S_ISREG(details.st_mode):
                raise ManagerError("Agent+ lock is not a regular file")
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            if "lock_fd" in locals():
                os.close(lock_fd)
            raise ManagerError("Another Agent+ upgrade or recover is in progress") from exc
        except ManagerError:
            if "lock_fd" in locals():
                os.close(lock_fd)
            raise
        except OSError as exc:
            if "lock_fd" in locals():
                os.close(lock_fd)
            raise _os_failure("Cannot acquire Agent+ lock", exc) from exc
        try:
            os.ftruncate(lock_fd, 0)
            os.lseek(lock_fd, 0, os.SEEK_SET)
            _write_all(lock_fd, f"{os.getpid()}:{token}\n".encode("ascii"), "upgrade lock")
            _fsync(lock_fd, "upgrade lock")
            _fsync(agent_fd, "upgrade lock directory")
            yield
        finally:
            try:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            except OSError as exc:
                raise _os_failure("Cannot release Agent+ lock", exc) from exc
            finally:
                os.close(lock_fd)


class TransactionWorkspace:
    def __init__(self, filesystem: TransactionFilesystem, transaction_id: str, root_fd: int, snapshot_fd: int, stage_fd: int) -> None:
        self.filesystem = filesystem
        self.transaction_id = transaction_id
        self.root_fd = root_fd
        self.snapshot_fd = snapshot_fd
        self.stage_fd = stage_fd

    def close(self) -> None:
        os.close(self.snapshot_fd)
        os.close(self.stage_fd)
        os.close(self.root_fd)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: TracebackType | None) -> None:
        self.close()

    def parent(self, area: str, relative: str, *, create: bool = False) -> tuple[int, str]:
        root = self.snapshot_fd if area == "snapshot" else self.stage_fd
        return _walk_parent(root, relative, create=create)

    def source_file(self, area: str, relative: str) -> int:
        root = self.snapshot_fd if area == "snapshot" else self.stage_fd
        parent, leaf = _walk_parent(root, relative)
        try:
            return _open_regular(parent, leaf)
        finally:
            os.close(parent)


def _atomic_write_json_at(parent_fd: int, name: str, data: bytes) -> None:
    temporary = f".{name}.{uuid.uuid4().hex}.tmp"
    fd: int | None = None
    try:
        fd = _open_regular(parent_fd, temporary, writable=True, create=True)
        _write_all(fd, data, name)
        _fsync(fd, name)
        try:
            existing = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        except OSError as exc:
            raise _os_failure(f"Cannot inspect {name}", exc) from exc
        if existing is not None and (stat.S_ISLNK(existing.st_mode) or not stat.S_ISREG(existing.st_mode)):
            raise ManagerError(f"Unsafe atomic JSON destination: {name}")
        try:
            os.rename(temporary, name, src_dir_fd=parent_fd, dst_dir_fd=parent_fd)
        except OSError as exc:
            raise _os_failure(f"Cannot commit atomic JSON {name}", exc) from exc
        _fsync(parent_fd, name)
    finally:
        if fd is not None:
            os.close(fd)
        try:
            os.unlink(temporary, dir_fd=parent_fd)
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise _os_failure(f"Cannot remove temporary JSON {name}", exc) from exc


def _publish_journal_at(parent_fd: int, data: bytes) -> None:
    """Publish one journal through a fixed, discoverable pending file."""
    fd: int | None = None
    created = False
    try:
        fd = _open_regular(parent_fd, JOURNAL_PENDING_NAME, writable=True, create=True)
        created = True
        _write_all(fd, data, JOURNAL_NAME)
        _fsync(fd, JOURNAL_NAME)
        try:
            existing = os.stat(JOURNAL_NAME, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            existing = None
        except OSError as exc:
            raise _os_failure(f"Cannot inspect {JOURNAL_NAME}", exc) from exc
        if existing is not None and (
            stat.S_ISLNK(existing.st_mode) or not stat.S_ISREG(existing.st_mode)
        ):
            raise ManagerError(f"Unsafe journal destination: {JOURNAL_NAME}")
        try:
            os.rename(
                JOURNAL_PENDING_NAME,
                JOURNAL_NAME,
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
            )
        except OSError as exc:
            raise _os_failure("Cannot publish transaction journal", exc) from exc
        _fsync(parent_fd, "transaction journal directory")
    finally:
        if fd is not None:
            os.close(fd)
        if created:
            try:
                os.unlink(JOURNAL_PENDING_NAME, dir_fd=parent_fd)
            except FileNotFoundError:
                pass
            except OSError as exc:
                raise _os_failure("Cannot remove pending transaction journal", exc) from exc


def _read_json(data: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ManagerError) as exc:
        raise ManagerError(f"Invalid {label}") from exc
    if type(value) is not dict:
        raise ManagerError(f"Invalid {label}")
    return value


def _manifest(fs: TransactionFilesystem) -> dict[str, Any]:
    data = _read_json(_read_target(fs, ".agent-plus/install-manifest.json"), "install manifest")
    if set(data) != MANIFEST_KEYS or data.get("schema_version") != SCHEMA:
        raise ManagerError("Unsupported Agent+ install manifest")
    profile = data.get("profile")
    if type(profile) is not str or profile not in ALLOWED_PROFILES:
        raise ManagerError("Invalid Agent+ install profile")
    if data.get("source_repository") != SOURCE_REPOSITORY:
        raise ManagerError("Invalid Agent+ source identity")
    managed = data.get("managed_files")
    if type(managed) is not dict or set(managed) != set(_managed_sources(fs.source_path, profile)):
        raise ManagerError("Managed-file set does not match the Agent+ release")
    for relative, digest in managed.items():
        if not _safe_manifest_entry(relative, digest):
            raise ManagerError("Invalid managed-file entry")
    return data


def _safe_manifest_entry(relative: Any, digest: Any) -> bool:
    if type(relative) is not str or type(digest) is not str:
        return False
    try:
        _safe_parts(relative)
    except ManagerError:
        return False
    return len(digest) == 64 and all(character in "0123456789abcdef" for character in digest)


def _read_target(fs: TransactionFilesystem, relative: str) -> bytes:
    fd = fs.target_file(relative)
    try:
        return _read_fd(fd, relative)
    finally:
        os.close(fd)


def _target_digest(fs: TransactionFilesystem, relative: str) -> str:
    fd = fs.target_file(relative)
    try:
        return _hash_fd(fd, relative)
    finally:
        os.close(fd)


def _manifest_data(fs: TransactionFilesystem, profile: str) -> dict[str, Any]:
    sources = _managed_sources(fs.source_path, profile)
    hashes: dict[str, str] = {}
    for relative, source in sorted(sources.items()):
        source_fd = fs.source_file(source)
        try:
            hashes[relative] = _hash_fd(source_fd, f"canonical {relative}")
        finally:
            os.close(source_fd)
    return {
        "schema_version": SCHEMA,
        "agent_plus_version": _version_from_fs(fs),
        "profile": profile,
        "source_repository": SOURCE_REPOSITORY,
        "managed_files": hashes,
    }


def _version_from_fs(fs: TransactionFilesystem) -> str:
    source = fs.source_file(fs.source_path / "VERSION")
    try:
        value = _read_fd(source, "canonical VERSION").decode("utf-8").strip()
    except UnicodeDecodeError as exc:
        raise ManagerError("VERSION is not valid UTF-8") from exc
    finally:
        os.close(source)
    if not value or any(character.isspace() for character in value):
        raise ManagerError("VERSION must contain one non-empty token")
    return value


def _write_manifest_at(fs: TransactionFilesystem, parent_fd: int, profile: str) -> dict[str, Any]:
    value = _manifest_data(fs, profile)
    _atomic_write_json_at(parent_fd, "install-manifest.json", (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())
    return value


def _record_manifest_data(fs: TransactionFilesystem, profile: str) -> dict[str, Any]:
    sources = _managed_sources(fs.source_path, profile)
    hashes: dict[str, str] = {}
    for relative in sorted(sources):
        hashes[relative] = _target_digest(fs, relative)
    return {
        "schema_version": SCHEMA,
        "agent_plus_version": _version_from_fs(fs),
        "profile": profile,
        "source_repository": SOURCE_REPOSITORY,
        "managed_files": hashes,
    }


def _drift(fs: TransactionFilesystem, manifest: dict[str, Any]) -> list[str]:
    drift: list[str] = []
    managed = manifest["managed_files"]
    for relative, expected in sorted(managed.items()):
        try:
            actual = _target_digest(fs, relative)
        except ManagerError:
            drift.append(f"missing:{relative}")
        else:
            if actual != expected:
                drift.append(f"modified:{relative}")
    return drift


def _copy_for_upgrade(
    source_fd: int,
    destination_parent_fd: int,
    destination_name: str,
    phase: str,
    expected: str | None = None,
) -> str:
    return _copy_fd_to_atomic_destination(source_fd, destination_parent_fd, destination_name, expected, phase)


def _replace_for_upgrade(
    source_fd: int,
    destination_parent_fd: int,
    destination_name: str,
    phase: str,
    expected: str | None = None,
) -> str:
    """Copy candidate bytes into a target-parent temp and rename within that handle."""
    return _copy_fd_to_atomic_destination(source_fd, destination_parent_fd, destination_name, expected, phase)


def _copy_to_atomic_restore(
    source_fd: int,
    destination_parent_fd: int,
    destination_name: str,
    expected: str,
) -> str:
    return _copy_fd_to_atomic_destination(source_fd, destination_parent_fd, destination_name, expected, "recovery")


def _journal_base(transaction_id: str, profile: str, managed: dict[str, str]) -> dict[str, Any]:
    commit_files = [*sorted(managed), ".agent-plus/install-manifest.json"]
    return {
        "schema_version": TRANSACTION_SCHEMA,
        "transaction_id": transaction_id,
        "profile": profile,
        "state": "SNAPSHOTTING",
        "managed_files": sorted(managed),
        "recovery_files": sorted([*managed, ".agent-plus/install-manifest.json"]),
        "recovery_digests": {},
        "candidate_managed_files": {},
        "candidate_version": "",
        "prior_manifest_sha256": "",
        "candidate_manifest_sha256": "",
        "snapshot_complete": False,
        "stage_complete": False,
        "commit_files": commit_files,
        "committed_files": [],
        "restored_files": [],
        "last_error": "",
    }


def _validate_journal(value: dict[str, Any]) -> dict[str, Any]:
    if set(value) != JOURNAL_KEYS or value.get("schema_version") != TRANSACTION_SCHEMA:
        raise ManagerError("Invalid Agent+ transaction journal")
    if type(value.get("transaction_id")) is not str:
        raise ManagerError("Invalid transaction identifier")
    _safe_parts(value["transaction_id"])
    if value.get("profile") not in ALLOWED_PROFILES:
        raise ManagerError("Invalid transaction profile")
    if value.get("state") not in {"SNAPSHOTTING", "STAGING", "READY", "COMMITTING", "RECOVERY_REQUIRED", "RECOVERING", "COMMITTED", "RECOVERED", "ABORTED"}:
        raise ManagerError("Invalid transaction state")
    for key in (
        "managed_files",
        "recovery_files",
        "commit_files",
        "committed_files",
        "restored_files",
    ):
        if type(value.get(key)) is not list or not all(type(item) is str for item in value[key]):
            raise ManagerError("Invalid transaction path list")
        for item in value[key]:
            _safe_parts(item)
        if len(value[key]) != len(set(value[key])):
            raise ManagerError("Transaction path list contains duplicates")
    for key in ("recovery_digests", "candidate_managed_files"):
        if type(value.get(key)) is not dict:
            raise ManagerError("Invalid transaction digest map")
        for relative, digest in value[key].items():
            if not _safe_manifest_entry(relative, digest):
                raise ManagerError("Invalid transaction digest entry")
    for key in ("snapshot_complete", "stage_complete"):
        if type(value.get(key)) is not bool:
            raise ManagerError("Invalid transaction completion flag")
    for key in ("candidate_version", "prior_manifest_sha256", "candidate_manifest_sha256", "last_error"):
        if type(value.get(key)) is not str:
            raise ManagerError("Invalid transaction metadata")
    managed_files = value["managed_files"]
    expected_recovery = sorted([*managed_files, ".agent-plus/install-manifest.json"])
    if managed_files != sorted(managed_files) or value["recovery_files"] != expected_recovery:
        raise ManagerError("Transaction recovery set is not exact")
    expected_commit = [*managed_files, ".agent-plus/install-manifest.json"]
    if value["commit_files"] != expected_commit:
        raise ManagerError("Transaction commit set is not exact")
    if value["committed_files"] != value["commit_files"][: len(value["committed_files"])]:
        raise ManagerError("Transaction commit progress is invalid")
    if value["restored_files"] != value["recovery_files"][: len(value["restored_files"])]:
        raise ManagerError("Transaction recovery progress is invalid")
    recovery_keys = set(value["recovery_digests"])
    if value["snapshot_complete"]:
        if recovery_keys != set(value["recovery_files"]):
            raise ManagerError("Transaction recovery digests are incomplete")
        if not _safe_manifest_entry(
            ".agent-plus/install-manifest.json", value["prior_manifest_sha256"]
        ):
            raise ManagerError("Transaction prior manifest digest is invalid")
    elif recovery_keys or value["prior_manifest_sha256"]:
        raise ManagerError("Incomplete snapshot contains recovery authority")
    candidate_keys = set(value["candidate_managed_files"])
    if value["stage_complete"]:
        if candidate_keys != set(managed_files):
            raise ManagerError("Transaction candidate set is not exact")
        if not value["candidate_version"] or any(
            character.isspace() for character in value["candidate_version"]
        ):
            raise ManagerError("Transaction candidate version is invalid")
        if not _safe_manifest_entry(
            ".agent-plus/install-manifest.json", value["candidate_manifest_sha256"]
        ):
            raise ManagerError("Transaction candidate manifest digest is invalid")
    elif candidate_keys or value["candidate_version"] or value["candidate_manifest_sha256"]:
        raise ManagerError("Incomplete stage contains candidate authority")
    if value["state"] in SNAPSHOT_REQUIRED_STATES and not value["snapshot_complete"]:
        raise ManagerError("Transaction state requires a complete snapshot")
    if value["state"] == "COMMITTED" and value["committed_files"] != value["commit_files"]:
        raise ManagerError("Committed transaction has incomplete progress")
    if value["state"] == "RECOVERED" and value["restored_files"] != value["recovery_files"]:
        raise ManagerError("Recovered transaction has incomplete progress")
    return value


def _load_journal(fs: TransactionFilesystem) -> dict[str, Any]:
    journal = _validate_journal(_read_json(fs.journal_bytes(), "transaction journal"))
    expected = sorted(_managed_sources(fs.source_path, journal["profile"]))
    if journal["managed_files"] != expected:
        raise ManagerError("Transaction managed-file set does not match the Agent+ release")
    return journal


def _restart_action(
    journal: dict[str, Any],
) -> Literal["abort", "verify_commit", "verify_recovery", "cleanup", "restore"]:
    """Map each valid durable journal to one restart action."""
    if not journal["snapshot_complete"]:
        return "abort"
    if journal["state"] == "COMMITTED":
        return "verify_commit"
    if journal["state"] == "RECOVERED":
        return "verify_recovery"
    if journal["state"] == "ABORTED":
        return "cleanup"
    return "restore"


def _set_state(fs: TransactionFilesystem, journal: dict[str, Any], state: str, error: str = "") -> None:
    journal["state"] = state
    journal["last_error"] = error
    fs.write_journal(journal)


def _close_workspace(workspace: TransactionWorkspace) -> None:
    workspace.close()


def _remove_tree_at(parent_fd: int, name: str) -> None:
    child_fd = _open_dir_at(parent_fd, name)
    try:
        _validate_tree_fd(child_fd, name)
        try:
            entries = os.listdir(child_fd)
        except OSError as exc:
            raise _os_failure(f"Cannot list transaction workspace {name}", exc) from exc
        for entry in entries:
            try:
                details = os.stat(entry, dir_fd=child_fd, follow_symlinks=False)
            except OSError as exc:
                raise _os_failure(f"Cannot inspect transaction workspace entry {entry}", exc) from exc
            if stat.S_ISLNK(details.st_mode):
                raise ManagerError(f"Transaction workspace contains symlink: {entry}")
            if stat.S_ISDIR(details.st_mode):
                _remove_tree_at(child_fd, entry)
            elif stat.S_ISREG(details.st_mode):
                try:
                    os.unlink(entry, dir_fd=child_fd)
                except OSError as exc:
                    raise _os_failure(f"Cannot remove transaction workspace entry {entry}", exc) from exc
            else:
                raise ManagerError(f"Unsupported transaction workspace entry: {entry}")
        _fsync(child_fd, f"transaction workspace {name}")
    finally:
        os.close(child_fd)
    try:
        os.rmdir(name, dir_fd=parent_fd)
        _fsync(parent_fd, "transaction workspace directory")
    except OSError as exc:
        raise _os_failure(f"Cannot remove transaction workspace {name}", exc) from exc


def _validate_tree_fd(directory_fd: int, label: str) -> None:
    try:
        entries = os.listdir(directory_fd)
    except OSError as exc:
        raise _os_failure(f"Cannot inspect transaction workspace {label}", exc) from exc
    for entry in entries:
        try:
            details = os.stat(entry, dir_fd=directory_fd, follow_symlinks=False)
        except OSError as exc:
            raise _os_failure(f"Cannot inspect transaction workspace entry {entry}", exc) from exc
        if stat.S_ISLNK(details.st_mode):
            raise ManagerError(f"Transaction workspace contains symlink: {entry}")
        if stat.S_ISDIR(details.st_mode):
            child_fd = _open_dir_at(directory_fd, entry)
            try:
                _validate_tree_fd(child_fd, entry)
            finally:
                os.close(child_fd)
        elif not stat.S_ISREG(details.st_mode):
            raise ManagerError(f"Unsupported transaction workspace entry: {entry}")


def _cleanup_workspace(fs: TransactionFilesystem, transaction_id: str) -> None:
    transactions_fd = fs.transaction_parent()
    try:
        _remove_tree_at(transactions_fd, transaction_id)
    finally:
        os.close(transactions_fd)


def _copy_snapshot(fs: TransactionFilesystem, workspace: TransactionWorkspace, journal: dict[str, Any], manifest: dict[str, Any]) -> None:
    digests: dict[str, str] = {}
    for relative in journal["recovery_files"]:
        source_fd = fs.target_file(relative)
        try:
            expected = manifest["managed_files"].get(relative) if relative != ".agent-plus/install-manifest.json" else _hash_fd(source_fd, relative)
            actual = _hash_fd(source_fd, relative)
            if expected is not None and actual != expected:
                raise ManagerError(f"Snapshot source changed: {relative}")
            parent, leaf = workspace.parent("snapshot", relative, create=True)
            try:
                _copy_for_upgrade(source_fd, parent, leaf, "snapshot", actual)
            finally:
                os.close(parent)
            digests[relative] = actual
        finally:
            os.close(source_fd)
    journal["recovery_digests"] = digests
    journal["prior_manifest_sha256"] = digests[".agent-plus/install-manifest.json"]
    journal["snapshot_complete"] = True


def _copy_stage(fs: TransactionFilesystem, workspace: TransactionWorkspace, journal: dict[str, Any], profile: str) -> dict[str, Any]:
    candidate = _manifest_data(fs, profile)
    sources = _managed_sources(fs.source_path, profile)
    for relative, source in sorted(sources.items()):
        source_fd = fs.source_file(source)
        try:
            parent, leaf = workspace.parent("stage", relative, create=True)
            try:
                _copy_for_upgrade(source_fd, parent, leaf, "stage", candidate["managed_files"][relative])
            finally:
                os.close(parent)
        finally:
            os.close(source_fd)
    stage_agent = _walk_dir(workspace.stage_fd, ".agent-plus", create=True)
    try:
        _atomic_write_json_at(stage_agent, "install-manifest.json", (json.dumps(candidate, indent=2, sort_keys=True) + "\n").encode())
    finally:
        os.close(stage_agent)
    candidate_manifest_fd = workspace.source_file("stage", ".agent-plus/install-manifest.json")
    try:
        journal["candidate_manifest_sha256"] = _hash_fd(candidate_manifest_fd, "candidate manifest")
    finally:
        os.close(candidate_manifest_fd)
    journal["candidate_managed_files"] = candidate["managed_files"]
    journal["candidate_version"] = candidate["agent_plus_version"]
    journal["stage_complete"] = True
    return candidate


def _commit(fs: TransactionFilesystem, workspace: TransactionWorkspace, journal: dict[str, Any]) -> None:
    for relative in journal["commit_files"]:
        source_fd = workspace.source_file("stage", relative)
        try:
            parent, leaf = fs.target_parent(relative)
            try:
                expected = journal["candidate_managed_files"].get(relative, journal["candidate_manifest_sha256"])
                _replace_for_upgrade(source_fd, parent, leaf, "commit", expected)
            finally:
                os.close(parent)
        finally:
            os.close(source_fd)
        journal["committed_files"].append(relative)
        fs.write_journal(journal)


def _verify_committed(fs: TransactionFilesystem, journal: dict[str, Any]) -> None:
    for relative, expected in journal["candidate_managed_files"].items():
        if _target_digest(fs, relative) != expected:
            raise ManagerError(f"Committed file verification failed: {relative}")
    if _target_digest(fs, ".agent-plus/install-manifest.json") != journal["candidate_manifest_sha256"]:
        raise ManagerError("Committed manifest verification failed")


def _verify_recovered(fs: TransactionFilesystem, journal: dict[str, Any]) -> None:
    """Authenticate the installed recovery set before terminal cleanup."""
    manifest = _manifest(fs)
    if sorted(manifest["managed_files"]) != journal["managed_files"]:
        raise ManagerError("Recovered target managed-file set is not exact")
    for relative in journal["recovery_files"]:
        expected = journal["recovery_digests"][relative]
        if _target_digest(fs, relative) != expected:
            raise ManagerError(f"Recovered target verification failed: {relative}")


def _preflight_recovery_sources(
    workspace: TransactionWorkspace, journal: dict[str, Any]
) -> None:
    """Verify the complete recovery set before the first target write."""
    for relative in journal["recovery_files"]:
        expected = journal["recovery_digests"][relative]
        source_fd = workspace.source_file("snapshot", relative)
        try:
            if _hash_fd(source_fd, f"snapshot {relative}") != expected:
                raise ManagerError(f"Recovery snapshot integrity mismatch: {relative}")
        finally:
            os.close(source_fd)


def record(target: Path, profile: str) -> None:
    if profile not in ALLOWED_PROFILES:
        raise ManagerError(f"Unknown profile: {profile}")
    with TransactionFilesystem(target) as fs:
        agent_fd = fs.open_agent()
        value = _record_manifest_data(fs, profile)
        _atomic_write_json_at(agent_fd, "install-manifest.json", (json.dumps(value, indent=2, sort_keys=True) + "\n").encode())


def status(target: Path) -> int:
    with TransactionFilesystem(target) as fs, fs.lock(allow_stale=False):
            if fs.transaction_record_exists():
                raise ManagerError("Pending Agent+ transaction; run recover --target")
            manifest = _manifest(fs)
            drift = _drift(fs, manifest)
            if drift:
                for item in drift:
                    print(f"LOCAL_DRIFT {item}")
                return 1
            available = _version_from_fs(fs)
            if manifest.get("agent_plus_version") != available:
                print(f"UPDATE_AVAILABLE installed={manifest.get('agent_plus_version')} available={available}")
                return 3
            print(f"AGENT_PLUS_CURRENT version={available} profile={manifest['profile']}")
            return 0


def upgrade(target: Path) -> None:
    with TransactionFilesystem(target) as fs, fs.lock(allow_stale=False):
            if fs.transaction_record_exists():
                raise ManagerError("Pending Agent+ transaction; run recover --target")
            manifest = _manifest(fs)
            drift = _drift(fs, manifest)
            if drift:
                raise ManagerError("Refusing upgrade because a managed file changed locally: " + drift[0])
            profile = manifest["profile"]
            transaction_id = uuid.uuid4().hex
            journal = _journal_base(transaction_id, profile, manifest["managed_files"])
            fs.write_journal(journal)
            try:
                with fs.workspace(transaction_id, create=True) as workspace:
                    _copy_snapshot(fs, workspace, journal, manifest)
                    journal["state"] = "STAGING"
                    fs.write_journal(journal)
                    _copy_stage(fs, workspace, journal, profile)
                    journal["state"] = "READY"
                    fs.write_journal(journal)
                    journal["state"] = "COMMITTING"
                    fs.write_journal(journal)
                    _commit(fs, workspace, journal)
                    _verify_committed(fs, journal)
                    journal["state"] = "COMMITTED"
                    fs.write_journal(journal)
            except ManagerError as exc:
                journal["state"] = "RECOVERY_REQUIRED" if journal["snapshot_complete"] else "ABORTED"
                journal["last_error"] = str(exc)
                fs.write_journal(journal)
                raise ManagerError(f"{exc}; run recover --target to resume") from exc
            _cleanup_workspace(fs, transaction_id)
            fs.remove_journal()
            print(f"Agent+ upgraded to {_version_from_fs(fs)} at {fs.target_path}")


def recover(target: Path) -> None:
    with TransactionFilesystem(target) as fs, fs.lock(allow_stale=True):
            if not fs.prepare_journal_recovery():
                print("Agent+ recovery: no pending transaction")
                return
            journal = _load_journal(fs)
            transaction_id = journal["transaction_id"]
            restart_action = _restart_action(journal)
            if restart_action == "abort":
                try:
                    if fs.transaction_workspace_exists(transaction_id):
                        _cleanup_workspace(fs, transaction_id)
                    fs.remove_journal()
                except ManagerError as exc:
                    raise ManagerError(
                        f"Recovery terminal cleanup failed; retry recover --target: {exc}"
                    ) from exc
                print("Agent+ recovery: discarded incomplete precommit transaction")
                return
            with fs.workspace(transaction_id) as workspace:
                if restart_action == "verify_commit":
                    _verify_committed(fs, journal)
                elif restart_action == "verify_recovery":
                    try:
                        _preflight_recovery_sources(workspace, journal)
                        _verify_recovered(fs, journal)
                    except ManagerError as exc:
                        journal["state"] = "RECOVERY_REQUIRED"
                        journal["last_error"] = str(exc)
                        fs.write_journal(journal)
                        raise ManagerError(f"{exc}; retry recover --target") from exc
                elif restart_action == "restore":
                    try:
                        _preflight_recovery_sources(workspace, journal)
                        for relative in journal["recovery_files"]:
                            expected = journal["recovery_digests"][relative]
                            source_fd = workspace.source_file("snapshot", relative)
                            try:
                                parent, leaf = fs.target_parent(relative)
                                try:
                                    _copy_to_atomic_restore(source_fd, parent, leaf, expected)
                                finally:
                                    os.close(parent)
                            finally:
                                os.close(source_fd)
                            if relative not in journal["restored_files"]:
                                journal["restored_files"].append(relative)
                            journal["state"] = "RECOVERING"
                            fs.write_journal(journal)
                        for relative, expected in journal["recovery_digests"].items():
                            if _target_digest(fs, relative) != expected:
                                raise ManagerError(f"Recovery verification failed: {relative}")
                        journal["state"] = "RECOVERED"
                        journal["last_error"] = ""
                        fs.write_journal(journal)
                    except ManagerError as exc:
                        journal["state"] = "RECOVERY_REQUIRED"
                        journal["last_error"] = str(exc)
                        fs.write_journal(journal)
                        raise ManagerError(f"{exc}; retry recover --target") from exc
            try:
                _cleanup_workspace(fs, transaction_id)
                fs.remove_journal()
            except ManagerError as exc:
                raise ManagerError(f"Recovery terminal cleanup failed; retry recover --target: {exc}") from exc
            print("Agent+ recovery: restored prior installation")


def _registry() -> tuple[Path, dict[str, Any]]:
    path = _source_root() / ".agent-plus" / "local-projects.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManagerError("Local project registry is absent or invalid. Copy .agent-plus/local-projects.example.json first.") from exc
    if type(value) is not dict or type(value.get("projects")) is not dict:
        raise ManagerError("Invalid local project registry")
    return path, value["projects"]


def projects() -> None:
    _, entries = _registry()
    for name, entry in sorted(entries.items()):
        if type(entry) is not dict or type(entry.get("root")) is not str:
            raise ManagerError(f"Invalid local project entry: {name}")
        print(f"{name}\t{entry.get('role', 'consumer')}\t{entry['root']}")


def context(name: str) -> int:
    _, entries = _registry()
    entry = entries.get(name)
    if type(entry) is not dict or type(entry.get("root")) is not str:
        raise ManagerError(f"Unknown local project: {name}")
    root = Path(entry["root"]).expanduser().resolve()
    command = root / "scripts" / "ai-context.sh"
    if not command.is_file():
        raise ManagerError(f"Project context command is missing: {command}")
    return subprocess.run([str(command)], cwd=root, check=False).returncode


def _version(root: Path) -> str:
    return (root / "VERSION").read_text(encoding="utf-8").strip()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agent-plus-manager")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("status", "upgrade", "recover"):
        child = subparsers.add_parser(command)
        child.add_argument("--target", required=True, type=Path)
    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--target", required=True, type=Path)
    record_parser.add_argument("--profile", required=True)
    subparsers.add_parser("projects")
    context_parser = subparsers.add_parser("context")
    context_parser.add_argument("name")
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if args.command == "record":
            record(args.target, args.profile)
        elif args.command == "status":
            return status(args.target)
        elif args.command == "upgrade":
            upgrade(args.target)
        elif args.command == "recover":
            recover(args.target)
        elif args.command == "projects":
            projects()
        elif args.command == "context":
            return context(args.name)
    except ManagerError as exc:
        print(f"AGENT_PLUS_ERROR {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
