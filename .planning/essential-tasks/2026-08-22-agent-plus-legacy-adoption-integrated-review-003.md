# Agent+ legacy-adoption integrated review 003

Date: 2026-08-22

Role: fresh independent engineering reviewer

Review mode: engineering sweep

Verdict: PASS

## Scope and authority

This review assessed only the owner-authorized attempt-003 legacy-adoption boundary. I inspected
the five changed promotion files and their direct legacy-adoption consumers. I did not inspect a
maker transcript and did not modify implementation, tests, release state, Git state, or any
consumer project.

No release, consumer synchronization, consumer adoption, SECOND LOOK change, or release authority
is granted by this record.

## Input and byte evidence

- Controlling task: .planning/essential-tasks/2026-08-22-agent-plus-legacy-adoption-hook-and-doctor.md
  (sha256:7dd6fff27ba4a0893ede3a1aba710e603f537d7ab9eb0484c48458fd7eda7692).
- Prior integrated review: .planning/essential-tasks/2026-08-22-agent-plus-legacy-adoption-integrated-review-002.md
  (sha256:b9a1d3ae40f448e6ab149771ef52408a6f2368f227e55da994e55dd9c660da18).
- Review packet before closeout: .agent-plus/agent-plus-legacy-adoption-architecture-review-003.json
  (sha256:695eb2188c3499d230167fa602c0df9f932e854149353564cebe033fde385f00).
- Changed implementation bytes inspected:
  - scripts/agent_plus_manager.py — sha256:6b280e1cfe713055636776cf9bca40677c096aae21a77e029a8844a80ff10376
  - scripts/agent-plus-doctor.sh — sha256:c0150a097e3c0272d56f5b8b2fa5b0969734065b419c351b8487afe6de85454f
  - scripts/ai-context.sh — sha256:ca7596869f8b1eea9fc8af54c0bf7f4e47c210e45f318e34972ceab17f495690
  - bootstrap/base/scripts/ai-context.sh — sha256:c1a56ca2fe38d4cbc48db12b76052cea99c63047162523f413f42ed14d04f8c3
  - tests/test_agent_plus_legacy_adoption.py — sha256:df407cc07af313710f042187dffaaca28bca1c2d20df3224c8b4bb32aaa8f51e

The attempt-003 design is present in the inspected bytes: the manager uses a private nonblocking
open for the fixed hook; the copied doctor exposes one sourceable verifier with the exact 13-file
set; canonical and bootstrap context source that verifier; and hook execution uses the validated
descriptor.

## Deterministic checks

Commands and results:

~~~text
python3 -m unittest discover -s tests -p 'test_agent_plus_legacy_adoption.py'
Ran 11 tests in 7.312s — OK

python3 -m unittest discover -s tests -p 'test_agent_plus_lifecycle.py'
Ran 29 tests in 6.205s — OK

python3 -m unittest discover -s tests
Ran 128 tests in 14.243s — OK

bash scripts/validate-public-package.sh
Canonical/bootstrap guard bindings: PASS
Internal Markdown links: PASS
Public package validation: PASS

python3 - <<'PY'  # compile every Python file under scripts/ and tests/ with compile(...)
Python compilation: PASS
PY

/bin/sh -n scripts/agent-plus-doctor.sh scripts/ai-context.sh \
  bootstrap/base/scripts/ai-context.sh scripts/agent-plus
POSIX shell syntax: PASS
~~~

The focused suite includes the descriptor-swap, hook-exit, optional-state routing, initialized
doctor, upgrade, FIFO, and first/middle/last omission tests. I also ran a separate disposable
target matrix with paths containing spaces. It invoked the canonical manager, copied doctor,
canonical context, and bootstrap context directly. Its exact terminal result was:

~~~text
exact-managed-before-record: PASS - rc=0
divergent-managed-block: PASS - rc=1
project-owned-preservation: PASS - adopt=0 upgrade=0
fixed-hook-path: PASS - status=1 doctor=1
hook-failure-before-context: PASS - [1, 1, 1, 1]
hook-symlink-and-nonregular-block: PASS - symlink=True dir=True adopt_fifo=True post=[1, 1, 1, 1, 1]
absent-hook-policy: PASS - init=0 legacy_adopt=1
legacy-doctor-without-initializer-examples: PASS - rc=0
initialized-doctor-unchanged: PASS - rc=0
status-current-requires-exactness: PASS - current=0 drift=1
upgrade-preserves-adoption-seam: PASS - upgrade=0 status=0 doctor=0
partial-adoption-fail-closed: PASS - first:.agent-plus/PROFILE.md:[1, 1, 1, 1, 1]; middle:CLAUDE.md:[1, 1, 1, 1, 1]; last:tests/test_interface_consumer_guard.py:[1, 1, 1, 1, 1]
DIRECT_SYNTHETIC_MATRIX=PASS
~~~

The FIFO attack used no writer and a two-second timeout for adopt, status, canonical doctor,
copied doctor, canonical context, and bootstrap context. Each rejected without a context header.
The omission attack removed the first, middle, and last managed entry and ran all five named
consumers for every position. Each rejected before context output.

## Registered attack matrix

