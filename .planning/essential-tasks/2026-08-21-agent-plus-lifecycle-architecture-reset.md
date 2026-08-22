---
task: "Replace Agent+ upgrade rollback with a durable recovery state machine"
owner_role: "maker"
tier: "2"
time_budget: "90 minutes"
attempt_limit: 2
orchestration_mode: "deep"
exact_model: "Sol controller; one exclusive Luna xhigh architecture maker; deterministic evaluator; one fresh Luna xhigh reviewer"
reasoning: "premium"
authorization_scope: "Owner authorized the registered lifecycle architecture reset after two review BLOCKs"
ownership_map: "Sol owns reset registration and synthesis; Luna owns architecture implementation; deterministic tools evaluate; fresh Luna reviews; owner owns release"
chain_stages: "registered reset -> exclusive architecture maker -> deterministic evaluator -> fresh reviewer -> Sol synthesis"
concurrency: "one writer; lifecycle transaction lock required at runtime; no parallel maker edits"
tool_budget: "maker 40 calls or 90 minutes; reviewer 20 calls or 45 minutes"
context_budget: "40K premium ceiling; 12-25K maker and reviewer targets"
reserve_use: "premium hard-architecture reserve authorized"
checkpoint_interval: "one bounded wait per stage; stop at maker, evaluator, or reviewer BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "transaction journal and immutable recovery snapshot in disposable tests; this necessity card"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "expanded lifecycle suite; full package; Ruff; strict mypy; compilation; shell syntax; diff check"
fresh_verifier_contract: "independent complete architecture-reset matrix; no maker transcript; no repair"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-lifecycle-reset-task.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-lifecycle-reset-review.json"
---

# Agent+ lifecycle architecture reset

## Necessity

- **Decision:** replace the upgrade recovery interface after two BLOCKs at
  `portable-lifecycle-integrity`.
- **Uncertainty:** whether one closed state machine can keep complete recovery assets across every
  commit, restore, cleanup, interruption, and restart failure.
- **Existing evidence:** the first review found mixed managed files after a copy failure. The
  second review found that partial rollback consumes recovery assets.
- **Minimum action:** replace implicit destructive rollback with one durable transaction journal,
  one immutable complete recovery snapshot, and one deterministic idempotent recover command.
- **Unlock:** safe Agent+ upgrades that can complete or recover after process and filesystem
  failures without manual artifact reconstruction.

## Boundary

- **Allowed artifacts:** `scripts/agent_plus_manager.py`, `scripts/agent-plus`, lifecycle tests,
  lifecycle documentation, this card, the stable promotion dossier, and registered reset packets.
- **Allowed actions:** replace the lifecycle upgrade/recovery architecture and add sanitized
  synthetic crash and recovery tests.
- **Forbidden actions:** third local rollback patch, destructive use of project-owned paths, edits
  to SECOND LOOK or global installed skills, real project upgrade, Git, release, scientific/live
  work, or unrelated Agent+ changes.
- **Review mode:** engineering sweep.
- **Failure-class coverage:** complete registered `portable-lifecycle-integrity` matrix plus
  closeout and Discovery regression checks.
- **Simplification trigger:** any design that consumes recovery artifacts or permits multiple
  ambiguous recovery routes must be replaced before review.
- **User-visible outcome:** one upgrade command that either completes or leaves one complete,
  verifiable, recoverable transaction.
- **Stop condition:** deterministic evaluator or fresh reviewer `PASS` or `BLOCK`.
- **Stop behavior:** collect every registered architecture-reset attack.
- **Attack matrix:** exact ordered lifecycle items in the canonical ledger.
- **Named coverage:** exact ordered lifecycle items in the canonical ledger.
- **Promotion dossier:** `.planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md`.
- **Dispatch guard:** registered architecture-reset packet at BLOCK count `2`.
- **Review closeout guard:** one complete architecture-reset review packet and closeout receipt.
- **Changed interfaces:** upgrade transaction schema, recovery snapshot, journal, lock, CLI recover
  route, terminal cleanup, and manager error contract.
- **Consumer discovery:** manager, wrapper CLI, doctor/status/upgrade/recover, docs, tests, and public
  validator.
- **Consumer closure:** every discovered consumer receives a deterministic test or no-change
  disposition.
- **Runtime wrappers:** subprocess CLI only. No dynamic project adapter.
- **Real-shape smoke:** disposable init, interrupted upgrade, status, recover, retry, doctor, and
  protected-state preservation.
- **Repeat trigger:** changed implementation evidence or one fresh reviewer finding.
- **Acceptance:** full registered reset matrix, public package, Ruff, strict mypy, compilation,
  shell syntax, and diff check pass.

## Removed caller choices

- `consumable-recovery-assets`;
- `implicit-rollback-state`;
- `in-place-destructive-rollback`.

The only recovery route is the durable transaction record plus the idempotent `recover` command.

## Decision branches

