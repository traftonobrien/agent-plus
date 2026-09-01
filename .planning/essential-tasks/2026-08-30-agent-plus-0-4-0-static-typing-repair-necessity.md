# Agent+ 0.4.0 manifest static-typing repair — necessity

Date: 2026-08-30

Status: `AUTHORIZED BOUNDED REPAIR`.

- **Decision:** Whether the lifecycle manager can retain its exact runtime manifest validation while
  also passing the strict static-typing gate required by prior Agent+ releases.
- **Uncertainty:** Runtime tests and public validation pass, but strict mypy cannot prove two
  managed-set identity values are strings after the current dictionary reads.
- **Existing evidence:** Ruff passes. Strict mypy reports exactly two errors at the current-manifest
  assignment and `_manifest_set_id` return. A read-only sweep found no adjacent static defect.
- **Minimum action:** Introduce explicit local value narrowing at those two seams, add one malformed
  helper probe if needed, and rerun the complete registered matrix.
- **Unlock:** The proposed `0.4.0` release scope can return to fresh review and a later owner release
  decision.
- **Stop condition:** Maker `PASS` or `BLOCK`, deterministic evaluation, then one fresh independent
  review before release-readiness acceptance.
- **Repeat trigger:** Another strict-mypy defect, any runtime behavior change, or reviewer `BLOCK`.
- **Budget:** One bounded production repair plus focused synthetic coverage. No version change,
  staging, commit, push, tag, release, consumer synchronization, data access, or scientific work.

Failure class: `manifest-strict-mypy-narrowing` under `AGENT_PLUS_RELEASE_READINESS`.

Public boundary: generic manifest parsing only. No proving-project state or consumer artifact is in
scope.
