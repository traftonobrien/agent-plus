# Astra host setup

The 0.4.1 package provides portable instructions, bootstrap controls, and native project skills.
Host configuration remains an explicit local setup step. Installing Agent+ does not change it.

## Select and verify the runtime

Select GPT-6 Astra in Codex and retain your chosen reasoning effort. High was the tested baseline.
A command-line request can select the same model explicitly:

```sh
codex --version
codex exec --model gpt-6-astra -c model_reasoning_effort='"high"' "Explain this project's startup command. Do not edit files."
```

The local compatibility check on September 5, 2026 used Codex CLI 0.153.4 successfully.
CLI 0.146.0 rejected Astra before model execution. This observation does not establish the minimum
supported version. Follow the official [Codex CLI installation instructions](https://developers.openai.com/codex/cli)
for your installation method. The desktop app and a separately installed shell CLI may use different
versions. Verify the runtime used by the actual task.

## Check instruction and skill scope

Run `./scripts/ai-context.sh` from the project root. Read the named current artifact and applicable
procedures. The selected model remains in control. Routine work uses proportionate checks; formal
reviews and release decisions retain their existing requirements.

Codex discovers twelve project skills through `.agents/skills/`. These are checked regular-file
mirrors of `skills/`, with complete assets and references. The package does not install global copies
or remove existing plugins. Avoid installing a second copy of the same workflow without checking
which instruction source the runtime selects.

If you maintain custom agent role files, validate their required metadata with the installed runtime.
A local GSD compatibility repair supplied role names and existing descriptions without changing role
instructions or model settings. Those machine-specific files are not part of this distribution.

## What was checked

Local Astra/high policy scenarios tested instruction conflicts, model selection, delegation,
verification, skill selection, and restart behavior. They do not measure coding speed or establish
that high effort is optimal. Compare representative tasks before claiming a performance improvement.
Consumer upgrades remain explicit, release-pinned operations under [Agent+ Sync](../skills/agent-plus-sync/SKILL.md).
