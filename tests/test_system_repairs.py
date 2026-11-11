from __future__ import annotations

import importlib.util
import json
import os
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

    def faulted_init(self, root, injection):
        harness = root.parent / "fault-injection"
        harness.mkdir()
        (harness / "sitecustomize.py").write_text(
            "import os, signal, sys\nfrom pathlib import Path\n"
            "if Path(sys.argv[0]).name == 'agent_plus_init_commit.py':\n"
            "    target = Path(sys.argv[2])\n"
            "    link, mkdir = os.link, os.mkdir\n"
            + "".join("    " + line + "\n" for line in injection.splitlines())
        )
        return subprocess.run(
            [str(ROOT / "scripts/agent-plus"), "init", "--target", str(root),
             "--profile", "research", "--brain-note", "Synthetic", "--github-actions"],
            env={**os.environ, "PYTHONPATH": str(harness), "PYTHONDONTWRITEBYTECODE": "1"},
            capture_output=True, text=True, check=False, timeout=15,
        )

    def test_initializer_rolls_back_after_late_directory_collision(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            result = self.faulted_init(root, """
def collide(name, *args, **kwargs):
    if name == '.cursor':
        mkdir(target / name)
        (target / name / 'owner.txt').write_text('owner')
    return mkdir(name, *args, **kwargs)
os.mkdir = collide
""")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertEqual({p.name for p in root.iterdir()}, {".cursor"})
            self.assertEqual((root / ".cursor/owner.txt").read_text(), "owner")

    def test_initializer_preserves_owner_replacement_and_late_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            result = self.faulted_init(root, """
def collide(source, name, **kwargs):
    if name == 'CLAUDE.md':
        replacement = target / 'replacement'
        replacement.write_text('owner replacement')
        replacement.replace(target / 'AGENTS.md')
        (target / '.cursor/owner.txt').write_text('owner addition')
        (target / 'CLAUDE.md').write_text('owner collision')
    return link(source, name, **kwargs)
os.link = collide
""")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(
                {p.relative_to(root).as_posix() for p in root.rglob("*")},
                {"AGENTS.md", "CLAUDE.md", ".cursor", ".cursor/owner.txt"},
            )
            self.assertEqual((root / "AGENTS.md").read_text(), "owner replacement")
            self.assertEqual((root / "CLAUDE.md").read_text(), "owner collision")
            self.assertEqual((root / ".cursor/owner.txt").read_text(), "owner addition")

    def test_initializer_preserves_directory_replaced_during_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            result = self.faulted_init(root, """
open_dir = os.open
def replace_directory():
    if not (target / 'displaced').exists():
        (target / '.cursor').rename(target / 'displaced')
        mkdir(target / '.cursor', 0o700)
        (target / 'CLAUDE.md').write_text('owner collision')
def replace_after_mkdir(name, *args, **kwargs):
    mkdir(name, *args, **kwargs)
    if name == '.cursor' and (target / name).is_dir():
        replace_directory()
def replace_before_open(name, *args, **kwargs):
    if name == '.cursor' and kwargs.get('dir_fd') is not None and (target / name).exists():
        replace_directory()
    return open_dir(name, *args, **kwargs)
os.mkdir = replace_after_mkdir
os.open = replace_before_open
""")
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertEqual(
                {p.relative_to(root).as_posix() for p in root.rglob("*")},
                {".cursor", "displaced", "CLAUDE.md"},
            )
            self.assertEqual((root / ".cursor").stat().st_mode & 0o777, 0o700)
            self.assertEqual((root / "CLAUDE.md").read_text(), "owner collision")

    def test_initializer_preserves_in_place_file_edits_after_collision(self):
        for edit in ("content", "mode"):
            with self.subTest(edit=edit), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "project"
                root.mkdir()
                result = self.faulted_init(root, f"""
def collide(source, name, **kwargs):
    if name == 'CLAUDE.md':
        (target / name).write_text('owner collision')
    link(source, name, **kwargs)
    if name == 'AGENTS.md':
        path = target / name
        original = path.stat()
        if {edit!r} == 'content':
            path.write_bytes(b'Z' * original.st_size)
            os.utime(path, ns=(original.st_atime_ns, original.st_mtime_ns))
        else:
            path.chmod(0o600)
os.link = collide
""")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn("already exists", result.stderr)
                self.assertEqual({p.name for p in root.iterdir()}, {"AGENTS.md", "CLAUDE.md"})
                path = root / "AGENTS.md"
                if edit == "content":
                    expected_size = (ROOT / "bootstrap/base/AGENTS.md").stat().st_size
                    self.assertEqual(path.read_bytes(), b"Z" * expected_size)
                else:
                    self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_initializer_preserves_metadata_edits_after_collision(self):
        edits = ("xattr", "acl") if sys.platform == "darwin" else ("xattr",)
        for kind in ("file", "directory"):
            for edit in edits:
                with self.subTest(kind=kind, edit=edit), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory) / "project"
                    root.mkdir()
                    result = self.faulted_init(root, f"""
import subprocess
def collide(source, name, **kwargs):
    if name == 'CLAUDE.md':
        path = target / ('AGENTS.md' if {kind!r} == 'file' else '.cursor')
        if {edit!r} == 'acl':
            subprocess.run(['chmod', '+a', 'everyone allow read', str(path)], check=True)
        elif sys.platform == 'darwin':
            subprocess.run(['xattr', '-w', 'user.agentplus', 'owner', str(path)], check=True)
        else:
            os.setxattr(path, 'user.agentplus', b'owner')
        (target / name).write_text('owner collision')
    return link(source, name, **kwargs)
os.link = collide
""")
                    self.assertNotEqual(result.returncode, 0, result.stdout)
                    self.assertIn("already exists", result.stderr)
                    path = root / ("AGENTS.md" if kind == "file" else ".cursor")
                    self.assertTrue(path.exists())
                    if edit == "acl":
                        result = subprocess.run(
                            ["ls", "-lde", str(path)], capture_output=True, text=True, check=True,
                        )
                        self.assertIn("everyone allow " + ("read" if kind == "file" else "list"), result.stdout)
                    elif sys.platform == "darwin":
                        result = subprocess.run(
                            ["xattr", "-p", "user.agentplus", str(path)],
                            capture_output=True, text=True, check=True,
                        )
                        self.assertEqual(result.stdout.strip(), "owner")
                    else:
                        self.assertEqual(os.getxattr(path, "user.agentplus"), b"owner")

    def test_initializer_rolls_back_on_sigterm_and_can_retry(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "project"
            root.mkdir()
            (root / "scripts").mkdir()
            (root / "scripts/owner.txt").write_text("owner")
            result = self.faulted_init(root, """
def terminate(source, name, **kwargs):
    link(source, name, **kwargs)
    if name == 'agent-plus-doctor.yml':
        os.kill(os.getpid(), signal.SIGTERM)
os.link = terminate
""")
            self.assertEqual(result.returncode, 143, result.stdout + result.stderr)
            self.assertIn("installation interrupted", result.stderr)
            self.assertEqual(
                {p.relative_to(root).as_posix() for p in root.rglob("*")},
                {"scripts", "scripts/owner.txt"},
            )
            self.assertEqual((root / "scripts/owner.txt").read_text(), "owner")
            retry = self.initialize(root)
            self.assertEqual(retry.returncode, 0, retry.stdout + retry.stderr)
            self.assertTrue((root / ".agent-plus/install-manifest.json").is_file())

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
