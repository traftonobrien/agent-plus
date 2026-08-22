# Claude Runtime Profile

Start with `scripts/ai-context.sh`. Read only the exact plan, evidence record, review, or handoff named by `.claude-memory.md`.

Apply `AI_AGENT_OUTPUT_POLICY.md` automatically. An external output-style plugin is optional.

- When no research contract exists, decide whether the idea is contract-ready. Route unclear ideas
  to `$agent-plus-discovery-grill`; do not turn discovery completion into contract acceptance or work
  authorization.
- Use deterministic tools before model reasoning.
- Make one bounded artifact per task.
- Follow the tier and authority limits in `AI_WORKFLOW.md`.
- Select one mode (`quick`, `standard`, `deep`, or `scientific/live`) before dispatch. Extra
  capacity changes bounded throughput only; it never changes authority, context, retries, reviewer
  count, or owner authorization.
- For engineering, explore independently, freeze the evidence handoff, then use one exclusive
  maker, deterministic evaluator, fresh verifier, and Sol synthesis. Stop on `BLOCK`; do not
  auto-repair after a reviewer `BLOCK`.
- Stop after two failed attempts and write a typed `BLOCK`.
- Do not self-certify or promote a scientific claim.
