---
task: "Authenticate installed managed bytes before terminal recovery cleanup"
owner_role: "maker"
tier: "3"
time_budget: "90 minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "one Luna xhigh maker; deterministic evaluator; one different fresh Luna xhigh reviewer"
reasoning: "hard architecture"
authorization_scope: "Owner authorized one engineering-only architecture chain on 2026-08-22"
ownership_map: "Maker owns lifecycle implementation and tests; Sol owns deterministic evaluation; fresh reviewer owns integrated review; owner owns release"
chain_stages: "registered attempt-08 -> maker -> deterministic evaluator -> fresh reviewer -> owner release decision"
concurrency: "one writer; sequential stages; no recursive delegation"
tool_budget: "maker 40 calls or 90 minutes; reviewer 20 calls or 45 minutes"
context_budget: "40K ceiling; 12K-25K architecture target"
reserve_use: "hard-architecture reserve approved"
checkpoint_interval: "stop at maker, evaluator, or reviewer BLOCK"
overnight: "no"
unattended_execution: "yes for any long-running deterministic command"
unattended_command: "one bounded evaluator launch that writes process-owned terminal evidence"
durable_evidence: "task card, task guard receipt, tests, evaluator terminal record, review packet, review record, and promotion dossier"
return_check: "one check of the evaluator terminal record after the process returns"
polling_policy: "zero AI polling"
evaluator_commands: "complete focused lifecycle suite; full public validator; anti-loop suite; Ruff; strict mypy; compilation; shell syntax; diff check"
fresh_verifier_contract: "one different Luna xhigh reviewer completes every registered attack and named-coverage item, then returns PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-terminal-recovery-task-008.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-terminal-recovery-review-008.json"
---

# Agent+ terminal recovery authentication reset

## Accepted boundary held closed

The editorial-pass and implementation-subtraction feature is accepted. Its closeout receipt is
`sha256:2903dc923814a9d85eb3ec73a1f3213ea9a6ff3f190d95cc024a3ce0dbcd2d55`.
Do not change or review that feature unless its bytes, sources, or acceptance contract changes.

## Necessity

- **Decision:** determine whether terminal recovery cleanup can occur only after the installed
  managed bytes match the durable recovery authority.
- **Uncertainty:** find the smallest closed architecture that authenticates terminal recovery while
  preserving all accepted lifecycle and path-safety invariants.
- **Existing evidence:** closed attempt-07 proved that a structurally valid `RECOVERED` journal can
  select cleanup while mixed managed bytes remain installed.
- **Minimum action:** remove the unauthenticated terminal-cleanup choice. Bind cleanup to exact
  installed-byte authentication against the journal recovery digests.
- **Unlock:** one fresh integrated lifecycle review decision for Agent+ `0.2.0`.

## Boundary

- **Allowed artifacts:** `scripts/agent_plus_manager.py`, lifecycle tests, lifecycle attempt-08
  packets and records, the lifecycle promotion dossier, canonical ledger, hot memory, and evaluator
  evidence.
- **Allowed actions:** implement one sanitized architecture correction, add deterministic tests,
  run disposable attacks, and update lifecycle state records.
- **Forbidden actions:** editorial feature changes or review, Git operations, release, publication,
  downstream synchronization, real project upgrade, scientific work, modeling, or SECOND LOOK work.
- **Architecture rule:** a terminal `RECOVERED` state is not cleanup authority by itself. Cleanup is
  possible only after the target managed set and manifest authenticate against durable recovery
  digests through descriptor-anchored, non-following reads.
- **Removed caller choice:** no journal state or progress field can request unauthenticated terminal
  recovery cleanup.
- **Preserved invariants:** lifecycle, path safety, journal publication, recovery assets, lock
  ownership, source containment, exact managed set, and restart behavior.
- **Changed interface:** terminal recovery restart selection and cleanup authorization only.
- **Consumer discovery:** lifecycle manager, CLI, status, doctor, tests, bootstrap package, and
  public validator.
- **Real-shape smoke:** reproduce the attempt-07 valid-looking `RECOVERED` journal with mixed target
  bytes. Recovery must retain durable state and restore or fail closed. It must never clean up while
  the target is unauthenticated.
- **Stop condition:** maker, deterministic evaluator, or fresh reviewer returns `BLOCK`, or the
  fresh reviewer returns `PASS`.
- **Acceptance:** the complete deterministic lifecycle and public-package matrix passes, followed
  by one different fresh Luna xhigh review of all registered attacks and named coverage.

## Decision branches

- **If maker BLOCK:** stop. Do not evaluate, review, repair, or release.
- **If evaluator BLOCK:** stop. Do not review, repair, or release.
- **If reviewer BLOCK:** stop. Do not repair or release in this chain.
- **If reviewer PASS:** update Agent+ state truthfully and stop for the owner's release decision.

