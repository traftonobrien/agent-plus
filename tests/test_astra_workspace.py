from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StartupContextTests(unittest.TestCase):
    def make_project(self, base: Path) -> Path:
        project = base / 'project with spaces'
        (project / 'scripts').mkdir(parents=True)
        (project / '.planning').mkdir()
        (project / '.agent-plus').mkdir()
        shutil.copy2(ROOT / 'scripts/ai-context.sh', project / 'scripts/ai-context.sh')
        for name in ['AGENTS.md', 'AI_WORKFLOW.md', 'AI_AGENT_OUTPUT_POLICY.md', '.claude-memory.md', '.planning/STATE.md']:
            (project / name).write_text(f'{name} CONTENT\n', encoding='utf-8')
        return project

    def run_context(self, project: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run([str(project / 'scripts/ai-context.sh')], cwd=project.parent,
                              capture_output=True, text=True, timeout=3)

    def test_complete_current_files_and_explicit_procedure_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            for name in ['AGENTS.md', '.claude-memory.md', '.planning/STATE.md']:
                (project / name).write_text(('history\n' * 350) + f'{name} END-OF-FILE\n')
            result = self.run_context(project)
            self.assertEqual(result.returncode, 0, result.stderr)
            for name in ['AGENTS.md', '.claude-memory.md', '.planning/STATE.md']:
                self.assertIn(f'{name} END-OF-FILE', result.stdout)
            self.assertIn('AI_AGENT_OUTPUT_POLICY.md CONTENT', result.stdout)
            self.assertIn('Both remain binding', result.stdout)
            self.assertIn('AI_WORKFLOW.md before model assignment', result.stdout)

    def test_failing_hook_prevents_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            hook = project / '.agent-plus/project-startup-check.sh'
            hook.write_text('#!/bin/sh\nexit 19\n'); hook.chmod(0o755)
            result = self.run_context(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('## AGENTS.md', result.stdout)

    def test_unsafe_or_unreadable_output_policy_never_emits_partial_packet(self) -> None:
        for kind in ['missing', 'symlink', 'fifo', 'directory', 'invalid-utf8']:
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temporary:
                project = self.make_project(Path(temporary))
                policy = project / 'AI_AGENT_OUTPUT_POLICY.md'; policy.unlink()
                if kind == 'symlink': policy.symlink_to(project / 'AGENTS.md')
                elif kind == 'fifo': os.mkfifo(policy)
                elif kind == 'directory': policy.mkdir()
                elif kind == 'invalid-utf8': policy.write_bytes(b'\xff')
                result = self.run_context(project)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('## AGENTS.md', result.stdout)

    def test_state_symlink_parent_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            (project / '.planning').rename(project / 'saved-planning')
            (project / '.planning').symlink_to(project / 'saved-planning', target_is_directory=True)
            result = self.run_context(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('## AGENTS.md', result.stdout)

    def test_missing_workflow_still_blocks_before_context(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = self.make_project(Path(temporary))
            (project / 'AI_WORKFLOW.md').unlink()
            result = self.run_context(project)
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn('## AGENTS.md', result.stdout)


class SkillDiscoveryTests(unittest.TestCase):
    def test_every_public_skill_has_unique_metadata_and_exact_discovery_target(self) -> None:
        names: set[str] = set()
        skills = list((ROOT / 'skills').glob('*/SKILL.md'))
        for path in skills:
            text = path.read_text()
            self.assertTrue(text.startswith('---\n'), str(path))
            frontmatter = text.split('---', 2)[1]
            name = re.search(r'^name: ([a-z][a-z0-9-]+)$', frontmatter, re.M)
            description = re.search(r'^description: (.+)$', frontmatter, re.M)
            self.assertIsNotNone(name, str(path)); self.assertIsNotNone(description, str(path))
            assert name and description
            self.assertNotIn(name[1], names)
            names.add(name[1])
            self.assertLessEqual(len(description[1]), 400)
            mirror = ROOT / '.agents/skills' / name[1]
            self.assertTrue(mirror.is_dir(), str(mirror))
            self.assertFalse(mirror.is_symlink(), str(mirror))
            def inventory(directory: Path) -> dict[str, tuple[bytes, int]]:
                result: dict[str, tuple[bytes, int]] = {}
                for entry in directory.rglob('*'):
                    self.assertFalse(entry.is_symlink(), str(entry))
                    if '__pycache__' in entry.parts or entry.suffix == '.pyc':
                        continue
                    if entry.is_file():
                        result[entry.relative_to(directory).as_posix()] = (
                            entry.read_bytes(), entry.stat().st_mode & 0o777
                        )
                    else:
                        self.assertTrue(entry.is_dir(), str(entry))
                return result
            self.assertEqual(inventory(mirror), inventory(path.parent), name[1])
        self.assertEqual({p.name for p in (ROOT / '.agents/skills').iterdir()}, names)

    def test_shared_startup_and_workflow_are_exactly_portable(self) -> None:
        for name in ['AI_WORKFLOW.md', 'ESSENTIAL_WORK_PROTOCOL.md', 'AI_AGENT_OUTPUT_POLICY.md', 'scripts/ai-context.sh']:
            self.assertEqual((ROOT / name).read_bytes(), (ROOT / 'bootstrap/base' / name).read_bytes(), name)

    def test_same_applicability_contract_reaches_both_instruction_entrypoints(self) -> None:
        def contract(path: Path) -> str:
            return path.read_text().split('## Task applicability\n', 1)[1].split('## Context layers\n', 1)[0]
        self.assertEqual(contract(ROOT / 'AGENTS.md'), contract(ROOT / 'bootstrap/base/AGENTS.md'))


if __name__ == '__main__':
    unittest.main()
