"""Verify one fixed release candidate with read-only source Git access."""

from __future__ import annotations

import hashlib
import json
import os
import pwd
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid
from collections.abc import Sequence
from pathlib import Path, PurePosixPath
from typing import Any, NamedTuple, NoReturn

CONFIG_SCHEMA = "agent-plus-release-candidate/v2"
RECEIPT_SCHEMA = "agent-plus-release-candidate-receipt/v2"
CONFIG_RELATIVE = Path(".agent-plus/release-candidate.json")
RECEIPT_RELATIVE = Path("outputs/release-candidate/receipt.json")
SEMVER_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
COMMIT_RE = re.compile(r"[0-9a-f]{40}")
CONFIG_KEYS = {
    "schema_version",
    "current_version",
    "candidate_version",
    "base_commit",
    "manifest_path",
}
LOCAL_EXACT_EXCLUSIONS = {".agent-plus/.engineering-boundaries.json.lock", "Icon\r"}
LOCAL_PREFIX_EXCLUSIONS = ("outputs/",)
STATIC_FILES = (
    "scripts/agent_plus_manager.py",
    "scripts/active_chain_guard.py",
    "scripts/anti_loop_guard.py",
    "scripts/verify_release_candidate.py",
)
RUFF_FILES = STATIC_FILES + (
    "tests/test_agent_plus_lifecycle.py",
    "tests/test_agent_plus_legacy_adoption.py",
    "tests/test_release_candidate_verifier.py",
)
MYPY_VERSION = "2.3.1"
RUFF_VERSION = "0.16.5"
SOURCE_COMMANDS = {"ls-tree", "cat-file", "ls-files"}
GIT = shutil.which("git", path=os.defpath) or "git"


class CandidateError(RuntimeError):
    """A typed failure with bounded, public-safe diagnostics."""

    def __init__(
        self, code: str, message: str, details: dict[str, object] | None = None
    ) -> None:
        super().__init__(f"{code} {message}")
        self.code = code
        self.message = message
        self.details = details or {}


class CandidateConfig(NamedTuple):
    current_version: str
    candidate_version: str
    base_commit: str
    manifest_path: str


class FileValue(NamedTuple):
    mode: str
    data: bytes


def _error(code: str, message: str) -> NoReturn:
    raise CandidateError(code, message)


def _object_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            _error("E_CONFIG_DUPLICATE_KEY", "configuration contains a duplicate key")
        result[key] = value
    return result


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _safe_relative(value: str, label: str, *, public: bool = True) -> str:
    path = PurePosixPath(value)
    if (
        not value
        or not path.parts
        or any(c in value for c in ("\x00\n\r" if public else "\x00"))
        or path.is_absolute()
        or path.as_posix() != value
        or ".." in path.parts
    ):
        _error("E_UNSAFE_PATH", f"{label} must be a normalized relative file path")
    if public and path.parts[0] in {".git", "outputs"}:
        _error("E_UNSAFE_PATH", f"{label} is outside the public candidate surface")
    return value


def _directory_fd(path: Path) -> int:
    """Open every absolute directory component without following links."""
    descriptor = os.open(path.anchor, os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor
            )
            os.close(descriptor)
            descriptor = child
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _read_file(root: Path, relative: str, code: str = "E_SOURCE_FILE") -> FileValue:
    _safe_relative(relative, "file", public=False)
    parent = -1
    descriptor = -1
    try:
        parent = _directory_fd(root / Path(relative).parent)
        descriptor = os.open(
            Path(relative).name,
            os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK,
            dir_fd=parent,
        )
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            _error(code, "required file is not a regular file")
        with os.fdopen(descriptor, "rb", closefd=False) as stream:
            data = stream.read()
        after = os.fstat(descriptor)
        if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_mode) != (
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
            after.st_mode,
        ):
            _error("E_SOURCE_CHANGED", "file changed while it was read")
        return FileValue("100755" if before.st_mode & 0o111 else "100644", data)
    except OSError as exc:
        raise CandidateError(code, "required file is unavailable or unsafe") from exc
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if parent >= 0:
            os.close(parent)


def _text(data: bytes, code: str) -> str:
    try:
        return data.decode("utf-8")
    except UnicodeError as exc:
        raise CandidateError(code, "required text is not UTF-8") from exc


