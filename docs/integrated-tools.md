# Integrated External Tools and Workflows

The skills in `skills/` are custom Agent+ procedures. The tools below are external projects or installed workflows. Agent+ can integrate with them, but does not claim to have created them.

| Integration | Role in an Agent+ workflow | Boundary |
| --- | --- | --- |
| [Get Shit Done](https://github.com/open-gsd/gsd-core) | Phase planning, execution packets, and verification structure. | External workflow. Review its license and version before use. |
| [SuperClaude](https://github.com/gwendall/superclaude) | Command-oriented GitHub workflow for commits, changelogs, documentation, and code review. | External workflow. It does not certify scientific evidence. |
| [Tavily](https://tavily.com/) | Web research and source discovery. | Discovery is not source validation. |
| [NotebookLM](https://notebooklm.google.com/) | Source-grounded exploration and synthesis. | Outputs require source and claim review. |
| Caveman and Cavecrew | Agent workflow and collaboration support. | External tools. They do not own project authority. Pin the installed package source before use. |
| [I Have ADHD](https://github.com/ayghri/i-have-adhd) | Action-first, visible-state operating style. | External MIT-licensed skill. Agent+ adapts its response shape in `AI_AGENT_OUTPUT_POLICY.md` and does not require the skill at runtime. Inspected commit: `72c33eee81ea439cf01991e93729adfce2ffc99e`. |
| [Matt Pocock's Skills](https://github.com/mattpocock/skills) | Project grilling plus engineering disciplines for domain language, module design, bug diagnosis, and throwaway prototyping. | External skills. They improve the work around an analysis but do not certify baseball evidence or promote claims. Pin the upstream commit and preserve the license. |

Pin versions or commits in a consuming project. Confirm each license and upstream guidance at the time of integration. Do not vendor external content unless its license permits it and attribution is preserved.

## Matt Pocock skills used in the Agent+ workflow

Agent+ uses selected skills from Matt Pocock's public repository:

| Skill | Use in a baseball project |
| --- | --- |
| `grill-me` and `grilling` | Provide a portable, stateless design-tree interview for sharpening an idea without writing project files. |
| `domain-modeling` | Sharpens the shared vocabulary for questions, artifacts, gates, claims, and decisions. |
| `codebase-design` | Encourages deep modules with small interfaces, clear seams, and testable implementations. |
| `diagnosing-bugs` | Builds a red-capable feedback loop, then reproduces, minimizes, hypothesizes, instruments, and regression-tests a failure. |
| `prototype` | Uses throwaway code to answer one design or state-model question before production work. |

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

The canonical `skills/` directories are the source. Regular-file mirrors under `.agents/skills/`
expose them to Codex. Public validation requires identical file sets, bytes, and modes, including
references, assets, and license notices. All skills carry name and description metadata.
The seven generic procedure names use an `agent-plus-` skill-name prefix to distinguish local policy
from installed global tools. Directory paths remain stable for existing references.

Use `$agent-plus-model-review` for prospective workflow comparison and `$agent-plus-session-context-handoff`
for local closeout. The installed global `model-review` is a separate session-usage collector. It must
not run merely because an Agent+ policy mentions model review. Explicit invocation still selects it.

Consumer bootstrap installs the managed control plane. Native mirrors apply to this repository only.
Install optional consumer skills separately from an accepted release as described above. Existing
third-party plugin bytes are unchanged. When maintaining a skill, update its canonical directory and
its complete native mirror together; the parity test rejects drift.

The official [skill documentation](https://learn.chatgpt.com/docs/build-skills) explains metadata,
progressive disclosure, symlink discovery, and duplicate names. Trigger tests must cover both
intended matches and nearby requests that must not activate the workflow.
