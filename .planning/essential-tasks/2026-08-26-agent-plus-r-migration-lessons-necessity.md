# Agent+ R migration lessons — necessity

- **Decision:** Whether Agent+ should preserve the generic workflow lessons proven by a full-volume
  R migration without importing project data or creating another system.
- **Uncertainty:** The existing lean R rule does not yet require complete behavioral parity, an
  early performance falsifier, cost-separated pipeline targets, or retention of failed attempts.
- **Existing evidence:** One proving project reached exact parity only after replacing row-wise
  large-table mutation, separating expensive replay from a cheap downstream target, and retaining
  earlier failed runs as causal evidence.
- **Minimum action:** Add four short generic rules to the canonical and bootstrap R workflow,
  clarify that the existing outcome audit keeps failed attempts, and add focused text tests.
- **Unlock:** Future R migrations receive the successful pattern without a new framework.
- **Stop condition:** Canonical/bootstrap parity, focused tests, and public validation pass.
- **Repeat trigger:** A later proving project identifies a different reusable failure class.
- **Budget:** One documentation-sized patch and existing deterministic validation. No release,
  synchronization, Git operation, scientific execution, data access, or new dependency.

Failure class: `R_MIGRATION_VISIBLE_PARITY_WITH_HIDDEN_BEHAVIOR_AND_COST_COUPLING`.

Public boundary: generic R behavior only. Project paths, data, counts, scientific decisions,
artifacts, and transcripts remain private and are not copied upstream.
