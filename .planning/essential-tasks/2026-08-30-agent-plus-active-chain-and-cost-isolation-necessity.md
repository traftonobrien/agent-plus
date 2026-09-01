# Agent+ active-chain and cost-isolation upgrade — necessity

- **Decision:** Whether Agent+ should make the recent successful bounded-chain and exact-target
  routing pattern a generic public default.
- **Uncertainty:** Canonical Agent+ defines stages, stop rules, cached targets, and authority
  boundaries in prose, but it cannot deterministically reject an early chain closeout, a stale
  copied authority, or a broad upstream rerun when only one cheap downstream target changed.
- **Existing evidence:** The proving project completed long engineering work reliably when one small
  chain capsule routed every stage, live authority files remained authoritative, expensive current
  ancestors were reused, and two adjacent launch failures forced one boundary sweep.
- **Minimum action:** Add one generic read-only active-chain guard with synthetic tests, then add
  short canonical and bootstrap rules for live authority, exact target-graph isolation,
  deterministic loop detection, and owner-decision escalation.
- **Unlock:** Agent+ consumers can keep long multi-stage work moving without copying private
  authority, stopping early, or repeating expensive current work.
- **Stop condition:** Focused guard tests, canonical/bootstrap byte parity, complete public tests,
  and public-package validation pass.
- **Repeat trigger:** A proving project identifies a different reachable chain-routing or
  cost-isolation failure class.
- **Budget:** Deep engineering-only session. One accountable writer, deterministic evaluation, no
  sub-agents, no scientific execution, no data access, and no release action.

Failure class: `MULTI_STAGE_CHAIN_EARLY_CLOSEOUT_STALE_AUTHORITY_AND_BROAD_RERUN`.

Public boundary: generic routing state and synthetic paths only. Project plans, scientific values,
counts, identities, artifacts, receipts, private paths, and transcripts remain outside Agent+.

Authorization boundary: the owner authorized implementation and broad optimization. Commit, push,
tag, release, consumer synchronization, and proving-project mutation are not authorized.
