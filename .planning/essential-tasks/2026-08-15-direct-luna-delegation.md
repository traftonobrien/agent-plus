---
task: "Add direct Sol-to-Luna delegation to Agent+ defaults"
owner_role: "maker"
tier: "2"
time_budget: "30 minutes"
context_budget: "Agent+ routing files and bootstrap copies only"
attempt_limit: 2
---

# Essential Task Card

## Necessity

- **Decision:** Make direct model-selected delegation the Agent+ default when the owner asks for sub-agents or parallel work.
- **Uncertainty:** The current routing policy names Sol and Luna roles but does not say that Sol can create Luna sub-agents directly.
- **Existing evidence:** The active Codex delegation interface exposes `gpt-5.6-luna` with High and xhigh reasoning. The latest bounded model review also shows that Sol still handles more routine turns than the Luna-first policy intends.
- **Minimum action:** Update the canonical Agent+ workflow and project instructions plus their bootstrap copies.
- **Unlock:** Future Agent+ projects can use one Sol-managed task instead of manual cross-chat Luna handoffs.

## Boundary

- **Allowed artifacts:** `AGENTS.md`, `AI_WORKFLOW.md`, `bootstrap/base/AGENTS.md`, `bootstrap/base/AI_WORKFLOW.md`, `.planning/STATE.md`, `.claude-memory.md`, and this card.
- **Forbidden actions:** No model benchmark, sub-agent creation, recursive delegation, Git operation, or edit to existing dirty files.
- **Stop condition:** The canonical and bootstrap policies state the same direct-delegation route and pass deterministic text checks.
- **Repeat trigger:** Model access, rate, delegation support, or a bounded benchmark changes.
- **Acceptance:** Required routing phrases exist in all four policy surfaces and no unrelated file is changed by this task.

## Decision branches

- **If PASS:** Use direct Sol-to-Luna delegation when the owner explicitly requests it.
- **If BLOCK or FAIL:** Keep manual model selection and record the missing capability or policy conflict.

## Closeout

```yaml
decision_changed: yes
blocker_closed: manual_cross_chat_luna_handoff
work_unlocked: direct_bounded_luna_subagents
repeat_trigger: model_access_rate_delegation_or_benchmark_change
```
