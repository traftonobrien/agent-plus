# Session Handoff — Template

Update the current task’s existing handoff. An existing local memory file can serve as this record. Keep the latest verified state and next action first. When a separate handoff exists, project memory links here instead of copying changing task state. Replace this opening as work changes. Keep it short enough to resume without reading the history. Reconcile any current tracker summary. Omit fields that do not apply.

When no work remains, state complete and awaiting a new request. Do not invent work or repeat unchanged passing checks solely to fill a handoff. The next-action and restart fields are optional for a completed task.

## Verified state

- Completed artifact: `[path or ID]`
- Verification performed: `[tested revision, exact command, result and material untested behavior; link existing evidence]`
- Completed lanes and accepted choices: `[what stays closed]`
- Deferred work: `[what is waiting and why, or none]`

## Limits and BLOCKs

- Open limit: `[limit]`
- BLOCK: `[ID and reason, or none]`
- Forbidden next actions: `[actions]`

## Next action

- One bounded next action: `[action when work remains, or none; task complete]`
- Required inputs: `[files or identifiers]`
- Acceptance check: `[check]`

## Restart

`[exact command]`

## Historical records

Dated decisions and evidence links belong below this boundary. Their old statuses and next actions
are historical, not current instructions. Keep material decisions, unique evidence and required
exact history. Do not archive every replaced opening or add an entry for each unchanged check or minor edit.
