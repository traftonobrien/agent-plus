# Agent+ surplus-capacity flock audit record

Outcome: `BLOCK`

Date: `2026-08-21`

## Scope

Sol dispatched four independent Luna xhigh workers for read-only review of:

- engineering review closeout, bounded-recovery defaults, and interface-consumer closure;
- the portable Agent+ lifecycle in disposable projects;
- Discovery Grill behavior and project-start integration;
- SECOND LOOK synchronization metadata and routing-measurement readiness.

No worker edited Agent+, SECOND LOOK, protected evidence, or a real ledger. No scientific or live
work, Git operation, release, or promotion occurred. Sol compared the worktree against a pre-flock
status snapshot before recording this result.

## Deterministic baseline

- Public package validator: `PASS`.
- Unit tests: `63 passed`.
- Canonical/bootstrap guard bindings: `PASS`.
- Internal Markdown links: `PASS`.
- Canonical/bootstrap anti-loop guard SHA-256:
  `73b9722d37452cda93f3d4aff0d96a982aa92dacc0d64a549daa82dea95f2aca`.
- Canonical/bootstrap interface-consumer guard SHA-256:
  `e2f30112737a25378ddbf0ff9d5fa52db49b4c4cef495063310ae38ef20271da`.

These checks are maker evidence. They do not close the findings below.

## Integrated findings

### BLOCK — Engineering review closeout is bypassable and unregistered

1. `scripts/anti_loop_guard.py` accepts direct `--record-block` mutation with only a boundary and
   failure class. A scratch ledger advanced from BLOCK count `0` to `1` without a completed review
   packet or closeout receipt.
2. A complete packet produces the same receipt with and without
   `--require-complete-engineering-review`. The receipt does not attest that closeout-mode
   validation occurred.
3. The canonical ledger registers only `EXAMPLE_LAUNCHER_INTERFACE`. It does not register the
   current Agent+ interface-consumer/defaults promotion boundary. The SECOND LOOK Stage 0 lineage
   boundary is a different boundary and failure class.
4. Safe read-only interface attacks otherwise passed. Consumer omission, unsafe paths, duplicate
   and unknown fields, failed smoke status, invalid runtime keys, and incomplete source identity
   failed closed.

The current review cannot produce an authorized review-grade closeout. Do not record a real ledger
BLOCK from this review.

### BLOCK — Portable lifecycle authority and recovery are incomplete

Disposable clean-room attacks reproduced these defects:

1. A manifest with `managed_files: {}` reports current. Upgrade then overwrites a locally changed
   managed file.
2. A false `source_repository` value reports current and upgrades successfully.
3. The lifecycle manifest and doctor omit `scripts/interface_consumer_guard.py`.
4. Initialization can copy a partial control set before failure. A second initialization then
   refuses the existing controls, so no rollback or resume path exists.
5. `--brain-note` is inserted into YAML without safe scalar encoding.

Fresh initialization, normal status and doctor, unchanged upgrade, ordinary drift refusal, version
mismatch, manifest absence or corruption, path-with-spaces handling, and project-state preservation
passed.

### BLOCK — Discovery state does not preserve the final authority handoff

1. The skill requires owner confirmation before contract drafting, but the single discovery schema
   has no durable confirmation state. After interruption, `READY_FOR_CONTRACT` cannot distinguish
   awaiting confirmation from confirmed.
2. `NEEDS_EVIDENCE` and `NEEDS_PROTOTYPE` require a bounded task, stop condition, and acceptance
   check. The persisted schema has no fields for these items.

Static contract inspection, disposable initialization, single-file persistence, interruption and
resume routing, privacy controls, typed exits, scope split, and contract-ready routing otherwise
passed. Voice turn-taking and model privacy behavior remain uncertified without a live skill
invocation.

### BLOCK — Routing experiment is authorized but not measurable by chain

The owner-authorized ten-chain experiment can proceed only after a fixed manifest and chain-level
schema exist. The current model-review output is aggregate. It does not bind completion, attempts,
wall time, per-chain context, reviewer corrections, write overlap, or premium-review conclusion
changes to each chain.

### BLOCK — Interface-consumer synchronization is premature

SECOND LOOK cannot be classified as downstream drift for interface-consumer closure because the
canonical control remains maker-complete and unaccepted. Synchronization must wait for a reviewed
and released Agent+ version.

### NO_ACTION — Canonical/bootstrap workflow wording differs intentionally

Canonical and bootstrap `AI_WORKFLOW.md` files are not byte-identical. No control requires exact
byte identity for these two documents. The bootstrap contains the required compact semantic
controls. Exact bindings apply to the named guard, protocol, and task-template surfaces.

## Required next action

Create one registered Agent+ `0.2.0` release promotion boundary with separate ledger-bound failure
classes for:

- review-closeout enforcement and review registration;
- portable lifecycle integrity and recoverable initialization;
- Discovery Grill confirmation and bounded handoff durability.

Freeze the complete attack and named-coverage matrices before dispatch. Then authorize one bundled
maker repair. Do not auto-repair from this reviewer record. After deterministic validation, obtain
one fresh integrated review. Keep routing measurement as a separate research contract because it
does not repair the release boundary.

## Open limits

- Agent+ `0.2.0` remains unreleased.
- Existing dirty worktree changes remain preserved.
- No commit, push, tag, release, announcement, downstream synchronization, scientific work, or live
  execution is authorized.
- The public example coverage outcome remains `BLOCK-COVERAGE-EXAMPLE`.

## Restart

```bash
cd agent-plus && scripts/ai-context.sh
```
