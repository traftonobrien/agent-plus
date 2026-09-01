# Agent+ active-chain lifecycle delivery review 001

Date: 2026-08-30

## Verdict

`PASS` — the lifecycle-delivery candidate closes the registered initialization, manifest,
additive-upgrade, recovery, doctor, and release-boundary attacks.

This PASS accepts engineering readiness only. It does not authorize promotion, version change,
release, Git mutation, data access, scientific work, or consumer synchronization.

All `27/27` attacks and all `18/18` named coverage items were assessed. No Critical, Important, or
Minor finding remains.

## Review boundary

- The frozen packet, live review JSON, active capsule, engineering ledger, implementation files,
  deterministic tests, and public validator were inspected.
- This was an independent verifier pass. The maker transcript was not read or used.
- No implementation, test, ledger, consumer, release, Git, data, or scientific state was changed.
- The worktree was already dirty. Existing unrelated changes were preserved.

## Frozen identity checks

All frozen packet hashes matched before the independent probes.

| Path | SHA-256 |
| --- | --- |
| `scripts/agent_plus_manager.py` | `9b1098be3287b01e991506a1ad00fbea2a0957ae1dcbff0696fbd900bd1cfca2` |
| `scripts/agent-plus-init.sh` | `91f9f6ddb6df4a747ed224738ce6fefe3078b470666772f7d397e65367597e09` |
| `scripts/agent-plus-doctor.sh` | `146f0977b0db79b255b0a0fa311d425d223d85da890ffc505ce2e92aa5d72c76` |
| `tests/test_agent_plus_lifecycle.py` | `8b56761558aa16d90eaecea111d59fe1b3d9748afcb5754bafde994506df549d` |
| `tests/test_agent_plus_legacy_adoption.py` | `177876f5a591db60f73450222bc52ac7c5c50897beb305c8e6b7611ebb9fe34c` |
| `bootstrap/base/scripts/ai-context.sh` | `c1a56ca2fe38d4cbc48db12b76052cea99c63047162523f413f42ed14d04f8c3` |
| `README.md` | `f2d7daf1daa1c677a88d00eb5c229e95ab7c48aec227c004a0ac50859e8ed58f` |
| `docs/architecture.md` | `bfc87a78011a9ba1d7bcf29a56b7f93b4e55bfb69f6b99591672e95916405a3c` |
| `docs/bootstrap-a-baseball-project.md` | `2bb620da9e34b9569337ba4d317481b4a7c3eda147d52bbe473f0e5c7405a92b` |
| `docs/active-chain-capsule.md` | `b38f610d18f2ad024ed15f65830d9a0f9f6311c3b0f468463a4f20bd8ca91749` |
| `.agent-plus/engineering-boundaries.json` | `78ed2b182967cbd60161bdc650e46249b0534386d98cb19b9038e03657533ded` |
| `.agent-plus/agent-plus-active-chain-lifecycle-task-001.json` | `7434ad3896f93919fa01df66bcf9652b18e3dc3b9b62cc98f136f9d6a7b616d6` |
| Lifecycle necessity | `74a92b13c9e08f0813a1d6a404682de27bf4681c02c61e0ca9879c0fb46bccfb` |
| Maker receipt | `3fa4009efc5bdb375b996c7b4cc5b6a84f1d28ae0e9de20da6e4d112be986360` |

Canonical and bootstrap active-chain guards matched at
`3784a41abe967c4d964c268ca999ebe202dbf9a5639382feaa16023197c04389`.
Canonical and bootstrap example capsules matched at
`2cb9cd7b6219de1f4065efce8af269f5bd67e33809e0cce01610cda7b38e04eb`.
The bootstrap context command and all required lifecycle commands had executable modes.

## Attack matrix

