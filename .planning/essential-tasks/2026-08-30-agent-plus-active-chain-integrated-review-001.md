# Agent+ active-chain and cost-isolation integrated review

Date: 2026-08-30

## Verdict

`BLOCK` — the active-chain and connected cost-isolation bundle is not ready for the owner's
promotion or release decision.

The review is complete. All 20 attacks and all 16 named coverage areas were assessed. The
blocking finding is in the active-chain schema boundary. No repair was made.

This verdict does not authorize a release, version change, Git mutation, consumer synchronization,
data access, scientific work, or a same-chain repair.

## Review boundary

- Base release commit: `ea147c0e2b2dac481238f96c37b56a31fe65033b`.
- Inputs were the frozen review packet, completion audit, live ledger, active capsule, candidate
  files, connected policy files, deterministic receipts, and the relevant worktree diff.
- No maker transcript, private proving-project evidence, baseball data, or scientific artifact was
  read.
- Unrelated dirty worktree changes were preserved.

## Frozen identities

The following pre-review hashes matched the packet:

| Frozen path | SHA-256 |
| --- | --- |
| `scripts/active_chain_guard.py` and `bootstrap/base/scripts/active_chain_guard.py` | `826a8a551a15fd30f9742a957718f48ddc115e582f2ec802d95543df4ae921e7` |
| `tests/test_active_chain_guard.py` | `9f31561f8c2ab724a935e18a2863f9ccfc9d39429df58e8ca5fdd67824ca6858` |
| `scripts/anti_loop_guard.py` and `bootstrap/base/scripts/anti_loop_guard.py` | `a0a7dd94bd5594305fd9ccd1dcd29e96d3dc424dc62ee3700836436fc3bae705` |
| `tests/test_anti_loop_guard.py` | `10145faacc2c469e10c4e7ce2b4311553b72efc581d71c65b10e6c1acf6c0724` |
| `.agent-plus/engineering-boundaries.json` | `0172a521d07a622b8803184bc2393148d3b1775bd122951ab1066fd4955d5dbd` |
| `.agent-plus/agent-plus-active-chain-review-001.json` before completion | `f4514259fd8592b9c2030bdd9417c6138f50a79263f5cdc9c0d1f284677c730b` |
| `.agent-plus/active-chain-example.json` and bootstrap copy | `2cb9cd7b6219de1f4065efce8af269f5bd67e33809e0cce01610cda7b38e04eb` |
| `docs/active-chain-capsule.md` | `53c3d06e73889aabab82a5e96730e1fc4beea478cca14c684c5bdef6912ae79f` |
| `AI_WORKFLOW.md` | `689ce6e8c826af3526f4de8ff1aa17799851d552c2b9edf7811d10ecb285d249` |
| `bootstrap/base/AI_WORKFLOW.md` | `4642e00c969f605cbdc146a9128c3344ea1cdfbb51cee62b558300eacfaaf743` |
| `ESSENTIAL_WORK_PROTOCOL.md` and bootstrap copy | `e7705493da2ae917701d2e3cf5c184950b0526fab5f85e05e4ec82143219b97d` |
| `.planning/templates/ESSENTIAL-TASK.md` and bootstrap copy | `081086da62a1469e39f6142f0a43fe6551b346625e3a205a6be5dccb76e80864` |
| `bootstrap/profiles/research/PROFILE.md` | `132c4b34efc729d14ca865373beb3593d2bf42fcfe3a62ffe9f9ca829a0da02c` |

The completed review packet now has SHA-256
`cdf8c82b4c79c24de019cf31344f099fa4ef51b08e630213e68cddfb2a27bb92`.

## Attack matrix

Every item was assessed. The declared scenarios passed except where the schema robustness finding
below applies to the broader `guard-schema` boundary.

| # | Attack | Result |
| ---: | --- | --- |
| 1 | `active-first-pending-routing` | PASS |
| 2 | `pass-closeout-complete` | PASS |
| 3 | `null-block-closeout` | PASS |
| 4 | `early-closeout-rejection` | PASS |
| 5 | `terminal-continue-rejection` | PASS |
| 6 | `stage-order-rejection` | PASS |
| 7 | `stage-evidence-binding` | PASS |
| 8 | `authority-path-containment` | PASS |
| 9 | `authority-symlink-rejection` | PASS for direct file and escaping-directory symlinks |
| 10 | `long-authority-path` | PASS |
| 11 | `unknown-duplicate-json-rejection` | PASS |
| 12 | `nonfinite-and-boolean-count-rejection` | PASS |
| 13 | `capsule-location-containment` | PASS |
| 14 | `capsule-size-boundary` | PASS |
| 15 | `two-failure-reset-enforcement` | PASS |
| 16 | `anti-loop-authority-separation` | PASS |
| 17 | `canonical-bootstrap-byte-binding` | PASS |
| 18 | `template-policy-routing` | PASS |
| 19 | `exact-target-graph-default` | PASS |
| 20 | `public-validator` | PASS |

