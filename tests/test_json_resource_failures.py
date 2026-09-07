from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def module(relative: str):
    spec = importlib.util.spec_from_file_location(Path(relative).stem, ROOT / relative)
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


interface = module("scripts/interface_consumer_guard.py")
chain = module("scripts/active_chain_guard.py")
manager = module("scripts/agent_plus_manager.py")
release = module("scripts/verify_release_candidate.py")
outcome = module("skills/outcome-audit/outcome_audit.py")


def payloads():
    yield "[" * 10000 + "0" + "]" * 10000
    yield '{"x":' * 10000 + "0" + "}" * 10000
    if hasattr(sys, "get_int_max_str_digits") and sys.get_int_max_str_digits():
        yield "9" * 10000


class JsonResourceTests(unittest.TestCase):
    def assert_block(self, command, root, fragment, env=None):
        # The lifecycle command retains its kernel-lease file by design.
        # Control and artifact bytes must remain unchanged.
        before = {
            str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file() and p.name != "upgrade.lock"
        }
        result = subprocess.run(
            command,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            env=env,
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(fragment, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        after = {
            str(p.relative_to(root)): p.read_bytes()
            for p in root.rglob("*")
            if p.is_file() and p.name != "upgrade.lock"
        }
        self.assertEqual(before, after)

    def test_imported_loaders_reject_exhaustion_with_existing_error_types(self):
        for payload in payloads():
            with (
                self.subTest(size=len(payload)),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                (root / ".agent-plus").mkdir()
                receipt = root / ".agent-plus/active-chain.json"
                receipt.write_text(payload)
                with self.assertRaises(interface.InterfaceConsumerGuardBlocked):
                    interface.load_receipt(receipt)
                with self.assertRaises(chain.ChainError):
                    chain._load_capsule(receipt, root)
                with self.assertRaises(manager.ManagerError):
                    manager._read_json(payload.encode(), "manifest")
                with self.assertRaises(outcome.OutcomeAuditError):
                    outcome.strict_json_loads(payload)
                (root / ".agent-plus/release-candidate.json").write_text(payload)
                with self.assertRaises(release.CandidateError):
                    release.load_config(root)
                (root / ".agent-plus/local-projects.json").write_text(payload)
                original = manager._source_root
                try:
                    manager._source_root = lambda root=root: root
                    with self.assertRaises(manager.ManagerError):
                        manager._registry()
                finally:
                    manager._source_root = original

    def test_valid_below_limit_json_is_not_rejected_by_parser(self):
        payload = '{"x":' * 20 + "0" + "}" * 20
        expected = json.loads(payload)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agent-plus").mkdir()
            path = root / ".agent-plus/active-chain.json"
            path.write_text(payload)
            self.assertEqual(interface.load_receipt(path), expected)
            self.assertEqual(chain._load_capsule(path, root), expected)
            self.assertEqual(
                manager._read_json(payload.encode(), "synthetic"), expected
            )
            self.assertEqual(outcome.strict_json_loads(payload), expected)

    def test_cli_and_bootstrap_guards_return_typed_block_without_mutation(self):
        for payload in payloads():
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / ".agent-plus").mkdir()
                path = root / ".agent-plus/active-chain.json"
                path.write_text(payload)
                for prefix in ("scripts", "bootstrap/base/scripts"):
                    self.assert_block(
                        [
                            sys.executable,
                            str(ROOT / prefix / "interface_consumer_guard.py"),
                            "--root",
                            str(root),
                            "--receipt",
                            str(path),
                        ],
                        root,
                        "INTERFACE_CONSUMER_CLOSURE_BLOCKED",
                    )
                    self.assert_block(
                        [
                            sys.executable,
                            str(ROOT / prefix / "active_chain_guard.py"),
                            "--root",
                            str(root),
                            "--capsule",
                            str(path),
                            "--mode",
                            "closeout",
                        ],
                        root,
                        "BLOCK_CHAIN_JSON",
                    )
                (root / ".agent-plus/install-manifest.json").write_text(payload)
                self.assert_block(
                    [
                        sys.executable,
                        str(ROOT / "scripts/agent_plus_manager.py"),
                        "status",
                        "--target",
                        str(root),
                    ],
                    root,
                    "Invalid install manifest",
                )
                self.assert_block(
                    [
                        sys.executable,
                        str(ROOT / "skills/outcome-audit/outcome_audit.py"),
                        "validate",
                        str(path),
                    ],
                    root,
                    "MALFORMED_JSON",
                )

    def test_standalone_normal_and_legacy_doctor_loaders(self):
        declaration = {
            "schema_version": "agent-plus-legacy-adoption/v1",
            "mode": "legacy-adopted",
            "profile": "research",
            "startup_check_path": ".agent-plus/project-startup-check.sh",
        }
        for payload in payloads():
            for mode in ("normal-manifest", "legacy-declaration", "legacy-manifest"):
                with (
                    self.subTest(mode=mode),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = Path(directory)
                    (root / ".agent-plus").mkdir()
                    (root / "scripts").mkdir()
                    doctor = root / "scripts/agent-plus-doctor.sh"
                    shutil.copy2(ROOT / "scripts/agent-plus-doctor.sh", doctor)
                    (root / ".agent-plus/install-manifest.json").write_text(payload)
                    if mode == "legacy-declaration":
                        (root / ".agent-plus/legacy-adoption.json").write_text(payload)
                    elif mode == "legacy-manifest":
                        (root / ".agent-plus/legacy-adoption.json").write_text(
                            json.dumps(declaration)
                        )
                    self.assert_block(
                        ["sh", str(doctor), "--target", str(root)], root, "Invalid"
                    )


if __name__ == "__main__":
    unittest.main()
