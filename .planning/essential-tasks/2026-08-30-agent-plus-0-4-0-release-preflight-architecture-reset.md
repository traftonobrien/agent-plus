---
task: "Replace ad hoc Agent+ release-candidate export commands with one closed deterministic verifier"
owner_role: "maker, deterministic evaluator, fresh verifier"
tier: "2"
time_budget: "90 maker minutes, 45 reviewer minutes"
attempt_limit: 1
orchestration_mode: "standard"
exact_model: "Sol controller and maker, deterministic evaluator, one fresh independent Luna xhigh verifier after separate delegation authority"
reasoning: "implementation"
authorization_scope: "The owner said Yes you can always keep going after the required release-preflight architecture reset was requested"
ownership_map: "controller owns boundary, packet, and routing; controller is the exclusive maker; deterministic tools evaluate; a fresh verifier must be separate; owner retains Git, release, and consumer authority"
chain_stages: "authorization, maker, deterministic evaluation, fresh review, closeout"
concurrency: "one writer; sequential stages; no sub-agent is authorized in the maker stage"
tool_budget: "40 maker calls or 90 minutes; 20 reviewer calls or 45 minutes"
context_budget: "8K-15K maker target; 25K ordinary ceiling"
reserve_use: "not used"
checkpoint_interval: "stop at maker, evaluator, or reviewer BLOCK"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: ".planning/essential-tasks/2026-08-30-agent-plus-0-4-0-release-preflight-architecture-reset.md"
return_check: "anti-loop admission, exact verifier receipt, complete public validator, and fresh review"
polling_policy: "not-applicable"
evaluator_commands: "focused release-verifier tests; exact zero-option verifier; strict mypy; Ruff; complete public validator; active-chain guard; diff and scope checks"
fresh_verifier_contract: "one independent reviewer receives the contract, frozen files, deterministic receipt, and full registered matrix; it returns PASS or BLOCK and does not repair"
promotion_dossier: ".planning/essential-tasks/2026-08-30-agent-plus-0-4-0-release-readiness.md"
anti_loop_packet: ".agent-plus/agent-plus-0-4-0-release-preflight-reset-task-002.json"
review_closeout: "planned after deterministic evaluator PASS"
active_chain_capsule: ".agent-plus/active-chain.json"
active_chain_guard: "python3 scripts/active_chain_guard.py --capsule .agent-plus/active-chain.json --mode continue"
authority_refs: "AGENTS.md, AI_WORKFLOW.md, ESSENTIAL_WORK_PROTOCOL.md, engineering ledger, review 001, and release-readiness dossier"
cost_isolation: "Reuse accepted typed implementation and all current public files. Change only the release-preflight control and its tests, configuration, documentation, and evidence."
---

# Agent+ 0.4.0 release-preflight architecture reset

## Necessity

- **Decision:** Can one closed command prove the exact Agent+ release candidate without an archive,
  a caller-selected copy method, or mutation of the live repository?
- **Uncertainty:** The maker's disposable-index procedure passed, but the fresh reviewer selected a
  temporary `tar` archive that failed before validation.
- **Existing evidence:** The typed manifest seam, strict mypy, Ruff, focused tests, and live public
  validator pass. The reviewer completed the matrix and returned `BLOCK` only because the required
  simulated-version validator did not start.
- **Minimum action:** Put the proven temporary-index, temporary-object, checkout-index, simulated
  version, and validator sequence behind one zero-option command with one fixed configuration.
- **Unlock:** One deterministic PASS permits a fresh independent architecture review. It does not
  authorize release or consumer synchronization.

## Why this is an architecture reset

Two blocks are recorded at
`AGENT_PLUS_RELEASE_READINESS/manifest-strict-mypy-narrowing`. Another local patch is forbidden.
The reset removes the two ledger-approved caller choices:

- `implicit-any-managed-set-identity`
- `skip-strict-mypy-release-gate`

