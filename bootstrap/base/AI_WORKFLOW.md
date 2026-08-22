# AI Workflow

## Routing

| Tier | Work | Required control |
| --- | --- | --- |
| 0 | Search, count, hash, parse, test, and score. | Record exact output. |
| 1 | Reversible extraction, classification, and drafts. | Check before use. |
| 2 | Bounded implementation. | Named acceptance check. |
| 3 | Leakage, architecture, and fresh review. | Independent context. |

The maker creates. The evaluator computes. The verifier reviews. The human owner decides what can be claimed.

Every task records allowed inputs, budget, acceptance check, and stop condition. No silent model fallback is allowed.

## Direct model delegation

When the owner explicitly requests delegation, sub-agents, parallel work, or Luna, Sol manages the
task and creates model-selected Luna sub-agents directly. The owner should not need to open separate
chats or copy results between them.

- Luna High: routine diagnostics, corrections, documentation, tests, and scoped implementation.
- Luna xhigh: complex multi-file engineering, architecture tracing, long read-only work, and fresh
  engineering review.
- Sol: task splitting, boundaries, progress, synthesis, and the owner-facing result.
- Premium reasoning: scientific ambiguity, leakage, frozen contracts, hard architecture, and
  irreversible promotion decisions.

Give every worker one concrete deliverable, exact ownership, allowed inputs, a stop condition, and a
budget. Select its model explicitly and pass bounded context. Parallel tasks must be independent;
workers must not overlap edits, recursively spawn, silently fall back, or self-certify. Use one
bounded wait instead of polling. If direct model selection is unavailable, record `BLOCK` rather
than create repeated manual cross-chat handoffs.

## Higher-capacity session profile

Extra capacity increases bounded throughput only. It does not increase authority, context ceilings,
retry count, reviewer count, or owner decision rights. Select one mode in the task packet:

| Mode | Route | Total wall-time budget |
| --- | --- | ---: |
| `quick` | Sol/high control; at most one Luna High explorer; Luna High maker; deterministic evaluator; fresh Luna xhigh only at promotion. | 45 minutes |
| `standard` (default) | Sol/high control; two independent Luna High explorers; Luna xhigh maker; deterministic evaluator; one fresh Luna xhigh reviewer. | 90 minutes |
| `deep` | Sol/high control; up to three independent Luna xhigh explorers; one accountable maker (Luna xhigh or explicitly selected Claude Sonnet high; Opus high only for named hard architecture/frozen contract); deterministic evaluator; one fresh independent reviewer. | 120 minutes |
| `scientific/live` | Up to two read-only Luna xhigh readiness explorers; zero parallel workers during live execution; deterministic metrics; fresh premium scientific reviewer only for the named decision; human owner authorization before data access, live execution, or promotion. | Owner-set task budget |

An owner command may authorize plan → independent explorers → frozen evidence handoff → exclusive
maker → deterministic evaluator → fresh reviewer → Sol synthesis for engineering only. Exploration
may be parallel; all later stages are sequential. Use a controller plus two workers by default and
never more than three workers, one writer per repository, no overlapping writes, no recursive spawn,
no silent fallback, and one bounded wait per stage. The reviewer receives the contract, artifact,
receipts, and attack matrix, not the maker transcript. Stop on maker, evaluator, or reviewer
`BLOCK`; do not auto-repair after a reviewer `BLOCK`.

Context remains capped at 25K ordinary and 40K premium. Targets are 4–8K routine, 8–15K
implementation, and 12–25K premium; start fresh at 60–80K accumulated tokens. Routine makers use
32 tool calls/60 minutes, complex makers 40/90 minutes, engineering reviewers 20/45 minutes, and
scientific/live reviewers 12/25 minutes. Failed attempts remain capped at two. Reserve 25% of
premium allowance for scientific, leakage, hard-architecture, or irreversible decisions. Do not burn
capacity without a decision-relevant deliverable.

