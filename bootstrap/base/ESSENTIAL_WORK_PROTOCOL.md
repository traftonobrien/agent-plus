# Essential Work Protocol

Agent+ seeks the minimum sufficient evidence for a real decision.

## Applicability

Use the task classification in `AGENTS.md`. A read-only answer or routine reversible maintenance
does not require a formal packet, independent worker, or research contract. A change to shared
controls, shared interfaces, scientific meaning, authority, or promotion uses the formal route.
Routine autonomy never changes a scientific or release boundary.

## Necessity card

Before substantive, scientific, irreversible, promotion, or release work, complete [the essential
task template](.planning/templates/ESSENTIAL-TASK.md). Routine reversible work uses its changed file,
command, focused check, and result as the local record.

| Field | Required answer |
| --- | --- |
| Decision | What decision can the result change? |
| Uncertainty | What material fact is unknown? |
| Existing evidence | Why is it insufficient? |
| Minimum action | What is the cheapest adequate check? |
| Unlock | What becomes possible if it closes? |
| Stop condition | What exact evidence ends the work? |
| Repeat trigger | What must change before repeating it? |
| Budget | What time, context, and attempts are authorized? |

## Decision test

If `PASS` and `BLOCK` lead to the same next action, do not start the task. It has no decision value.

## Prior evidence disposition

Before creating a definition, method, or implementation, search the accessible accepted work that
could answer the same question. Bind the search to the relevant source identity, semantic component,
and implementation surface. Do not rely on project names or a new session boundary to decide that
earlier evidence is unrelated.

Record each relevant component with exactly one disposition:

- `REUSE_IDENTICAL`: the claim, inputs, meaning, implementation, environment, and acceptance contract
  match the current use.
- `REUSE_WITH_TASK_DELTA`: an accepted component transfers, while the current task separately owns a
  changed population, denominator, output, or other named decision.
- `CONFLICT_REVIEW`: source identity, meaning, implementation, or accepted evidence differs and must be
  reconciled before reuse or replacement.
- `NOT_APPLICABLE`: no relevant accepted component exists, or the inspected component does not answer
  the current question. Record the search basis instead of silently starting from scratch.

Reuse of a component never transfers another task's permissions, acceptance receipts, task status, publication
decision, or release authority. A rule against inheriting task authority does not
justify recreating an accepted source-bound definition or implementation. When the search finds a
match, state the reusable component and the task-owned delta before new work begins.

This prevents automatic transfer of authority or acceptance. It does not prohibit reusing a saved table or
accepted result as evidence or input. Confirm that source, population, definitions and recorded limits fit
the new use. Cite the existing accepted evidence and identify the actual task-specific gap before rebuilding.
Applicable standing authorization is not revoked by a new chat.

### Learning from completed work

Record accepted results, reusable artifact locations and relevant limits in the existing task handoff.
Link newly accepted reusable artifacts from their existing owning index at closeout. Update the existing
procedure when an owner correction or repeated failure demonstrates a reusable lesson, within current
authority and with the applicable shared-control review. Task-specific observations stay in the handoff.
At the next related task, retrieve those owners and compatible accepted work before planning new work.
Do not create another lessons register or require every old transcript as startup context.

## Implementation subtraction ladder

After tracing the affected flow and before adding code, stop at the first adequate option:

1. Does this need to exist?
2. Does an accepted implementation already exist in the repository?
3. Does the standard library provide the required behavior?
4. Does a native platform feature provide it?
5. Does an already-installed dependency provide it?
6. If none applies, what is the smallest correct implementation for the named consumer?

This ladder never removes required validation, security, accessibility, data-loss protection,
scientific controls, or a requested acceptance check. A small change in an untraced location is not
simplification. Prefer deletion, reuse, and boring code only after the real call path is understood.

