---
task: "Repair the registered Agent+ 0.2.0 release boundary as one bundled engineering change"
owner_role: "maker"
tier: "2"
time_budget: "90 minutes"
attempt_limit: 2
orchestration_mode: "deep"
exact_model: "Sol controller; one exclusive Luna xhigh maker; deterministic evaluator; one fresh Luna xhigh reviewer"
reasoning: "implementation"
authorization_scope: "Owner authorized the registered Agent+ 0.2.0 boundary and one bundled maker repair"
ownership_map: "Sol owns registration and synthesis; Luna owns repair files; deterministic tools evaluate; fresh Luna reviews; owner owns release"
chain_stages: "registration -> exclusive maker -> deterministic evaluator -> fresh reviewer -> Sol synthesis"
concurrency: "one writer; no overlapping edits; no parallel work after dispatch"
tool_budget: "maker 40 calls or 90 minutes; reviewer 20 calls or 45 minutes"
context_budget: "40K premium ceiling; 12-25K maker and review targets"
reserve_use: "premium engineering reserve authorized for the registered release boundary"
checkpoint_interval: "one bounded wait per sequential stage; stop at maker, evaluator, or reviewer BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this dossier and deterministic command outputs"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "focused unit tests; full unittest suite; public validator; disposable lifecycle attacks; diff check"
fresh_verifier_contract: "review the complete frozen matrices without maker transcript; no repair; one integrated PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-*-task.json; three guard PASS receipts required"
review_closeout: ".agent-plus/agent-plus-0-2-0-*-review.json; three complete closeout receipts required"
---

# Agent+ 0.2.0 release promotion dossier

## Necessity

- **Decision:** repair the three registered engineering failure classes before any Agent+ release.
- **Uncertainty:** whether one constrained repair can close every frozen attack without importing
  proving-project authority or weakening bootstrap safety.
- **Existing evidence:** the 2026-08-21 surplus flock audit reproduced each failure class and
  returned `BLOCK`.
- **Minimum action:** one exclusive maker repairs the complete boundary, deterministic tools
  evaluate it, and one fresh reviewer attacks the complete frozen matrices.
- **Unlock:** one evidence-based owner decision about Agent+ `0.2.0` release readiness.

## Boundary

- **Allowed artifacts:** canonical and bootstrap guards, ledgers, lifecycle scripts, doctor,
  validators, Discovery skills and templates, focused tests, this dossier, task/review packets, hot
  memory, and public state.
- **Allowed actions:** implement the frozen generic repairs with sanitized synthetic tests.
- **Forbidden actions:** edit SECOND LOOK, copy private state, record a real BLOCK before complete
  closeout, run scientific/live work, or perform Git or release actions.
- **Review mode:** engineering sweep.
- **Failure-class coverage:** `review-closeout-enforcement`, `portable-lifecycle-integrity`, and
  `discovery-handoff-durability`.
- **Simplification trigger:** a second BLOCK at any one registered failure class requires an
  architecture reset at `agent-plus/0.2.0-release`.
- **User-visible outcome:** a portable Agent+ control plane that preserves local work and durable
  authority handoffs.
- **Stop condition:** evaluator or fresh reviewer `PASS` or `BLOCK` across the complete matrix.
- **Stop behavior:** collect every frozen engineering attack before one integrated verdict.
- **Attack matrix:** exact ordered items in `.agent-plus/engineering-boundaries.json`.
- **Named coverage:** exact ordered items in `.agent-plus/engineering-boundaries.json`.
- **Promotion dossier:** this file.
- **Dispatch guard:** three planned packets must pass against the canonical registered ledger.
- **Review closeout guard:** three complete review packets must pass
  `--require-complete-engineering-review` before an owner decision.
- **Changed interfaces:** guard CLI and receipt, install manifest, managed-file set, initialization
  transaction, project YAML, Discovery state schema, and Agent+ router handoff.
- **Consumer discovery:** deterministic searches across canonical, bootstrap, lifecycle, skill,
  validator, and test surfaces.
- **Consumer closure:** every discovered canonical and bootstrap consumer receives a disposition.
- **Runtime wrappers:** lifecycle subprocess calls only. No dynamic project adapter is permitted.
- **Real-shape smoke:** disposable init, status, doctor, upgrade, drift, interruption, and Discovery
  resume fixtures.
- **Repeat trigger:** changed implementation evidence or one fresh integrated reviewer finding.
- **Acceptance:** all focused matrices, full public validation, and three review-closeout receipts
  pass.

## Decision branches

- **If PASS:** update this dossier and hot memory, then return to the owner for release authority.
- **If BLOCK or FAIL:** update this dossier with the complete finding matrix and stop. Do not
  auto-repair.

## Registration

- Owner authorization: `Proceed` on 2026-08-21.
- Boundary: `AGENT_PLUS_0_2_0_RELEASE`.
- Reset namespace: `agent-plus/0.2.0-release`.
- Bootstrap authority remains example-only. The canonical release ledger is not copied into new
  projects.
- Dispatch receipts:
  - closeout current: `sha256:873f2a5e05a5bb0f501d604cbdfd907c90f7bcc997d8547ff3effd416ffcf18f`;
  - lifecycle current: `sha256:b4a3abe14d7e4b5ed74aa1be3a651dc3effa2726f6f3d7856d8428bb3171fd60`;
  - discovery current: `sha256:e08252dfb222b108bd73b3048cc6e069f8502db5ebfc78b870214c2da696f975`.