The reset also makes candidate export an internal implementation detail. A reviewer runs the fixed
command and cannot select `tar`, `cp`, an alternate manifest, an output root, or a Git index.

## Boundary

- **Allowed artifacts:** `scripts/verify_release_candidate.py`,
  `.agent-plus/release-candidate.json`, `tests/test_release_candidate_verifier.py`,
  `docs/release-candidate-verification.md`, `scripts/validate-public-package.sh`, `README.md`, this
  card, the architecture-reset task and review packets, the release-readiness dossier, state, hot
  memory, exact candidate manifest, and the local active-chain capsule.
- **Allowed actions:** Add one closed verifier, synthetic tests, public documentation, deterministic
  receipts, and exact routing evidence. Run temporary filesystem and Git plumbing operations outside
  the repository.
- **Forbidden actions:** Do not change the typed manager repair, lifecycle behavior, accepted
  policies, `VERSION`, the live Git index, repository object store, commit, tag, release, consumer,
  proving project, data, or scientific state.
- **Review mode:** engineering sweep.
- **Failure-class coverage:**
  `AGENT_PLUS_RELEASE_READINESS/manifest-strict-mypy-narrowing` and its complete registered matrix.
- **Simplification trigger:** This is the required reset after two blocks. Any maker, evaluator, or
  reviewer `BLOCK` stops the chain. No same-chain repair follows.
- **User-visible outcome:** Agent+ maintainers can run one exact command to verify a release
  candidate without choosing or reconstructing the export procedure.
- **Stop condition:** PASS requires the zero-option verifier, exact scope, simulated version, full
  public validator, static gates, unchanged index, temporary object isolation, and fresh review.
- **Stop behavior:** collect the named engineering matrix, then stop on a boundary verdict.
- **Attack matrix:** exact registered eight-item matrix; pending.
- **Named coverage:** exact registered seven-item coverage matrix; pending.
- **Promotion dossier:**
  `.planning/essential-tasks/2026-08-30-agent-plus-0-4-0-release-readiness.md`.
- **Dispatch guard:** the registered architecture-reset task must pass before implementation.
- **Review closeout guard:** a complete architecture-reset review packet must pass before any
  release decision.
- **Changed interfaces:** one zero-option command and one closed configuration schema.
- **Consumer discovery:** search `verify_release_candidate`, `release-candidate.json`, and the fixed
  command across scripts, tests, docs, README, candidate manifest, and validator.
- **Consumer closure:** the script, fixed configuration, focused tests, documentation, candidate
  manifest, and public validator must agree.
- **Runtime wrappers:** standard-library subprocess calls to Git, Python, shell validator, `uvx`
  mypy, and `uvx` Ruff.
- **Real-shape smoke:** run `python3 scripts/verify_release_candidate.py` from repository root.
- **Repeat trigger:** any verifier, configuration, manifest, release version, static command, or
  candidate-scope change.
- **Acceptance:** exact task admission, focused tests, zero-option real-shape PASS receipt, strict
  mypy, Ruff, complete public validation, exact scope, unchanged index, and fresh review.

## Decision branches

- **If PASS:** Freeze the reset, obtain one fresh independent review, then stop for a separate owner
  release decision.
- **If BLOCK or FAIL:** Close the reset honestly. Do not patch, retry, release, or synchronize.

## Closeout

The maker completed the closed verifier, fixed configuration, synthetic tests, public
documentation, exact candidate-manifest integration, and public-validator integration. Before the
terminal launch, the 79-path scope was exact; focused tests passed `7/7`; strict mypy and Ruff
passed; the active-chain guard continued at `maker`; and the complete public validator passed
`171/171`.

The one authorized zero-option launch returned:

```text
RELEASE_CANDIDATE_BLOCK E_LIVE_OBJECT_MUTATION repository object store changed during verification
```

