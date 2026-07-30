# Project Instructions

## Purpose

This is an Agent+-managed baseball project. Keep the research question, evidence, and claim boundary explicit.

## Stable rules

1. Read this file, `.claude-memory.md`, and `.planning/STATE.md` before work.
2. Use `AI_WORKFLOW.md` and `ESSENTIAL_WORK_PROTOCOL.md` as binding controls.
3. Use deterministic checks for counts, schemas, hashes, tests, and metrics.
4. Separate maker, evaluator, verifier, and human decision roles.
5. Treat `PASS`, `NULL`, and `BLOCK` as valid outcomes.
6. Keep raw data, secrets, and runtime artifacts out of Git.

## Context layers

- `AGENTS.md`: project-wide instructions.
- `CLAUDE.md`: Claude runtime profile.
- `.claude-memory.md`: current verified state only.
- `.planning/`: active plans, reviews, and state.
- Obsidian Brain: durable curated knowledge.
- `handoffs/`: task-specific restart state.

## Closeout

Verify changed state proportionately. Update local memory and one handoff. State one exact next action and restart command.
