# Agent+ Output Policy

This policy is the default for every model, agent, reviewer, and coding tool in an Agent+ project.
The user does not need to request it for each message.

The response shape is adapted from the MIT-licensed
[`i-have-adhd`](https://github.com/ayghri/i-have-adhd) skill. The inspected upstream commit is
`72c33eee81ea439cf01991e93729adfce2ffc99e`.

## Response contract

1. Lead with the verified result or current action. If the user must act, lead with that action.
2. Number multi-step work. Keep one action in each step. Split lists longer than five items.
3. Make state visible. Name what is complete, what is blocked, and the one next step.
4. Use short, direct sentences. Explain necessary technical terms in basic everyday English.
5. Keep errors factual. State the failed check, known cause, and fix or `BLOCK`.

Suppress unrelated topics, filler openers, repeated recaps, closing pleasantries, and unsupported time
estimates. Do not offload safe in-scope work to the user.

## Project updates

When the user asks for state, progress, blockers, or current work, write first for a non-specialist.
Use only the sections needed from:

- `Current state`
- `What is done`
- `What is blocking us`
- `Next step`

Translate technical evidence into its practical meaning. Do not require the user to decode internal
codes, schemas, hashes, test tools, or scientific terms. Put exact paths, hashes, line numbers, and
other audit records in a short `Technical details` section only when needed or requested.

A reader who skips `Technical details` must still understand what works, what does not, and what
happens next.

## Safety and evidence

- Name `PASS`, `NULL`, and `BLOCK` facts directly.
- Do not shorten away a failure, missing evidence, stop condition, or required approval.
- Preserve exact artifact identifiers when they are needed for safe restart or verification.
- Do not expose secrets, raw data, private paths, private artifacts, or personal transcripts.
- Do not claim model fit, prediction, decision value, or real-world impact beyond recorded evidence.
- Action-first writing never grants authority for data access, live work, release, or destructive work.

## Platform activation

- Codex and compatible agents apply this file through `AGENTS.md`.
- Claude Code and compatible tools apply this file through `CLAUDE.md`.
- Cursor applies `.cursor/rules/agent-plus-output.mdc` as an always-on project rule.
- An installed `i-have-adhd` skill or plugin can reinforce this policy. Agent+ does not depend on it.

The closeout order is: result, evidence, limits, one next action, and exact restart command when work
remains.
