---
name: outcome-audit
description: Record closed prospective workflow outcomes, report honest reliability measures, and verify a sanitized private-evidence receipt through a fixed project-local layout.
---

# Agent+ Outcome Audit

## Trigger

Use when a project needs prospective workflow outcome measures or an independent review needs a
sanitized receipt for private evidence. Do not reconstruct outcomes from chat, transcripts, or
ambiguous historical notes.

## Purpose

This optional file-based skill keeps workflow outcomes separate from scientific claims. It uses one
closed record schema, one deterministic scorecard, and one fixed private-evidence receipt boundary.
It does not add a service, database, dashboard, scheduler, transcript parser, or second ledger.

## Required inputs

- A prospective JSON record with `schema_version: agent-plus/outcome-record/v1`.
- Opaque `ref:` identifiers and `sha256:` content digests.
- Ordered `maker`, `evaluator`, and `reviewer` events.
- Separate `work_item` disposition and `scientific` eligibility and status.
- For a private receipt, the current project root with the fixed
  `.agent-plus/outcome-audit/evidence-manifest.json` layout.

## Allowed actions

### Record and validate

1. Create a record with these exact top-level fields:
   `schema_version`, `record_ref`, `work_item_ref`, `attempt_ref`, `created_at`, `events`,
   `work_item`, `scientific`, and `provenance`.
2. Give each event these exact fields:
   `event_ref`, `stage`, `status`, `occurred_at`, `evidence_refs`, `failure_code`, and
   `duration_seconds`.
3. Use a contiguous event prefix in this order: maker, evaluator, reviewer.
4. End a failed attempt at the first `BLOCK` or `ABSTAIN` event. A `BLOCK` event must carry a
   causal failure code and at least one opaque evidence reference.
5. Complete a passing attempt with all three `PASS` events. The tool derives `attempt_outcome`
   and `terminal_failure`. Do not supply either field.
6. Use the fixed CLI from the Agent+ repository:

   ```sh
   python3 skills/outcome-audit/outcome_audit.py validate RECORDS.json
   python3 skills/outcome-audit/outcome_audit.py report RECORDS.json
   python3 skills/outcome-audit/outcome_audit.py abstain --reason AMBIGUOUS_HISTORY
   ```

The validator rejects unknown keys, duplicate JSON keys, skipped or reordered stages, terminal
continuation, duplicate references, invalid digests, contradictory scientific status, and missing
causal authority.

### Report

The report derives first-pass quality, eventual reliability, reviewer escape, eligible scientific
success, causal failure concentration, measured duration, attempts per work item, and multi-attempt
frequency. Reviewer escape means a reviewer `BLOCK` after an evaluator `PASS`. Duration uses only
event `duration_seconds` values that are present for every event in an attempt. It never derives a
duration from timestamps or narrative bounds.

Each rate has a numerator, denominator, rate, and 95% Wilson interval. A zero denominator produces
`null` for the rate and interval. Grades are `UNRATED` unless an owner supplies valid bands before
the report runs:

```sh
python3 skills/outcome-audit/outcome_audit.py report RECORDS.json --bands OWNER_BANDS.json
```

Ambiguous history is an explicit abstention. It is not a failed attempt and does not enter a
denominator.

### Sanitized private-evidence receipt

Run the receipt command from the project root. It accepts no private source path or output path:

```sh
python3 /path/to/agent-plus/skills/outcome-audit/outcome_audit.py receipt
```

The public receipt helpers are also closed and use the current working directory only:

```python
receipt = verify_private_evidence()
receipt = write_fixed_receipt()
```

`write_fixed_receipt()` verifies the current project, creates the generated receipt, and writes
only `.agent-plus/outcome-audit/receipt.json`. It accepts no project root, output path, or caller
receipt payload.

The fixed layout is:

```text
.agent-plus/outcome-audit/evidence-manifest.json
.agent-plus/outcome-audit/evidence/*.json
.agent-plus/outcome-audit/receipt.json
```

The manifest names the exact source set with `source_set_digest`, source digests, item counts, and
one-to-one bindings with `binding_set_digest`. Each
source is strict JSON with `schema_version`, `source_ref`, and `items`; each item has only an opaque
`item_ref` and a `sha256:` `item_digest`. The verifier first enumerates the fixed evidence directory
without following symlinks. Its direct `*.json` regular-file entry set must exactly equal the
manifest source paths. Missing, extra, duplicate, non-JSON, directory, socket, FIFO, device, or
symlink entries block. It then reads regular files without following path components or symlink
leaves. It requires project-root containment and the fixed evidence prefix.

The receipt contains status, non-private counts, content digests, binding digests, and a receipt
digest. It does not contain paths, source references, item references, source content, transcripts,
session identifiers, or domain-specific details. Missing, denied, mismatched, substituted,
traversed, symlinked, duplicate, tampered, or unstructured input returns `BLOCK`. A `BLOCK` result
must not be treated as a reviewer verdict or a promotion decision.

## Required outputs

- A deterministic validation result or typed `BLOCK`.
- A deterministic JSON scorecard with metric denominators and Wilson intervals.
- An explicit abstention for ambiguous history.
- A deterministic fixed-layout receipt with `PASS` or `BLOCK`.
- The exact command, record set, receipt status, and unresolved limitation in the project handoff.

## Acceptance checks

- Closed schemas reject unknown fields, duplicate keys, skipped stages, terminal continuation,
  duplicate refs, and caller-supplied derived outcomes.
- Maker, evaluator, and reviewer authority remains ordered and terminal failure remains causal.
- Attempt outcome, work-item disposition, and scientific status remain separate.
- First-pass, eventual, reviewer-escape, scientific-success, duration, failure, retry, Wilson,
  zero-denominator, and grade behavior pass synthetic tests.
- Receipt omission, substitution, tamper, traversal, symlink, duplicate, count, privacy, and replay
  attacks fail closed or replay byte-for-byte.
- The router, bootstrap guide, and public validator discover this optional skill.

## Handoff requirements

Record the record-set digest, report digest, receipt digest when present, exact commands, `PASS`,
`ABSTAIN`, or `BLOCK`, unresolved findings, and one exact next action. Do not copy private evidence,
private paths, transcripts, or project-specific identifiers into Agent+.

## Explicit limits

- This skill does not infer outcomes from historical narrative.
- It does not parse transcripts or grant reviewer access to private evidence.
- It does not assign scientific or owner grades automatically.
- It does not create a service, database, dashboard, scheduler, second ledger, release, or promotion
  authority.
- A receipt `PASS` is evidence for an independent review. It is not a review verdict.