- The pre-maker receipt identifiers are superseded because the repaired receipt schema now binds
  `validation_mode` and `closeout_mode`.
- Registration validation: full public package `64 passed`; bindings and links `PASS`.
- Maker status: `MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`.
- Evaluator status: `PASS`.
- Fresh review status: `BLOCK — portable-lifecycle-integrity`.
- Planned reviewer dispatch receipts:
  - closeout: `sha256:37a603375cd551075a2f7d77d1591221235e31367e100b792cdfe2548bd0eaed`;
  - lifecycle: `sha256:8bcf24337e035039a1a825e1da0a9ea052baf6875fd9cf52337e693171eeae13`;
  - discovery: `sha256:a40dee97284ca372dca669d63622a7aa25dcb7f85a699abcb53f5f39637df187`.

## Maker evidence — 2026-08-21

Status: `MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`

Changed surfaces:

- `scripts/anti_loop_guard.py`
- `bootstrap/base/scripts/anti_loop_guard.py`
- `tests/test_anti_loop_guard.py`
- `scripts/agent_plus_manager.py`
- `scripts/agent-plus-init.sh`
- `scripts/agent-plus-doctor.sh`
- `tests/test_agent_plus_lifecycle.py`
- `skills/agent-plus-discovery-grill/SKILL.md`
- `skills/agent-plus-discovery-grill/assets/PROJECT-DISCOVERY.md`
- `skills/agent-plus/SKILL.md`
- `scripts/validate-public-package.sh`
- `bootstrap/base/tests/test_interface_consumer_guard.py`

Implemented controls:

- `--record-block` now requires a complete engineering review packet and closeout validation.
  Boundary and failure class values come from the validated packet. Receipt identity binds the
  closeout mode. Validation and ledger mutation run under one lock. The result binds the closeout
  receipt.
- Install manifests now require the exact source identity, profile, managed-file set, safe paths,
  and SHA-256 entries. The interface-consumer guard and its synthetic smoke are managed. Init uses
  a staging transaction with rollback, rejects symlinked target control directories, and uses
  JSON-quoted YAML scalars. Doctor validates the managed interface-consumer closure.
- Discovery persists `owner_confirmation` and one bounded handoff task, stop condition, and
  acceptance check. The router requires confirmed durable state before discovery-based contract
  drafting.

Deterministic evidence:

- `./scripts/validate-public-package.sh` — 70 tests passed, canonical/bootstrap guard bindings
  passed, internal links passed, and public-package validation passed.
- `sh -n scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh` — PASS.
- `python3 -m py_compile scripts/anti_loop_guard.py scripts/agent_plus_manager.py` — PASS.
- `git diff --check` — PASS.
- Disposable initialization, status, doctor, path-with-spaces, hostile brain-note, manifest
  tampering, symlink drift, staged-init rollback, and retry checks — PASS.
- Direct caller-controlled BLOCK mutation — rejected. Complete closeout — recorded only with the
  bound closeout receipt in synthetic test state.

Limits and reviewer inputs:

- No real ledger BLOCK was recorded. No review packet was self-certified or closed.
- Fresh review must attack every ordered matrix in `.agent-plus/engineering-boundaries.json`, with
  special attention to closeout TOCTOU and receipt identity, manifest symlink and rollback safety,
  and resumed Discovery routing.
- No Git, release, downstream synchronization, scientific work, live work, or routing experiment
  occurred.

## Fresh integrated review — 2026-08-21

Outcome: `BLOCK`

- `review-closeout-enforcement`: complete declared matrix `PASS`.
- `discovery-handoff-durability`: complete declared matrix and static behavioral contract `PASS`.
- `portable-lifecycle-integrity`: complete declared matrix `PASS`, with one additional adjacent
  upgrade-failure attack returning `BLOCK`.
- `scripts/agent_plus_manager.py` copies managed upgrade files directly. An injected failure after
  the second copy leaves some files updated while the manifest remains old. A retry then refuses
  because the installation has drift.
- Copy failures outside `ManagerError` can escape the typed CLI error boundary.
- Live voice and model behavior remain outside this engineering review.

Complete review closeout receipts before the ledger mutation:

- closeout: `sha256:0ee88a38664892cfa6113041405f5a7a8b9399cc6bc7d712979dc286eb05e42e`;
- lifecycle: `sha256:72ce227e6fd0ebf96f175affeb61d8496279432478df782d71f4a5a184422679`;
- discovery: `sha256:2f796a6bd343dc60f56236473409d4f544e7fd42d1a247753f688a41722c1363`.

The lifecycle `BLOCK` was recorded only after complete closeout:

- result: `sha256:701ceec5a1945e10187cf8039ff524ad0905dc7326017bf4f4afa5b99f2d9523`;
- updated ledger: `sha256:23b41c456636e2ab107bd7b099004acdc433b557c6b44e9ee5e3f71ff307f8a0`;
- `portable-lifecycle-integrity` BLOCK count: `1`;
- architecture reset required: `false`.

No other failure-class BLOCK was recorded. No repair followed this reviewer verdict.

## Required next action after review BLOCK