## Named coverage

| # | Coverage | Result |
| ---: | --- | --- |
| 1 | `guard-schema` | BLOCK due Finding I-1 |
| 2 | `guard-cli` | PASS |
| 3 | `terminal-semantics` | PASS |
| 4 | `path-safety` | PASS for declared direct and escaping-path cases |
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

## Findings

### Important

#### I-1 — malformed enum values raise an uncaught `TypeError`

The active-chain validator tests enum membership before checking that the value is a hashable
string. A JSON array or object in `status`, `change_kind`, or a stage `role` or `status` reaches a
set-membership operation and raises `TypeError: unhashable type: 'list'` instead of a typed
`ChainError`. This affects the public Python API and produces an unhandled traceback through the
CLI. The malformed input is rejected, but the schema boundary is not fail-closed with the declared
typed guard behavior.

Evidence:

- `scripts/active_chain_guard.py:167-169` checks stage `role` and `status` with set membership
  without a string/type check.
- `scripts/active_chain_guard.py:187-193` checks chain `status` and `change_kind` with set
  membership without a string/type check.
- Independent temporary-capsule probes with list values for each field produced an uncaught
  `TypeError`, while the valid and declared negative tests passed.

This finding blocks engineering readiness. No same-chain repair is proposed or applied.

## Commands and receipts

- `python3 tests/test_active_chain_guard.py` — `15/15` passed.
- `PYTHONPATH=. python3 tests/test_anti_loop_guard.py` — `54/54` passed.
- `python3 tests/test_workflow_defaults.py` — `7/7` passed.
- `python3 -m unittest discover -s tests -p 'test_*.py'` — `147/147` passed.
- `python3 -m py_compile scripts/active_chain_guard.py bootstrap/base/scripts/active_chain_guard.py scripts/anti_loop_guard.py bootstrap/base/scripts/anti_loop_guard.py` — PASS.
- Canonical/bootstrap byte comparisons for both guards, the protocol, the template, and the
  example capsule — PASS.
- Active example closeout — `ACTIVE_CHAIN_CLOSEOUT_PASS chain=public-example-chain`.
- Live active capsule continuation — `ACTIVE_CHAIN_CONTINUE chain=active-chain-review-readiness stage=fresh_review`.
- Planned anti-loop dispatch — PASS with receipt
  `sha256:5db138c260311831b093175bbe38939c39a41bac31390a49d3c7fae7c793ba00`.
- Required complete-review closeout guard — PASS with receipt
  `sha256:aac523d9b1704566df547108c42802e0fcfe3189a400cac2a3c5811904496f7b7`.
- `./scripts/validate-public-package.sh` — PASS after removal of the reviewer-generated temporary
  model-review report. The existing unrelated `outputs/` state was preserved.
- `git diff --check ea147c0e2b2dac481238f96c37b56a31fe65033b` — PASS.

Deterministic checks are evidence only. They do not override Finding I-1 or this verdict.

## Public-safety limits

No raw baseball data, credentials, private paths, personal transcripts, proprietary artifacts,
consumer project files, dependencies, scientific results, or release state were added or accessed.
No Git, release, publication, data-access, scientific, or consumer-synchronization action was
performed. The engineering ledger was not mutated. Only this review record, the completed review
packet, and the active-chain fresh-review stage are authorized review-state changes.

## Closeout

- Review packet status: `complete`.
- Attack matrix status: `complete`.
- Named coverage status: `complete`.
- Fresh-review verdict: `BLOCK`.
- Required closeout receipt: `sha256:aac523d9b1704566df547108c42802e0fcfe3189a400cac2a3c5811904496f7b7`.
- Next action: owner-authorized bounded repair and a new fresh review after the blocking schema
  boundary is corrected. This review does not authorize that repair.

## Controller evidence registration

After the completed review closeout passed, the controller recorded this `BLOCK` in the live
engineering ledger. The failure class now has `block_count=1`. The completed packet passes again
against the updated ledger with receipt
`sha256:92ee4f60d8977d199f6207170d6f93407ec6bff550aef5e08cbe337721bf17fc`.

## Restart

```sh
./scripts/ai-context.sh
```
