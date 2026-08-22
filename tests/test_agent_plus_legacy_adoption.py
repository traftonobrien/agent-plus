from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import Any
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
COMMAND = ROOT / "scripts" / "agent-plus"


class AgentPlusLegacyAdoptionTests(unittest.TestCase):
    def run_command(
        self,
        *arguments: str,
        expected: int = 0,
        timeout: float | None = None,
    ) -> subprocess.CompletedProcess[str]:
        try:
            result = subprocess.run(
                [str(COMMAND), *arguments],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            self.fail(f"command exceeded {timeout} seconds: {arguments}: {exc}")
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def run_target_command(
        self,
        target: Path,
        command: list[str],
        *,
        expected: int = 0,
        timeout: float | None = None,
    ) -> subprocess.CompletedProcess[str]:
        try:
            result = subprocess.run(
                command,
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired as exc:
            self.fail(f"command exceeded {timeout} seconds: {command}: {exc}")
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result

    def make_fifo_hook(self, target: Path) -> None:
        hook = target / ".agent-plus/project-startup-check.sh"
        hook.unlink()
        os.mkfifo(hook)

    def make_context_copies(self, target: Path) -> tuple[Path, Path]:
        canonical = target / "scripts/canonical-ai-context.sh"
        bootstrap = target / "scripts/bootstrap-ai-context.sh"
        shutil.copyfile(ROOT / "scripts/ai-context.sh", canonical)
        shutil.copyfile(ROOT / "bootstrap/base/scripts/ai-context.sh", bootstrap)
        canonical.chmod(0o755)
        bootstrap.chmod(0o755)
        return canonical, bootstrap

    def make_legacy_target(self, temporary: Path) -> Path:
        source = temporary / "initialized source"
        target = temporary / "legacy target with spaces"
        source.mkdir()
        target.mkdir()
        self.run_command(
            "init",
            "--target",
            str(source),
            "--profile",
            "research",
            "--brain-note",
            "Synthetic",
        )
        manifest = json.loads(
            (source / ".agent-plus/install-manifest.json").read_text(encoding="utf-8")
        )
        for relative in manifest["managed_files"]:
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / relative, destination)
            if relative in {"scripts/ai-context.sh", "scripts/agent-plus-doctor.sh"}:
                destination.chmod(0o755)
        hook = target / ".agent-plus/project-startup-check.sh"
        hook.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        hook.chmod(0o755)
        (target / ".claude-memory.md").write_text("legacy-memory-sentinel\n", encoding="utf-8")
        (target / ".planning/STATE.md").write_text("legacy-state-sentinel\n", encoding="utf-8")
        (target / "project-owned.txt").write_text("preserve\n", encoding="utf-8")
        return target

    def load_manager(self) -> Any:
        spec = importlib.util.spec_from_file_location(
            "agent_plus_manager_legacy_test", ROOT / "scripts/agent_plus_manager.py"
        )
        if spec is None or spec.loader is None:
            raise AssertionError("Cannot load Agent+ manager")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_exact_adoption_preserves_owned_files_and_runs_fixed_hook_before_context(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            declaration = json.loads(
                (target / ".agent-plus/legacy-adoption.json").read_text(encoding="utf-8")
            )
            self.assertEqual(
                declaration,
                {
                    "schema_version": "agent-plus-legacy-adoption/v1",
                    "mode": "legacy-adopted",
                    "profile": "research",
                    "startup_check_path": ".agent-plus/project-startup-check.sh",
                },
            )
            hook = target / ".agent-plus/project-startup-check.sh"
            hook.write_text("#!/bin/sh\nprintf 'HOOK_OK\\n'\n", encoding="utf-8")
            hook.chmod(0o755)
            doctor = self.run_command("doctor", "--target", str(target))
            self.assertIn("legacy-adopted", doctor.stdout)
            self.run_command("status", "--target", str(target))
            context = subprocess.run(
                [str(target / "scripts/ai-context.sh")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(context.returncode, 0, context.stderr)
            self.assertTrue(context.stdout.startswith("HOOK_OK\n## AGENTS.md"))
            self.assertIn("## .claude-memory.md", context.stdout)
            self.assertIn("legacy-memory-sentinel", context.stdout)
            self.assertIn("## .planning/STATE.md", context.stdout)
            self.assertIn("legacy-state-sentinel", context.stdout)
            self.assertEqual((target / "project-owned.txt").read_text(), "preserve\n")
            self.assertFalse((target / ".agent-plus/project.yaml").exists())

    def test_doctor_requires_hook_exit_zero_in_canonical_and_copied_routes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            hook = target / ".agent-plus/project-startup-check.sh"
            hook.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            hook.chmod(0o755)
            canonical = self.run_command("doctor", "--target", str(target), expected=1)
            self.assertIn("exit status 7", canonical.stderr)
            copied = subprocess.run(
                [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(copied.returncode, 1, copied.stdout + copied.stderr)
            self.assertIn("exit status 7", copied.stderr)
            context = subprocess.run(
                [str(target / "scripts/ai-context.sh")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(context.returncode, 1, context.stdout + context.stderr)
            self.assertNotIn("## AGENTS.md", context.stdout)

    def test_legacy_context_safely_omits_absent_memory_and_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            (target / ".claude-memory.md").unlink()
            (target / ".planning/STATE.md").unlink()
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            context = subprocess.run(
                [str(target / "scripts/ai-context.sh")],
                cwd=target,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(context.returncode, 0, context.stderr)
            self.assertNotIn("## .claude-memory.md", context.stdout)
            self.assertNotIn("## .planning/STATE.md", context.stdout)

    def test_divergent_managed_bytes_do_not_create_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            with (target / "AGENTS.md").open("a", encoding="utf-8") as handle:
                handle.write("drift\n")
            result = self.run_command(
                "adopt", "--target", str(target), "--profile", "research", expected=1
            )
            self.assertIn("managed bytes differ", result.stderr)
            self.assertFalse((target / ".agent-plus/install-manifest.json").exists())

    def test_symlink_startup_check_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            agent = target / ".agent-plus"
            (agent / "outside.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            (agent / "project-startup-check.sh").unlink()
            (agent / "project-startup-check.sh").symlink_to(agent / "outside.sh")
            result = self.run_command(
                "adopt", "--target", str(target), "--profile", "research", expected=1
            )
            self.assertIn("Unsafe optional target file", result.stderr)
            self.assertFalse((target / ".agent-plus/install-manifest.json").exists())

    def test_missing_startup_check_blocks_adoption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            (target / ".agent-plus/project-startup-check.sh").unlink()
            result = self.run_command(
                "adopt", "--target", str(target), "--profile", "research", expected=1
            )
            self.assertIn("requires the fixed project startup check", result.stderr)
            self.assertFalse((target / ".agent-plus/install-manifest.json").exists())

    def test_upgrade_preserves_adoption_declaration_and_startup_seam(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            declaration_before = (target / ".agent-plus/legacy-adoption.json").read_bytes()
            hook_before = (target / ".agent-plus/project-startup-check.sh").read_bytes()
            self.run_command("upgrade", "--target", str(target))
            self.assertEqual(
                (target / ".agent-plus/legacy-adoption.json").read_bytes(), declaration_before
            )
            self.assertEqual((target / ".agent-plus/project-startup-check.sh").read_bytes(), hook_before)
            self.run_command("doctor", "--target", str(target))
            self.run_command("status", "--target", str(target))

    def test_removed_startup_check_blocks_declared_adoption(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            (target / ".agent-plus/project-startup-check.sh").unlink()
            self.run_command("status", "--target", str(target), expected=1)
            self.run_command("doctor", "--target", str(target), expected=1)

    def test_hook_path_replacement_after_validation_does_not_change_executed_bytes(self) -> None:
        manager = self.load_manager()
        with tempfile.TemporaryDirectory() as directory:
            target = self.make_legacy_target(Path(directory))
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            hook = target / ".agent-plus/project-startup-check.sh"
            replacement = target / ".agent-plus/replacement.sh"
            replacement.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            replacement.chmod(0o755)
            real_run = manager.subprocess.run

            def swap_path(command: Any, *args: Any, **kwargs: Any) -> Any:
                hook.rename(target / ".agent-plus/original.sh")
                replacement.rename(hook)
                return real_run(command, *args, **kwargs)

            with mock.patch.object(manager.subprocess, "run", side_effect=swap_path):
                manager.doctor(target)
            self.assertEqual((target / ".agent-plus/original.sh").read_text(), "#!/bin/sh\nexit 0\n")

    def test_fifo_startup_hook_rejects_without_writer_within_two_seconds(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            adopt_target = self.make_legacy_target(temporary)
            self.make_fifo_hook(adopt_target)
            self.run_command(
                "adopt",
                "--target",
                str(adopt_target),
                "--profile",
                "research",
                expected=1,
                timeout=2,
            )

            valid_root = temporary / "valid"
            valid_root.mkdir()
            target = self.make_legacy_target(valid_root)
            self.run_command("adopt", "--target", str(target), "--profile", "research")
            self.make_fifo_hook(target)
            canonical_context, bootstrap_context = self.make_context_copies(target)
            checks = [
                (
                    "status",
                    [str(COMMAND), "status", "--target", str(target)],
                ),
                (
                    "canonical doctor",
                    [str(COMMAND), "doctor", "--target", str(target)],
                ),
                (
                    "copied doctor",
                    [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                ),
                ("canonical context", [str(canonical_context)]),
                ("bootstrap context", [str(bootstrap_context)]),
            ]
            for label, command in checks:
                result = self.run_target_command(
                    target,
                    command,
                    expected=1,
                    timeout=2,
                )
                self.assertNotIn("## AGENTS.md", result.stdout, label)

    def test_subset_manifest_rejects_first_middle_last_without_context_header(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            for position in ("first", "middle", "last"):
                case_root = temporary / position
                case_root.mkdir()
                target = self.make_legacy_target(case_root)
                self.run_command("adopt", "--target", str(target), "--profile", "research")
                manifest_path = target / ".agent-plus/install-manifest.json"
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                managed = list(manifest["managed_files"])
                index = {"first": 0, "middle": len(managed) // 2, "last": -1}[position]
                managed.pop(index)
                manifest["managed_files"] = {
                    relative: manifest["managed_files"][relative] for relative in managed
                }
                manifest_path.write_text(
                    json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                canonical_context, bootstrap_context = self.make_context_copies(target)
                checks = [
                    [str(COMMAND), "status", "--target", str(target)],
                    [str(COMMAND), "doctor", "--target", str(target)],
                    [str(target / "scripts/agent-plus-doctor.sh"), "--target", str(target)],
                    [str(canonical_context)],
                    [str(bootstrap_context)],
                ]
                for command in checks:
                    result = self.run_target_command(target, command, expected=1)
                    self.assertNotIn("## AGENTS.md", result.stdout)


if __name__ == "__main__":
    unittest.main()
