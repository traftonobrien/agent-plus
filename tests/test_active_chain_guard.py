from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "active_chain_guard", ROOT / "scripts" / "active_chain_guard.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ActiveChainGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "policy.md").write_text("policy\n", encoding="utf-8")
        (self.root / "receipt.md").write_text("receipt\n", encoding="utf-8")
        (self.root / ".agent-plus").mkdir()
        self.capsule = self.root / ".agent-plus" / "active-chain.json"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def value(self) -> dict[str, object]:
        return {
            "schema_version": "agent-plus-active-chain/v1",
            "chain_id": "example-chain",
            "objective": "Close one bounded public example.",
            "status": "active",
            "current_stage": "make",
            "terminal_condition": "pass_null_or_block",
            "change_kind": "local_repair",
            "stages": [
                {"id": "plan", "role": "controller", "status": "pass", "evidence": "receipt.md"},
                {"id": "make", "role": "maker", "status": "pending", "evidence": ""},
                {"id": "evaluate", "role": "evaluator", "status": "pending", "evidence": ""},
                {"id": "review", "role": "verifier", "status": "pending", "evidence": ""},
            ],
            "same_interface_failure_limit": 2,
            "same_interface_failures": 0,
            "authority_refs": ["policy.md"],
            "hard_boundaries": ["no_data_access", "no_release"],
        }

    def write(self, value: dict[str, object]) -> None:
        self.capsule.write_text(json.dumps(value), encoding="utf-8")

    def test_active_chain_routes_to_first_pending_stage(self) -> None:
        self.write(self.value())
        self.assertEqual(
            MODULE.validate(self.capsule, self.root, "continue"),
            "ACTIVE_CHAIN_CONTINUE chain=example-chain stage=make",
        )

    def test_active_chain_rejects_early_closeout(self) -> None:
        self.write(self.value())
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_EARLY_CLOSEOUT"):
            MODULE.validate(self.capsule, self.root, "closeout")

    def test_pass_closeout_requires_every_stage(self) -> None:
        value = self.value()
        value["status"] = "pass"
        value["current_stage"] = None
        for stage in value["stages"]:  # type: ignore[index,union-attr]
            stage["status"] = "pass"
            stage["evidence"] = "receipt.md"
        self.write(value)
        self.assertEqual(
            MODULE.validate(self.capsule, self.root, "closeout"),
            "ACTIVE_CHAIN_CLOSEOUT_PASS chain=example-chain",
        )

    def test_block_and_null_are_honest_terminal_outcomes(self) -> None:
        for terminal in ("block", "null"):
            value = self.value()
            value["status"] = terminal
            value["current_stage"] = None
            stages = value["stages"]  # type: ignore[assignment]
            stages[1]["status"] = terminal  # type: ignore[index]
            stages[1]["evidence"] = "receipt.md"  # type: ignore[index]
            self.write(value)
            expected = f"ACTIVE_CHAIN_CLOSEOUT_{terminal.upper()} chain=example-chain"
            self.assertEqual(MODULE.validate(self.capsule, self.root, "closeout"), expected)

    def test_two_failures_require_architecture_reset(self) -> None:
        value = self.value()
        value["same_interface_failures"] = 2
        self.write(value)
        with self.assertRaisesRegex(
            MODULE.ChainError, "BLOCK_CHAIN_ARCHITECTURE_RESET_REQUIRED"
        ):
            MODULE.validate(self.capsule, self.root, "continue")
        value["change_kind"] = "architecture_reset"
        self.write(value)
        self.assertIn("ACTIVE_CHAIN_CONTINUE", MODULE.validate(self.capsule, self.root, "continue"))

    def test_authority_reference_must_be_live_safe_file(self) -> None:
        value = self.value()
        value["authority_refs"] = ["../outside.md"]
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_PATH"):
            MODULE.validate(self.capsule, self.root, "continue")

    def test_capsule_must_use_one_project_local_location(self) -> None:
        value = self.value()
        outside = Path(self.temporary.name).parent / "outside-active-chain.json"
        outside.write_text(json.dumps(value), encoding="utf-8")
        try:
            with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_CAPSULE_PATH"):
                MODULE.validate(outside, self.root, "continue")

            alternate = self.root / "alternate-active-chain.json"
            alternate.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_CAPSULE_PATH"):
                MODULE.validate(alternate, self.root, "continue")

            link = self.root / ".agent-plus" / "active-chain-example.json"
            link.symlink_to(self.capsule)
            self.write(value)
            with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_CAPSULE_FILE"):
                MODULE.validate(link, self.root, "continue")
        finally:
            outside.unlink(missing_ok=True)

    def test_authority_reference_supports_long_repository_path(self) -> None:
        directory = self.root / ("a" * 40) / ("b" * 40)
        directory.mkdir(parents=True)
        authority = directory / "authority-contract.md"
        authority.write_text("authority\n", encoding="utf-8")
        value = self.value()
        value["authority_refs"] = [authority.relative_to(self.root).as_posix()]
        self.write(value)
        self.assertIn("ACTIVE_CHAIN_CONTINUE", MODULE.validate(self.capsule, self.root, "continue"))

    def test_authority_symlink_and_parent_escape_fail_closed(self) -> None:
        outside = Path(self.temporary.name).parent / "outside-active-chain-authority.md"
        outside.write_text("outside\n", encoding="utf-8")
        try:
            direct = self.root / "authority-link.md"
            direct.symlink_to(self.root / "policy.md")
            value = self.value()
            value["authority_refs"] = ["authority-link.md"]
            self.write(value)
            with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_PATH"):
                MODULE.validate(self.capsule, self.root, "continue")

            parent = self.root / "escaped"
            parent.symlink_to(outside.parent, target_is_directory=True)
            value["authority_refs"] = [f"escaped/{outside.name}"]
            self.write(value)
            with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_PATH"):
                MODULE.validate(self.capsule, self.root, "continue")
        finally:
            outside.unlink(missing_ok=True)

    def test_stage_order_and_current_stage_must_agree(self) -> None:
        value = self.value()
        value["stages"][2]["status"] = "pass"  # type: ignore[index]
        value["stages"][2]["evidence"] = "receipt.md"  # type: ignore[index]
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_STAGE_ORDER"):
            MODULE.validate(self.capsule, self.root, "continue")

        value = self.value()
        value["current_stage"] = "review"
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_ROUTING"):
            MODULE.validate(self.capsule, self.root, "continue")

    def test_terminal_capsule_cannot_continue(self) -> None:
        value = self.value()
        value["status"] = "block"
        value["current_stage"] = None
        value["stages"][1]["status"] = "block"  # type: ignore[index]
        value["stages"][1]["evidence"] = "receipt.md"  # type: ignore[index]
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_NOT_ACTIVE"):
            MODULE.validate(self.capsule, self.root, "continue")

    def test_boolean_and_nonfinite_failure_counts_fail_closed(self) -> None:
        value = self.value()
        value["same_interface_failures"] = True
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_FAILURE_COUNT"):
            MODULE.validate(self.capsule, self.root, "continue")

        raw = json.dumps(self.value()).replace(
            '"same_interface_failures": 0', '"same_interface_failures": NaN'
        )
        self.capsule.write_text(raw, encoding="utf-8")
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_NONFINITE_NUMBER"):
            MODULE.validate(self.capsule, self.root, "continue")

    def test_enum_fields_reject_arrays_and_objects_with_typed_errors(self) -> None:
        cases = (
            ("chain-status", "BLOCK_CHAIN_STATUS"),
            ("change-kind", "BLOCK_CHAIN_CHANGE_KIND"),
            ("stage-role", "BLOCK_CHAIN_STAGE_ROLE"),
            ("stage-status", "BLOCK_CHAIN_STAGE_STATUS"),
        )
        for case, error_code in cases:
            for malformed in ([], {}):
                with self.subTest(case=case, malformed=type(malformed).__name__):
                    value = self.value()
                    if case == "chain-status":
                        value["status"] = malformed
                    elif case == "change-kind":
                        value["change_kind"] = malformed
                    elif case == "stage-role":
                        value["stages"][1]["role"] = malformed  # type: ignore[index]
                    else:
                        value["stages"][1]["status"] = malformed  # type: ignore[index]
                    self.write(value)
                    with self.assertRaisesRegex(MODULE.ChainError, error_code):
                        MODULE.validate(self.capsule, self.root, "continue")

    def test_cli_reports_malformed_enum_without_traceback(self) -> None:
        value = self.value()
        value["status"] = []
        self.write(value)
        result = subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "active_chain_guard.py"),
                "--root",
                str(self.root),
                "--capsule",
                str(self.capsule),
                "--mode",
                "continue",
            ],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("BLOCK_CHAIN_STATUS", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_unknown_fields_and_duplicate_keys_fail_closed(self) -> None:
        value = self.value()
        value["note"] = "not allowed"
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_SCHEMA"):
            MODULE.validate(self.capsule, self.root, "continue")

    def test_oversized_capsule_fails_before_json_validation(self) -> None:
        self.capsule.write_text("{" + (" " * MODULE.MAX_CAPSULE_BYTES) + "}", encoding="utf-8")
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_CAPSULE_SIZE"):
            MODULE.validate(self.capsule, self.root, "continue")
        text = json.dumps(self.value())
        self.capsule.write_text(text[:-1] + ',"chain_id":"duplicate"}', encoding="utf-8")
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_DUPLICATE_KEY"):
            MODULE.validate(self.capsule, self.root, "continue")

    def test_completed_stage_requires_existing_evidence(self) -> None:
        value = self.value()
        value["stages"][0]["evidence"] = "missing.md"  # type: ignore[index]
        self.write(value)
        with self.assertRaisesRegex(MODULE.ChainError, "BLOCK_CHAIN_PATH"):
            MODULE.validate(self.capsule, self.root, "continue")


if __name__ == "__main__":
    unittest.main()
