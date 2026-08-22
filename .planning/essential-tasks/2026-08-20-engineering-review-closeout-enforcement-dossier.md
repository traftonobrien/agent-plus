# Engineering review closeout enforcement dossier

## Necessity

- **Decision:** prevent partial engineering reviews from triggering another maker-review loop.
- **Evidence:** SECOND LOOK accumulated five BLOCKs at the active F-16 Stage 0 lineage boundary,
  while review prompts repeatedly stopped after one local defect.
- **Minimum action:** require a registered boundary before dispatch and a complete ledger-bound
  attack matrix before another maker or owner decision.
- **Outcome:** one bundled repair and one integrated review per promotion boundary.
- **Stop condition:** deterministic package validation passes; fresh independent review remains
  required before release.

## Implemented boundary

- Added `--require-complete-engineering-review` to the canonical and bootstrap guard copies.
- The closeout flag accepts only a completed engineering-sweep review packet.
- A planned review can start, but it cannot unlock another maker or record a BLOCK.
- Task templates now require one stable promotion dossier, a dispatch receipt, and a closeout
  receipt.
- Workflow policy now requires guard validation before engineering maker/reviewer dispatch and
  forbids dispatch from a partial reviewer narrative.
- SECOND LOOK registered `SECOND_LOOK_F16_STAGE0_LINEAGE/authority-consistency`, its complete attack
  matrix, and one planned review packet. The planned packet passes the guard.

## Deterministic receipt

- Guard unit tests: 49 passed.
- Public-package validator: 60 passed; canonical/bootstrap bindings PASS; links PASS.
- Ruff: clean.
- Strict mypy: clean.
- Canonical, bootstrap, and SECOND LOOK guard SHA-256:
  `73b9722d37452cda93f3d4aff0d96a982aa92dacc0d64a549daa82dea95f2aca`.
- SECOND LOOK policy verifier: `AI_WORKFLOW_POLICY_OK`.
- F-16 planned dispatch receipt:
  `sha256:8b7ed3630ca606fff6c922fdaa51160dafd4d8d868e8b6b287d6736b4bddb69b`.

## Integrated review

Pending fresh independent Agent+ review. Do not commit, push, tag, release, or announce this change.
The reviewer must attack planned-versus-complete closeout, non-review packet rejection, incomplete
matrix rejection, ledger drift, canonical/bootstrap parity, and the SECOND LOOK consumer binding.