Expand the registered lifecycle matrix before another dispatch with the complete adjacent failure
class:

- partial upgrade failure;
- upgrade rollback or safe retry;
- typed copy and filesystem failures;
- preservation of the prior manifest and managed-file set until commit.

Then request explicit owner authorization for one bundled lifecycle local repair and one fresh
integrated review. Do not auto-repair from this verdict.

## Transactional-upgrade repair authorization — 2026-08-21

- Owner authorization: `Expand the lifecycle matrix and execute one bundled transactional-upgrade
  repair.`
- Change kind: `local_repair` at lifecycle BLOCK count `1`.
- Expanded attack matrix: `partial-upgrade-failure`, `upgrade-rollback-or-safe-retry`,
  `typed-copy-filesystem-failures`, and `prior-manifest-preservation`.
- Expanded named coverage: `transactional-upgrade`, `typed-manager-errors`, `upgrade-recovery`, and
  `commit-ordering`.
- Task packet: `.agent-plus/agent-plus-0-2-0-lifecycle-task-002.json`.
- Dispatch receipt:
  `sha256:78695d91e2d0e1ed4d8610e8e51fb4db5746560bfa704a7f0688c62e428b847e`.
- Maker status: `MAKER_COMPLETE`.
- Evaluator status: `PASS` after the authorized bounded test-lint correction.
- Fresh review status: `BLOCK — transaction source-side symlink escape`.
- Planned reset-review packet: `.agent-plus/agent-plus-0-2-0-lifecycle-reset-review.json`.
- Planned reset-review receipt:
  `sha256:b68e016df7dc0fe2458351c894e52a8517aa5cb33d2429ed43e099cde64b0e01`.
- Planned lifecycle review packet: `.agent-plus/agent-plus-0-2-0-lifecycle-review-002.json`.
- Planned lifecycle review receipt:
  `sha256:fed871d42c5d449697f8925266e5721189e7ac6bda8b56445ce275d40510514f`.

## Transactional-upgrade maker evidence — 2026-08-21

Status: `MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`

Changed surfaces:

- `scripts/agent_plus_manager.py`
- `tests/test_agent_plus_lifecycle.py`
- this transactional-upgrade maker-evidence subsection

Implemented controls:

- Upgrade copies the complete managed set into private staging before target mutation.
- Staged files and the candidate manifest are validated before commit.
- Prior managed bytes and the prior manifest are copied to a recovery directory before commit.
- Commit uses ordered `os.replace` operations for each managed file and the manifest.
- A commit failure restores committed files from the recovery directory before returning.
- Copy, replace, manifest, and expected filesystem failures return `ManagerError` CLI output.
- A rollback failure returns a high-severity typed error with a durable recovery location.
- Manifest and managed-file symlink paths fail closed before upgrade mutation.

Deterministic evidence:

- Focused lifecycle suite: `13 passed`.
- `./scripts/validate-public-package.sh`: `76 tests passed`, canonical/bootstrap guard bindings
  passed, internal links passed, and public-package validation passed.
- `python3 -m py_compile scripts/agent_plus_manager.py tests/test_agent_plus_lifecycle.py` — PASS.
- `sh -n scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh scripts/agent-plus` — PASS.
- `git diff --check` — PASS.
- Ruff and strict mypy were not installed in the execution environment.

Fresh review inputs:

- Complete registered lifecycle matrix, including first/middle/final staging and commit failures.
- Manifest-write and manifest-replace failures.
- Exact prior managed bytes and manifest identity after every recoverable failure.
- Retry after recoverable failure, typed CLI errors, path spaces, drift refusal, symlink attacks,
  protected state, and unrelated state preservation.
- Rollback failure behavior, including the durable recovery location and retained backups.

- Maker status: `complete`.
- Evaluator status: `BLOCK`.
- Fresh review status: not dispatched.

## Transactional-upgrade evaluator — PASS

Functional and type evidence passed:

- focused lifecycle suite: `13 passed`;
- full public package: `76 passed`;
- public validator, canonical/bootstrap bindings, and links: `PASS`;
- Python compilation and shell syntax: `PASS`;
- strict mypy on `scripts/agent_plus_manager.py`: `PASS`;
- Ruff on `scripts/agent_plus_manager.py` and `tests/test_agent_plus_lifecycle.py`: `PASS`;
- `git diff --check`: `PASS`.

The authorized test-lint correction resolved all 10 reported violations in
`tests/test_agent_plus_lifecycle.py`:

- four `B023` loop-closure binding violations;
- six `SIM117` nested-context violations.

The failure-injection semantics and complete lifecycle matrix remain unchanged. No fresh reviewer
was dispatched. No ledger BLOCK was recorded because the evaluator correction did not produce a
review verdict.

Required next action: dispatch one fresh independent integrated lifecycle review against the
complete registered matrix. Do not release or mutate the ledger before that review.

## Transactional-upgrade fresh integrated review — BLOCK

Outcome: second `BLOCK` at `portable-lifecycle-integrity`.

The expanded declared matrix was completed. The reviewer found one architecture-level recovery
defect:

- rollback restores each backup with `os.replace`;
- a successful restore consumes that backup;
- if a later restore fails, the durable recovery directory no longer contains the complete prior
  managed set;
