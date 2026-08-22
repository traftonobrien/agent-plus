from __future__ import annotations

import importlib.util
import inspect
import json
import os
import socket
import stat
import subprocess
import tempfile
import unittest
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "skills" / "outcome-audit" / "outcome_audit.py"
SPEC = importlib.util.spec_from_file_location("outcome_audit", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def digest(raw: bytes) -> str:
    return "sha256:" + sha256(raw).hexdigest()


def event(stage: str, status: str = "PASS", index: int = 1, failure: str | None = None, duration: float | None = 1.0) -> dict:
    return {
        "event_ref": f"ref:event-{index}",
        "stage": stage,
        "status": status,
        "occurred_at": f"2026-08-22T00:0{index}:00Z",
        "evidence_refs": [] if status != "BLOCK" else [f"ref:evidence-{index}"],
        "failure_code": failure,
        "duration_seconds": duration,
    }


def record(
    work: str,
    attempt: str,
    statuses: tuple[str, ...] = ("PASS", "PASS", "PASS"),
    failure: str = "contract",
    created: str = "2026-08-22T00:00:00Z",
    eligibility: str = "ELIGIBLE",
    scientific_status: str = "PASS",
    durations: tuple[float | None, ...] = (1.0, 2.0, 3.0),
) -> dict:
    events = []
    for index, status in enumerate(statuses, start=1):
        events.append(
            event(
                ("maker", "evaluator", "reviewer")[index - 1],
                status,
                index,
                failure if status == "BLOCK" else None,
                durations[index - 1],
            )
        )
    return {
        "schema_version": MODULE.RECORD_SCHEMA,
        "record_ref": f"ref:record-{attempt}",
        "work_item_ref": f"ref:work-{work}",
        "attempt_ref": f"ref:attempt-{attempt}",
        "created_at": created,
        "events": events,
        "work_item": {"disposition": "COMPLETED"},
        "scientific": {"eligibility": eligibility, "status": scientific_status},
        "provenance": {
            "source_refs": ["ref:source-synthetic"],
            "input_digest": digest(b"input"),
            "contract_digest": digest(b"contract"),
        },
    }


class OutcomeRecordTests(unittest.TestCase):
    def test_valid_pass_and_causal_terminal_failure_are_derived(self) -> None:
        passed = MODULE.validate_record(record("one", "one"))
        self.assertEqual(passed["attempt_outcome"], "PASS")
        self.assertIsNone(passed["terminal_failure"])
        blocked = MODULE.validate_record(record("two", "two", ("PASS", "BLOCK"), "missing-input"))
        self.assertEqual(blocked["attempt_outcome"], "BLOCK")
        self.assertEqual(
            blocked["terminal_failure"], {"stage": "evaluator", "code": "missing-input"}
        )

    def test_closed_schema_rejects_unknown_duplicate_and_caller_derived_fields(self) -> None:
        value = record("one", "one")
        value["attempt_outcome"] = "PASS"
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record(value)
        duplicate = '{"a":1,"a":2}'
        with self.assertRaises(MODULE.OutcomeAuditError) as context:
            MODULE.strict_json_loads(duplicate)
        self.assertEqual(context.exception.code, "DUPLICATE_JSON_KEY")
        malformed_refs = record("two", "two")
        malformed_refs["events"][0]["evidence_refs"] = [[]]
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record(malformed_refs)

    def test_order_terminal_continuation_and_missing_authority_block(self) -> None:
        reordered = record("one", "one")
        reordered["events"][1]["stage"] = "reviewer"
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record(reordered)
        continued = record("two", "two", ("PASS", "BLOCK"), "bad-output")
        continued["events"].append(event("reviewer", "PASS", 3))
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record(continued)
        incomplete = record("three", "three", ("PASS",))
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record(incomplete)
        duplicate_time = record("four", "four")
        duplicate_time["record_ref"] = "ref:record-four-b"
        duplicate_time["attempt_ref"] = "ref:attempt-four-b"
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record_set([record("four", "four-a"), duplicate_time])

    def test_work_item_and_scientific_status_are_separate_but_closed(self) -> None:
        value = record("one", "one", eligibility="INELIGIBLE", scientific_status="FAIL")
        value["work_item"]["disposition"] = "DEFERRED"
        result = MODULE.validate_record(value)
        self.assertEqual(result["work_item_disposition"], "DEFERRED")
        self.assertEqual(result["scientific_eligibility"], "INELIGIBLE")
        contradiction = record("two", "two", eligibility="INELIGIBLE", scientific_status="PASS")
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.validate_record(contradiction)

    def test_abstention_does_not_infer_history(self) -> None:
        abstention = MODULE.abstain_ambiguous_history()
        self.assertEqual(abstention["status"], "ABSTAIN")
        self.assertEqual(abstention["reason"], "AMBIGUOUS_HISTORY")
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.abstain_ambiguous_history("invented-success")


class OutcomeReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.records = MODULE.validate_record_set(
            [
                record("one", "one", ("PASS", "BLOCK"), "missing-input", eligibility="ELIGIBLE", scientific_status="FAIL"),
                record("one", "two", created="2026-08-22T01:00:00Z"),
                record("two", "three", ("PASS", "PASS", "BLOCK"), "review-gap", eligibility="ELIGIBLE", scientific_status="FAIL"),
                record("three", "four", eligibility="ELIGIBLE", scientific_status="PASS"),
            ]
        )

    def test_all_metrics_have_expected_denominators_and_failure_concentration(self) -> None:
        result = MODULE.report(self.records)
        self.assertEqual(result["metrics"]["first_pass_quality"]["numerator"], 1)
        self.assertEqual(result["metrics"]["first_pass_quality"]["denominator"], 3)
        self.assertEqual(result["metrics"]["eventual_reliability"]["numerator"], 2)
        self.assertEqual(result["metrics"]["eventual_reliability"]["denominator"], 3)
        self.assertEqual(result["metrics"]["reviewer_escape"]["numerator"], 1)
        self.assertEqual(result["metrics"]["reviewer_escape"]["denominator"], 3)
        self.assertEqual(result["metrics"]["eligible_scientific_success"]["numerator"], 2)
        self.assertEqual(result["metrics"]["eligible_scientific_success"]["denominator"], 4)
        self.assertEqual(result["failure_concentration"]["missing-input"]["denominator"], 2)
        self.assertEqual(result["attempts_per_work_item"]["mean"], 4 / 3)
        self.assertEqual(result["multi_attempt_frequency"]["numerator"], 1)
        self.assertEqual(result["multi_attempt_frequency"]["denominator"], 3)

    def test_measured_duration_ignores_unmeasured_attempts_and_wilson_is_known(self) -> None:
        result = MODULE.report(self.records)
        self.assertEqual(result["duration_seconds"]["measured_attempts"], 4)
        self.assertAlmostEqual(MODULE.wilson_interval(1, 2)["lower"], 0.0945286548, places=8)
        self.assertAlmostEqual(MODULE.wilson_interval(1, 2)["upper"], 0.9054713452, places=8)
        partial = MODULE.validate_record_set([record("one", "partial", durations=(None, 2.0, 3.0))])
        self.assertEqual(MODULE.report(partial)["duration_seconds"]["measured_attempts"], 0)

    def test_zero_denominator_and_grades_are_safe(self) -> None:
        result = MODULE.report([])
        for metric in result["metrics"].values():
            self.assertIsNone(metric["rate"])
            self.assertIsNone(metric["wilson_95"])
            self.assertEqual(metric["grade"], "UNRATED")
        bands = {
            "first_pass_quality": [{"minimum": 0.0, "maximum": 1.0, "grade": "OWNER"}]
        }
        graded = MODULE.report(self.records, bands)
        self.assertEqual(graded["metrics"]["first_pass_quality"]["grade"], "OWNER")
        self.assertEqual(graded["metrics"]["eventual_reliability"]["grade"], "UNRATED")
        with self.assertRaises(MODULE.OutcomeAuditError):
            MODULE.report([1])


class PrivateReceiptTests(unittest.TestCase):
    def make_project(self) -> tuple[Path, dict[str, bytes]]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        evidence_dir = root / MODULE.EVIDENCE_PREFIX
        evidence_dir.mkdir(parents=True)
        source_values = {
            "ref:source-a": {
                "schema_version": MODULE.EVIDENCE_SOURCE_SCHEMA,
                "source_ref": "ref:source-a",
                "items": [
                    {"item_ref": "ref:item-a", "item_digest": digest(b"item-a")},
                    {"item_ref": "ref:item-b", "item_digest": digest(b"item-b")},
                ],
            },
            "ref:source-b": {
                "schema_version": MODULE.EVIDENCE_SOURCE_SCHEMA,
                "source_ref": "ref:source-b",
                "items": [{"item_ref": "ref:item-c", "item_digest": digest(b"item-c")}],
            },
        }
        raw_sources: dict[str, bytes] = {}
        source_entries = []
        bindings = []
        for index, (source_ref, value) in enumerate(source_values.items(), start=1):
            raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
            relative = MODULE.EVIDENCE_PREFIX / f"source-{index}.json"
            (root / relative).write_bytes(raw)
            raw_sources[source_ref] = raw
            item_refs = [item["item_ref"] for item in value["items"]]
            item_digests = [item["item_digest"] for item in value["items"]]
            binding_digest = MODULE._binding_digest(source_ref, item_refs, item_digests)
            source_entries.append(
                {
                    "source_ref": source_ref,
                    "relative_path": str(relative),
                    "content_digest": digest(raw),
                    "item_count": len(item_refs),
                }
            )
            bindings.append(
                {
                    "source_ref": source_ref,
                    "item_refs": item_refs,
                    "item_digests": item_digests,
                    "item_count": len(item_refs),
                    "binding_digest": binding_digest,
                }
            )
        manifest = {
            "schema_version": MODULE.EVIDENCE_MANIFEST_SCHEMA,
            "contract_digest": digest(b"contract"),
            "population_digest": digest(b"population"),
            "source_count": len(source_entries),
            "sources": source_entries,
            "bindings": bindings,
        }
        manifest["source_set_digest"] = MODULE._source_set_digest(
            [
                {
                    **source,
                    "item_refs": [],
                    "item_digests": [],
                }
                for source in source_entries
            ]
        )
        manifest["binding_set_digest"] = MODULE._binding_set_digest(bindings)
        (root / MODULE.MANIFEST_RELATIVE).parent.mkdir(parents=True, exist_ok=True)
        (root / MODULE.MANIFEST_RELATIVE).write_text(
            MODULE.canonical_json(manifest) + "\n", encoding="utf-8"
        )
        return root, raw_sources

    @contextmanager
    def in_project(self, root: Path):
        previous = Path.cwd()
        os.chdir(root)
        try:
            yield
        finally:
            os.chdir(previous)

    def verify(self, root: Path) -> dict:
        with self.in_project(root):
            return MODULE.verify_private_evidence()

    def write(self, root: Path) -> dict:
        with self.in_project(root):
            return MODULE.write_fixed_receipt()

    def test_receipt_helpers_are_closed_and_reject_caller_root_and_payload(self) -> None:
        self.assertEqual(list(inspect.signature(MODULE.verify_private_evidence).parameters), [])
        self.assertEqual(list(inspect.signature(MODULE.write_fixed_receipt).parameters), [])
        root, _ = self.make_project()
        with self.assertRaises(TypeError):
            MODULE.verify_private_evidence(root)
        with self.assertRaises(TypeError):
            MODULE.write_fixed_receipt(root, {"status": "PASS"})

    def test_receipt_uses_only_current_working_directory(self) -> None:
        root, _ = self.make_project()
        with tempfile.TemporaryDirectory() as other_name:
            other = Path(other_name)
            with self.in_project(root):
                self.assertEqual(MODULE.verify_private_evidence()["status"], "PASS")
            with self.in_project(other):
                self.assertEqual(MODULE.verify_private_evidence()["status"], "BLOCK")
                receipt = MODULE.write_fixed_receipt()
                self.assertEqual(receipt["status"], "BLOCK")
            self.assertTrue((other / MODULE.RECEIPT_RELATIVE).is_file())
            self.assertFalse((root / MODULE.RECEIPT_RELATIVE).is_file())

    def test_receipt_validates_exact_set_bindings_and_hides_private_fields(self) -> None:
        root, _ = self.make_project()
        receipt = self.verify(root)
        self.assertEqual(receipt["status"], "PASS")
        rendered = MODULE.canonical_json(receipt)
        for private in ("source-a", "source-b", "item-a", "item-b", "item-c", "source-1.json"):
            self.assertNotIn(private, rendered)
        self.assertEqual(self.write(root), receipt)
        first = (root / MODULE.RECEIPT_RELATIVE).read_bytes()
        replay = self.verify(root)
        self.assertEqual(self.write(root), replay)
        self.assertEqual(first, (root / MODULE.RECEIPT_RELATIVE).read_bytes())

    def test_omission_substitution_tamper_and_wrong_counts_block(self) -> None:
        root, _ = self.make_project()
        manifest_path = root / MODULE.MANIFEST_RELATIVE
        manifest = json.loads(manifest_path.read_text())
        manifest["source_count"] = 1
        manifest_path.write_text(MODULE.canonical_json(manifest))
        self.assertEqual(self.verify(root)["status"], "BLOCK")
        root, _ = self.make_project()
        source_path = root / MODULE.EVIDENCE_PREFIX / "source-1.json"
        source_path.write_bytes(source_path.read_bytes() + b"tamper")
        self.assertEqual(self.verify(root)["status"], "BLOCK")
        root, _ = self.make_project()
        manifest = json.loads((root / MODULE.MANIFEST_RELATIVE).read_text())
        manifest["sources"][0]["item_count"] = 99
        (root / MODULE.MANIFEST_RELATIVE).write_text(MODULE.canonical_json(manifest))
        self.assertEqual(self.verify(root)["status"], "BLOCK")

    def test_exact_evidence_population_rejects_unlisted_missing_duplicate_and_non_json(self) -> None:
        root, _ = self.make_project()
        evidence_dir = root / MODULE.EVIDENCE_PREFIX
        self.assertEqual(self.verify(root)["status"], "PASS")
        (evidence_dir / "unlisted.json").write_text("{}")
        extra = self.verify(root)
        self.assertEqual(extra["status"], "BLOCK")
        self.assertEqual(extra["error_code"], "EXTRA_SOURCE")

        root, _ = self.make_project()
        (root / MODULE.EVIDENCE_PREFIX / "source-1.json").unlink()
        missing = self.verify(root)
        self.assertEqual(missing["status"], "BLOCK")
        self.assertEqual(missing["error_code"], "MISSING_SOURCE")

        root, _ = self.make_project()
        manifest_path = root / MODULE.MANIFEST_RELATIVE
        manifest = json.loads(manifest_path.read_text())
        manifest["sources"][1]["relative_path"] = manifest["sources"][0]["relative_path"]
        manifest_path.write_text(MODULE.canonical_json(manifest))
        duplicate = self.verify(root)
        self.assertEqual(duplicate["status"], "BLOCK")
        self.assertEqual(duplicate["error_code"], "DUPLICATE_SOURCE_PATH")

        root, _ = self.make_project()
        (root / MODULE.EVIDENCE_PREFIX / "unlisted.txt").write_text("{}")
        non_json = self.verify(root)
        self.assertEqual(non_json["status"], "BLOCK")
        self.assertEqual(non_json["error_code"], "NON_JSON_ENTRY")

    def test_exact_evidence_population_rejects_directory_fifo_socket_and_device(self) -> None:
        def assert_block_with_entry(create_entry) -> None:
            root, _ = self.make_project()
            create_entry(root / MODULE.EVIDENCE_PREFIX / "unlisted.json")
            result = self.verify(root)
            self.assertEqual(result["status"], "BLOCK")
            self.assertEqual(result["error_code"], "NONREGULAR")

        assert_block_with_entry(lambda path: path.mkdir())
        assert_block_with_entry(lambda path: os.mkfifo(path))

        def create_socket(path: Path) -> None:
            server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            short_path = Path("/tmp") / f"outcome-audit-{os.getpid()}-{id(path)}"
            try:
                server.bind(str(short_path))
                os.replace(short_path, path)
            finally:
                server.close()
                if short_path.exists():
                    short_path.unlink()

        assert_block_with_entry(create_socket)

        root, _ = self.make_project()
        class FakeDeviceEntry:
            name = "unlisted.json"

            def is_symlink(self) -> bool:
                return False

            def stat(self, *, follow_symlinks: bool) -> os.stat_result:
                if follow_symlinks:
                    raise AssertionError("device attack must not follow symlinks")
                values = [0] * 10
                values[0] = stat.S_IFCHR | 0o600
                return os.stat_result(values)

        with patch.object(MODULE.os, "scandir", return_value=iter([FakeDeviceEntry()])):
            result = self.verify(root)
        self.assertEqual(result["status"], "BLOCK")
        self.assertEqual(result["error_code"], "NONREGULAR")

    def test_traversal_symlink_duplicate_and_unstructured_inputs_block(self) -> None:
        root, _ = self.make_project()
        manifest_path = root / MODULE.MANIFEST_RELATIVE
        manifest = json.loads(manifest_path.read_text())
        manifest["sources"][0]["relative_path"] = str(MODULE.EVIDENCE_PREFIX / "../outside.json")
        manifest_path.write_text(MODULE.canonical_json(manifest))
        self.assertEqual(self.verify(root)["status"], "BLOCK")
        root, _ = self.make_project()
        source = root / MODULE.EVIDENCE_PREFIX / "source-1.json"
        target = root / MODULE.EVIDENCE_PREFIX / "real-source.json"
        source.unlink()
        target.write_text("{}")
        source.symlink_to(target)
        self.assertEqual(self.verify(root)["status"], "BLOCK")
        root, _ = self.make_project()
        manifest = json.loads((root / MODULE.MANIFEST_RELATIVE).read_text())
        manifest["bindings"].append(manifest["bindings"][0])
        manifest["source_count"] = 3
        manifest_path = root / MODULE.MANIFEST_RELATIVE
        manifest_path.write_text(MODULE.canonical_json(manifest))
        self.assertEqual(self.verify(root)["status"], "BLOCK")
        root, _ = self.make_project()
        source = root / MODULE.EVIDENCE_PREFIX / "source-1.json"
        source.write_text("[1, 2, 3]")
        self.assertEqual(self.verify(root)["status"], "BLOCK")

    def test_duplicate_json_and_missing_manifest_block_without_fallback(self) -> None:
        root, _ = self.make_project()
        (root / MODULE.MANIFEST_RELATIVE).write_text('{"schema_version":"x","schema_version":"y"}')
        receipt = self.verify(root)
        self.assertEqual(receipt, {"schema_version": MODULE.RECEIPT_SCHEMA, "status": "BLOCK", "error_code": "DUPLICATE_JSON_KEY"})
        root, _ = self.make_project()
        (root / MODULE.MANIFEST_RELATIVE).unlink()
        receipt = self.verify(root)
        self.assertEqual(receipt["status"], "BLOCK")


class DiscoveryAndCoverageTests(unittest.TestCase):
    def test_cli_validation_report_abstention_and_receipt_have_bounded_interfaces(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            records_path = root / "records.json"
            records_path.write_text(
                MODULE.canonical_json([record("one", "one")]) + "\n", encoding="utf-8"
            )
            command = ["python3", str(MODULE_PATH)]
            validated = subprocess.run(
                [*command, "validate", str(records_path)], capture_output=True, text=True, check=False
            )
            self.assertEqual(validated.returncode, 0, validated.stderr)
            reported = subprocess.run(
                [*command, "report", str(records_path)], capture_output=True, text=True, check=False
            )
            self.assertEqual(reported.returncode, 0, reported.stderr)
            abstained = subprocess.run(
                [*command, "abstain", "--reason", "AMBIGUOUS_HISTORY"], capture_output=True, text=True, check=False
            )
            self.assertEqual(abstained.returncode, 0, abstained.stderr)
            receipt = subprocess.run(
                [*command, "receipt", "arbitrary-private-path"],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(receipt.returncode, 0)
            self.assertIn("usage:", receipt.stderr)
            for option in ("--root", "--output", "--evidence", "--include", "--exclude"):
                rejected = subprocess.run(
                    [*command, "receipt", option, str(root)],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    check=False,
                )
                self.assertNotEqual(rejected.returncode, 0)
                self.assertIn("usage:", rejected.stderr)
            missing_receipt = subprocess.run(
                [*command, "receipt"], cwd=root, capture_output=True, text=True, check=False
            )
            self.assertNotEqual(missing_receipt.returncode, 0)
            self.assertEqual(json.loads(missing_receipt.stdout)["status"], "BLOCK")
            self.assertTrue((root / MODULE.RECEIPT_RELATIVE).is_file())

    def test_router_docs_validator_and_registered_matrix_are_present(self) -> None:
        router = (ROOT / "skills/agent-plus/SKILL.md").read_text()
        docs = (ROOT / "docs/bootstrap-a-baseball-project.md").read_text()
        validator = (ROOT / "scripts/validate-public-package.sh").read_text()
        skill = (ROOT / "skills/outcome-audit/SKILL.md").read_text()
        for text in (router, docs, validator):
            self.assertIn("outcome-audit", text)
        for phrase in (
            "closed prospective",
            "Wilson",
            "ABSTAIN",
            "fixed project-local",
            "source_set_digest",
            "binding",
            "symlink",
            "UNRATED",
        ):
            self.assertIn(phrase, skill)
        packet = json.loads((ROOT / ".agent-plus/agent-plus-outcome-audit-task-001.json").read_text())
        self.assertEqual(
            set(packet["attack_matrix"]["items"]),
            {
                "exact-schema-rejection", "ordered-terminal-authority", "attempt-disposition-separation",
                "scientific-status-separation", "first-pass-denominator", "eventual-success-grouping",
                "reviewer-escape-denominator", "wilson-small-sample", "zero-denominator-null",
                "duration-measured-only", "retry-efficiency", "abstention-no-inference", "fixed-receipt-interface",
                "evidence-omission-substitution", "traversal-symlink-tamper", "strict-json-duplicate",
                "receipt-privacy", "deterministic-replay", "router-doc-discovery", "public-validator",
            },
        )
        self.assertEqual(len(packet["named_coverage"]["items"]), 12)


if __name__ == "__main__":
    unittest.main()