def load_config(root: Path) -> CandidateConfig:
    try:
        raw = json.loads(
            _text(
                _read_file(root, str(CONFIG_RELATIVE), "E_CONFIG_FILE").data,
                "E_CONFIG_JSON",
            ),
            object_pairs_hook=_object_no_duplicates,
        )
    except json.JSONDecodeError as exc:
        raise CandidateError(
            "E_CONFIG_JSON", "release configuration is invalid JSON"
        ) from exc
    if (
        not isinstance(raw, dict)
        or set(raw) != CONFIG_KEYS
        or raw.get("schema_version") != CONFIG_SCHEMA
    ):
        _error(
            "E_CONFIG_SCHEMA", "release configuration has unsupported fields or schema"
        )
    if any(type(raw[key]) is not str for key in CONFIG_KEYS):
        _error("E_CONFIG_TYPE", "release configuration values must be strings")
    current, candidate, base = (
        raw["current_version"],
        raw["candidate_version"],
        raw["base_commit"],
    )
    manifest = _safe_relative(raw["manifest_path"], "manifest_path")
    if (
        not SEMVER_RE.fullmatch(current)
        or not SEMVER_RE.fullmatch(candidate)
        or current == candidate
    ):
        _error(
            "E_CONFIG_VERSION",
            "release versions must be distinct exact semantic versions",
        )
    if not COMMIT_RE.fullmatch(base):
        _error("E_CONFIG_COMMIT", "base commit must be a full lowercase SHA-1 identity")
    if not manifest.startswith(".planning/essential-tasks/"):
        _error(
            "E_CONFIG_MANIFEST",
            "manifest must use the fixed planning evidence directory",
        )
    return CandidateConfig(current, candidate, base, manifest)


def load_manifest(root: Path, relative: str) -> list[str]:
    items = _text(
        _read_file(root, relative, "E_MANIFEST_FILE").data, "E_MANIFEST_FILE"
    ).splitlines()
    normalized = [_safe_relative(item, "manifest item") for item in items]
    if not normalized or normalized != sorted(set(normalized)):
        _error("E_MANIFEST_ORDER", "candidate manifest must be sorted and unique")
    if "VERSION" not in normalized:
        _error("E_MANIFEST_VERSION", "candidate manifest must contain VERSION")
    for item in normalized:
        _read_file(root, item, "E_MANIFEST_FILE")
    return normalized


def expected_candidate_paths(paths: Sequence[str]) -> list[str]:
    return sorted(
        {
            p
            for p in paths
            if p not in LOCAL_EXACT_EXCLUSIONS
            and not any(p.startswith(prefix) for prefix in LOCAL_PREFIX_EXCLUSIONS)
        }
        | {"VERSION"}
    )


def _environment(temporary: Path | None = None) -> dict[str, str]:
    """Do not inherit Git, shell, Python, loader, or tool configuration variables."""
    path_parts = [str(Path(sys.executable).parent), *os.defpath.split(os.pathsep)]
    env = {
        "PATH": os.pathsep.join(dict.fromkeys(path_parts)),
        "LANG": "C.UTF-8",
        "LC_ALL": "C",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_SYSTEM": os.devnull,
        "GIT_OPTIONAL_LOCKS": "0",
        "GIT_NO_LAZY_FETCH": "1",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONNOUSERSITE": "1",
    }
    if temporary is not None:
        for name in ("home", "cache", "tmp"):
            (temporary / name).mkdir(exist_ok=True)
        env.update(
            HOME=str(temporary / "home"),
            XDG_CONFIG_HOME=str(temporary / "home"),
            XDG_CACHE_HOME=str(temporary / "cache"),
            UV_CACHE_DIR=str(temporary / "cache" / "uv"),
            TMPDIR=str(temporary / "tmp"),
            UV_NO_CONFIG="1",
            MYPY_CACHE_DIR=str(temporary / "cache" / "mypy"),
            RUFF_CACHE_DIR=str(temporary / "cache" / "ruff"),
        )
    return env


