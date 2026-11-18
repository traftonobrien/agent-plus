# Integrated External Tools and Workflows

The skills in `skills/` are custom Agent+ procedures. The tools below are external projects or installed workflows. Agent+ can integrate with them, but does not claim to have created them.

| Integration | Role in an Agent+ workflow | Boundary |
| --- | --- | --- |
| [Tavily](https://tavily.com/) | Web research and source discovery. | Discovery is not source validation. |
| [NotebookLM](https://notebooklm.google.com/) | Source-grounded exploration and synthesis. | Outputs require source and claim review. |
| [Caveman and Cavecrew](https://github.com/JuliusBrussee/caveman) | Compressed communication and delegation guidance. | External MIT-licensed skills. Their installed bytes map to separate exact upstream revisions recorded below; no engine or proxy code is bundled. |
| [I Have ADHD](https://github.com/ayghri/i-have-adhd/tree/72c33eee81ea439cf01991e93729adfce2ffc99e) | Action-first, visible-state operating style. | External MIT-licensed skill. Agent+ adapts its response shape in `AI_AGENT_OUTPUT_POLICY.md`; the [source record](attribution/output-policy.md) preserves the pinned source and notice. |
| [Matt Pocock's Skills](https://github.com/mattpocock/skills/tree/9c9f36ccd3995266cd675468af71639c8dde1ec5) | Project grilling plus engineering disciplines for domain language, module design, bug diagnosis, and throwaway prototyping. | External MIT-licensed skills inspected at `9c9f36ccd3995266cd675468af71639c8dde1ec5`. They improve work around an analysis but do not certify evidence or promote claims. |

The pinned revisions above are the versions inspected for this attribution audit on 2026-08-31;
they are not automatic update authority. Confirm each license and upstream guidance before changing
an installation. Agent+ does not redistribute these external workflows, except for the separately
attributed adaptations named in their source records. Do not vendor external content unless its
license permits it and attribution is preserved.

## Parked workflows

GSD and SuperClaude are parked. Agent+ does not install, invoke or require either suite in its
normal setup, planning, coding, review or restart routes. Use the existing Agent+ procedures.
An explicit owner request can select a parked workflow; merely finding its files or citations
is not a reason to activate it.

The entries below preserve source attribution only. No workflow code, compatibility records or
historical examples were deleted.

| Parked reference | Former role | Retained provenance |
| --- | --- | --- |
| [Get Shit Done](https://github.com/gsd-build/get-shit-done/tree/2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f) | Phase planning, execution packets, and verification structure. | External MIT-licensed workflow version `1.22.4`, inspected at `2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f`. No GSD code is bundled here. |
| [SuperClaude](https://github.com/SuperClaude-Org/SuperClaude_Framework/tree/226c45cc93b865108843a669c6545d421784b68c) | Command-oriented workflow for analysis, implementation, documentation, and review. | External MIT-licensed command source inspected at `226c45cc93b865108843a669c6545d421784b68c`. Local wrappers and aliases are not presented as upstream files. |

## Secondary skill source records

These are the exact external skill or command sources recorded alongside Agent+. GSD and
SuperClaude remain parked references, not active workflow recommendations. External installations
remain separate from Agent+. A citation here does not make them Agent+ code and does not grant them
scientific, release, or owner authority.

### Get Shit Done

- Package: `get-shit-done-cc` version `1.22.4`.
- Repository: [`gsd-build/get-shit-done`](https://github.com/gsd-build/get-shit-done).
- Inspected commit: [`2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f`](https://github.com/gsd-build/get-shit-done/tree/2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f).
- Representative sources: [`commands/gsd/plan-phase.md`](https://github.com/gsd-build/get-shit-done/blob/2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f/commands/gsd/plan-phase.md) and [`get-shit-done/workflows/plan-phase.md`](https://github.com/gsd-build/get-shit-done/blob/2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f/get-shit-done/workflows/plan-phase.md).
- License: [MIT](https://github.com/gsd-build/get-shit-done/blob/2eaed7a8475839958f9ec76ca4c26d9a0bbfc33f/LICENSE).

The former `open-gsd/gsd-core` citation did not identify the installed `get-shit-done-cc` source and
is intentionally not used.

### SuperClaude

- Repository: [`SuperClaude-Org/SuperClaude_Framework`](https://github.com/SuperClaude-Org/SuperClaude_Framework).
- Inspected commit: [`226c45cc93b865108843a669c6545d421784b68c`](https://github.com/SuperClaude-Org/SuperClaude_Framework/tree/226c45cc93b865108843a669c6545d421784b68c).
- Representative source: [`src/superclaude/commands/analyze.md`](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/226c45cc93b865108843a669c6545d421784b68c/src/superclaude/commands/analyze.md).
- License: [MIT](https://github.com/SuperClaude-Org/SuperClaude_Framework/blob/226c45cc93b865108843a669c6545d421784b68c/LICENSE).

Installed `source-command-sc-*` skills wrap or adapt the command sources. The citation does not
claim that local wrappers, aliases, or the local `sc-brain` command are unchanged upstream files.
The former `gwendall/superclaude` citation pointed to a different repository and is intentionally
not used.

### Caveman and Cavecrew

The installed skill bytes require separate pins:

- `caveman`: [`skills/caveman/SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/e8eae0ff283bb808e50cb1a9cee9dc0129d9316e/skills/caveman/SKILL.md) at
  [`e8eae0ff283bb808e50cb1a9cee9dc0129d9316e`](https://github.com/JuliusBrussee/caveman/tree/e8eae0ff283bb808e50cb1a9cee9dc0129d9316e), with its [MIT license](https://github.com/JuliusBrussee/caveman/blob/e8eae0ff283bb808e50cb1a9cee9dc0129d9316e/LICENSE).
- `cavecrew`: [`skills/cavecrew/SKILL.md`](https://github.com/JuliusBrussee/caveman/blob/7bb71309e8749a4f112aacd3a54b3941d8689905/skills/cavecrew/SKILL.md) at
  [`7bb71309e8749a4f112aacd3a54b3941d8689905`](https://github.com/JuliusBrussee/caveman/tree/7bb71309e8749a4f112aacd3a54b3941d8689905), with the skill covered by the repository's [MIT scope](https://github.com/JuliusBrussee/caveman/blob/7bb71309e8749a4f112aacd3a54b3941d8689905/LICENSE).

The repository also contains engine-linked BSL-licensed components at later revisions. Agent+
does not bundle or attribute those components as skill code.

### Adapted secondary sources

- The output-policy adaptation pins Ayoub Ghriss's `i-have-adhd` source and MIT notice in the
  [output-policy attribution record](attribution/output-policy.md).
- The Discovery Grill adaptation pins Matt Pocock's `grill-me` and `grilling` sources and MIT
  notice in its [attribution record](../skills/agent-plus-discovery-grill/references/attribution.md).
- The Editorial Pass synthesis pins `no-ai-slop`, `Slopbeth`, and `anti-slop`, with their MIT
  notices, in its [attribution record](../skills/editorial-pass/references/attribution.md).
- The implementation-subtraction control pins Dietrich Gebert's Ponytail rules and MIT notice in
  its [attribution record](attribution/implementation-subtraction.md).

Operator-only support skills such as `audit-agent-plus-improvements` and `github-deep-research`
remain local and are not redistributed by Agent+. Their current files declare no external upstream
adaptation; they require a separate provenance review before any future public distribution.

## Matt Pocock skills used in the Agent+ workflow

Agent+ uses selected skills from Matt Pocock's public repository:

| Skill | Use in a baseball project |
| --- | --- |
| [`grill-me`](https://github.com/mattpocock/skills/blob/9c9f36ccd3995266cd675468af71639c8dde1ec5/skills/productivity/grill-me/SKILL.md) and [`grilling`](https://github.com/mattpocock/skills/blob/9c9f36ccd3995266cd675468af71639c8dde1ec5/skills/productivity/grilling/SKILL.md) | Provide a portable, stateless design-tree interview for sharpening an idea without writing project files. |
| [`domain-modeling`](https://github.com/mattpocock/skills/blob/9c9f36ccd3995266cd675468af71639c8dde1ec5/skills/engineering/domain-modeling/SKILL.md) | Sharpens the shared vocabulary for questions, artifacts, gates, claims, and decisions. |
| [`codebase-design`](https://github.com/mattpocock/skills/blob/9c9f36ccd3995266cd675468af71639c8dde1ec5/skills/engineering/codebase-design/SKILL.md) | Encourages deep modules with small interfaces, clear seams, and testable implementations. |
| [`diagnosing-bugs`](https://github.com/mattpocock/skills/blob/9c9f36ccd3995266cd675468af71639c8dde1ec5/skills/engineering/diagnosing-bugs/SKILL.md) | Builds a red-capable feedback loop, then reproduces, minimizes, hypothesizes, instruments, and regression-tests a failure. |
| [`prototype`](https://github.com/mattpocock/skills/blob/9c9f36ccd3995266cd675468af71639c8dde1ec5/skills/engineering/prototype/SKILL.md) | Uses throwaway code to answer one design or state-model question before production work. |

These skills are integrated engineering disciplines, not Agent+ creations. Their value in the
system is that they improve the quality of the question, the implementation seam, the diagnostic
loop, and the decision to promote a prototype. They still operate under Agent+'s research contract,
deterministic evidence, and verification rules.

## Agent+ stateful adaptation

[`agent-plus-discovery-grill`](../skills/agent-plus-discovery-grill/SKILL.md) is an Agent+ adaptation
of Matt Pocock's grilling method. It asks one question at a time for voice-friendly discovery and
updates `.planning/discovery/PROJECT-DISCOVERY.md` after each answer. The file is a decision brief,
not a transcript. Completion routes to a research contract, evidence task, prototype, scope split,
or `BLOCKED`; it does not authorize analysis or promote a claim.

Install the original and the Agent+ adaptation as separate skills so upstream updates remain clean:

```sh
npx skills@latest add mattpocock/skills --skill=grill-me
npx skills@latest add traftonobrien/agent-plus --skill=agent-plus-discovery-grill
```

The Agent+ adaptation preserves explicit upstream attribution in its skill folder. Review the
current upstream instructions and license before updating either installation.

## Native Agent+ skill discovery

The canonical `skills/` directories are the source. Matching installed directories under
`.agents/skills/` expose them to Codex. Update each affected installed copy with its canonical
source. The existing discovery test checks content and file-mode parity. All skills carry name
and description metadata.
The seven generic procedure names use an `agent-plus-` skill-name prefix to distinguish local policy
from installed global tools. Directory paths remain stable for existing references.

Use `$agent-plus-model-review` for prospective workflow comparison and `$agent-plus-session-context-handoff`
for local closeout. The installed global `model-review` is a separate session-usage collector. It must
not run merely because an Agent+ policy mentions model review. Explicit invocation still selects it.

Consumer bootstrap installs the managed control plane, not this repository's installed skill copies.
Install optional skills separately from an accepted release as described above. Never copy links
pointing back to a developer checkout into a consumer. Existing third-party plugin bytes are unchanged.

The official [skill documentation](https://learn.chatgpt.com/docs/build-skills) explains metadata,
progressive disclosure, symlink discovery, and duplicate names. Trigger tests must cover both
intended matches and nearby requests that must not activate the workflow.
