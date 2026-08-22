---
task: "Replace the Agent+ lifecycle state module and add the portable output contract"
owner_role: "maker"
tier: "2"
time_budget: "120 minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Sol maker; deterministic evaluator; separate fresh reviewer required"
reasoning: "implementation"
authorization_scope: "Owner authorized all proposed Agent+ updates on 2026-08-21"
ownership_map: "Sol owns this maker and deterministic evaluation; a separate fresh reviewer owns review; owner owns release"
chain_stages: "registered attempt-04 -> maker -> deterministic evaluator -> fresh reviewer -> owner release decision"
concurrency: "one writer; no parallel work"
tool_budget: "maker 50 calls or 120 minutes; reviewer 25 calls or 60 minutes"
context_budget: "40K ceiling; 15-25K implementation target"
reserve_use: "hard-architecture reserve approved"
checkpoint_interval: "stop at the first maker or evaluator BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this card, tests, validator output, and promotion dossier"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "focused lifecycle and output tests; full validator; Ruff; strict mypy; compilation; shell syntax; diff check"
fresh_verifier_contract: "fresh read-only reviewer completes the full registered matrix and returns one PASS or BLOCK"
promotion_dossier: ".planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md"
anti_loop_packet: ".agent-plus/agent-plus-0-2-0-clean-room-task-004.json"
review_closeout: ".agent-plus/agent-plus-0-2-0-clean-room-review-004.json"
---

# Agent+ clean-room system update

## Necessity

- **Decision:** determine whether Agent+ `0.2.0` can safely install its complete control set and
  make the accepted plain-language output behavior portable.
- **Uncertainty:** whether one replacement lifecycle state contract can reject incomplete recovery
  records, preserve lock ownership, and manage every required file without reopening prior path
  escapes.
- **Existing evidence:** attempt-03 closed the old path escapes but lost managed files, accepted an
  incomplete recovery set, and removed another process's lock. The public output policy is also
  absent from the generated-project template and lifecycle manifest.
- **Minimum action:** replace the lifecycle state and lock interfaces, define one complete managed
  release contract, and add one portable output policy across supported agent runtimes.
- **Unlock:** one fresh review decision for Agent+ `0.2.0`.

## Boundary

- **Allowed artifacts:** canonical and bootstrap output controls; supported runtime adapters;
  lifecycle manager, initializer, doctor, validator, tests, documentation, this card, registered
  packet, ledger, promotion dossier, and hot memory.
- **Allowed actions:** sanitized public-safe implementation and deterministic checks.
- **Forbidden actions:** edits to SECOND LOOK; data access; scientific work; real project upgrades;
  commit, push, tag, release, or announcement before fresh review PASS.
- **Review mode:** engineering sweep.
- **Failure-class coverage:** the complete registered `portable-lifecycle-integrity` matrix, with
  direct coverage for output policy management, exact recovery sets, and replacement lock ownership.
- **Simplification trigger:** attempt-04 is one replacement. Any evaluator or reviewer BLOCK stops
  the chain. No local correction follows.
- **User-visible outcome:** a new Agent+ project receives clear everyday-language rules and can be
  installed, checked, updated, and recovered without mixed control files.
- **Stop condition:** deterministic evaluator or fresh reviewer returns `PASS` or `BLOCK`.
- **Stop behavior:** complete the named engineering matrix when safe, then stop on the verdict.
- **Attack matrix:** registered ledger order; pending.
- **Named coverage:** registered ledger order; pending.
- **Promotion dossier:** `.planning/essential-tasks/2026-08-21-agent-plus-0-2-0-release-promotion-dossier.md`.
- **Dispatch guard:** attempt-04 task packet must return a guard PASS receipt before implementation.
- **Review closeout guard:** a complete review packet must pass closeout validation before release.
- **Changed interfaces:** managed release file set, transaction journal schema, lock lease, output
  policy, and platform activation files.
- **Consumer discovery:** canonical package, bootstrap template, initializer, lifecycle manager,
  doctor, validator, tests, Codex, Claude, Cursor, and SECOND LOOK after release.
- **Consumer closure:** every discovered consumer must be updated or explicitly kept as a project
  adapter.
- **Runtime wrappers:** shell CLI plus Python lifecycle manager.
- **Real-shape smoke:** initialize a disposable project, run doctor and status, perform update and
  recovery attacks, and verify the installed output rules.
