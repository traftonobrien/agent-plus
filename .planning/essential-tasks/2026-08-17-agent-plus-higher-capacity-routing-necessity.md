---
task: "Implement the owner-authorized generic higher-capacity Agent+ routing policy and bootstrap parity"
owner_role: "maker"
tier: "2"
time_budget: "one bounded implementation session"
attempt_limit: 2
orchestration_mode: "standard"
exact_model: "Sol/high control; Luna xhigh maker; deterministic evaluator; fresh Luna xhigh reviewer required"
reasoning: "implementation"
authorization_scope: "Owner-authorized public policy and bootstrap documentation only; no live or scientific execution"
ownership_map: "Sol/controller; this maker; deterministic scripts; fresh independent reviewer; human owner"
chain_stages: "plan -> policy implementation -> deterministic validation -> fresh review -> Sol synthesis"
concurrency: "No parallel workers for this bounded documentation change; one writer"
tool_budget: "Routine documentation and validation budgets from AI_WORKFLOW.md; maximum two failed attempts"
context_budget: "25K ordinary / 40K premium ceilings; implementation target 8-15K"
reserve_use: "No premium reserve used; reserve remains for scientific, leakage, hard-architecture, or irreversible decisions"
checkpoint_interval: "One bounded wait per stage; stop at any BLOCK"
overnight: "no"
evaluator_commands: "sh -n scripts/*.sh bootstrap/base/scripts/*.sh; python3 -m unittest discover -s tests -p 'test_*.py'; bash scripts/validate-public-package.sh; bootstrap init and doctor"
fresh_verifier_contract: "Review changed policy and bootstrap files independently; verify mode limits, authority boundaries, template fields, parity, and absence of owner-specific plan names; do not use maker transcript"
---

# Necessity and decision record

## Decision

Should the public Agent+ package document a generic higher-capacity session profile that improves
bounded throughput while preserving authority, context, retry, reviewer, scientific/live, and human
authorization gates? `PASS` enables the public policy and bootstrap route to be reviewed. `BLOCK`
leaves the existing routing policy unchanged and requires a new owner decision.

## Uncertainty

The existing policy defines model tiers and direct delegation, but does not define the owner-confirmed
capacity modes, per-role budgets, overnight boundary, reserve use, review cadence, or complete task
packet fields. The public package must state those controls without naming a personal plan or making a
performance claim.

## Existing evidence

The local model-review baseline had zero traffic. It therefore provides no measured throughput,
quality, or correction-rate result. The owner authorized this generic policy and a 10-completed-chain
experiment; that authorization is a routing decision, not a measured performance claim. Guard v2,
role separation, the two-BLOCK architecture reset, first-error scientific/live behavior, and outcome
metrics are already accepted controls and remain unchanged.

## Minimum action

Update the binding public policy, project instructions, essential-work template, routing guide, router
skill, Claude profile, and their bootstrap equivalents. Add no implementation, ledger, receipt, data,
or personal-plan detail. Run the public validator, unit tests, shell syntax checks, bootstrap
initializer, and generated-project doctor.

## Boundary and stop condition

Allowed artifacts are the listed Agent+ policy/bootstrap files, this record, `.planning/STATE.md`, and
`.claude-memory.md`. Do not edit SECOND LOOK, Guard v2 implementation, ledgers, accepted receipts,
README, scripts, or Git state. Stop at the first failed validation; a fresh review `BLOCK` ends the
chain and does not trigger auto-repair.

## Decision branches

- **If PASS:** hand the exact changed files, validation receipts, and this record to one fresh
  independent reviewer; keep scientific/live and public coverage gates unchanged.
- **If BLOCK:** preserve the evidence, report the exact failed boundary, and wait for a changed
  contract or explicit owner direction. Do not retry through a fallback.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: fresh independent review of the higher-capacity routing boundary
user_visible_outcome: public Agent+ and generated projects have a complete generic bounded-capacity routing contract
repeat_trigger: model/rate/plan change; two routing BLOCKs; 10 completed bounded chains; 14 days; average context above 40K; reviewer correction above 20%
status: AGENT_PLUS_HIGH_CAPACITY_ROUTING_MAKER_COMPLETE — FRESH REVIEW REQUIRED
```

## Validation receipts

- `sh -n scripts/*.sh bootstrap/base/scripts/*.sh`: PASS.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: PASS, 45 tests.
- Isolated bootstrap initializer and `scripts/agent-plus-doctor.sh`: PASS.
- Changed-file public-safety, whitespace, link, and frontmatter checks: PASS.
- `bash scripts/validate-public-package.sh`: PASS after the generated model-review report was made
  public-safe by replacing its private local project path with `agent-plus`.
