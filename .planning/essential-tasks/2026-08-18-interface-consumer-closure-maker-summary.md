# Interface-consumer closure maker summary

## Current state

Maker work is complete. Agent+ now has a reusable, deterministic check that blocks an interface
change when a repository consumer was omitted from the declared review surface. This is not yet an
accepted Agent+ release change. One fresh integrated review is required.

## What changed

- Added `agent-plus-interface-consumer-closure/v1`, a closed JSON receipt schema.
- Added `scripts/interface_consumer_guard.py` and its exact bootstrap copy.
- Added a public-safe example receipt and seven falsifying tests.
- Added consumer discovery, runtime-wrapper closure, and real-shape smoke fields to the essential
  task protocol and template.
- Added the guard, parity hashes, and public example to `scripts/validate-public-package.sh`.

The guard searches declared repository roots for declared interface tokens. The receipt must name
the interface definition and every discovered consumer. Unknown fields, duplicate JSON keys,
unsafe paths, missing or extra consumers, invalid ordering, and a missing required real-shape smoke
all fail closed.

## Deterministic receipts

- Focused guard tests: 7 passed.
- Full Agent+ unit suite: 56 passed.
- Public-package validator: PASS.
- Canonical/bootstrap bindings and internal Markdown links: PASS.
- Ruff: clean on the new guard and tests.
- Strict mypy: clean on the new guard and tests.
- Canonical/bootstrap guard copies: byte-identical.

Final hashes:

- Guard: `e2f30112737a25378ddbf0ff9d5fa52db49b4c4cef495063310ae38ef20271da`
- Guard tests: `4d7e69cae97a797d437ddfcea8ceb06af63428e445d470d2cc33f10a731517f0`
- Public example: `1e7050739621b56d98adc6729696f1660e6d249910d32c2ce4e3e529fdf21f79`
- Protocol: `df033994623a402602c06c0a529d7a11ee23c97745cd08061dbbc659ec295541`
- Essential-task template: `f16caaa462408cae2e772817cf50ee28eec34ecce46e88fe3164a8820c40b248`

## Boundaries

No release, commit, push, tag, or announcement occurred. No SECOND LOOK scientific authority was
changed. The downstream proving-project adapter is maker-complete and belongs in the same fresh
integrated review.

Status: `AGENT_PLUS_INTERFACE_CONSUMER_CLOSURE_MAKER_COMPLETE — FRESH INTEGRATED REVIEW REQUIRED`.
