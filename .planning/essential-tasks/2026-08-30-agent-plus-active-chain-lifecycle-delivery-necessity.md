# Agent+ active-chain lifecycle delivery necessity

Date: 2026-08-30

Status: `AUTHORIZED`.

## Decision

Close the active-chain delivery gap across initialization, manifests, upgrades, recovery, and
doctor checks. Then run deterministic evaluation and one fresh independent lifecycle review.

## Why this work is necessary

- A clean initializer exits successfully without delivering `scripts/active_chain_guard.py`.
- The initializer copies the example capsule but does not manage its digest.
- The copied doctor reports `PASS` when the guard is absent and both controls are unmanaged.
- The released transaction format rejects a prior exact managed set before it can add new files.
- A partial additive upgrade has no durable rule to remove candidate-only files during recovery.

## Minimum lifecycle design

1. Add one authenticated current managed-set identity and one exact historical v1 set.
2. Accept only the released `0.2.0` and `0.3.0` v1 manifests with the exact historical set.
3. Permit additive managed-set upgrades only.
4. Reject managed-file removal and candidate-only destination collisions.
5. Preserve uncommitted collision files and reject modified committed additions during recovery.
6. Record candidate-only files in the transaction journal.
7. Remove committed candidate-only files during recovery before terminal cleanup.
8. Deliver and manage the active-chain guard and sanitized example in new projects.
9. Make normal and legacy doctor routes verify the exact manifest set and managed digests.
10. Preserve required executable modes through upgrade and recovery copies.

## Limits

- No managed-file removal migration.
- No fallback to an unknown manifest version, schema, set identity, or file set.
- No overwrite of an unmanaged destination.
- No change to active-chain semantics, scientific authority, or claim authority.
- No proving-project mutation, data access, Git mutation, release, or consumer synchronization.
- Stop on a substantive evaluator finding or reviewer `BLOCK`.

## Acceptance

- Clean initialization delivers both active-chain controls and records both digests.
- Historical v1 manifests remain valid only for the exact released managed set.
- Status reports an available generation update for an exact historical installation.
- Additive upgrade and legacy-adoption upgrade succeed without changing project-owned state.
- Injected partial commit recovery restores the prior installation and removes candidate-only files.
- Missing, drifted, subset, superset, forged, or colliding states fail closed.
- Managed context, doctor, and guard commands remain executable after upgrade and recovery.
- Canonical and bootstrap active-chain files remain byte-identical.
- Focused lifecycle tests and full public validation pass.
- One fresh reviewer completes the registered matrix with `PASS`.

## Authorization

The owner authorized this bounded lifecycle-delivery closure on 2026-08-30.

## Restart

```sh
./scripts/ai-context.sh
```
