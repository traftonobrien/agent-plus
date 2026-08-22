---
task: "<bounded deliverable>"
owner_role: "maker | evaluator | verifier"
tier: "0 | 1 | 2 | 3"
time_budget: "<minutes>"
attempt_limit: 2
orchestration_mode: "quick | standard | deep | scientific/live"
exact_model: "<controller, explorers, maker, evaluator, reviewer>"
reasoning: "<routine | implementation | premium | scientific>"
authorization_scope: "<owner command and permitted boundary>"
ownership_map: "<controller, workers, writer, evaluator, verifier, owner>"
chain_stages: "<ordered stages and sequential boundary>"
concurrency: "<worker count, parallel stages, writer rule>"
tool_budget: "<per-role calls and wall time>"
context_budget: "<ordinary/premium ceilings and target>"
reserve_use: "<25% premium reserve decision or not used>"
checkpoint_interval: "<wait/checkpoint rule>"
overnight: "no | explicit owner mode with limits"
unattended_execution: "no | one authorized launch"
unattended_command: "<exact command or not-applicable>"
durable_evidence: "<progress path and terminal path or not-applicable>"
return_check: "<one check after return or not-applicable>"
polling_policy: "zero AI polls while running or not-applicable"
evaluator_commands: "<exact deterministic commands>"
fresh_verifier_contract: "<independent inputs, attack matrix, and stop rule>"
promotion_dossier: "<one stable boundary dossier path updated in place>"
anti_loop_packet: "<planned packet path and guard PASS receipt>"
review_closeout: "<completed packet path and closeout guard PASS receipt>"
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
- **Allowed actions:** `<actions explicitly permitted>`
- **Forbidden actions:** `<actions explicitly forbidden>`
- **Review mode:** `<engineering sweep | scientific/live first-error gate>`
- **Failure-class coverage:** `<interface and adjacent invariants the run must exhaust>`
- **Simplification trigger:** `<state that forbids another local patch>`
- **User-visible outcome:** `<result enabled, not tests or process files>`
- **Stop condition:** `<PASS or BLOCK evidence>`
- **Stop behavior:** `<collect named engineering matrix | stop at first error>`
- **Attack matrix:** `<cases and complete/pending status for a review>`
- **Named coverage:** `<invariants and complete/pending status for a review>`
- **Promotion dossier:** `<one stable contract, cumulative matrix, receipt, and review location>`
- **Dispatch guard:** `<registered ledger boundary plus planned-packet PASS receipt>`
- **Review closeout guard:** `<complete-matrix PASS receipt required before another maker>`
- **Changed interfaces:** `<exact symbols, signatures, tuple shapes, schemas, callbacks, or return objects; none if not applicable>`
- **Consumer discovery:** `<receipt path plus deterministic search roots and tokens; not-required only when no interface changed>`
- **Consumer closure:** `<every discovered production, wrapper, diagnostic, launcher, serializer, test, and documentation consumer with disposition>`
- **Runtime wrappers:** `<dynamic patches, Any-typed adapters, subprocesses, reflection, or none>`
- **Real-shape smoke:** `<exact operational fixture command and receipt; required for dynamic or weakly typed consumers>`
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
user_visible_outcome: <result enabled, not tests or process files>
repeat_trigger: <exact changed state>
```
