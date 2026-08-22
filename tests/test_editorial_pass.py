from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/editorial-pass/SKILL.md"
ATTRIBUTION = ROOT / "skills/editorial-pass/references/attribution.md"
CHECKER = ROOT / "scripts/editorial_preservation_check.py"


class EditorialPassTests(unittest.TestCase):
    def test_skill_preserves_judgment_and_rejects_authorship_scoring(self) -> None:
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Make the smallest useful editorial change",
            "Do not guess who wrote the text",
            "Keep passive voice",
            "Keep an em dash",
            "Do not ban all adverbs",
            "Do not optimize prose to evade a detector",
        ):
            self.assertIn(phrase, text)

    def test_attribution_pins_sources_and_preserves_licenses(self) -> None:
        text = ATTRIBUTION.read_text(encoding="utf-8")
        for commit in (
            "d30eddb9e04562234f2070b5ee63ca4649d9a05e",
            "b33718bb9283c11b09567dc714f92d90ffb7bd16",
            "36b4a7e8d41b55ff5dff568a22f62bb0214967df",
        ):
            self.assertIn(commit, text)
        for path, notice in (
            ("PETER-YANG-LICENSE.txt", "Copyright (c) 2026 Peter Yang"),
            ("EHMO-LICENSE.txt", "Copyright (c) 2026 ehmo"),
            ("MATT-SILVERLOCK-LICENSE.txt", "Copyright (c) 2014 Matt Silverlock"),
        ):
            license_text = (ATTRIBUTION.parent / path).read_text(encoding="utf-8")
            self.assertIn(notice, license_text)
            self.assertIn("permission notice shall be included", license_text)

    def run_checker(self, source: str, revised: str, *extra: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_path = root / "source.txt"
            revised_path = root / "revised.txt"
            source_path.write_text(source, encoding="utf-8")
            revised_path.write_text(revised, encoding="utf-8")
            return subprocess.run(
                [
                    "python3",
                    str(CHECKER),
                    str(source_path),
                    str(revised_path),
                    "--format",
                    "json",
                    *extra,
                ],
                check=False,
                capture_output=True,
                text=True,
            )

    def test_checker_accepts_preserved_evidence(self) -> None:
        result = self.run_checker(
            'Agent Plus measured 42 cases on 2026-08-22. See https://example.test and `GateV2`.',
            'On 2026-08-22, Agent Plus measured 42 cases with `GateV2`. Source: https://example.test.',
            "--protect",
            "Agent Plus",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["verdict"], "PASS")

    def test_checker_blocks_changed_evidence_and_names_complete_set(self) -> None:
        result = self.run_checker(
            'Agent Plus measured 42 cases. See https://example.test and `GateV2`.',
            'Agent Plus measured 40 cases with GateV3.',
            "--protect",
            "Agent Plus",
        )
        self.assertEqual(result.returncode, 1)
        receipt = json.loads(result.stdout)
        self.assertEqual(receipt["verdict"], "BLOCK")
        self.assertEqual(
            set(receipt["missing_tokens"]),
            {"42", "https://example.test", "`GateV2`"},
        )

    def test_checker_blocks_unknown_protected_term(self) -> None:
        result = self.run_checker(
            "Agent Plus preserves exact terms.",
            "Agent Plus preserves exact terms.",
            "--protect",
            "SECOND LOOK",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Protected term is absent from source", json.loads(result.stdout)["error"])

    def test_subtraction_protocol_is_bound_and_attributed(self) -> None:
        canonical = (ROOT / "ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        bootstrap = (ROOT / "bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md").read_text(encoding="utf-8")
        self.assertEqual(canonical, bootstrap)
        for phrase in (
            "## Implementation subtraction ladder",
            "Does this need to exist?",
            "DietrichGebert/ponytail",
            "2ed6c52c9d7e5e56942508591085fd45dea277d3f",
        ):
            self.assertIn(phrase, canonical)


if __name__ == "__main__":
    unittest.main()
