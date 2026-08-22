---
task: "Replace random journal temp files with one discoverable pending-journal protocol"
owner_role: "maker"
tier: "2"
time_budget: "100 minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Sol maker; deterministic evaluator; separate fresh reviewer required"
reasoning: "implementation"
authorization_scope: "Owner authorized a new attempt for the attempt-06 review BLOCK on 2026-08-21"
ownership_map: "Sol owns maker and evaluation; a fresh reviewer owns review; owner owns release"
chain_stages: "registered attempt-07 -> red regression -> maker -> evaluator -> fresh reviewer -> owner decision"
concurrency: "one writer; no parallel work"
tool_budget: "maker 45 calls or 100 minutes; reviewer 25 calls or 60 minutes"
context_budget: "40K ceiling; 15-25K implementation target"
reserve_use: "hard-architecture reserve approved"
checkpoint_interval: "stop at maker, evaluator, or reviewer BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this card, regression tests, validator output, review packet, and promotion dossier"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "focused lifecycle tests; full validator; Ruff; strict mypy; compilation; shell syntax; diff check"
fresh_verifier_contract: "fresh read-only reviewer runs the complete matrix and returns one PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-pending-journal-task-007.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-pending-journal-review-007.json"
---

# Agent+ pending-journal publication reset

## Necessity

- **Decision:** determine whether every durable journal artifact can remain discoverable after any
  write or cleanup failure.
- **Uncertainty:** whether one fixed pending file can replace random temp names without weakening
  atomic publication or path safety.
- **Existing evidence:** attempt-06 removed untracked workspaces. Its review found that combined
  journal-write and temp-file cleanup failure leaves a random hidden file that recovery cannot find.
- **Minimum action:** replace random journal temp names with one fixed pending name. All lifecycle
  commands must recognize final and pending journal state.
- **Unlock:** one fresh review decision for Agent+ `0.2.0` journal publication.

## Boundary

- **Allowed artifacts:** lifecycle manager, lifecycle tests, canonical ledger, attempt-07 packets,
  this card, promotion dossier, and hot memory.
- **Allowed actions:** sanitized implementation, disposable attacks, and deterministic checks.
- **Forbidden actions:** SECOND LOOK edits, real project upgrades, data access, scientific work,
  Git operations, release, tag, announcement, or publication.
- **Review mode:** engineering sweep.
- **Architecture decision:** the journal writer owns exactly two fixed names:
  `upgrade-transaction.pending` and `upgrade-transaction.json`.
- **Removed caller choice:** the writer cannot create random hidden journal temporary names.
- **Changed interface:** journal existence, publication, restart, status, and cleanup.
- **Consumer discovery:** lifecycle command, Python manager, status, doctor, tests, and generated
  projects.
- **Real-shape smoke:** combine initial write failure with pending cleanup failure. Restart must
  discover and remove the pending file without target mutation.
- **Stop condition:** deterministic evaluator or fresh reviewer returns `PASS` or `BLOCK`.
- **Acceptance:** every durable journal artifact uses a fixed name and has one typed restart route.

## Decision branches

- **If PASS:** dispatch one fresh independent review. Release remains blocked.
- **If BLOCK:** stop attempt-07. Do not repair or release.

## Initial closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: attempt-07 red regression and maker evaluation
user_visible_outcome: every durable journal artifact has one discoverable restart route
repeat_trigger: deterministic evaluator or fresh reviewer result
```

## Maker and deterministic evaluator — PASS — 2026-08-21

The exact attempt-06 failure first reproduced. A failed initial journal write plus failed random
temp cleanup left a hidden file that `recover` could not find.

The journal module now owns two fixed names: `upgrade-transaction.pending` and
`upgrade-transaction.json`. It publishes through the pending file. `status` and `upgrade` stop on
either file. `recover` removes a safe pending file before it uses the final journal. A pending
symlink or nonregular file fails closed.

Deterministic evidence:

- Exact combined write-and-cleanup failure before the change: hidden random temp reproduced.
- Exact regression after the change: fixed pending file discovered and recovered.
- Pending command blocking and symlink rejection: `PASS`.
- Attempt-05 and attempt-06 regressions: `PASS`.
- Focused lifecycle suite: `28 passed`.
- Full public suite: `92 passed`.
- Public validator, canonical/bootstrap bindings, and links: `PASS`.
- Ruff and strict mypy: `PASS`.
- Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Task guard receipt:
  `sha256:c4dd81e021d2c7a1e86bc1d8db1a9bca2068e93e15a37513bffd5384ade5b436`.
- Manager SHA-256:
  `a1b0356dd87bdb469b10243eca25bff87f412f210199bfb0c66c2e0d62706fc6`.
- Lifecycle test SHA-256:
  `24f91dbbaa6a83d53ee0880e7b0bd81320ce64e4ba4c36ce2070415d79bd2719`.

Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

No SECOND LOOK file, real project, Git state, release, tag, announcement, or publication changed.

## Fresh independent review — BLOCK — 2026-08-21

The fresh reviewer completed all `42` lifecycle attacks and all `32` named coverage items. The
fixed pending-journal publication interface passed its write, cleanup, fsync, rename, restart,
symlink, and combined-failure attacks.

The review found a separate terminal state-machine failure. A valid recovery journal can be changed
to `RECOVERED` with complete progress fields. `recover` then selects cleanup without verifying the
installed target bytes. It removes the journal and workspace while mixed managed content remains.

- Verdict: `BLOCK`.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-pending-journal-review-record-007.md`.
- Closeout receipt:
  `sha256:2e9b52759a9431a9f3c89bb20ab69325f7dd37cdba09ed41cb263b35c199b1e0`.
- Recorded BLOCK result:
  `sha256:2df85a3314e3049a71db545427ba4deead9d5c499858ea040480057581ce91d2`.
- Updated ledger digest:
  `sha256:b162857b764223b0ff28815475b20b15f0acfaf181c73368da72b5c43734dfdf`.
- Lifecycle BLOCK count: `7`; architecture reset remains required.

Attempt-07 is closed. No further repair, Git operation, release, real-project upgrade, or SECOND
LOOK synchronization is authorized from this result.
