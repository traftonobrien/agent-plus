---
task: "Publish durable transaction intent before creating workspace assets"
owner_role: "maker"
tier: "2"
time_budget: "90 minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Sol maker; deterministic evaluator; separate fresh reviewer required"
reasoning: "implementation"
authorization_scope: "Owner authorized a new attempt for the attempt-05 review BLOCK on 2026-08-21"
ownership_map: "Sol owns maker and evaluation; a fresh reviewer owns review; owner owns release"
chain_stages: "registered attempt-06 -> red regression -> maker -> evaluator -> fresh reviewer -> owner decision"
concurrency: "one writer; no parallel work"
tool_budget: "maker 40 calls or 90 minutes; reviewer 25 calls or 60 minutes"
context_budget: "40K ceiling; 15-25K implementation target"
reserve_use: "hard-architecture reserve approved"
checkpoint_interval: "stop at maker, evaluator, or reviewer BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this card, regression test, validator output, review packet, and promotion dossier"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "focused lifecycle tests; full validator; Ruff; strict mypy; compilation; shell syntax; diff check"
fresh_verifier_contract: "fresh read-only reviewer runs the complete matrix and returns one PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-atomic-setup-task-006.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-atomic-setup-review-006.json"
---

# Agent+ atomic transaction setup reset

## Necessity

- **Decision:** determine whether transaction setup can avoid all untracked durable workspace
  state.
- **Uncertainty:** whether the journal can become durable before workspace creation and still permit
  safe restart after each setup failure.
- **Existing evidence:** attempt-05 fixed incomplete-journal recovery. Its review found that the
  first journal-write failure leaves an orphan workspace with no recovery route.
- **Minimum action:** publish durable transaction intent before workspace creation. An incomplete
  precommit restart must not require workspace assets.
- **Unlock:** one fresh review decision for Agent+ `0.2.0` lifecycle setup.

## Boundary

- **Allowed artifacts:** lifecycle manager, lifecycle tests, canonical ledger, attempt-06 packets,
  this card, promotion dossier, and hot memory.
- **Allowed actions:** sanitized implementation, disposable attacks, and deterministic checks.
- **Forbidden actions:** SECOND LOOK edits, real project upgrades, data access, scientific work,
  Git operations, release, tag, announcement, or publication.
- **Review mode:** engineering sweep.
- **Architecture decision:** durable transaction intent must exist before workspace assets.
- **Removed caller choice:** setup cannot create an untracked workspace before journal authority.
- **Changed interface:** internal transaction setup order and incomplete-precommit restart cleanup.
- **Consumer discovery:** lifecycle command, Python manager, status, doctor, tests, and generated
  projects.
- **Real-shape smoke:** fail the first journal write, fail workspace creation after a durable
  journal, restart, and verify no orphan or target mutation.
- **Stop condition:** deterministic evaluator or fresh reviewer returns `PASS` or `BLOCK`.
- **Acceptance:** each setup interruption leaves no state or one discoverable journal with a safe
  restart route.

## Decision branches

- **If PASS:** dispatch one fresh independent review. Release remains blocked.
- **If BLOCK:** stop attempt-06. Do not repair or release.

## Initial closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: attempt-06 red regression and maker evaluation
user_visible_outcome: interrupted setup has one discoverable safe restart route
repeat_trigger: deterministic evaluator or fresh reviewer result
```

## Maker and deterministic evaluator — PASS — 2026-08-21

The exact attempt-05 failure first reproduced. A failed initial journal write left an orphan
transaction workspace. `recover` reported no pending transaction and did not remove it.

The setup order now writes durable transaction intent before workspace creation. If the first
journal write fails, no workspace exists. If workspace creation fails later, the journal remains
discoverable. Recovery selects safe abort without requiring workspace assets and removes all setup
state.

Deterministic evidence:

- Exact initial-write regression before the change: orphan workspace reproduced.
- Exact initial-write regression after the change: `PASS`.
- Workspace-creation failure after durable intent: `PASS`.
- Attempt-05 incomplete-snapshot recovery regression: `PASS`.
- Focused lifecycle suite: `26 passed`.
- Full public suite: `90 passed`.
- Public validator, canonical/bootstrap bindings, and links: `PASS`.
- Ruff and strict mypy: `PASS`.
- Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Task guard receipt:
  `sha256:cf904e98ffe6840a7d411fdc3d410fe7cdfde9cb944846cf4f2f31a06f18aaca`.
- Manager SHA-256:
  `1b34c4ca3c039a6946f9cfa55993dc347e9c8addb12058d5de3476b607891ce7`.
- Lifecycle test SHA-256:
  `31c66f63f4df4e64f13302aaafa89aeacb34854fd685d8e44c11ffd1d9890c0f`.

Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

No SECOND LOOK file, real project, Git state, release, tag, announcement, or publication changed.

## Fresh independent review — BLOCK — 2026-08-21

The fresh reviewer completed all `41` lifecycle attacks and all `31` named coverage items. The
attempt-05 orphan-workspace failure is closed. Initial journal failure leaves no workspace.
Workspace failure after journal publication keeps a discoverable safe abort route.

The review found one adjacent setup artifact. If the first journal write fails and removal of its
hidden temporary file also fails, `.agent-plus/.upgrade-transaction.json.<id>.tmp` remains. No final
journal exists. `recover` reports no pending transaction and cannot remove the temporary file.

- Verdict: `BLOCK`.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-atomic-setup-review-record-006.md`.
- Closeout receipt:
  `sha256:63d7c9d447717b4ae3813eebf1f37951494a005ff8ef03f4950c61498037d2ac`.
- Recorded BLOCK result:
  `sha256:faa8285bceb56d0e8c071af01df8c2b1d28d7c3674004ebe3f1e3774d3cea961`.
- Updated ledger digest:
  `sha256:419e359f0a3f687bd14691bcb7949bb84b78c083a6b4d4dd6de945763b625574`.
- Lifecycle BLOCK count: `6`; architecture reset remains required.

Attempt-06 is closed. No further repair, Git operation, release, real-project upgrade, or SECOND
LOOK synchronization is authorized from this result.
