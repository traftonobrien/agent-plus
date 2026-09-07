from __future__ import annotations

import importlib.util
import tempfile
import json
import hashlib
import unittest
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/interface_consumer_guard.py"
SPEC = importlib.util.spec_from_file_location("interface_consumer_guard", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def _write_fixture(root: Path) -> dict[str, Any]:
    (root / "src").mkdir()
    (root / "tests").mkdir()
    (root / "src/interface.py").write_text("def changed_shape():\n    return 1\n")
    (root / "src/runtime.py").write_text("from interface import changed_shape\n")
    (root / "tests/test_shape.py").write_text("# changed_shape real-shape smoke\n")
    packet = {
        "schema_version": guard.INTERFACE_CONSUMER_SCHEMA_VERSION,
        "interfaces": [
            {
                "interface_id": "changed-shape",
                "definition_path": "src/interface.py",
                "search_roots": ["src", "tests"],
                "search_tokens": ["changed_shape"],
                "consumers": [
                    {
                        "path": "src/runtime.py",
                        "kind": "runtime_wrapper",
                        "disposition": "updated",
                        "acceptance_checks": ["pytest tests/test_shape.py"],
                    },
                    {
                        "path": "tests/test_shape.py",
                        "kind": "test",
                        "disposition": "updated",
                        "acceptance_checks": ["pytest tests/test_shape.py"],
                    },
                ],
            }
        ],
        "real_shape_smoke": {
            "required": True,
            "status": "PASS",
            "command": "pytest tests/test_shape.py",
            "evidence": guard.SMOKE_PATH,
        },
    }

    (root / ".agent-plus").mkdir()
    (root / guard.SMOKE_LOG).write_bytes(b"synthetic output")
    (root / guard.SMOKE_PATH).write_text(json.dumps({
        "schema_version": "agent-plus-interface-smoke/v1", "command": packet["real_shape_smoke"]["command"],
        "exit_code": 0, "inputs": guard._snapshot_inputs(packet, root),
        "output_sha256": hashlib.sha256(b"synthetic output").hexdigest()}))
    return packet


class InterfaceConsumerGuardTests(unittest.TestCase):
    def test_public_example_closes_every_discovered_consumer(self) -> None:
        raw = guard.load_receipt(ROOT / ".agent-plus/interface-consumer-closure-example.json")
        guard.validate_receipt(raw, root=ROOT)

    def test_valid_synthetic_receipt_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            guard.validate_receipt(_write_fixture(root), root=root)

    def test_undeclared_runtime_wrapper_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = _write_fixture(root)
            raw["interfaces"][0]["consumers"] = raw["interfaces"][0]["consumers"][1:]
            with self.assertRaisesRegex(
                guard.InterfaceConsumerGuardBlocked, "undeclared=.*src/runtime.py"
            ):
                guard.validate_receipt(raw, root=root)

    def test_declared_but_unobserved_consumer_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = _write_fixture(root)
            raw["interfaces"][0]["consumers"].append(
                {
                    "path": "tests/unused.py",
                    "kind": "test",
                    "disposition": "tested_unchanged",
                    "acceptance_checks": ["pytest tests/unused.py"],
                }
            )
            (root / "tests/unused.py").write_text("# unrelated\n")
            raw["interfaces"][0]["consumers"] = sorted(
                raw["interfaces"][0]["consumers"], key=lambda item: item["path"]
            )
            with self.assertRaisesRegex(guard.InterfaceConsumerGuardBlocked, "missing=.*unused.py"):
                guard.validate_receipt(raw, root=root)

    def test_required_smoke_must_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = _write_fixture(root)
            raw["real_shape_smoke"]["status"] = "NOT_REQUIRED"
            raw["real_shape_smoke"]["command"] = "not-required"
            raw["real_shape_smoke"]["evidence"] = "not-required"
            with self.assertRaisesRegex(guard.InterfaceConsumerGuardBlocked, "did not PASS"):
                guard.validate_receipt(raw, root=root)

    def test_unknown_fields_and_duplicate_json_keys_block(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = _write_fixture(root)
            raw["extra"] = True
            with self.assertRaisesRegex(guard.InterfaceConsumerGuardBlocked, "fields differ"):
                guard.validate_receipt(raw, root=root)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            path.write_text('{"schema_version":"x","schema_version":"y"}')
            with self.assertRaisesRegex(guard.InterfaceConsumerGuardBlocked, "duplicate JSON key"):
                guard.load_receipt(path)

    def test_paths_and_canonical_order_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = _write_fixture(root)
            raw["interfaces"][0]["definition_path"] = "../escape.py"
            with self.assertRaisesRegex(guard.InterfaceConsumerGuardBlocked, "safe repository"):
                guard.validate_receipt(raw, root=root)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = _write_fixture(root)
            raw["interfaces"][0]["search_roots"] = ["tests", "src"]
            with self.assertRaisesRegex(guard.InterfaceConsumerGuardBlocked, "canonical sorted"):
                guard.validate_receipt(raw, root=root)


if __name__ == "__main__":
    unittest.main()
