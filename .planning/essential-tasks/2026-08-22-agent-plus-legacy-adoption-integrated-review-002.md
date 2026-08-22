# Agent+ legacy-adoption integrated review 002

Date: 2026-08-22

Role: fresh independent engineering reviewer

Review mode: engineering sweep

Verdict: `BLOCK`

## Scope and authority

This review assessed only the owner-authorized legacy-adoption repair boundary. The review used
the exact changed bytes, direct consumers, evaluator PASS receipt, and disposable synthetic
targets. The review did not use a maker transcript.

No release, Git action, consumer synchronization, consumer adoption, SECOND LOOK change, or
repair is authorized by this record.

## Input and byte evidence

- Repair packet: `.agent-plus/agent-plus-legacy-adoption-repair-task-002.json`
  `sha256:09334f2a13e2634b69c56cd430abe89169ffe1c83de74f5581b72c8f29d6a765`.
- Evaluator PASS record:
  `.planning/essential-tasks/2026-08-22-agent-plus-legacy-adoption-evaluator-pass-002.md`
  `sha256:08721cac5c5a72bc9afd76fd56f41201fbabff4911e17e423b43b1e2f0fb67fe`.
- Repair dispatch guard receipt:
  `sha256:569419776feddbe4bc659b89ddbbfdf23bf07de13f81b73b129a69a01ca0eed1`.
- Pre-review anti-loop PASS receipt supplied by the dispatch:
  `sha256:385f4b47b44a4c6d181dcddf7b055411c17e9612d8a47115cd6cdb154cda383`.
- All 10 expected changed-file SHA-256 values matched the dispatch packet.
- Reviewer evidence:
  `outputs/agent-plus-legacy-adoption-reviewer-002/matrix.json`.

## Deterministic checks

- Legacy-adoption tests: `9` passed.
- Lifecycle tests: `29` passed.
- Full public test discovery: `108` passed.
- Public validator: `PASS`.
- The evaluator-reported Ruff, strict mypy, compilation, shell syntax, binding, link, and diff
  checks were accepted as input evidence. No implementation byte differed from the expected
  dispatch hashes.

## Attack matrix

| Registered attack | Outcome | Evidence |
| --- | --- | --- |
| `exact-managed-before-record` | `PASS` | Exact managed bytes were admitted before declaration and manifest publication. |
| `divergent-managed-block` | `PASS` | Divergent managed bytes blocked adoption without declaration or manifest. |
| `project-owned-preservation` | `PASS` | Synthetic project-owned bytes remained unchanged and unmanaged. |
| `fixed-hook-path` | `PASS` | Alternate declaration hook paths were rejected. |
| `hook-failure-before-context` | `PASS` | Canonical doctor, copied doctor, and context rejected exit status `7`; context emitted no managed header. |
| `hook-symlink-and-nonregular-block` | `BLOCK` | Symlink and directory hooks were rejected. A FIFO hook caused `adopt` to exceed the two-second bounded command timeout before the non-regular check. |
| `absent-hook-policy` | `PASS` | Initialized projects accepted an absent optional hook. Legacy adoption rejected an absent required hook. |
| `legacy-doctor-without-initializer-examples` | `PASS` | Canonical and copied doctor passed without initializer-only project examples. |
| `initialized-doctor-unchanged` | `PASS` | Initialized doctor behavior remained unchanged when an optional hook exited `7`. |
| `status-current-requires-exactness` | `PASS` | Current status passed. Managed drift returned non-zero. |
| `upgrade-preserves-adoption-seam` | `PASS` | Upgrade preserved declaration, hook bytes, and project-owned bytes. Doctor and status passed after upgrade. |
| `partial-adoption-fail-closed` | `BLOCK` | Canonical doctor rejected a subset manifest. Copied doctor and context returned success for the same legacy declaration and subset `managed_files` manifest. |
| `public-validator` | `PASS` | `scripts/validate-public-package.sh` passed. |

## Named coverage

| Named coverage | Outcome | Evidence |
| --- | --- | --- |
| `lifecycle-cli` | `PASS` | CLI lifecycle commands ran against disposable targets. |
| `manager-record-and-adopt-interface` | `PASS` | Initializer record and exact-byte adopt interfaces passed. |
| `manifest-schema` | `BLOCK` | Copied doctor and context accepted a subset managed-file manifest. |
| `adoption-declaration` | `PASS` | Closed declaration fields and fixed path were enforced. |
| `context-script` | `BLOCK` | Failing hooks and state routing passed, but subset manifest validation returned success. |
| `project-hook` | `BLOCK` | Symlink and directory checks passed. FIFO open blocked before rejection. |
| `doctor` | `BLOCK` | Canonical doctor rejected the subset manifest. Copied doctor returned `Agent+ doctor: PASS [legacy-adopted]`. |
| `initializer` | `PASS` | Initialized-project behavior and optional hook policy passed. |
| `status` | `PASS` | Current and drift status checks passed. |
| `upgrade-and-recovery` | `PASS` | Adoption seam remained intact through upgrade. |
| `sync-workflow` | `PASS` | Sync guidance names adoption, status, doctor, and upgrade routes. |
| `bootstrap` | `PASS` | Bootstrap context contains the fixed hook and descriptor-bound execution. |
| `public-docs` | `PASS` | README, bootstrap guide, and sync skill contain public adoption guidance. |
| `synthetic-tests` | `PASS` | The focused synthetic suite and reviewer disposable matrix completed. |
| `public-validator` | `PASS` | Public validator passed. |

## Findings

1. **FIFO startup hook can block adoption.**

   The manager opens `.agent-plus/project-startup-check.sh` with `O_RDONLY | O_NOFOLLOW` before
   it calls `fstat`. A FIFO therefore waits for a writer instead of reaching the non-regular-file
   rejection. The standalone copied doctor and both context scripts use the same blocking open
   shape. This violates the required fail-closed non-regular-hook contract.

   Relevant bytes: `scripts/agent_plus_manager.py:654-667`,
   `scripts/agent-plus-doctor.sh:104-129`, `scripts/ai-context.sh:63-92`, and
   `bootstrap/base/scripts/ai-context.sh:65-94`.

2. **Copied doctor and context do not enforce the exact manifest schema.**

   A legacy declaration with a valid schema and profile plus a subset `managed_files` map was
   accepted by the copied doctor and context. The copied doctor checks only that the map is
   non-empty, and context checks only that it is a map. The canonical manager rejects the same
   bytes because it checks the exact managed set. This creates inconsistent consumers and breaks
   the partial-adoption fail-closed contract.

   Relevant bytes: `scripts/agent-plus-doctor.sh:75-103`,
   `scripts/ai-context.sh:48-62`, and `bootstrap/base/scripts/ai-context.sh:50-64`.

## Limitations

- Disposable targets were synthetic and used paths with spaces. No private project state or
  baseball data was used.
- The existing deterministic descriptor-swap test passed within the independent `108`-test run.
  This review did not claim an additional hostile external-process race against the standalone
  shell wrapper.
- The reviewer did not design or implement repair. The two findings remain open.

## Integrated decision

`BLOCK`. The legacy-adoption boundary is not ready for release, consumer adoption, or
synchronization. The next attempt requires a new owner-authorized bundled repair, deterministic
evaluator rerun, and fresh independent review. No same-review repair is permitted.

Exact restart command after new authorization:

```sh
scripts/ai-context.sh
```
