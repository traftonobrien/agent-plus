---
task: "Repair the optional public-safe Agent+ outcome audit exact evidence-population boundary"
owner_role: "maker, evaluator, verifier"
tier: "2"
time_budget: "90 maker minutes, 45 reviewer minutes"
attempt_limit: 1
orchestration_mode: "deep"
exact_model: "Sol controller, Luna xhigh maker, deterministic evaluator, fresh different Luna xhigh reviewer"
reasoning: "implementation"
authorization_scope: "Owner authorized attempt-04 architecture cleanup to replace literal private attack payloads with symbolic public evidence, preserve implementation hashes, rerun deterministic acceptance, and obtain one fresh review; no release or downstream synchronization"
ownership_map: "controller owns boundary and packets; one maker owns the optional skill, tests, router, docs, and validator; deterministic evaluator owns receipts; fresh reviewer owns the integrated verdict; owner retains release and downstream synchronization"
chain_stages: "dispatch guard, maker, deterministic evaluator, fresh integrated reviewer, closeout"
concurrency: "one exclusive writer; sequential maker, evaluator, reviewer"
tool_budget: "40 maker calls or 90 minutes; 20 reviewer calls or 45 minutes"
context_budget: "8K-15K implementation target; 25K ordinary ceiling"
reserve_use: "premium reserve not used"
checkpoint_interval: "one bounded wait per dispatched agent"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: ".planning/essential-tasks/2026-08-22-agent-plus-outcome-audit-necessity.md and the task/review packets"
return_check: "anti-loop guard plus deterministic acceptance matrix"
polling_policy: "zero AI polls while running"
evaluator_commands: "focused unittest, complete unittest suite, public package validator, skill CLI synthetic matrix, strict privacy scan, anti-loop review closeout"
fresh_verifier_contract: "Review only the sanitized changed surface and deterministic receipts; exhaust the registered matrix; return one explicit PASS or BLOCK; do not repair findings"
promotion_dossier: ".planning/essential-tasks/2026-08-22-agent-plus-outcome-audit-necessity.md"
anti_loop_packet: ".agent-plus/agent-plus-outcome-audit-task-004.json plus guard PASS"
review_closeout: ".agent-plus/agent-plus-outcome-audit-review-004.json plus closeout guard PASS"
---

# Essential Task Card

## Attempt 04 sanitized evidence-record reset

- **Decision:** Whether public evidence can preserve the exact attack class, location class, verdict, and receipt without reproducing a sensitive payload.
- **Existing finding:** Attempt 03 implementation and deterministic evaluation passed, but the fresh reviewer found that its public dossier repeated two private-path attack payloads verbatim.
- **Minimum action:** Change only this dossier. Replace every unsafe literal payload with stable symbolic labels such as `PRIVATE_PATH_ATTACK_HOT_MEMORY` and `PRIVATE_PATH_ATTACK_PUBLIC_DOC`. Preserve the attacked surface class, expected BLOCK, observed BLOCK, validator identity, and reviewer conclusion.
- **Removed choice:** `literal-private-payload-in-public-evidence-record`.
- **Frozen implementation:** `skills/outcome-audit/outcome_audit.py` must remain `e1b94b1b8c6ad138ac7e8d7d2b0ac6d13d4175e52fcc771cac90406a448fc663`; `tests/test_outcome_audit.py` must remain `b92e96cb35d2d735979dadf5aa55a753abf9737f52562e387095afe6c5255cbf`; `skills/outcome-audit/SKILL.md` must remain `d694b45ca1596336cdd25f93c9f701f808d32a22eb28b9c07aaea6b1defa6c31`; the validator must remain `104115a84fceff8aafd8970f91f4dce8e6afa486e1701726c0cf73095db252a0`.
- **Allowed write surface:** This dossier only for the maker; controller-owned task/review packets and state remain separate.
- **Forbidden:** No implementation, test, validator, hot-memory, state, release, Git, lifecycle, downstream, or SECOND LOOK change by the maker.
- **Acceptance:** Zero private absolute-path tokens in the public dossier; public validator PASS; frozen hashes exact; complete matrix PASS; one fresh independent review PASS.
- **Stop:** Maker, evaluator, or reviewer `BLOCK` ends attempt 04. No same-chain repair.
- **Owner authorization:** The user said, “Go,” on 2026-08-22.

