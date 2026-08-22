---
schema: agent-plus-project-discovery/v1
status: DISCOVERY_ACTIVE
owner_confirmation: AWAITING
updated: YYYY-MM-DD
---

# Project Discovery

## Project decision

- **Decision this work may change:**
- **Primary user or owner:**
- **Why this matters now:**

## Problem definition

- **Current question:**
- **Population or product scope:**
- **Time boundary:**
- **Explicit exclusions:**
- **Null or BLOCK path:**
- **Maximum permitted claim:**

## Settled decisions

| Decision | Reason | Date |
| --- | --- | --- |

## Unknowns and assumptions

| Item | Type | Resolution route |
| --- | --- | --- |

Use `unknown` or `assumption` for Type. Use `conversation`, `evidence`, `prototype`, or `owner decision` for Resolution route.

## Rejected alternatives

| Alternative | Why rejected |
| --- | --- |

Record only reasons a future worker would otherwise relitigate.

## Evidence and prototype needs

- **Evidence needed:**
- **Prototype needed:**
- **Available sources or systems:**
- **Forbidden or unavailable inputs:**

## Current frontier

- **Open decisions:**
- **Next question:**
- **Recommended answer:**

## Bounded handoff

Use exactly one bounded handoff when the exit state is `NEEDS_EVIDENCE` or
`NEEDS_PROTOTYPE`. Leave these fields empty for other exit states.

- **Task (`handoff_task`):**
- **Stop condition (`handoff_stop_condition`):**
- **Acceptance check (`handoff_acceptance_check`):**

## Exit

- **State:** `DISCOVERY_ACTIVE`
- **Owner confirmation:** `AWAITING`
- **Why:**
- **Next artifact or action:**
- **Restart instruction:** `Use $agent-plus-discovery-grill and resume from .planning/discovery/PROJECT-DISCOVERY.md.`

Allowed final states: `READY_FOR_CONTRACT`, `NEEDS_EVIDENCE`, `NEEDS_PROTOTYPE`, `SPLIT_SCOPE`, or `BLOCKED`.
Allowed owner confirmation states: `AWAITING` or `CONFIRMED`.
