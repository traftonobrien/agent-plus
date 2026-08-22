---
name: agent-plus
description: Route baseball research and analytical-product work through an installed Agent+ project control plane.
---

# Agent+ Router

## Trigger

Use when the user asks to use Agent+, start controlled baseball work, or route a new baseball project.

## Purpose

Confirm the project control plane, load bounded context, and route the task to the smallest matching Agent+ procedure.

## Required inputs

- The project root.
- The initial idea or the already-settled research or product decision.
- The permitted data and action scope.

## Allowed actions

1. Run the project doctor and context commands.
2. Read planning state and check whether a discovery brief or accepted research contract exists.
3. If the decision, user, scope, null or BLOCK path, evidence need, or claim ceiling is unclear,
   route to `$agent-plus-discovery-grill`. Do not draft a contract yet.
4. Route to the research-contract template only when the one discovery file has
   `status: READY_FOR_CONTRACT` and durable `owner_confirmation: CONFIRMED`, or when the owner
   supplied a contract-ready decision.
   A missing confirmation field is `AWAITING` and fails closed after resume.
5. Route publication-oriented detect, humanize, or de-slop requests to `$editorial-pass`. Keep the
   project's output policy active for ordinary status and technical responses.
6. Route Agent+ version, calibration, upgrade, and synchronization requests to `$agent-plus-sync`.
7. Select one bounded procedure from the installed Agent+ skill set and create the required
   necessity card before substantive work.

## Required outputs

- Current project gate.
- Selected procedure and authority tier.
- Discovery state or accepted contract identity when one exists.
- Exact next action or typed `BLOCK`.

## Acceptance checks

- The project doctor passes.
- Unclear ideas route to one discovery brief instead of premature contract drafting.
- `READY_FOR_CONTRACT` still requires user confirmation before contract drafting.
- `READY_FOR_CONTRACT` with `owner_confirmation: AWAITING` routes back to discovery after resume.
- `NEEDS_EVIDENCE` and `NEEDS_PROTOTYPE` require one persisted bounded handoff task, stop condition,
  and acceptance check.
- The selected work has a decision, stop condition, and acceptance check.
- Editorial work routes to `$editorial-pass` without claiming authorship detection.
- Agent+ update work routes to `$agent-plus-sync` and audits before mutation.
- The task does not exceed the active claim or data authority.

## Handoff requirements

Record the outcome, evidence, limits, next action, and restart command in project-local state.

## Explicit limits

- This skill does not install Agent+ by itself.
- This skill does not treat discovery as evidence, contract acceptance, or work authorization.
- This skill does not grant data, live, scientific, or promotion authority.
- This skill does not make a chat transcript the system of record.
