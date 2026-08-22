# Agent+ Anti-Loop Guard v2 maker summary

Date: 2026-08-16
Role: maker (not the reviewer, not the acceptor)
Status: `AGENT_PLUS_ANTI_LOOP_GUARD_V2_MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`

## Current state

Anti-Loop Guard v1 is removed and replaced. v1 reached its second BLOCK at the same decision
interface, so a third keyword or wording patch was forbidden. v2 is an architecture reset of that
interface: one closed, strictly structured schema in which no caller-supplied natural-language
value can change an authorization decision.

The guard is synchronized across the Agent+ canonical copy, the bootstrap copy, and the SECOND LOOK
consumer copy. Nothing is accepted. One fresh independent reviewer must decide it.

## What changed

1. **Closed decision schema (`anti-loop-guard/v2`).** Every authorization field is a fixed enum or
   an exact ledger-approved identifier:
   - `change_kind`: `local_repair`, `architecture_reset`, or `execution`.
   - `outcome_kind`: one of five permitted outcome categories. Process work has no category.
   - `outcome_id`: an exact ledger-approved milestone identifier.
   - `reset_namespace`, `attempt_id`, `removed_caller_choices`: present only on an
     architecture-reset packet, and each value must be ledger-approved.
   - `stop_policy`, `review_mode`, `review_status`, `packet_type`: closed enums.
2. **All free text is removed.** v1's `action`, `user_visible_outcome`, `allowed_actions`,
   `forbidden_actions`, `stop_condition`, `acceptance_check`, `simplification_trigger.rule`, and
   `constrained_interface.caller_choices_removed` are gone, together with the keyword outcome
   heuristic and the relabel regular expression. No parallel natural-language path was added.
3. **Ledger-bound authorization.** The ledger owns the BLOCK count, the reset requirement, the
   approved reset namespace, the authorized attempt identifier, the permitted removed caller
   choices, the permitted outcome identifiers and their categories, and both required matrices. A
   packet cannot relabel a local repair as an architecture reset, because the ledger, not the
   packet, decides. `failure_class_coverage` and every matrix item must be ledger-declared.
4. **Closed input boundary.** JSON object keys must be strings at every depth; direct Python
   mappings are checked recursively for non-string keys before any sort; duplicate keys are
   rejected at every depth; unknown fields are rejected at every depth; nesting is bounded;
   malformed JSON, NaN, infinity, and unsupported schema versions return typed guard errors.
   Counters must be exact non-negative integers, so booleans, floats, negatives, numeric strings,
   NaN, and infinity are rejected.
5. **Preserved v1 protections.** Ledger-bound attack matrix and named coverage, lock-serialized
   concurrent BLOCK recording without lost updates, atomic and crash-recoverable writes, a
   fail-closed canonical/bootstrap hash binding, deterministic receipts, non-arbitrary reset
   namespaces, and the complete previous attack matrix all remain green.
6. **Receipt hardening.** The receipt binds the canonical normalized packet and the complete
   normalized ledger. Both are deep-copied before hashing, so mutating a caller's packet or ledger
   after the call cannot change the receipt. Input key order does not change the receipt.

## New falsifying attacks added

- Disguised process-only outcomes: `tests pass; data`, `review complete; result`,
  `files changed; model`, `receipts and results`, `validation passed; readiness`.
- Well-formed but unauthorized outcome identifiers: `tests-pass-data`, `docs-updated`,
  `lint-passed`, `files-written`.
- Process outcome categories outside the closed enum: `tests_passed`, `lint_passed`,
  `files_written`, `docs_updated`, `review_complete`, including a ledger that tries to declare one.
- Architecture-reset relabeling through nested caller-controlled values:
  `["Relabel a local patch"]`, `["local patching"]`, `["local_patch"]`, `["narrow-patch"]`.
- Wording variants placed in unknown or nested fields, including `notes` and a matrix
  `description`.
- Direct Python mappings with non-string keys (`1`, `None`, `True`, `2.5`) at the top level and
  nested inside a matrix and inside `permitted_outcomes`.
