---
task: "<bounded deliverable>"
owner_role: "maker | evaluator | verifier"
tier: "0 | 1 | 2 | 3"
time_budget: "<minutes>"
context_budget: "<maximum inputs>"
attempt_limit: 2
---

# Essential Task Card

## Necessity

- **Decision:** `<decision that can change>`
- **Uncertainty:** `<unknown fact>`
- **Existing evidence:** `<why insufficient>`
- **Minimum action:** `<cheapest adequate action>`
- **Unlock:** `<concrete next work>`

## Boundary

- **Allowed artifacts:** `<exact paths or IDs>`
- **Forbidden actions:** `<actions>`
- **Stop condition:** `<PASS or BLOCK evidence>`
- **Repeat trigger:** `<required state change>`
- **Acceptance:** `<command or rubric>`

## Decision branches

- **If PASS:** `<next action>`
- **If BLOCK or FAIL:** `<different next action>`

If both branches are the same, reject the task.

## Closeout

```yaml
decision_changed: yes | no
blocker_closed: <ID or none>
work_unlocked: <next action or none>
repeat_trigger: <exact changed state>
```
