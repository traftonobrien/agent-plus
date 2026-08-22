# Agent+ 0.2.0 terminal recovery authentication review 008

## Result

Verdict: PASS.

The fresh independent review completed the registered engineering sweep. Terminal recovery
cleanup now requires the installed recovery set and manifest to match the durable recovery
digests. A valid-looking RECOVERED journal cannot remove recovery state while managed bytes are
mixed.

This PASS does not authorize release, publication, or downstream synchronization.

The reviewer did not request or use the maker transcript. The reviewer used the registered task,
ledger, implementation, tests, evaluator terminal evidence, evaluator log, and reviewer-owned
disposable evidence.

## Scope and evidence

The review used the current dirty working tree. It did not edit implementation, tests, the ledger,
state truth, promotion records, editorial records, Git state, or SECOND LOOK.

Reviewer-owned evidence:

- outputs/attempt-08-reviewer/deterministic-run.log
- outputs/attempt-08-reviewer/deterministic-run.exit with value 0
- outputs/attempt-08-reviewer/forged-recovery.log
- outputs/attempt-08-reviewer/forged-recovery.exit with value 0

Registered evaluator evidence:

- outputs/attempt-08-evaluator-run-2/terminal.json reports PASS, 12 completed steps, and no
  failed step.
- outputs/attempt-08-evaluator-run-2/evaluator.log contains the complete evaluator receipts.

Expected implementation hashes matched:

~~~text
7002578537b0d030acfc11c221c8fd1c097571d3770ce787a9b6e3ab337c35e5  scripts/agent_plus_manager.py
2d23c3fb6aac3a91a1120d8069c6465f547fbb0013db98be4a67aef47cc1f220  tests/test_agent_plus_lifecycle.py
~~~

## Deterministic results

The reviewer ran one bounded deterministic sweep. The result was PASS.

~~~text
python3 -m unittest discover -s tests -p 'test_agent_plus_lifecycle.py'
29 tests passed

bash scripts/validate-public-package.sh
99 tests passed
Canonical/bootstrap guard bindings: PASS
Internal Markdown links: PASS
Public package validation: PASS

python3 -m unittest discover -s tests -p 'test_anti_loop_guard.py'
53 tests passed

python3 -m py_compile scripts/agent_plus_manager.py scripts/anti_loop_guard.py \
  scripts/interface_consumer_guard.py tests/test_agent_plus_lifecycle.py
PASS

sh -n scripts/agent-plus scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh \
  scripts/validate-public-package.sh
PASS

git diff --check -- scripts/agent_plus_manager.py tests/test_agent_plus_lifecycle.py
PASS
~~~

The reviewer ran the complete-review guard:

~~~text
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-0-2-0-terminal-recovery-review-008.json \
  --require-complete-engineering-review
~~~

The guard returned PASS with this closeout receipt:

~~~text
sha256:331cc2b02681c81acaba8aee90b9c84042dc823b0ca80f582700b15007cef038
~~~

The complete-review guard receipt reports closeout_mode=true, review_status=complete,
block_count=7, and validation_mode=engineering_review_closeout.

## Blocking boundary attack

The reviewer independently reproduced the attempt-07 attack in a disposable project.

1. The reviewer induced a commit failure after one managed-file commit.
2. The reviewer confirmed a durable RECOVERY_REQUIRED journal and recovery workspace.
3. The reviewer changed one managed file to reviewer-controlled mixed bytes.
4. The reviewer changed only valid journal fields to state=RECOVERED, complete
   restored_files, and an empty last_error.
5. recover rejected terminal cleanup because the installed recovery set did not match the
   durable recovery digests.
6. The journal changed to RECOVERY_REQUIRED, the journal and workspace remained, and mixed bytes
   remained installed.
7. A later recover restored the complete snapshot and removed the journal only after exact-byte
   verification.

The reviewer-owned log records:

~~~text
forged RECOVERED rejected: Recovered target verification failed: .agent-plus/PROFILE.md; retry recover --target
forged RECOVERED terminal cleanup attack: PASS
retained state: RECOVERY_REQUIRED
recovery restored exact prior bytes: PASS
~~~