## Attempt 03 architecture reset

- **Decision:** Replace the remaining caller-selected receipt helpers with one cwd-only verify-and-write operation and make canonical hot memory portable without weakening the recursive public-safety scan.
- **Why architecture reset:** Two BLOCKs are recorded. A third local patch is forbidden. The reset removes receipt root/payload choices and the machine-local restart-command choice instead of adding exclusions, manifests, or configuration.
- **Accepted design:** Keep `scripts/validate-public-package.sh` byte-identical at SHA-256 `104115a84fceff8aafd8970f91f4dce8e6afa486e1701726c0cf73095db252a0`. Keep root `.claude-memory.md` in the public safety boundary, replace its absolute restart sequence with the fixed portable `./scripts/ai-context.sh`, and state that it runs from repository root. Close outcome receipt verification/writing to cwd and internally generated receipts only.
- **Removed choices:** `caller-selected-receipt-root`, `caller-supplied-receipt-payload`, and `machine-local-hot-memory-restart-command`.
- **Allowed write surface:** `.claude-memory.md`, `skills/outcome-audit/outcome_audit.py`, `tests/test_outcome_audit.py`, and `skills/outcome-audit/SKILL.md`, plus controller-owned dossier and attempt packets.
- **Forbidden design:** No public release manifest, scan exclusion, private sidecar, environment override, path option, new service, database, scheduler, transcript parser, or Git operation.
- **Acceptance:** Existing exact-population attacks stay green; receipt helpers expose no root or payload; CLI path options fail; recursive safety validator is byte-identical and passes; private absolute paths remain rejected by the unchanged validator; complete suite and fresh independent review pass.
- **Stop:** Maker, evaluator, or reviewer `BLOCK` ends attempt 03. No same-chain repair.
- **Owner authorization:** The user said, “Proceed,” on 2026-08-22.

## Attempt 02 authorization

- **Decision:** Whether fixed, non-following directory enumeration plus exact manifest equality closes the unlisted-evidence failure without adding another configurable interface.
- **Existing finding:** Attempt 01 returned the same `PASS` receipt after an unlisted JSON file was added under `.agent-plus/outcome-audit/evidence/`.
- **Minimum repair:** Enumerate the fixed evidence directory without following symlinks, require every entry to be one manifest-declared regular JSON source, reject missing, extra, duplicate, symlink, directory, and non-JSON entries, and add the exact synthetic attack.
- **Allowed write surface:** `skills/outcome-audit/outcome_audit.py`, `tests/test_outcome_audit.py`, and `skills/outcome-audit/SKILL.md` only, plus controller-owned dossier and attempt packets.
- **Stop:** Maker, evaluator, or reviewer `BLOCK` ends attempt 02. No same-chain repair.
- **If PASS:** Record acceptance and stop before release or consumer synchronization.
- **If BLOCK:** Record the complete finding set. Because that would be the second BLOCK at this interface, require architecture simplification before any later attempt.
- **Owner authorization:** The user said, “Let's run all of this,” on 2026-08-22.

## Necessity

- **Decision:** Whether Agent+ can ship one lean optional capability that measures workflow outcomes and verifies sanitized receipts without importing project-specific state.
- **Uncertainty:** Whether a closed generic record, deterministic metrics, abstention rules, and a privacy-preserving receipt can remain small, falsifiable, and publicly safe.
- **Existing evidence:** SECOND LOOK has one reviewed proposal and a successful local proving implementation, but canonical Agent+ does not yet expose or validate the generic capability.
- **Minimum action:** Add one optional file-based skill, one closed schema and CLI, synthetic fixtures/tests, and the minimum router, documentation, and public-validator bindings.
- **Unlock:** A fresh integrated PASS permits owner consideration of a later Agent+ release; it does not authorize release or consumer synchronization.

## Boundary

