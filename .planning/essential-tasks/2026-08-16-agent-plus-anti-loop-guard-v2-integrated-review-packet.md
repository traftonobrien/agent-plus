# Agent+ Anti-Loop Guard v2 fresh integrated review packet

Date: 2026-08-16
Requested reviewer: one fresh independent session that is not this maker
Verdict required: `AGENT_PLUS_ANTI_LOOP_GUARD_V2_REVIEW_ACCEPTED` or
`AGENT_PLUS_ANTI_LOOP_GUARD_V2_REVIEW_BLOCKED`

## Scientific and authority boundary

- The reviewer is read-only. It may falsify the guard. It may not design the repair.
- The reviewer decides one named engineering question: does the v2 guard decide local repair
  against architecture reset, and reject process-only outcomes, without any dependence on
  caller-supplied wording?
- Acceptance of the guard does not authorize F-16 rehearsal, Wave B, modeling, certified data, or
  promotion. Those remain owner decisions and remain stopped.

## Changed promotion surface

Agent+ repository:

- `scripts/anti_loop_guard.py`
- `bootstrap/base/scripts/anti_loop_guard.py`
- `.agent-plus/engineering-boundaries.json`
- `bootstrap/base/.agent-plus/engineering-boundaries.json`
- `.agent-plus/engineering-closure-example.json`
- `bootstrap/base/.agent-plus/engineering-closure-example.json`
- `tests/test_anti_loop_guard.py`
- `README.md`, `AI_WORKFLOW.md`, `bootstrap/base/AI_WORKFLOW.md` guard sections
- `.planning/STATE.md`, `.claude-memory.md`

SECOND LOOK repository:

- `scripts/anti_loop_guard.py` (byte-identical copy)
- `.agent-plus/engineering-boundaries.json`
- `.planning/essential-tasks/2026-08-15-f16-launcher-narrow-patch-rejected.json`
- `.planning/essential-tasks/2026-08-15-f16-launcher-architecture-reset.json`
- `AI_WORKFLOW.md` guard section
- `.planning/essential-tasks/2026-08-16-agent-plus-anti-loop-guard-v2-necessity-card.md`
- `.planning/STATE.md`, `.claude-memory.md`

## Deterministic receipt to validate

- Guard SHA-256 in all three roots:
  `b9519db5171e1e2003bb4d94ab3b600e907e057cd446d9b1ac65a5d78d1c6f8c`
- Agent+ and bootstrap ledger SHA-256:
  `9e33d2b67ea2f49d4c9abd2d1733ffcabdede5f04ca3c161b59898c29ea96703`
- Agent+ example receipt:
  `sha256:cb31bd9953ba1af53823b533477cc14519664da80695b8fee074e4408596ef7f`
- SECOND LOOK ledger SHA-256:
  `1a4752d1f587a780fb957c7a8c16609850f15aadae547e5685c96c3e1c6d5c3d`
- SECOND LOOK narrow-patch packet returns typed `E_THIRD_LOCAL_REPAIR`.
- SECOND LOOK architecture-reset packet returns
  `sha256:e8654e6e93918d11e7635befafeb23faf5dccc0c63b5eadef645c3be0ad955d5`.
- Agent+ focused suite: 45 tests, OK.
- `scripts/validate-public-package.sh`: PASS. `scripts/agent-plus-doctor.sh`: PASS.
- SECOND LOOK `python3 scripts/verify_ai_workflow_policy.py`: `AI_WORKFLOW_POLICY_OK`.
- `ruff check` and `mypy --strict` on changed Python files: clean.

## Required independent attacks

The reviewer must author its own attacks. Do not rerun the unchanged maker suite as proof.

1. **Wording independence.** Try to make any authorization outcome change by editing only
   descriptive or nested caller-controlled text. Every such attempt must fail with a typed error.
2. **Outcome closure.** Try to declare process work as a user or scientific outcome through the
   `outcome_kind` enum, the `outcome_id` value, the ledger `permitted_outcomes` map, or any
   combination.
3. **Reset relabeling.** With a ledger at BLOCK count 2, try to pass a local repair as an
   architecture reset, and try an unauthorized namespace, attempt identifier, or removed caller
   choice.
