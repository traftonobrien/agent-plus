---
task: "Replace pathname transaction I/O with a descriptor-anchored workspace architecture"
owner_role: "maker"
tier: "2"
time_budget: "120 minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Sol controller; one exclusive Luna xhigh maker; deterministic evaluator; one separate Luna xhigh reviewer"
reasoning: "premium"
authorization_scope: "Owner explicitly authorized a new necessity card and replacement transaction-workspace architecture while keeping release blocked"
ownership_map: "Sol owns registration/evaluation/synthesis; Luna maker owns replacement; separate Luna reviewer is read-only; owner owns any release decision"
chain_stages: "registered attempt-03 -> exclusive maker -> deterministic evaluator -> separate reviewer -> Sol closeout"
concurrency: "one writer; no overlapping maker or reviewer edits"
tool_budget: "maker 50 calls or 120 minutes; reviewer 25 calls or 60 minutes"
context_budget: "50K premium ceiling; 15-30K maker and reviewer targets"
reserve_use: "premium architecture reserve explicitly authorized"
checkpoint_interval: "one bounded wait per sequential stage; stop at evaluator or reviewer BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "descriptor-anchored disposable transaction fixtures and this card"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "complete lifecycle suite; source/destination swap races; full validator; Ruff; strict mypy; compilation; shell syntax; diff check"
fresh_verifier_contract: "separate Luna reviewer; complete registered matrix; read-only; one integrated PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-workspace-task-003.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-workspace-review-003.json"
---

# Agent+ transaction-workspace architecture replacement

## Necessity

- **Decision:** replace pathname-based transaction source and workspace I/O after the accepted
  `attempt-02` architecture review found external-write and external-source-consumption escapes.
- **Uncertainty:** whether a restart-safe descriptor-anchored filesystem boundary can make every
  snapshot, stage, journal, commit, and recovery operation non-following and race-resistant.
- **Existing evidence:** target-side lexical containment passed, but a snapshot destination ancestor
  swap redirected `shutil.copy2`, and a staged-source ancestor swap redirected `os.replace`.
- **Minimum action:** introduce one closed transaction filesystem abstraction that opens each
  directory component without following symlinks, anchors operations to directory handles, copies
  from verified regular-file handles, and atomically replaces only within an already-open target
  parent handle.
- **Unlock:** a fresh independent decision on whether Agent+ `0.2.0` lifecycle integrity is ready;
  release remains separately blocked.

## Boundary

- **Allowed artifacts:** lifecycle manager and wrapper, lifecycle tests, directly affected public
  lifecycle documentation, this card, the promotion dossier, and registered attempt-03 packets.
- **Forbidden actions:** another pathname-check patch, edits to SECOND LOOK or global skills, real
  project upgrades, Git, release, promotion, announcement, or downstream synchronization.
- **Changed interface:** all transaction workspace I/O, including snapshot, stage, journal,
  lock/restart reopen, commit source, recovery source, and atomic target replacement.
- **Removed choices:** `path-following-transaction-io`, `post-write-transaction-validation`, and
  `rename-consuming-staged-source`.
- **Required architecture:** open the resolved target once; securely traverse transaction-relative
  paths with non-following directory opens; use verified regular-file descriptors as copy sources;
  write to temporary files in stable destination directory handles; fsync; rename within the same
  destination handle; never rename a staged source into the target.
- **Restart rule:** `recover` must reopen the exact lexical workspace with the same non-following
  traversal and fail closed before mutation if any component changed type or identity.
- **Platform rule:** if required descriptor-relative/non-following primitives are unavailable, fail
  typed before transaction mutation; do not silently fall back to pathname I/O.
- **Review mode:** complete engineering sweep of the exact ledger-ordered matrix and coverage.
- **Stop condition:** deterministic evaluator or separate reviewer `PASS` or `BLOCK`.
- **Acceptance:** no external sentinel mutation or consumption under snapshot, stage, journal,
  target, or concurrent ancestor swaps; immutable recovery and restart behavior remain intact; all
  standard gates pass.

## Decision branches

- **If evaluator PASS:** register and dispatch one separate Luna reviewer. PASS does not release.
- **If evaluator BLOCK:** stop and record evidence; no local repair under attempt-03.
- **If reviewer PASS:** close the review packet and return to the owner for a separate release
  decision while release remains blocked.
- **If reviewer BLOCK:** close and record the BLOCK; stop without repair or release.

## Registration evidence

