# Astra workspace tuning

This guide describes instruction and context changes for an Astra-selected Codex session.
It does not establish faster execution, better research, or a release decision.

## Sources and scope

The official [Astra guidance](https://developers.openai.com/api/docs/guides/latest-model) recommends
checking conflicting instructions, autonomy, writing, delegation, and verification. The implementation
uses project-specific wording while retaining Agent+ authority and evidence rules.
The official [skill guide](https://learn.chatgpt.com/docs/build-skills) describes metadata and discovery.
The official [instruction guide](https://learn.chatgpt.com/docs/agent-configuration/agents-md) describes
instruction precedence and loading. Guidance was checked on 2026-09-04.

## Effective behavior

- Complete authorized work with the smallest adequate check and all required boundary checks.
- Resolve routine uncertainty from accessible evidence; ask when the missing answer changes the result.
- Keep authorization scoped. An outline does not authorize implementation; implementation does not authorize release.
- Treat new messages as steering. Preserve completed work and resume after answering side questions.
- Explain any skill-caused pause with its exact source and applicable instruction.

`AGENTS.md` owns task classification. `AI_WORKFLOW.md` owns model routes, formal stages, and budgets.
`ESSENTIAL_WORK_PROTOCOL.md` owns necessity, correction, and verification rules. Output policy owns
writing. Current state belongs in hot memory; past evidence remains in the planning history.

## Startup and discovery

`scripts/ai-context.sh` validates the existing startup seam and reads complete current records.
It emits instructions, output policy, memory, state, and explicit references to binding procedures.
Read the essential protocol for implementation; read the workflow for formal orchestration or model
assignment. Neither a reference nor omitted historical output makes a policy optional.

Do not truncate records at an arbitrary line number. Keep hot memory short and move superseded state
to an explicitly historical artifact. Preserve evidence bytes and unresolved holds. Consumer state
is project-owned and is never rewritten by a canonical update.

The canonical and bootstrap startup scripts share identical bytes. Optional memory/state remain
optional on the legacy route. A missing or unsafe required file prevents context output.
Native skill discovery uses regular-file mirrors of canonical skill directories in this repository.
The public validator requires complete byte and mode parity, including skill references and assets.
This keeps native discovery compatible with the existing regular-file release verifier.
Optional skill installation in consumers remains a separate release-pinned operation.

## Model and runtime settings

The owner-selected model has priority. The initial Codex tuning baseline is `gpt-6-astra` with high
reasoning. The host configuration already selected it. Lower-cost worker models keep their assigned
roles. A Claude session uses its selected Claude model. No rule silently changes a runtime model.

The default is zero delegated workers without authorization. Authorized work uses only useful
independent workers, one writer, and a fresh reviewer at the required boundary. Budgets are ceilings.
Do not spend capacity to satisfy a worker count or test count.

Record deliberately retrieved task context separately from runtime-injected instructions, cached
input, and accumulated tokens. Do not estimate exact usage from bytes. Native compaction and durable
handoffs support continued work. A cumulative threshold alone does not force restart.

If a future project implements an Astra API caller, check Responses tool calling, unsupported
sampling parameters, and current effort support in the official migration guide. Async tools,
mid-turn steering, and cache-preserving configuration changes need compatible runtime code.
This public package adds no API caller or custom harness to obtain those capabilities.

Host setup is documented in [Astra host setup](astra-host-setup.md). The package does not update
a user's CLI, model selection, global instructions, or role profiles automatically.

## Bounded comparison

Use the same task and acceptance contract for these arms:

1. Astra/high with prior instructions.
2. Astra/high with revised instructions.
3. Revised instructions with one changed reasoning setting, only after the first comparison.

Use prospective evidence. Record acceptance, unnecessary interruptions, elapsed time, tool calls,
retries, and reviewer corrections where observable. Missing usage remains unavailable. Retain failures.
A policy scenario review is not an actual coding run. Context-size reduction is not task-speed proof.
Use existing outcome-audit records only for runs fitting their closed schema; do not add schema fields
or fabricate maker/evaluator/reviewer events for a simple diagnostic.

The bounded scenario set covers routine maintenance, explanation-only scope, formal control edits,
model selection, unauthorized delegation, requested delegation, absent data authority, first-error
unattended execution, evaluator corrections, reviewer findings, skill selection, and resumed state.
Compare observed behavior before claiming a general gain. Independent review checks instruction
coherence and the implementation boundary; it does not certify Astra as the best model.

## Verification and rollout

Run focused startup tests, workflow checks, and existing lifecycle/legacy smoke coverage. The public
validator checks the integrated package, skill discovery, bootstrap bindings, privacy, and links.
Preserve independent review and exact release scope before publication. Consumer upgrades use the
transactional lifecycle from an accepted release. Tuning does not synchronize consumers automatically.
