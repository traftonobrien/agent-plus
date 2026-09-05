#!/usr/bin/env python3
"""Small, deterministic outcome audit and private-evidence receipt tool.

The module has two deliberately separate boundaries:

* outcome records are prospective, closed JSON records;
* private evidence is checked through the fixed ``.agent-plus/outcome-audit``
  project-local layout and produces a sanitized receipt.

No transcript, private path, or caller-supplied outcome is accepted.
"""

from __future__ import annotations

import argparse
import datetime as _datetime
import hashlib
import json
import math
import os
import re
import stat
import sys
from collections.abc import Mapping, Sequence
from itertools import pairwise
from pathlib import Path, PurePosixPath
from typing import Any

RECORD_SCHEMA = "agent-plus/outcome-record/v1"
RECORDS_SCHEMA = "agent-plus/outcome-record-set/v1"
REPORT_SCHEMA = "agent-plus/outcome-audit-report/v1"
ABSTENTION_SCHEMA = "agent-plus/outcome-abstention/v1"
EVIDENCE_MANIFEST_SCHEMA = "agent-plus/private-evidence-manifest/v1"
EVIDENCE_SOURCE_SCHEMA = "agent-plus/private-evidence-source/v1"
RECEIPT_SCHEMA = "agent-plus/private-evidence-receipt/v1"

OUTCOME_AUDIT_DIR = Path(".agent-plus") / "outcome-audit"
MANIFEST_RELATIVE = OUTCOME_AUDIT_DIR / "evidence-manifest.json"
RECEIPT_RELATIVE = OUTCOME_AUDIT_DIR / "receipt.json"
EVIDENCE_PREFIX = OUTCOME_AUDIT_DIR / "evidence"

STAGES = ("maker", "evaluator", "reviewer")
EVENT_STATUSES = ("PASS", "BLOCK", "ABSTAIN")
WORK_DISPOSITIONS = ("COMPLETED", "DEFERRED", "ABANDONED", "ABSTAINED")
SCIENTIFIC_ELIGIBILITY = ("ELIGIBLE", "INELIGIBLE", "ABSTAIN")
SCIENTIFIC_STATUS = ("PASS", "FAIL", "NOT_RUN", "ABSTAIN")

