from __future__ import annotations

import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.anti_loop_guard import (
    OUTCOME_CATALOG,
    OUTCOME_KINDS,
    GuardError,
    load_ledger,
    record_block,
    validate_ledger,
    validate_packet,
)

ROOT = Path(__file__).resolve().parents[1]
GUARD = ROOT / "scripts" / "anti_loop_guard.py"
LEDGER_PATH = ROOT / ".agent-plus" / "engineering-boundaries.json"
EXAMPLE_PACKET_PATH = ROOT / ".agent-plus" / "engineering-closure-example.json"

SCHEMA = "anti-loop-guard/v2"


def ledger_state(**changes: object) -> dict[str, object]:
    state: dict[str, object] = {
        "block_count": 0,
        "architecture_reset_required": False,
        "reset_namespace": "rehearsals/wave-b-f16-read-only",
        "authorized_attempt_id": "attempt-03",
        "permitted_removed_choices": ["arbitrary-root", "arbitrary-diagnostic-root"],
        "permitted_outcomes": {"example-readiness-decision": "scientific_readiness_decision"},
        "required_attack_matrix": ["missing-root", "alias-and-nesting"],
        "required_named_coverage": ["root-binding", "adjacent-invariants"],
    }
    state.update(changes)
    return state


def ledger(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": SCHEMA,
        "boundaries": {
            "TEST_INTERFACE": {
                "failure_classes": {
                    "root-binding": ledger_state(),
                    "alias-and-nesting": ledger_state(
                        required_attack_matrix=["alias-and-nesting"],
                        required_named_coverage=["adjacent-invariants"],
                    ),
                }
            }
        },
    }
    value.update(changes)
    return value


def packet(**changes: object) -> dict[str, object]:
    value: dict[str, object] = {
        "schema_version": SCHEMA,
        "packet_id": "TEST-PACKET-001",
        "packet_type": "review",
        "boundary_id": "TEST_INTERFACE",
        "failure_class": "root-binding",
        "ledger_ref": "TEST_INTERFACE/root-binding",
        "review_mode": "engineering_sweep",
        "change_kind": "local_repair",
        "outcome_kind": "scientific_readiness_decision",
        "outcome_id": "example-readiness-decision",
        "failure_class_coverage": ["root-binding", "alias-and-nesting"],
        "stop_policy": "collect_named_matrix",
        "review_status": "complete",
        "attack_matrix": {"status": "complete", "items": ["missing-root", "alias-and-nesting"]},
        "named_coverage": {"status": "complete", "items": ["root-binding", "adjacent-invariants"]},
    }
    value.update(changes)
    return value


def scientific_packet(**changes: object) -> dict[str, object]:
    value = packet(
        packet_id="TEST-SCIENTIFIC-001",
        packet_type="task",
        review_mode="scientific_first_error_gate",
        change_kind="execution",
        stop_policy="stop_first_error",
        review_status="planned",
        attack_matrix={"status": "not_applicable", "items": []},
        named_coverage={"status": "pending", "items": ["root-binding"]},
    )
    value.update(changes)
    return value


def reset_packet(**changes: object) -> dict[str, object]:
    value = packet(
        packet_id="TEST-ARCHITECTURE-RESET-001",
        packet_type="task",
        change_kind="architecture_reset",
        review_status="planned",
        attack_matrix={"status": "pending", "items": []},
        named_coverage={"status": "pending", "items": ["root-binding"]},
        reset_namespace="rehearsals/wave-b-f16-read-only",
        attempt_id="attempt-03",
        removed_caller_choices=["arbitrary-root"],
    )
    value.update(changes)
    return value


def blocked_ledger() -> dict[str, object]:
    return record_block(
        record_block(ledger(), "TEST_INTERFACE", "root-binding"), "TEST_INTERFACE", "root-binding"
    )


class GuardTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = ledger()

    def assert_code(self, code: str, call: object) -> None:
        with self.assertRaises(GuardError) as context:
            call()  # type: ignore[operator]
        self.assertEqual(context.exception.code, code)


