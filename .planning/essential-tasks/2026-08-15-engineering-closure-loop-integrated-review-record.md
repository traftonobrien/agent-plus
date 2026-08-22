# Agent+ Anti-Loop Guard v1 independent integrated review record

Date: 2026-08-15
Reviewer: fresh independent Luna xhigh session; not the maker
Verdict: `AGENT_PLUS_ANTI_LOOP_GUARD_V1_REVIEW_BLOCKED`

## Current state

The guard is not accepted. The maker tests and public validator pass, but reviewer-authored
read-only attacks found defects at the packet parser, ledger loader, architecture-reset boundary,
receipt identity, and mutable ledger writer. The public example remains a process demonstration and
does not unlock scientific execution or any production claim.

## What passed

- Positive engineering, scientific first-error, and live first-error packets were accepted.
- Required-field, malformed scalar, stable-ID, unknown-ID, packet/ledger mismatch, unknown-field,
  ledger BLOCK-count, reset-flag, first/second BLOCK, and third local/bundled repair attacks were
  handled as expected typed failures.
- Missing or incomplete completed-review matrices and the scientific/live continuation attempts
  were rejected. Valid constrained-interface reset controls rejected absolute/parent namespaces,
  empty choices, invalid identifiers, and missing interface fields.
- `python3 -m unittest discover -s tests -p 'test_*.py'`: 16 passed. Public validation passed.
- Bootstrap guard and ledger copies match their canonical hashes; generated-project doctor passed.
- The SECOND LOOK narrow F-16 packet returned `E_THIRD_LOCAL_REPAIR`; the attempt-05 reset packet
  returned the claimed PASS receipt `sha256:66f980eec6bcc0e396ade472d8845a12a53b1e283c6c7a20bec8d2e28e757439`;
  the active policy verifier exited 0.

## What failed or remains

Reviewer temporary matrix: 32 grouped checks; 16 expected controls passed and 16 defects remained.

1. Unhashable `packet_type`, `review_mode`, or `review_status` values raise uncaught `TypeError`
   instead of a typed guard error. The CLI emits a traceback and exits 1.
2. Duplicate JSON boundary or failure-class keys are silently accepted by `json.loads`; the last
   value wins. Duplicate ledger entries therefore do not fail closed.
3. `simplification_trigger.block_count: 2.0` is accepted as the two-BLOCK trigger. The ledger
   itself rejects float/string/boolean counts, but the packet trigger has a numeric type hole.
4. A completed engineering packet accepts arbitrary false or duplicate attack-matrix and named-
   coverage items, including `"No attack was run"` and `"Everything"`.
5. `user_visible_outcome` accepts process-only claims such as `tests pass`, `review complete`, and
   `files changed`, despite the contract requiring a user-visible result.
6. After two BLOCKs, an architecture-reset packet can relabel a local patch in its action text and
   can select any relative namespace (`arbitrary/rehearsal/root`, `foo/./bar`, or `foo//bar`).
   The validator does not prove a fixed approved namespace or prevent semantic relabeling.
7. PASS receipt identity excludes outcome, coverage, matrices, trigger, and action-list content.
   Mutating the user-visible outcome produced the same receipt ID, so the receipt is not bound to
   the reviewed packet contract.
8. Concurrent `--record-block` writers lost updates (16 writers produced 13 in one run). Atomic
   replacement prevents torn bytes but does not provide concurrency-safe BLOCK counting.
9. Recomputed `scripts/anti_loop_guard.py` SHA-256 is
   `ef5cb55baea8dc6a6c4a5b33b8d8df66c1cd7f2b3e4b23b3cfedb0c97e201e70`, while the active SECOND
   LOOK hot-memory claim is `83e720dff429db8e944a0122a8ca68ea6188b5de68bb6dcda1a570cde6af85f1`.
   The persisted hash claim is stale or otherwise unsupported by current bytes.

These are independent promotion blockers. No repair was designed or applied. No certified data,
rehearsal, live Wave B, modeling, promotion, or Git operation occurred.

## Next step

Keep the guard and dependent promotion boundary BLOCKED. Bundle the complete finding set into one
maker repair, then rerun one fresh integrated review; do not authorize a local patch or scientific
execution.

## Technical details

- Guard: `scripts/anti_loop_guard.py` (current SHA-256 above).
- Ledger: `.agent-plus/engineering-boundaries.json`.
- Canonical/bootstrap ledger SHA-256: `303326bc01b6f16a59fe5b24f3d923fe6c3cb226cb01eca83ce3cf4dcbeb9a4b`.
- Canonical/bootstrap guard SHA-256: `ef5cb55baea8dc6a6c4a5b33b8d8df66c1cd7f2b3e4b23b3cfedb0c97e201e70`.
- Maker receipt: `.planning/essential-tasks/2026-08-15-engineering-closure-loop-repair-maker-receipt.md`.
- Review packet: `.planning/essential-tasks/2026-08-15-engineering-closure-loop-integrated-review-packet.md`.
- Reviewer used temporary attack code outside `tests/`; no maker file was edited.

`AGENT_PLUS_ANTI_LOOP_GUARD_V1_REVIEW_BLOCKED`
