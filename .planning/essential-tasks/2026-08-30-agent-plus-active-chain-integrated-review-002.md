# Agent+ active-chain and cost-isolation integrated review 002

Date: 2026-08-30

## Verdict

`PASS` — the complete unreleased active-chain and connected cost-isolation bundle is ready for
engineering readiness closeout.

This PASS accepts engineering readiness only. It does not authorize promotion, version change,
release, Git mutation, data access, scientific work, or consumer synchronization.

All 21 registered attacks and all 16 named coverage areas were assessed. No Critical, Important,
or Minor finding remains. The array and object enum failure from review 001 now returns typed
`ChainError` through the API and a typed CLI denial without a traceback.

## Review boundary

- Base release commit: `ea147c0e2b2dac481238f96c37b56a31fe65033b`.
- This was one fresh independent review context. It did not make the original bundle or repair.
- Review 001, the repair necessity, the maker receipt, frozen candidates, live ledger, active
  capsule, policy, protocol, templates, research profile, and public documentation were read.
- No maker transcript, private proving-project evidence, baseball data, scientific artifact,
  dependency, release state, or consumer state was read or changed.
- Unrelated dirty worktree changes were preserved.

## Frozen identities

All packet identities matched their required SHA-256 values before substantive review.

| Frozen path | SHA-256 |
| --- | --- |
| `scripts/active_chain_guard.py` and `bootstrap/base/scripts/active_chain_guard.py` | `3784a41abe967c4d964c268ca999ebe202dbf9a5639382feaa16023197c04389` |
| `tests/test_active_chain_guard.py` | `43a8da4b8010474e321807e7f472714d18ff6647d58f2c7b2550a8fb7bad71bf` |
| `scripts/anti_loop_guard.py` and `bootstrap/base/scripts/anti_loop_guard.py` | `a0a7dd94bd5594305fd9ccd1dcd29e96d3dc424dc62ee3700836436fc3bae705` |
| `tests/test_anti_loop_guard.py` | `10145faacc2c469e10c4e7ce2b4311553b72efc581d71c65b10e6c1acf6c0724` |
| `.agent-plus/engineering-boundaries.json` | `617f8d2ebfef2960ddc5027cb476a5b2299de38908c54ad1ada44cdf478a39e3` |
| `.agent-plus/agent-plus-active-chain-typed-enum-repair-002.json` | `f98aef61bf60845cee96e9e65062e7f8416a7122b34610f883feda6e17b9cb84` |
| `.agent-plus/agent-plus-active-chain-review-002.json` before completion | `9deeae20e34f94f67b0ecc0c734259eb1659c3ddb75ce688ef358cd88fb567ee` |
| Review 001 record | `0ea1c4ea7cdaf4bc2878b76d3e4fb14fc28eca5d4b2c28c3c694ea9116039d51` |
| Typed enum repair maker receipt | `a0b4724d498a4d4219ae314381b6acba096e8b674ea47881557cbefa6a525bd2` |
| Typed enum repair necessity | `36f401f8298ff9ada406302049ae88fa4fc872c024cc73db744318655191ffb6` |
| Canonical and bootstrap example capsules | `2cb9cd7b6219de1f4065efce8af269f5bd67e33809e0cce01610cda7b38e04eb` |
| `docs/active-chain-capsule.md` | `53c3d06e73889aabab82a5e96730e1fc4beea478cca14c684c5bdef6912ae79f` |
| `AI_WORKFLOW.md` | `689ce6e8c826af3526f4de8ff1aa17799851d552c2b9edf7811d10ecb285d249` |
| `bootstrap/base/AI_WORKFLOW.md` | `4642e00c969f605cbdc146a9128c3344ea1cdfbb51cee62b558300eacfaaf743` |
| Canonical and bootstrap `ESSENTIAL_WORK_PROTOCOL.md` | `e7705493da2ae917701d2e3cf5c184950b0526fab5f85e05e4ec82143219b97d` |
| Canonical and bootstrap essential-task template | `081086da62a1469e39f6142f0a43fe6551b346625e3a205a6be5dccb76e80864` |
| `bootstrap/profiles/research/PROFILE.md` | `132c4b34efc729d14ca865373beb3593d2bf42fcfe3a62ffe9f9ca829a0da02c` |

## Attack matrix