- the independent scratch attack retained `11/12` recovery assets;
- the typed high-severity error passed, but the recovery evidence was incomplete.

The following controls passed: staging and backup failures, first/middle/final commit failures,
successful rollback, exact-byte restoration, immediate retry, cleanup failures, symlink and
manifest attacks, typed error handling, manifest-last ordering, protected state, full package,
Ruff, strict mypy, compilation, shell syntax, closeout regression, and Discovery regression.

Complete closeout receipt:
`sha256:d0c82b3fe73ea65f10ae9cfc8ca164d8d971afdf06e05b3586634483024dc348`.

Recorded BLOCK result:
`sha256:4f487109dc6114eee0caf7054fe692fa7dc7cd3092b67830981d60f2ae8c331b`.

Updated canonical ledger identity:
`sha256:8bebd2fa4949bbd79890375f7e08c8154cae7c2f6eeeb2a8a16f5ee9491bd8ff`.

- Lifecycle BLOCK count: `2`.
- Architecture reset required: `true`.
- No third local patch is permitted.
- No repair followed this reviewer verdict.

## Required architecture reset

Replace the consumable per-file rollback interface with a constrained durable upgrade state
machine. The replacement must keep one immutable complete recovery snapshot until terminal commit
or verified recovery, use a durable transaction record, and provide one deterministic resume or
recover route. It must remove in-place destructive rollback and consumable recovery assets from
the caller-visible design.

Before dispatch, create a new necessity card, update the ledger-approved reset attempt and removed
caller choices, freeze the architecture-reset matrix, and obtain explicit owner authorization. Do
not implement a third local repair.

## Lifecycle architecture-reset authorization — 2026-08-21

- Owner authorization: `yes`, confirming `Create and execute the registered lifecycle architecture
  reset.`
- Necessity card:
  `.planning/essential-tasks/2026-08-21-agent-plus-lifecycle-architecture-reset.md`.
- Reset packet: `.agent-plus/agent-plus-0-2-0-lifecycle-reset-task.json`.
- Reset namespace: `agent-plus/0.2.0-release`.
- Attempt: `attempt-02`.
- Removed choices: `consumable-recovery-assets`, `implicit-rollback-state`, and
  `in-place-destructive-rollback`.
- Dispatch receipt:
  `sha256:63a87ca671d3d8ee74f02aa9d45d36ec7ff6ecbb101cad6cd06debca0fd27804`.
- Maker status: `MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`.
- Evaluator status: `PASS` after the bounded target-containment correction and complete
  reevaluation.
- Fresh review status: pending registered dispatch.

## Lifecycle architecture-reset maker evidence — 2026-08-21

Status: `MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`

Changed surfaces:

- `scripts/agent_plus_manager.py`
- `scripts/agent-plus`
- `tests/test_agent_plus_lifecycle.py`
- `README.md`
- `docs/architecture.md`
- `docs/bootstrap-a-baseball-project.md`

The lifecycle interface now uses one durable `agent-plus-upgrade-transaction/v1` journal, one
complete hash-verified read-only recovery snapshot, a per-target runtime lock, and one explicit
idempotent `recover --target` route. Upgrade stages and validates the candidate before mutation;
commit progress is journaled; recovery copies snapshot bytes to temporary files before atomic
replacement and never consumes the snapshot. Status and upgrade fail closed while a transaction is
present. Terminal cleanup follows verified `COMMITTED` or `RECOVERED` state; cleanup failure
retains the journal and workspace for recover. Expected filesystem, integrity, symlink, journal,
and concurrency failures are typed, while programmer exceptions are not broadly swallowed.

Deterministic evidence:

- Focused lifecycle suite: `13 passed`.
- Full public package: `76 passed`; canonical/bootstrap bindings and internal links `PASS`.
- Ruff on manager and lifecycle tests: `PASS`.
- Strict mypy on the manager: `PASS`.
- Python compilation, shell syntax, and `git diff --check`: `PASS`.

Limits: no real project upgrade, ledger mutation, Git operation, release, or promotion occurred.
One fresh independent Luna xhigh architecture review remains required against the complete reset
matrix. No release claim is made.

## Lifecycle architecture-reset evaluator — BLOCK — 2026-08-21

- The deterministic suite remained green: `13` focused lifecycle tests, `76` full tests, public
  validation, Ruff, strict mypy, compilation, shell syntax, and `git diff --check` all passed.
- A disposable registered path/symlink attack replaced the target `.planning` directory with a
  symlink to an external directory after a recoverable commit failure.
- `recover` followed that ancestor symlink and replaced the external
  `templates/ESSENTIAL-TASK.md` sentinel with immutable snapshot bytes.
- Recovery returned a typed failure only during terminal verification, after the out-of-target
  mutation had already occurred.
- Root cause: `_copy_to_atomic_restore` checks a relative path from `destination.parent.parent`, so
  it does not inspect the starting ancestor itself for nested managed paths.
- Evaluator verdict: `BLOCK` on the registered transaction/path-symlink matrix item.
- No fresh review packet was created or dispatched. No ledger BLOCK, release, Git operation, or
  real project upgrade occurred.
- Required next action: revise the reset architecture so every recovery destination is proven to
  remain beneath the resolved target with every ancestor checked immediately before replacement;
  then rerun the complete evaluator matrix before fresh review.

