---
name: agent-plus-claim-evidence-register
description: Check a proposed Agent+ research claim against evidence before publication. Not routine code verification.
---

# Claim-Evidence Register

## Trigger

Use before publishing, presenting, or promoting a research statement.

## Purpose

Match every proposed claim to its required evidence level and evidence record.

## Required inputs

- Proposed claim text.
- Research contract version.
- Evidence record identifiers.
- Intended public wording.

## Allowed actions

- Classify the claim as fit, prediction, decision value, or impact.
- Compare evidence against the required level.
- Mark the claim supported, unsupported, or BLOCK.

## Required outputs

- Updated claim-evidence register.
- Approved wording or a rejected wording explanation.
- Any required verifier action.

## Acceptance checks

- Each claim has an evidence record.
- Claim level does not exceed evidence level.
- Unsupported wording is removed or marked BLOCK.

## Handoff requirements

State claim IDs reviewed, their statuses, and the one next promotion or evidence action.

## Explicit limits

Do not create evidence. Do not infer real-world impact from offline metrics. Do not promote a claim without human approval.