| # | Attack | Result | Evidence |
| ---: | --- | --- | --- |
| 1 | `active-first-pending-routing` | PASS | Independent active capsule route returned the first pending stage. |
| 2 | `pass-closeout-complete` | PASS | Independent all-pass capsule closeout returned `ACTIVE_CHAIN_CLOSEOUT_PASS`. |
| 3 | `null-block-closeout` | PASS | Independent null and block capsules returned typed terminal closeouts. |
| 4 | `early-closeout-rejection` | PASS | Active closeout returned `BLOCK_CHAIN_EARLY_CLOSEOUT`. |
| 5 | `terminal-continue-rejection` | PASS | Terminal continuation returned `BLOCK_CHAIN_NOT_ACTIVE`. |
| 6 | `stage-order-rejection` | PASS | Out-of-order stage state returned `BLOCK_CHAIN_STAGE_ORDER`. |
| 7 | `stage-evidence-binding` | PASS | Wrong current stage returned `BLOCK_CHAIN_ROUTING`. |
| 8 | `authority-path-containment` | PASS | Parent escape returned `BLOCK_CHAIN_PATH`. |
| 9 | `authority-symlink-rejection` | PASS | Direct authority symlink returned `BLOCK_CHAIN_PATH`. |
| 10 | `long-authority-path` | PASS | Long nested regular authority path was accepted. |
| 11 | `unknown-duplicate-json-rejection` | PASS | Duplicate JSON key returned `BLOCK_CHAIN_DUPLICATE_KEY`. |
| 12 | `nonfinite-and-boolean-count-rejection` | PASS | Boolean and `NaN` counts returned typed failures. |
| 13 | `malformed-enum-type-rejection` | PASS | Arrays and objects across chain status, change kind, stage role, and stage status passed API probes `8/8`. |
| 14 | `capsule-location-containment` | PASS | Outside and symlink capsule paths returned typed containment failures. |
| 15 | `capsule-size-boundary` | PASS | Oversized capsule returned `BLOCK_CHAIN_CAPSULE_SIZE`. |
| 16 | `two-failure-reset-enforcement` | PASS | Two failures rejected continuation without architecture reset. |
| 17 | `anti-loop-authority-separation` | PASS | Ledger-bound anti-loop tests and source tracing preserved reset and outcome authority. |
| 18 | `canonical-bootstrap-byte-binding` | PASS | Active-chain and anti-loop guard copies and bound files matched. |
| 19 | `template-policy-routing` | PASS | Workflow, protocol, template, and research-profile routes were present and consistent. |
| 20 | `exact-target-graph-default` | PASS | Exact target graph, expensive-ancestor reuse, loop detection, and simplification routing were present. |
| 21 | `public-validator` | PASS | Complete public validator passed. |

The CLI malformed-enum probe independently returned code 1 with `BLOCK_CHAIN_STATUS` and no
`Traceback` in stderr. The complete independent active-chain matrix returned `27/27` passing
cases.

## Named coverage

| # | Coverage | Result |
| ---: | --- | --- |
| 1 | `guard-schema` | PASS |
| 2 | `guard-cli` | PASS |
| 3 | `terminal-semantics` | PASS |
| 4 | `path-safety` | PASS |
| 5 | `failure-limit` | PASS |
| 6 | `anti-loop-authority` | PASS |
| 7 | `canonical-script` | PASS |
| 8 | `bootstrap-script` | PASS |
| 9 | `example-capsules` | PASS |
| 10 | `synthetic-tests` | PASS |
| 11 | `workflow-policy` | PASS |
| 12 | `essential-protocol` | PASS |
| 13 | `task-template` | PASS |
| 14 | `research-profile` | PASS |
| 15 | `public-docs` | PASS |
| 16 | `public-validator` | PASS |

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

Review 001 Finding I-1 is closed by the explicit string checks at the four enum seams in
`scripts/active_chain_guard.py` and its byte-identical bootstrap copy. The independent API and
CLI probes verified typed rejection for the complete malformed enum set.

## Commands and outputs

- `python3 tests/test_active_chain_guard.py` — `17/17` passed.
- `PYTHONPATH=. python3 tests/test_anti_loop_guard.py` — `54/54` passed.
- `python3 tests/test_workflow_defaults.py` — `7/7` passed.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — `149/149` passed.
- `python3 -m py_compile` for both active-chain and anti-loop canonical/bootstrap guards — PASS.
- Canonical/bootstrap byte comparisons — PASS.
- Public example closeout — `ACTIVE_CHAIN_CLOSEOUT_PASS chain=public-example-chain`.
- Pre-update live capsule continuation — `ACTIVE_CHAIN_CONTINUE chain=active-chain-typed-enum-repair stage=fresh_review`.
- Repair packet anti-loop validation — PASS with receipt `sha256:4952f6cae7bea1e2c80e5a4ff92e9b13ec4e7d0d56f139336a7984c462923b84`.
- Independent active-chain probes — `27/27` passed, including API enum `8/8` and CLI no-traceback rejection `1/1`.
- `./scripts/validate-public-package.sh` — PASS with 149 tests, bindings, links, and privacy checks.
- Required complete-review closeout guard — receipt recorded below.

## Public-safety limits

No raw baseball data, credentials, private paths, personal transcripts, proprietary artifacts,
consumer project files, dependencies, scientific results, or release state were added or accessed.
No Git, release, publication, data-access, scientific, or consumer-synchronization action was
performed. Only this review record, the completed review packet, and the active-chain fresh-review
stage were changed under review ownership.

## Closeout

- Review packet status: `complete`.
- Attack matrix status: `complete`.
- Named coverage status: `complete`.
- Fresh-review verdict: `PASS`.
- Required closeout receipt: `sha256:3ceb5acd7637c4568663a2c93216aa8b065d0ace32a723485fda1ea51be9ecfc`.
- Active capsule route after review: `current_stage=closeout`.
- Next action: controller closeout, then a separate owner release decision.

## Restart

```sh
./scripts/ai-context.sh
```