class ValidPathTests(GuardTestCase):
    def test_valid_engineering_closure(self) -> None:
        receipt = validate_packet(packet(), self.ledger)
        self.assertEqual(receipt["status"], "PASS")
        self.assertTrue(str(receipt["receipt_id"]).startswith("sha256:"))

    def test_complete_engineering_review_is_valid_closeout(self) -> None:
        receipt = validate_packet(
            packet(), self.ledger, require_complete_engineering_review=True
        )
        self.assertEqual(receipt["review_status"], "complete")
        self.assertEqual(receipt["validation_mode"], "engineering_review_closeout")
        self.assertTrue(receipt["closeout_mode"])

    def test_standard_and_closeout_receipts_are_not_identical(self) -> None:
        standard = validate_packet(packet(), self.ledger)
        closeout = validate_packet(
            packet(), self.ledger, require_complete_engineering_review=True
        )
        self.assertNotEqual(standard["receipt_id"], closeout["receipt_id"])
        self.assertEqual(standard["validation_mode"], "standard")
        self.assertFalse(standard["closeout_mode"])

    def test_planned_engineering_review_cannot_close(self) -> None:
        self.assert_code(
            "E_INCOMPLETE_COVERAGE",
            lambda: validate_packet(
                packet(
                    review_status="planned",
                    attack_matrix={"status": "pending", "items": []},
                    named_coverage={"status": "pending", "items": []},
                ),
                self.ledger,
                require_complete_engineering_review=True,
            ),
        )

    def test_task_or_scientific_packet_cannot_close_engineering_review(self) -> None:
        for value in (
            packet(packet_type="task"),
            scientific_packet(),
        ):
            self.assert_code(
                "E_INVALID_REVIEW_CLOSEOUT",
                lambda value=value: validate_packet(
                    value, self.ledger, require_complete_engineering_review=True
                ),
            )

    def test_valid_scientific_and_live_first_error_gates(self) -> None:
        for mode in ("scientific_first_error_gate", "live_first_error_gate"):
            receipt = validate_packet(scientific_packet(review_mode=mode), self.ledger)
            self.assertEqual(receipt["review_mode"], mode)
            self.assertEqual(receipt["change_kind"], "execution")

    def test_architecture_reset_is_accepted_after_trigger(self) -> None:
        receipt = validate_packet(reset_packet(), blocked_ledger())
        self.assertEqual(receipt["status"], "PASS")
        self.assertTrue(receipt["architecture_reset_required"])

    def test_first_and_second_block_tracking(self) -> None:
        first = record_block(self.ledger, "TEST_INTERFACE", "root-binding")
        state = first["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"]  # type: ignore[index]
        self.assertEqual(state["block_count"], 1)
        self.assertFalse(state["architecture_reset_required"])
        second = record_block(first, "TEST_INTERFACE", "root-binding")
        state = second["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"]  # type: ignore[index]
        self.assertEqual(state["block_count"], 2)
        self.assertTrue(state["architecture_reset_required"])
        # record_block never mutates its input ledger.
        self.assertEqual(
            self.ledger["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
                "block_count"
            ],
            0,
        )  # type: ignore[index]


