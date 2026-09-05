# Project Instructions

## Purpose

This is an Agent+-managed baseball project. Keep the research question, evidence, and claim boundary explicit.

## Stable rules

1. Read this file, `.claude-memory.md`, and `.planning/STATE.md` before work.
2. Read `.agent-plus/PROJECT.md` for project-specific rules and authority.
3. Use `AI_WORKFLOW.md`, `AI_AGENT_OUTPUT_POLICY.md`, and `ESSENTIAL_WORK_PROTOCOL.md` as binding
   controls. Apply the output policy automatically for every response.
4. For a new research or product definition, if the decision is unclear, use `$agent-plus-discovery-grill` to maintain one
   `.planning/discovery/PROJECT-DISCOVERY.md` brief. Do not draft a contract until the owner confirms
   the final discovery synthesis.
5. Use deterministic checks for counts, schemas, hashes, tests, and metrics.
6. Separate maker, evaluator, verifier, and human decision roles.
7. Treat `PASS`, `NULL`, and `BLOCK` as valid outcomes.
8. Keep raw data, secrets, and runtime artifacts out of Git.
9. When the owner explicitly requests delegation or parallel work, the selected controller may directly create bounded,
   model-selected Luna sub-agents under `AI_WORKFLOW.md`; do not require manual cross-chat handoffs.
10. Engineering readiness reviews collect the complete reachable defect class before one bundled
   repair. A second BLOCK at the same interface forces simplification, not a third local patch.
11. Validate task and review packets with `scripts/anti_loop_guard.py` and the
   `.agent-plus/engineering-boundaries.json` ledger before promotion.
12. Select one bounded session mode (`quick`, `standard`, `deep`, or `scientific/live`) and apply
    its model, worker, context, time, and authorization limits. Extra capacity never grants
    authority, retries, context, reviewers, or promotion rights.
13. Keep successful recovery interfaces closed. Unattended execution uses one authorized launch,
    process-written durable evidence, zero AI polling, and one result check on return.
14. Route an owner-authorized multi-stage chain through one `.agent-plus/active-chain.json` capsule.
    Validate it before each stage and before closeout. The capsule references live authority files;
    it never copies scientific values, schemas, thresholds, or artifact identities.

## Task applicability

Carry the authorized task to its acceptance check. Read accessible evidence before asking for input.
Use a reasonable reversible default when uncertainty does not change the outcome. Existing authorization
persists within its scope. Prepare a concrete result before asking for any remaining required approval.
An explanation or outline request authorizes that deliverable, not implementation or publication.

- Routine reversible maintenance uses the changed file, command, focused check, and result as its record.
  It needs no formal chain, worker, research contract, or new permission prompt solely because AI assists.
- Shared controls, shared interfaces, substantive engineering, and promotion readiness use the task
  packet and registered boundary in `ESSENTIAL_WORK_PROTOCOL.md` and `AI_WORKFLOW.md`.
- Scientific, live, destructive, and release work retains its specific authorization and first-error stop.
- Fix routine mechanical defects and continue. Formal evaluator corrections use the single eligible
  small-correction rule. A reviewer BLOCK stops the chain and cannot authorize its own repair.
- After two failures at the same interface, use the existing simplification and ledger rules.

The user's current instruction takes precedence over skill guidelines, subject to platform rules.
If a skill causes a pause, identify its exact file, quote the rule, and explain why it applies.
Do not infer an approval requirement from a generic caution. Apply one matching skill by exact source.
Treat later user messages as task steering. Answer side questions and resume unless the task is replaced.

## Context and model routing

Run `scripts/ai-context.sh` once at startup. It prints complete instructions, current memory, and state.
Read the exact active artifact next. Read `ESSENTIAL_WORK_PROTOCOL.md` for implementation and verification,
and `AI_WORKFLOW.md` before model assignment, a formal chain, review, or unattended execution.
All three binding policy files remain authoritative even when the startup packet references them.
Do not reload unchanged context or archived history without a task-relevant reason.

Use the model explicitly selected by the owner or runtime. For an Astra-selected session, the controller
is `gpt-6-astra`; preserve the effective reasoning effort, with high as this tuning baseline.
Do not switch the controller to Sol because of an old template. Deterministic tools remain the first
choice for counts, hashes, and tests. Worker selection follows the authorized workflow.

## Context layers

- `AGENTS.md`: project-wide instructions.
- `CLAUDE.md`: Claude runtime profile.
- `.claude-memory.md`: current verified state only.
- `.agent-plus/PROJECT.md`: project-specific rules and authority.
- `.planning/`: active plans, reviews, and state.
- Obsidian Brain: durable curated knowledge.
- `handoffs/`: task-specific restart state.

## Output

Use basic everyday English first for state, progress, blocker, and current-work updates. Keep exact
technical records in a final `Technical details` section only when they are needed or requested.

## Closeout

Verify changed state proportionately. Update local memory and one handoff. State one exact next action and restart command.
