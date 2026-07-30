# Session Context Handoff

## Trigger

Use when a bounded task pauses, ends, changes owner, or needs a safe restart.

## Purpose

Convert temporary session work into an exact, reviewable restart record.

## Required inputs

- Changed files or artifact identifiers.
- Verification performed and result.
- Open limits, BLOCKs, and forbidden actions.
- One next action and restart command.

## Allowed actions

- Create or update a task-specific handoff.
- Rewrite changing verified project memory.
- Link durable decisions to curated knowledge.

## Required outputs

- Handoff using the template.
- Updated verified state when state changed.
- Exact restart command.

## Acceptance checks

- A new operator can locate the exact evidence.
- The next action is singular and bounded.
- BLOCKs name a resume condition.

## Handoff requirements

The output is the handoff. It must include verified state, limits, next action, and restart command.

## Explicit limits

Do not summarize a private transcript into public material. Do not claim unverified work is complete. Do not overwrite durable knowledge with temporary notes.