class LedgerBoundDecisionTests(GuardTestCase):
    def test_third_local_repair_is_rejected(self) -> None:
        self.assert_code(
            "E_THIRD_LOCAL_REPAIR", lambda: validate_packet(packet(), blocked_ledger())
        )

    def test_execution_at_a_reset_boundary_is_rejected(self) -> None:
        self.assert_code(
            "E_ARCHITECTURE_RESET_REQUIRED",
            lambda: validate_packet(scientific_packet(), blocked_ledger()),
        )

    def test_reset_without_ledger_authorization_is_rejected(self) -> None:
        self.assert_code(
            "E_RESET_NOT_TRIGGERED", lambda: validate_packet(reset_packet(), self.ledger)
        )

    def test_unknown_boundary_and_failure_class(self) -> None:
        self.assert_code(
            "E_UNKNOWN_BOUNDARY",
            lambda: validate_packet(
                packet(
                    boundary_id="UNKNOWN_INTERFACE", ledger_ref="UNKNOWN_INTERFACE/root-binding"
                ),
                self.ledger,
            ),
        )
        self.assert_code(
            "E_UNKNOWN_FAILURE_CLASS",
            lambda: validate_packet(
                packet(failure_class="other-class", ledger_ref="TEST_INTERFACE/other-class"),
                self.ledger,
            ),
        )

    def test_packet_ledger_mismatch_is_rejected(self) -> None:
        self.assert_code(
            "E_PACKET_LEDGER_MISMATCH",
            lambda: validate_packet(packet(ledger_ref="TEST_INTERFACE/other"), self.ledger),
        )

    def test_coverage_must_be_ledger_declared_and_include_the_failure_class(self) -> None:
        self.assert_code(
            "E_INCOMPLETE_COVERAGE",
            lambda: validate_packet(
                packet(failure_class_coverage=["alias-and-nesting"]), self.ledger
            ),
        )
        self.assert_code(
            "E_UNKNOWN_FAILURE_CLASS",
            lambda: validate_packet(
                packet(failure_class_coverage=["root-binding", "invented-class"]), self.ledger
            ),
        )

    def test_completed_matrices_are_bound_to_the_ledger(self) -> None:
        self.assert_code(
            "E_INCOMPLETE_COVERAGE",
            lambda: validate_packet(
                packet(attack_matrix={"status": "complete", "items": ["missing-root"]}), self.ledger
            ),
        )
        self.assert_code(
            "E_INCOMPLETE_COVERAGE",
            lambda: validate_packet(
                packet(named_coverage={"status": "complete", "items": ["invented-item"]}),
                self.ledger,
            ),
        )
        self.assert_code(
            "E_INCOMPLETE_COVERAGE",
            lambda: validate_packet(
                packet(attack_matrix={"status": "pending", "items": []}), self.ledger
            ),
        )

    def test_pending_matrix_cannot_invent_items(self) -> None:
        self.assert_code(
            "E_INCOMPLETE_COVERAGE",
            lambda: validate_packet(
                scientific_packet(named_coverage={"status": "pending", "items": ["invented-item"]}),
                self.ledger,
            ),
        )

    def test_stop_policy_and_change_kind_are_bound_to_review_mode(self) -> None:
        self.assert_code(
            "E_INVALID_STOP_POLICY",
            lambda: validate_packet(
                scientific_packet(stop_policy="collect_named_matrix"), self.ledger
            ),
        )
        self.assert_code(
            "E_INVALID_STOP_POLICY",
            lambda: validate_packet(packet(stop_policy="stop_first_error"), self.ledger),
        )
        self.assert_code(
            "E_INVALID_CHANGE_KIND",
            lambda: validate_packet(packet(change_kind="execution"), self.ledger),
        )
        self.assert_code(
            "E_INVALID_CHANGE_KIND",
            lambda: validate_packet(scientific_packet(change_kind="local_repair"), self.ledger),
        )


