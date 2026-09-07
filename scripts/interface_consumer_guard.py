#!/usr/bin/env python3
"""Fail closed when a changed interface omits a discovered repository consumer."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import shlex
import stat
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

INTERFACE_CONSUMER_SCHEMA_VERSION = "agent-plus-interface-consumer-closure/v1"

_TOP_FIELDS = frozenset({"schema_version", "interfaces", "real_shape_smoke"})
_INTERFACE_FIELDS = frozenset(
    {"interface_id", "definition_path", "search_roots", "search_tokens", "consumers"}
)
_CONSUMER_FIELDS = frozenset({"path", "kind", "disposition", "acceptance_checks"})
_SMOKE_FIELDS = frozenset({"required", "status", "command", "evidence"})
_KINDS = frozenset(
    {
        "production",
        "runtime_wrapper",
        "diagnostic",
        "launcher",
        "serializer",
        "test",
        "docs",
    }
)
_DISPOSITIONS = frozenset(
    {"updated", "tested_unchanged", "proven_unreachable", "not_runtime_consumer"}
)
_TEXT_SUFFIXES = frozenset(
    {
        ".py",
        ".sh",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".md",
        ".json",
        ".r",
        ".rmd",
        ".qmd",
        ".sql",
        ".yaml",
        ".yml",
        ".ipynb",
    }
)


class InterfaceConsumerGuardBlocked(ValueError):
    """Raised when an interface-consumer closure receipt is incomplete or malformed."""


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InterfaceConsumerGuardBlocked(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _exact_fields(
    raw: object, expected: frozenset[str], *, where: str
) -> dict[str, Any]:
    if not isinstance(raw, dict) or any(not isinstance(key, str) for key in raw):
        raise InterfaceConsumerGuardBlocked(
            f"{where} must be an object with string keys"
        )
    observed = frozenset(raw)
    if observed != expected:
        raise InterfaceConsumerGuardBlocked(
            f"{where} fields differ: missing={sorted(expected - observed)} "
            f"extra={sorted(observed - expected)}"
        )
    return raw


def _nonempty_string(value: object, *, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InterfaceConsumerGuardBlocked(f"{where} must be a non-empty string")
    return value


def _relative_path(value: object, *, where: str) -> Path:
    text = _nonempty_string(value, where=where)
    path = Path(text)
    if path.is_absolute() or ".." in path.parts or path == Path("."):
        raise InterfaceConsumerGuardBlocked(
            f"{where} must be a safe repository-relative path"
        )
    return path


def _ordered_strings(value: object, *, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise InterfaceConsumerGuardBlocked(f"{where} must be a non-empty ordered list")
    result = tuple(_nonempty_string(item, where=f"{where} item") for item in value)
    if len(set(result)) != len(result):
        raise InterfaceConsumerGuardBlocked(f"{where} contains duplicates")
    if result != tuple(sorted(result)):
        raise InterfaceConsumerGuardBlocked(
            f"{where} must be in canonical sorted order"
        )
    return result


# Fixed generated/state exclusions. Caller search roots cannot hide source consumers.
_EXCLUDED = frozenset(
    {
        ".git",
        ".agent-plus",
        ".planning",
        "outputs",
        "__pycache__",
        ".mypy_cache",
        ".ruff_cache",
        ".pytest_cache",
        "node_modules",
        ".venv",
    }
)
SMOKE_PATH = ".agent-plus/interface-smoke.json"
SMOKE_LOG = ".agent-plus/interface-smoke.log"


def _safe_file(root: Path, relative: str) -> Path:
    path = root / _relative_path(relative, where="evidence path")
    for part in (path, *path.parents):
        if part == root:
            break
        if part.is_symlink():
            raise InterfaceConsumerGuardBlocked("symlink in searched or evidence path")
    if not path.is_file():
        raise InterfaceConsumerGuardBlocked(f"missing regular file: {relative}")
    return path


def _read_text(path: Path) -> str:
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK | os.O_NOFOLLOW)
        with os.fdopen(fd, "r", encoding="utf-8") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise OSError("not regular")
            return source.read()
    except (OSError, UnicodeError) as exc:
        raise InterfaceConsumerGuardBlocked(
            f"cannot read searched file {path.name}"
        ) from exc


def _discover(
    root: Path, search_roots: tuple[Path, ...], tokens: tuple[str, ...]
) -> set[str]:
    for search_root in search_roots:
        absolute = root / search_root
        if not absolute.is_dir() or absolute.is_symlink():
            raise InterfaceConsumerGuardBlocked(
                f"search root does not exist or is unsafe: {search_root}"
            )
    discovered: set[str] = set()
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in _EXCLUDED)
        for name in sorted(files):
            path = Path(directory) / name
            if path.suffix.lower() not in _TEXT_SUFFIXES:
                continue
            relative = path.relative_to(root).as_posix()
            _safe_file(root, relative)
            if any(token in _read_text(path) for token in tokens):
                discovered.add(relative)
        for name in dirs:
            if (Path(directory) / name).is_symlink():
                raise InterfaceConsumerGuardBlocked(
                    "symlinked source directory requires reconciliation"
                )
    return discovered


def _snapshot_inputs(packet: dict[str, Any], root: Path) -> dict[str, str]:
    paths = {interface["definition_path"] for interface in packet["interfaces"]}
    paths.update(
        consumer["path"]
        for interface in packet["interfaces"]
        for consumer in interface["consumers"]
    )
    return {
        path: hashlib.sha256(_safe_file(root, path).read_bytes()).hexdigest()
        for path in sorted(paths)
    }


def _verify_smoke(packet: dict[str, Any], root: Path) -> None:
    smoke = packet["real_shape_smoke"]
    if smoke["evidence"] != SMOKE_PATH:
        raise InterfaceConsumerGuardBlocked(f"smoke evidence must be {SMOKE_PATH}")
    evidence = _exact_fields(
        load_receipt(_safe_file(root, SMOKE_PATH)),
        frozenset(
            {"schema_version", "command", "exit_code", "inputs", "output_sha256"}
        ),
        where="smoke evidence",
    )
    if (
        evidence["schema_version"] != "agent-plus-interface-smoke/v1"
        or type(evidence["exit_code"]) is not int
        or evidence["exit_code"] != 0
    ):
        raise InterfaceConsumerGuardBlocked("smoke evidence did not succeed")
    if evidence["command"] != smoke["command"] or evidence[
        "inputs"
    ] != _snapshot_inputs(packet, root):
        raise InterfaceConsumerGuardBlocked("smoke command or input identity differs")
    if (
        evidence["output_sha256"]
        != hashlib.sha256(_safe_file(root, SMOKE_LOG).read_bytes()).hexdigest()
    ):
        raise InterfaceConsumerGuardBlocked("smoke output identity differs")


def record_smoke(packet: dict[str, Any], root: Path, command: list[str]) -> None:
    """Run only an explicit CLI command, never execute the command from receipt data."""
    structural = copy.deepcopy(packet)
    structural["real_shape_smoke"] = {
        "required": False,
        "status": "NOT_REQUIRED",
        "command": "not-required",
        "evidence": "not-required",
    }
    validate_receipt(structural, root=root)
    if not command or shlex.join(command) != packet["real_shape_smoke"]["command"]:
        raise InterfaceConsumerGuardBlocked(
            "explicit smoke command must match the contract"
        )
    before = _snapshot_inputs(packet, root)
    result = subprocess.run(
        command, cwd=root, capture_output=True, timeout=60, check=False
    )
    if result.returncode != 0 or before != _snapshot_inputs(packet, root):
        raise InterfaceConsumerGuardBlocked("smoke failed or changed its input files")
    directory = root / ".agent-plus"
    if directory.is_symlink():
        raise InterfaceConsumerGuardBlocked("unsafe smoke directory")
    directory.mkdir(exist_ok=True)
    output = result.stdout + result.stderr
    evidence = {
        "schema_version": "agent-plus-interface-smoke/v1",
        "command": shlex.join(command),
        "exit_code": result.returncode,
        "inputs": before,
        "output_sha256": hashlib.sha256(output).hexdigest(),
    }
    for relative, data in (
        (SMOKE_LOG, output),
        (SMOKE_PATH, json.dumps(evidence, sort_keys=True).encode()),
    ):
        fd, temporary = tempfile.mkstemp(dir=directory)
        try:
            with os.fdopen(fd, "wb") as dest:
                dest.write(data)
                dest.flush()
                os.fsync(dest.fileno())
            os.replace(temporary, root / relative)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)


def validate_receipt(raw: object, *, root: Path) -> None:
    """Validate one closed receipt and rediscover every declared interface consumer."""

    packet = _exact_fields(raw, _TOP_FIELDS, where="receipt")
    if packet["schema_version"] != INTERFACE_CONSUMER_SCHEMA_VERSION:
        raise InterfaceConsumerGuardBlocked(
            "unsupported interface-consumer schema version"
        )

    interfaces = packet["interfaces"]
    if not isinstance(interfaces, list) or not interfaces:
        raise InterfaceConsumerGuardBlocked("interfaces must be a non-empty list")
    interface_ids: list[str] = []
    for index, item in enumerate(interfaces):
        interface = _exact_fields(item, _INTERFACE_FIELDS, where=f"interfaces[{index}]")
        interface_id = _nonempty_string(
            interface["interface_id"], where=f"interfaces[{index}].interface_id"
        )
        interface_ids.append(interface_id)
        definition = _relative_path(
            interface["definition_path"], where=f"interfaces[{index}].definition_path"
        )
        definition_absolute = root / definition
        if not definition_absolute.is_file():
            raise InterfaceConsumerGuardBlocked(
                f"definition path does not exist: {definition}"
            )
        roots = tuple(
            _relative_path(value, where=f"interfaces[{index}].search_roots item")
            for value in _ordered_strings(
                interface["search_roots"], where=f"interfaces[{index}].search_roots"
            )
        )
        tokens = _ordered_strings(
            interface["search_tokens"], where=f"interfaces[{index}].search_tokens"
        )
        if not any(token in _read_text(definition_absolute) for token in tokens):
            raise InterfaceConsumerGuardBlocked(
                f"definition {definition} contains none of the declared search tokens"
            )

        consumers = interface["consumers"]
        if not isinstance(consumers, list):
            raise InterfaceConsumerGuardBlocked(
                f"interfaces[{index}].consumers must be a list"
            )
        declared: set[str] = set()
        ordered_paths: list[str] = []
        for consumer_index, consumer_item in enumerate(consumers):
            consumer = _exact_fields(
                consumer_item,
                _CONSUMER_FIELDS,
                where=f"interfaces[{index}].consumers[{consumer_index}]",
            )
            path = _relative_path(
                consumer["path"],
                where=f"interfaces[{index}].consumers[{consumer_index}].path",
            ).as_posix()
            ordered_paths.append(path)
            if path in declared:
                raise InterfaceConsumerGuardBlocked(
                    f"consumer path is duplicated: {path}"
                )
            declared.add(path)
            if not (root / path).is_file():
                raise InterfaceConsumerGuardBlocked(
                    f"consumer path does not exist: {path}"
                )
            if not isinstance(consumer["kind"], str) or consumer["kind"] not in _KINDS:
                raise InterfaceConsumerGuardBlocked(f"consumer {path} has unknown kind")
            if (
                not isinstance(consumer["disposition"], str)
                or consumer["disposition"] not in _DISPOSITIONS
            ):
                raise InterfaceConsumerGuardBlocked(
                    f"consumer {path} has unknown disposition"
                )
            _ordered_strings(
                consumer["acceptance_checks"],
                where=f"consumer {path} acceptance_checks",
            )
        if ordered_paths != sorted(ordered_paths):
            raise InterfaceConsumerGuardBlocked(
                "consumer paths must be in canonical sorted order"
            )

        discovered = _discover(root, roots, tokens)
        expected = declared | {definition.as_posix()}
        if discovered != expected:
            raise InterfaceConsumerGuardBlocked(
                f"interface {interface_id} consumer closure differs: "
                f"undeclared={sorted(discovered - expected)} "
                f"missing={sorted(expected - discovered)}"
            )

    if interface_ids != sorted(interface_ids) or len(set(interface_ids)) != len(
        interface_ids
    ):
        raise InterfaceConsumerGuardBlocked(
            "interface IDs must be unique and canonically sorted"
        )

    smoke = _exact_fields(
        packet["real_shape_smoke"], _SMOKE_FIELDS, where="real_shape_smoke"
    )
    if not isinstance(smoke["required"], bool):
        raise InterfaceConsumerGuardBlocked(
            "real_shape_smoke.required must be a boolean"
        )
    status = _nonempty_string(smoke["status"], where="real_shape_smoke.status")
    if status not in {"PASS", "NOT_REQUIRED"}:
        raise InterfaceConsumerGuardBlocked(
            "real_shape_smoke.status must be PASS or NOT_REQUIRED"
        )
    command = _nonempty_string(smoke["command"], where="real_shape_smoke.command")
    evidence = _nonempty_string(smoke["evidence"], where="real_shape_smoke.evidence")
    if smoke["required"] and status != "PASS":
        raise InterfaceConsumerGuardBlocked("required real-shape smoke did not PASS")
    if status == "PASS":
        _verify_smoke(packet, root)
    if status == "NOT_REQUIRED" and (
        command != "not-required" or evidence != "not-required"
    ):
        raise InterfaceConsumerGuardBlocked(
            "NOT_REQUIRED smoke must use exact not-required fields"
        )


def load_receipt(path: Path) -> object:
    try:
        return json.loads(
            _read_text(path),
            object_pairs_hook=_pairs_no_duplicates,
            parse_constant=lambda value: (_ for _ in ()).throw(
                InterfaceConsumerGuardBlocked("nonfinite JSON value")
            ),
        )
    except InterfaceConsumerGuardBlocked:
        raise
    except (OSError, ValueError, RecursionError, OverflowError) as exc:
        raise InterfaceConsumerGuardBlocked(
            f"cannot load interface-consumer receipt: {exc}"
        ) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--record-smoke", action="store_true")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        packet = load_receipt(args.receipt)
        if args.record_smoke:
            if not isinstance(packet, dict):
                raise InterfaceConsumerGuardBlocked("receipt must be an object")
            command = args.command[1:] if args.command[:1] == ["--"] else args.command
            record_smoke(packet, root, command)
        validate_receipt(packet, root=root)
    except (
        InterfaceConsumerGuardBlocked,
        OSError,
        UnicodeError,
        subprocess.TimeoutExpired,
        KeyError,
        TypeError,
    ) as exc:
        print(f"INTERFACE_CONSUMER_CLOSURE_BLOCKED: {exc}", file=sys.stderr)
        return 2
    print("INTERFACE_CONSUMER_CLOSURE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