- Attempt-03 task packet guard: `PASS`.
- Dispatch receipt:
  `sha256:330d8389d0ee716347cadf2d9814f60d1ea27e42788c7b809a22d90c70e29347`.
- Registration baseline: `78` public tests plus canonical/bootstrap bindings and links `PASS`.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: attempt-03 guard validation and exclusive Luna maker dispatch
user_visible_outcome: release remains blocked pending replacement architecture evidence
repeat_trigger: complete evaluator or separate reviewer result
```

## Maker evidence — attempt-03 — 2026-08-21

Status: `MAKER_COMPLETE — COMPLETE DETERMINISTIC EVALUATION REQUIRED`

- Replaced pathname transaction I/O with `TransactionFilesystem`, which opens the resolved target
  and canonical source roots once and keeps descriptor-relative, `O_NOFOLLOW` directory and regular
  file handles for the complete command lifetime.
- Journal, lock, transaction workspace, snapshot, stage, restart reopen, destination parents, and
  source files use the same non-following descriptor boundary. Unsupported platforms fail typed
  before transaction mutation; there is no pathname fallback.
- Snapshot and stage assets are copied through opened regular-file descriptors into fsynced
  temporary files. Candidate and recovery commits use copy-to-temp plus `os.rename` within a stable
  destination directory handle; staged and snapshot source assets are never consumed.
- Journal recovery digests verify every snapshot path, type, and hash before restoration. Cleanup
  preflights the complete workspace so a symlink or cleanup failure cannot destroy the remaining
  durable recovery assets.
- Added deterministic disposable tests for snapshot-ancestor swap, staged-source ancestor swap,
  source-handle swap during copy, transaction-directory restart reopen, external sentinel
  nonmutation, immutable source assets, target ancestor swaps, partial restore, and idempotent
  recovery.

Evidence:

- Focused lifecycle suite: `19 passed`.
- Full public suite and validator: `82 passed`; canonical/bootstrap bindings and internal links
  `PASS`.
- Attempt-03 packet guard: `PASS`, receipt
  `sha256:330d8389d0ee716347cadf2d9814f60d1ea27e42788c7b809a22d90c70e29347`.
- Ruff, strict mypy, Python compilation, shell syntax, and `git diff --check`: `PASS`.

Limits: this is maker evidence only. No ledger mutation, review packet creation, Git operation,
real project upgrade, release, promotion, or downstream synchronization occurred. Complete
deterministic independent evaluation and the separate reviewer gate remain required; release stays
blocked.

## Deterministic evaluator — BLOCK — 2026-08-21

Standard evidence remained green:

- Focused lifecycle suite: `19 passed`.
- Full public suite and validator: `82 passed`; canonical/bootstrap bindings and links `PASS`.
- Ruff, strict mypy, Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Descriptor attacks for snapshot/stage ancestor swaps, opened-source replacement, restart reopen,
  and external sentinel preservation passed.

Complete registered-matrix findings:

1. **Managed interface coverage regressed.** `_managed_sources` omits
   `scripts/interface_consumer_guard.py` and `tests/test_interface_consumer_guard.py`. A disposable
   initialized target's manifest omitted both; replacing the installed guard with a no-op still
   returned `AGENT_PLUS_CURRENT` from `status`.
2. **Journal corruption is accepted.** `_validate_journal` checks types and safe strings but does
   not require exact canonical managed, recovery, digest, or progress sets. In a disposable
   different-candidate commit failure, removing one committed file from `recovery_files` and
   `recovery_digests` let `recover` return `0`, delete the journal, and leave candidate bytes in the
   supposedly recovered installation.
3. **Lock ownership is not preserved.** Replacing `upgrade.lock` while a command held the lock
   caused the original holder's `finally` block to unlink the replacement owner's lock without
   detecting an inode/token change.

Evaluator verdict: `BLOCK` on `managed-interface-guard`, `journal-corruption`,
`concurrent-upgrade-recover`, `exact-managed-set`, `interface-guard-lifecycle`,
`upgrade-transaction-schema`, `transaction-state-machine`, and `concurrency-lock`.

Stop: attempt-03 permits one architecture implementation and requires stopping at evaluator BLOCK.
No local correction, review packet, independent reviewer, ledger mutation, Git operation, real
upgrade, release, promotion, or downstream synchronization followed.

## Final closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: owner decision to hold 0.2.0 after attempt-03 evaluator BLOCK
user_visible_outcome: descriptor escapes closed but lifecycle exactness and concurrency regressed
repeat_trigger: new explicit owner authorization after a revised necessity decision
```