## Lifecycle architecture-reset maker correction — target containment — 2026-08-21

Status: `MAKER_CORRECTION_COMPLETE — COMPLETE REEVALUATION REQUIRED`

The correction introduces one target-root-aware `_target_destination` invariant shared by commit and
recovery. It requires the exact lexical `target / relative` destination, checks every ancestor from
target through the final component for symlinks at the last responsible moment, and confirms the
resolved destination remains beneath the resolved target. Resolution is used only as an assertion;
the write remains on the lexical expected path and never uses an external resolved path.

The lifecycle tests now include the exact swapped `.planning` ancestor attack for recovery and a
corresponding commit-path swap. Both reject before replacement, preserve external sentinel bytes,
and leave a durable transaction that can be repaired after the local path is restored.

Deterministic reevaluation:

- Focused lifecycle suite: `15 passed`.
- Full public package: `78 passed`; public validation, canonical/bootstrap bindings, and links
  `PASS`.
- Ruff, strict mypy, Python compilation, shell syntax, and `git diff --check`: `PASS`.

This correction is maker/evaluator evidence only. No fresh reviewer, ledger mutation, Git operation,
real project upgrade, release, or promotion occurred. Complete independent reevaluation remains
required.

## Lifecycle architecture-reset complete reevaluation — PASS — 2026-08-21

- Focused lifecycle suite: `15 passed`.
- Full public package: `78 passed`; validator, canonical/bootstrap bindings, and links `PASS`.
- Ruff, strict mypy, Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Independent disposable recovery attack: swapped `.planning` ancestor rejected before replacement,
  external sentinel unchanged, durable journal retained.
- Independent disposable commit attack: swapped `.planning` ancestor rejected before replacement,
  external sentinel unchanged, durable journal retained.
- Reset task packet remains valid with receipt
  `sha256:63a87ca671d3d8ee74f02aa9d45d36ec7ff6ecbb101cad6cd06debca0fd27804`.
- Evaluator verdict: `PASS`; one fresh complete architecture review is now required.

## Lifecycle architecture-reset fresh review — BLOCK — 2026-08-21

- Planned receipt validated:
  `sha256:b68e016df7dc0fe2458351c894e52a8517aa5cb33d2429ed43e099cde64b0e01`.
- All `29` required attack-matrix items and `21` named-coverage items were completed in canonical
  ledger order.
- Target-side swapped `.planning` attacks passed for both commit and recovery; external sentinels
  remained unchanged.
- BLOCK finding 1: swapping the transaction `snapshot` ancestor to an external symlink before
  snapshot copy redirected `shutil.copy2` outside the target. Validation detected the problem only
  after the external sentinel changed.
- BLOCK finding 2: swapping staged source `.agent-plus` to an external directory before commit let
  `os.replace` move external content into the managed target and consume the external sentinel.
- Matrix result: `transaction-path-symlink` BLOCK.
- Named coverage result: `transactional-upgrade` and `upgrade-recovery` BLOCK; every other declared
  item passed.
- Focused lifecycle suite: `15 passed`; full public package: `78 passed`; Ruff, strict mypy,
  compilation, shell syntax, guard regressions, public validator, closeout regressions, and
  Discovery regression passed.
- Complete-review closeout receipt:
  `sha256:4f104e6a2733286dacdbdeebd5acf55b66c88ef87c57ac3cc34937e676598fb5`.
- Recorded BLOCK result:
  `sha256:01b44a7754e6f2ed6326db2fbb3f9a9d16a397594c44a20d1cde8bf3c6984fbe`.
- Updated canonical ledger digest:
  `sha256:bed1b895c85fc52a795995afbbc0d8c3dd7a1572a41b44e8868cc552730b1105`.
- Lifecycle BLOCK count: `3`; architecture reset remains required.
- No further repair, Git operation, real upgrade, release, promotion, or downstream synchronization
  followed the reviewer verdict.

## Closeout

## Transaction-workspace replacement authorization — 2026-08-21

- Owner authorization: `Authorize a new necessity card and replacement transaction-workspace
  architecture for Agent+ 0.2.0. Keep release blocked. Use Luna maker and independent reviewer
  gates.`
- Necessity card:
  `.planning/essential-tasks/2026-08-21-agent-plus-transaction-workspace-architecture.md`.
- Task packet: `.agent-plus/agent-plus-0-2-0-workspace-task-003.json`.
- Attempt: `attempt-03`.
- Removed choices: `path-following-transaction-io`, `post-write-transaction-validation`, and
  `rename-consuming-staged-source`.
- Release status: `BLOCKED` throughout this chain.
- Dispatch receipt:
  `sha256:330d8389d0ee716347cadf2d9814f60d1ea27e42788c7b809a22d90c70e29347`.