- **Repeat trigger:** a complete evaluator or fresh reviewer result.
- **Acceptance:** all focused and full checks pass with no external mutation, mixed recovery,
  missing managed control, or foreign lock removal.

## Decision branches

- **If PASS:** prepare one fresh independent review. Release remains blocked.
- **If BLOCK or FAIL:** stop attempt-04. Do not repair or release.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: attempt-04 deterministic evaluation
user_visible_outcome: Agent+ output and lifecycle controls enter one replacement implementation
repeat_trigger: deterministic evaluator or fresh reviewer result
```

## Maker and deterministic evaluator — PASS — 2026-08-21

The replacement uses transaction journal schema `agent-plus-upgrade-transaction/v2` and a
kernel-owned file lease. The lease file remains in place and is never unlinked during release.
The journal owns exact managed, recovery, candidate, commit, and progress sets. Recovery validates
the complete snapshot and journal before the first target write.

The complete managed release now includes `AI_AGENT_OUTPUT_POLICY.md`, the Cursor always-on rule,
the interface-consumer guard, and its test. The output policy is byte-identical in canonical and
bootstrap roots. Codex, Claude, and Cursor receive portable activation rules without a required
external plugin.

Direct regression evidence:

- A shortened recovery set is rejected without recovery writes or false success.
- A coordinated journal subset cannot redefine the Agent+ release.
- Lock release preserves a replacement owner's lock bytes.
- A generated project manages and drift-checks the output policy, Cursor rule, interface guard,
  and interface-guard test.

Deterministic evidence:

- Focused lifecycle suite: `23 passed`.
- Full public suite: `87 passed`.
- Public package validator, canonical/bootstrap bindings, and links: `PASS`.
- Ruff, strict mypy, Python compilation, shell syntax, and `git diff --check`: `PASS`.
- Manager SHA-256:
  `ff45319592cde6c0c091d9f49414a1afd21275a821ba74cd84796f32a68f1265`.
- Output policy SHA-256 in both roots:
  `01cfc67c10179fc2212f0965434862150e418fd648cc5f628e200ad9d4ebd338`.
- Attempt-04 task receipt:
  `sha256:e40f01591ee56b5d86994e79791c0cb36392d14403a190b910435791e5a223c6`.
- Planned fresh-review receipt:
  `sha256:5c377ca184a6b06241d0c82de463fea2d8ddee099ed614d4f1f0eb0f645cf9d1`.

Status: `MAKER_AND_DETERMINISTIC_EVALUATOR_PASS — FRESH REVIEW REQUIRED`.

No reviewer was dispatched. No SECOND LOOK file, real project, Git state, release, tag,
announcement, or downstream synchronization changed. Release remains blocked.

## Fresh independent review — BLOCK — 2026-08-21

The fresh Luna xhigh reviewer completed the full registered review boundary. All `39` lifecycle
attack items and all `29` named coverage items were closed in exact ledger order. The public suite
passed `87` tests, and validator, compilation, shell syntax, and diff checks passed.

The review found one adjacent lifecycle failure. If the durable journal write fails while recording
snapshot progress, the retained journal can remain in `SNAPSHOTTING` with no recovery digest for a
managed file. A later `recover` indexes that missing digest and raises raw
`KeyError: '.agent-plus/PROFILE.md'`. This violates the typed error, durable journal, and transaction
state controls.

- Verdict: `BLOCK`.
- Review record:
  `.planning/essential-tasks/2026-08-21-agent-plus-clean-room-review-record.md`.
- Closeout receipt:
  `sha256:c52086932d1d4abc7ae6ca2f805e7c83e46f5f6081ea4377e50e79fdb53faaa0`.
- Recorded BLOCK result:
  `sha256:2a2c60d23299e76c7eb4174b0c14ee0dfe0117f49e3ecca69221b94e1ad6c410`.
- Canonical ledger digest:
  `sha256:20302450a22a76a0210b4822ca79911525ac01cf8cbe60106aaa763c1feb5bff`.
- Lifecycle BLOCK count: `4`; architecture reset remains required.

Attempt-04 is closed. No repair, Git operation, release, announcement, real-project upgrade, or
SECOND LOOK synchronization is authorized from this result. The next step is an owner decision to
hold `0.2.0` or authorize a new necessity and architecture decision.