- **Allowed artifacts:** `skills/outcome-audit/**`, `tests/test_outcome_audit.py`, `skills/agent-plus/SKILL.md`, `README.md`, `docs/bootstrap-a-baseball-project.md`, `scripts/validate-public-package.sh`, this dossier, and the registered task/review packets.
- **Allowed actions:** Add sanitized generic policy, schemas, implementation, synthetic data, deterministic tests, routing, docs, and validation; run read-only deterministic checks.
- **Forbidden actions:** Modify lifecycle, manager, initializer, doctor, legacy-adoption code, release identity, Git state, downstream projects, private data, scientific artifacts, or the existing legacy-adoption BLOCK.
- **Review mode:** engineering sweep
- **Failure-class coverage:** `AGENT_PLUS_OUTCOME_AUDIT/closed-outcome-record-and-private-evidence-receipt` and every registered adjacent invariant.
- **Simplification trigger:** Any maker, evaluator, or reviewer BLOCK ends this chain; no same-review repair.
- **User-visible outcome:** Agent+ users can record closed workflow outcomes, calculate honest reliability and efficiency measures, and verify a sanitized receipt without exposing private evidence.
- **Stop condition:** PASS requires the complete registered deterministic matrix and one fresh independent integrated PASS; otherwise BLOCK.
- **Stop behavior:** collect named engineering matrix, then stop on any boundary verdict BLOCK.
- **Attack matrix:** exact-schema rejection; ordered terminal authority; attempt/disposition/scientific separation; metric denominators; Wilson intervals; null zero denominators; measured duration; retry efficiency; abstention; fixed receipt interface; omission/substitution/traversal/symlink/tamper/duplicate/count/privacy/replay attacks; routing/docs/validator.
- **Named coverage:** skill contract, schema, validator, reporter, statistics, receipt, privacy, synthetic fixtures/tests, router, docs, public validator.
- **Promotion dossier:** this file, updated in place.
- **Dispatch guard:** registered ledger boundary plus `.agent-plus/agent-plus-outcome-audit-task-001.json` PASS.
- **Review closeout guard:** complete `.agent-plus/agent-plus-outcome-audit-review-001.json` plus closeout guard PASS.
- **Changed interfaces:** New optional `$outcome-audit` skill and its closed command/data contracts only.
- **Consumer discovery:** Deterministic searches for `outcome-audit`, `agent-outcome-record`, and receipt command names across skills, docs, tests, and validator.
- **Consumer closure:** Router, public docs, test suite, and public validator must all name or exercise the optional capability.
- **Runtime wrappers:** Python standard-library subprocess tests only.
- **Real-shape smoke:** Synthetic temporary-project CLI tests using the conventional project-local `.agent-plus/outcome-audit/` layout.
- **Repeat trigger:** Changed code, schema, metric formula, receipt contract, routing, or owner-approved release action.
- **Acceptance:** Exact registered matrix PASS, complete unit suite PASS, public validator PASS, privacy scan PASS, deterministic replay PASS, and fresh independent integrated PASS.

## Decision branches

- **If PASS:** Update canonical state truthfully and stop for separate owner authority before release or downstream synchronization.
- **If BLOCK or FAIL:** Record the exact finding and stop; do not repair it in this chain.

## Closeout

```yaml
decision_changed: no
blocker_closed: none
work_unlocked: none
user_visible_outcome: BLOCK - exact private evidence population is not proven
repeat_trigger: explicit owner authorization for a new repair chain that closes unlisted evidence detection
```

## Deterministic evaluator result

Verdict: `BLOCK`

Passing evidence:

- Focused outcome-audit suite: `14` tests passed.
- Complete public suite: `122` tests passed.
- Public package validator: `PASS`.
- Canonical/bootstrap guard bindings and internal Markdown links: `PASS`.
- Python compilation: `PASS`.
- New-surface project-identity and private-state scan: `PASS`.
- Dispatch guard receipt: `sha256:554b566cbcd81ab53e4ac29fd042d6bd31c6f21fde4fa415f48e561ac1844ed9`.

Blocking evidence:

- The evaluator created a valid synthetic fixed-layout evidence population and obtained `PASS`.
- It then added `.agent-plus/outcome-audit/evidence/unlisted.json` without adding that source to the manifest.
- Verification still returned `PASS`, and the sanitized receipt was byte-for-byte equivalent as a value.
- Therefore the verifier proves only the manifest-declared subset, not the exact evidence directory population. The registered `evidence-omission-substitution` attack is not closed.

The bare-shell and locked-environment Ruff commands were unavailable on this machine. Ruff was not
an acceptance command in this card, so this did not determine the verdict. The exact-source-set
failure independently determines `BLOCK`.

