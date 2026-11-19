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
- One next action and restart command when work remains, or a completed state.

## Allowed actions

- Update the existing task handoff or local memory when it already serves as the restart record. Create a handoff only when no suitable record exists.
- Replace its short current opening. Keep completed lanes, current artifacts and limits there. Include one next action and restart command when work remains. Otherwise state complete and awaiting a new request.
- Do not invent work or repeat unchanged passing checks solely to fill a handoff. Resume completed work only for a new request, changed evidence or a concrete unresolved concern.
- Retain material superseded decisions, unique evidence and required exact history below a historical boundary. Do not archive each replaced opening or unchanged check.
- Reconcile current tracker summaries with that opening. Keep deferred work distinct from authorized execution.
- Keep changing execution state in one record. If a separate handoff is needed, Project memory points to it and records only project-wide changes.
- Link reusable accepted artifacts from their existing owner; do not create another lessons register.
- For a material recurring correction, record the owning code or template and its focused check here. Update a shared guide only for reusable judgment the implementation cannot enforce. Do not repeat unchanged lessons at each closeout.

## Required outputs

- Updated existing restart record when state changed. The repository’s `templates/session-handoff-template.md` supplies optional structure, not another file requirement.
- No additional record for a routine edit that leaves restart state unchanged.
- Exact restart command when work remains.

## Acceptance checks

- A new operator can locate the current action and exact evidence without reading the whole history.
- Prior states remain clearly historical; a routine edit does not create a new handoff file solely because AI assisted.
- Read only the current opening at restart, then follow evidence links needed for the selected action.
- Completed writing, analysis, graphics and delivery can have separate states. A future step is not a new assignment.
- The next action, if any, is singular and bounded. A completed task has no required next action.
- BLOCKs name a resume condition.

## Handoff requirements

The output is the handoff. Include verified state and limits, plus a next action and restart command when work remains. Otherwise state complete and awaiting a new request. Use the repository’s `examples/sample-handoff.md` when useful. Keep a standalone installed skill usable when that repository example is unavailable.

## Explicit limits

Do not summarize a private transcript into public material. Do not claim unverified work is complete. Do not overwrite durable knowledge with temporary notes.
