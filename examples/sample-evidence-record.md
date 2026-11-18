# Example: Evidence Record

> **Synthetic example.** No raw baseball data or private artifact is included.

The counts below are illustrative inputs, not measurements from an executed command. This example demonstrates the research evidence path, not the minimum record for an ordinary edit.

## Identity

- Record ID: `EX-EVID-001`
- Contract ID: `EX-CONTRACT-001 v1`
- Status: `BLOCK`
- Artifact reference: `example-manifest-v1`

## Deterministic evidence

- Expected monthly partitions: 12.
- Located partitions: 11.
- Independent inventory receipt: absent.
- Coverage reconciliation: not possible.

## Interpretation

The system can state that coverage is not verified. It cannot state that the population is complete, compute a model comparison, or make a prediction claim.

## Resume condition

Add an independent inventory receipt, reconcile every required partition, and request fresh verification.

## Alternative: ordinary code correction

This separate hypothetical example belongs in the existing task record. It is not another stage of the research example above. The following checks are proposed, not executed, so they do not establish PASS.

- Change: repair the shared CSV writer that drops required columns, rather than patching each reader.
- Check: run the actual writer and reader on a disposable known-answer fixture. Compare column names, units, missing values and numerical results with independent expectations.
- Negative control: remove a required column and confirm that the check fails. Restore the correct writer and confirm that it passes.
- Limits: this small check does not rerun the accepted analysis or establish live integration. Record the tested revision, exact command and observed result when performed.

Close the coding task when its required checks pass. Keep unrelated source, scientific or publication limits scoped to their own actions. Add no separate handoff or review file merely to describe this correction.