No receipt was written. Live `VERSION` remains `0.3.0`, `HEAD` remains
`ea147c0e2b2dac481238f96c37b56a31fe65033b`, and the real index remains byte-identical at
`4e7bdda169a1d25cfc6f14c3a3f97b855ec54e772c9b1f2eaaacfa2a5512a1e9`. Read-only inspection found
75 loose object files with modification times at the launch boundary, including the candidate root
tree. Their sorted relative-name digest is
`6ba8c2ec27ae6214aae188346ef7bfd197feefef53bb18bf76659839e2815d71`.
This confirms that the isolation claim did not hold; it does not establish which Git subprocess
ignored or escaped the intended object directory.

A follow-up read-only identity comparison found 65 blobs and 10 trees in that 75-object set. Sixty-
six candidate paths resolve to those new blob identities; duplicate file content explains why path
matches can exceed unique blobs. The shape is consistent with a concurrent full candidate snapshot,
but it does not identify the writer. A future design must either run outside the canonical Git
object store entirely or replace whole-store immutability with a boundary that can distinguish
host snapshot objects from prohibited ref, index, worktree, or release mutations.

Per the reset contract, this is terminal `BLOCK`. There is no repair, rerun, evaluator promotion,
fresh-review dispatch, release decision, or consumer synchronization in this chain. The new
verifier artifacts remain unaccepted dirty-worktree material.

```yaml
decision_changed: yes
blocker_closed: no
work_unlocked: none
user_visible_outcome: one closed release-candidate verification command
repeat_trigger: verifier or candidate authority changes
```

## Owner-authorized successor: attempt 003

The owner explicitly authorized continued release preflight, parallel Sol agents, high reasoning,
next-stage preparation, and a comprehensive review packet on 2026-08-30. This is a new architecture
chain, not a rerun of attempt 002. Publication and consumer changes remain separate decisions.

- Mode: deep, capped at the owner's one-hour window. Sol/high overrides the usual worker model
  for this task only. Three independent read-only workers support one exclusive repository writer.
- Decision: can a detached candidate validate without directing any write-capable Git command at
  the canonical repository or weakening exact-scope, static, privacy, or review gates?
- Existing evidence: attempt 002 detected object metadata changes but did not identify their writer.
  Preserve that BLOCK and distinguish observed metadata from proved content additions.
- Exploration: one bounded code/architecture audit, one canonical history synthesis, and one
  next-stage readiness audit. No recursive agents or overlapping writers.
- Maker boundary: verifier, verifier tests, fixed configuration, release documentation, package
  integration, exact manifest, existing release dossier, registered task/review packets, ledger
  admission, local capsule, current state, and local owner-facing outputs.
- Acceptance: synthetic hostile-environment/path/scope tests, detached real-shape preflight,
  strict typing and lint, public validator, unchanged canonical index/refs/worktree identities,
  exact candidate receipt, and one fresh independent review.
- Simplification: remove write-capable commands from the source repository. Do not explain away
  unexpected source mutation. Distinguish concurrent observation from actor attribution.
- Stop: collect the complete reachable engineering matrix. A substantive maker/evaluator/reviewer
  BLOCK stops implementation and launch work. Independent owner-report preparation may finish.
- Outcome: a reviewable release-candidate decision plus a readable owner packet and prepared
  next-stage instructions. Tests and documents alone do not imply release acceptance.
- Budget: 60 minutes total, three research workers at 12 minutes each, one maker at 25 minutes,
  deterministic evaluator, one fresh reviewer at 12 minutes, and synthesis within remaining time.
- Public safety: public controls receive only generic evidence. Task-history synthesis stays in
  ignored local outputs. Do not copy proving-project transcripts or scientific state upstream.

### Successor evidence and maker dispatch

The independent code audit reproduced Git alternate-object freshening in a disposable fixture.
The old verifier returned its object-mutation error while object names and content stayed identical.
Existing object timestamps changed. Therefore earlier statements that the timestamp scan proved
75 new loose objects, a candidate root tree, or a concurrent host writer are withdrawn. Attempt 002
remains BLOCK, because it failed its stated immutability check. Its actor attribution was unproved.

