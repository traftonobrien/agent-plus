#!/usr/bin/env python3
"""Fail-closed engineering-closure and first-error packet guard (v2).

The guard has no project-specific imports.  It validates a small JSON ledger and
one bounded task/review packet, then emits a deterministic PASS receipt.

v2 is a closed structured schema.  No caller-supplied natural-language value can
change an authorization decision.  Every decision field is a closed enum or an
exact ledger-approved identifier.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import tempfile
from collections.abc import Iterator, Mapping, Sequence
from contextlib import contextmanager, suppress
from pathlib import Path
from types import MappingProxyType
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - the supported runtime is POSIX
    fcntl = None  # type: ignore[assignment]

SCHEMA_VERSION = "anti-loop-guard/v2"

ENGINEERING_SWEEP = "engineering_sweep"
SCIENTIFIC_FIRST_ERROR = "scientific_first_error_gate"
LIVE_FIRST_ERROR = "live_first_error_gate"
REVIEW_MODES = frozenset({ENGINEERING_SWEEP, SCIENTIFIC_FIRST_ERROR, LIVE_FIRST_ERROR})

LOCAL_REPAIR = "local_repair"
ARCHITECTURE_RESET = "architecture_reset"
EXECUTION = "execution"
CHANGE_KINDS = frozenset({LOCAL_REPAIR, ARCHITECTURE_RESET, EXECUTION})

COLLECT_NAMED_MATRIX = "collect_named_matrix"
STOP_FIRST_ERROR = "stop_first_error"
STOP_POLICIES = frozenset({COLLECT_NAMED_MATRIX, STOP_FIRST_ERROR})

PACKET_TYPES = frozenset({"task", "review"})
REVIEW_STATUSES = frozenset({"planned", "complete"})
MATRIX_STATUSES = frozenset({"pending", "complete", "not_applicable"})

# Guard-owned, immutable outcome registry.  A ledger may select a subset of these
# exact identifiers, but it cannot create, rename, or recategorize an outcome.
# Process work (tests, lint, files, docs, receipts, reviews) has no catalog entry
# and therefore cannot be declared as a user or scientific outcome.
OUTCOME_CATALOG: Mapping[str, str] = MappingProxyType(
    {
        "agent-plus-control-plane-capability": "user_visible_capability",
        "certified-data-access-decision": "data_access_decision",
        "example-readiness-decision": "scientific_readiness_decision",
        "f16-rehearsal-readiness-decision": "scientific_readiness_decision",
        "model-evaluation-result": "model_evaluation_result",
        "validated-scientific-result": "scientific_result",
    }
)
OUTCOME_KINDS = frozenset(OUTCOME_CATALOG.values())

# Architecture-reset namespaces are not arbitrary.  The ledger must name one of
# these, and the packet must name exactly what the ledger names.
APPROVED_RESET_NAMESPACES = frozenset(
    {
        "agent-plus/0.2.0-release",
        "agent-plus/active-chain-routing",
        "rehearsals/wave-b-f16-read-only",
    }
)

BOUNDARY_ID = re.compile(r"^[A-Z][A-Z0-9_-]{2,63}$")
FAILURE_CLASS_ID = re.compile(r"^[a-z][a-z0-9._-]{2,63}$")
PACKET_ID = re.compile(r"^[A-Z][A-Z0-9_-]{2,79}$")
OUTCOME_ID = re.compile(r"^[a-z][a-z0-9-]{2,63}$")
ATTEMPT_ID = re.compile(r"^attempt-[0-9]{2}$")
CALLER_CHOICE_ID = re.compile(r"^[a-z][a-z0-9_-]{2,63}$")
MATRIX_ITEM_ID = re.compile(r"^[a-z][a-z0-9-]{2,63}$")

MAX_BLOCK_COUNT = (2**63) - 1
MAX_DEPTH = 12

LEDGER_KEYS = frozenset({"schema_version", "boundaries"})
BOUNDARY_KEYS = frozenset({"failure_classes"})
FAILURE_STATE_KEYS = frozenset(
    {
        "block_count",
        "architecture_reset_required",
        "reset_namespace",
        "authorized_attempt_id",
        "permitted_removed_choices",
        "permitted_outcomes",
        "required_attack_matrix",
        "required_named_coverage",
    }
)

BASE_PACKET_KEYS = frozenset(
    {
        "schema_version",
        "packet_id",
        "packet_type",
        "boundary_id",
        "failure_class",
        "ledger_ref",
        "review_mode",
        "change_kind",
        "outcome_kind",
        "outcome_id",
        "failure_class_coverage",
        "stop_policy",
        "review_status",
        "attack_matrix",
        "named_coverage",
    }
)
RESET_PACKET_KEYS = frozenset({"reset_namespace", "attempt_id", "removed_caller_choices"})
MATRIX_KEYS = frozenset({"status", "items"})


class _DuplicateKeyError(ValueError):
    pass


class GuardError(ValueError):
    """A short, typed, user-actionable validation error."""

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


def _error(code: str, message: str) -> GuardError:
    return GuardError(code, message)


# ---------------------------------------------------------------- primitives


def _require_string_keys(value: Any, label: str, depth: int = 0) -> None:
    """Reject non-string mapping keys and unbounded nesting at every depth."""

    if depth > MAX_DEPTH:
        raise _error("E_INVALID_STRUCTURE", f"{label} is nested deeper than {MAX_DEPTH} levels")
    if isinstance(value, Mapping):
        for key, item in value.items():
            if not isinstance(key, str):
                raise _error("E_INVALID_KEY_TYPE", f"{label} contains a non-string mapping key")
            _require_string_keys(item, label, depth + 1)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _require_string_keys(item, label, depth + 1)


def _require_keys(
    value: Mapping[str, Any],
    required: frozenset[str] | set[str],
    allowed: frozenset[str] | set[str],
    label: str,
) -> None:
    missing = sorted(set(required) - set(value))
    if missing:
        raise _error("E_MISSING_FIELD", f"{label} missing {','.join(missing)}")
    unknown = sorted(set(value) - set(allowed))
    if unknown:
        raise _error("E_UNKNOWN_FIELD", f"{label} has {','.join(unknown)}")


def _require_pattern(
    value: Any, field: str, pattern: re.Pattern[str], *, code: str = "E_INVALID_FIELD"
) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        raise _error(code, f"{field} must match {pattern.pattern}")
    return value


def _require_choice(
    value: Any, field: str, choices: frozenset[str], *, code: str = "E_INVALID_FIELD"
) -> str:
    """Validate an enum without letting an unhashable value escape."""

    if not isinstance(value, str) or value not in choices:
        raise _error(code, f"{field} must be one of {','.join(sorted(choices))}")
    return value


def _require_bool(value: Any, field: str, *, code: str = "E_INVALID_FIELD") -> bool:
    if not isinstance(value, bool):
        raise _error(code, f"{field} must be a boolean")
    return value


def _require_exact_nonnegative_int(value: Any, field: str, *, code: str = "E_INVALID_FIELD") -> int:
    """Reject bools, floats, strings, and values outside the persisted contract."""

    if type(value) is not int or value < 0 or value > MAX_BLOCK_COUNT:
        raise _error(code, f"{field} must be an exact non-negative integer <= {MAX_BLOCK_COUNT}")
    return value


def _require_id_list(
    value: Any,
    field: str,
    pattern: re.Pattern[str],
    *,
    allow_empty: bool = False,
    code: str = "E_INVALID_FIELD",
) -> list[str]:
    if not isinstance(value, list) or (not allow_empty and not value):
        raise _error(code, f"{field} must be a non-empty list of identifiers")
    result = [_require_pattern(item, f"{field} item", pattern, code=code) for item in value]
    if len(set(result)) != len(result):
        raise _error(code, f"{field} contains duplicate items")
    return result


def _reject_duplicate_pairs(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateKeyError(key)
        result[key] = value
    return result


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _load_json(path: Path, *, kind: str) -> dict[str, Any]:
    if not path.is_file():
        raise _error(f"E_MISSING_{kind.upper()}", f"{kind} file is missing")
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=lambda constant: (_ for _ in ()).throw(ValueError(constant)),
        )
    except _DuplicateKeyError as exc:
        raise _error("E_DUPLICATE_KEY", f"{kind} contains duplicate key {exc}") from exc
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError, OverflowError) as exc:
        raise _error(f"E_MALFORMED_{kind.upper()}", f"{kind} is not valid JSON") from exc
    except ValueError as exc:
        raise _error(
            f"E_MALFORMED_{kind.upper()}", f"{kind} contains an invalid JSON value"
        ) from exc
    if not isinstance(value, dict):
        raise _error(f"E_MALFORMED_{kind.upper()}", f"{kind} root must be an object")
    return value


# ------------------------------------------------------------------- ledger


def _validate_failure_state(raw_state: Any, label: str) -> dict[str, Any]:
    if not isinstance(raw_state, Mapping):
        raise _error("E_MALFORMED_LEDGER", f"state {label} must be an object")
    _require_keys(raw_state, FAILURE_STATE_KEYS, FAILURE_STATE_KEYS, f"state {label}")

    block_count = _require_exact_nonnegative_int(
        raw_state["block_count"], f"state {label} block_count", code="E_MALFORMED_LEDGER"
    )
    reset_required = _require_bool(
        raw_state["architecture_reset_required"],
        f"state {label} architecture_reset_required",
        code="E_MALFORMED_LEDGER",
    )
    if reset_required != (block_count >= 2):
        raise _error("E_MALFORMED_LEDGER", f"state {label} reset flag disagrees with BLOCK count")

    reset_namespace = raw_state["reset_namespace"]
    if not isinstance(reset_namespace, str) or reset_namespace not in APPROVED_RESET_NAMESPACES:
        raise _error(
            "E_UNAUTHORIZED_NAMESPACE", f"state {label} names an unapproved reset namespace"
        )
    attempt_id = _require_pattern(
        raw_state["authorized_attempt_id"],
        f"state {label} authorized_attempt_id",
        ATTEMPT_ID,
        code="E_MALFORMED_LEDGER",
    )

    permitted_removed_choices = _require_id_list(
        raw_state["permitted_removed_choices"],
        f"state {label} permitted_removed_choices",
        CALLER_CHOICE_ID,
        code="E_MALFORMED_LEDGER",
    )
    required_attack_matrix = _require_id_list(
        raw_state["required_attack_matrix"],
        f"state {label} required_attack_matrix",
        MATRIX_ITEM_ID,
        code="E_MALFORMED_LEDGER",
    )
    required_named_coverage = _require_id_list(
        raw_state["required_named_coverage"],
        f"state {label} required_named_coverage",
        MATRIX_ITEM_ID,
        code="E_MALFORMED_LEDGER",
    )

    raw_outcomes = raw_state["permitted_outcomes"]
    if not isinstance(raw_outcomes, Mapping) or not raw_outcomes:
        raise _error(
            "E_MALFORMED_LEDGER", f"state {label} permitted_outcomes must be a non-empty object"
        )
    permitted_outcomes: dict[str, str] = {}
    for outcome_id, outcome_kind in raw_outcomes.items():
        _require_pattern(
            outcome_id, f"state {label} outcome id", OUTCOME_ID, code="E_MALFORMED_LEDGER"
        )
        if outcome_id not in OUTCOME_CATALOG:
            raise _error(
                "E_MALFORMED_LEDGER",
                f"state {label} outcome id is not in the guard-owned outcome catalog",
            )
        declared_kind = _require_choice(
            outcome_kind, f"state {label} outcome kind", OUTCOME_KINDS, code="E_MALFORMED_LEDGER"
        )
        catalog_kind = OUTCOME_CATALOG[outcome_id]
        if declared_kind != catalog_kind:
            raise _error(
                "E_MALFORMED_LEDGER",
                f"state {label} outcome kind does not match the guard-owned outcome catalog",
            )
        permitted_outcomes[outcome_id] = catalog_kind

    return {
        "block_count": block_count,
        "architecture_reset_required": reset_required,
        "reset_namespace": reset_namespace,
        "authorized_attempt_id": attempt_id,
        "permitted_removed_choices": permitted_removed_choices,
        "permitted_outcomes": permitted_outcomes,
        "required_attack_matrix": required_attack_matrix,
        "required_named_coverage": required_named_coverage,
    }


def validate_ledger(ledger: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and return the canonical ledger object."""

    if not isinstance(ledger, Mapping):
        raise _error("E_MALFORMED_LEDGER", "ledger root must be an object")
    _require_string_keys(ledger, "ledger")
    _require_keys(ledger, LEDGER_KEYS, LEDGER_KEYS, "ledger")
    if ledger["schema_version"] != SCHEMA_VERSION:
        raise _error("E_UNKNOWN_LEDGER_STATE", f"ledger schema version must be {SCHEMA_VERSION}")

    boundaries = ledger["boundaries"]
    if not isinstance(boundaries, Mapping) or not boundaries:
        raise _error("E_MALFORMED_LEDGER", "ledger boundaries must be a non-empty object")

    normalized: dict[str, Any] = {"schema_version": SCHEMA_VERSION, "boundaries": {}}
    for boundary_id, raw_boundary in boundaries.items():
        _require_pattern(boundary_id, "ledger boundary id", BOUNDARY_ID, code="E_UNKNOWN_BOUNDARY")
        if not isinstance(raw_boundary, Mapping):
            raise _error("E_MALFORMED_LEDGER", f"boundary {boundary_id} must be an object")
        _require_keys(raw_boundary, BOUNDARY_KEYS, BOUNDARY_KEYS, f"boundary {boundary_id}")
        failure_classes = raw_boundary["failure_classes"]
        if not isinstance(failure_classes, Mapping) or not failure_classes:
            raise _error("E_MALFORMED_LEDGER", f"boundary {boundary_id} has no failure classes")
        normalized_classes: dict[str, Any] = {}
        for failure_class, raw_state in failure_classes.items():
            _require_pattern(
                failure_class,
                f"boundary {boundary_id} failure class",
                FAILURE_CLASS_ID,
                code="E_UNKNOWN_FAILURE_CLASS",
            )
            normalized_classes[failure_class] = _validate_failure_state(
                raw_state, f"{boundary_id}/{failure_class}"
            )
        normalized["boundaries"][boundary_id] = {"failure_classes": normalized_classes}
    return normalized


