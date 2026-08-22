#!/usr/bin/env python3
"""Fail closed when a changed interface omits a discovered repository consumer."""

from __future__ import annotations

import argparse
import json
import sys
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
    {"production", "runtime_wrapper", "diagnostic", "launcher", "serializer", "test", "docs"}
)
_DISPOSITIONS = frozenset(
    {"updated", "tested_unchanged", "proven_unreachable", "not_runtime_consumer"}
)
_TEXT_SUFFIXES = frozenset({".py", ".sh", ".js", ".jsx", ".ts", ".tsx", ".md", ".json"})


class InterfaceConsumerGuardBlocked(ValueError):
    """Raised when an interface-consumer closure receipt is incomplete or malformed."""


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise InterfaceConsumerGuardBlocked(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _exact_fields(raw: object, expected: frozenset[str], *, where: str) -> dict[str, Any]:
    if not isinstance(raw, dict) or any(not isinstance(key, str) for key in raw):
        raise InterfaceConsumerGuardBlocked(f"{where} must be an object with string keys")
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
        raise InterfaceConsumerGuardBlocked(f"{where} must be a safe repository-relative path")
    return path


def _ordered_strings(value: object, *, where: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not value:
        raise InterfaceConsumerGuardBlocked(f"{where} must be a non-empty ordered list")
    result = tuple(_nonempty_string(item, where=f"{where} item") for item in value)
    if len(set(result)) != len(result):
        raise InterfaceConsumerGuardBlocked(f"{where} contains duplicates")
    if result != tuple(sorted(result)):
        raise InterfaceConsumerGuardBlocked(f"{where} must be in canonical sorted order")
    return result


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InterfaceConsumerGuardBlocked(f"cannot read searched file {path}: {exc}") from exc


def _discover(root: Path, search_roots: tuple[Path, ...], tokens: tuple[str, ...]) -> set[str]:
    discovered: set[str] = set()
    for search_root in search_roots:
        absolute = root / search_root
        if not absolute.is_dir():
            raise InterfaceConsumerGuardBlocked(f"search root does not exist: {search_root}")
        for path in sorted(absolute.rglob("*")):
            if not path.is_file() or path.suffix not in _TEXT_SUFFIXES:
                continue
            text = _read_text(path)
            if any(token in text for token in tokens):
                discovered.add(path.relative_to(root).as_posix())
    return discovered


def validate_receipt(raw: object, *, root: Path) -> None:
    """Validate one closed receipt and rediscover every declared interface consumer."""

    packet = _exact_fields(raw, _TOP_FIELDS, where="receipt")
    if packet["schema_version"] != INTERFACE_CONSUMER_SCHEMA_VERSION:
        raise InterfaceConsumerGuardBlocked("unsupported interface-consumer schema version")

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
            raise InterfaceConsumerGuardBlocked(f"definition path does not exist: {definition}")
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
            raise InterfaceConsumerGuardBlocked(f"interfaces[{index}].consumers must be a list")
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
                raise InterfaceConsumerGuardBlocked(f"consumer path is duplicated: {path}")
            declared.add(path)
            if not (root / path).is_file():
                raise InterfaceConsumerGuardBlocked(f"consumer path does not exist: {path}")
            if consumer["kind"] not in _KINDS:
                raise InterfaceConsumerGuardBlocked(f"consumer {path} has unknown kind")
            if consumer["disposition"] not in _DISPOSITIONS:
                raise InterfaceConsumerGuardBlocked(f"consumer {path} has unknown disposition")
            _ordered_strings(
                consumer["acceptance_checks"],
                where=f"consumer {path} acceptance_checks",
            )
        if ordered_paths != sorted(ordered_paths):
            raise InterfaceConsumerGuardBlocked("consumer paths must be in canonical sorted order")

        discovered = _discover(root, roots, tokens)
        expected = declared | {definition.as_posix()}
        if discovered != expected:
            raise InterfaceConsumerGuardBlocked(
                f"interface {interface_id} consumer closure differs: "
                f"undeclared={sorted(discovered - expected)} "
                f"missing={sorted(expected - discovered)}"
            )

    if interface_ids != sorted(interface_ids) or len(set(interface_ids)) != len(interface_ids):
        raise InterfaceConsumerGuardBlocked("interface IDs must be unique and canonically sorted")

    smoke = _exact_fields(packet["real_shape_smoke"], _SMOKE_FIELDS, where="real_shape_smoke")
    if not isinstance(smoke["required"], bool):
        raise InterfaceConsumerGuardBlocked("real_shape_smoke.required must be a boolean")
    status = _nonempty_string(smoke["status"], where="real_shape_smoke.status")
    if status not in {"PASS", "NOT_REQUIRED"}:
        raise InterfaceConsumerGuardBlocked("real_shape_smoke.status must be PASS or NOT_REQUIRED")
    command = _nonempty_string(smoke["command"], where="real_shape_smoke.command")
    evidence = _nonempty_string(smoke["evidence"], where="real_shape_smoke.evidence")
    if smoke["required"] and status != "PASS":
        raise InterfaceConsumerGuardBlocked("required real-shape smoke did not PASS")
    if status == "NOT_REQUIRED" and (command != "not-required" or evidence != "not-required"):
        raise InterfaceConsumerGuardBlocked("NOT_REQUIRED smoke must use exact not-required fields")


def load_receipt(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs_no_duplicates)
    except InterfaceConsumerGuardBlocked:
        raise
    except (OSError, json.JSONDecodeError) as exc:
        raise InterfaceConsumerGuardBlocked(
            f"cannot load interface-consumer receipt: {exc}"
        ) from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        root = args.root.resolve(strict=True)
        validate_receipt(load_receipt(args.receipt), root=root)
    except (InterfaceConsumerGuardBlocked, OSError) as exc:
        print(f"INTERFACE_CONSUMER_CLOSURE_BLOCKED: {exc}", file=sys.stderr)
        return 2
    print("INTERFACE_CONSUMER_CLOSURE_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
