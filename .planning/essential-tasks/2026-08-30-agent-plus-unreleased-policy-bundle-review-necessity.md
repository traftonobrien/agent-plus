# Agent+ unreleased policy bundle review — necessity

Date: 2026-08-30

- **Decision:** Whether the unreleased Lean R, bounded small-correction, R migration, complexity,
  and versioning refinements are accepted as one coherent public Agent+ policy bundle.
- **Uncertainty:** Deterministic checks cover their text and canonical/bootstrap bindings, but no
  fresh independent review names all of their semantic and authority boundaries.
- **Existing evidence:** The public validator passes `163/163`. The active-chain/cost-isolation and
  lifecycle-delivery implementation boundaries have separate accepted fresh reviews and remain
  hash-stable.
- **Minimum action:** Freeze only the uncovered policy surfaces, run deterministic checks, and
  dispatch one fresh independent policy-focused reviewer against a closed attack matrix.
- **Unlock:** The current unreleased public bundle becomes ready for a separate owner release
  decision without reopening already accepted implementation reviews.
- **Stop condition:** `PASS` or `BLOCK` after all `22` attacks and `10` named coverage items.
- **Repeat trigger:** Any frozen policy byte changes or the reviewer returns `BLOCK`.
- **Budget:** One deterministic evaluation and one fresh review. No implementation repair, Git
  mutation, version change, release, consumer synchronization, data access, or scientific work.

Failure class: `unreviewed-unreleased-policy-bundle` under
`AGENT_PLUS_POLICY_REFINEMENTS`.

Public boundary: generic workflow policy and synthetic checks only. Proving-project data, state,
receipts, paths, transcripts, and scientific authority remain excluded.