- Maker: `MAKER_COMPLETE — COMPLETE DETERMINISTIC EVALUATION REQUIRED`.
- Evaluator: `BLOCK`.
- Separate reviewer: not dispatched.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: owner decision to hold 0.2.0 or authorize a new transaction-workspace architecture
user_visible_outcome: blocked because transaction source paths can escape through swapped symlinks
repeat_trigger: new necessity card and explicit owner authorization for a replacement interface
```

## Transaction-workspace replacement maker evidence — attempt-03 — 2026-08-21

Status: `MAKER_COMPLETE — COMPLETE DETERMINISTIC EVALUATION REQUIRED`.

The manager now uses one closed `TransactionFilesystem` boundary for target, canonical source,
`.agent-plus`, lock, journal, transaction workspace, snapshot, stage, restart reopen, and every
destination parent. Directory components and regular files are opened descriptor-relatively with
`O_NOFOLLOW`; source hashes are computed from the exact opened descriptors used for copying.
Snapshot and stage writes are fsynced temporary-file copies. Commit and recover copy into a
temporary file and atomically rename only within the already-open destination directory handle.
Recovery sources remain immutable and present. Journal state and recovery digests are durable,
typed expected failures remain fail-closed, and programmer exceptions are not broadly swallowed.
Workspace cleanup preflights all entries to retain recovery assets on symlink or cleanup failure.

New disposable lifecycle coverage exercises target, snapshot, stage, and transaction ancestor
swaps; source-handle replacement during copy; restart reopen; external sentinels; source asset
non-consumption; partial restore/resume; crash detection; concurrency; cleanup; corruption; and
programmer-error boundaries.

Evidence:

- Focused lifecycle: `19 passed`.
- Full public suite: `82 passed`.
- `bash scripts/validate-public-package.sh`: `PASS` (82 tests, canonical/bootstrap bindings and
  links).
- Attempt-03 guard: `PASS`, receipt
  `sha256:330d8389d0ee716347cadf2d9814f60d1ea27e42788c7b809a22d90c70e29347`.
- Ruff, strict mypy, compilation, shell syntax, and `git diff --check`: `PASS`.

This section is maker evidence only and does not claim evaluator/reviewer PASS, promotion, or
release. No ledger, review packet, Git, real project, or release state was changed. The complete
deterministic evaluator and separate independent reviewer remain required; release remains blocked.

## Transaction-workspace replacement evaluator — BLOCK — attempt-03

- Descriptor-anchored source and destination attacks passed, including the two prior reviewer
  external-sentinel escapes.
- Required lifecycle regression: the managed set dropped
  `scripts/interface_consumer_guard.py` and `tests/test_interface_consumer_guard.py`; status did not
  detect a replaced installed interface guard.
- Required journal regression: a corrupted recovery subset was accepted, recovery returned
  success, removed its journal, and left omitted candidate bytes installed.
- Required concurrency regression: a replaced live lock was deleted by the prior holder because
  lock ownership was not revalidated before unlink.
- Standard gates remained green: `19` focused tests, `82` full tests, public validator, Ruff,
  strict mypy, compilation, shell syntax, and diff check.
- Evaluator verdict: `BLOCK`; attempt-03 stops before independent review.
- No review packet, ledger mutation, Git operation, real upgrade, release, promotion, or downstream
  synchronization occurred.

## Clean-room Agent+ system update — attempt-04 — deterministic PASS

- Owner authorized the full Agent+ update, including the portable output contract and replacement
  lifecycle state and lock interfaces.
- Registered task receipt:
  `sha256:e40f01591ee56b5d86994e79791c0cb36392d14403a190b910435791e5a223c6`.
- The generated-project template now carries the basic everyday-language output contract across
  Codex, Claude, and Cursor. The external `i-have-adhd` skill or plugin is optional.
- Transaction journal v2 requires exact release-owned managed, recovery, candidate, commit, and
  progress sets. Complete recovery inputs are checked before target mutation.
- The lock is a kernel-owned lease. Release never unlinks the shared lock path, so a replacement
  owner remains intact.
- Direct tests reproduce and close all three attempt-03 findings.
- Focused lifecycle: `23 passed`. Full public suite: `87 passed`.
- Public validator, canonical/bootstrap bindings, links, Ruff, strict mypy, compilation, shell
  syntax, and diff check: `PASS`.
- Planned fresh-review receipt:
  `sha256:5c377ca184a6b06241d0c82de463fea2d8ddee099ed614d4f1f0eb0f645cf9d1`.
- Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.
- No reviewer, Git operation, release, announcement, real upgrade, or SECOND LOOK synchronization
  followed.

## Clean-room Agent+ system update — attempt-04 fresh review BLOCK

- Fresh independent Luna xhigh review completed the exact registered matrices: `39` lifecycle
  attacks and `29` named coverage items.
- The three attempt-03 regressions were covered. The `87` public tests, validator, compilation,
  shell syntax, and diff checks passed.
- Adjacent BLOCK: an injected durable journal-write failure during snapshot progress left a
  `SNAPSHOTTING` journal with `snapshot_complete: false` and missing recovery digests. Running
  `recover` then raised raw `KeyError: '.agent-plus/PROFILE.md'`.
- This violates the typed-manager-error, durable-transaction-record, and
  transaction-state-machine controls.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-clean-room-review-record.md`.
- Complete closeout receipt:
  `sha256:c52086932d1d4abc7ae6ca2f805e7c83e46f5f6081ea4377e50e79fdb53faaa0`.
- Recorded BLOCK result:
  `sha256:2a2c60d23299e76c7eb4174b0c14ee0dfe0117f49e3ecca69221b94e1ad6c410`.
- Canonical ledger digest:
  `sha256:20302450a22a76a0210b4822ca79911525ac01cf8cbe60106aaa763c1feb5bff`.
- Lifecycle BLOCK count: `4`; architecture reset remains required.

