# Agent+ active-chain completion audit

Date: 2026-08-30

Outcome: `PASS — ENGINEERING REVIEW ACCEPTED; OWNER DECISION REQUIRED`.

This audit proves review readiness. It does not provide the independent verdict and does not
authorize promotion, release, Git mutation, or consumer synchronization.

## Requirement audit

| Requirement | Authoritative evidence | Result |
| --- | --- | --- |
| One generic active-chain route | Canonical and bootstrap `scripts/active_chain_guard.py` | `PASS` |
| Live authority remains external | Closed schema, safe project-local authority references, and policy text | `PASS` |
| Stage and terminal state are deterministic | Ordered stage checks plus `PASS`, `NULL`, and `BLOCK` closeout tests | `PASS` |
| Early closeout and terminal continuation fail closed | Focused negative tests | `PASS` |
| Two failures cannot route another local repair | Active-chain check plus authoritative anti-loop ledger | `PASS` |
| Capsule input is closed | Only the active capsule and sanitized example locations are accepted | `PASS` |
| Path and input parsing fail closed | Containment, symlink, duplicate-key, nonfinite, type, and size tests | `PASS` |
| Canonical and bootstrap controls remain bound | Public-package byte checks | `PASS` |
| Exact target-graph and current-ancestor reuse are defaults | Workflow, protocol, template, and research profile tests | `PASS` |
| Live authority outranks memory and transcripts | Workflow and protocol policy tests | `PASS` |
| Adjacent launch failures stop patch-and-run behavior | `LOOP_DETECTED` policy and ledger route | `PASS` |
| Meaning-changing subtraction returns to the owner | `OWNER_DECISION_REQUIRED` policy tests | `PASS` |
| Review admission is ledger-bound | Planned review packet passes standard anti-loop validation | `PASS` |
| Maker evidence cannot impersonate review acceptance | Complete-review mode rejects the planned packet | `PASS` |
| Public safety and package integrity hold | Full public validator, link check, and privacy scan | `PASS` |
| Fresh independent verdict exists | Review packet remains `planned` | `PENDING` |

## Synchronization status

- Agent+ version: released `v0.3.0`; this capability is unreleased.
- Proving project: SECOND LOOK, read-only during this audit.
- Inventory: 197 public control surfaces were hashed without reading baseball data or artifacts.
- Exact-copy status: the anti-loop guard is exact. The proving-project active-chain guard is a
  project adapter and is not a canonical source.
- Downstream drift: none declared before an accepted Agent+ release.

## Findings

- `UPSTREAM_CANDIDATE`: external capsule path closure.
  - Failure class: a caller could validate routing state outside the project root.
  - Change: bind capsules to the two documented project-local locations and reject symlinks.
  - Acceptance: focused negative tests, canonical/bootstrap binding, and public validation pass.
- `PROJECT_ADAPTER`: SECOND LOOK scientific stage names, authority rules, and live-data boundaries.
  - These controls remain project-owned and did not move upstream.
- `PRIVATE_STATE`: proving-project plans, receipts, data identities, scientific values, and history.
  - These surfaces were excluded from canonical implementation and public evidence.
- `NO_ACTION`: generic live-authority precedence, exact target isolation, failure limits, fresh
  session routing, and owner-decision escalation are now covered by canonical controls.
- `DOWNSTREAM_DRIFT`: none. The new capability has no accepted release.

## Deterministic evidence

- Focused active-chain tests: `15/15`.
- Focused anti-loop tests: `54/54`.
- Workflow-default tests: `7/7`.
- Complete public suite: `147/147`.
- Public-package validation: `PASS`.
- Planned review receipt:
  `sha256:5db138c260311831b093175bbe38939c39a41bac31390a49d3c7fae7c793ba00`.
- Complete-review mode: expected `E_INCOMPLETE_COVERAGE` while review status is `planned`.

## Post-audit review result

- Fresh integrated review 001 assessed all 20 attacks and 16 coverage areas.
- Verdict: `BLOCK` on the typed enum schema boundary.
- Finding: array or object values in chain and stage enum fields can raise uncaught `TypeError`.
- Completed review receipt:
  `sha256:aac523d9b1704566df547108c42802e0fcfe3189a400cac2a3c5811904496f7b7`.
- The ledger records `block_count=1`. Post-record closeout receipt:
  `sha256:92ee4f60d8977d199f6207170d6f93407ec6bff550aef5e08cbe337721bf17fc`.
- No repair followed the reviewer verdict.

## Repair 002 and final review

- The owner authorized one new bounded repair chain.
- Four string checks close every affected enum membership seam without changing allowed values.
- API array and object probes pass `8/8`; the CLI traceback probe passes `1/1`.
- Focused active-chain tests pass `17/17`; the complete suite passes `149/149`.
- Fresh review 002 passed all `21/21` attacks, `16/16` coverage areas, and `27/27` independent
  probes. It found no Critical, Important, or Minor issue.
- Accepted closeout receipt:
  `sha256:3ceb5acd7637c4568663a2c93216aa8b065d0ace32a723485fda1ea51be9ecfc`.
- The only remaining action is the explicit owner promotion, release, or synchronization decision.

## Limits

- Review 001 returned `BLOCK`; owner-authorized repair 002 and fresh review 002 closed that finding.
- No engineering review finding remains open.
- No proving-project mutation, data access, scientific execution, dependency change, version
  change, Git mutation, release, or consumer synchronization occurred.

## Next action

Stop for the explicit owner promotion, release, or consumer-synchronization decision.

## Restart

```sh
./scripts/ai-context.sh
```