class OutcomeTests(GuardTestCase):
    def test_disguised_process_only_outcomes_are_rejected(self) -> None:
        for outcome_id in (
            "tests pass; data",
            "review complete; result",
            "files changed; model",
            "receipts and results",
            "validation passed; readiness",
        ):
            self.assert_code(
                "E_UNAUTHORIZED_OUTCOME",
                lambda outcome_id=outcome_id: validate_packet(
                    packet(outcome_id=outcome_id), self.ledger
                ),
            )

    def test_well_formed_but_unauthorized_outcome_id_is_rejected(self) -> None:
        for outcome_id in ("tests-pass-data", "docs-updated", "lint-passed", "files-written"):
            self.assert_code(
                "E_UNAUTHORIZED_OUTCOME",
                lambda outcome_id=outcome_id: validate_packet(
                    packet(outcome_id=outcome_id), self.ledger
                ),
            )

    def test_process_outcome_kinds_are_outside_the_closed_enum(self) -> None:
        for outcome_kind in (
            "tests_passed",
            "lint_passed",
            "files_written",
            "docs_updated",
            "review_complete",
        ):
            self.assert_code(
                "E_INVALID_FIELD",
                lambda outcome_kind=outcome_kind: validate_packet(
                    packet(outcome_kind=outcome_kind), self.ledger
                ),
            )

    def test_outcome_kind_must_match_the_ledger_entry(self) -> None:
        self.assert_code(
            "E_UNAUTHORIZED_OUTCOME",
            lambda: validate_packet(packet(outcome_kind="model_evaluation_result"), self.ledger),
        )

    def test_ledger_cannot_declare_a_process_outcome_kind(self) -> None:
        malformed = ledger()
        malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
            "permitted_outcomes"
        ] = {  # type: ignore[index]
            "tests-pass": "tests_passed"
        }
        self.assert_code("E_MALFORMED_LEDGER", lambda: validate_packet(packet(), malformed))

    def test_guard_owned_catalog_rejects_process_ids_for_every_outcome_kind(self) -> None:
        for outcome_id in (
            "tests-passed",
            "files-written",
            "lint-passed",
            "docs-updated",
            "review-complete",
        ):
            for outcome_kind in OUTCOME_KINDS:
                malformed = ledger()
                malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
                    "permitted_outcomes"
                ] = {outcome_id: outcome_kind}  # type: ignore[index]
                self.assert_code(
                    "E_MALFORMED_LEDGER", lambda malformed=malformed: validate_ledger(malformed)
                )

    def test_guard_owned_catalog_rejects_forged_ids_and_recategorization(self) -> None:
        for outcome_id in (
            "example-readiness-decision-renamed",
            "Example-readiness-decision",
            "../example-readiness-decision",
            "example-readiness-decision/child",
        ):
            malformed = ledger()
            malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
                "permitted_outcomes"
            ] = {outcome_id: "scientific_readiness_decision"}  # type: ignore[index]
            self.assert_code(
                "E_MALFORMED_LEDGER", lambda malformed=malformed: validate_ledger(malformed)
            )

        for outcome_id, outcome_kind in OUTCOME_CATALOG.items():
            wrong_kind = next(kind for kind in OUTCOME_KINDS if kind != outcome_kind)
            malformed = ledger()
            malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
                "permitted_outcomes"
            ] = {outcome_id: wrong_kind}  # type: ignore[index]
            self.assert_code(
                "E_MALFORMED_LEDGER", lambda malformed=malformed: validate_ledger(malformed)
            )

    def test_catalog_authorized_user_scientific_and_execution_outcomes_pass(self) -> None:
        all_outcomes = dict(OUTCOME_CATALOG)
        current = ledger()
        current["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
            "permitted_outcomes"
        ] = all_outcomes  # type: ignore[index]

        user_visible = validate_packet(
            packet(
                outcome_kind="user_visible_capability",
                outcome_id="agent-plus-control-plane-capability",
            ),
            current,
        )
        self.assertEqual(user_visible["outcome_id"], "agent-plus-control-plane-capability")

        scientific = validate_packet(
            packet(
                outcome_kind="scientific_result",
                outcome_id="validated-scientific-result",
            ),
            current,
        )
        self.assertEqual(scientific["outcome_id"], "validated-scientific-result")

        execution = validate_packet(
            scientific_packet(
                outcome_kind="data_access_decision",
                outcome_id="certified-data-access-decision",
            ),
            current,
        )
        self.assertEqual(execution["change_kind"], "execution")

    def test_packet_cannot_use_catalog_id_outside_ledger_subset(self) -> None:
        self.assert_code(
            "E_UNAUTHORIZED_OUTCOME",
            lambda: validate_packet(
                packet(
                    outcome_kind="user_visible_capability",
                    outcome_id="agent-plus-control-plane-capability",
                ),
                self.ledger,
            ),
        )


