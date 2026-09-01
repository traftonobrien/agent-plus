# Agent+ active-chain typed enum repair necessity

Date: 2026-08-30

Status: `AUTHORIZED`.

## Decision

Repair the one schema failure class from fresh integrated review 001. Then run deterministic
evaluation and one new fresh independent integrated review.

## Why this work is necessary

- Fresh review 001 returned `BLOCK` after all 20 attacks and 16 coverage areas.
- JSON arrays or objects in `status`, `change_kind`, or stage enum fields can raise uncaught
  `TypeError` instead of typed `ChainError`.
- The public guard promises closed schema validation and typed fail-closed behavior.

## Minimum action

1. Add one table-driven regression test for arrays and objects in every affected enum field.
2. Validate the enum value type before set membership.
3. Keep the public schema, allowed values, terminal semantics, and authority boundaries unchanged.
4. Copy the exact repair to the bootstrap guard.
5. Run focused tests, the complete public validator, and one new fresh review.

## Limits

- No new enum, dependency, fallback, caller choice, or exception-swallowing path.
- No change to scientific, privacy, security, claim, promotion, or release authority.
- No proving-project mutation, data access, scientific execution, Git mutation, release, or
  consumer synchronization.
- Stop on any second defect or new reviewer `BLOCK`.

## Acceptance

- Every array and object probe returns typed `ChainError` through the Python API.
- The CLI rejects the same malformed inputs without a traceback.
- Existing valid and invalid capsule behavior remains unchanged.
- Canonical and bootstrap guards remain byte-identical.
- Full public validation passes.
- One new fresh reviewer returns `PASS` on the complete registered matrix.

## Authorization

The owner authorized this new bounded repair chain on 2026-08-30 after review 001 returned
`BLOCK`.

## Restart

```sh
./scripts/ai-context.sh
```
