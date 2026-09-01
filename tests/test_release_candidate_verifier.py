from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from typing import cast
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "verify_release_candidate", ROOT / "scripts/verify_release_candidate.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReleaseCandidateVerifierTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(dir=Path("/tmp").resolve())
        self.root = Path(self.temporary.name)
        self.original_cwd = Path.cwd()
        self.env = MODULE._environment()
        self.git("init", "-q")
        self.git("config", "user.name", "Synthetic")
        self.git("config", "user.email", "synthetic@example.invalid")
        self.write("VERSION", "0.3.0\n")
        self.write("a.txt", "base\n")
        self.write(".gitignore", "outputs/\nignored-local.txt\n")
        self.write(
            "scripts/validate-public-package.sh",
            '#!/bin/sh\nset -eu\ntest "$(cat VERSION)" = 0.4.0\n',
        )
        self.git("add", ".")
        self.git("commit", "-qm", "Synthetic base")
        self.base = self.git("rev-parse", "HEAD").decode().strip()
        self.manifest = ".planning/essential-tasks/candidate.txt"
        self.config = {
            "schema_version": MODULE.CONFIG_SCHEMA,
            "current_version": "0.3.0",
            "candidate_version": "0.4.0",
            "base_commit": self.base,
            "manifest_path": self.manifest,
        }
        self.write(str(MODULE.CONFIG_RELATIVE), json.dumps(self.config))
        self.write("a.txt", "candidate\n")
        self.paths = [str(MODULE.CONFIG_RELATIVE), self.manifest, "VERSION", "a.txt"]
        self.write_manifest()
        os.chdir(self.root)

    def tearDown(self) -> None:
        os.chdir(self.original_cwd)
        self.temporary.cleanup()

    def write(self, path: str, text: str) -> None:
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(text, encoding="utf-8")

    def write_manifest(self) -> None:
        self.write(self.manifest, "\n".join(sorted(self.paths)) + "\n")

    def git(self, *args: str, data: bytes | None = None) -> bytes:
        return subprocess.run(
            [MODULE.GIT, *args],
            cwd=self.root,
            env=self.env,
            input=data,
            capture_output=True,
            check=True,
        ).stdout

    def validator(self, root: Path, env: dict[str, str]) -> None:
        self.assertNotEqual(root, self.root)
        self.assertNotIn("GIT_DIR", env)
        self.assertFalse((root / ".git/objects/info/alternates").exists())
        self.assertEqual((root / "VERSION").read_text(), "0.4.0\n")
        MODULE._run(
            ("sh", "scripts/validate-public-package.sh"),
            root,
            env=env,
            code="E_PUBLIC_VALIDATOR",
        )

    def verify(self) -> dict[str, object]:
        with mock.patch.object(
            MODULE, "_validate_candidate", side_effect=self.validator
        ):
            return cast(dict[str, object], MODULE.verify(self.root))

    def receipt(self) -> dict[str, object]:
        return cast(
            dict[str, object],
            json.loads((self.root / MODULE.RECEIPT_RELATIVE).read_text()),
        )

    def test_full_path_success_preserves_source(self) -> None:
        before = MODULE.source_snapshot(self.root)
        receipt = self.verify()
        self.assertEqual(receipt["status"], "PASS")
        self.assertEqual(before, MODULE.source_snapshot(self.root))
        self.assertEqual(receipt["source_before"], receipt["source_after"])
        self.assertEqual(receipt["toolchain"], {"mypy": "2.3.1", "ruff": "0.16.5"})

    def test_existing_source_loose_object_is_not_freshened(self) -> None:
        oid = (
            self.git("hash-object", "-w", "--stdin", data=b"candidate\n")
            .decode()
            .strip()
        )
        path = self.root / ".git/objects" / oid[:2] / oid[2:]
        os.utime(path, ns=(1000000000000000000, 1000000000000000000))
        before = path.stat().st_mtime_ns
        self.verify()
        self.assertEqual(before, path.stat().st_mtime_ns)

    def test_existing_packed_objects_are_not_freshened(self) -> None:
        self.git("repack", "-ad")
        before = MODULE.tree_snapshot(self.root / ".git/objects")
        self.verify()
        self.assertEqual(before, MODULE.tree_snapshot(self.root / ".git/objects"))

    def test_hostile_environment_cannot_route_children_to_source(self) -> None:
        hostile = {
            name: str(self.root / ".git")
            for name in (
                "GIT_DIR",
                "GIT_COMMON_DIR",
                "GIT_INDEX_FILE",
                "GIT_OBJECT_DIRECTORY",
                "GIT_ALTERNATE_OBJECT_DIRECTORIES",
                "GIT_WORK_TREE",
                "GIT_CONFIG_GLOBAL",
                "GIT_TRACE",
                "GIT_TRACE2_EVENT",
                "BASH_ENV",
                "ENV",
                "PYTHONPATH",
                "PYTHONHOME",
                "LD_PRELOAD",
                "DYLD_INSERT_LIBRARIES",
            )
        }
        hostile.update(
            GIT_CONFIG_COUNT="1",
            GIT_CONFIG_KEY_0="core.worktree",
            GIT_CONFIG_VALUE_0=str(self.root),
            TMPDIR=str(self.root),
        )
        with mock.patch.dict(os.environ, hostile):
            self.verify()

    def test_source_git_commands_are_read_only_and_baseline_precedes_them(self) -> None:
        commands: list[str] = []
        original = MODULE._source_git

        def inspect(root: Path, args: tuple[str, ...], **kwargs: object) -> bytes:
            self.assertEqual(self.receipt()["status"], "RUNNING")
            commands.append(args[0])
            return cast(bytes, original(root, args, **kwargs))

        with mock.patch.object(MODULE, "_source_git", side_effect=inspect):
            self.verify()
        self.assertEqual(set(commands), {"ls-tree", "cat-file", "ls-files"})
        with self.assertRaisesRegex(MODULE.CandidateError, "E_SOURCE_COMMAND"):
            MODULE._source_git(self.root, ("write-tree",))

    def test_source_filters_and_fsmonitor_are_not_executed(self) -> None:
        self.write(".gitattributes", "*.txt filter=hostile\n")
        self.paths.append(".gitattributes")
        self.write_manifest()
        sentinel = self.root / "outputs/filter-ran"
        for key in (
            "filter.hostile.clean",
            "filter.hostile.smudge",
            "filter.hostile.process",
            "core.fsmonitor",
        ):
            self.git("config", key, f"touch '{sentinel}'; exit 1")
        self.verify()
        self.assertFalse(sentinel.exists())

    def test_literal_special_names_and_executable_modes(self) -> None:
        for path in (
            "space name.txt",
            "colon:name.txt",
            "star*.txt",
            ":(glob)literal.txt",
        ):
            self.write(path, "literal\n")
            self.paths.append(path)
        self.write("executable.sh", "#!/bin/sh\nexit 0\n")
        (self.root / "executable.sh").chmod(0o755)
        self.paths.append("executable.sh")
        self.write_manifest()
        self.verify()

    def test_extra_public_path_blocks(self) -> None:
        self.write("extra.txt", "unlisted\n")
        with self.assertRaisesRegex(MODULE.CandidateError, "E_SCOPE_MISMATCH"):
            self.verify()

    def test_ignored_and_exact_local_exclusions_are_not_exported(self) -> None:
        self.write("ignored-local.txt", "private synthetic fixture\n")
        self.write("Icon\r", "metadata\n")
        self.write("outputs/local.txt", "local\n")
        self.write(".agent-plus/.engineering-boundaries.json.lock", "lock\n")
        self.verify()

    def test_staged_only_change_cannot_disappear(self) -> None:
        self.write("staged.txt", "base\n")
        self.git("add", "staged.txt")
        self.git("commit", "-qm", "Additional synthetic base")
        self.base = self.git("rev-parse", "HEAD").decode().strip()
        self.config["base_commit"] = self.base
        self.write(str(MODULE.CONFIG_RELATIVE), json.dumps(self.config))
        self.write("staged.txt", "index only\n")
        self.git("add", "staged.txt")
        self.write("staged.txt", "base\n")
        with self.assertRaisesRegex(MODULE.CandidateError, "E_SCOPE_MISMATCH"):
            self.verify()

    def test_unmerged_index_and_gitlink_entries_reject(self) -> None:
        for record in (
            f"100644 {'a' * 40} 1\ta.txt\0",
            f"160000 commit {'a' * 40}\tsub\0",
        ):
            with self.assertRaisesRegex(MODULE.CandidateError, "E_GIT_ENTRY"):
                MODULE._entries(record.encode(), index=" 1\t" in record)

    def test_ancestor_symlink_and_fifo_reject(self) -> None:
        outside = self.root / "outside"
        outside.mkdir()
        (outside / "file").write_text("data\n")
        (self.root / "linked").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(MODULE.CandidateError):
            MODULE._read_file(self.root, "linked/file")
        os.mkfifo(self.root / "fifo")
        with self.assertRaisesRegex(MODULE.CandidateError, "E_SOURCE_FILE"):
            MODULE._read_file(self.root, "fifo")

    def test_dot_traversal_and_control_paths_reject(self) -> None:
        for path in (
            ".",
            "../x",
            "a/../x",
            "a//x",
            "/x",
            "a\nx",
            "a\0x",
            ".git/config",
            "outputs/x",
        ):
            with self.subTest(path=path), self.assertRaises(MODULE.CandidateError):
                MODULE._safe_relative(path, "test")

    def test_closed_config_and_duplicate_keys(self) -> None:
        for key, value in (
            ("unknown", "x"),
            ("candidate_version", []),
            ("manifest_path", "."),
        ):
            config = dict(self.config)
            config[key] = value
            self.write(str(MODULE.CONFIG_RELATIVE), json.dumps(config))
            with self.assertRaises(MODULE.CandidateError):
                MODULE.load_config(self.root)
        self.write(str(MODULE.CONFIG_RELATIVE), '{"x":1,"x":2}')
        with self.assertRaisesRegex(MODULE.CandidateError, "E_CONFIG_DUPLICATE_KEY"):
            MODULE.load_config(self.root)

    def test_manifest_order_duplicates_and_version(self) -> None:
        for text in ("a.txt\nVERSION\n", "VERSION\nVERSION\n", "a.txt\n"):
            self.write(self.manifest, text)
            with self.assertRaises(MODULE.CandidateError):
                MODULE.load_manifest(self.root, self.manifest)

    def test_source_mutation_is_checked_even_after_validator_failure(self) -> None:
        def mutate(root: Path, env: dict[str, str]) -> None:
            self.write("a.txt", "changed by synthetic attack\n")
            raise MODULE.CandidateError("E_PUBLIC_VALIDATOR", "synthetic failure")

        with (
            mock.patch.object(MODULE, "_validate_candidate", side_effect=mutate),
            self.assertRaisesRegex(MODULE.CandidateError, "E_SOURCE_MUTATION"),
        ):
            MODULE.verify(self.root)
        self.assertEqual(self.receipt()["error_code"], "E_SOURCE_MUTATION")

    def test_source_ref_change_blocks(self) -> None:
        def mutate(root: Path, env: dict[str, str]) -> None:
            self.write(".git/refs/tags/synthetic", self.base + "\n")

        with (
            mock.patch.object(MODULE, "_validate_candidate", side_effect=mutate),
            self.assertRaisesRegex(MODULE.CandidateError, "E_SOURCE_MUTATION"),
        ):
            MODULE.verify(self.root)

    def test_candidate_mutation_blocks(self) -> None:
        def mutate(root: Path, env: dict[str, str]) -> None:
            (root / "a.txt").write_text("changed\n")

        with (
            mock.patch.object(MODULE, "_validate_candidate", side_effect=mutate),
            self.assertRaisesRegex(MODULE.CandidateError, "E_CANDIDATE_CHANGED"),
        ):
            MODULE.verify(self.root)

    def test_new_candidate_file_blocks(self) -> None:
        def mutate(root: Path, env: dict[str, str]) -> None:
            (root / "injected.py").write_text("unexpected = True\n")

        with (
            mock.patch.object(MODULE, "_validate_candidate", side_effect=mutate),
            self.assertRaisesRegex(MODULE.CandidateError, "E_CANDIDATE_CHANGED"),
        ):
            MODULE.verify(self.root)

    def test_candidate_mode_change_blocks(self) -> None:
        def mutate(root: Path, env: dict[str, str]) -> None:
            (root / "a.txt").chmod(0o755)

        with (
            mock.patch.object(MODULE, "_validate_candidate", side_effect=mutate),
            self.assertRaisesRegex(MODULE.CandidateError, "E_CANDIDATE_CHANGED"),
        ):
            MODULE.verify(self.root)

    def test_missing_source_file_blocks_before_validation(self) -> None:
        (self.root / "a.txt").unlink()
        with (
            mock.patch.object(MODULE, "_validate_candidate") as validator,
            self.assertRaisesRegex(MODULE.CandidateError, "E_MANIFEST_FILE"),
        ):
            MODULE.verify(self.root)
        validator.assert_not_called()

    def test_missing_base_object_is_typed_and_does_not_fetch(self) -> None:
        original = MODULE._source_git

        def missing(root: Path, args: tuple[str, ...], **kwargs: object) -> bytes:
            if args[0] == "cat-file":
                self.assertEqual(MODULE._environment()["GIT_NO_LAZY_FETCH"], "1")
                return b"missing missing\n"
            return cast(bytes, original(root, args, **kwargs))

        with (
            mock.patch.object(MODULE, "_source_git", side_effect=missing),
            self.assertRaisesRegex(MODULE.CandidateError, "E_BASE_OBJECT"),
        ):
            self.verify()

    def test_replacement_refs_do_not_replace_base_bytes(self) -> None:
        self.write("replacement.txt", "replacement\n")
        self.git("add", "replacement.txt")
        self.git("commit", "-qm", "Replacement fixture")
        replacement = self.git("rev-parse", "HEAD").decode().strip()
        self.git("replace", self.base, replacement)
        files, _ = MODULE._base_files(self.root, self.base)
        self.assertNotIn("replacement.txt", files)

    def test_source_mode_change_blocks(self) -> None:
        def mutate(root: Path, env: dict[str, str]) -> None:
            (self.root / "a.txt").chmod(0o755)

        with (
            mock.patch.object(MODULE, "_validate_candidate", side_effect=mutate),
            self.assertRaisesRegex(MODULE.CandidateError, "E_SOURCE_MUTATION"),
        ):
            MODULE.verify(self.root)

    def test_configuration_failure_replaces_stale_success(self) -> None:
        self.verify()
        self.write(str(MODULE.CONFIG_RELATIVE), "malformed\n")
        with self.assertRaisesRegex(MODULE.CandidateError, "E_CONFIG_JSON"):
            self.verify()
        self.assertEqual(self.receipt()["status"], "BLOCK")

    def test_timeout_is_typed(self) -> None:
        with (
            mock.patch.object(
                MODULE.subprocess,
                "run",
                side_effect=subprocess.TimeoutExpired("synthetic", 1),
            ),
            self.assertRaisesRegex(MODULE.CandidateError, "E_TIMEOUT_TEST"),
        ):
            MODULE._run(("synthetic",), self.root, env=self.env, code="E_TIMEOUT_TEST")

    def test_full_path_failure_replaces_stale_success(self) -> None:
        first = self.verify()
        with (
            mock.patch.object(
                MODULE,
                "_validate_candidate",
                side_effect=MODULE.CandidateError(
                    "E_PUBLIC_VALIDATOR", "synthetic failure"
                ),
            ),
            self.assertRaises(MODULE.CandidateError),
        ):
            MODULE.verify(self.root)
        receipt = self.receipt()
        self.assertEqual(receipt["status"], "BLOCK")
        self.assertNotEqual(first["run_id"], receipt["run_id"])

    def test_pinned_tools_and_child_environment(self) -> None:
        env = MODULE._environment()
        with (
            mock.patch.object(MODULE.shutil, "which", return_value="uvx"),
            mock.patch.object(MODULE, "_run", return_value=b"") as run,
        ):
            MODULE._validate_candidate(self.root, env)
        self.assertIn("mypy==2.3.1", run.call_args_list[0].args[0])
        self.assertIn("ruff==0.16.5", run.call_args_list[1].args[0])
        self.assertTrue(all(call.kwargs["env"] is env for call in run.call_args_list))

    def test_failure_diagnostics_are_bounded_and_do_not_copy_stderr(self) -> None:
        with self.assertRaises(MODULE.CandidateError) as caught:
            MODULE._run(
                ("sh", "-c", "printf sensitive >&2; exit 7"),
                self.root,
                env=self.env,
                code="E_TEST",
            )
        self.assertEqual(caught.exception.details["exit_status"], 7)
        self.assertNotIn("sensitive", json.dumps(caught.exception.details))
        self.assertLess(len(json.dumps(caught.exception.details)), 250)

    def test_snapshot_detects_same_size_content_with_restored_mtime(self) -> None:
        path = self.root / ".git/description"
        before = MODULE.tree_snapshot(self.root / ".git")
        metadata = path.stat()
        path.write_bytes(b"x" * metadata.st_size)
        os.utime(path, ns=(metadata.st_atime_ns, metadata.st_mtime_ns))
        self.assertNotEqual(before, MODULE.tree_snapshot(self.root / ".git"))

    def test_receipt_symlink_parent_rejects(self) -> None:
        (self.root / "outputs").symlink_to(self.root / ".git", target_is_directory=True)
        with self.assertRaisesRegex(MODULE.CandidateError, "E_RECEIPT_PATH"):
            MODULE._write_receipt(self.root, {"status": "PASS"})

    def test_zero_option_interface(self) -> None:
        self.verify()
        with mock.patch.object(
            MODULE, "__file__", str(self.root / "scripts/verifier.py")
        ):
            self.assertEqual(MODULE.main(["--manifest", "other"]), 1)
        self.assertEqual(self.receipt()["status"], "BLOCK")
        self.assertEqual(self.receipt()["error_code"], "E_ARGUMENTS")


if __name__ == "__main__":
    unittest.main()
