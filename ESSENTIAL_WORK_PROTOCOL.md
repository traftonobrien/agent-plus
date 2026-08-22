# Essential Work Protocol

Agent+ seeks the minimum sufficient evidence for a real decision.

## Necessity card

Before new work, complete [the essential task template](.planning/templates/ESSENTIAL-TASK.md).

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
[`2ed6c52c9d7e5e56942508591085fd45dea277d3f`](https://github.com/DietrichGebert/ponytail/tree/2ed6c52c9d7e5e56942508591085fd45dea277d3f).

## Falsifier and question rule

Before dispatch, name the furthest authorized decision-relevant endpoint and one fact that would
invalidate the proposed path. Inspect accessible evidence instead of asking. Ask only when two
plausible answers require materially different actions and a cheap lookup cannot resolve the fact.
Otherwise choose the smallest reversible default and record it in the active task.

Use one fresh verifier at the promotion boundary. Do not add recursive builder-critic rounds,
sentence-level provenance tags, or phase-by-phase critique unless the task names a distinct risk
that the existing evaluator and verifier cannot test.

## Engineering closure rule

Classify the boundary before dispatch:

- **Engineering diagnostic or readiness closure:** promotion is blocked at the first defect, but
  read-only defect collection continues across the named interface and adjacent failure class until
  the matrix is complete, continuation becomes unsafe, or the task budget ends.
- **Scientific, live, destructive, or irreversible execution:** stop at the first invalid condition.

Do not use a first-defect stop rule to create serial engineering repair cycles. The verifier may
enumerate additional falsified invariants without designing the repair. The next maker owns one
bundled correction and one deterministic acceptance receipt for the complete reported class.

After the first engineering review `BLOCK`, expand the bounded attack matrix before repair. After a
second `BLOCK` at the same interface or failure class, do not authorize a third local patch cycle.
Escalate to simplification: constrain or replace the interface, remove unnecessary caller choices,
and test the new boundary end to end. A contract change still requires the human owner.

Prefer designs that make invalid states impossible. For temporary roots, paths, modes, schemas, or
other infrastructure inputs, use a fixed approved namespace and a small validated identifier when
arbitrary caller input has no named consumer. Do not build an expanding custom validator for
capability the project does not need.

When a closed-interface recovery passes its required review, preserve that interface as the default
for the failure class. Reopening removed choices requires a new necessity card, named consumer,
deterministic acceptance checks, and required review.

An engineering closure is successful only when it unlocks the named user-visible or scientific
milestone. Test counts, review records, and patches are evidence, not the outcome.

Every engineering chain must use a registered ledger boundary. Validate its planned packet before
maker or reviewer dispatch. Before a reviewer verdict can unlock another maker, validate a
completed review packet with `--require-complete-engineering-review`; the attack matrix and named
coverage must exactly match the ledger. A partial reviewer narrative may block promotion, but it
cannot authorize the next repair or increment the persisted BLOCK count.

Use one active promotion-boundary dossier for the task contract, cumulative findings, acceptance
receipt, and integrated review. Update it at each bounded state change. Preserve older evidence as
history without creating a fresh document family for every local defect.

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

The task card selects `quick`, `standard`, `deep`, or `scientific/live`. Extra capacity changes
bounded throughput only; it does not change authority, context ceilings, retry limits, reviewer
count, or owner authorization. Use the mode budgets and model routes in `AI_WORKFLOW.md`.

An engineering chain may run plan, independent exploration, frozen evidence handoff, one exclusive
maker, deterministic evaluation, one fresh review, and Sol synthesis. Exploration may be parallel;
all later stages are sequential. Use one writer per repository, no overlapping writes, no recursive
spawn, no silent fallback, and one bounded wait per stage. A maker, evaluator, or reviewer `BLOCK`
stops the chain. Never auto-repair after a reviewer `BLOCK`.

Overnight work needs an explicit owner command and is limited to read-only or reversible engineering
with a fixed queue of at most eight items. It cannot perform live, scientific, or promotion work.

## Unattended execution rule

Use one authorized launch for a bounded unattended process. Before launch, record the exact command,
durable progress and terminal evidence paths, expected return point, and one result check.

The process must write its own durable evidence. The AI controller performs zero polls while the
process runs and one result check after return. A launch error, process error, missing terminal
evidence, or failed check consumes the authorization and returns `BLOCK`.

Do not use fallback or retry behavior. Resume only after bounded repair, any required fresh review,
and new explicit authorization. Durable process evidence does not grant promotion authority.

Reserve 25% of premium capacity for scientific, leakage, hard-architecture, or irreversible
decisions. Re-run model review after 10 completed bounded chains or 14 days, and immediately after
model/rate/plan changes, two routing `BLOCK`s, average context above 40K, or reviewer correction
above 20%.

## Evidence reuse

Reuse evidence while its claim, implementation, inputs, environment, and acceptance contract remain unchanged. New session context does not invalidate evidence.

## Proportionate verification

| Changed state | Minimum check |
| --- | --- |
| Markdown or planning text | Structure, links, and stated contract. |
| One implementation module | Narrow tests and static checks. |
| New immutable artifact | Exact ID, schema, hash, lineage, and counters. |
| Publication release | Release validation and fresh independent review. |

## BLOCK rule

A missing source, incomplete coverage, failed test, unauthorized action, or absent review is a typed `BLOCK`. Do not estimate around it or reinterpret it as a passing result.