Overnight mode requires an explicit owner command and permits only read-only or reversible
engineering, at most three workers, a fixed queue of at most eight, and a default four-hour window.
Checkpoint every 30 minutes or 100K fresh tokens. No live, scientific, promotion, or queue-refill
work is permitted; stop on `BLOCK`.

## Unattended execution

Use unattended execution only when one bounded process can own the complete run and write durable
evidence without AI supervision. The task card must name the exact command, one authorized launch,
the durable progress and terminal evidence paths, the expected return point, and one result check.

After launch, the AI controller must not poll the process, terminal, logs, or evidence files. The
process writes its own progress and terminal state. On return, the controller performs one result
check against the named terminal evidence and acceptance rule.

A launch error, process error, missing terminal evidence, or failed return check consumes the
authorization and returns `BLOCK`. Do not fall back, relaunch, or retry. Resume only after bounded
repair, any required fresh review, and new explicit authorization. Process-written evidence does
not grant promotion authority or replace independent verification.

Repeat model review after 10 completed bounded chains or 14 days, and immediately after model/rate/
plan changes, two routing `BLOCK`s, average context above 40K, or reviewer correction above 20%.
This cadence is a maintenance control, not a performance claim.

## Engineering closure

Scientific, live, destructive, and irreversible execution stops at the first invalid condition.
Engineering diagnostics block promotion at the first defect but continue bounded read-only attacks
to collect the complete reachable defect class. One maker repairs that class and one fresh verifier
reviews the integrated boundary.

After a second BLOCK at the same interface, replace or constrain the interface instead of starting
a third local patch. Prefer designs that make invalid states impossible. Measure success by the
user-visible or scientific result unlocked, not by tests, files, tokens, or review count.

Before dispatching an engineering maker or reviewer, require a PASS receipt from
`scripts/anti_loop_guard.py` for a packet whose boundary and failure class already exist in the
ledger. A reviewer may start with a planned packet, but its verdict cannot unlock another maker or
owner decision until the ledger-bound review closes with complete attack-matrix and named-coverage
status using `--require-complete-engineering-review`. A defect blocks promotion immediately but
does not end safe read-only attacks in the declared matrix. Record a review BLOCK only after that
closeout passes. Do not dispatch a maker from a partial reviewer narrative.

Keep one active promotion-boundary dossier. Update its task contract, cumulative finding matrix,
acceptance receipt, and integrated review in place instead of creating a new packet set for every
local correction.

## Anti-loop guard packet

Use `scripts/anti_loop_guard.py` with `.agent-plus/engineering-boundaries.json` to validate each
task or review packet. Schema `anti-loop-guard/v2` is closed and strictly structured. Packets
require stable boundary and failure-class IDs, ledger-declared coverage, one `change_kind`, one
`outcome_kind` from a closed enum, one ledger-approved `outcome_id`, one stop policy, and both
ledger-bound matrices. A completed engineering review must prove complete attack-matrix and named
coverage. After two BLOCKs, only an architecture reset with the ledger-approved namespace, attempt
identifier, and removed caller choices may pass; scientific and live packets remain first-error
gates.

The packet carries no free text, so wording cannot relabel a local repair as an architecture reset.
The guard owns a closed exact outcome catalog; a ledger may select only a subset of its IDs and may
not create, rename, case-change, path-traverse, or recategorize an ID. Process work such as tests,
lint, files, documents, receipts, or reviews has no catalog entry and cannot be declared as a user
or scientific outcome. The guard rejects duplicate JSON keys and non-string mapping keys at every
depth, unknown fields, unsupported schema versions, wrong types, malformed JSON, and non-exact
BLOCK counts as typed errors. Completed matrices must match the exact names in the ledger. PASS
receipts bind the canonical packet and full ledger state. BLOCK updates use a lock plus durable
atomic replacement; lock, corruption, and write failures are typed guard errors.

After a closed-interface recovery passes its required review, keep the constrained interface as the
default for that failure class. Do not restore removed caller choices or open inputs without a new
necessity card, a named consumer, deterministic acceptance checks, and required review.
