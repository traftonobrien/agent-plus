# Example: Session Handoff

> **Synthetic example.** This handoff is a public pattern, not a record from a private project.

## Verified state

- Created `EX-EVID-001` for the synthetic coverage check.
- Verified that 11 of 12 required illustrative partitions are present.
- No model or performance result was created.

## BLOCK

- `BLOCK-COVERAGE-EXAMPLE`: Independent inventory receipt is missing.
- Do not replace the receipt with an estimate or an assumed complete month.

## Next action

Acquire the independent inventory receipt. Compare its partitions with `example-manifest-v1`. Update the evidence record only if the reconciliation is complete and reviewable.

## Restart

`cd agent-plus && sed -n '1,200p' examples/sample-evidence-record.md`