def _run(
    command: Sequence[str],
    cwd: Path,
    *,
    env: dict[str, str],
    code: str,
    input_bytes: bytes | None = None,
    timeout: int = 240,
) -> bytes:
    try:
        result = subprocess.run(
            list(command),
            cwd=cwd,
            env=env,
            input=input_bytes,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise CandidateError(code, "required command could not complete") from exc
    if result.returncode:
        raise CandidateError(
            code,
            "required command failed",
            {
                "exit_status": result.returncode,
                "stderr_bytes": len(result.stderr),
                "stderr_sha256": _digest_bytes(result.stderr),
                "stdout_sha256": _digest_bytes(result.stdout),
            },
        )
    return result.stdout


def _source_git(
    root: Path, args: Sequence[str], *, input_bytes: bytes | None = None
) -> bytes:
    if not args or args[0] not in SOURCE_COMMANDS:
        _error("E_SOURCE_COMMAND", "source Git command is not read-only")
    return _run(
        (
            GIT,
            f"--git-dir={root / '.git'}",
            f"--work-tree={root}",
            "-c",
            "core.fsmonitor=false",
            "-c",
            f"core.hooksPath={os.devnull}",
            *args,
        ),
        root,
        env=_environment(),
        input_bytes=input_bytes,
        code="E_SOURCE_GIT",
    )


def _detached_git(
    root: Path,
    args: Sequence[str],
    env: dict[str, str],
    input_bytes: bytes | None = None,
) -> bytes:
    return _run(
        (GIT, *args), root, env=env, input_bytes=input_bytes, code="E_DETACHED_GIT"
    )


def tree_snapshot(root: Path) -> str:
    """Hash bytes, modes, names, and modification times without following links."""
    records: list[object] = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        metadata = path.lstat()
        if path.is_symlink():
            _error("E_SNAPSHOT_PATH", "protected tree contains a symbolic link")
        if stat.S_ISREG(metadata.st_mode):
            payload = _read_file(root, relative).data
            records.append(
                (
                    relative,
                    metadata.st_mode,
                    metadata.st_mtime_ns,
                    _digest_bytes(payload),
                )
            )
        elif stat.S_ISDIR(metadata.st_mode):
            records.append((relative, metadata.st_mode, metadata.st_mtime_ns))
        else:
            _error("E_SNAPSHOT_PATH", "protected tree contains a nonregular entry")
    return _digest_bytes(_canonical_json(records).encode())


def source_snapshot(root: Path, *, exclude_outputs: bool = True) -> dict[str, str]:
    """Capture source Git and every non-output worktree file before Git runs."""
    git_dir = root / ".git"
    if git_dir.is_symlink() or not git_dir.is_dir():
        _error("E_REPOSITORY_LAYOUT", "a regular local .git directory is required")
    records: list[object] = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        parent = Path(directory)
        if parent == root:
            dirs[:] = [
                name
                for name in dirs
                if name != ".git" and not (exclude_outputs and name == "outputs")
            ]
        for name in sorted(dirs + files):
            path = parent / name
            relative = path.relative_to(root).as_posix()
            if exclude_outputs and relative == "outputs":
                continue
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                _error("E_SNAPSHOT_PATH", "source contains a symbolic link")
            if stat.S_ISREG(metadata.st_mode):
                value = _read_file(root, relative)
                records.append(
                    (
                        relative,
                        metadata.st_mode,
                        metadata.st_mtime_ns,
                        metadata.st_ctime_ns,
                        _digest_bytes(value.data),
                    )
                )
            elif not stat.S_ISDIR(metadata.st_mode):
                _error("E_SNAPSHOT_PATH", "source contains a nonregular entry")
    return {
        "git": tree_snapshot(git_dir),
        "worktree": _digest_bytes(_canonical_json(sorted(records, key=str)).encode()),
    }


def _head(root: Path) -> str:
    raw = _text(_read_file(root, ".git/HEAD").data, "E_HEAD").strip()
    if raw.startswith("ref: "):
        ref = _safe_relative(raw[5:], "HEAD reference", public=False)
        if not ref.startswith("refs/"):
            _error("E_HEAD", "HEAD reference is unsupported")
        if (root / ".git" / ref).exists():
            raw = _text(_read_file(root, ".git/" + ref).data, "E_HEAD").strip()
        else:
            packed = _text(_read_file(root, ".git/packed-refs").data, "E_HEAD")
            matches = [
                line.split(" ", 1)[0]
                for line in packed.splitlines()
                if line.endswith(" " + ref)
            ]
            if len(matches) != 1:
                _error("E_HEAD", "HEAD reference is unavailable")
            raw = matches[0]
    if not COMMIT_RE.fullmatch(raw):
        _error("E_HEAD", "HEAD does not name a supported commit")
    return raw


def _entries(raw: bytes, *, index: bool = False) -> dict[str, tuple[str, str]]:
    result: dict[str, tuple[str, str]] = {}
    try:
        for record in filter(None, raw.split(b"\0")):
            metadata, name = record.split(b"\t", 1)
            first, second, third = metadata.decode("ascii").split(" ")
            mode, oid = first, second if index else third
            if mode not in {"100644", "100755"} or (
                third != "0" if index else second != "blob"
            ):
                _error("E_GIT_ENTRY", "only regular stage-zero files are supported")
            path = _safe_relative(_text(name, "E_GIT_ENTRY"), "Git entry")
            if path in result or not COMMIT_RE.fullmatch(oid):
                _error("E_GIT_ENTRY", "Git entry identity is invalid")
            result[path] = (mode, oid)
    except (ValueError, UnicodeError) as exc:
        raise CandidateError("E_GIT_ENTRY", "Git entry output is malformed") from exc
    return result


def _base_files(
    root: Path, commit: str
) -> tuple[dict[str, FileValue], dict[str, tuple[str, str]]]:
    entries = _entries(_source_git(root, ("ls-tree", "-rz", "--full-tree", commit)))
    identities = sorted({oid for _, oid in entries.values()})
    response = _source_git(
        root,
        ("cat-file", "--batch"),
        input_bytes=("\n".join(identities) + "\n").encode(),
    )
    blobs: dict[str, bytes] = {}
    offset = 0
    try:
        for oid in identities:
            end = response.index(b"\n", offset)
            header = response[offset:end].decode("ascii").split(" ")
            if len(header) != 3 or header[:2] != [oid, "blob"]:
                _error("E_BASE_OBJECT", "base object is unavailable or not a blob")
            size = int(header[2])
            offset = end + 1
            if size < 0 or response[offset + size : offset + size + 1] != b"\n":
                _error("E_BASE_OBJECT", "base object framing is invalid")
            data = response[offset : offset + size]
            if _blob_oid(data) != oid:
                _error("E_BASE_OBJECT", "base object bytes do not match their identity")
            blobs[oid] = data
            offset += size + 1
        if offset != len(response):
            _error("E_BASE_OBJECT", "base object response has trailing data")
    except (ValueError, UnicodeError) as exc:
        raise CandidateError(
            "E_BASE_OBJECT", "base object response is malformed"
        ) from exc
    return {
        path: FileValue(mode, blobs[oid]) for path, (mode, oid) in entries.items()
    }, entries


def _blob_oid(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _candidate_files(
    root: Path,
    config: CandidateConfig,
    manifest: list[str],
    base: dict[str, FileValue],
    entries: dict[str, tuple[str, str]],
) -> dict[str, FileValue]:
    index = _entries(_source_git(root, ("ls-files", "--stage", "-z")), index=True)
    untracked = [
        _text(item, "E_SCOPE")
        for item in _source_git(
            root, ("ls-files", "--others", "--exclude-standard", "-z")
        ).split(b"\0")
        if item
    ]
    changed = {p for p in set(index) | set(entries) if index.get(p) != entries.get(p)}
    files: dict[str, FileValue] = {}
    for path in sorted(
        set(base) | set(index) | set(expected_candidate_paths(untracked))
    ):
        _safe_relative(path, "candidate path")
        value = _read_file(root, path)
        if base.get(path) != value:
            changed.add(path)
        files[path] = value
    if expected_candidate_paths(sorted(changed)) != manifest:
        _error(
            "E_SCOPE_MISMATCH", "manifest does not equal the exact public source scope"
        )
    files["VERSION"] = FileValue("100644", (config.candidate_version + "\n").encode())
    return files


def _write_files(root: Path, files: dict[str, FileValue]) -> None:
    for relative, value in files.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as stream:
            stream.write(value.data)
        destination.chmod(0o755 if value.mode == "100755" else 0o644)


def _stage_files(root: Path, files: dict[str, FileValue], env: dict[str, str]) -> str:
    _detached_git(root, ("read-tree", "--empty"), env)
    records = []
    for path, value in sorted(files.items()):
        oid = _text(
            _detached_git(
                root, ("hash-object", "--no-filters", "-w", "--stdin"), env, value.data
            ),
            "E_DETACHED_GIT",
        ).strip()
        if oid != _blob_oid(value.data):
            _error("E_DETACHED_OBJECT", "detached blob identity is incorrect")
        records.append(f"{value.mode} {oid}\t{path}".encode())
    _detached_git(
        root, ("update-index", "-z", "--index-info"), env, b"\0".join(records) + b"\0"
    )
    tree = _text(_detached_git(root, ("write-tree",), env), "E_DETACHED_GIT").strip()
    if not COMMIT_RE.fullmatch(tree):
        _error("E_DETACHED_OBJECT", "detached tree identity is invalid")
    return tree


def _files_digest(files: dict[str, FileValue]) -> str:
    return _digest_bytes(
        _canonical_json(
            [(p, v.mode, _digest_bytes(v.data)) for p, v in sorted(files.items())]
        ).encode()
    )


def _validate_candidate(root: Path, env: dict[str, str]) -> None:
    user_bin = Path(pwd.getpwuid(os.getuid()).pw_dir) / ".local" / "bin"
    tool_path = os.pathsep.join((str(user_bin), "/opt/homebrew/bin", os.defpath))
    uvx = shutil.which("uvx", path=tool_path)
    if uvx is None:
        _error("E_TOOLCHAIN", "the required uvx executable is unavailable")
    _run(
        (uvx, "--from", f"mypy=={MYPY_VERSION}", "mypy", "--strict", *STATIC_FILES),
        root,
        env=env,
        code="E_MYPY",
    )
    _run(
        (uvx, "--from", f"ruff=={RUFF_VERSION}", "ruff", "check", *RUFF_FILES),
        root,
        env=env,
        code="E_RUFF",
    )
    _run(
        ("sh", "scripts/validate-public-package.sh"),
        root,
        env=env,
        code="E_PUBLIC_VALIDATOR",
    )


def _detached_candidate(
    temporary: Path,
    base: dict[str, FileValue],
    files: dict[str, FileValue],
    manifest: list[str],
) -> str:
    root = temporary / "candidate"
    root.mkdir()
    env = _environment(temporary)
    empty_template = temporary / "empty-template"
    empty_template.mkdir()
    _detached_git(
        root,
        ("init", "-q", "--object-format=sha1", f"--template={empty_template}"),
        env,
    )
    base_tree = _stage_files(root, base, env)
    tree = _stage_files(root, files, env)
    changed = _detached_git(
        root, ("diff", "--cached", "--name-only", "--no-renames", "-z", base_tree), env
    )
    paths = sorted(_text(p, "E_DETACHED_SCOPE") for p in changed.split(b"\0") if p)
    if paths != manifest:
        _error("E_DETACHED_SCOPE", "detached changed scope does not equal the manifest")
    _detached_git(
        root, ("diff", "--cached", "--check", "--no-ext-diff", base_tree), env
    )
    _write_files(root, files)
    candidate_before = source_snapshot(root, exclude_outputs=False)
    try:
        _validate_candidate(root, env)
    finally:
        actual = {path: _read_file(root, path, "E_CANDIDATE_CHANGED") for path in files}
        if (
            actual != files
            or source_snapshot(root, exclude_outputs=False) != candidate_before
        ):
            _error(
                "E_CANDIDATE_CHANGED",
                "validation changed candidate bytes, modes, or Git state",
            )
    return tree


def _write_receipt(root: Path, body: dict[str, object]) -> dict[str, object]:
    result = dict(body)
    result["receipt_id"] = "sha256:" + _digest_bytes(_canonical_json(body).encode())
    try:
        descriptor = _directory_fd(root)
    except OSError as exc:
        raise CandidateError(
            "E_RECEIPT_PATH", "receipt root is unavailable or unsafe"
        ) from exc
    temporary_name = ".receipt-" + uuid.uuid4().hex
    created = False
    try:
        for part in RECEIPT_RELATIVE.parent.parts:
            try:
                os.mkdir(part, dir_fd=descriptor)
            except FileExistsError:
                pass
            child = os.open(
                part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor
            )
            os.close(descriptor)
            descriptor = child
        handle = os.open(
            temporary_name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=descriptor,
        )
        created = True
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            stream.write(_canonical_json(result) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(
            temporary_name,
            RECEIPT_RELATIVE.name,
            src_dir_fd=descriptor,
            dst_dir_fd=descriptor,
        )
        created = False
    except OSError as exc:
        raise CandidateError(
            "E_RECEIPT_PATH", "receipt destination is unavailable or unsafe"
        ) from exc
    finally:
        if created:
            os.unlink(temporary_name, dir_fd=descriptor)
        os.close(descriptor)
    return result


def verify(root: Path) -> dict[str, object]:
    root = root.absolute()
    if Path.cwd() != root:
        _error("E_ROOT", "run the verifier from the canonical repository root")
    run_id = uuid.uuid4().hex
    initial: dict[str, object] = {
        "schema_version": RECEIPT_SCHEMA,
        "run_id": run_id,
        "status": "RUNNING",
    }
    _write_receipt(root, initial)
    before: dict[str, str] | None = None
    try:
        before = source_snapshot(root)
        try:
            config = load_config(root)
            manifest = load_manifest(root, config.manifest_path)
            if _head(root) != config.base_commit:
                _error("E_BASE_COMMIT", "HEAD does not match the configured base")
            if (
                _read_file(root, "VERSION").data
                != (config.current_version + "\n").encode()
            ):
                _error("E_CURRENT_VERSION", "live VERSION does not match configuration")
            manifest_digest = _digest_bytes(_read_file(root, config.manifest_path).data)
            base, entries = _base_files(root, config.base_commit)
            files = _candidate_files(root, config, manifest, base, entries)
            temporary_parent = Path("/tmp").resolve()
            if temporary_parent == root or root in temporary_parent.parents:
                _error("E_TEMP_ROOT", "temporary namespace overlaps the source")
            with tempfile.TemporaryDirectory(
                prefix="agent-plus-release-candidate-", dir=temporary_parent
            ) as value:
                tree = _detached_candidate(Path(value), base, files, manifest)
        finally:
            preceding = sys.exc_info()[1]
            try:
                after = source_snapshot(root)
            except (CandidateError, OSError) as exc:
                raise CandidateError(
                    "E_SOURCE_MUTATION",
                    "protected source cannot be verified after execution",
                ) from exc
            if after != before:
                details: dict[str, object] = (
                    {"preceding_error": preceding.code}
                    if isinstance(preceding, CandidateError)
                    else {}
                )
                raise CandidateError(
                    "E_SOURCE_MUTATION",
                    "protected source state changed during verification",
                    details,
                )
        body: dict[str, object] = {
            **initial,
            "status": "PASS",
            "base_commit": config.base_commit,
            "current_version": config.current_version,
            "candidate_version": config.candidate_version,
            "candidate_path_count": len(manifest),
            "manifest_sha256": manifest_digest,
            "candidate_tree": tree,
            "candidate_files_sha256": _files_digest(files),
            "source_before": before,
            "source_after": after,
            "toolchain": {"mypy": MYPY_VERSION, "ruff": RUFF_VERSION},
            "gates": [
                "exact-public-scope",
                "read-only-source-git",
                "detached-object-store",
                "raw-byte-export",
                "simulated-version",
                "strict-mypy",
                "ruff",
                "public-validator",
                "candidate-unchanged",
                "source-unchanged",
            ],
        }
    except (CandidateError, OSError, ValueError, UnicodeError) as exc:
        error = (
            exc
            if isinstance(exc, CandidateError)
            else CandidateError("E_FILESYSTEM", "required source operation failed")
        )
        _write_receipt(
            root,
            {
                **initial,
                "status": "BLOCK",
                "error_code": error.code,
                "message": error.message,
                "diagnostics": error.details,
                "source_baseline_captured": before is not None,
            },
        )
        raise error from exc
    return _write_receipt(root, body)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    root = Path(__file__).resolve().parents[1]
    try:
        if arguments:
            _error("E_ARGUMENTS", "verifier accepts no arguments")
        receipt = verify(root)
    except CandidateError as exc:
        if exc.code in {"E_ARGUMENTS", "E_ROOT"}:
            try:
                _write_receipt(
                    root,
                    {
                        "schema_version": RECEIPT_SCHEMA,
                        "run_id": uuid.uuid4().hex,
                        "status": "BLOCK",
                        "error_code": exc.code,
                        "message": exc.message,
                    },
                )
            except CandidateError:
                pass
        print(f"RELEASE_CANDIDATE_BLOCK {exc.code} {exc.message}")
        return 1
    print(_canonical_json(receipt))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
