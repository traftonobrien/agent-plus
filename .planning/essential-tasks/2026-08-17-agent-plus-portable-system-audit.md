---
task: "Audit and establish Agent+ as the canonical portable baseball-work system"
owner_role: "maker"
tier: "2"
time_budget: "120 minutes"
attempt_limit: 2
orchestration_mode: "deep"
exact_model: "Sol controller and maker; deterministic shell and Python evaluator; fresh independent verifier required before publication"
reasoning: "premium"
authorization_scope: "Owner requested a full Agent+ audit, portable setup, and a SECOND LOOK contribution rule"
ownership_map: "Sol owns Agent+ and SECOND LOOK control edits; deterministic commands evaluate; a fresh verifier owns publication review; owner owns release"
chain_stages: "audit -> frozen design -> implementation -> deterministic evaluation -> fresh review -> owner release"
concurrency: "zero workers; one writer per repository"
tool_budget: "maker 40 calls or 90 minutes; evaluator 10 calls or 20 minutes; reviewer 20 calls or 45 minutes"
context_budget: "40K premium ceiling; 12K-25K target"
reserve_use: "Used for the canonical ownership and cross-project architecture decision"
checkpoint_interval: "one checkpoint after the audit and one after deterministic evaluation"
overnight: "no"
evaluator_commands: "scripts/validate-public-package.sh; generated-project initialization and doctor; SECOND LOOK policy verifier"
fresh_verifier_contract: "Review the install, upgrade, source-identity, drift, contribution, and public-safety matrix from changed files and deterministic receipts"
---

# Essential Task Card

## Necessity

- **Decision:** Decide whether this repository can become the canonical Agent+ distribution.
- **Uncertainty:** The current copy, upgrade, drift, and contribution interfaces are not verified.
- **Existing evidence:** Initialization and local validation pass, but installed projects have no version or upgrade contract.
- **Minimum action:** Audit both repositories, define one ownership model, and close the portable-system interface.
- **Unlock:** New baseball projects and external users can install Agent+ and receive controlled updates.

## Boundary

- **Allowed artifacts:** Public Agent+ controls, bootstrap files, scripts, tests, documentation, and SECOND LOOK workflow controls.
- **Allowed actions:** Read, compare, edit control files, add deterministic checks, and run non-scientific tests.
- **Forbidden actions:** Scientific execution, data reads, modeling, promotion, Git commit, Git push, and release publication.
- **Review mode:** Engineering sweep.
- **Failure-class coverage:** Canonical ownership, public install, version binding, safe upgrade, local override preservation, drift detection, contribution flow, and public safety.
- **Simplification trigger:** If copy synchronization needs project-specific path logic, replace it with a repository-owned manifest and commands.
- **User-visible outcome:** A user can install Agent+ into a new or existing project and verify which Agent+ version it uses.
- **Stop condition:** Deterministic checks pass, or a named interface remains `BLOCK`.
- **Stop behavior:** Collect the complete named engineering matrix before one correction.
- **Attack matrix:** Fresh target, existing Agent+ target, missing source, wrong source, modified managed file, valid upgrade, invalid profile, and public-safety scan.
- **Named coverage:** Install, doctor, status, upgrade, source identity, local state preservation, SECOND LOOK drift, and contribution documentation.
- **Repeat trigger:** A changed interface, failed deterministic check, or fresh-review finding.
- **Acceptance:** Public validation, disposable-project lifecycle checks, and SECOND LOOK policy verification pass.

## Decision branches

- **If PASS:** Request one fresh independent review, then publish the canonical repository.
- **If BLOCK or FAIL:** Keep the current GitHub release unchanged and repair the named interface.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: fresh independent integrated review
user_visible_outcome: versioned Agent+ install and safe-update interface is maker-complete
repeat_trigger: fresh-review finding or accepted release decision
```
