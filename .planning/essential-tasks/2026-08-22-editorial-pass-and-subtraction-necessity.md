---
task: "Add one attributed editorial skill and one attributed implementation-subtraction control"
owner_role: "maker"
tier: "2"
time_budget: "60 minutes"
attempt_limit: 1
orchestration_mode: "quick"
exact_model: "Sol maker, deterministic evaluator, fresh reviewer required before release"
reasoning: "implementation"
authorization_scope: "Owner authorized the audited Agent+ editorial and Ponytail adaptations"
ownership_map: "Sol is the only writer; deterministic tests evaluate; a fresh reviewer remains required"
chain_stages: "necessity card, maker, deterministic evaluation, fresh review, owner release decision"
concurrency: "one writer, no parallel workers"
tool_budget: "maker 32 calls and 60 minutes"
context_budget: "ordinary 25K ceiling, implementation target 8K-15K"
reserve_use: "not used"
checkpoint_interval: "return after deterministic evaluation"
overnight: "no"
unattended_execution: "no"
unattended_command: "not-applicable"
durable_evidence: "this task card and deterministic test output"
return_check: "not-applicable"
polling_policy: "not-applicable"
evaluator_commands: "python3 -m unittest discover -s tests -p 'test_editorial_pass.py'; bash scripts/validate-public-package.sh"
fresh_verifier_contract: "Review attribution, preservation behavior, public safety, protocol binding, and scope before release"
promotion_dossier: "this task card"
anti_loop_packet: "not dispatched; no promotion-boundary reviewer in this maker task"
review_closeout: "required before release"
---

# Editorial pass and implementation subtraction

## Necessity

- **Decision:** Whether Agent+ should ship one attributed editorial workflow and one subtraction-first implementation control.
- **Uncertainty:** The audited sources are useful, but Agent+ does not yet provide a focused voice-preserving editorial route or an explicit reuse ladder.
- **Existing evidence:** The audit established the source set and rejected rigid punctuation, vocabulary, detector, and self-scoring rules.
- **Minimum action:** Add one optional skill, one preservation checker, synthetic tests, and one concise protocol rule.
- **Unlock:** A later accepted Agent+ release can provide these controls to public consumers and SECOND LOOK.

## Boundary

- **Allowed artifacts:** `skills/editorial-pass/`, `scripts/editorial_preservation_check.py`, `tests/test_editorial_pass.py`, `ESSENTIAL_WORK_PROTOCOL.md`, its bootstrap copy, public validation, router, and public documentation.
- **Allowed actions:** Write original public-safe guidance, preserve third-party notices, add deterministic tests, and run existing validators.
- **Forbidden actions:** Lifecycle repair, Git commit or push, release, package publication, SECOND LOOK synchronization, private-state copying, scientific work, or live work.
- **Review mode:** Engineering sweep.
- **Failure-class coverage:** Attribution loss, source misrepresentation, factual-token drift, rigid style bans, unsupported AI-detector claims, bootstrap drift, and router omission.
- **Simplification trigger:** Any failed deterministic boundary stops this maker attempt. Do not expand into a general writing framework.
- **User-visible outcome:** Agent+ contains a reviewable editorial skill and subtraction-first control with durable citations.
- **Stop condition:** Deterministic checks pass or one complete `BLOCK` is recorded.
- **Stop behavior:** Collect the named deterministic failures, then stop.
- **Attack matrix:** Source citations, license notices, token preservation, explicit protected terms, JSON receipt, bootstrap equality, and public-package validation.
- **Named coverage:** Editorial trigger, detect/edit modes, evidence boundary, minimal edits, punctuation judgment, Ponytail attribution, and release hold.
- **Promotion dossier:** This task card.
- **Dispatch guard:** No subagent maker or reviewer dispatched in this task.
- **Review closeout guard:** Fresh independent review remains required before release.
- **Changed interfaces:** New optional skill and new command-line preservation checker.
- **Consumer discovery:** Agent+ router, README, bootstrap guide, public validator, and workflow-default tests.
- **Consumer closure:** Each named consumer receives a link or deterministic check.
- **Runtime wrappers:** None.
- **Real-shape smoke:** Synthetic command-line checker tests.
- **Repeat trigger:** A deterministic failure, reviewer finding, or changed upstream source decision.
- **Acceptance:** `python3 -m unittest discover -s tests -p 'test_editorial_pass.py'` and `bash scripts/validate-public-package.sh` pass.

## Decision branches

- **If PASS:** Stop with maker-complete state. Require fresh review before any release or downstream synchronization.
- **If BLOCK or FAIL:** Preserve evidence and return one bundled correction boundary. Do not release or synchronize.

## Closeout

Integrated status: `AGENT_PLUS_EDITORIAL_PASS_AND_SUBTRACTION_REVIEW_ACCEPTED — RELEASE BLOCKED`.

Deterministic evidence:

```text
python3 -m unittest discover -s tests -p 'test_editorial_pass.py'
6 tests passed

bash scripts/validate-public-package.sh
98 tests passed
Canonical/bootstrap guard bindings: PASS
Internal Markdown links: PASS
Public package validation: PASS

python3 .../skill-creator/scripts/quick_validate.py skills/editorial-pass
Skill is valid

ESSENTIAL_WORK_PROTOCOL.md and bootstrap/base/ESSENTIAL_WORK_PROTOCOL.md
sha256:dee177185f2a5c19542e95d3524c3d29cf37931e4d87df2d71bab514697f06cb
```

The initial focused command used module import syntax against a non-package `tests/` directory. It
returned an import error before loading a test. The corrected repository discovery command passed.
No implementation retry or hidden fallback occurred.

One fresh Luna xhigh reviewer completed every registered attack and named coverage item with
`PASS`. The completed closeout packet passed the guard with receipt
`sha256:2903dc923814a9d85eb3ec73a1f3213ea9a6ff3f190d95cc024a3ce0dbcd2d55`.
The feature boundary is accepted. The separate lifecycle `BLOCK` still prohibits release and
SECOND LOOK synchronization.

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: later release after separate lifecycle closure and owner authorization
user_visible_outcome: reviewable attributed editorial and subtraction controls in Agent+
repeat_trigger: changed feature bytes, source decision, or acceptance contract
```
