# Model Review

## Trigger

Run after a project milestone, a model or pricing change, a routing change, or a measured slowdown.
Do not run it only because a session restarted.

## Purpose

Measure whether model use, context loading, routing, and review effort are helping the project move
forward. The skill audits workflow behavior. It is not a scorecard for model intelligence and it
does not certify scientific results.

## Required inputs

Provide the project root, the prior audit checkpoint when one exists, the current workflow policy,
and the bounded question that could change. Do not include private prompts, secrets, or full raw
transcripts in a public report.

## Allowed actions

Collect deduplicated usage and workflow events, compare them with the prior checkpoint, identify
repeated or wasteful behavior, and recommend one bounded experiment or policy change. Measure
before interpreting. Keep deterministic collection separate from model interpretation.

## Required outputs

Return four sections: `Keep`, `Stop`, `Change`, and `Next experiment`. Include the evidence window,
limits, and whether a decision changed. If no decision changed, recommend no policy edit.

## Acceptance checks

The report must identify the evidence window, distinguish new work from repeated unchanged checks,
and name the decision or blocker affected. A policy verifier may confirm that defaults, hooks,
budgets, and repeat guards still match the accepted workflow contract.

## Handoff requirements

Record the report path, checkpoint, changed decision, open limit, and one concrete next action.

## Explicit limits

The skill cannot prove model quality, scientific validity, prediction, decision value, or impact.
It must not silently edit model policy, rerun unchanged evidence, or turn an efficiency finding
into a claim about research truth.
