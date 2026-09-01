# Agent+ active-chain lifecycle review 001 packet

Date: 2026-08-30

Status: `READY FOR FRESH INDEPENDENT REVIEW`.

## Review decision

Decide whether the lifecycle-delivery candidate closes every registered attack without weakening
manifest exactness, project-owned state, transaction recovery, or release authority.

The reviewer must inspect the current files and deterministic receipts. The reviewer must not use
the maker transcript as evidence and must not repair the candidate.

## Required scope

- Complete all `27` attack items in
  `.agent-plus/agent-plus-active-chain-lifecycle-review-001.json`.
- Complete all `18` named coverage items.
- Run independent probes for current init, historical v1 status, additive upgrade, collision,
  partial commit recovery, copied doctor, executable modes, and manifest or journal forgery.
- Confirm that project-owned state remains unchanged.
- Confirm that managed-file removal, release, Git mutation, and consumer synchronization remain
  outside the candidate.
- Return `PASS` or `BLOCK` with Critical, Important, and Minor findings.

## Frozen implementation identities

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

The canonical and bootstrap active-chain guards remain byte-identical at
`3784a41abe967c4d964c268ca999ebe202dbf9a5639382feaa16023197c04389`.
The canonical and bootstrap examples remain byte-identical at
`2cb9cd7b6219de1f4065efce8af269f5bd67e33809e0cce01610cda7b38e04eb`.
The bootstrap context command must also have an executable mode.

## Deterministic baseline

- Lifecycle: `42/42`.
- Legacy adoption: `12/12`.
- Active chain: `17/17`.
- Anti-loop: `54/54`.
- Workflow defaults: `7/7`.
- Complete public suite: `163/163`.
- Public validation: `PASS`.

## Stop conditions

- Stop with `BLOCK` for any unsafe overwrite, deletion, recovery cleanup, manifest ambiguity,
  project-owned mutation, untyped failure, missing attack, or incomplete named coverage.
- Do not modify implementation files.
- Do not release, mutate Git, access a consumer, or synchronize a project.

## Closeout command

After the review JSON contains the complete exact matrices, run:

```sh
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-active-chain-lifecycle-review-001.json \
  --require-complete-engineering-review
```
