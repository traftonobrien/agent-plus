# Agent+ 0.2.0 incomplete-journal review 005

## Result

Verdict: `BLOCK`.

The review packet is complete. Its lifecycle attack and named-coverage arrays match the ledger in
exact order. The closeout guard returned `PASS`.

The release remains blocked by one adjacent lifecycle failure. A failure during the initial durable
journal write leaves an orphan transaction workspace with no journal. The recovery command cannot
discover or remove that workspace.

## Scope

This was a fresh, read-only engineering review of the Agent+ 0.2.0 attempt-05 worktree.

The review covered:

- the lifecycle manager and shell lifecycle commands;
- the managed output policy and interface-consumer guard;
- disposable initialization, upgrade, failure, recovery, lock, and symlink cases;
- journal state validation and restart actions;
- the anti-loop closeout guard and its canonical/bootstrap examples;
- the Agent+ discovery skill, router, template, and bootstrap controls.

No network, private data, scientific work, real project, Git, release, or ledger mutation was used.
Only this review packet and this review record were reviewer-owned outputs.

## Independent checks

The following checks ran from the current dirty worktree:

```text
scripts/ai-context.sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
./scripts/validate-public-package.sh
python3 -m py_compile scripts/agent_plus_manager.py scripts/anti_loop_guard.py scripts/interface_consumer_guard.py
sh -n scripts/agent-plus scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh
git diff --check
python3 scripts/anti_loop_guard.py --ledger .agent-plus/engineering-boundaries.json --packet .agent-plus/agent-plus-0-2-0-incomplete-journal-review-005.json --require-complete-engineering-review
```

Results:

- `88` public tests passed.
- Public validation, canonical/bootstrap bindings, and internal links passed.
- Python compilation, shell syntax, and diff checks passed.
- The completed review closeout returned `PASS` with receipt
  `sha256:6c0a69f685e6242844803fe12808e5eefe74f47c04f091352b6c43a32a95353d`.

Reviewer-owned disposable attacks passed for:

- the exact managed output set, output-policy drift, protected project state, path spaces, and
  quoted project YAML;
- false source identity, invalid profile, and reduced managed-file manifests;
- first, middle, and terminal commit failures with exact-byte recovery and idempotent recovery;
- immutable recovery assets after partial restore failure;
- real filesystem rename failures with typed manager errors;
- incomplete, corrupted, reduced, and traversal journal inputs before target writes;
- target and transaction-workspace ancestor swaps with external sentinel preservation;
- opened-source descriptor stability after a source-path swap;
- lock ownership, concurrent command denial, and terminal cleanup retention;
- durable journal failures at snapshot transition, stage transition, ready/commit transition,
  commit progress, terminal commit, recovery progress, and terminal recovery;
- valid incomplete precommit recovery, which safely aborts without target writes, raw exceptions,
  retained journal, or transaction workspace, and supports an idempotent second recovery.

## Journal-write attack results

The post-initial journal-write stages were safe under one-shot and persistent failure injection.
Each failure returned a typed `ManagerError`, retained enough durable state for restart, preserved
the prior managed bytes, and completed recovery without a journal or transaction workspace.

The required incomplete-snapshot case was reproduced independently. A persistent failure after the
initial journal left:

```text
state: SNAPSHOTTING
snapshot_complete: false
recovery_digests: {}
```

`recover` selected the safe abort action. It did not write target files, raise a raw exception, or
leave the journal or transaction workspace. A second recovery reported no pending transaction.

The initial durable journal write is a separate failure boundary. A low-level `os.write` failure
while writing `upgrade-transaction.json` returned a typed manager error, preserved the installation,
and left this state:

```text
journal: absent
transaction workspace: present
recovery route: none
```

`recover` reported no pending transaction and left the orphan workspace. This violates atomic
transaction setup and leaves durable lifecycle state that the restart command cannot clean.

## Ordered matrix result

All three registered failure-class matrices were completed in ledger order. The lifecycle matrix
returned `BLOCK` because of the initial-journal finding. The other two matrices returned `PASS`.

### review-closeout-enforcement

Result: `PASS`. `7` attack items and `6` named-coverage items completed.