def load_ledger(path: Path) -> dict[str, Any]:
    return validate_ledger(_load_json(path, kind="ledger"))


def _lookup_state(
    ledger: Mapping[str, Any], boundary_id: str, failure_class: str
) -> dict[str, Any]:
    _require_pattern(boundary_id, "boundary_id", BOUNDARY_ID)
    _require_pattern(failure_class, "failure_class", FAILURE_CLASS_ID)
    boundaries = ledger["boundaries"]
    if boundary_id not in boundaries:
        raise _error("E_UNKNOWN_BOUNDARY", f"boundary {boundary_id} is not in the ledger")
    failure_classes = boundaries[boundary_id]["failure_classes"]
    if failure_class not in failure_classes:
        raise _error(
            "E_UNKNOWN_FAILURE_CLASS",
            f"failure class {boundary_id}/{failure_class} is not in the ledger",
        )
    state: dict[str, Any] = failure_classes[failure_class]
    return state


def record_block(ledger: Mapping[str, Any], boundary_id: str, failure_class: str) -> dict[str, Any]:
    """Return a new ledger with one BLOCK recorded; never mutates the input."""

    normalized = validate_ledger(ledger)
    state = _lookup_state(normalized, boundary_id, failure_class)
    current = int(state["block_count"])
    if current >= MAX_BLOCK_COUNT:
        raise _error(
            "E_BLOCK_COUNT_OVERFLOW", "BLOCK count cannot exceed the persisted integer contract"
        )
    state["block_count"] = current + 1
    state["architecture_reset_required"] = state["block_count"] >= 2
    return normalized


