# Agent+ 0.4.0 release-scope readiness

Date: 2026-08-30

Outcome: `PASS — DETACHED ENGINEERING PREFLIGHT AND INDEPENDENT REVIEW 003`.

The final administrative-byte refresh receipt must also match the current candidate before any
publication decision. Earlier results below are retained as history, not current launch authority.

## Decision boundary

Determine whether the fully accepted unreleased Agent+ bundle can form one complete, public-safe
candidate release without mutating the real Git index, worktree version, remote, tag, release, or
any consumer.

The recommended version is `0.4.0`, not `0.3.1`, because the bundle adds the active-chain routing
capsule, deterministic guard, managed lifecycle delivery, and an explicit authority boundary. This
is a recommendation only. The owner still controls the version and release decision.

## Candidate scope

The exact proposed path set is stored in
`.planning/essential-tasks/2026-08-30-agent-plus-0-4-0-release-scope-candidate.txt`.

The scope includes generic implementation, bootstrap parity, public documentation, synthetic
tests, ledger packets, accepted and blocked review history, necessity records, current acceptance
evidence, and the completed `0.3.0` publication record.

The scope excludes local routing state, the ledger lock, generated `outputs/`, the local project
registry, caches, and editor/macOS metadata. It contains no consumer file, raw data, credential,
private path, transcript, model result, or scientific artifact.

## Required preflight

- Candidate manifest is sorted, unique, complete, and contains only existing regular files.
- Every modified or untracked non-local path is classified.
- A disposable Git index starts at current `HEAD`, receives only the candidate scope, and simulates
  `VERSION=0.4.0` without changing the worktree or real index.
- The disposable staged path set equals the candidate manifest exactly.
- The staged diff passes whitespace and public-safety checks.
- Current accepted review closeouts reproduce against the current ledger.
- Full tests and public package validation pass from the live frozen worktree.
- Local and excluded paths remain absent from the candidate index.
- Local `HEAD` and remote `main` remain the verified `0.3.0` release base.

## Historical scope classification before attempt 003

- Exact current candidate paths: `73`.
- Tracked modified paths: `31`.
- Public untracked paths: `41`.
- Simulated version-only path: `VERSION`.
- Explicit local exclusions: `23`, comprising the ledger lock, generated `outputs/`, and
  editor/macOS metadata.
- Candidate manifest SHA-256:
  `8e96619ecc5df7feaf6ab77769475b9b7d7e3e8199e58ced8eb68f43d18ea1a0`.
- Sortedness, uniqueness, exact current-status coverage, regular-file existence, and absence of
  surplus paths: `PASS`.

## Preflight harness closure

Two adjacent harness launches failed before a candidate result existed: the first command was
rejected because its cleanup trap contained a deletion command, and the second exposed that Git's
alternate-object environment splits the repository path at its colon. This was recorded as
`LOOP_DETECTED`; no third blind launch occurred.

One bounded read-only sweep proved a temporary symlink to the repository object directory avoids
the colon parser while keeping all newly written objects outside the repository. The consolidated
harness then reached the candidate without modifying the real index or repository object store.

That first candidate run found one release-transition test-fixture false positive. The v1 legacy
fixture changed its schema to v1 but retained the simulated current `0.4.0` version, fabricating a
legacy format that never existed and that production correctly rejected. The accepted single
small-correction rule was applied once:

- Changed file: `tests/test_agent_plus_legacy_adoption.py`.
- Correction: pin the synthetic v1 manifest to the real historical `0.3.0` version.
- Production behavior, dependency, data, authority, and acceptance boundaries: unchanged.
- Reviewed pre-correction test hash:
  `177876f5a591db60f73450222bc52ac7c5c50897beb305c8e6b7611ebb9fe34c`.
- Corrected test hash:
  `91043db3fc817a0fc03fd269a80572d5f3792d02e40f13e6052392c19793217f`.

The one permitted identical candidate rerun passed. No further correction was needed.

## Repaired disposable-index result

- The pre-review exact staged path set equaled the 72-path manifest: `PASS`.
- Simulated staged `VERSION`: `0.4.0`.
- Complete public suite: `164/164 PASS`.
- Public validator, privacy, whitespace, links, and canonical/bootstrap bindings: `PASS`.
- Strict mypy on the manager and adjacent guards, plus Ruff on the changed implementation and
  tests: `PASS`.
- `scripts/active_chain_guard.py` and `bootstrap/base/scripts/ai-context.sh` staged modes:
  `100755`.
