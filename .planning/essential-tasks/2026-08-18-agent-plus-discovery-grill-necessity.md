---
task: "Add a voice-friendly, stateful discovery grill to the Agent+ public workflow"
owner_role: "maker"
tier: "1"
time_budget: "60 minutes"
attempt_limit: 2
orchestration_mode: "standard"
exact_model: "Sol maker; deterministic validators; fresh review remains separate"
reasoning: "implementation"
authorization_scope: "Create the public Agent+ skill, install a matching local copy, and install the unchanged upstream grill-me dependency"
ownership_map: "Sol writes and validates; owner decides public release; fresh reviewer decides acceptance"
chain_stages: "inspect upstream -> define boundary -> implement -> deterministic validation -> handoff"
concurrency: "one writer; no delegated workers"
tool_budget: "bounded local and upstream inspection plus repository validators"
context_budget: "active Agent+ controls and the selected upstream skills only"
reserve_use: "not used"
checkpoint_interval: "validate after implementation"
overnight: "no"
evaluator_commands: "skill quick validation and bash scripts/validate-public-package.sh"
fresh_verifier_contract: "Review attribution, trigger behavior, artifact safety, voice flow, and contract gate without relying on maker conclusions"
---

# Essential Task Card

## Necessity

- **Decision:** Whether Agent+ can turn an early project idea into a resumable, contract-ready problem definition without treating a chat transcript as project state.
- **Uncertainty:** The current workflow begins at the research-contract boundary but does not provide a voice-friendly discovery interview that saves settled decisions as they land.
- **Existing evidence:** Matt Pocock's `grill-me` provides the interview primitive, while Agent+ already provides the downstream contract and authority gates; neither alone provides the combined handoff.
- **Minimum action:** Install the unchanged upstream `grill-me` and `grilling` skills, then add one attributed Agent+ orchestration skill with one discovery artifact template.
- **Unlock:** Consumers can start a new baseball project conversationally and finish with an explicit route to contract, prototype, evidence gathering, scope split, or BLOCK.

## Boundary

- **Allowed artifacts:** `skills/agent-plus-discovery-grill/**`, `docs/integrated-tools.md`, `README.md`, the matching local skill folder, and this task card.
- **Allowed actions:** Inspect and install the named upstream skills, create the Agent+ derivative, document it, and run deterministic validation.
- **Forbidden actions:** Commit, push, tag, release, copy private transcripts, change scientific authority, or begin substantive baseball analysis.
- **Review mode:** engineering sweep
- **Failure-class coverage:** Trigger clarity, upstream attribution, voice interaction, incremental persistence, resume behavior, privacy, exit states, and research-contract handoff.
- **Simplification trigger:** If the skill needs a second state file or a transcript log, reduce it to one decision artifact before review.
- **User-visible outcome:** A consumer can invoke one Agent+ skill, answer one question at a time by voice or text, and resume from a durable decision record.
- **Stop condition:** Skill validation and public-package validation pass, or a named validation/contract defect is recorded as BLOCK.
- **Stop behavior:** Collect the complete named engineering matrix before repair.
- **Attack matrix:** Contract inspection covers stateless/original separation, new repo, interrupted session, unknown answer, evidence-dependent question, prototype-dependent question, scope split, and private-detail omission; fresh behavioral review remains pending.
- **Named coverage:** Attribution, single-file persistence, no raw transcript, typed exits, no automatic analysis authority, and restart path are present and deterministically validated; fresh behavioral review remains pending.
- **Repeat trigger:** Skill or integration documentation changes after validation.
- **Acceptance:** The local and public skill copies match; quick validation passes; the public-package validator passes; no commit or release claim is made.

## Decision branches

- **If PASS:** Prepare the skill and validation receipts for fresh review before any public release.
- **If BLOCK or FAIL:** Keep the current Agent+ contract-first entry point and revise the smallest failed interface.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: fresh independent behavioral and integration review
user_visible_outcome: voice-friendly project discovery with a resumable decision brief
repeat_trigger: reviewer defect or skill and integration documentation changes
```
