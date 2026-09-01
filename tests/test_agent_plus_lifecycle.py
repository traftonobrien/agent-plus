from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
COMMAND = ROOT / "scripts" / "agent-plus"


class AgentPlusLifecycleTests(unittest.TestCase):
    def run_command(self, *arguments: str, expected: int = 0) -> Any:
        result = subprocess.run(
            [str(COMMAND), *arguments],
            cwd=ROOT,
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def initialize(self, target: Path) -> None:
        self.run_command(
            "init",
            "--target",
            str(target),
            "--profile",
            "research",
            "--brain-note",
            "Example Project",
        )

    def downgrade_to_v1(self, target: Path, version: str = "0.3.0") -> None:
        manifest_path = target / ".agent-plus/install-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for relative in (
            ".agent-plus/active-chain-example.json",
            "scripts/active_chain_guard.py",
        ):
            (target / relative).unlink()
            manifest["managed_files"].pop(relative)
        manifest["schema_version"] = "agent-plus-install/v1"
        manifest["agent_plus_version"] = version
        manifest.pop("managed_set_id")
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )

    def load_manager(self) -> Any:
        spec = importlib.util.spec_from_file_location(
            "agent_plus_manager_test", ROOT / "scripts" / "agent_plus_manager.py"
        )
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def installation_snapshot(self, target: Path) -> dict[str, bytes]:
        manifest_path = target / ".agent-plus" / "install-manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        relatives = sorted(manifest["managed_files"])
        relatives.append(".agent-plus/install-manifest.json")
        return {relative: (target / relative).read_bytes() for relative in relatives}

    def assert_installation_snapshot(self, target: Path, snapshot: dict[str, bytes]) -> None:
        for relative, expected in snapshot.items():
            self.assertEqual((target / relative).read_bytes(), expected, relative)

    def journal(self, target: Path) -> dict[str, Any]:
        return json.loads(
            (target / ".agent-plus/upgrade-transaction.json").read_text(encoding="utf-8")
        )

    def induce_commit_failure(self, manager: Any, target: Path, fail_at: int) -> None:
        calls = 0
        real_replace = manager._replace_for_upgrade

        def fail_replace(
            source_fd: int,
            destination_parent_fd: int,
            destination_name: str,
            phase: str,
            expected: str | None = None,
        ) -> str:
            nonlocal calls
            calls += 1
            if calls == fail_at:
                raise manager.ManagerError("injected commit failure")
            return real_replace(source_fd, destination_parent_fd, destination_name, phase, expected)

        with (
            mock.patch.object(manager, "_replace_for_upgrade", side_effect=fail_replace),
            self.assertRaises(manager.ManagerError) as raised,
        ):
            manager.upgrade(target)
        self.assertIn("recover --target", str(raised.exception))

    def test_init_doctor_status_and_safe_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'project "quoted" with spaces'
            target.mkdir()
            self.run_command(
                "init",
                "--target",
                str(target),
                "--profile",
                "research",
                "--brain-note",
                'Brain: "private"\\nnext',
            )
            self.run_command("doctor", "--target", str(target))
            result = self.run_command("status", "--target", str(target))
            self.assertIn("AGENT_PLUS_CURRENT", result.stdout)
            yaml_text = (target / ".agent-plus/project.yaml").read_text(encoding="utf-8")
            self.assertIn('project_name: "project \\\"quoted\\\" with spaces"', yaml_text)
            self.assertIn('brain_note: "Brain: \\\"private\\\"\\\\nnext"', yaml_text)

    def test_init_delivers_and_manages_active_chain_controls(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            manifest = json.loads(
                (target / ".agent-plus/install-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["schema_version"], "agent-plus-install/v2")
            self.assertEqual(manifest["managed_set_id"], "agent-plus-active-chain-v1")
            for relative in (
                ".agent-plus/active-chain-example.json",
                "scripts/active_chain_guard.py",
            ):
                self.assertIn(relative, manifest["managed_files"])
                self.assertTrue((target / relative).is_file(), relative)
            for relative in (
                "scripts/ai-context.sh",
                "scripts/agent-plus-doctor.sh",
                "scripts/active_chain_guard.py",
            ):
                self.assertTrue((target / relative).stat().st_mode & 0o111, relative)
            copied_doctor = subprocess.run(
                [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                cwd=target,
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(copied_doctor.returncode, 0, copied_doctor.stderr)

    def test_historical_v1_manifests_are_exact_and_report_generation_update(self) -> None:
        for version in ("0.2.0", "0.3.0"):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "project"
                target.mkdir()
                self.initialize(target)
                self.downgrade_to_v1(target, version)
                status = self.run_command("status", "--target", str(target), expected=3)
                self.assertIn("UPDATE_AVAILABLE", status.stdout)
                self.assertIn("managed_set=agent-plus-active-chain-v1", status.stdout)
                self.run_command("doctor", "--target", str(target))
                copied_doctor = subprocess.run(
                    [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                    cwd=target,
                    check=False,
                    text=True,
                    capture_output=True,
                )
                self.assertEqual(copied_doctor.returncode, 0, copied_doctor.stderr)

    def test_historical_v1_subset_manifests_fail_across_consumers(self) -> None:
        for position in ("first", "middle", "last"):
            with self.subTest(position=position), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "project"
                target.mkdir()
                self.initialize(target)
                self.downgrade_to_v1(target)
                manifest_path = target / ".agent-plus/install-manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                relatives = list(manifest["managed_files"])
                index = {"first": 0, "middle": len(relatives) // 2, "last": -1}[position]
                manifest["managed_files"].pop(relatives[index])
                manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                self.run_command("status", "--target", str(target), expected=1)
                self.run_command("doctor", "--target", str(target), expected=1)
                copied = subprocess.run(
                    [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                    cwd=target,
                    check=False,
                    text=True,
                    capture_output=True,
                )
                self.assertNotEqual(copied.returncode, 0, position)

    def test_unknown_manifest_generation_and_nonexact_sets_fail_closed(self) -> None:
        for case in ("legacy-version", "set-id", "subset", "superset"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "project"
                target.mkdir()
                self.initialize(target)
                manifest_path = target / ".agent-plus/install-manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                if case == "legacy-version":
                    self.downgrade_to_v1(target, "9.9.9")
                elif case == "set-id":
                    manifest["managed_set_id"] = "unknown-managed-set"
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                elif case == "subset":
                    manifest["managed_files"].pop("scripts/active_chain_guard.py")
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                else:
                    manifest["managed_files"]["unmanaged.txt"] = "0" * 64
                    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
                self.run_command("status", "--target", str(target), expected=1)
                self.run_command("doctor", "--target", str(target), expected=1)

    def test_manifest_set_id_helper_rejects_non_string_identity(self) -> None:
        manager = self.load_manager()
        with self.assertRaisesRegex(manager.ManagerError, r"Invalid Agent\+ managed-set identity"):
            manager._manifest_set_id(
                {"schema_version": manager.SCHEMA, "managed_set_id": []}
            )

    def test_doctor_rejects_missing_or_drifted_active_chain_controls(self) -> None:
        attacks = (
            ("missing-guard", "scripts/active_chain_guard.py", "unlink"),
            ("missing-example", ".agent-plus/active-chain-example.json", "unlink"),
            ("drift-guard", "scripts/active_chain_guard.py", "write"),
            ("drift-example", ".agent-plus/active-chain-example.json", "write"),
        )
        for label, relative, action in attacks:
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "project"
                target.mkdir()
                self.initialize(target)
                path = target / relative
                if action == "unlink":
                    path.unlink()
                else:
                    path.write_text("drift\n", encoding="utf-8")
                self.run_command("doctor", "--target", str(target), expected=1)
                copied = subprocess.run(
                    [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                    cwd=target,
                    check=False,
                    text=True,
                    capture_output=True,
                )
                self.assertNotEqual(copied.returncode, 0, label)

    def test_status_and_doctor_reject_managed_command_mode_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            guard = target / "scripts/active_chain_guard.py"
            guard.chmod(0o644)
            status = self.run_command("status", "--target", str(target), expected=1)
            self.assertIn("LOCAL_DRIFT mode:scripts/active_chain_guard.py", status.stdout)
            self.run_command("doctor", "--target", str(target), expected=1)

    def test_additive_upgrade_from_v1_preserves_owned_state(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.downgrade_to_v1(target)
            owned = target / ".planning/STATE.md"
            owned.write_text("project-owned-state\n", encoding="utf-8")
            self.run_command("upgrade", "--target", str(target))
            manifest = json.loads(
                (target / ".agent-plus/install-manifest.json").read_text(encoding="utf-8")
            )
            self.assertEqual(manifest["schema_version"], "agent-plus-install/v2")
            self.assertEqual(manifest["managed_set_id"], "agent-plus-active-chain-v1")
            self.assertEqual(owned.read_text(encoding="utf-8"), "project-owned-state\n")
            self.assertTrue((target / "scripts/active_chain_guard.py").is_file())
            self.assertTrue((target / ".agent-plus/active-chain-example.json").is_file())
            for relative in (
                "scripts/ai-context.sh",
                "scripts/agent-plus-doctor.sh",
                "scripts/active_chain_guard.py",
            ):
                self.assertTrue((target / relative).stat().st_mode & 0o111, relative)
            copied_doctor = subprocess.run(
                [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                cwd=target,
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(copied_doctor.returncode, 0, copied_doctor.stderr)
            self.run_command("doctor", "--target", str(target))

    def test_additive_upgrade_rejects_candidate_only_collision_before_journal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.downgrade_to_v1(target)
            collision = target / "scripts/active_chain_guard.py"
            collision.write_text("project-owned\n", encoding="utf-8")
            result = self.run_command("upgrade", "--target", str(target), expected=1)
            self.assertIn("Refusing to overwrite unmanaged destination", result.stderr)
            self.assertEqual(collision.read_text(encoding="utf-8"), "project-owned\n")
            self.assertFalse((target / ".agent-plus/upgrade-transaction.json").exists())

    def test_candidate_only_race_is_preserved_during_recovery(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.downgrade_to_v1(target)
            collision = target / ".agent-plus/active-chain-example.json"
            real_preflight = manager._preflight_candidate_only_destinations

            def create_after_preflight(filesystem: Any, relatives: list[str]) -> None:
                real_preflight(filesystem, relatives)
                collision.write_text("concurrent-project-file\n", encoding="utf-8")

            with (
                mock.patch.object(
                    manager,
                    "_preflight_candidate_only_destinations",
                    side_effect=create_after_preflight,
                ),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)
            journal = self.journal(target)
            self.assertNotIn(str(collision.relative_to(target)), journal["committed_files"])
            manager.recover(target)
            self.assertEqual(collision.read_text(encoding="utf-8"), "concurrent-project-file\n")
            self.assertFalse((target / ".agent-plus/upgrade-transaction.json").exists())

    def test_recovery_blocks_if_a_committed_candidate_only_file_changed(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.downgrade_to_v1(target)
            calls = 0
            real_create = manager._create_for_upgrade

            def fail_second_create(*args: Any, **kwargs: Any) -> str:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise manager.ManagerError("injected candidate-only commit failure")
                return real_create(*args, **kwargs)

            with (
                mock.patch.object(manager, "_create_for_upgrade", side_effect=fail_second_create),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)
            committed_addition = target / ".agent-plus/active-chain-example.json"
            committed_addition.write_text("external-replacement\n", encoding="utf-8")
            with self.assertRaisesRegex(
                manager.ManagerError, "Candidate-only recovery file changed"
            ):
                manager.recover(target)
            self.assertEqual(
                committed_addition.read_text(encoding="utf-8"), "external-replacement\n"
            )
            self.assertTrue((target / ".agent-plus/upgrade-transaction.json").is_file())

    def test_additive_journal_set_identity_forgery_is_rejected(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.downgrade_to_v1(target)
            with manager.TransactionFilesystem(target) as filesystem:
                manifest = manager._manifest(filesystem)
                candidate = manager._manifest_data(filesystem, "research")
            baseline = manager._journal_base("synthetic", "research", manifest, candidate)
            attacks = {
                "candidate-only-subset": lambda value: value.__setitem__(
                    "candidate_only_files", value["candidate_only_files"][:-1]
                ),
                "unknown-prior-set": lambda value: value.__setitem__(
                    "prior_managed_set_id", "unknown-managed-set"
                ),
                "unknown-candidate-set": lambda value: value.__setitem__(
                    "candidate_managed_set_id", "unknown-managed-set"
                ),
            }
            for label, mutate in attacks.items():
                with self.subTest(label=label):
                    forged = json.loads(json.dumps(baseline))
                    mutate(forged)
                    with self.assertRaises(manager.ManagerError):
                        manager._validate_journal(forged)

    def test_additive_upgrade_recovery_removes_candidate_only_files(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.downgrade_to_v1(target)
            before = self.installation_snapshot(target)
            calls = 0
            real_create = manager._create_for_upgrade

            def fail_second_create(*args: Any, **kwargs: Any) -> str:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise manager.ManagerError("injected candidate-only commit failure")
                return real_create(*args, **kwargs)

            with (
                mock.patch.object(manager, "_create_for_upgrade", side_effect=fail_second_create),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)
            journal = self.journal(target)
            self.assertEqual(journal["schema_version"], "agent-plus-upgrade-transaction/v3")
            self.assertEqual(
                journal["candidate_only_files"],
                [".agent-plus/active-chain-example.json", "scripts/active_chain_guard.py"],
            )
            self.assertTrue((target / ".agent-plus/active-chain-example.json").is_file())
            manager.recover(target)
            self.assert_installation_snapshot(target, before)
            self.assertFalse((target / ".agent-plus/active-chain-example.json").exists())
            self.assertFalse((target / "scripts/active_chain_guard.py").exists())
            for relative in ("scripts/ai-context.sh", "scripts/agent-plus-doctor.sh"):
                self.assertTrue((target / relative).stat().st_mode & 0o111, relative)
            self.assertFalse((target / ".agent-plus/upgrade-transaction.json").exists())

    def test_managed_file_removal_is_not_a_supported_migration(self) -> None:
        manager = self.load_manager()
        prior = {
            "schema_version": "agent-plus-install/v2",
            "agent_plus_version": "0.3.0",
            "managed_set_id": manager.CURRENT_MANAGED_SET_ID,
            "profile": "research",
            "source_repository": manager.SOURCE_REPOSITORY,
            "managed_files": {relative: "0" * 64 for relative in manager.CURRENT_MANAGED_FILES},
        }
        candidate = json.loads(json.dumps(prior))
        candidate["managed_files"].pop("AGENTS.md")
        with self.assertRaisesRegex(manager.ManagerError, "Managed-file removal is not supported"):
            manager._journal_base("synthetic", "research", prior, candidate)

    def test_upgrade_success_preserves_project_owned_state_and_cleans_transaction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            state = target / ".planning/STATE.md"
            project_rules = target / ".agent-plus/PROJECT.md"
            state.write_text("project-owned-state\n", encoding="utf-8")
            project_rules.write_text("project-owned-rules\n", encoding="utf-8")
            self.run_command("upgrade", "--target", str(target))
            self.assertEqual(state.read_text(encoding="utf-8"), "project-owned-state\n")
            self.assertEqual(project_rules.read_text(encoding="utf-8"), "project-owned-rules\n")
            for relative in (
                "scripts/ai-context.sh",
                "scripts/agent-plus-doctor.sh",
                "scripts/active_chain_guard.py",
            ):
                self.assertTrue((target / relative).stat().st_mode & 0o111, relative)
            self.assertFalse((target / ".agent-plus/upgrade-transaction.json").exists())
            self.assertFalse(any((target / ".agent-plus/.transactions").iterdir()))

    def test_commit_failures_leave_one_recoverable_transaction_and_restore_exact_bytes(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)
            managed_count = len(json.loads((target / ".agent-plus/install-manifest.json").read_text())["managed_files"])
            for failure_point, fail_at in (
                ("first", 1),
                ("middle", max(2, managed_count // 2)),
                ("last", managed_count + 1),
            ):
                with self.subTest(failure_point=failure_point):
                    if self.journal_path_exists(target):
                        self.run_command("recover", "--target", str(target))
                    self.induce_commit_failure(manager, target, fail_at)
                    current = self.journal(target)
                    self.assertEqual(current["schema_version"], "agent-plus-upgrade-transaction/v3")
                    self.assertEqual(current["state"], "RECOVERY_REQUIRED")
                    self.assertTrue(current["snapshot_complete"])
                    self.run_command("status", "--target", str(target), expected=1)
                    self.run_command("upgrade", "--target", str(target), expected=1)
                    transaction = target / ".agent-plus/.transactions" / current["transaction_id"]
                    snapshot_root = transaction / "snapshot"
                    stage_root = transaction / "stage"
                    recovery_paths = tuple(current["recovery_files"])
                    self.assertTrue(all((snapshot_root / relative).is_file() for relative in recovery_paths))
                    self.assertTrue(all((stage_root / relative).is_file() for relative in recovery_paths))
                    self.run_command("recover", "--target", str(target))
                    self.assert_installation_snapshot(target, snapshot)
                    self.assertFalse(self.journal_path_exists(target))
                    self.run_command("recover", "--target", str(target))

    def journal_path_exists(self, target: Path) -> bool:
        return (target / ".agent-plus/upgrade-transaction.json").exists()

    def test_recover_safely_aborts_incomplete_snapshot_journal(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)
            calls = 0
            real_write = manager.TransactionFilesystem.write_journal

            def fail_after_initial_journal(filesystem: Any, journal: dict[str, Any]) -> None:
                nonlocal calls
                calls += 1
                if calls >= 2:
                    raise manager.ManagerError("injected durable journal write failure")
                real_write(filesystem, journal)

            with (
                mock.patch.object(
                    manager.TransactionFilesystem,
                    "write_journal",
                    new=fail_after_initial_journal,
                ),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)

            retained = self.journal(target)
            self.assertEqual(retained["state"], "SNAPSHOTTING")
            self.assertFalse(retained["snapshot_complete"])
            self.assertEqual(retained["recovery_digests"], {})

            manager.recover(target)

            self.assert_installation_snapshot(target, snapshot)
            self.assertFalse(self.journal_path_exists(target))
            self.assertFalse(any((target / ".agent-plus/.transactions").iterdir()))
            manager.recover(target)

    def test_initial_journal_write_failure_leaves_no_untracked_workspace(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)

            def fail_initial_journal(_filesystem: Any, _journal: dict[str, Any]) -> None:
                raise manager.ManagerError("injected initial journal write failure")

            with (
                mock.patch.object(
                    manager.TransactionFilesystem,
                    "write_journal",
                    new=fail_initial_journal,
                ),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)

            self.assertFalse(self.journal_path_exists(target))
            manager.recover(target)
            self.assert_installation_snapshot(target, snapshot)
            transactions = target / ".agent-plus/.transactions"
            self.assertFalse(transactions.exists() and any(transactions.iterdir()))

    def test_failed_initial_journal_pending_file_is_discoverable_and_recoverable(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)
            real_unlink = manager.os.unlink
            real_write_all = manager._write_all
            cleanup_names: list[str] = []

            def fail_journal_write(_fd: int, _data: bytes, label: str) -> None:
                if label == "upgrade-transaction.json":
                    raise manager.ManagerError("injected journal write failure")
                real_write_all(_fd, _data, label)

            def fail_pending_cleanup(path: str, *args: Any, **kwargs: Any) -> None:
                name = os.fspath(path)
                cleanup_names.append(name)
                if name == "upgrade-transaction.pending" or (
                    name.startswith(".upgrade-transaction.json.") and name.endswith(".tmp")
                ):
                    raise OSError("injected pending cleanup failure")
                real_unlink(path, *args, **kwargs)

            with (
                mock.patch.object(manager, "_require_platform", return_value=None),
                mock.patch.object(manager, "_write_all", side_effect=fail_journal_write),
                mock.patch.object(manager.os, "unlink", side_effect=fail_pending_cleanup),
                self.assertRaises(manager.ManagerError) as raised,
            ):
                manager.upgrade(target)

            agent = target / ".agent-plus"
            pending = agent / "upgrade-transaction.pending"
            self.assertTrue(
                pending.is_file(),
                (str(raised.exception), cleanup_names, tuple(path.name for path in agent.iterdir())),
            )
            self.assertFalse(self.journal_path_exists(target))

            manager.recover(target)

            self.assert_installation_snapshot(target, snapshot)
            self.assertFalse(pending.exists())
            self.assertFalse(
                tuple(agent.glob(".upgrade-transaction.json.*.tmp")),
            )

    def test_workspace_creation_failure_retains_discoverable_abort_route(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)
            real_workspace = manager.TransactionFilesystem.workspace

            def fail_workspace_creation(
                filesystem: Any,
                transaction_id: str,
                *,
                create: bool = False,
            ) -> Any:
                if create:
                    raise manager.ManagerError("injected workspace creation failure")
                return real_workspace(filesystem, transaction_id, create=create)

            with (
                mock.patch.object(
                    manager.TransactionFilesystem,
                    "workspace",
                    new=fail_workspace_creation,
                ),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)

            self.assertTrue(self.journal_path_exists(target))
            self.assertEqual(self.journal(target)["state"], "ABORTED")
            manager.recover(target)
            self.assert_installation_snapshot(target, snapshot)
            self.assertFalse(self.journal_path_exists(target))
            self.assertFalse(any((target / ".agent-plus/.transactions").iterdir()))

    def test_pending_journal_blocks_commands_and_rejects_symlink(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            target.mkdir()
            self.initialize(target)
            pending = target / ".agent-plus/upgrade-transaction.pending"
            pending.write_bytes(b"incomplete journal bytes")

            self.run_command("status", "--target", str(target), expected=1)
            self.run_command("upgrade", "--target", str(target), expected=1)
            self.run_command("recover", "--target", str(target))
            self.assertFalse(pending.exists())
            self.run_command("status", "--target", str(target))

            sentinel = root / "external-sentinel"
            sentinel_bytes = b"external pending target\n"
            sentinel.write_bytes(sentinel_bytes)
            pending.symlink_to(sentinel)

            self.run_command("status", "--target", str(target), expected=1)
            self.run_command("recover", "--target", str(target), expected=1)
            self.assertTrue(pending.is_symlink())
            self.assertEqual(sentinel.read_bytes(), sentinel_bytes)

    def test_partial_restore_failure_is_resumable_without_consuming_snapshot(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)
            self.induce_commit_failure(manager, target, 2)
            before = self.journal(target)
            transaction = target / ".agent-plus/.transactions" / before["transaction_id"]
            recovery_files = tuple(before["recovery_files"])
            calls = 0
            real_restore = manager._copy_to_atomic_restore

            def fail_restore(
                source_fd: int,
                destination_parent_fd: int,
                destination_name: str,
                expected: str,
            ) -> str:
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise manager.ManagerError("injected partial restore failure")
                return real_restore(source_fd, destination_parent_fd, destination_name, expected)

            with (
                mock.patch.object(manager, "_copy_to_atomic_restore", side_effect=fail_restore),
                self.assertRaises(manager.ManagerError) as raised,
            ):
                manager.recover(target)
            self.assertIn("retry recover", str(raised.exception))
            failed = self.journal(target)
            self.assertEqual(failed["state"], "RECOVERY_REQUIRED")
            self.assertEqual(
                tuple(sorted(failed["recovery_files"])),
                recovery_files,
            )
            self.assertTrue(all((transaction / "snapshot" / relative).is_file() for relative in recovery_files))
            manager.recover(target)
            self.assert_installation_snapshot(target, snapshot)
            self.assertFalse(self.journal_path_exists(target))

    def test_recovery_rejects_swapped_planning_ancestor_without_external_write(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            target.mkdir()
            self.initialize(target)
            self.induce_commit_failure(manager, target, 2)

            external = root / "external"
            (external / "templates").mkdir(parents=True)
            sentinel = external / "templates/ESSENTIAL-TASK.md"
            sentinel_bytes = b"external sentinel must remain unchanged\n"
            sentinel.write_bytes(sentinel_bytes)
            local_planning = target / ".planning"
            preserved_planning = target / ".planning.before-swap"
            local_planning.rename(preserved_planning)
            local_planning.symlink_to(external, target_is_directory=True)

            with self.assertRaises(manager.ManagerError):
                manager.recover(target)
            self.assertEqual(sentinel.read_bytes(), sentinel_bytes)
            self.assertTrue(self.journal_path_exists(target))
            self.assertEqual(self.journal(target)["state"], "RECOVERY_REQUIRED")
            self.assertTrue(local_planning.is_symlink())

            local_planning.unlink()
            preserved_planning.rename(local_planning)
            manager.recover(target)
            self.assertFalse(self.journal_path_exists(target))

    def test_commit_rejects_swapped_planning_ancestor_without_external_write(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            target.mkdir()
            self.initialize(target)
            external = root / "external"
            (external / "templates").mkdir(parents=True)
            sentinel = external / "templates/ESSENTIAL-TASK.md"
            sentinel_bytes = b"external commit sentinel must remain unchanged\n"
            sentinel.write_bytes(sentinel_bytes)
            real_replace = manager._replace_for_upgrade
            swapped = False

            def swap_before_planning_commit(
                source_fd: int,
                destination_parent_fd: int,
                destination_name: str,
                phase: str,
                expected: str | None = None,
            ) -> str:
                nonlocal swapped
                if destination_name == "ESSENTIAL-TASK.md" and not swapped:
                    local_planning = target / ".planning"
                    preserved_planning = target / ".planning.before-swap"
                    local_planning.rename(preserved_planning)
                    local_planning.symlink_to(external, target_is_directory=True)
                    swapped = True
                return real_replace(source_fd, destination_parent_fd, destination_name, phase, expected)

            with (
                mock.patch.object(manager, "_replace_for_upgrade", side_effect=swap_before_planning_commit),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)
            self.assertTrue(swapped)
            self.assertEqual(sentinel.read_bytes(), sentinel_bytes)
            self.assertTrue(self.journal_path_exists(target))
            self.assertEqual(self.journal(target)["state"], "RECOVERY_REQUIRED")
            self.assertTrue((target / ".planning").is_symlink())

            local_planning = target / ".planning"
            preserved_planning = target / ".planning.before-swap"
            local_planning.unlink()
            preserved_planning.rename(local_planning)
            manager.recover(target)
            self.assertFalse(self.journal_path_exists(target))

    def test_killed_upgrade_is_detected_and_recovered_after_restart(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            snapshot = self.installation_snapshot(target)
            child = subprocess.Popen(
                [
                    os.fspath(__import__("sys").executable),
                    "-c",
                    (
                        "import importlib.util, pathlib, sys, time; "
                        "spec=importlib.util.spec_from_file_location('agent_plus_child', "
                        "pathlib.Path('scripts/agent_plus_manager.py')); "
                        "module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); "
                        "real=module._replace_for_upgrade; calls=[0]; "
                        "exec(\"def slow(source_fd, destination_parent_fd, destination_name, phase, expected=None):\\n calls[0] += 1\\n result=real(source_fd, destination_parent_fd, destination_name, phase, expected)\\n if calls[0] == 1: time.sleep(30)\\n return result\"); "
                        "module._replace_for_upgrade=slow; module.upgrade(pathlib.Path(sys.argv[1]))"
                    ),
                    str(target),
                ],
                cwd=ROOT,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                if self.journal_path_exists(target) and self.journal(target)["state"] == "COMMITTING":
                    break
                time.sleep(0.02)
            self.assertTrue(self.journal_path_exists(target))
            child.kill()
            child.wait(timeout=5)
            if child.stdout is not None:
                child.stdout.close()
            if child.stderr is not None:
                child.stderr.close()
            self.run_command("status", "--target", str(target), expected=1)
            self.run_command("recover", "--target", str(target))
            self.assert_installation_snapshot(target, snapshot)
            self.assertFalse(self.journal_path_exists(target))

    def test_snapshot_and_journal_integrity_fail_closed_before_restore(self) -> None:
        manager = self.load_manager()
        for attack in ("snapshot", "journal"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "project"
                target.mkdir()
                self.initialize(target)
                original = self.installation_snapshot(target)
                self.induce_commit_failure(manager, target, 2)
                (target / "AGENTS.md").write_bytes(b"mixed managed state")
                mixed = self.installation_snapshot(target)
                journal = self.journal(target)
                if attack == "snapshot":
                    transaction = target / ".agent-plus/.transactions" / journal["transaction_id"]
                    victim = transaction / "snapshot" / next(iter(journal["recovery_files"]))
                    victim.chmod(0o644)
                    victim.write_bytes(b"tampered snapshot")
                else:
                    (target / ".agent-plus/upgrade-transaction.json").write_text(
                        '{"schema_version":"agent-plus-upgrade-transaction/v1"}',
                        encoding="utf-8",
                    )
                with self.assertRaises(manager.ManagerError):
                    manager.recover(target)
                if attack == "snapshot":
                    self.assertEqual(self.journal(target)["state"], "RECOVERY_REQUIRED")
                self.assertEqual(self.installation_snapshot(target), mixed)
                self.assertNotEqual(original, mixed)

    def test_recovered_journal_cannot_cleanup_unauthenticated_mixed_target(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            original = self.installation_snapshot(target)
            self.induce_commit_failure(manager, target, 2)

            mixed_bytes = b"attempt-07 mixed managed bytes\n"
            (target / "AGENTS.md").write_bytes(mixed_bytes)
            mixed = self.installation_snapshot(target)
            journal = self.journal(target)
            journal["state"] = "RECOVERED"
            journal["restored_files"] = list(journal["recovery_files"])
            journal["last_error"] = ""
            (target / ".agent-plus/upgrade-transaction.json").write_text(
                json.dumps(journal, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            with self.assertRaises(manager.ManagerError):
                manager.recover(target)

            self.assertEqual((target / "AGENTS.md").read_bytes(), mixed_bytes)
            self.assertEqual(self.installation_snapshot(target), mixed)
            self.assertTrue(self.journal_path_exists(target))
            self.assertTrue(
                (target / ".agent-plus/.transactions" / journal["transaction_id"]).is_dir()
            )
            self.assertEqual(self.journal(target)["state"], "RECOVERY_REQUIRED")

            manager.recover(target)
            self.assert_installation_snapshot(target, original)
            self.assertFalse(self.journal_path_exists(target))

    def test_incomplete_recovery_set_is_rejected_without_false_success(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.induce_commit_failure(manager, target, 2)
            before = self.installation_snapshot(target)
            journal = self.journal(target)
            omitted = journal["recovery_files"].pop()
            journal["recovery_digests"].pop(omitted)
            (target / ".agent-plus/upgrade-transaction.json").write_text(
                json.dumps(journal, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(manager.ManagerError):
                manager.recover(target)
            self.assertEqual(self.installation_snapshot(target), before)
            self.assertTrue((target / ".agent-plus/upgrade-transaction.json").is_file())

    def test_coordinated_journal_subset_cannot_redefine_the_release(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.induce_commit_failure(manager, target, 2)
            before = self.installation_snapshot(target)
            journal = self.journal(target)
            omitted = journal["committed_files"][0]
            journal["managed_files"].remove(omitted)
            journal["recovery_files"].remove(omitted)
            journal["recovery_digests"].pop(omitted)
            journal["candidate_managed_files"].pop(omitted)
            journal["commit_files"].remove(omitted)
            journal["committed_files"].remove(omitted)
            (target / ".agent-plus/upgrade-transaction.json").write_text(
                json.dumps(journal, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(manager.ManagerError):
                manager.recover(target)
            self.assertEqual(self.installation_snapshot(target), before)

    def test_complete_output_contract_is_managed_and_drift_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            manifest = json.loads(
                (target / ".agent-plus/install-manifest.json").read_text(encoding="utf-8")
            )
            for relative in (
                "AI_AGENT_OUTPUT_POLICY.md",
                ".cursor/rules/agent-plus-output.mdc",
                "scripts/interface_consumer_guard.py",
                "tests/test_interface_consumer_guard.py",
            ):
                self.assertIn(relative, manifest["managed_files"])
                self.assertTrue((target / relative).is_file(), relative)
            (target / "AI_AGENT_OUTPUT_POLICY.md").write_text(
                "replaced output contract\n", encoding="utf-8"
            )
            self.run_command("status", "--target", str(target), expected=1)

    def test_snapshot_symlink_and_destination_symlink_are_rejected(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            self.induce_commit_failure(manager, target, 2)
            journal = self.journal(target)
            transaction = target / ".agent-plus/.transactions" / journal["transaction_id"]
            victim = transaction / "snapshot" / next(iter(journal["recovery_files"]))
            target_bytes = target / next(iter(journal["recovery_files"]))
            victim.parent.chmod(0o755)
            victim.chmod(0o644)
            victim.unlink()
            victim.symlink_to(target_bytes)
            with self.assertRaises(manager.ManagerError):
                manager.recover(target)

    def test_descriptor_anchored_snapshot_workspace_swap_does_not_escape(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            target.mkdir()
            self.initialize(target)
            external = root / "external"
            external.mkdir()
            sentinel = external / "AGENTS.md"
            sentinel_bytes = b"snapshot external sentinel\n"
            sentinel.write_bytes(sentinel_bytes)
            real_copy = manager._copy_for_upgrade
            swapped = False

            def swap_snapshot(
                source_fd: int,
                destination_parent_fd: int,
                destination_name: str,
                phase: str,
                expected: str | None = None,
            ) -> str:
                nonlocal swapped
                if phase == "snapshot" and not swapped:
                    transaction_id = self.journal(target)["transaction_id"]
                    local = target / ".agent-plus/.transactions" / transaction_id / "snapshot"
                    preserved = local.with_name("snapshot.before-swap")
                    local.rename(preserved)
                    local.symlink_to(external, target_is_directory=True)
                    swapped = True
                return real_copy(source_fd, destination_parent_fd, destination_name, phase, expected)

            with (
                mock.patch.object(manager, "_copy_for_upgrade", side_effect=swap_snapshot),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)
            self.assertTrue(swapped)
            self.assertEqual(sentinel.read_bytes(), sentinel_bytes)
            transaction_id = self.journal(target)["transaction_id"]
            local = target / ".agent-plus/.transactions" / transaction_id / "snapshot"
            preserved = local.with_name("snapshot.before-swap")
            local.unlink()
            preserved.rename(local)
            manager.recover(target)
            self.assertFalse(self.journal_path_exists(target))

    def test_descriptor_anchored_stage_source_swap_does_not_consume_or_escape(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            target.mkdir()
            self.initialize(target)
            external = root / "external"
            (external / "templates").mkdir(parents=True)
            sentinel = external / "templates/ESSENTIAL-TASK.md"
            sentinel_bytes = b"stage external sentinel\n"
            sentinel.write_bytes(sentinel_bytes)
            real_replace = manager._replace_for_upgrade
            swapped = False

            def swap_stage(
                source_fd: int,
                destination_parent_fd: int,
                destination_name: str,
                phase: str,
                expected: str | None = None,
            ) -> str:
                nonlocal swapped
                if phase == "commit" and destination_name == "ESSENTIAL-TASK.md" and not swapped:
                    transaction_id = self.journal(target)["transaction_id"]
                    local = target / ".agent-plus/.transactions" / transaction_id / "stage/.planning"
                    preserved = local.with_name(".planning.before-swap")
                    local.rename(preserved)
                    local.symlink_to(external, target_is_directory=True)
                    swapped = True
                return real_replace(source_fd, destination_parent_fd, destination_name, phase, expected)

            with (
                mock.patch.object(manager, "_replace_for_upgrade", side_effect=swap_stage),
                self.assertRaises(manager.ManagerError),
            ):
                manager.upgrade(target)
            self.assertTrue(swapped)
            self.assertEqual(sentinel.read_bytes(), sentinel_bytes)
            transaction_id = self.journal(target)["transaction_id"]
            local = target / ".agent-plus/.transactions" / transaction_id / "stage/.planning"
            preserved = local.with_name(".planning.before-swap")
            local.unlink()
            preserved.rename(local)
            manager.recover(target)
            self.assertFalse(self.journal_path_exists(target))

    def test_source_handle_remains_bound_when_source_path_is_swapped(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "source"
            destination_root = root / "destination"
            source_root.mkdir()
            destination_root.mkdir()
            source = source_root / "payload"
            original = b"opened source bytes\n"
            source.write_bytes(original)
            external = root / "external-payload"
            external_bytes = b"external source must not be read\n"
            external.write_bytes(external_bytes)
            source_root_fd = manager._open_root(source_root, "synthetic source")
            destination_fd = manager._open_root(destination_root, "synthetic destination")
            source_fd = manager._open_regular(source_root_fd, "payload")
            try:
                source.rename(source_root / "payload.before-swap")
                source.symlink_to(external)
                manager._copy_for_upgrade(
                    source_fd,
                    destination_fd,
                    "payload.copy",
                    "source-handle",
                    manager._hash_bytes(original),
                )
            finally:
                os.close(source_fd)
                os.close(source_root_fd)
                os.close(destination_fd)
            self.assertEqual((destination_root / "payload.copy").read_bytes(), original)
            self.assertEqual(external.read_bytes(), external_bytes)

    def test_restart_reopen_rejects_swapped_transaction_ancestor(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            target = root / "project"
            target.mkdir()
            self.initialize(target)
            self.induce_commit_failure(manager, target, 2)
            external = root / "external"
            external.mkdir()
            sentinel = external / "sentinel"
            sentinel_bytes = b"restart external sentinel\n"
            sentinel.write_bytes(sentinel_bytes)
            transactions = target / ".agent-plus/.transactions"
            preserved = target / ".agent-plus/.transactions.before-swap"
            transactions.rename(preserved)
            transactions.symlink_to(external, target_is_directory=True)
            with self.assertRaises(manager.ManagerError):
                manager.recover(target)
            self.assertEqual(sentinel.read_bytes(), sentinel_bytes)
            self.assertTrue(self.journal_path_exists(target))
            transactions.unlink()
            preserved.rename(transactions)
            manager.recover(target)
            self.assertFalse(self.journal_path_exists(target))

    def test_staging_and_snapshot_failures_are_typed_and_recoverable(self) -> None:
        manager = self.load_manager()
        for phase in ("snapshot", "stage"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "project"
                target.mkdir()
                self.initialize(target)
                original = self.installation_snapshot(target)
                real_copy = manager._copy_for_upgrade
                calls = 0

                def fail_copy(
                    source_fd: int,
                    destination_parent_fd: int,
                    destination_name: str,
                    copy_phase: str,
                    expected: str | None = None,
                    injected_phase: str = phase,
                    copy_function: Any = real_copy,
                ) -> str:
                    nonlocal calls
                    if copy_phase == injected_phase:
                        calls += 1
                        if calls == 1:
                            raise manager.ManagerError(f"injected {injected_phase} failure")
                    return copy_function(
                        source_fd,
                        destination_parent_fd,
                        destination_name,
                        copy_phase,
                        expected,
                    )

                with (
                    mock.patch.object(manager, "_copy_for_upgrade", side_effect=fail_copy),
                    self.assertRaises(manager.ManagerError),
                ):
                    manager.upgrade(target)
                self.assertTrue(self.journal_path_exists(target))
                self.assert_installation_snapshot(target, original)
                self.run_command("recover", "--target", str(target))
                self.assertFalse(self.journal_path_exists(target))

    def test_cleanup_failure_retains_terminal_state_for_recover(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            captured: dict[str, str] = {}

            def fail_cleanup(parent_fd: int, name: str) -> None:
                captured["transaction"] = name
                raise manager.ManagerError("injected cleanup failure")

            with (
                mock.patch.object(manager, "_remove_tree_at", side_effect=fail_cleanup),
                self.assertRaises(manager.ManagerError) as raised,
            ):
                manager.upgrade(target)
            self.assertIn("cleanup", str(raised.exception))
            self.assertEqual(self.journal(target)["state"], "COMMITTED")
            self.assertTrue(captured["transaction"])
            manager.recover(target)
            self.assertFalse(self.journal_path_exists(target))

    def test_lock_blocks_upgrade_status_and_recover(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            lock = target / ".agent-plus/upgrade.lock"
            child = subprocess.Popen(
                [
                    sys.executable,
                    "-c",
                    (
                        "import fcntl, os, sys; "
                        "fd=os.open(sys.argv[1], os.O_RDWR|os.O_CREAT, 0o600); "
                        "fcntl.flock(fd, fcntl.LOCK_EX); print('LOCKED', flush=True); "
                        "sys.stdin.read()"
                    ),
                    str(lock),
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                text=True,
            )
            self.assertIsNotNone(child.stdout)
            self.assertEqual(child.stdout.readline().strip(), "LOCKED")
            try:
                for action in (manager.status, manager.upgrade, manager.recover):
                    with self.subTest(action=action.__name__), self.assertRaises(
                        manager.ManagerError
                    ):
                        action(target)
            finally:
                if child.stdin is not None:
                    child.stdin.close()
                child.wait(timeout=5)
                if child.stdout is not None:
                    child.stdout.close()
            manager.status(target)

    def test_lock_release_preserves_replacement_owner(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            lock = target / ".agent-plus/upgrade.lock"
            displaced = target / ".agent-plus/upgrade.lock.displaced"
            with manager.TransactionFilesystem(target) as filesystem:
                with filesystem.lock(allow_stale=False):
                    lock.rename(displaced)
                    replacement = b"replacement-owner\n"
                    lock.write_bytes(replacement)
                self.assertEqual(lock.read_bytes(), replacement)

    def test_programmer_errors_are_not_swallowed_as_manager_errors(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            with (
                mock.patch.object(manager, "_managed_sources", side_effect=ValueError("programmer error")),
                self.assertRaises(ValueError),
            ):
                manager.status(target)

    def test_drift_manifest_and_managed_symlinks_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "project"
            target.mkdir()
            self.initialize(target)
            managed = target / "AGENTS.md"
            moved = target / "AGENTS.original"
            managed.rename(moved)
            managed.symlink_to(moved)
            self.run_command("status", "--target", str(target), expected=1)

    def test_discovery_skill_contract_remains_bound_to_router(self) -> None:
        skill_root = ROOT / "skills" / "agent-plus-discovery-grill"
        required = (
            skill_root / "SKILL.md",
            skill_root / "agents" / "openai.yaml",
            skill_root / "assets" / "PROJECT-DISCOVERY.md",
            skill_root / "references" / "attribution.md",
            skill_root / "references" / "MATT-POCOCK-LICENSE.txt",
        )
        for path in required:
            self.assertTrue(path.is_file(), str(path))
        template = (skill_root / "assets" / "PROJECT-DISCOVERY.md").read_text(encoding="utf-8")
        router = (ROOT / "skills" / "agent-plus" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("schema: agent-plus-project-discovery/v1", template)
        for field in (
            "owner_confirmation: AWAITING",
            "handoff_task",
            "handoff_stop_condition",
            "handoff_acceptance_check",
        ):
            self.assertIn(field, template)
        self.assertIn("$agent-plus-discovery-grill", router)


if __name__ == "__main__":
    unittest.main()
