# Agent+ Anti-Loop Guard v2 fresh integrated review record

Date: 2026-08-16
Reviewer: one fresh independent integrated review session; not the maker
Verdict: `AGENT_PLUS_ANTI_LOOP_GUARD_V2_REVIEW_BLOCKED`

## Current state

Guard v2 is not accepted. The shared Agent+, bootstrap, and SECOND LOOK guard implementations are
synchronized, and the named engineering controls pass. A reviewer-authored ledger attack found one
decisive authorization defect: a process-only milestone can be inserted into the ledger under a
valid outcome category and then receives a PASS receipt. No production code, F-16 code, protected
root, certified data, rehearsal, modeling, promotion, or Git state was changed.

## What passed

- Guard SHA-256 matched in Agent+, bootstrap, and SECOND LOOK:
  `6a2b8c53560be68fc2aef34129a164a23d70aaa9ec1ef3d217ace9b43105e153`.
- Agent+ and bootstrap ledger SHA-256 matched the packet:
  `9e33d2b67ea2f49d4c9abd2d1733ffcabdede5f04ca3c161b59898c29ea96703`.
  The SECOND LOOK ledger matched its packet identity:
  `1a4752d1f587a780fb957c7a8c16609850f15aadae547e5685c96c3e1c6d5c3d`.
- Reviewer-authored attacks rejected disguised outcome text, invalid outcome kinds, reset
  relabeling, unauthorized namespaces and attempts, non-string keys at multiple depths, unknown
  fields, unsupported schema versions, deep nesting, wrong counters, and malformed CLI JSON.
- Architecture-reset requirements remained fail-closed at BLOCK count 2. Execution remained bound
  to scientific/live review modes and `stop_first_error`; execution at a reset boundary was
  rejected.
- PASS receipts were deterministic across key order and Agent+/bootstrap CLI copies, bound the
  complete ledger and normalized packet, and remained unchanged after caller mutation.
- Completed matrices and failure-class coverage rejected undeclared or incomplete items. Two
  concurrent BLOCK writers reached count 2 without a lost update. A torn ledger returned a typed
  malformed-ledger error. No v1 keyword, relabel, or free-text fields remain reachable in the guard.
- `scripts/validate-public-package.sh`: PASS (41 focused tests and package checks).
  Generated-project initialization plus doctor: PASS. SECOND LOOK policy verifier:
  `AI_WORKFLOW_POLICY_OK`. Ruff with the packet's `--line-length 100 --select E,F,I,UP,B,SIM`
  settings and strict mypy passed for the changed guard copies.

## What failed or remains

1. **Ledger-side process outcome bypass.** For each of `tests-passed`, `lint-passed`,
   `files-written`, `docs-updated`, and `review-complete`, the reviewer changed only a scratch
   ledger's `permitted_outcomes` map to declare the identifier as
   `user_visible_capability`, then supplied that exact identifier and enum value in an otherwise
   valid engineering packet. `validate_packet` returned a PASS receipt for every case:

   - `tests-passed`: `sha256:f1b9da43cb892eba885d483ffeced0f2b0995cf79c77441aaf76a945c4b6415c`
   - `lint-passed`: `sha256:4bf310321a6df36fe6ae7997dfa72ca4942bf1cd0c10127d1ae9fb4463e255a1`
   - `files-written`: `sha256:d299dbf1637ccd26126d90194ba34b3419cde19e3d0a09ae043329091954ebb7`
   - `docs-updated`: `sha256:3594864b3092256204b2daa5caad8ca66ebad55b2ef616b99fcd83197e50d3ec`
   - `review-complete`: `sha256:cf866704e9c5f71bedc56665de559a93b9763302fa06e0af28bf0b6d8eda362f`

   This defeats the stated v2 guarantee that process work has no outcome category. The closed
   enum only checks the category string; it does not prevent the ledger from assigning a
   process-only identifier to a valid category. Because the ledger is the authorization source,
   this is a decisive semantic authorization defect, not a wording-only packet attack.

## Next step

Keep Agent+ Guard v2 and the SECOND LOOK dependent boundary BLOCKED. Bundle the ledger-side outcome
closure with the existing v2 repair boundary, then obtain one fresh integrated review. Do not
authorize F-16 rehearsal, Wave B, certified-data reads, modeling, live execution, or promotion.
Do not apply a reviewer-designed repair in this record.

## Technical details

- Review scope: Agent+ canonical guard and ledger, bootstrap copies, SECOND LOOK consumer copy,
  prior v1 attack families, and the v2 packet's new attack families.
- The process-ID attacks used independent in-memory scratch ledgers; the repository ledger bytes
  were not modified.
- No persistent reviewer test file or temporary repository file was created.
- Historical v1 review records remain superseded evidence; this record is the current v2 verdict.

`AGENT_PLUS_ANTI_LOOP_GUARD_V2_REVIEW_BLOCKED`