4. **Input boundary.** Attack duplicate keys, non-string keys, unknown fields, wrong types,
   malformed JSON, NaN and infinity, unsupported schema versions, deep nesting, and counter type
   confusion through both the CLI and the public functions. No raw Python exception may escape.
5. **Ledger authority.** Confirm that a packet cannot widen coverage, matrices, namespaces,
   attempt identifiers, or outcomes beyond the ledger, and that a ledger whose reset flag disagrees
   with its BLOCK count is rejected.
6. **Receipt integrity.** Confirm determinism across key order and across the three guard copies,
   confirm that inputs are not mutated, and confirm that mutating inputs after the call cannot
   change the returned receipt.
7. **Preserved v1 matrix.** Confirm concurrency without lost updates, atomic and crash-recoverable
   writes, the canonical/bootstrap hash binding, and the first-error stop policy for scientific and
   live packets.

## Reviewer rules

- Continue bounded read-only attacks across the named boundary after the first defect. Collect the
  complete reachable failure class. Do not stop at the first failure and do not design a repair.
- Budget: 12 tool calls or 25 minutes, and at most two decisive independent attack families beyond
  receipt validation if the budget is tight.
- Do not run certified data, a rehearsal, Wave B, modeling, promotion, or any Git operation.
- Do not edit F-16 production code.
- Record the verdict, what passed, what failed, and the exact next step.

## Prior evidence

- v1 was blocked twice at this interface. The two 2026-08-16 fresh integrated review records hold
  those findings. v2 replaces the interface rather than patching it, so v1 receipts and the v1
  guard hash are superseded and are not acceptance evidence.
- Maker summary:
  `.planning/essential-tasks/2026-08-16-agent-plus-anti-loop-guard-v2-maker-summary.md`

## Outcome-catalog repair addendum — 2026-08-16

The prior fresh review found one ledger-authority defect: a scratch ledger could insert a
process-only ID such as `tests-passed` under a valid outcome category. This addendum is the single
bundled maker repair boundary for that finding. The guard now owns an immutable exact
`OUTCOME_CATALOG` mapping each permitted ID to one fixed category. A ledger may select a subset of
those entries only. Unknown, renamed, case-changed, path-like, and recategorized IDs fail as typed
malformed-ledger errors before any packet can receive a PASS receipt. Tests, lint, files, documents,
receipts, and reviews remain outside every promotable outcome category.

The canonical Agent+, bootstrap, and SECOND LOOK guards are byte-identical at SHA-256
`b9519db5171e1e2003bb4d94ab3b600e907e057cd446d9b1ac65a5d78d1c6f8c`. Agent+ and bootstrap ledger
and example-packet bytes remain identical at SHA-256 `9e33d2b67ea2f49d4c9abd2d1733ffcabdede5f04ca3c161b59898c29ea96703`
and `0407d2050e83ef395321b3ca1a99ff7559d355762041207a779087ca588aee0d`. The Agent+ example PASS
receipt remains `sha256:cb31bd9953ba1af53823b533477cc14519664da80695b8fee074e4408596ef7f` because the
receipt binds the normalized packet and ledger, not source-file bytes. The SECOND LOOK ledger and
architecture-reset packet remain at their existing identities and receipt.

## Required fresh outcome-catalog attacks

The reviewer must independently attack the complete v2 boundary again, including these repaired
cases:

1. Put each of `tests-passed`, `files-written`, `lint-passed`, `docs-updated`, and
   `review-complete` in a scratch ledger under every promotable `outcome_kind`; every ledger must
   fail before packet validation.
2. Reassign a catalog ID to a different category, and try a catalog ID that is renamed,
   case-changed, path-traversed, or otherwise forged; every ledger must fail.
3. Authorize a valid catalog ID in the ledger, then confirm valid user-visible, scientific, and
   execution packets pass, while a catalog ID absent from the ledger subset fails.
4. Re-run the prior v1/v2 wording, input-boundary, reset, first-error, ledger-binding,
   concurrency/atomicity, receipt-integrity, and three-root synchronization attacks.

Current maker evidence is 45 focused tests, public-package validation PASS, generated-project
doctor PASS, `AI_WORKFLOW_POLICY_OK`, Ruff PASS, and strict mypy PASS on each duplicate guard copy.
This remains maker evidence only. The reviewer must not design a repair or authorize F-16 rehearsal,
Wave B, certified-data reads, modeling, live execution, or promotion.
