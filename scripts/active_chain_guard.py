#!/usr/bin/env python3
"""Validate one bounded Agent+ active-chain capsule."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

SCHEMA = "agent-plus-active-chain/v1"
TOP_LEVEL_FIELDS = {
    "schema_version",
    "chain_id",
    "objective",
    "status",
    "current_stage",
    "terminal_condition",
    "change_kind",
    "stages",
    "same_interface_failure_limit",
    "same_interface_failures",
    "authority_refs",
    "hard_boundaries",
}
STAGE_FIELDS = {"id", "role", "status", "evidence"}
CHAIN_STATUSES = {"active", "pass", "null", "block"}
STAGE_STATUSES = {"pending", "pass", "null", "block"}
ROLES = {"controller", "explorer", "maker", "evaluator", "verifier", "owner", "closeout"}
CHANGE_KINDS = {"routine", "local_repair", "architecture_reset", "execution"}
HARD_BOUNDARIES = {
    "no_consumer_sync",
    "no_data_access",
    "no_dependency_change",
    "no_git_mutation",
    "no_live_execution",
    "no_private_state_copy",
    "no_release",
    "no_scientific_claim",
}
IDENTIFIER = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")
MAX_CAPSULE_BYTES = 64 * 1024
CAPSULE_PATHS = {
    PurePosixPath(".agent-plus/active-chain.json"),
    PurePosixPath(".agent-plus/active-chain-example.json"),
}


class ChainError(ValueError):
    """A typed active-chain validation failure."""


def _error(code: str, detail: str) -> ChainError:
    return ChainError(f"{code}: {detail}")


def _object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise _error("BLOCK_CHAIN_DUPLICATE_KEY", key)
        value[key] = item
    return value


def _resolve_capsule_path(path: Path, root: Path) -> Path:
    if path.is_symlink():
        raise _error("BLOCK_CHAIN_CAPSULE_FILE", "capsule must not be a symlink")
    try:
        resolved_root = root.resolve(strict=True)
        resolved_path = path.resolve(strict=True)
        relative_path = PurePosixPath(resolved_path.relative_to(resolved_root).as_posix())
    except (OSError, ValueError) as exc:
        raise _error("BLOCK_CHAIN_CAPSULE_PATH", "capsule must be inside the project root") from exc
    if relative_path not in CAPSULE_PATHS or not resolved_path.is_file():
        raise _error(
            "BLOCK_CHAIN_CAPSULE_PATH",
            "capsule must be .agent-plus/active-chain.json or its public example",
        )
    return resolved_path


def _load_capsule(path: Path, root: Path) -> dict[str, Any]:
    resolved_path = _resolve_capsule_path(path, root)
    try:
        if resolved_path.stat().st_size > MAX_CAPSULE_BYTES:
            raise _error("BLOCK_CHAIN_CAPSULE_SIZE", str(resolved_path.stat().st_size))
        value = json.loads(
            resolved_path.read_text(encoding="utf-8"),
            object_pairs_hook=_object_without_duplicate_keys,
            parse_constant=lambda token: (_ for _ in ()).throw(
                _error("BLOCK_CHAIN_NONFINITE_NUMBER", token)
            ),
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise _error("BLOCK_CHAIN_JSON", str(exc)) from exc
    if not isinstance(value, dict):
        raise _error("BLOCK_CHAIN_SCHEMA", "top level must be an object")
    return value


def _validate_text(value: Any, field: str, maximum: int) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise _error("BLOCK_CHAIN_TEXT", field)
    if "\n" in value or "\r" in value:
        raise _error("BLOCK_CHAIN_TEXT", f"{field} must be one line")
    return value


def _validate_identifier(value: Any, field: str) -> str:
    text = _validate_text(value, field, 64)
    if not IDENTIFIER.fullmatch(text):
        raise _error("BLOCK_CHAIN_IDENTIFIER", field)
    return text


def _validate_relative_file(root: Path, value: Any, field: str) -> str:
    text = _validate_text(value, field, 240)
    pure = PurePosixPath(text)
    if pure.is_absolute() or ".." in pure.parts or "." in pure.parts:
        raise _error("BLOCK_CHAIN_PATH", f"unsafe {field}: {text}")
    candidate = root.joinpath(*pure.parts)
    try:
        resolved_root = root.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=True)
        resolved_candidate.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise _error("BLOCK_CHAIN_PATH", f"missing or escaping {field}: {text}") from exc
    if candidate.is_symlink() or not candidate.is_file():
        raise _error("BLOCK_CHAIN_PATH", f"{field} must be a regular non-symlink file: {text}")
    return text


def _validate_string_list(
    value: Any,
    field: str,
    allowed: set[str] | None = None,
    maximum: int = 64,
) -> list[str]:
    if not isinstance(value, list) or not 1 <= len(value) <= 16:
        raise _error("BLOCK_CHAIN_LIST", field)
    result = [_validate_text(item, field, maximum) for item in value]
    if result != sorted(set(result)):
        raise _error("BLOCK_CHAIN_LIST", f"{field} must be sorted and unique")
    if allowed is not None and any(item not in allowed for item in result):
        raise _error("BLOCK_CHAIN_ENUM", field)
    return result


def _validate_stage_shape(root: Path, stages: Any) -> list[dict[str, Any]]:
    if not isinstance(stages, list) or not 1 <= len(stages) <= 12:
        raise _error("BLOCK_CHAIN_STAGES", "stages must contain 1 to 12 items")
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(stages):
        if not isinstance(raw, dict) or set(raw) != STAGE_FIELDS:
            raise _error("BLOCK_CHAIN_STAGE_SCHEMA", str(index))
        stage_id = _validate_identifier(raw["id"], f"stages[{index}].id")
        if stage_id in seen:
            raise _error("BLOCK_CHAIN_STAGE_ID", stage_id)
        seen.add(stage_id)
        role = raw["role"]
        status = raw["status"]
        evidence = raw["evidence"]
        if not isinstance(role, str) or role not in ROLES:
            raise _error("BLOCK_CHAIN_STAGE_ROLE", stage_id)
        if not isinstance(status, str) or status not in STAGE_STATUSES:
            raise _error("BLOCK_CHAIN_STAGE_STATUS", stage_id)
        if status == "pending":
            if evidence != "":
                raise _error("BLOCK_CHAIN_PENDING_EVIDENCE", stage_id)
        else:
            _validate_relative_file(root, evidence, f"stages[{index}].evidence")
        result.append(raw)
    return result


def validate(path: Path, root: Path, mode: str) -> str:
    value = _load_capsule(path, root)
    if set(value) != TOP_LEVEL_FIELDS or value.get("schema_version") != SCHEMA:
        raise _error("BLOCK_CHAIN_SCHEMA", "unknown, missing, or unsupported top-level field")

    chain_id = _validate_identifier(value["chain_id"], "chain_id")
    _validate_text(value["objective"], "objective", 240)
    status = value["status"]
    if not isinstance(status, str) or status not in CHAIN_STATUSES:
        raise _error("BLOCK_CHAIN_STATUS", str(status))
    if value["terminal_condition"] != "pass_null_or_block":
        raise _error("BLOCK_CHAIN_TERMINAL_CONDITION", str(value["terminal_condition"]))
    change_kind = value["change_kind"]
    if not isinstance(change_kind, str) or change_kind not in CHANGE_KINDS:
        raise _error("BLOCK_CHAIN_CHANGE_KIND", str(change_kind))

    failure_limit = value["same_interface_failure_limit"]
    failure_count = value["same_interface_failures"]
    if failure_limit != 2:
        raise _error("BLOCK_CHAIN_FAILURE_LIMIT", str(failure_limit))
    if isinstance(failure_count, bool) or not isinstance(failure_count, int):
        raise _error("BLOCK_CHAIN_FAILURE_COUNT", str(failure_count))
    if not 0 <= failure_count <= failure_limit:
        raise _error("BLOCK_CHAIN_FAILURE_COUNT", str(failure_count))
    if failure_count == failure_limit and change_kind != "architecture_reset":
        raise _error("BLOCK_CHAIN_ARCHITECTURE_RESET_REQUIRED", chain_id)

    authority_refs = _validate_string_list(
        value["authority_refs"], "authority_refs", maximum=240
    )
    for index, authority_ref in enumerate(authority_refs):
        _validate_relative_file(root, authority_ref, f"authority_refs[{index}]")
    _validate_string_list(value["hard_boundaries"], "hard_boundaries", HARD_BOUNDARIES)
    stages = _validate_stage_shape(root, value["stages"])
    stage_statuses = [stage["status"] for stage in stages]

    if status == "active":
        if mode == "closeout":
            next_stage = next(
                (stage["id"] for stage in stages if stage["status"] == "pending"), "unknown"
            )
            raise _error("BLOCK_CHAIN_EARLY_CLOSEOUT", f"next={next_stage}")
        if any(item in {"null", "block"} for item in stage_statuses):
            raise _error("BLOCK_CHAIN_ACTIVE_TERMINAL_STAGE", chain_id)
        first_pending = next(
            (index for index, item in enumerate(stage_statuses) if item == "pending"), None
        )
        if first_pending is None:
            raise _error("BLOCK_CHAIN_ACTIVE_COMPLETE", chain_id)
        if any(item != "pass" for item in stage_statuses[:first_pending]) or any(
            item != "pending" for item in stage_statuses[first_pending:]
        ):
            raise _error("BLOCK_CHAIN_STAGE_ORDER", chain_id)
        if value["current_stage"] != stages[first_pending]["id"]:
            raise _error("BLOCK_CHAIN_ROUTING", stages[first_pending]["id"])
        return f"ACTIVE_CHAIN_CONTINUE chain={chain_id} stage={stages[first_pending]['id']}"

    if mode == "continue":
        raise _error("BLOCK_CHAIN_NOT_ACTIVE", chain_id)
    if value["current_stage"] is not None:
        raise _error("BLOCK_CHAIN_TERMINAL_CURRENT_STAGE", chain_id)
    if status == "pass":
        if any(item != "pass" for item in stage_statuses):
            raise _error("BLOCK_CHAIN_PASS_INCOMPLETE", chain_id)
    else:
        terminal_indexes = [index for index, item in enumerate(stage_statuses) if item == status]
        if len(terminal_indexes) != 1:
            raise _error("BLOCK_CHAIN_TERMINAL_STAGE", chain_id)
        terminal_index = terminal_indexes[0]
        if any(item != "pass" for item in stage_statuses[:terminal_index]) or any(
            item != "pending" for item in stage_statuses[terminal_index + 1 :]
        ):
            raise _error("BLOCK_CHAIN_STAGE_ORDER", chain_id)
    return f"ACTIVE_CHAIN_CLOSEOUT_{status.upper()} chain={chain_id}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--mode", choices=("continue", "closeout"), required=True)
    args = parser.parse_args()
    try:
        print(validate(args.capsule, args.root, args.mode))
        return 0
    except ChainError as exc:
        print(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