Attempt-04 is closed. Release `0.2.0` remains blocked. No repair, Git operation, release,
announcement, real-project upgrade, or SECOND LOOK synchronization followed. The next step is an
owner decision to hold this worktree or authorize a new necessity and architecture decision for
the incomplete-snapshot journal boundary.

## Incomplete-journal recovery reset — attempt-05 deterministic PASS

- Owner authorized a new architecture attempt for the attempt-04 journal BLOCK.
- Registered task receipt:
  `sha256:6fd7bb05e1b5eb3e162f9d99b8f4790eacdb566d487518e157c07a76186d5292`.
- The exact reviewer attack first reproduced raw `KeyError: '.agent-plus/PROFILE.md'`.
- The lifecycle restart module now selects safe abort for an incomplete precommit snapshot.
- Safe abort removes the transaction workspace and journal without target-file writes.
- Journal states after snapshotting require a complete snapshot.
- Focused lifecycle suite: `24 passed`. Full public suite: `88 passed`.
- Public validator, Ruff, strict mypy, compilation, shell syntax, and diff check: `PASS`.
- Manager SHA-256:
  `a41151fb319f9568175f471393f07028628257e6bf22ab689dcf770f41a2d863`.
- Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

Release and SECOND LOOK synchronization remain blocked until one fresh independent review returns
`PASS`. No Git operation, release, real upgrade, or downstream edit followed.

## Terminal recovery authentication reset — attempt-08 fresh review PASS

- The accepted architecture requires exact installed recovery bytes and manifest to authenticate
  against durable recovery digests before cleanup.
- The complete unattended evaluator passed all `12` gates.
- The fresh reviewer passed all `42` lifecycle attacks and `32` named coverage items.
- Related review-closeout and discovery matrices passed, for `59/59` attacks and `46/46` named
  coverage items in total.
- The exact attempt-07 forged `RECOVERED` journal attack retained recovery state and later restored
  exact prior bytes.
- Complete closeout receipt:
  `sha256:331cc2b02681c81acaba8aee90b9c84042dc823b0ca80f582700b15007cef038`.
- Review record:
  `.planning/essential-tasks/2026-08-22-agent-plus-terminal-recovery-review-record-008.md`.

Status: `AGENT_PLUS_TERMINAL_RECOVERY_AUTHENTICATION_REVIEW_ACCEPTED — OWNER RELEASE DECISION REQUIRED`.

No Git operation, release, publication, real-project upgrade, downstream synchronization, or
SECOND LOOK change occurred. The next action is the explicit owner release decision.

## Agent+ sync integrated review — PASS

- Sync boundary: `16/16` attacks and `15/15` named coverage items `PASS`.
- Editorial re-review: `12/12` attacks and `11/11` named coverage items `PASS`.
- Lifecycle re-review: `42/42` attacks and `32/32` named coverage items `PASS`.
- Complete release-candidate evaluator: `15/15 PASS`.
- Sync closeout receipt:
  `sha256:e405c507689d44a2180d483b1650dc0ab67f6faa6e91d54ab3e02036cccf1c41`.
- Refreshed editorial receipt:
  `sha256:04791785ecd6f8790c5644d95fb444b4620a143d95f10245d3454d1e2e5dc210`.
- Refreshed terminal-recovery receipt:
  `sha256:33e4abc3c876e6f2e1b4e7f405040b52df6f1dac9e2e476b32ff713355142e8f`.
- Review record:
  `.planning/essential-tasks/2026-08-22-agent-plus-sync-integrated-review-record.md`.

Status: `AGENT_PLUS_0_2_0_RELEASE_CANDIDATE_ACCEPTED — OWNER RELEASE DECISION REQUIRED`.

No staging, commit, tag, push, publication, consumer upgrade, or SECOND LOOK synchronization
occurred.

## Exact release-scope preflight — PASS

- Temporary Git index only. The real index remained unchanged.
- Approved public release files: `134`.
- File-name manifest SHA-256:
  `7e5677eeb925dc119120b2aabdf19dfb2612661a88dff0c71419db2d1020fbf1`.
- Generated outputs, local project configuration, ledger lock, editor metadata, and the macOS
  artifact are excluded.
- Temporary staged diff, full 99-test public validator, bindings, links, and worktree diff checks:
  `PASS`.
- Remote `main` equals local base commit `47bce5928a578914165ae47cdeb2d4279df4debe`.
- No `v0.2.0` or `0.2.0` tag exists.

Status: `AGENT_PLUS_0_2_0_RELEASE_READY — EXPLICIT RELEASE AUTHORIZATION REQUIRED`.

## Pending-journal publication reset — attempt-07 fresh review BLOCK

- The fresh reviewer completed `42` lifecycle attacks and `32` named coverage items.
- Fixed pending-journal publication passed all required attacks.
- The attempt-06 hidden random temp failure is closed.
- Adjacent BLOCK: a valid-looking `RECOVERED` journal selects terminal cleanup without target-byte
  verification.
