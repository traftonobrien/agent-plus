# Claude Runtime Profile

Claude works under the project-wide rules in `AGENTS.md`.
Apply `AI_AGENT_OUTPUT_POLICY.md` automatically. An external output-style plugin is optional.

## Runtime boundary

- Start with `scripts/ai-context.sh`.
- Read `.claude-memory.md` for current verified state.
- Read the exact named plan, contract, evidence record, review, or handoff. Do not infer state from a full transcript.
- Use deterministic tools before model reasoning when a fact can be counted, hashed, tested, or parsed.
- Complete the requested bounded deliverable. Apply the task classification in `AGENTS.md`.
- Use the actually selected Claude model in this runtime. Astra is a Codex profile, not a Claude model.
- Do not self-certify work that requires an independent review.
- Select one mode (`quick`, `standard`, `deep`, or `scientific/live`) before dispatch. Extra
  capacity changes bounded throughput only; it never changes authority, context, retries, reviewer
  count, or owner authorization.
- For engineering, explore independently, freeze the evidence handoff, then use one exclusive
  maker, deterministic evaluator, fresh verifier, and controller synthesis. Use the formal evaluator small-correction rule where eligible; otherwise stop on `BLOCK`. Do not
  auto-repair after a reviewer `BLOCK`.
- Stop after two failed attempts and write a `BLOCK` with the missing evidence.

## Output boundary

Return: outcome, evidence, limits, next action, and restart reference. Do not expose sensitive material in public output.