- Real index SHA-256 before and after:
  `4e7bdda169a1d25cfc6f14c3a3f97b855ec54e772c9b1f2eaaacfa2a5512a1e9`.
- Current accepted active-chain, lifecycle, and policy closeouts reproduce against the current
  ledger with receipts
  `sha256:7a2471dfcf6c349b21180ff80108b5bcf200ddf5029d22d1e304fff35d6e2bea`,
  `sha256:ff348b51a8076e500bbbce5fa9f744f87bf7bee052b27a77eb50a8fcb413e460`, and
  `sha256:072b74fd7d1a0561ee7086998e9e949da10934c0f547f134d90d76bf187dccc8`.

## Historical external release-state observation

- Local `HEAD` and remote `main`:
  `ea147c0e2b2dac481238f96c37b56a31fe65033b`.
- Proposed annotated tag `v0.4.0`: absent.
- Proposed GitHub release `v0.4.0`: absent.

## Decision

The bounded repair now passes strict mypy, Ruff, `43/43` lifecycle tests, `12/12` legacy-adoption
tests, `164/164` complete tests, public validation, compilation, bindings, privacy, links, and diff
checks. It narrows the current manifest identity after exact runtime validation and adds typed
private-helper rejection for malformed identity input.

The pre-review repaired 72-path disposable candidate passed with simulated `VERSION=0.4.0`.
Strict mypy and Ruff pass inside that exported candidate, and the real Git index remains byte-
identical at `4e7bdda169a1d25cfc6f14c3a3f97b855ec54e772c9b1f2eaaacfa2a5512a1e9`.

Fresh review 001 assessed all `8` attacks and `7` named coverage items. The reviewer returned
`BLOCK` because the required disposable simulated-version validator did not start. Its temporary
`tar` archive returned `Special header too large`. Complete closeout receipt:
`sha256:ab87a2b1d035f1337a2686bffc9b3bf297386d8e7407912198327e4463a287e7`.

The controller recorded the review `BLOCK` with result
`sha256:d704c9223ebc44444dac3a39ce49dd0ab5cc33a349ad5a37846744d7a359e2fa`.
The ledger requires an architecture reset after two recorded blocks. The owner authorized reset
attempt 002. Its zero-option verifier, fixed configuration, tests, documentation, and validator
integration produced an exact 79-path candidate with manifest SHA-256
`3f533be8ad2296e9d711cecfff3e42b8258df405751887f706a8f43fa024e7ef`. Before the terminal launch,
focused tests passed `7/7`, strict mypy and Ruff passed, and the complete public validator passed
`171/171`.

The one permitted real launch returned
`RELEASE_CANDIDATE_BLOCK E_LIVE_OBJECT_MUTATION repository object store changed during
verification`. No receipt was written. Live `VERSION` remains `0.3.0`, `HEAD` remains the release
base, and the real index hash remains
`4e7bdda169a1d25cfc6f14c3a3f97b855ec54e772c9b1f2eaaacfa2a5512a1e9`. Read-only inspection found
75 loose Git object files with launch-boundary timestamps. That scan did not establish additions,
a candidate root tree, or a concurrent writer. A synthetic successor audit reproduced normal
alternate-object timestamp freshening without changed object names or bytes. Attempt 002 remains
terminal `BLOCK`; its implementation may not be repaired or rerun in that chain.

## Owner-authorized detached successor: attempt 003

The owner authorized continued preflight and one independent review. Maker construction passed
32 focused verifier tests, strict mypy, Ruff, and the 196-test complete public package validator.
The exact manifest contains 81 paths, SHA-256
`ed23a9aa8cbe52fd4924df675f056f90e970cbcfe5a4caac956b23061c507ddd`.
Real evaluator and independent reviewer launches both passed all ten gates with candidate tree
`af26236a8217aae7c0c3212ca47bf02fe1adb982`. Within each launch, source Git/worktree snapshots
matched before and after. Independent review passed 26 attacks, 17 coverage areas, and 50 probes.
There were no Critical, Important, or Minor findings. Review closeout:
`sha256:bdb2fdeff215ba00c450f6acf3a0f8b472c8392d4de8f88d31a26baf3990d8a4`.

The reviewer permits the specified administrative records to close without code/config/test or
manifest changes, followed by one final success-only refresh. The current final-byte identity is
recorded in `outputs/release-candidate/receipt.json`. The preceding evaluator and reviewer receipts
are preserved separately in that local directory. Their earlier tree is not the post-closeout
tree. Release and consumer authorization are not included. A final refresh BLOCK stops the chain.

