from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class WorkflowDefaultTests(unittest.TestCase):
    def test_canonical_and_bootstrap_controls_match(self) -> None:
        for relative in (
            "AGENTS.md",
            "AI_AGENT_OUTPUT_POLICY.md",
            "AI_WORKFLOW.md",
            "ESSENTIAL_WORK_PROTOCOL.md",
            ".cursor/rules/agent-plus-output.mdc",
            ".planning/templates/ESSENTIAL-TASK.md",
        ):
            canonical = (ROOT / relative).read_text(encoding="utf-8")
            bootstrap = (ROOT / "bootstrap/base" / relative).read_text(encoding="utf-8")
            if relative == "AGENTS.md":
                for phrase in ("one authorized launch", "zero AI polling", "one result check"):
                    self.assertIn(phrase, canonical, relative)
                    self.assertIn(phrase, bootstrap, relative)
            elif relative == "AI_WORKFLOW.md":
                for phrase in ("one authorized launch", "must not poll", "one result"):
                    self.assertIn(phrase, canonical, relative)
                    self.assertIn(phrase, bootstrap, relative)
            elif relative == "ESSENTIAL_WORK_PROTOCOL.md":
                for phrase in ("one authorized launch", "zero polls", "one result check"):
                    self.assertIn(phrase, canonical, relative)
                    self.assertIn(phrase, bootstrap, relative)
            elif relative == ".planning/templates/ESSENTIAL-TASK.md":
                for field in (
                    "unattended_execution:",
                    "polling_policy:",
                    "active_chain_capsule:",
                    "authority_refs:",
                ):
                    self.assertIn(field, canonical)
                    self.assertIn(field, bootstrap)
            if relative in (
                "AI_AGENT_OUTPUT_POLICY.md",
                "ESSENTIAL_WORK_PROTOCOL.md",
                ".planning/templates/ESSENTIAL-TASK.md",
                ".cursor/rules/agent-plus-output.mdc",
            ):
                self.assertEqual(canonical, bootstrap, relative)

    def test_plain_language_output_contract_is_portable(self) -> None:
        policy = (ROOT / "AI_AGENT_OUTPUT_POLICY.md").read_text(encoding="utf-8")
        agents = (ROOT / "bootstrap/base/AGENTS.md").read_text(encoding="utf-8")
        claude = (ROOT / "bootstrap/base/CLAUDE.md").read_text(encoding="utf-8")
        cursor = (ROOT / "bootstrap/base/.cursor/rules/agent-plus-output.mdc").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "basic everyday English",
            "What is blocking us",
            "Technical details",
            "The user does not need to request it",
        ):
            self.assertIn(phrase, policy)
        self.assertIn("Apply the output policy automatically", agents)
        self.assertIn("Apply `AI_AGENT_OUTPUT_POLICY.md` automatically", claude)
        self.assertIn("alwaysApply: true", cursor)

    def test_unattended_contract_is_complete(self) -> None:
        workflow = (ROOT / "AI_WORKFLOW.md").read_text(encoding="utf-8")
        template = (ROOT / ".planning/templates/ESSENTIAL-TASK.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "one authorized launch",
            "must not poll",
            "one result check",
            "Do not fall back, relaunch, or retry",
            "new explicit authorization",
        ):
            self.assertIn(phrase, workflow)
        self.assertRegex(workflow, re.compile(r"consumes\s+the\s+authorization"))
        for field in (
            "unattended_execution:",
            "unattended_command:",
            "durable_evidence:",
            "return_check:",
            "polling_policy:",
        ):
            self.assertIn(field, template)

    def test_closed_recovery_stays_closed(self) -> None:
        protocol = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("preserve that interface as the default", protocol)
        self.assertIn("Reopening removed choices requires a new necessity card", protocol)

    def test_lean_r_migration_defaults_are_portable(self) -> None:
        for relative in (
            "ESSENTIAL_WORK_PROTOCOL.md",
            "bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md",
        ):
            protocol = (ROOT / relative).read_text(encoding="utf-8")
            for phrase in (
                "Port complete accepted behavior",
                "representative volume",
                "Cache expensive stable stages separately",
                "Preserve failed attempts alongside the eventual result",
                "do not create a second metrics ledger",
            ):
                self.assertIn(phrase, protocol)

        profile = (ROOT / "bootstrap/profiles/research/PROFILE.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("trace complete source behavior", profile)
        self.assertIn("Retain failed attempts as evidence", profile)

    def test_complexity_is_a_diagnostic_not_a_score_gate(self) -> None:
        protocol = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        for phrase in (
            "Complexity is a diagnostic",
            "Do not impose one universal numeric threshold",
            "same branching across meaningless helpers",
            "not proof of correctness or quality",
        ):
                self.assertIn(phrase, protocol)

    def test_active_chain_and_exact_target_defaults_are_portable(self) -> None:
        for relative in (
            "AI_WORKFLOW.md",
            "bootstrap/base/AI_WORKFLOW.md",
            "ESSENTIAL_WORK_PROTOCOL.md",
            "bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md",
        ):
            text = (ROOT / relative).read_text(encoding="utf-8")
            for phrase in (
                ".agent-plus/active-chain.json",
                "live authority",
                "OWNER_DECISION_REQUIRED",
                "LOOP_DETECTED",
                "routing state only",
            ):
                self.assertIn(phrase, text, relative)

        protocol = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("inspect the exact dependency graph", protocol)
        self.assertRegex(protocol, re.compile(r"Reuse\s+current expensive ancestors"))
        profile = (ROOT / "bootstrap/profiles/research/PROFILE.md").read_text(encoding="utf-8")
        self.assertIn("smallest target that reaches the decision endpoint", profile)


if __name__ == "__main__":
    unittest.main()
