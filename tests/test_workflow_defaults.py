from __future__ import annotations

import re
import subprocess
import tempfile
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
                for phrase in ("AI_WORKFLOW.md#unattended-execution", "AI_WORKFLOW.md#attempt-boundary-and-pre-attempt-correction", "AI_WORKFLOW.md#capacity-and-context-limits"):
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

    def test_request_meaning_contract_reaches_new_installations(self) -> None:
        # Exercise the actual delivery path, not just the source copies.
        for profile in ("research", "product"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                result = subprocess.run(
                    [str(ROOT / "scripts/agent-plus"), "init", "--target", str(target),
                     "--profile", profile, "--brain-note", "Synthetic Example"],
                    cwd=ROOT, capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                for relative in (".planning/templates/ESSENTIAL-TASK.md", "ESSENTIAL_WORK_PROTOCOL.md"):
                    self.assertEqual((target / relative).read_bytes(), (ROOT / relative).read_bytes())
                template = (target / ".planning/templates/ESSENTIAL-TASK.md").read_text()
                for field in (
                    "Owner request", "Output mode and excluded work", "Unresolved consequential scope",
                    "Semantic contract", "Known-answer cases", "Current and reconstruction ownership",
                    "Prior evidence search", "Prior evidence disposition", "Authority separation",
                ):
                    self.assertIn(field, template)
                protocol = (target / "ESSENTIAL_WORK_PROTOCOL.md").read_text()
                for requirement in (
                    "do not create another assignment or expand authority",
                    "units, sign convention, row grain, metric type",
                    "scalar, vector, grouped, and missing-value behavior",
                    "Retain the regression that exposed a defect",
                    "historical reconstruction separate from the normal entry point",
                    "REUSE_IDENTICAL", "REUSE_WITH_TASK_DELTA", "CONFLICT_REVIEW",
                    "NOT_APPLICABLE", "never transfers another task's permissions",
                ):
                    self.assertIn(requirement, protocol)
                instructions = (target / "AGENTS.md").read_text()
                self.assertIn("Use applicable standing source grants", instructions)
                self.assertIn("do not invent a metadata-only restriction", instructions)
                if profile == "research":
                    installed = (target / ".agent-plus/PROFILE.md").read_bytes()
                    self.assertEqual(installed, (ROOT / "bootstrap/profiles/research/PROFILE.md").read_bytes())
                    for rule in ("R Markdown is optional", "Descriptive work needs no fitted model",
                                 "Ordinary exploration does not acquire a hash gate",
                                 "Preserve existing required identity checks"):
                        self.assertIn(rule, installed.decode())

    def test_prior_evidence_disposition_separates_reuse_from_authority(self) -> None:
        protocol = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        template = (ROOT / ".planning/templates/ESSENTIAL-TASK.md").read_text(
            encoding="utf-8"
        )
        for disposition in (
            "REUSE_IDENTICAL",
            "REUSE_WITH_TASK_DELTA",
            "CONFLICT_REVIEW",
            "NOT_APPLICABLE",
        ):
            self.assertIn(disposition, protocol)
            self.assertIn(disposition, template)
        for search_key in (
            "source identity",
            "semantic component",
            "implementation surface",
        ):
            self.assertIn(search_key, protocol)
            self.assertIn(search_key, template)
        for retained_authority in (
            "permissions",
            "population",
            "results",
            "receipts",
            "task status",
            "publication decision",
            "release authority",
        ):
            self.assertIn(retained_authority, " ".join(protocol.split()))

    def test_existing_task_route_precedes_new_discovery(self) -> None:
        router = (ROOT / "skills/agent-plus/SKILL.md").read_text()
        self.assertLess(router.index("Resolve the existing task"), router.index("For a new research"))
        for condition in ("A routine lookup, correction or restart", "task classification requires it",
                          "owner_confirmation: CONFIRMED", "owner_confirmation: AWAITING"):
            self.assertIn(condition, router)
        self.assertIn("does not grant data, live, scientific, or promotion authority", router)

    def test_restart_and_source_admission_records_have_one_owner(self) -> None:
        handoff = (ROOT / "skills/session-context-handoff/SKILL.md").read_text()
        source = (ROOT / "skills/source-log-workflow/SKILL.md").read_text()
        template = (ROOT / "templates/session-handoff-template.md").read_text()
        for condition in ("Update the existing task handoff", "Project memory points to it",
                          "do not create another lessons register"):
            self.assertIn(condition, handoff)
        self.assertIn("latest verified state and next action first", template)
        for heading in ("## Verified state", "## Limits and BLOCKs", "## Next action", "## Restart"):
            self.assertIn(heading, template)
        for condition in ("Reuse the existing source log", "current authority",
                          "actual conditions and unresolved holds", "without authorization"):
            self.assertIn(condition, source)

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
        protocol = (ROOT / "AI_WORKFLOW.md").read_text(encoding="utf-8")
        self.assertIn("preserve that interface as the default", protocol)
        self.assertIn("Reopening removed choices requires a new necessity card", protocol)

    def test_pre_attempt_mechanical_correction_boundary_is_explicit(self) -> None:
        workflow = (ROOT / "AI_WORKFLOW.md").read_text(encoding="utf-8")
        protocol = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        template = (ROOT / ".planning/templates/ESSENTIAL-TASK.md").read_text(encoding="utf-8")

        for phrase in (
            "first authorized irreversible, live, or scientific action",
            "first source or secret access",
            "attempt-journal creation or consumption",
            "one obvious syntax, quoting, path-handling, command-spelling, or test-harness",
            "Fix it once",
            "source, data, and secret reads remain at zero",
            "reviewer issued `BLOCK`",
            "a second correction is needed",
            "does not increment the governed attempt count and is not a retry",
            "After attempt start, the scientific or live first-error rule remains fully binding",
        ):
            self.assertIn(phrase, workflow)
        self.assertRegex(workflow, re.compile(r"task card\s+must name the exact attempt-start evidence"))
        for phrase in ("Missing or ambiguous evidence", "first-error rule remains fully binding"):
            self.assertIn(phrase, workflow)
        self.assertIn("AI_WORKFLOW.md#attempt-boundary-and-pre-attempt-correction", protocol)
        self.assertIn("**Attempt-start evidence:**", template)
        self.assertIn("**Pre-attempt correction allowance:**", template)

    def test_pre_attempt_boundary_distributed_files_match_bootstrap(self) -> None:
        for relative in (
            "AI_WORKFLOW.md",
            "ESSENTIAL_WORK_PROTOCOL.md",
            ".planning/templates/ESSENTIAL-TASK.md",
        ):
            self.assertEqual(
                (ROOT / relative).read_bytes(),
                (ROOT / "bootstrap/base" / relative).read_bytes(),
            )

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

        for relative in ("ESSENTIAL_WORK_PROTOCOL.md", "bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            for route in (
                "AI_WORKFLOW.md#engineering-closure-and-review",
                "AI_WORKFLOW.md#continuous-repair-default",
                "AI_WORKFLOW.md#bounded-session-modes",
            ):
                self.assertIn(route, text, relative)

        protocol = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertIn("inspect the exact dependency graph", protocol)
        self.assertRegex(protocol, re.compile(r"Reuse\s+current expensive ancestors"))
        profile = (ROOT / "bootstrap/profiles/research/PROFILE.md").read_text(encoding="utf-8")
        self.assertIn("smallest target that reaches the decision endpoint", profile)


if __name__ == "__main__":
    unittest.main()
