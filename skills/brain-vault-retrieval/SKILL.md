# Brain Vault Retrieval

## Trigger

Use when a bounded task needs durable sources, prior decisions, or an approved method from the Obsidian Brain.

## Purpose

Retrieve the smallest curated context packet that can answer a named question.

## Required inputs

- Task question and decision.
- Named Brain scope or search terms.
- Maximum context budget.

## Allowed actions

- Search titles, tags, and linked notes.
- Read the minimum relevant notes.
- Return source-linked excerpts or a no-evidence result.

## Required outputs

- A compact context packet.
- Exact note references.
- Confidence and unresolved gaps.

## Acceptance checks

- Each retrieved item is relevant to the stated task.
- The packet stays within its context budget.
- Facts are labeled as evidence, decision, or background.

## Handoff requirements

Record notes consulted, gaps, and the next deterministic or review action.

## Explicit limits

Do not search private archives by default. Do not substitute curated notes for live evidence. Do not expand scope without a changed decision.