## Initial closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: attempt-08 maker dispatch
user_visible_outcome: terminal recovery cleanup requires installed-byte authentication
repeat_trigger: maker, evaluator, or fresh reviewer result
```

## Attempt-08 maker evidence — 2026-08-22

Status: `MAKER_COMPLETE — DETERMINISTIC EVALUATION REQUIRED`

Changed files:

- `scripts/agent_plus_manager.py`
- `tests/test_agent_plus_lifecycle.py`
- this maker-evidence section

Implemented architecture:

- A valid `RECOVERED` journal now selects a dedicated terminal verification route rather than
  unconditional cleanup.
- Terminal verification first rechecks every immutable snapshot file against the journal recovery
  digests, then validates the target manifest and exact managed-file set, and finally hashes every
  installed recovery file against the durable recovery digests using the existing descriptor-
  anchored, non-following target reads.
- Any mismatch durably changes the journal to `RECOVERY_REQUIRED`, retains the journal and
  recovery workspace, and returns a typed retry error. A subsequent recover can restore the
  complete snapshot and clean up only after successful verification.
- Added the exact attempt-07 regression: a structurally valid `RECOVERED` journal plus mixed
  managed bytes cannot remove recovery state; the retained transaction then restores exact prior
  bytes.

Focused deterministic evidence:

- `python3 -m unittest discover -s tests -p 'test_agent_plus_lifecycle.py'` — `29` tests passed.
- `python3 -m py_compile scripts/agent_plus_manager.py tests/test_agent_plus_lifecycle.py` — `PASS`.
- `sh -n scripts/agent-plus scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh` — `PASS`.
- `git diff --check -- scripts/agent_plus_manager.py tests/test_agent_plus_lifecycle.py` — `PASS`.

Limits and handoff:

- The complete evaluator matrix, public-package acceptance matrix, anti-loop closeout, and fresh
  independent review remain outstanding and are not certified by this maker.
- No editorial-pass or subtraction artifact was changed or rereviewed. No ledger, state truth,
  release, publication, Git, downstream synchronization, real upgrade, scientific, modeling, or
  SECOND LOOK action occurred.

## Deterministic evaluator — BLOCK — 2026-08-22

Status: `EVALUATOR_BLOCK — REVIEW NOT DISPATCHED`

The one unattended evaluator launch returned terminal status `BLOCK` at the `ruff` step. The
process completed four earlier gates: the 29-test lifecycle suite, full public-package validator,
53-test anti-loop suite, and attempt-08 task guard. The evaluator stopped at the first failed gate.

Durable evidence:

- `outputs/attempt-08-evaluator/terminal.json`
- `outputs/attempt-08-evaluator/evaluator.log`

The terminal record reports `completed_steps: 4` and `failed_step: "ruff"`. No log polling or
intermediate evidence check occurred. One terminal-record check occurred after process return.

Per the owner contract, no reviewer was dispatched and no repair followed. Lifecycle BLOCK count
remains `7` because this evaluator result was not an integrated review closeout. Architecture reset
remains required. Release, publication, downstream synchronization, real upgrade, Git, scientific,
modeling, and SECOND LOOK work remain prohibited.

## Fresh evaluator authorization — 2026-08-22

The owner authorized progress after the first evaluator stopped. The durable log showed that Ruff
did not start. `uvx` could not initialize its default cache because of an operating-system
permission error. This was an evaluator-environment failure, not a code finding.

The bounded correction uses new isolated `UV_CACHE_DIR` and `XDG_CACHE_HOME` paths. It makes no
implementation change. The fresh authorization permits one complete unattended evaluator run from
the first gate. A process error or failed gate stops the run. A reviewer starts only after complete
evaluator PASS.

## Deterministic evaluator run-2 — PASS — 2026-08-22

The one unattended run completed all 12 registered evaluator steps and returned `PASS`. Its terminal
record is `outputs/attempt-08-evaluator-run-2/terminal.json`. The process log is
`outputs/attempt-08-evaluator-run-2/evaluator.log`.

The run included the complete lifecycle suite, public-package validator, anti-loop suite, task
guard, Ruff, strict mypy, compilation, shell syntax, diff check, and all three accepted editorial
record hash checks. One fresh independent Luna xhigh review is now required. Release remains
blocked.

## Fresh independent review — PASS — 2026-08-22

Status: `AGENT_PLUS_TERMINAL_RECOVERY_AUTHENTICATION_REVIEW_ACCEPTED — OWNER RELEASE DECISION REQUIRED`

One different fresh Luna xhigh reviewer completed all `42` lifecycle attacks and all `32` named
coverage items with `PASS`. Related review-closeout and discovery boundaries also passed, for
combined totals of `59/59` attacks and `46/46` named coverage items.

The reviewer independently reproduced the attempt-07 forged `RECOVERED` journal. Recovery rejected
terminal cleanup, retained the durable journal and workspace, changed state to
`RECOVERY_REQUIRED`, and later restored exact prior bytes. The completed packet passed exact
ledger-bound closeout validation with receipt
`sha256:331cc2b02681c81acaba8aee90b9c84042dc823b0ca80f582700b15007cef038`.

Review record:
`.planning/essential-tasks/2026-08-22-agent-plus-terminal-recovery-review-record-008.md`.

The lifecycle engineering boundary is accepted for an owner release decision. No release, Git,
publication, real upgrade, downstream synchronization, scientific work, modeling, or SECOND LOOK
work occurred.
