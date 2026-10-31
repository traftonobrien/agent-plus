---
name: agent-plus-session-context-handoff
description: Save one Agent+ task restart state in the active project. Not cross-project sync or transcript export.
---

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

- Update the existing task handoff; create one only when no suitable restart record exists.
- Keep changing execution state in that handoff. Project memory points to it and records only project-wide changes.
- Link reusable accepted artifacts from their existing owner; do not create another lessons register.

## Required outputs

- Updated restart record using the repository’s `templates/session-handoff-template.md`.
- Updated verified state when state changed.
- Exact restart command.

## Acceptance checks

- A new operator can locate the current action and exact evidence without reading the whole history.
- Prior states remain clearly historical; a routine edit does not create a new handoff file solely because AI assisted.
- The next action is singular and bounded.
- BLOCKs name a resume condition.

## Handoff requirements

The output is the handoff. It must include verified state, limits, next action, and restart command.

## Explicit limits

Do not summarize a private transcript into public material. Do not claim unverified work is complete. Do not overwrite durable knowledge with temporary notes.