class ArchitectureResetTests(GuardTestCase):
    def test_agent_plus_release_reset_namespace_is_approved(self) -> None:
        current = ledger()
        current["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][  # type: ignore[index]
            "reset_namespace"
        ] = "agent-plus/0.2.0-release"
        validated = validate_ledger(current)
        state = validated["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"]
        self.assertEqual(state["reset_namespace"], "agent-plus/0.2.0-release")

    def test_active_chain_reset_namespace_is_approved(self) -> None:
        current = ledger()
        current["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][  # type: ignore[index]
            "reset_namespace"
        ] = "agent-plus/active-chain-routing"
        validated = validate_ledger(current)
        state = validated["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"]
        self.assertEqual(state["reset_namespace"], "agent-plus/active-chain-routing")

    def test_unauthorized_reset_namespace_is_rejected(self) -> None:
        self.assert_code(
            "E_UNAUTHORIZED_NAMESPACE",
            lambda: validate_packet(
                reset_packet(reset_namespace="arbitrary/rehearsal/root"), blocked_ledger()
            ),
        )

    def test_ledger_reset_namespace_cannot_be_arbitrary(self) -> None:
        malformed = ledger()
        malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
            "reset_namespace"
        ] = "any/root"  # type: ignore[index]
        self.assert_code("E_UNAUTHORIZED_NAMESPACE", lambda: validate_ledger(malformed))

    def test_mismatched_attempt_id_is_rejected(self) -> None:
        for attempt_id in ("attempt-04", "attempt-3", "attempt-003", "ATTEMPT-03", "../attempt-03"):
            self.assert_code(
                "E_UNAUTHORIZED_ATTEMPT_ID",
                lambda attempt_id=attempt_id: validate_packet(
                    reset_packet(attempt_id=attempt_id), blocked_ledger()
                ),
            )

    def test_reset_relabeling_through_nested_caller_values_is_rejected(self) -> None:
        for choices in (
            ["Relabel a local patch"],
            ["local patching"],
            ["local_patch"],
            ["arbitrary-root", "narrow-patch"],
        ):
            self.assert_code(
                "E_UNAUTHORIZED_CALLER_CHOICE",
                lambda choices=choices: validate_packet(
                    reset_packet(removed_caller_choices=choices), blocked_ledger()
                ),
            )

    def test_reset_only_fields_are_absent_from_a_non_reset_packet(self) -> None:
        self.assert_code(
            "E_UNKNOWN_FIELD", lambda: validate_packet(packet(attempt_id="attempt-03"), self.ledger)
        )
        value = reset_packet()
        del value["attempt_id"]
        self.assert_code("E_MISSING_FIELD", lambda: validate_packet(value, blocked_ledger()))


