# Agent+ 0.2.0 clean-room review 004

## Result

Verdict: `BLOCK`.

The review packet is complete. Its attack and named-coverage arrays match the ledger in exact
order. The closeout guard returned `PASS`. The release remains blocked by one adjacent lifecycle
failure in durable journal recovery.

## Scope

This was a fresh, read-only engineering review of the Agent+ 0.2.0 attempt-04 worktree.

The review covered:

- the canonical lifecycle manager and shell lifecycle commands;
- the managed output policy and interface-consumer guard;
- disposable initialization, upgrade, failure, recovery, lock, and symlink cases;
- the anti-loop closeout guard and its canonical/bootstrap examples;
- the Agent+ discovery skill, router, template, and bootstrap controls.

No network, private data, scientific work, real project, Git, release, or ledger mutation was used.

## Independent checks

The following checks ran from the current worktree:

```text
scripts/ai-context.sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
./scripts/validate-public-package.sh
python3 -m py_compile scripts/agent_plus_manager.py scripts/anti_loop_guard.py scripts/interface_consumer_guard.py
sh -n scripts/agent-plus scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh
git diff --check
python3 scripts/anti_loop_guard.py --ledger .agent-plus/engineering-boundaries.json --packet .agent-plus/agent-plus-0-2-0-clean-room-review-004.json --require-complete-engineering-review
```

Results:

- `87` public tests passed.
- Public validation, canonical/bootstrap bindings, and internal links passed.
- Python compilation, shell syntax, and diff checks passed.
- The completed review closeout returned `PASS` with receipt
  `sha256:c52086932d1d4abc7ae6ca2f805e7c83e46f5f6081ea4377e50e79fdb53faaa0`.

Reviewer-owned disposable attacks also passed for:

- install, status, doctor, upgrade, and validation of the output policy, Cursor rule,
  interface-consumer guard, and guard test;
- missing managed files, changed managed bytes, exact manifest sets, profile values, quoted
  project YAML, brain-note values, paths with spaces, protected project state, and retry;
- first, middle, and final commit failures with exact-byte recovery and prior-manifest retention;
- partial restore failure, immutable snapshot retention, idempotent recovery, cleanup failure,
  interrupted upgrade recovery, and typed low-level filesystem errors;
- incomplete, corrupted, reduced, and traversal journal inputs before target writes;
- snapshot, stage-source, transaction-directory, target-ancestor, and opened-source symlink swaps;
- external sentinel preservation and non-consumption of source and recovery assets;
- a live kernel lock, a replacement lock path, and release of the original owner;
- direct BLOCK mutation without a closeout packet, closeout receipt identity, matrix drift,
  canonical/bootstrap example separation, and temporary-ledger closeout recording;
- discovery single-file state, owner confirmation resume gates, typed exits, unknown answers,
  privacy limits, contract-ready bypass prevention, and one bounded evidence/prototype handoff.

## Ordered matrix result

The three registered matrices were completed in ledger order.

### review-closeout-enforcement

Result: `PASS`.

Ordered attack matrix:

```text
direct-record-block-requires-closeout
receipt-attests-closeout-mode
registered-dispatch-boundary
canonical-bootstrap-ledger-separation
complete-matrix-exactness
unknown-reordered-drifted-matrix
no-real-ledger-mutation-before-closeout
```

Ordered named coverage:

```text
anti-loop-cli
receipt-schema
canonical-release-ledger
bootstrap-example-ledger
dispatch-packets
public-validator
```

### portable-lifecycle-integrity

Result: `BLOCK`.

The review completed all `39` registered attack items and all `29` registered named-coverage
items. The exact packet arrays are the authoritative ordered record. The integrated result is
`BLOCK` because of the adjacent failure below.

The registered attack order is:

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
exact-recovery-set, replacement-lock-owner-preservation
```

The registered named-coverage order is:

```text
manifest-schema, exact-managed-set, source-identity, profile-enum, interface-guard-lifecycle,
atomic-initialization, project-yaml, lifecycle-tests, doctor, transactional-upgrade,
typed-manager-errors, upgrade-recovery, commit-ordering, upgrade-transaction-schema,
immutable-recovery-snapshot, recover-command, transaction-state-machine, crash-restart-route,
recovery-integrity-verifier, concurrency-lock, lifecycle-cli, descriptor-anchored-transaction-io,
non-following-source-open, copy-based-candidate-commit, restart-safe-workspace-reopen,
source-containment-verifier, output-policy, exact-transaction-journal, lease-owned-lock
```

### discovery-handoff-durability

Result: `PASS`.

Ordered attack matrix:

```text
awaiting-confirmation-resume, confirmed-ready-resume, evidence-task-persistence,
prototype-task-persistence, single-file-state, unknown-answer, scope-split, privacy-omission,
contract-ready-bypass, typed-exits
```

Ordered named coverage:

```text
discovery-schema, owner-confirmation, bounded-handoff, resume-routing, agent-plus-router,
bootstrap-template, lifecycle-tests, public-validator
```

## Blocking finding

The following reviewer-owned attack found a reachable defect outside the frozen list but inside the
same lifecycle boundary:

1. Initialize a disposable project.
2. Allow the first transaction-journal write.
3. Inject a durable journal-write failure on the next journal write during snapshot progress.
4. Observe that `upgrade` returns a typed `ManagerError` but leaves the on-disk journal in
   `SNAPSHOTTING` with `snapshot_complete: false` and an empty `recovery_digests` map.
5. Run `recover` on the same root.

Observed result:

```text
upgrade: ManagerError: review injected durable journal write failure
journal state: SNAPSHOTTING
snapshot_complete: false
recovery_digests: {}
recover: KeyError: '.agent-plus/PROFILE.md'
```

`recover` indexes a missing recovery digest before it converts the state to a typed manager
failure. The lifecycle CLI catches `ManagerError`, not this raw `KeyError`. The result violates
the typed-manager-error, durable-transaction-record, and transaction-state-machine controls.

This finding is a review `BLOCK`. No repair was designed or applied.

## Limits and next action

Live voice and model behavior were outside this engineering boundary. No real project upgrade or
release decision was made. The canonical ledger was not changed by this review.

The next action is one bounded repair or architecture decision for the journal-write failure, then
a new owner-authorized deterministic evaluation and fresh independent review. Do not release or
synchronize downstream projects from this result.
