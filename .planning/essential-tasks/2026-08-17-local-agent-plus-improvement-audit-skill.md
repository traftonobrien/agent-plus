---
task: "Create a local skill that audits proving projects for reusable Agent+ improvements"
owner_role: "maker"
tier: "2"
time_budget: "60 minutes"
attempt_limit: 2
orchestration_mode: "standard"
exact_model: "Sol maker; deterministic skill validator and scanner tests"
reasoning: "implementation"
authorization_scope: "Owner requested a local Codex skill that scans a named repository for Agent+ system improvements"
ownership_map: "Sol owns the local skill; deterministic scripts evaluate; owner decides whether any proposed update proceeds"
chain_stages: "define interface -> initialize skill -> implement scanner and workflow -> deterministic validation -> closeout"
concurrency: "zero workers; one writer"
tool_budget: "32 calls or 60 minutes"
context_budget: "25K ceiling; 8K-15K target"
reserve_use: "not used"
checkpoint_interval: "one checkpoint after deterministic validation"
overnight: "no"
evaluator_commands: "skill quick validator; scanner positive and negative fixture tests"
fresh_verifier_contract: "required only before the skill promotes or applies an Agent+ system update"
---

# Essential Task Card

## Necessity

- **Decision:** Decide whether a named proving repository contains reusable Agent+ improvements.
- **Uncertainty:** Project-specific controls and generic Agent+ improvements are not consistently separated.
- **Existing evidence:** The upstream rule exists, but no reusable audit skill performs the classification.
- **Minimum action:** Create one read-only-by-default local skill with a deterministic surface inventory.
- **Unlock:** Future repository audits can produce bounded, sanitized Agent+ update proposals.

## Boundary

- **Allowed artifacts:** Local Codex skill files and named repository workflow surfaces.
- **Allowed actions:** Create the skill, scan metadata and hashes, validate structure, and test fixtures.
- **Forbidden actions:** Scan baseball data, copy private state, edit a target repository during audit, commit, push, publish, or promote an update.
- **Review mode:** Engineering sweep.
- **Failure-class coverage:** Source resolution, applicable instructions, surface inventory, classification, privacy exclusion, drift, and typed BLOCK behavior.
- **Simplification trigger:** If classification needs repository-specific code, keep it as evidence for human review instead of adding automatic promotion logic.
- **User-visible outcome:** One commandable skill can audit a named repository for Agent+ improvement candidates.
- **Stop condition:** Skill validation and scanner fixtures pass, or one named interface remains `BLOCK`.
- **Stop behavior:** Collect the complete named audit matrix.
- **Attack matrix:** Valid repository, missing repository, non-Git repository, private-data exclusion, exact copy, divergent copy, and project-only surface.
- **Named coverage:** Trigger, canonical source, target source, read-only default, classification, output contract, and update authorization.
- **Repeat trigger:** Real-use failure, new Agent+ surface class, or changed upstream contract.
- **Acceptance:** The skill validator passes and the scanner returns stable JSON for representative fixtures.

## Decision branches

- **If PASS:** Use the skill on SECOND LOOK in a separate read-only audit.
- **If BLOCK or FAIL:** Do not use the skill for an Agent+ update until the named interface is corrected.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: read-only SECOND LOOK system-improvement audit
user_visible_outcome: local Codex skill can inventory and classify Agent+ improvement candidates
repeat_trigger: changed skill implementation, new surface class, or real-use finding
```