Attempt 003 removes the alternate relationship entirely. Source Git commands are read-only and
run with explicit repository identity and a clean environment. Raw base blobs populate a detached
repository. No clone sharing, hard links, source hooks, or clean/smudge filters are used. Source
index, refs, object metadata, public bytes, and modes are checked on success and failure. Detached
candidate bytes and modes are checked again after validation. Stale PASS evidence must not survive
a failed attempt as current success.

The registered matrix contains 26 attacks and 17 named coverage areas. Maker admission passed:
`sha256:375adb0f3442a3b7e56b68750738d68a55f38d2ba5b61e430bbf9ea74050416a`.
The observed toolchain to pin is mypy `2.3.1` and Ruff `0.16.5`.

### Attempt 003 maker completion and evaluator boundary

The exclusive maker completed the six permitted implementation/configuration/documentation files.
Construction passed 32 focused synthetic tests, strict mypy, Ruff, and all 196 public-package
tests. Canonical/bootstrap bindings, privacy, links, whitespace, and toolchain checks passed.
The maker did not launch the canonical verifier. The exact public scope is now 81 paths.

The controller may run one real preflight on this frozen candidate. Only a PASS permits one fresh
independent Sol/high reviewer to run the same closed command and the complete 26-attack,
17-coverage matrix. A substantive failure ends launch and repair work. After a successful review,
administrative review/state records may be finalized and one success-only final candidate refresh
may bind those final bytes. This is not a failure retry and does not permit code repair. A final
refresh failure stops the chain. Its receipt belongs in ignored local outputs, preventing a
self-referential public tree hash.

### Attempt 003 independent review and administrative closeout

The controller evaluator passed the real closed command with all ten gates. A distinct Sol/high
reviewer independently passed the same command and matched all 81 frozen hashes/modes and the
same candidate tree. Complete coverage: 26/26 attacks, 17/17 named coverage, 50/50 independent
probes, and the current 196-test package suite including 32 verifier tests. No Critical,
Important, or Minor finding was reported. Current typing and lifecycle-fixture changes were
included explicitly; older administrative acceptance receipts were not substituted for review.

- Evaluator receipt: `sha256:0a7061fe7e4b54ab13a50c25fa44d104718b59d31646d94bcd1a7e8f994deb1b`.
- Reviewer receipt: `sha256:4a84abfc6335bb68d37e938753b98ffd70eacbeedaee01943eae92996b45a71c`.
- Reviewed tree: `af26236a8217aae7c0c3212ca47bf02fe1adb982`.
- Independent report SHA-256: `2c254f1783d3ff556e19e8c8cd54c0b5adb950c2be5dd1d65bb16edee2bb4f94`.
- Complete review closeout: `sha256:bdb2fdeff215ba00c450f6acf3a0f8b472c8392d4de8f88d31a26baf3990d8a4`.

Source Git snapshots matched across both launches. Source worktree snapshots matched within each
launch. Between launches, the controller advanced only the ignored active-chain capsule and added
ignored local evidence. That administrative transition explains the different cross-stage source
worktree digest; the public candidate bytes/modes and tree stayed identical.

The independent report permits only the review003 completion flag, hot memory, planning state,
existing release-readiness and reset dossiers, and current acceptance matrix to close. No
implementation, configuration, test, or manifest change follows review. The one already-authorized
final refresh binds these administrative bytes. Its current result and final tree belong in
`outputs/release-candidate/receipt.json`, not this self-including public candidate. The controller
must confirm the administrative-only delta before that launch and stop on any BLOCK.

The comprehensive owner packet, operating manual, unsigned next-stage handoffs, and exact evidence
index are local outputs. They do not grant publication or consumer authority. The earlier BLOCKs
remain intact. The separate scientific coverage gate remains BLOCK.
