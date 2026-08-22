# Agent+ 0.2.0 pending-journal publication review 007

## Result

Verdict: `BLOCK`.

The review packet is complete. Its lifecycle attack and named-coverage arrays match the ledger in
exact order. The complete-review guard returned `PASS`.

The fixed pending-journal publication controls passed. A separate valid-journal state-machine
attack returned `BLOCK`. `recover` trusts a structurally valid `RECOVERED` state and removes the
journal and workspace without verifying the target installation.

## Scope and evidence

The review used the current dirty working tree and reviewer-owned disposable project roots. It did
not edit implementation, tests, the ledger, SECOND LOOK, or Git state.

Commands and results:

```text
python3 -m unittest discover -s tests -p 'test_agent_plus_lifecycle.py'
28 tests passed

bash scripts/validate-public-package.sh
92 tests passed
Canonical/bootstrap guard bindings: PASS
Internal Markdown links: PASS
Public package validation: PASS

python3 -m unittest discover -s tests -p 'test_anti_loop_guard.py'
53 tests passed

python3 -m py_compile scripts/agent_plus_manager.py scripts/anti_loop_guard.py scripts/interface_consumer_guard.py tests/test_agent_plus_lifecycle.py
sh -n scripts/agent-plus scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh scripts/validate-public-package.sh
git diff --check
PASS

python3 scripts/anti_loop_guard.py --ledger .agent-plus/engineering-boundaries.json --packet .agent-plus/agent-plus-0-2-0-pending-journal-review-007.json --require-complete-engineering-review
PASS
receipt: sha256:2e9b52759a9431a9f3c89bb20ab69325f7dd37cdba09ed41cb263b35c199b1e0

reviewer-owned publication and restart probes
PASS for fixed publication, write failure, journal-file fsync failure, rename failure,
directory-fsync failure, combined initial-write and pending-cleanup failure, pending-only,
final-only, final-plus-pending, malformed pending entries, non-regular pending entries,
replacement-safe cleanup, and copy destination inspection, fsync, rename, and cleanup failures.
```

Ruff and strict mypy were not installed in the review environment. No live voice, model behavior,
real project upgrade, release, publication, or scientific work was in scope.

## Ordered matrix result

### review-closeout-enforcement

Result: `PASS`. All `7` attack items and all `6` named-coverage items completed in ledger order.

The anti-loop test suite and the complete-review guard covered direct BLOCK recording, receipt
binding, registered dispatch, exact matrix matching, and closeout-only ledger mutation.

### portable-lifecycle-integrity

Result: `BLOCK`. All `42` attack items and all `32` named-coverage items completed in ledger order.

The fixed pending-journal publication and restart route passed. The valid-journal state-machine
attack below is decisive.

### discovery-handoff-durability

Result: `PASS`. All `10` attack items and all `8` named-coverage items completed in ledger order.

The discovery template, skill, router, lifecycle regression, validator, and bootstrap surfaces
preserved one durable discovery file, owner confirmation, typed exits, and one bounded handoff.

## Blocking finding

The failure is reachable through the valid final-journal recovery path:

1. Initialize a disposable project.
2. Inject a commit failure after the first managed-file commit.
3. Confirm that the durable journal is `RECOVERY_REQUIRED` and the target has a recoverable
   transaction workspace.
4. Replace one committed managed file with reviewer-controlled mixed bytes.
5. Change only the valid journal fields `state` to `RECOVERED`, `restored_files` to the complete
   recovery set, and `last_error` to an empty string.
6. Run `recover`.

Observed result:

```text
recover: Agent+ recovery: restored prior installation
journal: removed
transaction workspace: removed
mixed managed file: retained
```

The edited journal passes `_validate_journal`. `_restart_action` maps `RECOVERED` to `cleanup`, and
`recover` performs terminal cleanup without `_preflight_recovery_sources` or target digest
verification. This permits a valid-looking terminal record to discard the only recovery route
while the target remains mixed.

Relevant implementation locations are `scripts/agent_plus_manager.py:771-847`,
`scripts/agent_plus_manager.py:858-868`, and `scripts/agent_plus_manager.py:1116-1153`.

This violates the transaction state-machine and recovery-integrity requirements. It blocks the
portable lifecycle boundary even though the pending-journal publication itself passed.

## Limits and next action

No repair was designed or applied. No ledger BLOCK was recorded by this reviewer. No release or
downstream synchronization is authorized.

The next action is one bounded architecture-level repair for terminal recovery-state validation,
followed by a new owner-authorized fresh review. Preserve this `BLOCK` and do not release Agent+
`0.2.0`.
