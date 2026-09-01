# Agent+ active-chain lifecycle delivery maker receipt

Date: 2026-08-30

Outcome: `PASS — MAKER AND DETERMINISTIC EVALUATION COMPLETE; FRESH REVIEW REQUIRED`.

## Delivered result

- New initialization delivers and manages `scripts/active_chain_guard.py` and the sanitized example.
- Manifest schema v2 binds each installation to one exact managed-set identity.
- Exact v1 manifests from released `0.2.0` and `0.3.0` remain valid historical inputs.
- Status reports an update when the version matches but the managed-set generation is historical.
- Upgrades permit additive managed-set changes only.
- Candidate-only files use no-replace publication and cannot overwrite unmanaged files.
- Recovery removes only additions that the transaction committed.
- Recovery preserves uncommitted collision files and blocks changed committed additions.
- Upgrade and recovery preserve required executable modes.
- Canonical and copied doctor routes verify exact managed sets, digests, paths, and command modes.

## Deterministic evidence

- Lifecycle suite: `42/42` passed.
- Legacy-adoption suite: `12/12` passed.
- Active-chain suite: `17/17` passed.
- Anti-loop suite: `54/54` passed.
- Workflow-default suite: `7/7` passed.
- Complete public suite: `163/163` passed.
- Public-package validator: `PASS` with `163/163` tests.
- Python compilation, shell syntax, JSON parsing, link checks, privacy checks, and diff checks: `PASS`.
- Canonical/bootstrap active-chain guard and example bindings: `PASS`.
- Bootstrap context command executable-mode check: `PASS`.
- Task admission receipt:
  `sha256:5534cfc8e2af9a2a62192d933f4ceed047a0c2d9f094383f7fc0cc2507defe92`.

## Clean synthetic lifecycle proof

- Current init: manifest v2, managed set `agent-plus-active-chain-v1`, `15` managed files.
- Guard and example delivery: `PASS`.
- Current doctor and status: `0`, `0`.
- Context, doctor, and active-chain guard executable modes: `PASS`.
- Historical v1 status: `3` with an available managed-set update.
- Historical v1 additive upgrade: `0`.
- Post-upgrade manifest: v2 with `15` managed files.
- Post-upgrade doctor: `0`.

## Implementation identities

- `scripts/agent_plus_manager.py`:
  `9b1098be3287b01e991506a1ad00fbea2a0957ae1dcbff0696fbd900bd1cfca2`.
- `scripts/agent-plus-init.sh`:
  `91f9f6ddb6df4a747ed224738ce6fefe3078b470666772f7d397e65367597e09`.
- `scripts/agent-plus-doctor.sh`:
  `146f0977b0db79b255b0a0fa311d425d223d85da890ffc505ce2e92aa5d72c76`.
- `tests/test_agent_plus_lifecycle.py`:
  `8b56761558aa16d90eaecea111d59fe1b3d9748afcb5754bafde994506df549d`.
- `tests/test_agent_plus_legacy_adoption.py`:
  `177876f5a591db60f73450222bc52ac7c5c50897beb305c8e6b7611ebb9fe34c`.
- `bootstrap/base/scripts/ai-context.sh`:
  `c1a56ca2fe38d4cbc48db12b76052cea99c63047162523f413f42ed14d04f8c3`.

## Boundary sweep additions

The initial delivery defect exposed three adjacent lifecycle conditions. The same packet now covers
all three:

1. Transaction copies previously removed executable modes.
2. A collision created after preflight must remain project-owned during recovery.
3. A committed addition changed before recovery must block deletion and retain durable recovery state.

## Small correction record

The first focused test command used module names for a non-package test directory. It failed before
test collection. The corrected discovery commands passed without an implementation change.

## Limits

- The maker does not certify this work.
- Managed-file removal remains unsupported.
- No release, version change, Git operation, consumer synchronization, proving-project change, data
  access, or scientific work occurred.
- One fresh independent reviewer must complete the registered attack and coverage matrices.

## Restart

```sh
./scripts/ai-context.sh
```
