---
name: agent-plus-discovery-grill
description: Turn an early baseball research, modeling, scouting, or analytical-product idea into a durable Agent+ discovery brief through a voice- or text-friendly interview. Use when starting a project, defining an unclear problem, stress-testing scope, or resuming discovery before a research contract exists.
---

# Agent+ Discovery Grill

## Trigger

Use when starting a baseball research, modeling, scouting, or analytical-product project; when the problem or scope is unclear; or when resuming discovery before a research contract exists.

## Purpose

Interrogate the idea until its decision, users, boundaries, unknowns, and evidence needs are explicit. Preserve settled decisions in one file while keeping scientific and action authority closed.

This skill adapts Matt Pocock's Grill Me design-tree method for Agent+ project discovery. Read [references/attribution.md](references/attribution.md) when distributing or modifying the skill.

## Required inputs

- Project root.
- Initial idea or decision.
- Known authority, data, privacy, and action boundaries.

## Allowed actions

### Start

1. Confirm the project root. If none exists, ask for one before writing.
2. Read project instructions and existing discovery or contract artifacts.
3. Inspect facts available from the workspace or tools. Do not ask the user to retrieve facts that can be checked directly.
4. Create `.planning/discovery/PROJECT-DISCOVERY.md` from [assets/PROJECT-DISCOVERY.md](assets/PROJECT-DISCOVERY.md) only if no discovery artifact exists.
5. Treat the artifact as a decision brief, not a transcript.
6. Preserve `owner_confirmation: AWAITING` until the owner confirms the final synthesis. Set it to
   `CONFIRMED` in the same file only after that confirmation.

### Grill

Map the problem as a decision tree. Recompute the unsettled frontier after every answer.

- In voice or conversational mode, ask one highest-leverage frontier question at a time.
- In text mode, still default to one question. Offer a numbered frontier round only when the user asks for batching.
- Give a recommended answer and the tradeoff behind it.
- Accept `I don't know`. Convert it into an explicit unknown and decide whether evidence, a prototype, or a conservative default can resolve it.
- Challenge fuzzy terms, conflicting goals, hidden users, unbounded populations, vague success claims, and solutions stated before the problem.
- Push back when an answer weakens the stated decision or exceeds available authority.
- When a question depends on a workspace fact, inspect it before continuing that branch.
- When a question cannot be settled by conversation, stop that branch and route it to evidence gathering or a bounded throwaway prototype.

After each user answer, update the discovery file immediately. Record only the current synthesis:

- settled decisions and reasons;
- unresolved questions and assumptions;
- rejected alternatives when the reason matters later;
- evidence or prototype needs;
- the current frontier and next question;
- the current exit state.

Do not save raw audio, verbatim answers, private chat text, hidden reasoning, or speculative claims. Remove sensitive details that are unnecessary for project control.

### Exit

Continue until no conversational question can materially improve the project definition. Then select exactly one state:

- `READY_FOR_CONTRACT`: the decision, research question, user, scope, null or BLOCK path, evidence need, and claim ceiling are clear enough to draft a research contract.
- `NEEDS_EVIDENCE`: a named external fact must be established first.
- `NEEDS_PROTOTYPE`: a named design or feasibility question needs a bounded disposable test.
- `SPLIT_SCOPE`: the idea contains multiple independent decisions that need separate discovery briefs.
- `BLOCKED`: required authority, access, ownership, or a decision is absent.

Show the user the concise final synthesis and ask them to confirm shared understanding. Do not draft
the research contract until the same file has `status: READY_FOR_CONTRACT` and
`owner_confirmation: CONFIRMED`. Do not begin data collection, modeling, implementation, or live
work merely because discovery is complete.

## Required outputs

- One updated `.planning/discovery/PROJECT-DISCOVERY.md` decision brief.
- One current typed exit state and its reason.
- One durable owner-confirmation state. `AWAITING` and `CONFIRMED` have different routing effects.
- One next question while active, or one exact next action and restart instruction at exit.

## Acceptance checks

- The file contains a decision, user, scope, null or BLOCK path, and current frontier or final route.
- Each unknown names a resolution route.
- The artifact contains no raw transcript, private chat text, hidden reasoning, or unnecessary sensitive detail.
- The final state does not imply contract acceptance, evidence, verification, or authorization.
- `READY_FOR_CONTRACT` is not routable until durable owner confirmation is `CONFIRMED`.
- `NEEDS_EVIDENCE` and `NEEDS_PROTOTYPE` persist exactly one handoff task, stop condition, and
  acceptance check in this file.
- The user confirms the final synthesis before contract drafting begins.

## Handoff requirements

After confirmation:

1. If `READY_FOR_CONTRACT`, route to the Agent+ research-contract template and preserve the discovery file as pre-contract context.
2. If `NEEDS_EVIDENCE` or `NEEDS_PROTOTYPE`, persist one bounded handoff in the discovery file
   using `handoff_task`, `handoff_stop_condition`, and `handoff_acceptance_check`.
3. If `SPLIT_SCOPE`, create no new briefs until the user selects the first decision.
4. If `BLOCKED`, record the exact unblock condition and restart instruction.

The discovery brief informs the next artifact. It never replaces an accepted research contract, necessity card, deterministic evidence, fresh verification, or human authorization.

## Explicit limits

- Do not treat conversation as evidence or acceptance.
- Do not store raw voice or chat transcripts.
- Do not create multiple discovery state files for one decision.
- Do not treat `READY_FOR_CONTRACT` with `owner_confirmation: AWAITING` as contract-ready.
- Do not begin data collection, modeling, implementation, live work, or claim promotion.
- Do not overwrite an accepted research contract or project-owned decision without explicit authority.
