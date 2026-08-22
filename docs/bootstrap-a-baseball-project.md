# Bootstrap a Baseball Project

Use the initializer only in a project directory you control. It creates a local Agent+ control plane. It never copies SECOND LOOK data, plans, evidence, or state.

## Create a project control plane

```sh
git clone https://github.com/traftonobrien/agent-plus.git
cd agent-plus
scripts/agent-plus init \
  --target "/absolute/path/to/baseball-project" \
  --profile research \
  --brain-note "05 Projects/My Baseball Project" \
  --github-actions
```

Profiles are `research`, `product`, and `scouting`.

Install the discovery skill when the project may begin with an unclear idea:

```sh
npx skills@latest add traftonobrien/agent-plus --skill=agent-plus-discovery-grill
```

Matt Pocock's original `grill-me` and `grilling` skills remain separate pinned external tools. The
Agent+ discovery skill carries its own attribution and durable project-brief workflow; it does not
replace or relabel the originals.

Install the optional editorial skill for publication-oriented detect and edit work:

```sh
npx skills@latest add traftonobrien/agent-plus --skill=editorial-pass
```

The skill includes pinned source citations and preserved MIT notices for `no-ai-slop`, `Slopbeth`,
and `anti-slop`. It does not claim authorship detection or impose universal punctuation bans.

Install the sync skill when this project must check or update its Agent+ controls:

```sh
npx skills@latest add traftonobrien/agent-plus --skill=agent-plus-sync
```

Run `$agent-plus-sync` in `audit` mode first. It requires an exact official release tag and explicit
authorization before it calls the transactional upgrade command.

Install the optional outcome-audit skill when the project needs prospective workflow measures or a
sanitized receipt for private evidence:

```sh
npx skills@latest add traftonobrien/agent-plus --skill=outcome-audit
```

Run its record and report commands on a closed prospective record set. Run the receipt command from
the project root. It reads only `.agent-plus/outcome-audit/evidence-manifest.json` and regular files
below `.agent-plus/outcome-audit/evidence/`. It emits no private path, source reference, or source
content. Missing, denied, mismatched, or unstructured evidence is `BLOCK`.

## Safety behavior

- The target directory must already exist.
- The initializer refuses to overwrite existing control files.
- It creates only project-local instructions, planning records, and scripts.
- It does not add data, secrets, or a remote repository.
- Generic Agent+ controls remain version-managed. Put local rules in `.agent-plus/PROJECT.md`.
- Every generated project receives the plain-language output policy and adapters for Codex, Claude,
  and Cursor. An external `i-have-adhd` skill or plugin is optional.

## Adopt an existing project

For an existing project, prepare the exact managed controls from this checkout and use the closed
adoption command:

```sh
scripts/agent-plus adopt \
  --target "/absolute/path/to/legacy-baseball-project" \
  --profile research
```

The command writes `.agent-plus/legacy-adoption.json` only after every managed target file matches
the canonical source byte-for-byte. It preserves project-owned files and does not require the
initializer-only example records. The declaration requires one project-owned startup seam:
`.agent-plus/project-startup-check.sh`. It must be an executable regular file. The managed
`scripts/ai-context.sh` and doctor run this fixed hook before context output or `PASS` and stop on
hook failure. Existing `.claude-memory.md` and `.planning/STATE.md` files are included in adopted
context when they are regular files; if legacy projects do not have them, those optional sections
are omitted. Normal initialized projects still require both files. No caller-selected hook path is
supported.

## Verify the new project

```sh
cd "/absolute/path/to/baseball-project"
"/absolute/path/to/agent-plus/scripts/agent-plus" doctor --target .
scripts/ai-context.sh
```

## Choose the first gate

- If the decision, user, scope, null or BLOCK path, evidence need, or claim ceiling is unclear, run
  `$agent-plus-discovery-grill`. It maintains one
  `.planning/discovery/PROJECT-DISCOVERY.md` decision brief.
- If the decision is already contract-ready, draft the research contract directly.
- For publication prose, route an explicit detect, humanize, or de-slop request to `$editorial-pass`.
- A `READY_FOR_CONTRACT` discovery state still requires the owner to confirm the final synthesis.
  It does not accept a contract or authorize data, modeling, live work, or promotion.

## Check and upgrade Agent+

Use `$agent-plus-sync` for the guided audit, authorization, update, and verification workflow. The
commands below are the underlying deterministic interface.

Run these commands from the cloned Agent+ repository:

```sh
scripts/agent-plus status --target "/absolute/path/to/baseball-project"
scripts/agent-plus upgrade --target "/absolute/path/to/baseball-project"
# If an upgrade reports an interrupted transaction:
scripts/agent-plus recover --target "/absolute/path/to/baseball-project"
```

The installation manifest identifies files that Agent+ manages. An upgrade stops when one of those
files changed locally. Resolve that change through an upstream contribution or a deliberate local
fork. If a filesystem error interrupts an upgrade, Agent+ preserves one complete recovery snapshot
and durable transaction journal; use the single `recover` route to restore the prior managed state.
Agent+ never replaces project-owned memory, planning state, research records, data, or the
engineering boundary ledger.

Use `.agent-plus/PROJECT.md` for local terminology, commands, source restrictions, and authority.
Agent+ upgrades preserve this file.

## Use the profiles

Read `.agent-plus/PROFILE.md` after initialization. It adds only the gates relevant to the project type. The project owner still defines its research contract, source authorization, and claim ceiling.
