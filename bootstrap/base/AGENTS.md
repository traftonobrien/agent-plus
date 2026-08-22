# Project Instructions

## Purpose

This is an Agent+-managed baseball project. Keep the research question, evidence, and claim boundary explicit.

## Stable rules

1. Read this file, `.claude-memory.md`, and `.planning/STATE.md` before work.
2. Read `.agent-plus/PROJECT.md` for project-specific rules and authority.
3. Use `AI_WORKFLOW.md`, `AI_AGENT_OUTPUT_POLICY.md`, and `ESSENTIAL_WORK_PROTOCOL.md` as binding
   controls. Apply the output policy automatically for every response.
4. If the project decision is unclear, use `$agent-plus-discovery-grill` to maintain one
   `.planning/discovery/PROJECT-DISCOVERY.md` brief. Do not draft a contract until the owner confirms
   the final discovery synthesis.
5. Use deterministic checks for counts, schemas, hashes, tests, and metrics.
6. Separate maker, evaluator, verifier, and human decision roles.
7. Treat `PASS`, `NULL`, and `BLOCK` as valid outcomes.
8. Keep raw data, secrets, and runtime artifacts out of Git.
9. When the owner explicitly requests delegation or parallel work, Sol may directly create bounded,
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
