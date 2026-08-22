# Agent+ legacy adoption deterministic evaluator — BLOCK

Date: 2026-08-22

Verdict: `BLOCK`

## Result

The maker implementation passed its declared suites, but an evaluator-owned disposable legacy
target proved three contract failures. No fresh reviewer was dispatched. No repair, release, Git
operation, consumer adoption, or SECOND LOOK change followed.

## Passing evidence

- Legacy-adoption focused suite: `6` tests passed.
- Existing lifecycle suite: `29` tests passed.
- Full public suite: `105` tests passed.
- Public validator: `PASS`; canonical/bootstrap bindings and internal links passed.
- Ruff: `PASS`.
- Strict mypy for the lifecycle manager: `PASS`.
- Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Planned task dispatch guard:
  `sha256:64cce1b180cc7578e6baacf7cd458d37ebc422ed11589a48c4e5a3082e30f29d`.

## Blocking evidence

The evaluator created one disposable exact-byte legacy target with a path containing spaces. It
installed the fixed startup check, ran the new `adopt` command, and then attacked the integrated
doctor and context routes.

1. The required startup check exited with status `7`, but `scripts/agent-plus doctor` returned
   success. Doctor validates the hook file but does not validate the hook result.
2. With a passing startup check, the managed legacy context command omitted the existing
   `.claude-memory.md` content.
3. The same context command omitted the existing `.planning/STATE.md` content.

The terminal evaluator text was:

```text
DETERMINISTIC_EVALUATOR_BLOCK
FINDING doctor-passed-while-required-startup-check-exited-7
FINDING legacy-context-omitted-project-hot-memory
FINDING legacy-context-omitted-planning-state
```

Static inspection also leaves hook path-rebinding resistance unproven. The managed context script
checks the hook path and later executes that path in separate operations. No descriptor-bound
execution receipt closes a swap between validation and execution. This is an open adjacent
invariant, not a separately demonstrated escape in this evaluator.

## Recovery boundary

The authorized implementation/evaluator chain is spent. Do not repair in this chain and do not
dispatch the planned fresh reviewer.

A new explicit owner authorization may permit one bundled repair that:

1. makes doctor execute and require a successful fixed project startup check;
2. preserves hot-memory and planning-state routing for adopted projects; and
3. binds execution to the validated hook file or deterministically proves path replacement cannot
   change the executed bytes.

That repair requires a complete deterministic evaluator rerun and one different fresh integrated
reviewer before any release decision.

Exact restart command:

```sh
scripts/ai-context.sh
```
