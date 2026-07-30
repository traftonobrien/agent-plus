# Bootstrap a Baseball Project

Use the initializer only in a project directory you control. It creates a local Agent+ control plane. It never copies SECOND LOOK data, plans, evidence, or state.

## Create a project control plane

```sh
git clone https://github.com/traftonobrien/agent-plus.git
cd agent-plus
scripts/agent-plus-init.sh \
  --target "/absolute/path/to/baseball-project" \
  --profile research \
  --brain-note "05 Projects/My Baseball Project" \
  --github-actions
```

Profiles are `research`, `product`, and `scouting`.

## Safety behavior

- The target directory must already exist.
- The initializer refuses to overwrite existing control files.
- It creates only project-local instructions, planning records, and scripts.
- It does not add data, secrets, or a remote repository.

## Verify the new project

```sh
cd "/absolute/path/to/baseball-project"
scripts/agent-plus-doctor.sh --target .
scripts/ai-context.sh
```

## Use the profiles

Read `.agent-plus/PROFILE.md` after initialization. It adds only the gates relevant to the project type. The project owner still defines its research contract, source authorization, and claim ceiling.