class ClosedInputBoundaryTests(GuardTestCase):
    def test_unsupported_schema_versions_are_typed(self) -> None:
        self.assert_code(
            "E_UNKNOWN_PACKET_STATE",
            lambda: validate_packet(packet(schema_version="anti-loop-guard/v1"), self.ledger),
        )
        self.assert_code(
            "E_UNKNOWN_LEDGER_STATE",
            lambda: validate_packet(packet(), ledger(schema_version="anti-loop-guard/v1")),
        )

    def test_unknown_fields_are_rejected_at_every_depth(self) -> None:
        self.assert_code(
            "E_UNKNOWN_FIELD", lambda: validate_packet(packet(notes="local patching"), self.ledger)
        )
        self.assert_code(
            "E_UNKNOWN_FIELD",
            lambda: validate_packet(
                packet(
                    attack_matrix={
                        "status": "complete",
                        "items": ["missing-root", "alias-and-nesting"],
                        "description": "This is a local patching path",
                    }
                ),
                self.ledger,
            ),
        )
        malformed = ledger()
        malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"]["note"] = (
            "extra"  # type: ignore[index]
        )
        self.assert_code("E_UNKNOWN_FIELD", lambda: validate_packet(packet(), malformed))

    def test_non_string_mapping_keys_are_typed_at_every_depth(self) -> None:
        for key in (1, None, True, 2.5):
            self.assert_code(
                "E_INVALID_KEY_TYPE",
                lambda key=key: validate_packet({**packet(), key: "x"}, self.ledger),  # type: ignore[dict-item]
            )
        self.assert_code(
            "E_INVALID_KEY_TYPE",
            lambda: validate_packet(
                packet(attack_matrix={"status": "complete", "items": [], None: "x"}), self.ledger
            ),
        )
        self.assert_code("E_INVALID_KEY_TYPE", lambda: validate_ledger({**ledger(), 1: "x"}))  # type: ignore[dict-item]
        nested = ledger()
        nested["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
            "permitted_outcomes"
        ] = {1: "x"}  # type: ignore[index]
        self.assert_code("E_INVALID_KEY_TYPE", lambda: validate_ledger(nested))

    def test_non_mapping_roots_are_typed(self) -> None:
        for value in ([], "packet", 3, None):
            self.assert_code(
                "E_MALFORMED_PACKET", lambda value=value: validate_packet(value, self.ledger)
            )  # type: ignore[arg-type]
            self.assert_code("E_MALFORMED_LEDGER", lambda value=value: validate_ledger(value))  # type: ignore[arg-type]

    def test_unhashable_and_wrong_type_enum_values_are_typed(self) -> None:
        for field, value in (
            ("packet_type", []),
            ("review_mode", {}),
            ("review_status", ["complete"]),
            ("change_kind", {}),
            ("stop_policy", 3),
            ("outcome_kind", []),
        ):
            self.assert_code(
                "E_INVALID_FIELD",
                lambda field=field, value=value: validate_packet(
                    packet(**{field: value}), self.ledger
                ),
            )

    def test_ledger_counters_reject_bools_floats_strings_and_negatives(self) -> None:
        for value in (2.0, True, False, "2", -1, 10**100):
            malformed = ledger()
            malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
                "block_count"
            ] = value  # type: ignore[index]
            self.assert_code(
                "E_MALFORMED_LEDGER", lambda malformed=malformed: validate_ledger(malformed)
            )

    def test_ledger_reset_flag_must_agree_with_the_block_count(self) -> None:
        malformed = ledger()
        malformed["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
            "architecture_reset_required"
        ] = True  # type: ignore[index]
        self.assert_code("E_MALFORMED_LEDGER", lambda: validate_ledger(malformed))

    def test_deeply_nested_input_is_typed(self) -> None:
        deep: object = "leaf"
        for _ in range(40):
            deep = {"next": deep}
        self.assert_code(
            "E_INVALID_STRUCTURE", lambda: validate_packet(packet(named_coverage=deep), self.ledger)
        )

    def test_missing_required_field_is_typed(self) -> None:
        value = packet()
        del value["named_coverage"]
        self.assert_code("E_MISSING_FIELD", lambda: validate_packet(value, self.ledger))
        value = packet()
        del value["change_kind"]
        self.assert_code("E_MISSING_FIELD", lambda: validate_packet(value, self.ledger))


