---
task: "Add a versioned Agent+ audit and synchronization skill"
owner_role: "maker"
tier: "2"
time_budget: "60 minutes"
attempt_limit: 1
orchestration_mode: "standard"
exact_model: "Sol maker and deterministic evaluator; fresh review required before release"
reasoning: "implementation"
authorization_scope: "Owner requested a reusable sync skill for future repositories and SECOND LOOK"
ownership_map: "Sol owns the skill and public routing; a fresh reviewer must own acceptance"
chain_stages: "necessity -> maker -> deterministic evaluator -> fresh review -> owner release decision"
concurrency: "one writer; no parallel work"
tool_budget: "32 calls or 60 minutes"
context_budget: "25K ceiling; 8K-15K implementation target"
reserve_use: "not used"
checkpoint_interval: "return after deterministic evaluation"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this card, skill validation, public validator, and later review record"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "skill validation; public validator; lifecycle tests; diff check"
fresh_verifier_contract: "review exact-tag authority, audit-first behavior, mutation authorization, recovery stop, preservation checks, discovery, and public safety"
promotion_dossier: "this task card"
anti_loop_packet: ".agent-plus/agent-plus-sync-task-001.json"
review_closeout: ".agent-plus/agent-plus-sync-review-001.json"
---

# Agent+ sync skill

## Necessity

- **Decision:** provide one reusable skill that audits and updates an installed Agent+ project from
  an exact official release.
- **Uncertainty:** make the workflow easy to invoke without duplicating the reviewed transaction
  manager or granting silent mutation and recovery authority.
- **Existing evidence:** Agent+ already has status, doctor, upgrade, and recover commands. Consumer
  repositories do not have one guided skill that resolves release authority, preserves local state,
  and records a calibrated result.
- **Minimum action:** add one instruction-only skill, router discovery, install guidance, and public
  validation binding.
- **Unlock:** after release, a consumer can install `$agent-plus-sync`, audit its Agent+ installation,
  and request one exact-version transactional update.

## Boundary

- **Allowed artifacts:** `skills/agent-plus-sync/`, Agent+ router, README, bootstrap guide, public
  validator, this card, and later review records.
- **Allowed actions:** public-safe instructions and deterministic validation.
- **Forbidden actions:** SECOND LOOK edits, a real consumer upgrade, Git release actions, lifecycle
  manager changes, editorial changes, scientific work, modeling, or silent network mutation.
- **Changed interface:** one new optional skill and one Agent+ router route.
- **Consumer discovery:** public README, bootstrap guide, router skill, skill metadata, and validator.
- **Stop condition:** deterministic evaluation or fresh review returns `PASS` or `BLOCK`.
- **Acceptance:** the skill validates, the public package passes, existing lifecycle tests pass, and
  one fresh reviewer accepts the audit, sync, verification, recovery-stop, and state-preservation
  contract.

## Decision branches

- **If maker or evaluator BLOCK:** stop and preserve the finding.
- **If reviewer BLOCK:** do not repair in the same review chain.
- **If reviewer PASS:** return for an explicit release decision.

## Maker and deterministic evaluator — PASS — 2026-08-22

Status: `AGENT_PLUS_SYNC_SKILL_MAKER_COMPLETE — FRESH REVIEW REQUIRED`

Implemented:

- Added `$agent-plus-sync` with read-only `audit`, authorized `sync`, and post-update `verify` modes.
- Required an exact official release tag and rejected untagged branches and dirty release checkouts.
- Routed all mutation through `scripts/agent-plus upgrade` instead of duplicating lifecycle logic.
- Preserved the one-authorization rule. An error stops without fallback, retry, or same-chain
  recovery.
- Added pre/post hashes for named project-owned controls and required post-sync status and doctor
  checks.
- Added Agent+ router, README, bootstrap install, and public-validator discovery.

Deterministic evidence:

- Skill validation: `PASS`.
- Full public package: `99 passed`; bindings, links, and package validation `PASS`.
- Focused lifecycle suite: `29 passed`.
- Scoped diff check: `PASS`.

Limits:

- No consumer repository, SECOND LOOK file, release tag, Git remote, or real installation changed.
- No lifecycle manager or accepted editorial file changed.
- One registered fresh review remains required before this skill can enter a release.

## Release-candidate evaluator — BLOCK — 2026-08-22

Status: `EVALUATOR_BLOCK — REVIEW AND RELEASE NOT DISPATCHED`

The one unattended release-candidate evaluator completed 10 gates and stopped at `ruff`. The
terminal record is `outputs/release-candidate-evaluator/terminal.json`, with the process log named
in that record. One terminal-result check occurred after process return. The log was not inspected.

The completed gates covered both skill validations, editorial tests, lifecycle tests, anti-loop
tests, the full public package, sync task and review dispatch guards, and refreshed lifecycle and
editorial closeout guards against the expanded ledger.

No repair, retry, fresh review, staging, commit, tag, push, release, consumer upgrade, or SECOND
LOOK edit followed. A bounded diagnosis and correction require new explicit authorization.

## Authorized Ruff correction and evaluator run-2 — PASS — 2026-08-22

The owner authorized one bounded diagnosis, correction, and fresh evaluator run. Ruff found two
exact issues in `scripts/editorial_preservation_check.py`: its shebang lacked executable mode, and
`Iterable` came from `typing` instead of `collections.abc`.

The correction changed only the import source and executable mode. Release-candidate evaluator
run-2 completed all 15 gates with `PASS`. Durable evidence is in
`outputs/release-candidate-evaluator-run-2/terminal.json` and its named log.

Status: `DETERMINISTIC_EVALUATOR_PASS — FRESH INTEGRATED REVIEW REQUIRED`

No fresh review, staging, commit, tag, push, release, consumer upgrade, or SECOND LOOK edit has
occurred.

## Fresh integrated review — PASS — 2026-08-22

Status: `AGENT_PLUS_SYNC_INTEGRATED_REVIEW_ACCEPTED — OWNER RELEASE DECISION REQUIRED`

One fresh Luna xhigh reviewer completed all registered boundaries:

- Agent+ sync: `16/16` attacks and `15/15` named coverage items `PASS`.
- Editorial and subtraction: `12/12` attacks and `11/11` named coverage items `PASS`.
- Portable lifecycle integrity: `42/42` attacks and `32/32` named coverage items `PASS`.
- Public package: `99 passed`; Ruff, strict mypy, compilation, shell syntax, bindings, links, and
  diff checks `PASS`.

Closeout receipts:

- Sync: `sha256:e405c507689d44a2180d483b1650dc0ab67f6faa6e91d54ab3e02036cccf1c41`.
- Editorial: `sha256:04791785ecd6f8790c5644d95fb444b4620a143d95f10245d3454d1e2e5dc210`.
- Terminal recovery: `sha256:33e4abc3c876e6f2e1b4e7f405040b52df6f1dac9e2e476b32ff713355142e8f`.

Review record:
`.planning/essential-tasks/2026-08-22-agent-plus-sync-integrated-review-record.md`.

No staging, commit, tag, push, release, consumer upgrade, or SECOND LOOK edit occurred. The owner
must make the separate release decision.
