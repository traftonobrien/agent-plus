# Agent+ 0.4.0 manifest static-typing repair — maker and evaluator receipt

Date: 2026-08-30

Outcome: `PASS — FRESH REVIEW REQUIRED`.

## Repair

- `scripts/agent_plus_manager.py` now reads the current managed-set identity into a raw local,
  validates its exact string type and registry membership, then assigns the narrowed value.
- `_manifest_set_id` now rejects a non-string current identity with typed `ManagerError` before
  returning it.
- `tests/test_agent_plus_lifecycle.py` directly probes the helper's malformed non-string seam.
- One eligible evaluator correction changed the new regular-expression literal to a raw string
  after Ruff reported an invalid escape. No second correction was needed.

## Deterministic evidence

- Task admission: `PASS` with receipt
  `sha256:756e5792adf3ed0dbf3ee47ddd6f1e2124c86c41b667523d5f26874d42f5620c`.
- Strict mypy: `PASS`, no issues in the manager, active-chain guard, or anti-loop guard.
- Ruff: `PASS` across all changed Python implementation and test files.
- Lifecycle tests: `43/43 PASS`.
- Legacy-adoption tests: `12/12 PASS`.
- Full public suite and validator: `164/164 PASS`.
- Python compilation, canonical/bootstrap bindings, privacy, links, and diff checks: `PASS`.

## Frozen maker identities

- `scripts/agent_plus_manager.py`:
  `f41a7111f73181442bd0de08334bb89364874c225548454f49f353d187d59c94`.
- `tests/test_agent_plus_lifecycle.py`:
  `99945656c0e5a0dc4f1c783d6357666443ac23360437e334cc52c5b37863c3f1`.
- `tests/test_agent_plus_legacy_adoption.py`:
  `91043db3fc817a0fc03fd269a80572d5f3792d02e40f13e6052392c19793217f`.

## Limits

This receipt is maker and deterministic-evaluator evidence only. It does not accept the repair or
authorize version change, staging, commit, push, tag, release, consumer synchronization, data
access, or scientific work. One fresh independent review must complete the registered `8` attacks
and `7` named coverage items.