# ------------------------------------------------------------------- packet


def _validate_matrix(
    value: Any, field: str, required_complete: bool, ledger_items: list[str]
) -> dict[str, Any]:
    """Bind a matrix claim to the ledger contract; no caller text is accepted."""

    if not isinstance(value, Mapping):
        raise _error("E_INVALID_FIELD", f"{field} must be an object")
    _require_keys(value, MATRIX_KEYS, MATRIX_KEYS, field)
    status = _require_choice(value["status"], f"{field}.status", MATRIX_STATUSES)
    items = _require_id_list(value["items"], f"{field}.items", MATRIX_ITEM_ID, allow_empty=True)
    unknown = sorted(set(items) - set(ledger_items))
    if unknown:
        raise _error(
            "E_INCOMPLETE_COVERAGE", f"{field} names items absent from the ledger contract"
        )
    if required_complete and status != "complete":
        raise _error(
            "E_INCOMPLETE_COVERAGE", f"{field} must be complete for a completed engineering review"
        )
    if status == "complete" and items != ledger_items:
        raise _error("E_INCOMPLETE_COVERAGE", f"{field} does not exactly match the ledger contract")
    return {"status": status, "items": items}


def validate_packet(
    packet: Mapping[str, Any],
    ledger: Mapping[str, Any],
    *,
    require_complete_engineering_review: bool = False,
) -> dict[str, Any]:
    """Validate a packet against exact ledger state and return a PASS receipt."""

    if not isinstance(packet, Mapping):
        raise _error("E_MALFORMED_PACKET", "packet root must be an object")
    _require_string_keys(packet, "packet")

    if packet.get("schema_version") != SCHEMA_VERSION:
        raise _error("E_UNKNOWN_PACKET_STATE", f"packet schema version must be {SCHEMA_VERSION}")
    if "change_kind" not in packet:
        raise _error("E_MISSING_FIELD", "packet missing change_kind")
    change_kind = _require_choice(packet["change_kind"], "change_kind", CHANGE_KINDS)

    # Reset-only fields exist only on a reset packet.  Invalid states are unrepresentable.
    keys = (
        BASE_PACKET_KEYS | RESET_PACKET_KEYS
        if change_kind == ARCHITECTURE_RESET
        else BASE_PACKET_KEYS
    )
    _require_keys(packet, keys, keys, "packet")

    packet_id = _require_pattern(packet["packet_id"], "packet_id", PACKET_ID)
    packet_type = _require_choice(packet["packet_type"], "packet_type", PACKET_TYPES)
    boundary_id = _require_pattern(packet["boundary_id"], "boundary_id", BOUNDARY_ID)
    failure_class = _require_pattern(packet["failure_class"], "failure_class", FAILURE_CLASS_ID)
    if packet["ledger_ref"] != f"{boundary_id}/{failure_class}":
        raise _error(
            "E_PACKET_LEDGER_MISMATCH", "ledger_ref does not match boundary_id/failure_class"
        )

    ledger_state = validate_ledger(ledger)
    state = _lookup_state(ledger_state, boundary_id, failure_class)

    review_mode = _require_choice(packet["review_mode"], "review_mode", REVIEW_MODES)
    stop_policy = _require_choice(packet["stop_policy"], "stop_policy", STOP_POLICIES)
    review_status = _require_choice(packet["review_status"], "review_status", REVIEW_STATUSES)

    if require_complete_engineering_review:
        if packet_type != "review" or review_mode != ENGINEERING_SWEEP:
            raise _error(
                "E_INVALID_REVIEW_CLOSEOUT",
                "engineering review closeout requires an engineering-sweep review packet",
            )
        if review_status != "complete":
            raise _error(
                "E_INCOMPLETE_COVERAGE",
                "engineering review closeout requires review_status complete",
            )

    if review_mode == ENGINEERING_SWEEP:
        if change_kind == EXECUTION:
            raise _error(
                "E_INVALID_CHANGE_KIND", "an engineering sweep cannot execute the scientific path"
            )
        if stop_policy != COLLECT_NAMED_MATRIX:
            raise _error(
                "E_INVALID_STOP_POLICY", "an engineering sweep must collect its named matrix"
            )
    else:
        if change_kind != EXECUTION:
            raise _error(
                "E_INVALID_CHANGE_KIND", "a scientific/live gate change_kind must be execution"
            )
        if stop_policy != STOP_FIRST_ERROR:
            raise _error(
                "E_INVALID_STOP_POLICY", "a scientific/live gate must stop at the first error"
            )

    # The ledger, not any packet wording, decides whether a reset is authorized.
    if state["architecture_reset_required"]:
        if change_kind == LOCAL_REPAIR:
            raise _error("E_THIRD_LOCAL_REPAIR", "two BLOCKs require an architecture reset")
        if change_kind != ARCHITECTURE_RESET:
            raise _error(
                "E_ARCHITECTURE_RESET_REQUIRED", "the ledger requires an architecture reset"
            )
    elif change_kind == ARCHITECTURE_RESET:
        raise _error("E_RESET_NOT_TRIGGERED", "the ledger does not authorize an architecture reset")

    outcome_id = _require_pattern(
        packet["outcome_id"], "outcome_id", OUTCOME_ID, code="E_UNAUTHORIZED_OUTCOME"
    )
    outcome_kind = _require_choice(packet["outcome_kind"], "outcome_kind", OUTCOME_KINDS)
    permitted_outcomes: dict[str, str] = state["permitted_outcomes"]
    if outcome_id not in permitted_outcomes:
        raise _error(
            "E_UNAUTHORIZED_OUTCOME", "outcome_id is not a ledger-approved milestone identifier"
        )
    if permitted_outcomes[outcome_id] != outcome_kind:
        raise _error(
            "E_UNAUTHORIZED_OUTCOME", "outcome_kind does not match the ledger entry for outcome_id"
        )

    coverage = _require_id_list(
        packet["failure_class_coverage"], "failure_class_coverage", FAILURE_CLASS_ID
    )
    declared = set(ledger_state["boundaries"][boundary_id]["failure_classes"])
    if failure_class not in coverage:
        raise _error("E_INCOMPLETE_COVERAGE", "failure_class is absent from failure_class_coverage")
    unknown_classes = sorted(set(coverage) - declared)
    if unknown_classes:
        raise _error(
            "E_UNKNOWN_FAILURE_CLASS",
            f"failure_class_coverage names undeclared {','.join(unknown_classes)}",
        )

    matrices_complete = review_mode == ENGINEERING_SWEEP and review_status == "complete"
    attack_matrix = _validate_matrix(
        packet["attack_matrix"], "attack_matrix", matrices_complete, state["required_attack_matrix"]
    )
    named_coverage = _validate_matrix(
        packet["named_coverage"],
        "named_coverage",
        matrices_complete,
        state["required_named_coverage"],
    )

    normalized_packet: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "packet_id": packet_id,
        "packet_type": packet_type,
        "boundary_id": boundary_id,
        "failure_class": failure_class,
        "ledger_ref": f"{boundary_id}/{failure_class}",
        "review_mode": review_mode,
        "change_kind": change_kind,
        "outcome_kind": outcome_kind,
        "outcome_id": outcome_id,
        "failure_class_coverage": coverage,
        "stop_policy": stop_policy,
        "review_status": review_status,
        "attack_matrix": attack_matrix,
        "named_coverage": named_coverage,
    }

    if change_kind == ARCHITECTURE_RESET:
        reset_namespace = packet["reset_namespace"]
        if not isinstance(reset_namespace, str) or reset_namespace != state["reset_namespace"]:
            raise _error(
                "E_UNAUTHORIZED_NAMESPACE",
                "reset_namespace must equal the ledger-approved namespace",
            )
        attempt_id = _require_pattern(
            packet["attempt_id"], "attempt_id", ATTEMPT_ID, code="E_UNAUTHORIZED_ATTEMPT_ID"
        )
        if attempt_id != state["authorized_attempt_id"]:
            raise _error(
                "E_UNAUTHORIZED_ATTEMPT_ID",
                "attempt_id does not match the ledger-authorized attempt",
            )
        removed = _require_id_list(
            packet["removed_caller_choices"],
            "removed_caller_choices",
            CALLER_CHOICE_ID,
            code="E_UNAUTHORIZED_CALLER_CHOICE",
        )
        unknown_choices = sorted(set(removed) - set(state["permitted_removed_choices"]))
        if unknown_choices:
            raise _error(
                "E_UNAUTHORIZED_CALLER_CHOICE",
                f"removed_caller_choices names unapproved {','.join(unknown_choices)}",
            )
        normalized_packet["reset_namespace"] = reset_namespace
        normalized_packet["attempt_id"] = attempt_id
        normalized_packet["removed_caller_choices"] = removed

    # Snapshot both canonical inputs so later caller mutation cannot change the receipt.
    canonical_packet = copy.deepcopy(normalized_packet)
    canonical_ledger = copy.deepcopy(ledger_state)
    closeout_mode = bool(require_complete_engineering_review)
    receipt_body = {
        "schema_version": SCHEMA_VERSION,
        "status": "PASS",
        "packet_id": packet_id,
        "boundary_id": boundary_id,
        "failure_class": failure_class,
        "ledger_identity": f"{boundary_id}/{failure_class}",
        "packet_sha256": _digest(canonical_packet),
        "ledger_sha256": _digest(canonical_ledger),
        "review_mode": review_mode,
        "validation_mode": (
            "engineering_review_closeout" if closeout_mode else "standard"
        ),
        "closeout_mode": closeout_mode,
        "change_kind": change_kind,
        "outcome_kind": outcome_kind,
        "outcome_id": outcome_id,
        "review_status": review_status,
        "block_count": state["block_count"],
        "architecture_reset_required": state["architecture_reset_required"],
    }
    return {**receipt_body, "receipt_id": f"sha256:{_digest(receipt_body)}"}