| Registered attack | Outcome | Evidence |
| --- | --- | --- |
| exact-managed-before-record | PASS | Disposable exact-byte target was adopted; declaration and manifest were published and managed bytes remained exact. |
| divergent-managed-block | PASS | One managed byte was changed; adopt returned 1 and did not publish a manifest. |
| project-owned-preservation | PASS | Project-owned sentinel survived adopt and upgrade byte-for-byte. |
| fixed-hook-path | PASS | Mutated declaration path made status and doctor reject. |
| hook-failure-before-context | PASS | Exit 7 rejected canonical doctor, copied doctor, and both context routes; no AGENTS.md header was emitted. |
| hook-symlink-and-nonregular-block | PASS | Symlink, directory, and no-writer FIFO hooks rejected; FIFO commands completed within two seconds. |
| absent-hook-policy | PASS | Initialized project accepted an absent optional hook; legacy adopt rejected a missing required hook. |
| legacy-doctor-without-initializer-examples | PASS | Copied doctor passed an adopted target without initializer-only project examples. |
| initialized-doctor-unchanged | PASS | Initialized doctor still passed with an optional hook that exits 7; it preserved existing non-adoption behavior. |
| status-current-requires-exactness | PASS | Current status passed; managed drift returned non-zero. |
| upgrade-preserves-adoption-seam | PASS | Upgrade preserved declaration, hook, and project-owned bytes; post-upgrade status and doctor passed. |
| partial-adoption-fail-closed | PASS | First, middle, and last manifest omissions returned non-zero in canonical status, canonical doctor, copied doctor, canonical context, and bootstrap context, with no context header. |
| public-validator | PASS | Public-package validator and its 128-test suite passed. |

All 13/13 registered attacks passed.

## Named coverage

| Named coverage | Outcome | Evidence |
| --- | --- | --- |
| lifecycle-cli | PASS | Direct init, adopt, status, doctor, and upgrade commands passed in disposable targets. |
| manager-record-and-adopt-interface | PASS | Exact-byte adoption passed and divergent bytes were rejected before manifest publication. |
| manifest-schema | PASS | Exact 13-file set was enforced by every copied consumer; first/middle/last omissions all rejected. |
| adoption-declaration | PASS | Closed declaration fields and fixed startup path were enforced. |
| context-script | PASS | Hook failure, FIFO, omission, and optional-state routing were checked before output. |
| project-hook | PASS | Regular executable, symlink, directory, FIFO, missing, and nonzero-exit behavior was checked. |
| doctor | PASS | Canonical and copied legacy doctor routes agreed on hook and manifest failures. |
| initializer | PASS | Initialized optional-hook policy and unchanged doctor behavior passed. |
| status | PASS | Current, drifted, fixed-path, FIFO, and subset-manifest targets were checked. |
| upgrade-and-recovery | PASS | Legacy adoption seam preservation passed; the complete lifecycle suite passed. |
| sync-workflow | PASS | Public validation and documentation/binding checks passed without changing sync authority. |
| bootstrap | PASS | Bootstrap context rejected FIFO and all three subset-manifest positions before headers. |
| public-docs | PASS | Public-package validation and internal link checks passed. |
| synthetic-tests | PASS | Focused tests and the separate disposable matrix passed. |
| public-validator | PASS | bash scripts/validate-public-package.sh passed. |

All 15/15 named coverage items passed.

## Frozen adjacent hashes

The required outcome-audit and validator bytes remained exact:

~~~text
e1b94b1b8c6ad138ac7e8d7d2b0ac6d13d4175e52fcc771cac90406a448fc663  skills/outcome-audit/outcome_audit.py
b92e96cb35d2d735979dadf5aa55a753abf9737f52562e387095afe6c5255cbf  tests/test_outcome_audit.py
d694b45ca1596336cdd25f93c9f701f808d32a22eb28b9c07aaea6b1defa6c31  skills/outcome-audit/SKILL.md
6864bb410a8824b64db1ac7f17e854c9189f43224056f89d9377110087c3c15b  .planning/essential-tasks/2026-08-22-agent-plus-outcome-audit-integrated-review-004.md
104115a84fceff8aafd8970f91f4dce8e6afa486e1701726c0cf73095db252a0  scripts/validate-public-package.sh
~~~

## Findings

No promotion-blocking finding remains in the declared attempt-003 boundary. The two attempt-002
findings are closed by the inspected behavior: FIFO hooks reject before any blocking read, and
all copied/canonical consumers require the exact managed-file set before context output.

## Integrated decision

PASS. The attempt-003 legacy-adoption engineering boundary is ready for a separate owner release
decision. This review does not authorize release, consumer synchronization, consumer adoption, or
SECOND LOOK changes.

Closeout guard:

~~~text
python3 scripts/anti_loop_guard.py \
  --ledger .agent-plus/engineering-boundaries.json \
  --packet .agent-plus/agent-plus-legacy-adoption-architecture-review-003.json \
  --require-complete-engineering-review
status: PASS
receipt_id: sha256:09058cb34a4cc6b4d36efa4d740825cbe08ff8fb364bb404e73b079e3c8640e6
packet_sha256: 23bfe53bf321f08b0934fc95d04d69b68a1510db5a7c8e0ede5fa587875eafde
ledger_sha256: 04f9bf9c846d4f78bd251a739576114c406b59e5547e2e597cfbc1ecf36bb860
~~~

Review packet closeout fields are now review_status: complete,
attack_matrix.status: complete, and named_coverage.status: complete.

Exact restart command for a later owner-authorized release decision:

~~~sh
./scripts/ai-context.sh
~~~
