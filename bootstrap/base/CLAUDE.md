# Claude Runtime Profile

Start with `scripts/ai-context.sh`. Read only the exact plan, evidence record, review, or handoff named by `.claude-memory.md`.

- Use deterministic tools before model reasoning.
- Make one bounded artifact per task.
- Follow the tier and authority limits in `AI_WORKFLOW.md`.
- Stop after two failed attempts and write a typed `BLOCK`.
- Do not self-certify or promote a scientific claim.
