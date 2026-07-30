# Agent+ AI Workflow

This is the binding public workflow for Agent+. It mirrors the control structure of a production research program without exposing private project state.

## Operating rule

Use deterministic tools first. Give AI systems narrow, reviewable assignments. Human scientific judgment owns research claims and promotion decisions.

## Routing matrix

| Tier | Use | Required control | Cannot certify |
| --- | --- | --- | --- |
| 0 | Search, parse, count, hash, validate, test, score. | Record exact command or artifact. | Narrative conclusion. |
| 1 | Reversible extraction, classification, summary, and drafting. | Human or deterministic check. | Data coverage, scientific safety, or promotion. |
| 2 | Bounded implementation and integration. | Named acceptance check. | Its own work. |
| 3 | Leakage, hard architecture, adversarial, or fresh review. | Independent context and changed evidence. | Deterministic evidence or human decision. |

## Task packet

Each task identifies the decision, uncertainty, allowed inputs, permitted actions, time and context budget, attempt limit, stop condition, acceptance check, and handoff owner. Use [the essential task template](.planning/templates/ESSENTIAL-TASK.md).

## Role separation

- The maker creates one bounded artifact.
- The evaluator runs deterministic checks.
- The fresh verifier assesses changed evidence independently.
- The human owner accepts, narrows, defers, or blocks the resulting claim.

No model self-certifies. No model silently changes its tier or falls back to another model.

## Context and memory

Start with `scripts/ai-context.sh`. Read the exact planning artifact named by `.claude-memory.md`. Do not load private transcripts or broad history by default. Use `.claude-memory.md` for current verified state and the Obsidian Brain for durable curated knowledge.

## Stop rules

- Stop after two failed attempts and record `BLOCK`.
- Do not repeat unchanged evidence merely because a new session starts.
- Do not advance past a contract, coverage, temporal-order, or verification gate.
- Treat `PASS`, `NULL`, and `BLOCK` as valid outcomes.
