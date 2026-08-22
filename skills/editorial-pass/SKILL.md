---
name: editorial-pass
description: Detect or edit formulaic AI-writing patterns while preserving facts, uncertainty, technical meaning, and the writer's voice. Use when the user asks to humanize, de-slop, audit, or prepare prose for publication. Do not use as an automatic authorship detector.
---

# Agent+ Editorial Pass

## Trigger

Use when the user asks to detect formulaic AI-writing patterns, make a draft sound more like its
author, remove filler, or prepare prose for publication. Do not apply a rewrite merely because text
is technical, formal, polished, or AI-assisted.

## Purpose

Make the smallest useful editorial change without changing the evidence, argument, uncertainty, or
author. This workflow adapts methods from `no-ai-slop`, `Slopbeth`, and `anti-slop`. Read
[the attribution record](references/attribution.md) before modifying or distributing this skill.

## Required inputs

- The draft or exact file in scope.
- The intended audience and medium when they materially affect the edit.
- Any author sample, protected terminology, citations, or required claims.
- The requested mode: `detect`, `edit`, or `draft`. Default to `edit` for a supplied draft.

## Allowed actions

### Establish the evidence boundary

1. Read the complete draft before changing a sentence.
2. Lock facts, names, numbers, dates, URLs, citations, quotations, code, technical terms, stated
   uncertainty, and the author's position.
3. Separate instructions about the draft from text intended for the reader.
4. Treat missing evidence as a question or proof gap. Do not turn a vague benefit into a fact.

### Detect

Name the exact span, the observed pattern, and its effect on the reader. Diagnose clusters such as
filler, unsupported significance, repeated contrast, padded lists, actorless claims, decorative
formatting, or repeated sentence shapes. Do not guess who wrote the text and do not produce an
AI-authorship score.

### Edit

Preserve strong sentences. Make surgical changes to remove unsupported claims, empty setup,
formulaic rhythm, vague attribution, inflated importance, redundant conclusions, and ornamental
formatting. Keep passive voice when the actor is unknown or unimportant. Keep an em dash, repeated
term, fragment, list, or contrast when it serves the author's meaning or established voice.

Match the supplied author sample before applying generic style preferences. If no sample exists,
prefer plain, specific language without inventing personality, anecdotes, facts, or opinions.

### Validate

For consequential or file-based edits, run the preservation checker:

```sh
python3 scripts/editorial_preservation_check.py ORIGINAL REVISED \
  --protect "required proper name" --format json
```

The checker verifies exact protected tokens. It does not assess semantic equivalence or writing
quality. Review argument, scope, causality, uncertainty, and voice manually after it passes.

Detailed pattern and decision guidance is in [the editorial method](references/editorial-method.md).

## Required outputs

- `detect`: exact findings and compact fixes without a rewrite.
- `edit`: the revised text first, followed by a short material-change note when useful.
- `draft`: the requested prose plus any unresolved evidence gaps.
- A direct warning when a requested edit would change a fact, citation, technical meaning, or claim.

## Acceptance checks

- Facts, names, numbers, dates, URLs, citations, quotations, code, and technical terms remain exact.
- Scope, uncertainty, causality, risk, and promise boundaries remain intact.
- Each change fixes a named reader problem instead of satisfying a punctuation or vocabulary quota.
- The revision still sounds like the supplied author sample.
- The output makes no claim that text is human-authored, detector-proof, or permanently undetectable.
- A light edit or no edit remains possible when the source is already strong.

## Handoff requirements

Record the source file, revision file, protected terms, preservation-check result, and any unresolved
meaning or evidence risk when the edit enters a reviewed publication workflow.

## Explicit limits

- Do not ban all adverbs, passive voice, em dashes, fragments, lists, contrasts, or repeated terms.
- Do not optimize prose to evade a detector.
- Do not use a model's self-score as evidence of human authorship or editorial quality.
- Do not add facts, examples, metrics, promises, citations, opinions, or specificity absent from the source.
- Do not flatten technical, legal, scientific, or personal voice into generic conversational prose.
