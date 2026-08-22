---
task: "Add reusable interface-consumer closure controls"
owner_role: "maker"
tier: "2"
time_budget: "4 hours"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Codex maker; deterministic evaluator; fresh reviewer later"
reasoning: "implementation"
authorization_scope: "Agent+ engineering only; no release"
ownership_map: "one maker writes canonical and bootstrap copies; evaluator runs public validation; fresh reviewer is separate"
chain_stages: "audit, make, evaluate, handoff"
concurrency: "one writer"
tool_budget: "bounded implementation and one package validation"
context_budget: "under ordinary ceiling"
reserve_use: "preserved"
checkpoint_interval: "after generic validator and after consumer integration"
overnight: "no"
evaluator_commands: "unit tests and scripts/validate-public-package.sh"
fresh_verifier_contract: "review generic policy, template, validator, synthetic attacks, and downstream adapter together"
---

# Essential Task Card

## Necessity

- **Decision:** Whether Agent+ can require proof that every consumer of a changed interface was considered before expensive integration work.
- **Uncertainty:** The current task card names a changed surface but does not close runtime wrappers, diagnostics, launchers, or other unchanged consumers.
- **Existing evidence:** A proving project changed a checkpoint-key shape while an untyped rehearsal wrapper retained the old shape and failed only after a full-volume run.
- **Minimum action:** Add a closed consumer-closure receipt, deterministic validator, synthetic attacks, and required task-card fields.
- **Unlock:** Consumer projects can block missing operational consumers before expensive rehearsals.

## Boundary

- **Allowed artifacts:** Agent+ protocol, canonical/bootstrap task templates, new generic validator/example, tests, and public validator wiring.
- **Allowed actions:** Public-safe generic implementation and deterministic validation.
- **Forbidden actions:** Project evidence, private paths, scientific rules, release, commit, push, tag, or announcement.
- **Review mode:** engineering sweep.
- **Failure-class coverage:** omitted direct consumer, diagnostic wrapper, launcher, serializer, test seam, bad disposition, missing real-shape smoke receipt, and path substitution.
- **Simplification trigger:** one integrated review BLOCK requires completing the same matrix; a second requires replacing the receipt interface.
- **User-visible outcome:** interface changes cannot be declared review-ready while a discovered consumer is omitted.
- **Stop condition:** unit tests and public-package validation PASS with canonical/bootstrap parity.
- **Stop behavior:** collect the complete named validator failure class.
- **Attack matrix:** missing consumer, extra undeclared hit, unknown fields, malformed paths, absent smoke, failed smoke, non-deterministic ordering.
- **Named coverage:** protocol, template, validator, example, bootstrap, package validator.
- **Repeat trigger:** validator or packet schema changes.
- **Acceptance:** focused unittest discovery plus `scripts/validate-public-package.sh`.

## Decision branches

- **If PASS:** Send the reusable control and proving-project adapter to one fresh integrated reviewer.
- **If BLOCK or FAIL:** Keep Agent+ unreleased and report the smallest incomplete interface.

## Closeout

```yaml
decision_changed: yes
blocker_closed: interface-consumer-closure-maker
work_unlocked: fresh integrated review
user_visible_outcome: omitted runtime consumers fail before expensive execution
repeat_trigger: implementation, inputs, or receipt schema changes
```
