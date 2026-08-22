# Agent+ 0.2.0 atomic transaction setup review 006

## Result

Verdict: `BLOCK`.

The review packet is complete. Its lifecycle attack and named-coverage arrays match the ledger in
exact order. The closeout guard returned `PASS`.

The lifecycle boundary has one adjacent setup failure. If the initial transaction journal write
fails and cleanup of its temporary file also fails, the temporary file remains in `.agent-plus`.
The journal is absent, so `recover` reports no pending transaction and cannot remove the file.
This violates the requirement that failed setup leave no untracked durable transaction state.

## Scope and evidence

The review used the dirty working tree as the source of truth. It used disposable project roots and
did not edit implementation, tests, the ledger, SECOND LOOK, or Git state.

Commands and results:

```text
python3 -m unittest discover -s tests -p 'test_agent_plus_lifecycle.py'
26 tests passed

./scripts/validate-public-package.sh
90 tests passed
Canonical/bootstrap guard bindings: PASS
Internal Markdown links: PASS
Public package validation: PASS

python3 -m py_compile scripts/agent_plus_manager.py scripts/anti_loop_guard.py scripts/interface_consumer_guard.py
sh -n scripts/agent-plus scripts/agent-plus-init.sh scripts/agent-plus-doctor.sh
git diff --check
PASS

python3 scripts/anti_loop_guard.py --ledger .agent-plus/engineering-boundaries.json --packet .agent-plus/agent-plus-0-2-0-atomic-setup-review-006.json --require-complete-engineering-review
PASS
receipt: sha256:63d7c9d447717b4ae3813eebf1f37951494a005ff8ef03f4950c61498037d2ac
```

Reviewer-owned disposable attacks passed for:

- initial journal write, temporary-file fsync, rename, and directory fsync failures;
- no journal, no workspace, and exact installed bytes after those failures;
- workspace creation failure after durable intent;
- partial workspace creation and pre-snapshot completion failure;
- snapshot, stage, commit, terminal-commit, and recovery journal failures;
- safe abort with missing, replaced, symlinked, and foreign transaction workspaces;
- the complete earlier lifecycle attack set through the fresh lifecycle suite and validator.

Ruff and strict mypy were not installed in the review environment. Live voice, model behavior,
real project upgrades, release, publication, and scientific work were outside this boundary.

## Ordered matrix result

### review-closeout-enforcement

Result: `PASS`. All `7` attack items and all `6` named-coverage items completed in ledger order.

### portable-lifecycle-integrity

Result: `BLOCK`. All `41` attack items and all `31` named-coverage items completed in ledger order.

The registered `initial-journal-write-failure` item passed when temporary cleanup succeeded. The
adjacent cleanup failure below returned `BLOCK`.

### discovery-handoff-durability

Result: `PASS`. All `10` attack items and all `8` named-coverage items completed in ledger order.

## Blocking finding

The failure is reachable through the initial journal setup path:

1. Initialize a disposable project.
2. Start `upgrade`.
3. Inject an `os.write` failure for the initial journal temporary file.
4. Inject an `os.unlink` failure for that temporary file during the `finally` cleanup.
5. Run `recover`.

Observed result:

```text
upgrade: ManagerError: Cannot remove temporary JSON upgrade-transaction.json: cleanup unavailable
journal: absent
transaction workspace: absent
recover: Agent+ recovery: no pending transaction
retained: .agent-plus/.upgrade-transaction.json.<id>.tmp
```

The target managed bytes remain unchanged. The retained temporary file is durable transaction
state without a journal or recovery route.

The relevant path creates the temporary file at `scripts/agent_plus_manager.py:506`,
reports cleanup failure at line `534`, publishes the first journal at line `1010`, and returns
without cleanup when no journal exists at line `1037`.

## Limits and next action

No repair was designed or applied. No ledger BLOCK was recorded. No release or downstream
synchronization is authorized.

The next action is one bounded maker repair for initial journal temporary-file cleanup and one new
owner-authorized fresh review. Preserve this BLOCK and do not release Agent+ `0.2.0`.