class ReceiptTests(GuardTestCase):
    def test_receipt_is_deterministic_across_independent_constructions(self) -> None:
        first = validate_packet(packet(), ledger())
        second = validate_packet(dict(reversed(list(packet().items()))), ledger())
        self.assertEqual(first, second)

    def test_receipt_binds_packet_and_full_ledger_state(self) -> None:
        first = validate_packet(packet(), self.ledger)
        second = validate_packet(packet(packet_id="TEST-PACKET-002"), self.ledger)
        third = validate_packet(
            packet(), record_block(self.ledger, "TEST_INTERFACE", "root-binding")
        )
        self.assertNotEqual(first["receipt_id"], second["receipt_id"])
        self.assertNotEqual(first["receipt_id"], third["receipt_id"])
        self.assertNotEqual(first["ledger_sha256"], third["ledger_sha256"])
        self.assertEqual(len(str(first["packet_sha256"])), 64)
        self.assertEqual(len(str(first["ledger_sha256"])), 64)

    def test_inputs_are_not_mutated_and_later_mutation_cannot_change_a_receipt(self) -> None:
        value = packet()
        current = ledger()
        packet_before = copy.deepcopy(value)
        ledger_before = copy.deepcopy(current)
        receipt = validate_packet(value, current)
        snapshot = copy.deepcopy(receipt)
        self.assertEqual(value, packet_before)
        self.assertEqual(current, ledger_before)
        value["packet_id"] = "TEST-PACKET-MUTATED"
        value["failure_class_coverage"].append("alias-and-nesting")  # type: ignore[attr-defined]
        current["boundaries"]["TEST_INTERFACE"]["failure_classes"]["root-binding"][
            "block_count"
        ] = 9  # type: ignore[index]
        self.assertEqual(receipt, snapshot)
        self.assertEqual(receipt, validate_packet(packet(), ledger()))