Adjacent valid-journal, snapshot, manifest, exact-set, descriptor and path-swap, cleanup-failure,
restart, recovery-asset, source-containment, journal-publication, and lease-lock routes passed in
the lifecycle and anti-loop suites. The reviewer checked the changed route at
scripts/agent_plus_manager.py:1022-1030 and scripts/agent_plus_manager.py:1132-1140.

## Ordered matrix result

All items below completed in ledger order with result PASS.

### portable-lifecycle-integrity

Attack matrix: 42/42 PASS.

~~~text
empty-managed-files
missing-managed-entry
false-source-repository
invalid-profile
managed-interface-guard
partial-init-failure
init-retry-or-rollback
brain-note-yaml
protected-state-preservation
path-with-spaces
normal-upgrade
partial-upgrade-failure
upgrade-rollback-or-safe-retry
typed-copy-filesystem-failures
prior-manifest-preservation
immutable-recovery-snapshot
durable-transaction-record
recovery-assets-never-consumed
recovery-after-partial-restore-failure
recover-command-idempotence
interrupted-upgrade-detection
terminal-commit-cleanup
terminal-recovery-cleanup
transaction-path-symlink
journal-corruption
recovery-snapshot-corruption
concurrent-upgrade-recover
cleanup-failure-retains-state
programmer-error-boundary
snapshot-ancestor-swap-before-copy
stage-source-ancestor-swap-before-commit
source-swap-during-open-copy
directory-handle-restart-reopen
external-sentinel-nonmutation
transaction-source-assets-not-consumed
non-following-directory-traversal
output-policy-lifecycle
exact-recovery-set
replacement-lock-owner-preservation
incomplete-snapshot-journal-recovery
initial-journal-write-failure
journal-pending-cleanup-failure
~~~

Named coverage: 32/32 PASS.

~~~text
manifest-schema
exact-managed-set
source-identity
profile-enum
interface-guard-lifecycle
atomic-initialization
project-yaml
lifecycle-tests
doctor
transactional-upgrade
typed-manager-errors
upgrade-recovery
commit-ordering
upgrade-transaction-schema
immutable-recovery-snapshot
recover-command
transaction-state-machine
crash-restart-route
recovery-integrity-verifier
concurrency-lock
lifecycle-cli
descriptor-anchored-transaction-io
non-following-source-open
copy-based-candidate-commit
restart-safe-workspace-reopen
source-containment-verifier
output-policy
exact-transaction-journal
lease-owned-lock
precommit-journal-abort
intent-before-workspace
discoverable-journal-publication
~~~

### review-closeout-enforcement

Attack matrix: 7/7 PASS.

~~~text
direct-record-block-requires-closeout
receipt-attests-closeout-mode
registered-dispatch-boundary
canonical-bootstrap-ledger-separation
complete-matrix-exactness
unknown-reordered-drifted-matrix
no-real-ledger-mutation-before-closeout
~~~

Named coverage: 6/6 PASS.

~~~text
anti-loop-cli
receipt-schema
canonical-release-ledger
bootstrap-example-ledger
dispatch-packets
public-validator
~~~

### discovery-handoff-durability

Attack matrix: 10/10 PASS.

~~~text
awaiting-confirmation-resume
confirmed-ready-resume
evidence-task-persistence
prototype-task-persistence
single-file-state
unknown-answer
scope-split
privacy-omission
contract-ready-bypass
typed-exits
~~~

Named coverage: 8/8 PASS.

~~~text
discovery-schema
owner-confirmation
bounded-handoff
resume-routing
agent-plus-router
bootstrap-template
lifecycle-tests
public-validator
~~~

Combined related-boundary totals are 59/59 attacks and 46/46 named-coverage items.

## Conclusion and limits

No blocking defect was found. The terminal recovery cleanup boundary is authenticated against the
durable recovery digests, and the attempt-07 forged terminal state cannot discard the recovery
route while installed bytes remain mixed.

No repair, release, publication, Git operation, real project upgrade, downstream synchronization,
scientific work, modeling, or SECOND LOOK work occurred.

The owner must make the separate release decision. Agent+ 0.2.0 remains unreleased until that
decision is explicit.