REF_PATTERN = re.compile(r"^ref:[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
DIGEST_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
FAILURE_PATTERN = re.compile(r"^[a-z][a-z0-9._-]{0,63}$")


class OutcomeAuditError(ValueError):
    """A typed, public-safe validation error."""

    def __init__(self, code: str, message: str = "invalid outcome-audit input") -> None:
        self.code = code
        super().__init__(message)


def _duplicate_reject(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if not isinstance(key, str):
            raise OutcomeAuditError("NON_STRING_KEY")
        if key in result:
            raise OutcomeAuditError("DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise OutcomeAuditError("NON_FINITE_JSON")


def strict_json_loads(raw: str | bytes) -> Any:
    """Load JSON with duplicate-key, non-string-key, and non-finite rejection."""

    try:
        return json.loads(
            raw,
            object_pairs_hook=_duplicate_reject,
            parse_constant=_reject_constant,
        )
    except OutcomeAuditError:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise OutcomeAuditError("MALFORMED_JSON") from exc


def canonical_json(value: Any) -> str:
    """Serialize a validated value in the one deterministic JSON form."""

    try:
        return json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise OutcomeAuditError("UNSERIALIZABLE_JSON") from exc


def canonical_bytes(value: Any) -> bytes:
    return canonical_json(value).encode("utf-8")


def sha256_digest(value: bytes | bytearray | memoryview) -> str:
    return "sha256:" + hashlib.sha256(bytes(value)).hexdigest()


def json_digest(value: Any) -> str:
    return sha256_digest(canonical_bytes(value))


def _exact_mapping(value: Any, keys: set[str], code: str = "SCHEMA_FIELDS") -> dict[str, Any]:
    if not isinstance(value, dict):
        raise OutcomeAuditError("SCHEMA_TYPE")
    if set(value) != keys:
        raise OutcomeAuditError(code)
    return value


def _string(value: Any, code: str = "SCHEMA_TYPE") -> str:
    if not isinstance(value, str):
        raise OutcomeAuditError(code)
    return value


def _enum(value: Any, choices: Sequence[str], code: str = "SCHEMA_ENUM") -> str:
    value = _string(value, code)
    if value not in choices:
        raise OutcomeAuditError(code)
    return value


def _ref(value: Any) -> str:
    value = _string(value, "OPAQUE_REF")
    if not REF_PATTERN.fullmatch(value):
        raise OutcomeAuditError("OPAQUE_REF")
    return value


def _digest(value: Any) -> str:
    value = _string(value, "DIGEST")
    if not DIGEST_PATTERN.fullmatch(value):
        raise OutcomeAuditError("DIGEST")
    return value


def _list(value: Any, code: str = "SCHEMA_TYPE") -> list[Any]:
    if not isinstance(value, list):
        raise OutcomeAuditError(code)
    return value


def _finite_number(value: Any, *, allow_null: bool = False) -> float | None:
    if value is None and allow_null:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise OutcomeAuditError("MEASURED_DURATION")
    if not math.isfinite(float(value)) or float(value) < 0:
        raise OutcomeAuditError("MEASURED_DURATION")
    return float(value)


def _timestamp(value: Any) -> str:
    value = _string(value, "TIMESTAMP")
    if not value.endswith("Z"):
        raise OutcomeAuditError("TIMESTAMP")
    try:
        parsed = _datetime.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        raise OutcomeAuditError("TIMESTAMP") from exc
    if parsed.tzinfo is None:
        raise OutcomeAuditError("TIMESTAMP")
    return value


def _validate_event(event: Any) -> dict[str, Any]:
    event = _exact_mapping(
        event,
        {"event_ref", "stage", "status", "occurred_at", "evidence_refs", "failure_code", "duration_seconds"},
        "EVENT_FIELDS",
    )
    _ref(event["event_ref"])
    _enum(event["stage"], STAGES, "EVENT_STAGE")
    status = _enum(event["status"], EVENT_STATUSES, "EVENT_STATUS")
    occurred_at = _timestamp(event["occurred_at"])
    refs = _list(event["evidence_refs"], "EVIDENCE_REFS")
    for ref in refs:
        _ref(ref)
    if len(refs) != len(set(refs)):
        raise OutcomeAuditError("DUPLICATE_EVIDENCE_REF")
    failure_code = event["failure_code"]
    if status == "BLOCK":
        failure_code = _string(failure_code, "CAUSAL_FAILURE")
        if not FAILURE_PATTERN.fullmatch(failure_code):
            raise OutcomeAuditError("CAUSAL_FAILURE")
        if not refs:
            raise OutcomeAuditError("CAUSAL_FAILURE_EVIDENCE")
    elif failure_code is not None:
        raise OutcomeAuditError("DUPLICATE_TERMINAL_AUTHORITY")
    duration = _finite_number(event["duration_seconds"], allow_null=True)
    return {
        "event_ref": event["event_ref"],
        "stage": event["stage"],
        "status": status,
        "occurred_at": occurred_at,
        "evidence_refs": list(refs),
        "failure_code": failure_code,
        "duration_seconds": duration,
    }


def validate_record(record: Any) -> dict[str, Any]:
    """Validate one closed prospective record and derive terminal authority."""

    record = _exact_mapping(
        record,
        {"schema_version", "record_ref", "work_item_ref", "attempt_ref", "created_at", "events", "work_item", "scientific", "provenance"},
        "RECORD_FIELDS",
    )
    if record["schema_version"] != RECORD_SCHEMA:
        raise OutcomeAuditError("SCHEMA_VERSION")
    record_ref = _ref(record["record_ref"])
    work_item_ref = _ref(record["work_item_ref"])
    attempt_ref = _ref(record["attempt_ref"])
    created_at = _timestamp(record["created_at"])

    events_raw = _list(record["events"], "EVENTS")
    if not 1 <= len(events_raw) <= len(STAGES):
        raise OutcomeAuditError("EVENT_COUNT")
    events = [_validate_event(event) for event in events_raw]
    stages = [event["stage"] for event in events]
    if tuple(stages) != STAGES[: len(stages)]:
        raise OutcomeAuditError("EVENT_ORDER")
    if len({event["event_ref"] for event in events}) != len(events):
        raise OutcomeAuditError("DUPLICATE_EVENT_REF")
    timestamps = [
        _datetime.datetime.fromisoformat(event["occurred_at"][:-1] + "+00:00")
        for event in events
    ]
    if any(left > right for left, right in pairwise(timestamps)):
        raise OutcomeAuditError("EVENT_TIME_ORDER")

    terminal = events[-1]
    if terminal["status"] == "PASS" and len(events) != len(STAGES):
        raise OutcomeAuditError("MISSING_TERMINAL_AUTHORITY")
    if any(event["status"] != "PASS" for event in events[:-1]):
        raise OutcomeAuditError("TERMINAL_CONTINUATION")
    if terminal["status"] == "PASS":
        attempt_outcome = "PASS"
        terminal_failure: dict[str, str] | None = None
    elif terminal["status"] == "BLOCK":
        attempt_outcome = "BLOCK"
        terminal_failure = {"stage": terminal["stage"], "code": terminal["failure_code"]}
    else:
        attempt_outcome = "ABSTAIN"
        terminal_failure = None

    work_item = _exact_mapping(record["work_item"], {"disposition"}, "WORK_ITEM_FIELDS")
    disposition = _enum(work_item["disposition"], WORK_DISPOSITIONS, "WORK_ITEM_DISPOSITION")

    scientific = _exact_mapping(record["scientific"], {"eligibility", "status"}, "SCIENTIFIC_FIELDS")
    eligibility = _enum(scientific["eligibility"], SCIENTIFIC_ELIGIBILITY, "SCIENTIFIC_ELIGIBILITY")
    scientific_status = _enum(scientific["status"], SCIENTIFIC_STATUS, "SCIENTIFIC_STATUS")
    if eligibility == "ABSTAIN" and scientific_status != "ABSTAIN":
        raise OutcomeAuditError("SCIENTIFIC_CONTRADICTION")
    if eligibility == "INELIGIBLE" and scientific_status == "PASS":
        raise OutcomeAuditError("SCIENTIFIC_CONTRADICTION")

    provenance = _exact_mapping(
        record["provenance"],
        {"source_refs", "input_digest", "contract_digest"},
        "PROVENANCE_FIELDS",
    )
    source_refs = _list(provenance["source_refs"], "PROVENANCE_REFS")
    if not source_refs:
        raise OutcomeAuditError("PROVENANCE_REFS")
    for ref in source_refs:
        _ref(ref)
    if len(source_refs) != len(set(source_refs)):
        raise OutcomeAuditError("PROVENANCE_REFS")
    input_digest = _digest(provenance["input_digest"])
    contract_digest = _digest(provenance["contract_digest"])

    normalized = {
        "schema_version": RECORD_SCHEMA,
        "record_ref": record_ref,
        "work_item_ref": work_item_ref,
        "attempt_ref": attempt_ref,
        "created_at": created_at,
        "events": events,
        "work_item": {"disposition": disposition},
        "scientific": {"eligibility": eligibility, "status": scientific_status},
        "provenance": {
            "source_refs": list(source_refs),
            "input_digest": input_digest,
            "contract_digest": contract_digest,
        },
    }
    return {
        "record": normalized,
        "record_ref": record_ref,
        "work_item_ref": work_item_ref,
        "attempt_ref": attempt_ref,
        "attempt_outcome": attempt_outcome,
        "terminal_failure": terminal_failure,
        "terminal_stage": terminal["stage"],
        "work_item_disposition": disposition,
        "scientific_eligibility": eligibility,
        "scientific_status": scientific_status,
    }


def validate_record_set(value: Any) -> list[dict[str, Any]]:
    """Validate a record array or the explicit closed record-set wrapper."""

    if isinstance(value, list):
        raw_records = value
    elif isinstance(value, dict):
        wrapper = _exact_mapping(value, {"schema_version", "records"}, "RECORD_SET_FIELDS")
        if wrapper["schema_version"] != RECORDS_SCHEMA:
            raise OutcomeAuditError("SCHEMA_VERSION")
        raw_records = _list(wrapper["records"], "RECORDS")
    else:
        raise OutcomeAuditError("RECORD_SET_TYPE")
    records = [validate_record(record) for record in raw_records]
    record_refs = [entry["record_ref"] for entry in records]
    attempt_refs = [entry["attempt_ref"] for entry in records]
    if len(record_refs) != len(set(record_refs)) or len(attempt_refs) != len(set(attempt_refs)):
        raise OutcomeAuditError("DUPLICATE_RECORD")
    seen_attempt_times: set[tuple[str, str]] = set()
    for entry in records:
        key = (entry["work_item_ref"], entry["record"]["created_at"])
        if key in seen_attempt_times:
            raise OutcomeAuditError("AMBIGUOUS_ATTEMPT_ORDER")
        seen_attempt_times.add(key)
    return records


def abstain_ambiguous_history(reason: str = "AMBIGUOUS_HISTORY") -> dict[str, str]:
    """Return an explicit abstention for legacy or ambiguous history."""

    if not isinstance(reason, str) or reason not in {
        "AMBIGUOUS_HISTORY",
        "MISSING_PROSPECTIVE_RECORD",
        "UNSTRUCTURED_HISTORY",
    }:
        raise OutcomeAuditError("ABSTENTION_REASON")
    return {"schema_version": ABSTENTION_SCHEMA, "status": "ABSTAIN", "reason": reason}


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> dict[str, float] | None:
    if (
        isinstance(successes, bool)
        or isinstance(trials, bool)
        or not isinstance(successes, int)
        or not isinstance(trials, int)
        or successes < 0
        or trials < 0
        or successes > trials
    ):
        raise OutcomeAuditError("STATISTICS_INPUT")
    if trials == 0:
        return None
    if not math.isfinite(z) or z <= 0:
        raise OutcomeAuditError("STATISTICS_INPUT")
    n = float(trials)
    p = float(successes) / n
    denominator = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denominator
    half = z * math.sqrt((p * (1.0 - p) / n) + (z * z / (4.0 * n * n))) / denominator
    return {"lower": max(0.0, centre - half), "upper": min(1.0, centre + half)}


def _ratio(successes: int, trials: int, bands: Any = None, metric: str = "") -> dict[str, Any]:
    interval = wilson_interval(successes, trials)
    rate = None if trials == 0 else float(successes) / float(trials)
    grade = _grade(rate, bands, metric)
    return {
        "numerator": successes,
        "denominator": trials,
        "rate": rate,
        "wilson_95": interval,
        "grade": grade,
    }


def _grade(rate: float | None, bands: Any, metric: str) -> str:
    if rate is None or bands is None:
        return "UNRATED"
    entries = bands.get(metric)
    if entries is None:
        return "UNRATED"
    for band in entries:
        if band["minimum"] <= rate <= band["maximum"]:
            return band["grade"]
    return "UNRATED"


def validate_bands(value: Any) -> dict[str, list[dict[str, Any]]]:
    if not isinstance(value, dict):
        raise OutcomeAuditError("BANDS_TYPE")
    result: dict[str, list[dict[str, Any]]] = {}
    for metric, entries in value.items():
        if not isinstance(metric, str) or not isinstance(entries, list) or not entries:
            raise OutcomeAuditError("BANDS_SCHEMA")
        previous = -1.0
        normalized: list[dict[str, Any]] = []
        for entry in entries:
            entry = _exact_mapping(entry, {"minimum", "maximum", "grade"}, "BANDS_SCHEMA")
            minimum = _finite_number(entry["minimum"])
            maximum = _finite_number(entry["maximum"])
            grade = _string(entry["grade"], "BANDS_SCHEMA")
            if minimum is None or maximum is None or minimum < 0 or maximum > 1 or minimum > maximum or minimum < previous:
                raise OutcomeAuditError("BANDS_SCHEMA")
            if not grade or grade == "UNRATED":
                raise OutcomeAuditError("BANDS_SCHEMA")
            previous = minimum
            normalized.append({"minimum": minimum, "maximum": maximum, "grade": grade})
        result[metric] = normalized
    return result


def report(records: Sequence[dict[str, Any]], bands: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Build a deterministic scorecard from already validated records."""

    entries = list(records)
    if entries and (not isinstance(entries[0], dict) or "attempt_outcome" not in entries[0]):
        entries = validate_record_set(entries)
    if any(not isinstance(entry, dict) or "attempt_outcome" not in entry for entry in entries):
        raise OutcomeAuditError("REPORT_INPUT")
    normalized_bands = validate_bands(bands) if bands is not None else None
    by_work: dict[str, list[dict[str, Any]]] = {}
    for entry in entries:
        by_work.setdefault(entry["work_item_ref"], []).append(entry)
    for work_entries in by_work.values():
        work_entries.sort(key=lambda entry: (entry["record"]["created_at"], entry["attempt_ref"]))
    first_pass_entries = [work_entries[0] for work_entries in by_work.values()]
    first_pass_successes = sum(entry["attempt_outcome"] == "PASS" for entry in first_pass_entries)
    eventual_successes = sum(any(entry["attempt_outcome"] == "PASS" for entry in work_entries) for work_entries in by_work.values())

    reviewer_entries = [entry for entry in entries if entry["terminal_stage"] == "reviewer"]
    reviewer_escapes = sum(
        entry["attempt_outcome"] == "BLOCK"
        and entry["terminal_failure"] is not None
        and entry["terminal_failure"]["stage"] == "reviewer"
        for entry in reviewer_entries
    )
    eligible_science = [
        entry
        for entry in entries
        if entry["scientific_eligibility"] == "ELIGIBLE"
        and entry["scientific_status"] in {"PASS", "FAIL"}
    ]
    eligible_science_success = sum(entry["scientific_status"] == "PASS" for entry in eligible_science)
    failures = [entry for entry in entries if entry["attempt_outcome"] == "BLOCK"]
    failure_codes: dict[str, int] = {}
    for entry in failures:
        failure = entry["terminal_failure"]
        if failure is not None:
            failure_codes[failure["code"]] = failure_codes.get(failure["code"], 0) + 1

    duration_values: list[float] = []
    for entry in entries:
        durations = [event["duration_seconds"] for event in entry["record"]["events"]]
        if all(duration is not None for duration in durations):
            duration_values.append(sum(float(duration) for duration in durations))
    duration_values.sort()
    work_count = len(by_work)
    attempt_count = len(entries)
    duration_summary: dict[str, Any]
    if duration_values:
        duration_summary = {
            "measured_attempts": len(duration_values),
            "total_seconds": sum(duration_values),
            "mean_seconds": sum(duration_values) / len(duration_values),
            "minimum_seconds": duration_values[0],
            "maximum_seconds": duration_values[-1],
        }
    else:
        duration_summary = {
            "measured_attempts": 0,
            "total_seconds": None,
            "mean_seconds": None,
            "minimum_seconds": None,
            "maximum_seconds": None,
        }

    metrics = {
        "first_pass_quality": _ratio(first_pass_successes, work_count, normalized_bands, "first_pass_quality"),
        "eventual_reliability": _ratio(eventual_successes, work_count, normalized_bands, "eventual_reliability"),
        "reviewer_escape": _ratio(reviewer_escapes, len(reviewer_entries), normalized_bands, "reviewer_escape"),
        "eligible_scientific_success": _ratio(
            eligible_science_success, len(eligible_science), normalized_bands, "eligible_scientific_success"
        ),
    }
    failure_concentration = {
        code: _ratio(count, len(failures), normalized_bands, "failure_concentration")
        for code, count in sorted(failure_codes.items())
    }
    grades = {name: metric["grade"] for name, metric in metrics.items()}
    grades["failure_concentration"] = {
        code: metric["grade"] for code, metric in failure_concentration.items()
    }
    return {
        "schema_version": REPORT_SCHEMA,
        "attempt_count": attempt_count,
        "work_item_count": work_count,
        "metrics": metrics,
        "failure_concentration": failure_concentration,
        "duration_seconds": duration_summary,
        "attempts_per_work_item": {
            "attempts": attempt_count,
            "work_items": work_count,
            "mean": None if work_count == 0 else float(attempt_count) / float(work_count),
        },
        "multi_attempt_frequency": _ratio(
            sum(len(work_entries) > 1 for work_entries in by_work.values()),
            work_count,
            normalized_bands,
            "multi_attempt_frequency",
        ),
        "grades": grades,
    }


def _manifest_path(root: Path) -> Path:
    return root / MANIFEST_RELATIVE


def _safe_relative(value: Any) -> str:
    value = _string(value, "SOURCE_PATH")
    if not value or "\\" in value:
        raise OutcomeAuditError("TRAVERSAL")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise OutcomeAuditError("TRAVERSAL")
    return value


def _read_regular_relative(root: Path, relative: str) -> bytes:
    """Read one regular file without following path components or the leaf."""

    relative = _safe_relative(relative)
    parts = PurePosixPath(relative).parts
    if not parts:
        raise OutcomeAuditError("TRAVERSAL")
    try:
        root = root.resolve()
    except (OSError, RuntimeError) as exc:
        raise OutcomeAuditError("PROJECT_ROOT") from exc
    root_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        parent_fd = os.open(root, root_flags)
    except FileNotFoundError as exc:
        raise OutcomeAuditError("MISSING") from exc
    except PermissionError as exc:
        raise OutcomeAuditError("DENIED") from exc
    except OSError as exc:
        raise OutcomeAuditError("EVIDENCE_READ") from exc
    try:
        for index, part in enumerate(parts):
            flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
            if index < len(parts) - 1:
                flags |= getattr(os, "O_DIRECTORY", 0)
            try:
                child_fd = os.open(part, flags, dir_fd=parent_fd)
            except FileNotFoundError as exc:
                raise OutcomeAuditError("MISSING") from exc
            except PermissionError as exc:
                raise OutcomeAuditError("DENIED") from exc
            except OSError as exc:
                raise OutcomeAuditError("SYMLINK_OR_NONREGULAR") from exc
            os.close(parent_fd)
            parent_fd = child_fd
        info = os.fstat(parent_fd)
        if not stat.S_ISREG(info.st_mode):
            raise OutcomeAuditError("NONREGULAR")
        chunks: list[bytes] = []
        with os.fdopen(parent_fd, "rb") as stream:
            parent_fd = -1
            while True:
                chunk = stream.read(1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
        return b"".join(chunks)
    finally:
        if parent_fd >= 0:
            os.close(parent_fd)


def _open_directory_relative(root: Path, relative: str) -> int:
    """Open one fixed-layout directory without following any path component."""

    relative = _safe_relative(relative)
    parts = PurePosixPath(relative).parts
    if not parts:
        raise OutcomeAuditError("TRAVERSAL")
    try:
        root = root.resolve()
    except (OSError, RuntimeError) as exc:
        raise OutcomeAuditError("PROJECT_ROOT") from exc
    root_flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        parent_fd = os.open(root, root_flags)
    except FileNotFoundError as exc:
        raise OutcomeAuditError("MISSING") from exc
    except PermissionError as exc:
        raise OutcomeAuditError("DENIED") from exc
    except OSError as exc:
        raise OutcomeAuditError("EVIDENCE_READ") from exc
    try:
        for part in parts:
            flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
            try:
                child_fd = os.open(part, flags, dir_fd=parent_fd)
            except FileNotFoundError as exc:
                raise OutcomeAuditError("MISSING") from exc
            except PermissionError as exc:
                raise OutcomeAuditError("DENIED") from exc
            except OSError as exc:
                raise OutcomeAuditError("SYMLINK_OR_NONREGULAR") from exc
            os.close(parent_fd)
            parent_fd = child_fd
        if not stat.S_ISDIR(os.fstat(parent_fd).st_mode):
            raise OutcomeAuditError("NONREGULAR")
        result = parent_fd
        parent_fd = -1
        return result
    finally:
        if parent_fd >= 0:
            os.close(parent_fd)


def _enumerate_evidence_entries(root: Path) -> set[str]:
    """Return the exact direct evidence entries without following symlinks."""

    evidence_fd = _open_directory_relative(root, str(EVIDENCE_PREFIX))
    entries: set[str] = set()
    try:
        try:
            directory_entries = list(os.scandir(evidence_fd))
        except (OSError, TypeError) as exc:
            raise OutcomeAuditError("EVIDENCE_READ") from exc
        for entry in directory_entries:
            if entry.is_symlink():
                raise OutcomeAuditError("SYMLINK_OR_NONREGULAR")
            try:
                info = entry.stat(follow_symlinks=False)
            except OSError as exc:
                raise OutcomeAuditError("EVIDENCE_READ") from exc
            if not stat.S_ISREG(info.st_mode):
                raise OutcomeAuditError("NONREGULAR")
            if not entry.name.endswith(".json"):
                raise OutcomeAuditError("NON_JSON_ENTRY")
            entries.add(str(EVIDENCE_PREFIX / entry.name))
    finally:
        os.close(evidence_fd)
    return entries


def _validate_source_document(value: Any) -> tuple[str, list[str], list[str]]:
    value = _exact_mapping(value, {"schema_version", "source_ref", "items"}, "SOURCE_SCHEMA")
    if value["schema_version"] != EVIDENCE_SOURCE_SCHEMA:
        raise OutcomeAuditError("SOURCE_SCHEMA")
    source_ref = _ref(value["source_ref"])
    items = _list(value["items"], "SOURCE_ITEMS")
    refs: list[str] = []
    digests: list[str] = []
    for item in items:
        item = _exact_mapping(item, {"item_ref", "item_digest"}, "SOURCE_ITEM_SCHEMA")
        refs.append(_ref(item["item_ref"]))
        digests.append(_digest(item["item_digest"]))
    if len(refs) != len(set(refs)):
        raise OutcomeAuditError("DUPLICATE_BINDING")
    return source_ref, refs, digests


def _source_set_digest(sources: Sequence[dict[str, Any]]) -> str:
    return json_digest(
        [
            {
                "source_ref": source["source_ref"],
                "relative_path": source["relative_path"],
                "content_digest": source["content_digest"],
                "item_count": source["item_count"],
            }
            for source in sorted(sources, key=lambda item: item["source_ref"])
        ]
    )


def _binding_digest(source_ref: str, refs: Sequence[str], digests: Sequence[str]) -> str:
    return json_digest(
        {
            "source_ref": source_ref,
            "item_refs": list(refs),
            "item_digests": list(digests),
            "item_count": len(refs),
        }
    )


def _binding_set_digest(bindings: Sequence[dict[str, Any]]) -> str:
    return json_digest(
        [
            {
                "source_ref": binding["source_ref"],
                "item_refs": binding["item_refs"],
                "item_digests": binding["item_digests"],
                "item_count": binding["item_count"],
                "binding_digest": binding["binding_digest"],
            }
            for binding in sorted(bindings, key=lambda item: item["source_ref"])
        ]
    )


def _block_receipt(code: str) -> dict[str, Any]:
    return {"schema_version": RECEIPT_SCHEMA, "status": "BLOCK", "error_code": code}


def verify_private_evidence() -> dict[str, Any]:
    """Verify fixed-layout private evidence and return a sanitized receipt."""

    root = Path.cwd()
    try:
        manifest_raw = _read_regular_relative(root, str(MANIFEST_RELATIVE))
        manifest = strict_json_loads(manifest_raw)
        manifest = _exact_mapping(
            manifest,
            {"schema_version", "contract_digest", "population_digest", "source_count", "sources", "bindings", "source_set_digest", "binding_set_digest"},
            "MANIFEST_SCHEMA",
        )
        if manifest["schema_version"] != EVIDENCE_MANIFEST_SCHEMA:
            raise OutcomeAuditError("MANIFEST_SCHEMA")
        contract_digest = _digest(manifest["contract_digest"])
        population_digest = _digest(manifest["population_digest"])
        source_count = manifest["source_count"]
        if isinstance(source_count, bool) or not isinstance(source_count, int) or source_count < 1:
            raise OutcomeAuditError("SOURCE_COUNT")
        source_entries = _list(manifest["sources"], "MANIFEST_SOURCES")
        binding_entries = _list(manifest["bindings"], "MANIFEST_BINDINGS")
        if len(source_entries) != source_count or len(binding_entries) != source_count:
            raise OutcomeAuditError("SOURCE_COUNT")
        declared_paths: set[str] = set()
        expected_prefix = str(EVIDENCE_PREFIX) + "/"
        for raw_source in source_entries:
            source = _exact_mapping(
                raw_source,
                {"source_ref", "relative_path", "content_digest", "item_count"},
                "SOURCE_ENTRY_SCHEMA",
            )
            relative_path = _safe_relative(source["relative_path"])
            path = PurePosixPath(relative_path)
            if (
                not relative_path.startswith(expected_prefix)
                or path.parent != PurePosixPath(str(EVIDENCE_PREFIX))
                or not path.name.endswith(".json")
            ):
                raise OutcomeAuditError("FIXED_RECEIPT_INTERFACE")
            if relative_path in declared_paths:
                raise OutcomeAuditError("DUPLICATE_SOURCE_PATH")
            declared_paths.add(relative_path)
        actual_paths = _enumerate_evidence_entries(root)
        if actual_paths != declared_paths:
            if declared_paths - actual_paths:
                raise OutcomeAuditError("MISSING_SOURCE")
            raise OutcomeAuditError("EXTRA_SOURCE")
        sources: list[dict[str, Any]] = []
        seen_refs: set[str] = set()
        for source in source_entries:
            source = _exact_mapping(source, {"source_ref", "relative_path", "content_digest", "item_count"}, "SOURCE_ENTRY_SCHEMA")
            source_ref = _ref(source["source_ref"])
            if source_ref in seen_refs:
                raise OutcomeAuditError("DUPLICATE_SOURCE")
            seen_refs.add(source_ref)
            relative_path = _safe_relative(source["relative_path"])
            item_count = source["item_count"]
            if isinstance(item_count, bool) or not isinstance(item_count, int) or item_count < 0:
                raise OutcomeAuditError("SOURCE_COUNT")
            content_digest = _digest(source["content_digest"])
            source_raw = _read_regular_relative(root, relative_path)
            if sha256_digest(source_raw) != content_digest:
                raise OutcomeAuditError("SOURCE_HASH_MISMATCH")
            source_doc = strict_json_loads(source_raw)
            actual_ref, item_refs, item_digests = _validate_source_document(source_doc)
            if actual_ref != source_ref or len(item_refs) != item_count:
                raise OutcomeAuditError("SOURCE_BINDING_MISMATCH")
            sources.append(
                {
                    "source_ref": source_ref,
                    "relative_path": relative_path,
                    "content_digest": content_digest,
                    "item_count": item_count,
                    "item_refs": item_refs,
                    "item_digests": item_digests,
                }
            )
        if _source_set_digest(sources) != _digest(manifest["source_set_digest"]):
            raise OutcomeAuditError("SOURCE_SET_MISMATCH")

        bindings: list[dict[str, Any]] = []
        binding_refs: set[str] = set()
        by_ref = {source["source_ref"]: source for source in sources}
        for raw_binding in binding_entries:
            binding = _exact_mapping(raw_binding, {"source_ref", "item_refs", "item_digests", "item_count", "binding_digest"}, "BINDING_SCHEMA")
            source_ref = _ref(binding["source_ref"])
            if source_ref in binding_refs or source_ref not in by_ref:
                raise OutcomeAuditError("DUPLICATE_BINDING")
            binding_refs.add(source_ref)
            item_refs = [_ref(ref) for ref in _list(binding["item_refs"], "BINDING_SCHEMA")]
            item_digests = [_digest(digest) for digest in _list(binding["item_digests"], "BINDING_SCHEMA")]
            item_count = binding["item_count"]
            if isinstance(item_count, bool) or not isinstance(item_count, int) or item_count < 0:
                raise OutcomeAuditError("BINDING_SCHEMA")
            source = by_ref[source_ref]
            if item_refs != source["item_refs"] or item_digests != source["item_digests"] or item_count != source["item_count"]:
                raise OutcomeAuditError("BINDING_MISMATCH")
            binding_digest = _digest(binding["binding_digest"])
            if binding_digest != _binding_digest(source_ref, item_refs, item_digests):
                raise OutcomeAuditError("BINDING_HASH_MISMATCH")
            bindings.append(
                {
                    "source_ref": source_ref,
                    "item_refs": item_refs,
                    "item_digests": item_digests,
                    "item_count": item_count,
                    "binding_digest": binding_digest,
                }
            )
        if binding_refs != seen_refs or _binding_set_digest(bindings) != _digest(manifest["binding_set_digest"]):
            raise OutcomeAuditError("BINDING_SET_MISMATCH")

        summaries = [
            {
                "ordinal": ordinal,
                "content_digest": source["content_digest"],
                "item_count": source["item_count"],
                "binding_digest": next(
                    binding["binding_digest"] for binding in bindings if binding["source_ref"] == source["source_ref"]
                ),
            }
            for ordinal, source in enumerate(sorted(sources, key=lambda item: item["source_ref"]), start=1)
        ]
        unsigned = {
            "schema_version": RECEIPT_SCHEMA,
            "status": "PASS",
            "contract_digest": contract_digest,
            "population_digest": population_digest,
            "source_count": source_count,
            "source_set_digest": _digest(manifest["source_set_digest"]),
            "binding_set_digest": _digest(manifest["binding_set_digest"]),
            "sources": summaries,
        }
        receipt = dict(unsigned)
        receipt["receipt_digest"] = json_digest(unsigned)
        return receipt
    except OutcomeAuditError as exc:
        return _block_receipt(exc.code)
    except (OSError, UnicodeError, TypeError, ValueError):
        return _block_receipt("DENIED_OR_UNSTRUCTURED")


def write_fixed_receipt() -> dict[str, Any]:
    """Verify the current project and write its generated receipt to the fixed path."""

    root = Path.cwd().resolve()
    receipt = verify_private_evidence()
    base = root / OUTCOME_AUDIT_DIR
    parent = root / ".agent-plus"
    for directory in (parent, base):
        try:
            if directory.exists():
                if directory.is_symlink() or not directory.is_dir():
                    raise OSError("fixed receipt directory is not a regular directory")
            else:
                directory.mkdir()
        except FileExistsError as exc:
            raise OSError("fixed receipt directory race") from exc
    target = root / RECEIPT_RELATIVE
    temporary = base / ".receipt.json.tmp"
    payload = (canonical_json(dict(receipt)) + "\n").encode("utf-8")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    fd = os.open(temporary, flags, 0o600)
    try:
        with os.fdopen(fd, "wb") as stream:
            fd = -1
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
    finally:
        if fd >= 0:
            os.close(fd)
    os.replace(temporary, target)
    return receipt


def _read_json_file(path: Path) -> Any:
    try:
        return strict_json_loads(path.read_bytes())
    except FileNotFoundError as exc:
        raise OutcomeAuditError("MISSING") from exc
    except PermissionError as exc:
        raise OutcomeAuditError("DENIED") from exc


def _print_json(value: Any) -> None:
    print(canonical_json(value))


def _command_validate(path: Path) -> int:
    try:
        records = validate_record_set(_read_json_file(path))
        _print_json({"status": "PASS", "record_count": len(records)})
        return 0
    except OutcomeAuditError as exc:
        _print_json({"status": "BLOCK", "error_code": exc.code})
        return 1


def _command_report(path: Path, bands_path: Path | None) -> int:
    try:
        records = validate_record_set(_read_json_file(path))
        bands = None if bands_path is None else _read_json_file(bands_path)
        _print_json(report(records, bands))
        return 0
    except OutcomeAuditError as exc:
        _print_json({"status": "BLOCK", "error_code": exc.code})
        return 1


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate closed outcome records and fixed-layout evidence receipts.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    validate = subparsers.add_parser("validate")
    validate.add_argument("records", type=Path)
    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("records", type=Path)
    report_parser.add_argument("--bands", type=Path)
    subparsers.add_parser("receipt")
    abstain = subparsers.add_parser("abstain")
    abstain.add_argument("--reason", default="AMBIGUOUS_HISTORY")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "validate":
        return _command_validate(args.records)
    if args.command == "report":
        return _command_report(args.records, args.bands)
    if args.command == "abstain":
        try:
            _print_json(abstain_ambiguous_history(args.reason))
            return 0
        except OutcomeAuditError as exc:
            _print_json({"status": "BLOCK", "error_code": exc.code})
            return 1
    if args.command == "receipt":
        try:
            receipt = write_fixed_receipt()
        except (OSError, ValueError):
            _print_json(_block_receipt("RECEIPT_WRITE"))
            return 1
        _print_json(receipt)
        return 0 if receipt["status"] == "PASS" else 1
    raise AssertionError("unreachable")


if __name__ == "__main__":
    sys.exit(main())
