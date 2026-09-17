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


def load(name):
    spec = importlib.util.spec_from_file_location(
        name, ROOT / "scripts" / (name + ".py")
    )
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


anti = load("anti_loop_guard")
chain = load("active_chain_guard")
consumer = load("interface_consumer_guard")
manager = load("agent_plus_manager")
scanner = load("public_safety_scan")


class RepairTests(unittest.TestCase):
    def initialize(self, root):
        return subprocess.run(
            [
                "sh",
                str(ROOT / "scripts/agent-plus-init.sh"),
                "--target",
                str(root),
                "--profile",
                "research",
                "--brain-note",
                "Synthetic",
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_bootstrap_generated_caches_are_not_installed(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source"
            shutil.copytree(ROOT / "bootstrap", source / "bootstrap")
            shutil.copytree(ROOT / "scripts", source / "scripts")
            shutil.copy2(ROOT / "VERSION", source / "VERSION")
            for relative in ("scripts", "tests"):
                cache = source / "bootstrap/base" / relative / "__pycache__"
                cache.mkdir(exist_ok=True)
                (cache / "synthetic.pyc").write_bytes(b"synthetic cache")
            target = Path(directory) / "target"
            target.mkdir()
            result = subprocess.run(
                ["sh", str(source / "scripts/agent-plus-init.sh"), "--target",
                 str(target), "--profile", "research", "--brain-note", "Synthetic"],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertFalse((target / "scripts/__pycache__").exists())
            self.assertFalse((target / "tests/__pycache__").exists())
            self.assertEqual(len(list((source / "bootstrap/base").rglob("synthetic.pyc"))), 2)

    def test_every_staged_leaf_collision_preserves_owner_content(self):
        leaves = sorted(
            path
            for path in manager.CURRENT_MANAGED_FILES
            if path.startswith(("scripts/", "tests/"))
        )
        for relative in leaves:
            for kind in ("file", "directory", "symlink"):
                with (
                    self.subTest(relative=relative, kind=kind),
                    tempfile.TemporaryDirectory() as directory,
                ):
                    root = Path(directory)
                    path = root / relative
                    path.parent.mkdir(exist_ok=True)
                    if kind == "file":
                        path.write_text("owner sentinel")
                    elif kind == "directory":
                        path.mkdir()
                        (path / "owner.txt").write_text("owner sentinel")
                    else:
                        (root / "owner.txt").write_text("owner sentinel")
                        path.symlink_to(root / "owner.txt")
                    result = self.initialize(root)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse((root / "AGENTS.md").exists())
                    self.assertEqual(
                        (
                            path / "owner.txt" if kind == "directory" else path
                        ).read_text(),
                        "owner sentinel",
                    )

    def test_duplicate_conflicting_and_distinct_closeouts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ledger = root / "ledger.json"
            packet = root / "packet.json"
            ledger.write_bytes(
                (ROOT / ".agent-plus/engineering-boundaries.json").read_bytes()
            )
            raw = json.loads(
                (ROOT / ".agent-plus/engineering-closure-example.json").read_text()
            )
            packet.write_text(json.dumps(raw))
            self.assertEqual(anti._record_block_file(ledger, packet)["block_count"], 1)
            before = ledger.read_bytes()
            self.assertEqual(
                anti._record_block_file(ledger, packet)["status"],
                "BLOCK_ALREADY_RECORDED",
            )
            self.assertEqual(before, ledger.read_bytes())
            raw["packet_id"] += "-SECOND"
            packet.write_text(json.dumps(raw))
            self.assertEqual(anti._record_block_file(ledger, packet)["block_count"], 2)
            self.assertEqual(
                anti._record_block_file(ledger, packet)["status"],
                "BLOCK_ALREADY_RECORDED",
            )
            raw["review_status"] = "planned"
            packet.write_text(json.dumps(raw))
            with self.assertRaises(anti.GuardError):
                anti._record_block_file(ledger, packet)

    def fixture(self, root):
        (root / "src").mkdir()
        (root / "src/api.py").write_text("def sample_api(): return 1\n")
        return {
            "schema_version": consumer.INTERFACE_CONSUMER_SCHEMA_VERSION,
            "interfaces": [
                {
                    "interface_id": "api",
                    "definition_path": "src/api.py",
                    "search_roots": ["src"],
                    "search_tokens": ["sample_api"],
                    "consumers": [],
                }
            ],
            "real_shape_smoke": {
                "required": False,
                "status": "NOT_REQUIRED",
                "command": "not-required",
                "evidence": "not-required",
            },
        }

    def test_all_supported_analytical_consumers_outside_declared_roots_block(self):
        for suffix in (".R", ".r", ".Rmd", ".qmd", ".sql", ".yaml", ".yml", ".ipynb"):
            with (
                self.subTest(suffix=suffix),
                tempfile.TemporaryDirectory() as directory,
            ):
                root = Path(directory)
                raw = self.fixture(root)
                (root / "other").mkdir()
                (root / "other" / ("consumer" + suffix)).write_text("sample_api()")
                with self.assertRaisesRegex(
                    consumer.InterfaceConsumerGuardBlocked, "undeclared"
                ):
                    consumer.validate_receipt(raw, root=root)

    def test_smoke_writer_binds_command_inputs_and_output(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = self.fixture(root)
            raw["real_shape_smoke"] = {
                "required": True,
                "status": "PASS",
                "command": "python3 -c 'print(1)'",
                "evidence": consumer.SMOKE_PATH,
            }
            with self.assertRaises(consumer.InterfaceConsumerGuardBlocked):
                consumer.validate_receipt(raw, root=root)
            consumer.record_smoke(raw, root, ["python3", "-c", "print(1)"])
            consumer.validate_receipt(raw, root=root)
            (root / "src/api.py").write_text("def sample_api(): return 2\n")
            with self.assertRaisesRegex(
                consumer.InterfaceConsumerGuardBlocked, "identity"
            ):
                consumer.validate_receipt(raw, root=root)
            consumer.record_smoke(raw, root, ["python3", "-c", "print(1)"])
            (root / consumer.SMOKE_LOG).write_text("tampered")
            with self.assertRaisesRegex(
                consumer.InterfaceConsumerGuardBlocked, "output identity"
            ):
                consumer.validate_receipt(raw, root=root)

    def test_bad_consumer_enums_and_encoding_are_typed(self):
        for field in ("kind", "disposition"):
            for invalid in ([], {}, None, 1):
                with tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    raw = self.fixture(root)
                    item = {
                        "path": "src/api.py",
                        "kind": "production",
                        "disposition": "updated",
                        "acceptance_checks": ["synthetic"],
                    }
                    item[field] = invalid
                    raw["interfaces"][0]["consumers"] = [item]
                    with self.assertRaises(consumer.InterfaceConsumerGuardBlocked):
                        consumer.validate_receipt(raw, root=root)
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "bad.json"
            p.write_bytes(b"\xff")
            with self.assertRaises(consumer.InterfaceConsumerGuardBlocked):
                consumer.load_receipt(p)

    def test_startup_requires_all_procedures_and_readiness_runs_hook(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(self.initialize(root).returncode, 0)
            hook = root / ".agent-plus/project-startup-check.sh"
            hook.write_text("#!/bin/sh\nexit 19\n")
            hook.chmod(0o755)
            structural = subprocess.run(
                [
                    "sh",
                    str(root / "scripts/agent-plus-doctor.sh"),
                    "--target",
                    str(root),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(structural.returncode, 0)
            self.assertIn("STRUCTURE_PASS", structural.stdout)
            readiness = subprocess.run(
                [
                    "sh",
                    str(root / "scripts/agent-plus-doctor.sh"),
                    "--target",
                    str(root),
                    "--readiness",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(readiness.returncode, 0)
            hook.unlink()
            (root / "ESSENTIAL_WORK_PROTOCOL.md").unlink()
            startup = subprocess.run(
                ["sh", str(root / "scripts/ai-context.sh")],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(startup.returncode, 0)
            self.assertNotIn("## AGENTS.md", startup.stdout)

    def test_terminal_block_at_limit_is_valid_but_continuation_is_not(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".agent-plus").mkdir()
            (root / "authority.md").write_text("synthetic")
            raw = json.loads(
                (ROOT / ".agent-plus/active-chain-example.json").read_text()
            )
            raw.update(
                status="block",
                same_interface_failures=2,
                change_kind="local_repair",
                authority_refs=["authority.md"],
            )
            raw["stages"][0].update(status="block", evidence="authority.md")
            for stage in raw["stages"][1:]:
                stage.update(status="pending", evidence="")
            path = root / ".agent-plus/active-chain.json"
            path.write_text(json.dumps(raw))
            self.assertIn("CLOSEOUT_BLOCK", chain.validate(path, root, "closeout"))
            with self.assertRaises(chain.ChainError):
                chain.validate(path, root, "continue")

    def test_same_version_source_difference_is_not_current(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            target = base / "target"
            target.mkdir()
            self.assertEqual(self.initialize(target).returncode, 0)
            source = base / "source"
            source.mkdir()
            for folder in ("bootstrap", "scripts"):
                shutil.copytree(ROOT / folder, source / folder)
            shutil.copy2(ROOT / "VERSION", source / "VERSION")
            p = source / "bootstrap/base/AI_WORKFLOW.md"
            p.write_text(p.read_text() + "\nSynthetic source difference.\n")
            original = manager._source_root
            try:
                manager._source_root = lambda: source
                self.assertEqual(manager.status(target), 3)
            finally:
                manager._source_root = original

    def test_public_scanner_checks_text_formats_without_echoing_secrets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            token = "gh" + "p_" + "A" * 24
            for suffix in (".py", ".json", ".yml", ".R", ".ipynb"):
                (root / ("fixture" + suffix)).write_text(token)
            findings = scanner.scan(root)
            self.assertEqual(len(findings), 5)
            self.assertNotIn(token, str(findings))


class PublicInventoryValidationTests(unittest.TestCase):
    def run_checks(self, root):
        # Execute the production heredoc, without a second implementation.
        source = (ROOT / "scripts/validate-public-package.sh").read_text()
        code = source.split("python3 - <<'PY_TEXT'\n", 1)[1].split("\nPY_TEXT\n", 1)[0]
        return subprocess.run(
            [sys.executable, "-c", code], cwd=root,
            capture_output=True, text=True, check=False,
        )

    def repository(self, root):
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        (root / ".gitignore").write_text("outputs/\n")

    def test_ignored_evidence_is_not_read_or_mutated(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.repository(root)
            (root / "public.md").write_text("Public text.\n")
            evidence = root / "outputs"
            evidence.mkdir()
            fixtures = {
                "old.md": b"[bad](missing.md)  \n",
                "old.sh": b"echo old  \n",
                "invalid.md": b"\xff",
            }
            for name, content in fixtures.items():
                (evidence / name).write_bytes(content)
            result = self.run_checks(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            for name, content in fixtures.items():
                self.assertEqual((evidence / name).read_bytes(), content)

    def test_tracked_files_under_ignored_paths_still_block(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.repository(root)
            (root / "outputs").mkdir()
            (root / "outputs/public.md").write_text("[bad](missing.md)\n")
            subprocess.run(["git", "-C", str(root), "add", "-f", "outputs/public.md"], check=True)
            result = self.run_checks(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Broken public link", result.stderr)

    def test_untracked_public_links_with_special_names_still_block(self):
        for name in ("new public.md", "new\npublic.md"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.repository(root)
                (root / name).write_text("[bad](missing.md)\n")
                result = self.run_checks(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Broken public link", result.stderr)

    def test_valid_public_file_directory_anchor_and_external_links_pass(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.repository(root)
            (root / "docs").mkdir()
            (root / "docs/target file.md").write_text("Target.\n")
            (root / "public.md").write_text(
                "[file](<docs/target file.md#anchor>)\n"
                "[directory](docs) [local](#anchor)\n"
                "[web](https://example.invalid/) [mail](mailto:example@example.invalid)\n"
            )
            result = self.run_checks(root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_public_markdown_and_shell_whitespace_still_block(self):
        for suffix in (".md", ".sh"):
            with self.subTest(suffix=suffix), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.repository(root)
                (root / ("public" + suffix)).write_text("Synthetic text. \n")
                result = self.run_checks(root)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Whitespace scan failed", result.stderr)

    def test_missing_inventory_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_checks(Path(directory))
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn("Internal Markdown links: PASS", result.stdout)

    def test_public_link_to_ignored_only_target_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.repository(root)
            (root / "outputs").mkdir()
            (root / "outputs/private.md").write_text("Ignored evidence.\n")
            (root / "public.md").write_text("[evidence](outputs/private.md)\n")
            result = self.run_checks(root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Broken public link", result.stderr)


if __name__ == "__main__":
    unittest.main()
