# Agent+ active-chain typed enum repair integrated review 002 packet

Date: 2026-08-30

Review status: `PLANNED`.

## Decision

Return one fresh independent `PASS` or `BLOCK` on the complete active-chain and connected
cost-isolation bundle after the typed enum repair. A `PASS` accepts engineering readiness only. It
does not authorize promotion, version change, release, Git mutation, or consumer synchronization.

## Reviewer contract

- Use one fresh context that did not make the original bundle or repair.
- Read this contract, review 001, candidate files, deterministic receipts, and registered matrix.
- Do not read a maker transcript or private proving-project evidence.
- Continue every safe read-only attack after the first defect.
- Do not repair any finding in the reviewer context.
- Do not access data, execute scientific work, change dependencies, mutate Git, release, publish,
  or synchronize a consumer.

## Repair boundary

Review 001 found that arrays and objects in four enum seams could raise uncaught `TypeError`. The
repair adds one string-type check before each existing set-membership check. It adds no enum,
dependency, fallback, caller choice, or authority change.

## Frozen candidate identities

- Canonical and bootstrap `scripts/active_chain_guard.py`:
  `3784a41abe967c4d964c268ca999ebe202dbf9a5639382feaa16023197c04389`
- `tests/test_active_chain_guard.py`:
  `43a8da4b8010474e321807e7f472714d18ff6647d58f2c7b2550a8fb7bad71bf`
- Canonical and bootstrap `scripts/anti_loop_guard.py`:
  `a0a7dd94bd5594305fd9ccd1dcd29e96d3dc424dc62ee3700836436fc3bae705`
- `tests/test_anti_loop_guard.py`:
  `10145faacc2c469e10c4e7ce2b4311553b72efc581d71c65b10e6c1acf6c0724`
- `.agent-plus/engineering-boundaries.json`:
  `617f8d2ebfef2960ddc5027cb476a5b2299de38908c54ad1ada44cdf478a39e3`
- `.agent-plus/agent-plus-active-chain-typed-enum-repair-002.json`:
  `f98aef61bf60845cee96e9e65062e7f8416a7122b34610f883feda6e17b9cb84`
- `.agent-plus/agent-plus-active-chain-review-002.json` before completion:
  `9deeae20e34f94f67b0ecc0c734259eb1659c3ddb75ce688ef358cd88fb567ee`
- Review 001 record:
  `0ea1c4ea7cdaf4bc2878b76d3e4fb14fc28eca5d4b2c28c3c694ea9116039d51`
- Typed enum repair maker receipt:
  `a0b4724d498a4d4219ae314381b6acba096e8b674ea47881557cbefa6a525bd2`
- Typed enum repair necessity:
  `36f401f8298ff9ada406302049ae88fa4fc872c024cc73db744318655191ffb6`
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
shared semantics. Enforce byte identity only for pairs bound by the public validator.

## Planned dispatch receipt

The exact ledger-bound review packet passes standard validation:

`sha256:442fe6a6499e807f854035b1c5867cc929bda3bcf1e7836cd28879b3470bfca2`

The completed reviewer packet must pass:

```sh
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-active-chain-review-002.json \
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
13. `malformed-enum-type-rejection`
14. `capsule-location-containment`
15. `capsule-size-boundary`
16. `two-failure-reset-enforcement`
17. `anti-loop-authority-separation`
18. `canonical-bootstrap-byte-binding`
19. `template-policy-routing`
20. `exact-target-graph-default`
21. `public-validator`

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

- Malformed enum API probes: `8/8`.
- Malformed enum CLI probe: `1/1`.
- Active-chain focused suite: `17/17`.
- Anti-loop focused suite: `54/54`.
- Workflow-default suite: `7/7`.
- Complete public suite: `149/149`.
- Compilation, byte bindings, links, privacy, and public validation: `PASS`.

These results are maker and evaluator evidence. They are not the fresh review verdict.

## Reviewer closeout

For `PASS`, complete every matrix item, run the closeout guard, write one integrated review record,
and update the active capsule review stage. Then stop for controller closeout and owner decision.

For `BLOCK`, complete every safe matrix item, run the closeout guard, write the complete finding
class, mark the active capsule terminal `block`, and stop. Do not design or apply a repair.

## Restart

```sh
./scripts/ai-context.sh
```
