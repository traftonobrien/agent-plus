# Example: Baseball Research Question

> **Synthetic example.** Names, dates, inputs, and identifiers are illustrative. This is not a result from SECOND LOOK or any other private project.

## Question

For a defined historical population, does adding a hitter's prior pitch-family exposure improve a declared chronological prediction target versus a count-and-location baseline?

## Decision

Decide whether the exposure feature may advance to a pre-specified out-of-sample evaluation. It may not advance if date coverage is incomplete or temporal order is not verified.

## Contract summary

- Population: approved historical plate appearances, after documented inclusion rules.
- Time rule: feature values may use only events earlier than the prediction timestamp.
- Comparator: a fixed count-and-location baseline.
- Null path: no improvement against the comparator under the stated metric.
- BLOCK path: an independent inventory cannot reconcile the required date partitions.
- Claim boundary: no claim beyond the evaluation level defined by the contract.

See [the full contract template](../templates/research-contract-template.md).
