# Agent+ active-chain and cost-isolation integrated review packet

Date: 2026-08-30

Review status: `PLANNED`.

## Decision

Return one fresh independent `PASS` or `BLOCK` on whether the active-chain and connected policy
bundle is ready for an owner release decision. A `PASS` accepts this engineering capability only.
It does not authorize a version change, release, Git mutation, or consumer synchronization.

## Reviewer contract

- Use one fresh engineering-review context that did not make this bundle.
- Read the contract, candidate files, deterministic receipts, and registered matrix.
- Do not read a maker transcript or private proving-project evidence.
- Continue every safe read-only attack after the first defect so the complete reachable class is
  reported once.
- Do not repair any finding in the reviewer context.
- Do not access data, execute scientific work, change dependencies, mutate Git, release, publish,
  or synchronize a consumer.

## Frozen candidate identities

- `scripts/active_chain_guard.py` and bootstrap copy:
  `826a8a551a15fd30f9742a957718f48ddc115e582f2ec802d95543df4ae921e7`
- `tests/test_active_chain_guard.py`:
  `9f31561f8c2ab724a935e18a2863f9ccfc9d39429df58e8ca5fdd67824ca6858`
- `scripts/anti_loop_guard.py` and bootstrap copy:
  `a0a7dd94bd5594305fd9ccd1dcd29e96d3dc424dc62ee3700836436fc3bae705`
- `tests/test_anti_loop_guard.py`:
  `10145faacc2c469e10c4e7ce2b4311553b72efc581d71c65b10e6c1acf6c0724`
- `.agent-plus/engineering-boundaries.json`:
  `0172a521d07a622b8803184bc2393148d3b1775bd122951ab1066fd4955d5dbd`
- `.agent-plus/agent-plus-active-chain-review-001.json`:
  `f4514259fd8592b9c2030bdd9417c6138f50a79263f5cdc9c0d1f284677c730b`
- Canonical and bootstrap example capsules:
  `2cb9cd7b6219de1f4065efce8af269f5bd67e33809e0cce01610cda7b38e04eb`
- `docs/active-chain-capsule.md`:
  `53c3d06e73889aabab82a5e96730e1fc4beea478cca14c684c5bdef6912ae79f`

## Connected policy identities

- `AI_WORKFLOW.md`:
  `689ce6e8c826af3526f4de8ff1aa17799851d552c2b9edf7811d10ecb285d249`
- `bootstrap/base/AI_WORKFLOW.md`:
  `4642e00c969f605cbdc146a9128c3344ea1cdfbb51cee62b558300eacfaaf743`
- Canonical and bootstrap `ESSENTIAL_WORK_PROTOCOL.md`:
  `e7705493da2ae917701d2e3cf5c184950b0526fab5f85e05e4ec82143219b97d`
- Canonical and bootstrap essential-task template:
  `081086da62a1469e39f6142f0a43fe6551b346625e3a205a6be5dccb76e80864`
- `bootstrap/profiles/research/PROFILE.md`:
  `132c4b34efc729d14ca865373beb3593d2bf42fcfe3a62ffe9f9ca829a0da02c`

The canonical and bootstrap workflow files are intentionally structurally different. Review their
shared semantics, not byte equality. The guard, example, protocol, and template pairs must remain
byte-identical where the public validator requires parity.

## Planned dispatch receipt

The exact ledger-bound review packet passed standard anti-loop validation:

`sha256:5db138c260311831b093175bbe38939c39a41bac31390a49d3c7fae7c793ba00`

The completed reviewer packet must pass:

```sh
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-active-chain-review-001.json \
  --require-complete-engineering-review
```

## Required attack matrix

1. `active-first-pending-routing`
2. `pass-closeout-complete`
3. `null-block-closeout`
4. `early-closeout-rejection`
5. `terminal-continue-rejection`
6. `stage-order-rejection`
7. `stage-evidence-binding`
8. `authority-path-containment`
9. `authority-symlink-rejection`
10. `long-authority-path`
11. `unknown-duplicate-json-rejection`
12. `nonfinite-and-boolean-count-rejection`
13. `capsule-location-containment`
14. `capsule-size-boundary`
15. `two-failure-reset-enforcement`
16. `anti-loop-authority-separation`
17. `canonical-bootstrap-byte-binding`
18. `template-policy-routing`
19. `exact-target-graph-default`
20. `public-validator`

## Required named coverage

1. `guard-schema`
2. `guard-cli`
3. `terminal-semantics`
4. `path-safety`
5. `failure-limit`
6. `anti-loop-authority`
7. `canonical-script`
8. `bootstrap-script`
9. `example-capsules`
10. `synthetic-tests`
11. `workflow-policy`
12. `essential-protocol`
13. `task-template`
14. `research-profile`
15. `public-docs`
16. `public-validator`

## Deterministic maker evidence

- Active-chain focused suite: `15/15`.
- Anti-loop focused suite: `54/54`.
- Workflow-default suite: `7/7`.
- Complete public suite: `147/147`.
- Python compilation: `PASS`.
- Canonical/bootstrap guard bindings: `PASS`.
- Internal Markdown links: `PASS`.
- Public privacy scan: `PASS`.
- Complete public-package validator: `PASS`.

These results are maker and evaluator evidence. They are not the fresh review verdict.

## Reviewer closeout

For `PASS`, complete every matrix item in the JSON review packet, run the complete closeout guard,
write one integrated review record, and update the active capsule review stage. Then stop for the
owner release decision.

For `BLOCK`, complete every safe matrix item, run the closeout guard before recording the persisted
BLOCK count, write the complete finding class, mark the active capsule terminal `block`, and stop.
Do not design or apply a repair.
