# Agent+ 0.4.0 manifest static-typing repair — independent review 001

Date: 2026-08-30

## Verdict

`BLOCK` — 8/8 registered attacks were assessed and 7/7 named coverage areas were assessed, but
the disposable simulated `VERSION=0.4.0` public-validator run did not reach validation. The
review therefore cannot accept release readiness. No implementation repair was performed.

## Findings

### Critical

None observed.

### Important

- The required disposable `VERSION=0.4.0` validation has no independent passing receipt. The
  temporary-copy harness stopped before the validator ran with `tar: Special header too large:
  %llu` followed by `Write error`. This leaves the simulated-release attack and release-scope
  acceptance blocked; the maker receipt is not substituted for fresh reviewer evidence.

### Minor

None observed in the typed implementation seam.

## Attack matrix — 8/8 assessed

1. `strict-mypy-manager` — PASS. Strict mypy reported no issues in the manager, active-chain
   guard, or anti-loop guard.
2. `legacy-manifest-type-narrowing` — PASS. Lifecycle/adoption execution and direct v1 helper
   probe accepted the historical v1 identity path.
3. `current-manifest-type-narrowing` — PASS. Current v2 execution and direct v2 helper probe
   returned the registered current identity.
4. `manifest-set-id-return-type` — PASS. Both valid helper returns were exact strings matching
   their registered IDs.
5. `malformed-managed-set-typed-error` — PASS. Missing, list, object, integer, and boolean
   current identity values each raised `ManagerError`, with no uncaught exception.
6. `lifecycle-regression` — PASS. Lifecycle suite completed `43/43`.
7. `simulated-0-4-0-public-validator` — BLOCK. Disposable archive/copy setup failed before the
   validator could execute; no simulated pass is claimed.
8. `public-validator` — PASS. Live public validator completed `164/164` and all listed checks.

## Named coverage — 7/7 assessed

- `manager-manifest-parser`: PASS for v1/v2 and exact registry checks exercised by lifecycle
  tests.
- `manifest-set-helper`: PASS for 2 valid and 5 malformed direct helper probes.
- `lifecycle-tests`: PASS, `43/43`.
- `legacy-adoption-tests`: PASS, `12/12`.
- `strict-mypy`: PASS, three production files.
- `release-scope-preflight`: BLOCK pending a successful disposable simulated-version run.
- `public-validator`: PASS, live `164/164`.

The required legacy v1, current v2, unknown, missing, non-string, subset, and superset managed-set
behaviors were assessed through the live lifecycle/adoption matrix; direct helper probes added the
valid v1/v2 returns and five malformed current-identity cases.

## Independent commands and results

```text
./scripts/ai-context.sh                                      PASS
python3 scripts/active_chain_guard.py --capsule .agent-plus/active-chain.json --mode continue
                                                              PASS (fresh_review admitted)
sha256sum of all 7 frozen packet inputs                       PASS (all exact)
mypy --strict scripts/agent_plus_manager.py \
  scripts/active_chain_guard.py scripts/anti_loop_guard.py   PASS
ruff check manager, adjacent guards, lifecycle/adoption tests PASS
python3 -m unittest discover -s tests -p test_agent_plus_lifecycle.py
                                                              PASS (43/43)
python3 -m unittest discover -s tests -p test_agent_plus_legacy_adoption.py
                                                              PASS (12/12)
sh scripts/validate-public-package.sh                         PASS (164/164)
disposable VERSION=0.4.0 public-validator                   BLOCK (tar setup error before run)
```

Direct `_manifest_set_id` probes: `7/7` (v1, v2, and five malformed current values). The live
tests and implementation inspection showed no version, registry, upgrade, recovery, doctor,
release, or authority change attributable to the typed-rejection seam. The worktree, VERSION,
real Git index, and repository object store were not mutated by the failed disposable setup.

## Exact files changed by this review

- `.agent-plus/agent-plus-0-4-0-static-typing-repair-review-001.json`
- `.planning/essential-tasks/2026-08-30-agent-plus-0-4-0-static-typing-repair-review-001.md`
- `.agent-plus/active-chain.json` (fresh-review terminal routing only)

No implementation, test, ledger, VERSION, Git, release, consumer, private-state, data, or
scientific artifact was changed.

## Controller evidence registration

The completed review packet passed ledger-bound closeout with receipt
`sha256:ab87a2b1d035f1337a2686bffc9b3bf297386d8e7407912198327e4463a287e7`.
The controller then recorded the review `BLOCK` in the live engineering ledger. The failure class
now has `block_count=2` and `architecture_reset_required=true`. The block-record result is
`sha256:d704c9223ebc44444dac3a39ce49dd0ab5cc33a349ad5a37846744d7a359e2fa`.

The reviewer wrote `blocked` instead of the capsule schema value `block`. The controller made one
routing-only correction and set `current_stage` to `null`. This correction did not change the
review verdict, finding, implementation, test results, or authority boundary.

No local repair or repeated disposable validation followed the reviewer `BLOCK`.