# -------------------------------------------------------------- persistence


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(_canonical_json(value) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        try:
            directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        except OSError as exc:
            raise _error(
                "E_LEDGER_WRITE", "cannot open the ledger directory for durability"
            ) from exc
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except BaseException:
        with suppress(OSError):
            os.unlink(temporary)
        raise


@contextmanager
def _ledger_lock(path: Path) -> Iterator[None]:
    """Serialize read/modify/write cycles; flock releases the lock after a crash."""

    if fcntl is None:
        raise _error("E_LEDGER_CONTENTION", "concurrent ledger updates require POSIX file locking")
    lock_path = path.with_name(f".{path.name}.lock")
    try:
        lock_handle = lock_path.open("a+", encoding="utf-8")
    except OSError as exc:
        raise _error("E_LEDGER_CONTENTION", "cannot open the ledger lock") from exc
    try:
        try:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
        except OSError as exc:
            raise _error("E_LEDGER_CONTENTION", "cannot acquire the ledger lock") from exc
        yield
    finally:
        with suppress(OSError):
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)
        lock_handle.close()


def _record_block_file(path: Path, packet_path: Path) -> dict[str, Any]:
    """Record a closeout BLOCK under one lock after validating the fresh packet."""

    if not path.is_file():
        raise _error("E_MISSING_LEDGER", "ledger file is missing")
    with _ledger_lock(path):
        current = load_ledger(path)
        packet = _load_json(packet_path, kind="packet")
        closeout_receipt = validate_packet(
            packet,
            current,
            require_complete_engineering_review=True,
        )
        boundary_id = str(closeout_receipt["boundary_id"])
        failure_class = str(closeout_receipt["failure_class"])
        updated = record_block(current, boundary_id, failure_class)
        _write_json(path, updated)
        updated_state = _lookup_state(updated, boundary_id, failure_class)
        result_body = {
            "schema_version": SCHEMA_VERSION,
            "status": "BLOCK_RECORDED",
            "boundary_id": boundary_id,
            "failure_class": failure_class,
            "closeout_receipt_id": closeout_receipt["receipt_id"],
            "closeout_receipt": closeout_receipt,
            "ledger_sha256": _digest(updated),
            **updated_state,
        }
        result_body["result_id"] = f"sha256:{_digest(result_body)}"
        return result_body


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate an Agent+ anti-loop packet")
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--packet", type=Path)
    parser.add_argument("--record-block", action="store_true")
    parser.add_argument("--require-complete-engineering-review", action="store_true")
    parser.add_argument("--boundary-id")
    parser.add_argument("--failure-class")
    args = parser.parse_args(argv)
    try:
        if args.record_block:
            if (
                args.packet is None
                or not args.require_complete_engineering_review
                or args.boundary_id is not None
                or args.failure_class is not None
            ):
                raise _error(
                    "E_INVALID_COMMAND",
                    "record-block needs a packet, closeout validation, and no caller boundary/failure",
                )
            output = _record_block_file(args.ledger, args.packet)
        else:
            if args.packet is None:
                raise _error("E_MISSING_PACKET", "packet is required")
            ledger = load_ledger(args.ledger)
            packet = _load_json(args.packet, kind="packet")
            output = validate_packet(
                packet,
                ledger,
                require_complete_engineering_review=args.require_complete_engineering_review,
            )
        print(_canonical_json(output))
        return 0
    except GuardError as exc:
        print(f"ANTI_LOOP_GUARD_ERROR {exc.code} {exc.message}")
        return 1
    except OSError as exc:
        print(f"ANTI_LOOP_GUARD_ERROR E_LEDGER_WRITE {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