- Unknown nested fields in a packet matrix and in a ledger failure state.
- Unsupported schema versions in both the packet and the ledger.
- Unauthorized outcome identifiers and an outcome kind that disagrees with the ledger entry.
- Unauthorized reset namespaces in both the packet and the ledger.
- Mismatched attempt identifiers: `attempt-04`, `attempt-3`, `attempt-003`, `ATTEMPT-03`,
  `../attempt-03`.
- Canonical packet and ledger mutation after receipt creation, plus a no-mutation check on both
  inputs.

## Verification receipts

All commands below were run in this maker session and passed.

1. `python3 -m unittest discover -s tests -p 'test_*.py'` in Agent+: **41 tests, OK**. This suite
   contains the complete v1 attack matrix and all new attacks.
2. `scripts/validate-public-package.sh`: **Public package validation: PASS**, including
   `Canonical/bootstrap guard bindings: PASS`.
3. `scripts/agent-plus-doctor.sh --target <generated project>`: **Agent+ doctor: PASS** on a
   freshly initialized research project.
4. `python3 scripts/verify_ai_workflow_policy.py` in SECOND LOOK: **AI_WORKFLOW_POLICY_OK**.
5. `ruff check` on all three changed Python files: **All checks passed** (line length 100,
   `E,F,I,UP,B,SIM`).
6. `mypy --strict` on the guard: **Success: no issues found**.
7. Determinism: the Agent+ canonical guard and the bootstrap copy produced byte-identical receipts
   from identical inputs, and the SECOND LOOK copy and the Agent+ copy produced byte-identical
   receipts from the SECOND LOOK reset packet.

## Artifact identities

- Guard SHA-256 (Agent+ canonical, bootstrap, and SECOND LOOK copies are identical):
  `6a2b8c53560be68fc2aef34129a164a23d70aaa9ec1ef3d217ace9b43105e153`
- Agent+ and bootstrap ledger SHA-256:
  `9e33d2b67ea2f49d4c9abd2d1733ffcabdede5f04ca3c161b59898c29ea96703`
- Agent+ and bootstrap example packet SHA-256:
  `0407d2050e83ef395321b3ca1a99ff7559d355762041207a779087ca588aee0d`
- Agent+ test suite SHA-256:
  `3dbb9584916ad8feea6e9bba8f35ba4953f805910624341fdeb2747f6cfc8072`
- Agent+ example PASS receipt:
  `sha256:cb31bd9953ba1af53823b533477cc14519664da80695b8fee074e4408596ef7f`
- SECOND LOOK ledger SHA-256:
  `1a4752d1f587a780fb957c7a8c16609850f15aadae547e5685c96c3e1c6d5c3d`
- SECOND LOOK narrow-patch packet SHA-256:
  `cbe63131678ff8b2e47fdc2c624f26380a2ade58681975f616ce3e197a3783a7` returns typed
  `E_THIRD_LOCAL_REPAIR`.
- SECOND LOOK architecture-reset packet SHA-256:
  `006031b8e81e8253c3aa6358c232f4327cbeba7f0cac88e8032b00746da5ad70` returns PASS receipt
  `sha256:e8654e6e93918d11e7635befafeb23faf5dccc0c63b5eadef645c3be0ad955d5`.

The v1 guard hash `19126181027321b2305bb1c0fd3164edd90a2b1d0726519667423c30c0046111` and every v1
receipt are superseded and must not be reused as acceptance evidence.

## Limits

- No fresh review, acceptance, or promotion is claimed. The maker did not self-certify.
- No certified data, rehearsal, Wave B, modeling, promotion, or Git operation occurred.
- No F-16 production code changed. The SECOND LOOK F-16 boundary remains OPEN/BLOCKED.
- The reset namespace enum currently contains one approved namespace. A new consumer boundary needs
  an owner decision to add another.

## Next step

Route one fresh independent reviewer to
`.planning/essential-tasks/2026-08-16-agent-plus-anti-loop-guard-v2-integrated-review-packet.md`.

`AGENT_PLUS_ANTI_LOOP_GUARD_V2_MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`
