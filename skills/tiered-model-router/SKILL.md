# Tiered Model Router

## Trigger

Use before assigning a task to a model, agent runtime, or deterministic tool.

## Purpose

Choose the lowest authority and cost that can safely close the task uncertainty.

## Required inputs

- Decision, uncertainty, and stop condition.
- Allowed files, tools, and network rule.
- Context, time, and attempt budget.
- Acceptance check and required role separation.
- Orchestration mode: `quick`, `standard`, `deep`, or `scientific/live`.
- Exact model, reasoning level, authorization scope, ownership map, and chain stages.
- Concurrency, tool/context budgets, reserve use, checkpoint interval, overnight setting, evaluator
  commands, and fresh verifier contract.

## Allowed actions

- Route to deterministic tooling, reversible assistance, bounded implementation, or fresh review.
- Write a bounded work order.
- Escalate after two failed attempts.
- Use the higher-capacity mode table in `AI_WORKFLOW.md` without expanding authority, context,
  retries, reviewer count, or owner authorization.
- Parallelize only independent exploration; keep one writer per repository and all later stages
  sequential.

## Required outputs

- Routing record with tier, exact tool or model, and rationale.
- Work order with allowed inputs and acceptance check.
- Escalation or BLOCK when no safe route exists.
- A complete task packet using the required fields in `.planning/templates/ESSENTIAL-TASK.md`.
- A frozen evidence handoff before the exclusive maker and an independent verifier contract at the
  promotion boundary.

## Acceptance checks

- The route names a real decision.
- The worker cannot certify its own result.
- PASS and BLOCK lead to different next actions.
- The selected mode's worker, writer, context, time, and authorization limits are met.
- The evaluator is deterministic, and the fresh verifier sees the contract, artifact, receipts, and
  attack matrix rather than the maker transcript.

## Handoff requirements

Record the resolved route, result, evidence reference, and next owner.

## Explicit limits

Do not allow silent fallback, recursive spawn, overlapping writes, or more than three workers. Do not
give a model more data or authority than the work order allows. Do not use a premium model for
routine search or counts. Stop on maker, evaluator, or reviewer `BLOCK`; never auto-repair after a
reviewer `BLOCK`. Scientific/live work remains first-error and requires human owner authorization
before data access, live execution, or promotion.
