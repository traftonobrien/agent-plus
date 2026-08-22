# Agent+ Anti-Loop Guard v1 fresh integrated review record

Date: 2026-08-16
Reviewer: one fresh independent Luna xhigh session; not the maker
Verdict: `AGENT_PLUS_ANTI_LOOP_GUARD_V1_REVIEW_BLOCKED`

## Current state

The consolidated repair is not accepted. The canonical, bootstrap, and SECOND LOOK guard bytes
match the claimed SHA-256, and the nine original finding families pass the required deterministic
attacks. Reviewer-authored adjacent attacks found two promotion blockers and one direct-API typed
error. No repair was designed or applied.

## What passed

- Reviewer temporary matrix: 120 checks passed in `/tmp/anti_loop_guard_review_r2.py`; the file is
  outside maker tests and is not a production artifact.
- Typed malformed JSON, duplicate keys at top-level and nested levels, exact integer BLOCK counts,
  ledger-bound complete matrices, basic process-only outcomes, fixed namespace/identifier checks,
  receipt binding, concurrent updates, lock serialization, torn-ledger recovery, and cross-root
  hash synchronization passed their expected controls.
- Valid engineering, scientific first-error, live first-error, stable/unknown boundary IDs,
  packet/ledger mismatch, first/second BLOCK tracking, `E_THIRD_LOCAL_REPAIR`, and the SECOND LOOK
  narrow-patch rejection all behaved as expected.
- The SECOND LOOK attempt-05 architecture-reset packet returned the claimed PASS receipt. Agent+
  public validation, bootstrap example validation, generated-project doctor, and the active
  SECOND LOOK policy verifier passed.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: 24 tests passed.

## What failed or remains

1. **Disguised process-only outcomes pass.** The guard accepts `tests pass; data`, `review complete;
   result`, `files changed; model`, `receipts and results`, and `validation passed; readiness`.
   The first example was sent through the CLI and returned exit code 0 with a PASS receipt
   (`sha256:b793a12729d534460b1fd85684e4a79b1ad1173f586da75f2c633b6cd698134a`). These strings do
   not name a user-visible or scientific result; they bypass the token heuristic by appending one
   allowed keyword.

2. **Reset relabel detection has bypasses.** A SECOND LOOK architecture-reset packet with
   `constrained_interface.caller_choices_removed: ["Relabel a local patch"]` returned exit code 0
   and PASS receipt `sha256:71d6dcfdf2159b33b67a666f0b685b21e80594bc4b0c044e4e3096797b56d940`.
   The same packet accepted `This is a local patching path` in `user_visible_outcome`,
   `acceptance_check`, or `stop_condition`. The detector scans mapping string values but not nested
   list values and does not catch this inflected relabel phrase.

3. **Direct mapping inputs can escape typed rejection.** Calling `validate_packet` or
   `validate_ledger` with an otherwise valid mapping plus a non-string top-level key (`1` or
   `None`) raises an uncaught `TypeError` while sorting unknown keys. JSON CLI objects cannot carry
   those key types, so this is an adjacent public-function interface finding, not a duplicate-JSON
   finding.

These findings block promotion of the shared guard and the SECOND LOOK proof. No certified data,
rehearsal, live Wave B, modeling, promotion, or Git operation occurred.

## Next step

Keep the guard and dependent SECOND LOOK boundary BLOCKED. Bundle the two semantic bypass classes
and the direct-API typed-error class with the existing repair boundary, then obtain one fresh
integrated review. Do not authorize F-16 rehearsal or scientific execution.

## Technical details

- Reviewer attack file: `/tmp/anti_loop_guard_review_r2.py` (temporary; outside maker tests).
- Agent+ guard: `scripts/anti_loop_guard.py`, SHA-256
  `19126181027321b2305bb1c0fd3164edd90a2b1d0726519667423c30c0046111`.
- Agent+ and bootstrap ledger SHA-256:
  `ae9a9c6f29fdc20962f89df04c3fe41385a645d06258ea67ce03ad0643ae478c`.
- SECOND LOOK ledger SHA-256:
  `d4f745f3250e297c9b73e618aa22c5069463b9977aa19f40baf002f0fb879eba`.
- Agent+ example receipt remains `sha256:8c70a34a463dd0de4e3c06ab6f983d16ba25fff7234215156527c70eb7b17e4d`.
- Maker receipt:
  `.planning/essential-tasks/2026-08-15-engineering-closure-loop-repair-maker-receipt.md`.
- Review packet:
  `.planning/essential-tasks/2026-08-15-engineering-closure-loop-integrated-review-packet.md`.

`AGENT_PLUS_ANTI_LOOP_GUARD_V1_REVIEW_BLOCKED`