No fresh reviewer was dispatched. No repair, release, Git operation, downstream synchronization,
or change to the separate legacy-adoption boundary followed.

## Attempt 02 maker result

Verdict: `MAKER_BLOCK`

Passing evidence:

- Exact evidence-directory enumeration was implemented inside the authorized three-file surface.
- Focused outcome-audit suite: `16` tests passed.
- Complete public unittest suite: `124` tests passed.
- Python compilation: `PASS`.
- Synthetic coverage rejects unlisted, missing, duplicate, symlink, non-JSON, directory, FIFO,
  socket, and device entries.

Blocking evidence:

- Required public package validation returned `BLOCK` because canonical `.claude-memory.md` contains
  a private absolute local restart path.
- `.claude-memory.md` was outside maker ownership. The maker did not repair or suppress the finding.
- Ruff was unavailable in the locked environment. The public-validator failure independently
  determines `BLOCK`.

This is the second recorded BLOCK at
`AGENT_PLUS_OUTCOME_AUDIT/closed-outcome-record-and-private-evidence-receipt`. The interface now
requires an owner-authorized architecture-reset packet before any later maker attempt. No evaluator
or reviewer was dispatched. No release, Git operation, or downstream synchronization followed.

## Attempt 03 deterministic evaluator result

Verdict: `PASS`

- Dispatch guard receipt:
  `sha256:36f4d198421c7e2f82f43a13e2e288ab6ff5d312d9824cb13522fc773d795e5f`.
- Focused outcome-audit suite: `18` tests passed.
- Complete public unittest suite: `126` tests passed.
- Python compilation and public package validation: `PASS`.
- `scripts/validate-public-package.sh` remained byte-identical at
  `104115a84fceff8aafd8970f91f4dce8e6afa486e1701726c0cf73095db252a0`.
- Root hot memory contains zero `MACHINE_LOCAL_PATH_PATTERN` tokens and uses only `./scripts/ai-context.sh` from the
  repository root.
- Receipt CLI rejected caller `--root`; helper signatures expose no root or payload parameters.
- An isolated public-package copy with `PRIVATE_PATH_ATTACK_HOT_MEMORY` injected into `.claude-memory.md`
  deterministically failed the unchanged public-safety scan.
- A second isolated copy attack, `PRIVATE_PATH_ATTACK_PUBLIC_DOC`, in `README.md` also failed the unchanged scan.
- Existing tests closed exact-population, omission, substitution, traversal, symlink, tamper,
  duplicate, non-JSON, directory, FIFO, socket, device, privacy, and deterministic replay cases.

Current architecture hashes:

- `.claude-memory.md`: `031a34081b7c5bc72f95fe54a154fe83f5ae819ad1c0dc452787daf767df31bf`.
- `skills/outcome-audit/outcome_audit.py`:
  `e1b94b1b8c6ad138ac7e8d7d2b0ac6d13d4175e52fcc771cac90406a448fc663`.
- `tests/test_outcome_audit.py`:
  `b92e96cb35d2d735979dadf5aa55a753abf9737f52562e387095afe6c5255cbf`.
- `skills/outcome-audit/SKILL.md`:
  `d694b45ca1596336cdd25f93c9f701f808d32a22eb28b9c07aaea6b1defa6c31`.

One fresh independent integrated review remains required. No release or downstream synchronization
is authorized by this evaluator PASS.

## Attempt 04 deterministic evaluator result

Verdict: `PASS`

- Dispatch guard receipt:
  `sha256:ef92366c95c9dcb52ffc8625428225df3d784356e666f4600b26131341957335`.
- Maker-sanitized dossier SHA-256 before the evaluator appended this receipt:
  `f8802864a158ff43a793772057c8c41af9cefafd25f5aea9ddd90b6cb7efbf75`.
- Dossier private-path scan: `PASS`; only symbolic attack labels remain.
- Frozen outcome implementation, tests, skill, and validator hashes: exact.
- Focused outcome-audit suite: `18` tests passed.
- Complete public unittest suite: `126` tests passed.
- Python compilation and complete public package validation: `PASS`.
- The attempt-03 implementation remains unchanged. Attempt 04 changed only the public dossier.

One fresh independent integrated review remains required. No release or downstream synchronization
is authorized by this evaluator PASS.
