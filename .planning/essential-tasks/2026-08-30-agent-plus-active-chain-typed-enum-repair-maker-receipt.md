# Agent+ active-chain typed enum repair maker and evaluator receipt

Date: 2026-08-30

Outcome: `PASS — FRESH REVIEW REQUIRED`.

## Boundary

This repair addresses only Finding I-1 from fresh integrated review 001. It does not change the
schema, allowed enum values, stage rules, terminal behavior, authority, or release boundary.

## Reproduction

The minimized Python API probe set `status` to a JSON array. It deterministically returned:

```text
RED_UNCAUGHT_TYPEERROR unhashable type: 'list'
```

A table-driven regression then reproduced the same uncaught `TypeError` for arrays and objects in:

- chain `status`
- chain `change_kind`
- stage `role`
- stage `status`

The CLI probe also failed because `BLOCK_CHAIN_STATUS` was absent and a traceback reached stderr.
One initial unittest command used an invalid package import path and ran no product test. The direct
repository unittest interface then produced the intended red evidence.

## Diagnosis

The confirmed cause was direct set membership before type validation at all four enum seams. The
chain-only and CLI-only alternatives were falsified by the complete API matrix.

## Repair

- Require a string before each chain or stage enum membership test.
- Preserve the existing typed error code for each field.
- Apply the same four guards to the canonical and bootstrap scripts.
- Add table-driven array and object regression probes for every affected field.
- Add one subprocess test that requires a typed CLI error without a traceback.

## Deterministic evidence

- API malformed-enum matrix: `8/8` passed after repair.
- CLI traceback rejection: `1/1` passed after repair.
- Focused active-chain suite: `17/17`.
- Complete public suite: `149/149`.
- Python compilation: `PASS`.
- Canonical/bootstrap guard binding: `PASS`.
- Internal links and public privacy validation: `PASS`.
- Complete public-package validator: `PASS`.
- Repair task admission receipt:
  `sha256:4952f6cae7bea1e2c80e5a4ff92e9b13ec4e7d0d56f139336a7984c462923b84`.

## Limits

- This is maker and deterministic evaluator evidence only.
- No reviewer assessed the repair.
- No proving-project mutation, data access, scientific execution, dependency change, Git mutation,
  version change, release, or consumer synchronization occurred.

## Next action

Run one new fresh independent integrated review against the 21-attack matrix. Stop on `BLOCK`. If
the review passes, close the active chain and stop for the owner release decision.

## Restart

```sh
./scripts/ai-context.sh
```