```text
direct-record-block-requires-closeout
receipt-attests-closeout-mode
registered-dispatch-boundary
canonical-bootstrap-ledger-separation
complete-matrix-exactness
unknown-reordered-drifted-matrix
no-real-ledger-mutation-before-closeout
```

```text
anti-loop-cli
receipt-schema
canonical-release-ledger
bootstrap-example-ledger
dispatch-packets
public-validator
```

### portable-lifecycle-integrity

Result: `BLOCK`. All `40` attack items and all `30` named-coverage items completed.

```text
empty-managed-files, missing-managed-entry, false-source-repository, invalid-profile,
managed-interface-guard, partial-init-failure, init-retry-or-rollback, brain-note-yaml,
protected-state-preservation, path-with-spaces, normal-upgrade, partial-upgrade-failure,
upgrade-rollback-or-safe-retry, typed-copy-filesystem-failures, prior-manifest-preservation,
immutable-recovery-snapshot, durable-transaction-record, recovery-assets-never-consumed,
recovery-after-partial-restore-failure, recover-command-idempotence, interrupted-upgrade-detection,
terminal-commit-cleanup, terminal-recovery-cleanup, transaction-path-symlink, journal-corruption,
recovery-snapshot-corruption, concurrent-upgrade-recover, cleanup-failure-retains-state,
programmer-error-boundary, snapshot-ancestor-swap-before-copy,
stage-source-ancestor-swap-before-commit, source-swap-during-open-copy,
directory-handle-restart-reopen, external-sentinel-nonmutation,
transaction-source-assets-not-consumed, non-following-directory-traversal, output-policy-lifecycle,
exact-recovery-set, replacement-lock-owner-preservation, incomplete-snapshot-journal-recovery
```

```text
manifest-schema, exact-managed-set, source-identity, profile-enum, interface-guard-lifecycle,
atomic-initialization, project-yaml, lifecycle-tests, doctor, transactional-upgrade,
typed-manager-errors, upgrade-recovery, commit-ordering, upgrade-transaction-schema,
immutable-recovery-snapshot, recover-command, transaction-state-machine, crash-restart-route,
recovery-integrity-verifier, concurrency-lock, lifecycle-cli, descriptor-anchored-transaction-io,
non-following-source-open, copy-based-candidate-commit, restart-safe-workspace-reopen,
source-containment-verifier, output-policy, exact-transaction-journal, lease-owned-lock,
precommit-journal-abort
```

### discovery-handoff-durability

Result: `PASS`. `10` attack items and `8` named-coverage items completed.

```text
awaiting-confirmation-resume, confirmed-ready-resume, evidence-task-persistence,
prototype-task-persistence, single-file-state, unknown-answer, scope-split, privacy-omission,
contract-ready-bypass, typed-exits
```

```text
discovery-schema, owner-confirmation, bounded-handoff, resume-routing, agent-plus-router,
bootstrap-template, lifecycle-tests, public-validator
```

## Blocking finding

The following reviewer-owned attack found a reachable defect inside the lifecycle boundary:

1. Initialize a disposable project.
2. Start `upgrade`.
3. Inject a low-level durable write failure while creating the initial
   `.agent-plus/upgrade-transaction.json`.
4. Observe a typed manager error.
5. Inspect the target.

Observed result:

```text
upgrade: ManagerError: Cannot write upgrade-transaction.json: disk full
journal: absent
transaction workspace: present
recover: Agent+ recovery: no pending transaction
transaction workspace after recover: present
```

The workspace is created before the initial journal write. The failure exits before the guarded
upgrade body can select `ABORTED` or clean the workspace. The recovery command requires a journal,
so it cannot remove the orphan transaction. A later upgrade can create another transaction beside
the orphan.

This is a lifecycle `BLOCK`. No repair was designed or applied.

## Limits and next action

Live voice and model behavior were outside this engineering boundary. No real project upgrade or
release decision was made. The canonical ledger was not changed by this review.

The next action is one bounded architecture repair for initial journal creation and cleanup,
followed by a new owner-authorized deterministic evaluation and fresh independent review. Do not
release or synchronize downstream projects from this result.
