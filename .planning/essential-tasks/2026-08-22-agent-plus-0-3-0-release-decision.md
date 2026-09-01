---
task: "Publish the accepted Agent+ outcome-audit and legacy-adoption boundaries as v0.3.0"
owner_role: "owner release decision"
tier: "3"
time_budget: "45 minutes"
attempt_limit: 1
orchestration_mode: "standard"
exact_model: "Sol controller; deterministic release evaluator; no maker or duplicate reviewer"
reasoning: "release promotion"
authorization_scope: "Owner command continue after the exact Agent+ release decision was named"
ownership_map: "Sol owns exact scope and release operations; accepted reviewers own engineering evidence; owner owns publication"
chain_stages: "scope freeze -> temporary-index evaluation -> exact staging -> commit -> annotated tag -> push -> GitHub release -> remote verification"
concurrency: "one controller; no parallel writer"
tool_budget: "one release attempt; stop at first failure"
context_budget: "bounded to accepted records and release surfaces"
reserve_use: "not used"
checkpoint_interval: "one check at each irreversible boundary"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this card, accepted integrated reviews, Git commit/tag, and GitHub release"
return_check: "verify remote main, peeled annotated tag, and public GitHub release"
polling_policy: "not-applicable"
evaluator_commands: "review closeout guards; frozen hashes; full public validator; compile; shell syntax; diff check; temporary-index scope"
fresh_verifier_contract: "reuse unchanged hash-bound outcome-audit and legacy-adoption integrated PASS records"
promotion_dossier: ".planning/essential-tasks/2026-08-22-agent-plus-0-3-0-release-decision.md"
anti_loop_packet: "accepted boundary packets only; no implementation dispatch"
review_closeout: "outcome receipt ef242f6a; legacy receipt 09058cb3"
---

# Agent+ 0.3.0 release decision

## Necessity

- **Decision:** publish the two accepted post-0.2.0 public capabilities as one exact release.
- **Uncertainty:** whether the dirty worktree can be reduced to one complete public-safe release
  scope without local outputs, locks, editor metadata, or consumer state.
- **Existing evidence:** outcome-audit attempt 04 and legacy-adoption attempt 003 each have complete
  deterministic evaluation and fresh independent integrated `PASS` records.
- **Minimum action:** freeze one explicit file scope, evaluate it through a temporary Git index,
  publish one annotated release only if every gate passes, and verify the remote identities.
- **Unlock:** an exact official release that SECOND LOOK may separately audit and adopt.

## Boundary

- **Allowed artifacts:** accepted outcome-audit and legacy-adoption implementation, tests, public
  docs, canonical ledger and packets, public planning evidence, `VERSION`, public state, and hot
  memory.
- **Allowed actions:** set version `0.3.0`; run deterministic release checks; stage only the exact
  accepted scope; create one commit and annotated tag; push that commit and tag; publish and verify
  one public GitHub release.
- **Forbidden actions:** include `outputs/`, the ledger lock, editor/macOS metadata, local registry,
  private paths, consumer state, SECOND LOOK files, scientific artifacts, or any unreviewed repair.
- **Review mode:** release promotion from unchanged accepted engineering evidence.
- **Failure-class coverage:** public scope completeness, frozen accepted bytes, privacy, exact tag
  identity, remote publication, and exclusion of local-only files.
- **Simplification trigger:** any scope ambiguity or failed gate stops the one release attempt.
- **User-visible outcome:** Agent+ users can install an exact official release containing the
  outcome-audit and legacy-adoption capabilities.
- **Stop condition:** verified public release `PASS` or first release error `BLOCK`.
- **Stop behavior:** fail closed at the first release error; do not retry or repair in this chain.
- **Attack matrix:** changed-file inventory; excluded-file inventory; frozen hashes; both closeout
  guards; complete test suite; public validator; compilation; shell syntax; diff check; temporary
  index; remote base; absent target tag; pushed commit; peeled tag; public release.
- **Named coverage:** version, manager, doctors, contexts, bootstrap, outcome skill, tests, routing,
  docs, validator, ledger, evidence records, release notes, remote identities.
- **Promotion dossier:** this file.
- **Dispatch guard:** not applicable; no maker or reviewer is dispatched.
- **Review closeout guard:** both accepted complete packets must reproduce their closeout `PASS`.
- **Changed interfaces:** none beyond the already accepted outcome-audit and legacy-adoption
  interfaces.
- **Consumer discovery:** accepted integrated reviews bind every named consumer.
- **Consumer closure:** accepted integrated reviews report complete coverage.
- **Runtime wrappers:** existing lifecycle subprocess boundary only.
- **Real-shape smoke:** accepted disposable legacy targets plus the complete public suite.
- **Repeat trigger:** any changed accepted byte, failed release command, tag collision, remote drift,
  or GitHub publication mismatch.
- **Acceptance:** exact public scope; all deterministic gates `PASS`; remote main and peeled tag equal
  the release commit; GitHub release is public, not draft, and not prerelease.

## Decision branches

- **If PASS:** record the exact release identity and stop before consumer synchronization.
- **If BLOCK or FAIL:** preserve the worktree and report the exact failed gate; do not retry.

## Deterministic preflight — PASS

- Exact release scope: `41` files.
- Sorted file-name manifest SHA-256:
  `46da1516e26246377c197e9b5e845931310aad43ab191f25687bc04ef0df753e`.
- The temporary index matched the explicit scope exactly and passed staged diff checks.
- Complete public suite: `128/128 PASS`.
- Public-package safety, canonical/bootstrap bindings, and internal links: `PASS`.
- Python compilation, POSIX shell syntax, and worktree diff checks: `PASS`.
- Outcome-audit and legacy-adoption closeout guards: `PASS` against the current canonical ledger.
- Frozen accepted implementation and review hashes: exact.
- Remote `main` equals the local base commit
  `7e07511a8620f6447f3e6817379d62fa5f94726e`.
- Tag and GitHub release `v0.3.0`: absent before publication.
- Excluded local-only paths remain outside the scope: `outputs/`, ledger lock, macOS/editor
  metadata, local registry, consumer state, and SECOND LOOK.

Status: `AGENT_PLUS_0_3_0_RELEASE_READY — ONE AUTHORIZED PUBLICATION ATTEMPT`.

## Publication and remote verification — PASS

- Release commit:
  `ea147c0e2b2dac481238f96c37b56a31fe65033b`.
- Annotated tag: `v0.3.0`.
- Atomic push of `main` and `v0.3.0`: `PASS`.
- Remote `main` and the peeled annotated tag both resolve to the release commit.
- Public GitHub release:
  `https://github.com/traftonobrien/agent-plus/releases/tag/v0.3.0`.
- GitHub state: public, not draft, and not prerelease.
- The only remaining untracked paths are the preserved local ledger lock, macOS/editor metadata,
  and generated `outputs/`; none entered the release.
- No consumer synchronization, SECOND LOOK edit, scientific work, or modeling followed.

Status: `AGENT_PLUS_0_3_0_RELEASED — CONSUMER SYNCHRONIZATION REQUIRES SEPARATE AUTHORIZATION`.

## Closeout

```yaml
decision_changed: yes
blocker_closed: exact official post-0.2.0 release absent
work_unlocked: separate SECOND LOOK adoption audit
user_visible_outcome: Agent+ 0.3.0 is an exact public release
repeat_trigger: explicit consumer synchronization authorization or changed release state
```