## Limits

This readiness audit cannot set `VERSION`, stage the real index, commit, push, create a tag, publish
a release, synchronize a consumer, or modify a proving project. Any final release attempt requires
one separate exact owner authorization and a fresh preflight after release-record fields change.

## Exact owner publication decision — authorized 2026-08-31

The owner selected `0.4.0`, annotated tag `v0.4.0`, branch `main`, canonical repository
`https://github.com/traftonobrien/agent-plus`, and release title `Agent+ 0.4.0`. Remote `main` was
read-only verified at `ea147c0e2b2dac481238f96c37b56a31fe65033b`; the target tag and GitHub
release were absent before mutation.

One new success-only preflight refresh is authorized because this decision changes administrative
release records. The active `.planning/discovery/PROJECT-DISCOVERY.md` article brief appeared after
the accepted candidate. It is preserved locally and excluded from publication through the exact
repository-local exclude file. The public manifest remains the accepted 81-path scope with SHA-256
`ed23a9aa8cbe52fd4924df675f056f90e970cbcfe5a4caac956b23061c507ddd`.

After the refreshed preflight passes, set the release worktree and exact staged `VERSION` to
`0.4.0`. Stage only the 81 manifest paths. Require the staged tree to equal the refreshed receipt
tree. Create one conventional release commit, one annotated tag, and one atomic push of `main` and
`v0.4.0`. Publish one public GitHub release that is neither draft nor prerelease. Verify remote
`main`, the peeled tag, and the GitHub release against the created commit.

Outputs, ledger lock, active capsule, local registry, editor/macOS metadata, consumer state,
private state, data, scientific artifacts, and the active discovery brief remain excluded. No
consumer synchronization is authorized. Stop on the first failure or uncertain result. Do not
retry, amend after publication, force-push, replace an existing tag, or publish a second release.

Status: `AGENT_PLUS_0_4_0_RELEASE_AUTHORIZED — ONE BOUNDED PUBLICATION ATTEMPT`.

## Publication attempt 001 — BLOCK

The one authorized refreshed preflight returned
`RELEASE_CANDIDATE_BLOCK E_SOURCE_MUTATION protected source state changed during verification`.
Receipt: `sha256:5cfbd1a2eb1d3c9a713b7d622a1afcd3bed0dc5616e5d4de4e5d47f6e769a1f3`.
The baseline was captured. The receipt does not identify a path or actor, so no attribution is
made. This result consumes the authorized refresh and publication attempt.

The stop occurred before live `VERSION` change, staging, release-commit object creation, commit,
tag, push, or GitHub release. The real index, local `HEAD`, remote `main`, and released `v0.3.0`
remain unchanged. `v0.4.0` tag and release remain absent. The active article discovery brief is
preserved locally and excluded.

Another attempt requires new owner authority after the source is quiescent. Do not retry this
chain or infer publication permission from its earlier PASS receipts.

Status: `AGENT_PLUS_0_4_0_PUBLICATION_001_BLOCK — STOPPED BEFORE GIT PUBLICATION`.

## Publication attempt 002 — owner-authorized isolated checkout

The owner directed the release to continue tonight and authorized one new attempt. This attempt
does not rerun attempt 001 in the active checkout. It freezes hashes and executable modes for the
same 81 manifest paths, copies only those paths into a clean isolated checkout at remote base
`ea147c0e2b2dac481238f96c37b56a31fe65033b`, and proves the active source freeze is identical
before and after transfer.

The isolated checkout receives one zero-option release-candidate preflight. PASS requires the
unchanged manifest, detached simulated `VERSION=0.4.0`, all 196 package tests, strict mypy, Ruff,
exact scope, and isolated-source preservation. Only that PASS authorizes setting the isolated
worktree `VERSION` to `0.4.0`, staging the exact manifest, comparing the staged tree to the receipt,
committing, tagging, atomic push, GitHub release creation, and remote verification.

The active source checkout is never staged or committed during this attempt. Its local discovery
brief remains preserved and excluded. Outputs, locks, active capsule, registry, metadata,
consumers, private state, data, and science remain excluded. Stop at the first failure or uncertain
result. Do not retry, force-push, replace a tag, or synchronize a consumer.

Status: `AGENT_PLUS_0_4_0_PUBLICATION_002_AUTHORIZED — ONE ISOLATED PUBLICATION ATTEMPT`.
