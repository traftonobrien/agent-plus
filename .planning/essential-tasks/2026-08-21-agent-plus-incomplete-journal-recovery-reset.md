---
task: "Replace ambiguous incomplete-journal recovery with one safe precommit abort route"
owner_role: "maker"
tier: "2"
time_budget: "90 minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Sol maker; deterministic evaluator; separate fresh reviewer required"
reasoning: "implementation"
authorization_scope: "Owner authorized a new attempt for the attempt-04 review BLOCK on 2026-08-21"
ownership_map: "Sol owns maker and deterministic evaluation; a fresh reviewer owns review; owner owns release"
chain_stages: "registered attempt-05 -> red regression -> maker -> deterministic evaluator -> fresh reviewer -> owner decision"
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
fresh_verifier_contract: "fresh read-only reviewer runs the complete registered matrix and returns one PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-incomplete-journal-task-005.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-incomplete-journal-review-005.json"
---

# Agent+ incomplete-journal recovery reset

## Necessity

- **Decision:** determine whether an interrupted upgrade can always reach one typed, safe restart
  route.
- **Uncertainty:** whether a retained journal from failed snapshot progress can be discarded without
  target writes or mixed installed bytes.
- **Existing evidence:** attempt-04 review left a valid `SNAPSHOTTING` journal with no recovery
  digests. `recover` then raised a raw `KeyError`.
- **Minimum action:** make each accepted journal state select one complete recovery action. An
  incomplete precommit snapshot must select safe abort and cleanup.
- **Unlock:** one fresh review decision for the Agent+ `0.2.0` lifecycle.

## Boundary

- **Allowed artifacts:** lifecycle manager, lifecycle tests, canonical ledger, attempt-05 packets,
  this card, promotion dossier, and hot memory.
- **Allowed actions:** sanitized implementation, disposable attacks, and deterministic checks.
- **Forbidden actions:** SECOND LOOK edits, real project upgrades, data access, scientific work,
  Git operations, release, tag, announcement, or publication.
- **Review mode:** engineering sweep.
- **Failure-class coverage:** the complete registered lifecycle matrix plus incomplete snapshot
  journal recovery.
- **Architecture decision:** a journal state must map to one safe action. Recovery cannot infer
  authority from missing snapshot data.
- **Removed caller choice:** callers cannot treat an incomplete journal as recoverable installation
  authority.
- **Changed interface:** restart behavior for a durable `SNAPSHOTTING` journal.
- **Consumer discovery:** lifecycle command, Python manager, status, doctor, tests, and generated
  projects.
- **Runtime wrapper:** `scripts/agent-plus recover --target`.
- **Real-shape smoke:** fail the journal write after snapshot copy, restart, recover, and verify the
  original installation bytes.
- **Stop condition:** deterministic evaluator or fresh reviewer returns `PASS` or `BLOCK`.
- **Acceptance:** no raw exception, no target mutation, no mixed bytes, no retained journal, and an
  idempotent second recovery.

## Decision branches

- **If PASS:** dispatch one fresh independent review. Release remains blocked.
- **If BLOCK:** stop attempt-05. Do not repair or release.

## Initial closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: attempt-05 red regression and maker evaluation
user_visible_outcome: interrupted upgrades have one typed safe restart route
repeat_trigger: deterministic evaluator or fresh reviewer result
```

## Maker and deterministic evaluator — PASS — 2026-08-21

The red regression injected a persistent journal-write failure after the initial durable journal.
The retained record had state `SNAPSHOTTING`, `snapshot_complete: false`, and no recovery digests.
The old `recover` route raised raw `KeyError: '.agent-plus/PROFILE.md'`.

The lifecycle module now maps each valid durable journal to one restart action. An incomplete
precommit snapshot selects safe abort. Recovery closes the workspace handles, removes the
transaction workspace and journal, and does not write to the installed control files. States after
snapshotting require a complete snapshot during journal validation.

Deterministic evidence:

- Exact red regression before the change: raw `KeyError` reproduced.
- Exact regression after the change: `PASS`.
- Focused lifecycle suite: `24 passed`.
- Full public suite: `88 passed`.
- Public validator, canonical/bootstrap bindings, and links: `PASS`.
- Ruff and strict mypy: `PASS`.
- Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Task guard receipt:
  `sha256:6fd7bb05e1b5eb3e162f9d99b8f4790eacdb566d487518e157c07a76186d5292`.
- Manager SHA-256:
  `a41151fb319f9568175f471393f07028628257e6bf22ab689dcf770f41a2d863`.
- Lifecycle test SHA-256:
  `daa822ec61a992b69c92ab10b97668ea245f93fdb84153f7ba6b3aa37372d57b`.

Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

No SECOND LOOK file, real project, Git state, release, tag, announcement, or publication changed.

## Fresh independent review — BLOCK — 2026-08-21

The fresh reviewer completed all `40` lifecycle attacks and all `30` named coverage items. The
attempt-04 failure is closed. Persistent failure after the initial journal now selects safe abort,
preserves installed bytes, removes the journal and workspace, and permits an idempotent second
recovery.

The review found one earlier setup failure. A low-level failure during the first durable journal
write occurs after workspace creation. It leaves no journal and one orphan transaction workspace.
`recover` reports no pending transaction and does not remove that workspace.

- Verdict: `BLOCK`.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-incomplete-journal-review-record-005.md`.
- Closeout receipt:
  `sha256:6c0a69f685e6242844803fe12808e5eefe74f47c04f091352b6c43a32a95353d`.
- Recorded BLOCK result:
  `sha256:f460a32dea4c204bda7336787485bbf174d7b6b4a1cb04cb7b641c6b4f58afce`.
- Updated ledger digest:
  `sha256:dc6118c554d38d34be521c253ba5a321348b19c519b4f428e945c85a3270cc97`.
- Lifecycle BLOCK count: `5`; architecture reset remains required.

Attempt-05 is closed. No further repair, Git operation, release, real-project upgrade, or SECOND
LOOK synchronization is authorized from this result.