- **If PASS:** request one fresh independent architecture review. PASS does not release Agent+.
- **If BLOCK:** stop and update the stable dossier. Do not add another local rollback patch.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: bounded target-containment revision and complete deterministic reevaluation
user_visible_outcome: blocked because recovery can mutate an external symlink destination
repeat_trigger: changed implementation evidence closing the swapped-ancestor attack
```

## Maker evidence — 2026-08-21

Status: `MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`

Changed surfaces:

- `scripts/agent_plus_manager.py`
- `scripts/agent-plus`
- `tests/test_agent_plus_lifecycle.py`
- `README.md`
- `docs/architecture.md`
- `docs/bootstrap-a-baseball-project.md`
- this maker-evidence subsection

Implemented architecture:

- Upgrade creates one closed-schema `agent-plus-upgrade-transaction/v1` journal and an immutable,
  hash-verified snapshot of every managed file plus the prior manifest before target mutation.
- Journal writes use temporary-file replacement, file flush/fsync, and directory fsync; journal
  state records snapshot, staging, commit, restore, and terminal progress.
- A fixed per-target lock serializes upgrade and recover. Stale locks are cleared only by the
  explicit recover route after process-death detection.
- `status` and `upgrade` fail closed on any durable transaction and point to
  `recover --target <path>`.
- Commit failures retain the transaction. Recovery verifies every journal path and snapshot hash,
  restores through copy-to-temp plus atomic replace, never consumes snapshot assets, and can resume
  after a partial restore failure.
- Verified `COMMITTED` and `RECOVERED` states are cleaned only after terminal verification. Cleanup
  failures retain the terminal journal and workspace for a subsequent recover cleanup.
- Symlink/path attacks, journal corruption, snapshot corruption, expected filesystem errors, and
  programmer exceptions have separate fail-closed behavior; project-owned state is not included in
  the managed or recovery sets.

Deterministic evidence:

- Focused lifecycle suite: `13 passed`, including first/middle/last commit failures, staging and
  snapshot failures, killed-process restart recovery, partial restore and resume, repeated recover,
  journal/snapshot corruption, symlink attacks, lock contention, cleanup failure, protected state,
  and programmer-error boundary.
- `./scripts/validate-public-package.sh`: `76 tests passed`, canonical/bootstrap guard bindings,
  internal links, and public-package validation `PASS`.
- `uvx --from ruff ruff check scripts/agent_plus_manager.py tests/test_agent_plus_lifecycle.py` —
  `PASS`.
- `uvx --from mypy mypy --strict scripts/agent_plus_manager.py` — `PASS`.
- `python3 -m py_compile scripts/agent_plus_manager.py tests/test_agent_plus_lifecycle.py` —
  `PASS`.
- `sh -n scripts/agent-plus scripts/*.sh bootstrap/base/scripts/*.sh` — `PASS`.
- `git diff --check` — `PASS`.

Limits and handoff:

- No real project upgrade, Git operation, release, ledger mutation, or promotion occurred.
- Deterministic evaluation subsequently returned `BLOCK`; fresh review was not dispatched.

## Deterministic evaluator — BLOCK

- Standard gates passed: `13` focused lifecycle tests, `76` full tests, public validation, Ruff,
  strict mypy, compilation, shell syntax, and diff check.
- Disposable attack: after a recoverable commit failure, replace target `.planning` with a symlink
  to an external directory, then invoke `recover`.
- Observed result: recovery overwrote the external `templates/ESSENTIAL-TASK.md` sentinel with
  snapshot bytes, then returned a typed terminal-verification failure.
- Failure class: registered transaction/path-symlink coverage.
- Root cause: the destination guard begins below the target for nested paths and therefore omits
  the first ancestor from its symlink walk.
- Stop: no fresh reviewer, review packet closeout, ledger mutation, Git operation, or release.
- Restart: make target-root containment and full ancestor validation an invariant immediately
  before every atomic commit/restore replacement, add the exact regression, and rerun the complete
  reset evaluator.

## Maker correction — target containment — 2026-08-21

Status: `MAKER_CORRECTION_COMPLETE — COMPLETE REEVALUATION REQUIRED`

The evaluator defect is addressed with one shared `_target_destination` invariant. It validates the
exact lexical `target / relative` destination, checks every ancestor from target through the final
path component for symlinks immediately before replacement, and verifies the resolved destination
remains beneath the resolved target. The resolved path is used only for containment checking; both
commit and recovery continue to write to the lexical expected destination.

Changed surfaces:

- `scripts/agent_plus_manager.py`
- `tests/test_agent_plus_lifecycle.py`
- this correction subsection

New regressions prove that swapping target `.planning` to an external directory is rejected before
both recovery and commit replacement, preserves the external sentinel bytes, and leaves the
transaction durably recoverable. Existing immutable snapshot, journal, lock, typed failure, and
project-state tests remain active.

Deterministic reevaluation evidence:

- Focused lifecycle suite: `15 passed`.
- Full public package: `78 passed`; public validation, canonical/bootstrap bindings, and links
  `PASS`.
- Ruff, strict mypy, Python compilation, shell syntax, and `git diff --check`: `PASS`.

No fresh review, ledger mutation, Git operation, real project upgrade, release, or promotion
occurred. A complete independent reevaluation remains required.

## Complete deterministic reevaluation — PASS

- `15` focused lifecycle tests and `78` full tests passed.
- Public validation, Ruff, strict mypy, compilation, shell syntax, and diff check passed.
- Independent disposable recovery and commit attacks both rejected a swapped `.planning` ancestor
  before replacement, preserved external sentinel bytes, and retained the durable journal.
- Evaluator verdict: `PASS`.
- Next gate: one fresh independent Luna xhigh review of the exact complete registered matrix.

## Fresh architecture review — BLOCK

- The reviewer completed all `29` required attacks and `21` named coverage items.
- `transaction-path-symlink` BLOCK: snapshot-copy source ancestry can be redirected to an external
  directory before post-copy validation, and staged commit sources can be swapped to external
  content before `os.replace`.
- Target-side containment correction passed its recovery and commit attacks.
- Closeout receipt:
  `sha256:4f104e6a2733286dacdbdeebd5acf55b66c88ef87c57ac3cc34937e676598fb5`.
- BLOCK result:
  `sha256:01b44a7754e6f2ed6326db2fbb3f9a9d16a397594c44a20d1cde8bf3c6984fbe`.
- Lifecycle BLOCK count: `3`; architecture reset remains required.
- Stop: no further repair or release action is permitted under this attempt.