| # | Attack | Result | Independent evidence |
| ---: | --- | --- | --- |
| 1 | `clean-init-guard-delivery` | PASS | Clean temporary initialization delivered `scripts/active_chain_guard.py`. |
| 2 | `clean-init-example-delivery` | PASS | Clean temporary initialization delivered `.agent-plus/active-chain-example.json`. |
| 3 | `current-manifest-set-identity` | PASS | Current manifest identified `agent-plus-active-chain-v1`. |
| 4 | `current-manifest-exact-set` | PASS | Current manifest contained the exact 15-file registry set. |
| 5 | `v1-0-2-0-set-compatibility` | PASS | Historical `0.2.0` manifest reported update and upgraded additively. |
| 6 | `v1-0-3-0-set-compatibility` | PASS | Historical `0.3.0` manifest reported update and upgraded additively. |
| 7 | `unknown-v1-version-rejection` | PASS | Unknown legacy version was rejected by status and doctor. |
| 8 | `unknown-v2-set-identity-rejection` | PASS | Unknown v2 managed-set identity was rejected by status and doctor. |
| 9 | `subset-current-set-rejection` | PASS | Current managed-file subset was rejected by status and doctor. |
| 10 | `superset-current-set-rejection` | PASS | Current managed-file superset was rejected by status and doctor. |
| 11 | `status-generation-update` | PASS | Historical manifests returned `UPDATE_AVAILABLE` with the current set identity. |
| 12 | `additive-upgrade-state-preservation` | PASS | Project-owned state survived an additive upgrade byte-for-byte. |
| 13 | `candidate-only-path-collision-block` | PASS | Pre-existing candidate-only path blocked before journal creation. |
| 14 | `candidate-only-race-preservation` | PASS | A post-preflight project file survived failed upgrade and recovery. |
| 15 | `candidate-only-replacement-block` | PASS | Changed committed candidate-only file blocked recovery cleanup and retained the journal. |
| 16 | `managed-removal-rejection` | PASS | Direct journal construction rejected managed-file removal. |
| 17 | `managed-executable-mode-preservation` | PASS | Required executable modes were preserved through initialization and upgrade. |
| 18 | `partial-added-file-commit-recovery` | PASS | Injected partial commit produced a typed recoverable transaction. |
| 19 | `recovery-removes-candidate-only-files` | PASS | Recovery removed only committed candidate-only files and restored v1 bytes. |
| 20 | `forged-journal-set-rejection` | PASS | Forged candidate-only and prior/candidate set identities were rejected. |
| 21 | `doctor-missing-guard` | PASS | Canonical and copied doctor rejected a missing active-chain guard. |
| 22 | `doctor-missing-example` | PASS | Canonical and copied doctor rejected a missing active-chain example. |
| 23 | `doctor-managed-drift` | PASS | Canonical and copied doctor rejected managed control drift. |
| 24 | `legacy-adoption-upgrade` | PASS | Legacy adoption upgraded to the current set and preserved declaration and hook bytes. |
| 25 | `copied-doctor-manifest-parity` | PASS | Copied doctor passed for current and legacy-adopted temporary targets. |
| 26 | `canonical-bootstrap-byte-binding` | PASS | Guard, anti-loop guard, protocol, template, and example bindings matched. |
| 27 | `public-validator` | PASS | Public package validator completed all checks. |

## Named coverage

| # | Coverage | Result |
| ---: | --- | --- |
| 1 | `manifest-schema` | PASS |
| 2 | `managed-set-registry` | PASS |
| 3 | `initializer` | PASS |
| 4 | `doctor` | PASS |
| 5 | `copied-doctor` | PASS |
| 6 | `status` | PASS |
| 7 | `transactional-upgrade` | PASS |
| 8 | `recovery-journal` | PASS |
| 9 | `collision-protection` | PASS |
| 10 | `managed-file-modes` | PASS |
| 11 | `legacy-adoption` | PASS |
| 12 | `active-chain-guard` | PASS |
| 13 | `active-chain-example` | PASS |
| 14 | `lifecycle-tests` | PASS |
| 15 | `legacy-tests` | PASS |
| 16 | `bootstrap` | PASS |
| 17 | `public-docs` | PASS |
| 18 | `public-validator` | PASS |

## Findings by severity

- Critical: none.
- Important: none.
- Minor: none.

## Commands and receipts

- `./scripts/ai-context.sh` — completed before review.
- `python3 tests/test_agent_plus_lifecycle.py` — `42/42` passed.
- `python3 tests/test_agent_plus_legacy_adoption.py` — `12/12` passed.
- `python3 tests/test_active_chain_guard.py` — `17/17` passed.
- `PYTHONPATH=. python3 -m unittest discover -s tests -p 'test_*.py'` — `163/163` passed.
- Shell syntax checks for canonical and bootstrap shell scripts — PASS.
- Python compilation for lifecycle and guard modules — PASS.
- Canonical/bootstrap byte comparisons — PASS.
- Active example closeout — `ACTIVE_CHAIN_CLOSEOUT_PASS chain=public-example-chain`.
- Independent lifecycle probe group 1 — PASS for manifest, status, upgrade, collision, and removal attacks.
- Independent lifecycle probe group 2 — PASS for race, replacement, recovery, forged journal, doctor, adoption, and copied-doctor attacks.
- `./scripts/validate-public-package.sh` — PASS with `163/163` tests, bindings, links, and privacy checks.
- `git diff --check` — PASS.
- Required complete-review anti-loop closeout — PASS with receipt `sha256:c77ba7104f89e9ebbaa693c342a3dd940b9e8576b2457032252c7a1038136d10`.

## Limits

No raw baseball data, credentials, private project files, consumer state, release state, or
scientific artifacts were accessed. No implementation files, tests, ledger state, Git state,
release state, or consumers were changed.

## Closeout

- Review JSON status: `complete`.
- Attack matrix status: `complete` with `27/27` passing items.
- Named coverage status: `complete` with `18/18` passing items.
- Fresh-review verdict: `PASS`.
- Active capsule route: `current_stage=closeout`, with `fresh_review=pass`.
- Next action: controller closeout and a separate owner release decision.

## Restart

```sh
./scripts/ai-context.sh
```