class CommandLineTests(GuardTestCase):
    def run_guard(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(GUARD), *arguments], check=False, capture_output=True, text=True
        )

    def test_example_packet_passes_through_the_cli(self) -> None:
        result = self.run_guard("--ledger", str(LEDGER_PATH), "--packet", str(EXAMPLE_PACKET_PATH))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")

    def test_cli_requires_complete_engineering_review_at_closeout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger_path = root / "ledger.json"
            ledger_path.write_text(json.dumps(ledger()), encoding="utf-8")
            packet_path = root / "packet.json"
            planned = packet(
                review_status="planned",
                attack_matrix={"status": "pending", "items": []},
                named_coverage={"status": "pending", "items": []},
            )
            packet_path.write_text(json.dumps(planned), encoding="utf-8")
            result = self.run_guard(
                "--ledger",
                str(ledger_path),
                "--packet",
                str(packet_path),
                "--require-complete-engineering-review",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("E_INCOMPLETE_COVERAGE", result.stdout)

            packet_path.write_text(json.dumps(packet()), encoding="utf-8")
            result = self.run_guard(
                "--ledger",
                str(ledger_path),
                "--packet",
                str(packet_path),
                "--require-complete-engineering-review",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_duplicate_keys_are_rejected_at_top_and_nested_levels(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger_path = root / "ledger.json"
            ledger_path.write_text(json.dumps(ledger()), encoding="utf-8")
            packet_path = root / "packet.json"
            packet_path.write_text('{"packet_id":"A","packet_id":"B"}', encoding="utf-8")
            result = self.run_guard("--ledger", str(ledger_path), "--packet", str(packet_path))
            self.assertIn("ANTI_LOOP_GUARD_ERROR E_DUPLICATE_KEY", result.stdout)

            compact = json.dumps(ledger(), separators=(",", ":"))
            ledger_path.write_text(
                compact.replace('"block_count":0', '"block_count":0,"block_count":0', 1),
                encoding="utf-8",
            )
            result = self.run_guard(
                "--ledger", str(ledger_path), "--packet", str(EXAMPLE_PACKET_PATH)
            )
            self.assertIn("ANTI_LOOP_GUARD_ERROR E_DUPLICATE_KEY", result.stdout)

    def test_malformed_json_and_missing_files_are_typed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger_path = root / "ledger.json"
            ledger_path.write_text("{not json", encoding="utf-8")
            result = self.run_guard(
                "--ledger", str(ledger_path), "--packet", str(EXAMPLE_PACKET_PATH)
            )
            self.assertIn("ANTI_LOOP_GUARD_ERROR E_MALFORMED_LEDGER", result.stdout)

            ledger_path.write_text(
                json.dumps(ledger(), separators=(",", ":")).replace(
                    '"block_count":0', '"block_count":NaN', 1
                ),
                encoding="utf-8",
            )
            result = self.run_guard(
                "--ledger", str(ledger_path), "--packet", str(EXAMPLE_PACKET_PATH)
            )
            self.assertIn("ANTI_LOOP_GUARD_ERROR E_MALFORMED_LEDGER", result.stdout)

            result = self.run_guard(
                "--ledger", str(root / "absent.json"), "--packet", str(EXAMPLE_PACKET_PATH)
            )
            self.assertIn("ANTI_LOOP_GUARD_ERROR E_MISSING_LEDGER", result.stdout)

    def test_missing_ledger_file_is_typed_in_process(self) -> None:
        self.assert_code(
            "E_MISSING_LEDGER", lambda: load_ledger(ROOT / ".agent-plus" / "does-not-exist.json")
        )

    def test_concurrent_block_records_do_not_lose_updates(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger_path = root / "ledger.json"
            ledger_path.write_text(json.dumps(ledger()), encoding="utf-8")
            packet_path = root / "packet.json"
            packet_path.write_text(json.dumps(packet()), encoding="utf-8")
            (root / ".ledger.json.interrupted-write").write_text("not valid json", encoding="utf-8")
            processes = [
                subprocess.Popen(
                    [
                        sys.executable,
                        str(GUARD),
                        "--ledger",
                        str(ledger_path),
                        "--packet",
                        str(packet_path),
                        "--record-block",
                        "--require-complete-engineering-review",
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                for _ in range(2)
            ]
            results = [process.communicate(timeout=30) for process in processes]
            self.assertTrue(all(process.returncode == 0 for process in processes), results)
            state = load_ledger(ledger_path)["boundaries"]["TEST_INTERFACE"]["failure_classes"][
                "root-binding"
            ]
            self.assertEqual(state["block_count"], 2)
            self.assertTrue(state["architecture_reset_required"])

    def test_direct_record_block_without_closeout_packet_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger_path = root / "ledger.json"
            ledger_path.write_text(json.dumps(ledger()), encoding="utf-8")
            result = self.run_guard(
                "--ledger",
                str(ledger_path),
                "--record-block",
                "--boundary-id",
                "TEST_INTERFACE",
                "--failure-class",
                "root-binding",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("E_INVALID_COMMAND", result.stdout)
            self.assertEqual(load_ledger(ledger_path), ledger())

    def test_record_block_returns_closeout_receipt_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger_path = root / "ledger.json"
            packet_path = root / "packet.json"
            ledger_path.write_text(json.dumps(ledger()), encoding="utf-8")
            packet_path.write_text(json.dumps(packet()), encoding="utf-8")
            result = self.run_guard(
                "--ledger",
                str(ledger_path),
                "--packet",
                str(packet_path),
                "--record-block",
                "--require-complete-engineering-review",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            output = json.loads(result.stdout)
            self.assertEqual(output["status"], "BLOCK_RECORDED")
            self.assertEqual(output["closeout_receipt_id"], output["closeout_receipt"]["receipt_id"])
            self.assertTrue(output["closeout_receipt"]["closeout_mode"])
            self.assertEqual(output["block_count"], 1)


class BootstrapTests(GuardTestCase):
    def test_bootstrap_copies_guard_controls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "synthetic-project"
            target.mkdir()
            result = subprocess.run(
                [
                    str(ROOT / "scripts" / "agent-plus-init.sh"),
                    "--target",
                    str(target),
                    "--profile",
                    "research",
                    "--brain-note",
                    "Synthetic",
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "scripts" / "anti_loop_guard.py").is_file())
            self.assertTrue((target / ".agent-plus" / "engineering-boundaries.json").is_file())
            doctor = subprocess.run(
                [str(ROOT / "scripts" / "agent-plus-doctor.sh"), "--target", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(doctor.returncode, 0, doctor.stderr)


if __name__ == "__main__":
    unittest.main()
