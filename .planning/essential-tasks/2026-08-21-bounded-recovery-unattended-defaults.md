# Bounded recovery and unattended execution defaults

## Necessity

- **Decision:** preserve two accepted operating patterns as reusable Agent+ defaults.
- **Uncertainty:** the current policy does not fully bind closed-interface recovery to later work or
  define a complete unattended execution contract.
- **Existing evidence:** a proving project completed a bounded recovery and an unattended run, but
  its local state cannot become Agent+ policy by implication.
- **Minimum action:** add generic policy, task-card fields, bootstrap parity, and synthetic tests.
- **Unlock:** new Agent+ projects can use both patterns without copying proving-project details.

## Boundary

- **Allowed artifacts:** public Agent+ policy, bootstrap copies, routing documentation, task
  templates, tests, validator, hot memory, and public state.
- **Allowed actions:** add sanitized defaults and deterministic checks.
- **Forbidden actions:** copy project paths, identities, counts, scientific details, receipts, or
  runtime state; commit, push, tag, release, or announce.
- **Review mode:** engineering sweep.
- **Failure-class coverage:** reopened interfaces, hidden retries, AI polling, weak process evidence,
  and authorization reuse after failure.
- **Simplification trigger:** any default that needs project-specific knowledge must remain a local
  adapter.
- **User-visible outcome:** Agent+ users receive a reusable bounded-recovery and unattended-run
  contract.
- **Stop condition:** focused tests and the public-package validator pass, or a deterministic check
  returns `BLOCK`.
- **Stop behavior:** collect the named documentation and bootstrap parity matrix.
- **Attack matrix:** canonical/bootstrap drift; missing one-launch rule; missing durable terminal
  evidence; polling allowed; retry allowed after failure; closed choices reopened.
- **Named coverage:** public policy, essential protocol, task template, bootstrap copies, routing
  guide, validator, and synthetic tests.
- **Promotion dossier:** this file.
- **Dispatch guard:** not required for a documentation-only generic default with no guard schema
  change.
- **Review closeout guard:** fresh review is required before release.
- **Changed interfaces:** task-card fields and public operating-policy contract.
- **Consumer discovery:** deterministic repository search plus canonical/bootstrap parity test.
- **Consumer closure:** canonical policy, bootstrap policy, template, routing guide, README, and
  validator.
- **Runtime wrappers:** none.
- **Real-shape smoke:** not required because no runtime execution interface changes.
- **Repeat trigger:** a new consumer need or a failed acceptance check.
- **Acceptance:** `python3 -m unittest discover -s tests -p 'test_workflow_defaults.py'` and
  `scripts/validate-public-package.sh`.

## Decision branches

- **If PASS:** record maker-complete state and request fresh review before release.
- **If BLOCK or FAIL:** keep the defaults unaccepted and repair only the reported generic boundary.

## Closeout

```yaml
decision_changed: yes
blocker_closed: none
work_unlocked: fresh review before release
user_visible_outcome: reusable defaults are maker-complete
repeat_trigger: changed evidence or reviewer finding
```
