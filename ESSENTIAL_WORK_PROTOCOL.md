# Essential Work Protocol

Agent+ seeks the minimum sufficient evidence for a real decision.

## Necessity card

Before new work, complete [the essential task template](.planning/templates/ESSENTIAL-TASK.md).

| Field | Required answer |
| --- | --- |
| Decision | What decision can the result change? |
| Uncertainty | What material fact is unknown? |
| Existing evidence | Why is it insufficient? |
| Minimum action | What is the cheapest adequate check? |
| Unlock | What becomes possible if it closes? |
| Stop condition | What exact evidence ends the work? |
| Repeat trigger | What must change before repeating it? |
| Budget | What time, context, and attempts are authorized? |

## Decision test

If `PASS` and `BLOCK` lead to the same next action, do not start the task. It has no decision value.

## Evidence reuse

Reuse evidence while its claim, implementation, inputs, environment, and acceptance contract remain unchanged. New session context does not invalidate evidence.

## Proportionate verification

| Changed state | Minimum check |
| --- | --- |
| Markdown or planning text | Structure, links, and stated contract. |
| One implementation module | Narrow tests and static checks. |
| New immutable artifact | Exact ID, schema, hash, lineage, and counters. |
| Publication release | Release validation and fresh independent review. |

## BLOCK rule

A missing source, incomplete coverage, failed test, unauthorized action, or absent review is a typed `BLOCK`. Do not estimate around it or reinterpret it as a passing result.