- Recovery removes the journal and workspace while mixed managed bytes remain.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-pending-journal-review-record-007.md`.
- Complete closeout receipt:
  `sha256:2e9b52759a9431a9f3c89bb20ab69325f7dd37cdba09ed41cb263b35c199b1e0`.
- Recorded BLOCK result:
  `sha256:2df85a3314e3049a71db545427ba4deead9d5c499858ea040480057581ce91d2`.
- Updated ledger digest:
  `sha256:b162857b764223b0ff28815475b20b15f0acfaf181c73368da72b5c43734dfdf`.
- Lifecycle BLOCK count: `7`; architecture reset remains required.

Attempt-07 is closed. Release `0.2.0` remains blocked. No further repair, Git operation, release,
real-project upgrade, or SECOND LOOK synchronization followed. The next step is an owner decision
to hold this worktree or authorize terminal recovery verification as a new architecture attempt.

## Atomic transaction setup reset — attempt-06 fresh review BLOCK

- The fresh reviewer completed `41` lifecycle attacks and `31` named coverage items.
- The attempt-05 orphan-workspace failure is closed.
- Initial journal failure leaves no workspace.
- Workspace failure after journal publication keeps a safe abort route.
- Adjacent BLOCK: combined initial journal-write failure and temporary-file cleanup failure leaves
  `.agent-plus/.upgrade-transaction.json.<id>.tmp`.
- No final journal exists, so `recover` cannot discover or remove this file.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-atomic-setup-review-record-006.md`.
- Complete closeout receipt:
  `sha256:63d7c9d447717b4ae3813eebf1f37951494a005ff8ef03f4950c61498037d2ac`.
- Recorded BLOCK result:
  `sha256:faa8285bceb56d0e8c071af01df8c2b1d28d7c3674004ebe3f1e3774d3cea961`.
- Updated ledger digest:
  `sha256:419e359f0a3f687bd14691bcb7949bb84b78c083a6b4d4dd6de945763b625574`.
- Lifecycle BLOCK count: `6`; architecture reset remains required.

Attempt-06 is closed. Release `0.2.0` remains blocked. No further repair, Git operation, release,
real-project upgrade, or SECOND LOOK synchronization followed. The next step is an owner decision
to hold this worktree or replace the temporary JSON writer interface.

## Pending-journal publication reset — attempt-07 deterministic PASS

- Owner authorized a replacement interface for the attempt-06 hidden-temp BLOCK.
- Registered task receipt:
  `sha256:c4dd81e021d2c7a1e86bc1d8db1a9bca2068e93e15a37513bffd5384ade5b436`.
- The exact combined write-and-cleanup attack reproduced before implementation.
- Journal publication now uses fixed pending and final names.
- `status`, `upgrade`, and `recover` recognize pending state.
- Pending symlinks and nonregular files fail closed.
- Focused lifecycle suite: `28 passed`. Full public suite: `92 passed`.
- Public validator, Ruff, strict mypy, compilation, shell syntax, and diff check: `PASS`.
- Manager SHA-256:
  `a1b0356dd87bdb469b10243eca25bff87f412f210199bfb0c66c2e0d62706fc6`.
- Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

Release and SECOND LOOK synchronization remain blocked until one fresh independent review returns
`PASS`. No Git operation, release, real upgrade, or downstream edit followed.

## Incomplete-journal recovery reset — attempt-05 fresh review BLOCK

- The fresh reviewer completed `40` lifecycle attacks and `30` named coverage items.
- The attempt-04 raw `KeyError` failure is closed.
- All failures after the initial journal write recovered safely.
- Adjacent BLOCK: failure during the first durable journal write leaves an orphan transaction
  workspace and no journal.
- `recover` cannot discover or remove that workspace.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-incomplete-journal-review-record-005.md`.
- Complete closeout receipt:
  `sha256:6c0a69f685e6242844803fe12808e5eefe74f47c04f091352b6c43a32a95353d`.
- Recorded BLOCK result:
  `sha256:f460a32dea4c204bda7336787485bbf174d7b6b4a1cb04cb7b641c6b4f58afce`.
- Updated ledger digest:
  `sha256:dc6118c554d38d34be521c253ba5a321348b19c519b4f428e945c85a3270cc97`.
- Lifecycle BLOCK count: `5`; architecture reset remains required.

Attempt-05 is closed. Release `0.2.0` remains blocked. No further repair, Git operation, release,
real-project upgrade, or SECOND LOOK synchronization followed. The next step is an owner decision
to hold the worktree or authorize a new atomic transaction-setup architecture.

## Atomic transaction setup reset — attempt-06 deterministic PASS

- Owner authorized a new architecture attempt for the attempt-05 setup BLOCK.
- Registered task receipt:
  `sha256:cf904e98ffe6840a7d411fdc3d410fe7cdfde9cb944846cf4f2f31a06f18aaca`.
- The exact first-journal-write attack reproduced the orphan workspace before implementation.
- Durable transaction intent now exists before workspace creation.
- Initial journal failure leaves no workspace.
- Workspace creation failure leaves a discoverable journal and safe abort route.
- Focused lifecycle suite: `26 passed`. Full public suite: `90 passed`.
- Public validator, Ruff, strict mypy, compilation, shell syntax, and diff check: `PASS`.
- Manager SHA-256:
  `1b34c4ca3c039a6946f9cfa55993dc347e9c8addb12058d5de3476b607891ce7`.
- Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

Release and SECOND LOOK synchronization remain blocked until one fresh independent review returns
`PASS`. No Git operation, release, real upgrade, or downstream edit followed.
