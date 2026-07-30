# Claude Runtime Profile

Claude works under the project-wide rules in `AGENTS.md`.

## Runtime boundary

- Start with `scripts/ai-context.sh`.
- Read `.claude-memory.md` for current verified state.
- Read the exact named plan, contract, evidence record, review, or handoff. Do not infer state from a full transcript.
- Use deterministic tools before model reasoning when a fact can be counted, hashed, tested, or parsed.
- Make one bounded artifact per task. Do not self-certify it.
- Stop after two failed attempts and write a `BLOCK` with the missing evidence.

## Output boundary

Return: outcome, evidence, limits, next action, and restart reference. Do not expose sensitive material in public output.