This control adapts Dietrich Gebert's MIT-licensed
[`DietrichGebert/ponytail`](https://github.com/DietrichGebert/ponytail) decision ladder. The inspected
upstream commit is
[`2ed6c52c9d7e5e56942508591085fd45dea277d3`](https://github.com/DietrichGebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3).

### Lean R migration rule

Port complete accepted behavior, not only visible labels or final counts. Trace exclusions,
missing and unknown values, exceptional cases, and downstream consumers before claiming parity.
Test the dominant operation on representative volume before a long run; use vectorized operations
and joins for large tables. Cache expensive stable stages separately from cheap, frequently changed
targets so a downstream correction does not repeat upstream computation.

Before an expensive target run, inspect the exact dependency graph and record which named targets
are current or outdated. Run the smallest named target that can reach the decision endpoint. Reuse
current expensive ancestors and reject a broad rebuild when only a cheap downstream target changed.
Treat a downstream reset as a new failure class only when deterministic graph evidence proves it
cannot reach the exhausted upstream interface.

Before expensive execution, test shared helpers with tiny known-answer cases for scalar, vector, grouped, and missing-value behavior when applicable.
Test signed endpoints and repeated transformations when applicable. Retain the regression that exposed a defect through refactoring or simplification.
Use the existing focused test path. Do not create a second analytical pipeline for review.

Keep historical reconstruction separate from the normal entry point when it is not a current dependency.
Name the current run, accepted result, and reconstruction owner in the existing task card.
This guidance does not authorize changing accepted membership or scientific definitions.

Preserve failed attempts alongside the eventual result. Record their causal failure code, measured
duration when available, and the correction or simplification that changed the outcome. Use the
existing outcome audit when prospective rates are needed; do not create a second metrics ledger.

### Complexity is a diagnostic

Use high cyclomatic complexity or deeply nested branching as a prompt to simplify the real decision
flow. Prefer fewer states, combined equivalent predicates, table-driven rules, and direct data
transformations when they make behavior clearer. A lower score is useful only when focused tests
preserve behavior and the resulting code is easier to follow.

Do not impose one universal numeric threshold, add a dependency only to produce the score, or split
the same branching across meaningless helpers to satisfy a lint rule. Complexity is evidence for
subtraction, not proof of correctness or quality.

## Falsifier and question rule

Before dispatch, name the furthest authorized decision-relevant endpoint and one fact that would
invalidate the proposed path. Inspect accessible evidence instead of asking. Ask only when two
plausible answers require materially different actions and a cheap lookup cannot resolve the fact.
Otherwise choose the smallest reversible default and record it in the active task.

Bind the actual question, requested population, output mode, and excluded work in the existing task card.
Supporting cues and skill requirements do not create another assignment or expand authority.
Reference an accepted contract instead of restating its answers. Apply only relevant fields to descriptive work and ordinary documents.

Before analytical implementation, resolve units, sign convention, row grain, metric type, endpoint transformations, and source availability.
Keep observed ranges separate from selection rules and geometric regions separate from recorded events.
These definitions belong in the accepted contract or project adapter. Arithmetic checks alone cannot establish their meaning.

Use one fresh verifier at the promotion boundary. Do not add recursive builder-critic rounds,
sentence-level provenance tags, or phase-by-phase critique unless the task names a distinct risk
that the existing evaluator and verifier cannot test.

## Engineering closure rule

Use [AI Workflow](<AI_WORKFLOW.md#engineering-closure-and-review>) for formal diagnosis, bundled correction, reviewer BLOCK, simplification and registered-ledger admission.
That owner also controls complete read-only defect collection, fixed input namespaces, cumulative history and the single promotion dossier. An engineering result must unlock its named user-visible or scientific endpoint.

### Continuous repair default

Use the [AI Workflow repair rule](<AI_WORKFLOW.md#continuous-repair-default>) for routine maintenance and the eligible formal-evaluator correction. This route does not grant scientific/live execution, source access, review acceptance or another consumed attempt.

## Interface-consumer closure

When a task changes a shared function signature, type, tuple shape, schema, serialized field,
exported constant, callback, or return object, its changed surface includes every repository
consumer of that interface, even when the consumer file itself did not change. Runtime wrappers,
diagnostics, launchers, serializers, monkeypatches, and monitoring code are consumers, not optional
observability.

Before promotion, the maker must produce one closed interface-consumer receipt and validate it with
`scripts/interface_consumer_guard.py`. The receipt names deterministic search tokens and roots,
classifies every discovered consumer, and binds each consumer to an acceptance check. Omission is a
`BLOCK`; an unchanged file is not proof that it is unaffected.

Any dynamically patched or weakly typed consumer must also receive one real-shape smoke test through
the operational path. Broad unit suites and static checks do not replace that test when `Any`,
reflection, monkeypatching, a subprocess, or a serialization boundary prevents type checking from
seeing the interface. Run this smoke test before production-scale, overnight, live, or destructive
work.

## Higher-capacity routing boundary

Use [AI Workflow session modes](<AI_WORKFLOW.md#bounded-session-modes>) and [capacity limits](<AI_WORKFLOW.md#capacity-and-context-limits>) for model selection, budgets, bounded waits, exclusive writes and the active-chain capsule.
Extra capacity changes throughput only. It grants no extra authority, retries, reviewers, context or promotion rights. The same owner governs overnight scope and queue limits.

## Unattended execution rule

Use [AI Workflow](<AI_WORKFLOW.md#attempt-boundary-and-pre-attempt-correction>) for scientific/live attempt-start and correction limits, and its [unattended execution](<AI_WORKFLOW.md#unattended-execution>) section for one launch, process-written evidence, zero AI polls and one return check.
A failed or missing result does not grant another launch. The workflow's [capacity rules](<AI_WORKFLOW.md#capacity-and-context-limits>) own the premium reserve and model-review cadence. Scientific, source, human and release authority stay separate.

## Evidence reuse

Reuse evidence while its claim, implementation, inputs, environment, and acceptance contract remain unchanged. New session context does not invalidate evidence.

Live policy, contracts, code, and deterministic evidence outrank memory, planning state, the Brain,
and transcripts. These context layers route work but do not grant authority. Reference live
authority files instead of copying their values into a task packet or chain capsule.

## Proportionate verification

| Changed state | Minimum check |
| --- | --- |
| Markdown or planning text | Structure, links, and stated contract. |
| One implementation module | Narrow tests and static checks. |
| New immutable artifact | Exact ID, schema, hash, lineage, and counters. |
| Publication release | Release validation and fresh independent review. |

After adequate checks pass, broaden or repeat only for changed evidence or an unresolved concern.
Do not add tests that merely mirror a reversible low-impact edit. Required boundary checks still apply.

## BLOCK rule

A missing source, incomplete coverage, failed test, unauthorized action, or absent review is a typed `BLOCK`. Do not estimate around it or reinterpret it as a passing result.

## Upstream MIT notice for the subtraction ladder

Copyright (c) 2026 DietrichGebert

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
