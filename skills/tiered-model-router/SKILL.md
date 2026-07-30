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

## Allowed actions

- Route to deterministic tooling, reversible assistance, bounded implementation, or fresh review.
- Write a bounded work order.
- Escalate after two failed attempts.

## Required outputs

- Routing record with tier, exact tool or model, and rationale.
- Work order with allowed inputs and acceptance check.
- Escalation or BLOCK when no safe route exists.

## Acceptance checks

- The route names a real decision.
- The worker cannot certify its own result.
- PASS and BLOCK lead to different next actions.

## Handoff requirements

Record the resolved route, result, evidence reference, and next owner.

## Explicit limits

Do not allow silent fallback. Do not give a model more data or authority than the work order allows. Do not use a premium model for routine search or counts.
