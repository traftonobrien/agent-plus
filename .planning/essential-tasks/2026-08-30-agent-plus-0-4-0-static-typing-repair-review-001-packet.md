# Agent+ 0.4.0 manifest static-typing repair review 001 packet

Date: 2026-08-30

Status: `READY FOR FRESH INDEPENDENT REVIEW`.

## Decision

Decide whether the bounded type-narrowing repair closes the strict-mypy release blocker without
weakening exact manifest validation, legacy compatibility, managed-set identity, or lifecycle
behavior.

The reviewer must use this packet, the planned review JSON, ledger, active capsule, live frozen
files, and deterministic maker receipt. The reviewer must not use the maker transcript or repair a
finding.

## Required scope

- Complete all `8` registered attacks and `7` named coverage items.
- Confirm strict mypy passes the manager and adjacent guards.
- Probe legacy v1, current v2, unknown, missing, non-string, subset, and superset managed-set cases.
- Confirm `_manifest_set_id` returns a string for valid v1/v2 manifests and typed `ManagerError` for
  malformed current identity input.
- Confirm no version, managed-set registry, upgrade, recovery, doctor, release, or authority
  behavior changed beyond typed rejection at the private helper seam.
- Run the live focused and complete tests plus a disposable simulated `VERSION=0.4.0` public
  validator.
- Return `PASS` or `BLOCK` with Critical, Important, and Minor findings.

## Frozen identities

| Path | SHA-256 |
| --- | --- |
| `scripts/agent_plus_manager.py` | `f41a7111f73181442bd0de08334bb89364874c225548454f49f353d187d59c94` |
| `tests/test_agent_plus_lifecycle.py` | `99945656c0e5a0dc4f1c783d6357666443ac23360437e334cc52c5b37863c3f1` |
| `tests/test_agent_plus_legacy_adoption.py` | `91043db3fc817a0fc03fd269a80572d5f3792d02e40f13e6052392c19793217f` |
| `.agent-plus/engineering-boundaries.json` | `33841697f2b07eac0f9331bc3e7b490dd267b32eaeaf0ad320e679848e155853` |
| `.agent-plus/agent-plus-0-4-0-static-typing-repair-task-001.json` | `9f1f098f4aee048cc9bd8fc421b64cc5e5b986f299d818a64c5d6b4a100c3278` |
| Repair necessity | `53711e1be36818d495b1cb4c925a6919793040528f77ef1910fd52a41effac78` |
| Maker and evaluator receipt | `20e9e09bb948d0d9e94c886a0637e7456a7e4030b99adb386abfc5a52054478e` |

## Deterministic baseline

- Strict mypy: `PASS` on three production files.
- Ruff: `PASS` on changed implementation and tests.
- Lifecycle: `43/43`.
- Legacy adoption: `12/12`.
- Complete public suite and validator: `164/164`.
- Python compilation, canonical/bootstrap bindings, privacy, links, and diff checks: `PASS`.
- Exact repaired candidate scope: `72` paths with manifest SHA-256
  `1293401367fa7a26d62ec058184b3a4720d92b64bf2587be5bf89e4bc8836b07`.
- Disposable simulated `VERSION=0.4.0`: public validator `164/164`, strict mypy, Ruff, exact staged
  path equality, and unchanged real index all `PASS`.

## Stop conditions

- Stop with `BLOCK` for any new behavior freedom, manifest ambiguity, untyped failure, incomplete
  matrix, failed simulated release version, or frozen hash mismatch.
- Do not modify implementation, tests, ledger, state, version, Git, release, or consumers.

## Closeout command

```sh
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-0-4-0-static-typing-repair-review-001.json \
  --require-complete-engineering-review
```
