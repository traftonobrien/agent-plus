# Release-candidate verification

Agent+ uses one closed command to verify the exact public release candidate recorded in the
repository:

```sh
python3 scripts/verify_release_candidate.py
```

Run it from the canonical repository root. The command accepts no arguments. Its fixed
configuration is `.agent-plus/release-candidate.json`, and that configuration names the current
version, proposed version, release base commit, and exact candidate manifest. Changing any of
those values is a new release-candidate decision and requires the normal review boundary.

## What the command proves

The verifier fails closed unless all of these checks pass:

- the base, stage-zero index, and public worktree yield exactly the sorted candidate manifest;
- `HEAD`, live `VERSION`, and the release configuration agree;
- a detached Git index contains the raw base files and exactly the authorized changes;
- the temporary candidate uses the proposed version without editing live `VERSION`;
- strict mypy, Ruff, and the complete public-package validator pass in the exported candidate;
- candidate bytes, executable modes, and Git state remain unchanged during validation;
- source Git bytes, modes, and modification times remain unchanged;
- non-output source worktree bytes, modes, and file timestamps remain unchanged, including on failure.

Source Git access is limited to `ls-tree`, raw `cat-file --batch`, and `ls-files` inventory reads.
The verifier captures its source baseline before those commands. It disables optional locks, lazy
object fetching, replacement refs, inherited Git routing, and global or system Git configuration.
It does not run source `status`, `add`, `checkout-index`, or `write-tree` commands.

The verifier creates a detached repository in the system temporary namespace. It ignores inherited
temporary-root settings. It copies no source Git configuration, index, hardlinks, or alternates.
Raw blobs enter the detached object store through `hash-object --no-filters` and literal index
records. Clean, smudge, and process filters do not participate. Existing alternate objects can have
their timestamps refreshed by Git writers, so alternate stores cannot satisfy this boundary.

The verifier requires a POSIX host and a regular local SHA-1 repository with regular stage-zero files. Linked
worktrees, symlinks, nonregular files, gitlinks, missing files, and unresolved index stages block.
The source index remains part of exact scope. A staged-only change cannot disappear because the
worktree happens to match the base. File reads reject symlinked parent components.

The static gates use `mypy==2.3.1` and `ruff==0.16.5`. Validation children receive a fresh environment,
isolated home and cache directories, and no inherited shell, Python, loader, or Git overrides.
Git comes from the system executable path. Tool lookup uses fixed user and system installation
directories, not the caller's executable path. The installed executables remain trusted inputs.
This is process routing, not an operating-system sandbox against malicious validation code.

## Receipt and authority

A run first atomically replaces `outputs/release-candidate/receipt.json` with `RUNNING` and a new
run identity. It finishes with `PASS` or `BLOCK`. A failed or interrupted run cannot leave the old
success receipt as its current evidence. An unavailable receipt destination blocks before Git runs.
The latest command result takes precedence if the receipt itself cannot be written.

A PASS receipt records the exact manifest digest, raw candidate identity, Git tree, pinned toolchain,
gate list, and before-and-after source identities. A BLOCK records its failure code and bounded
command diagnostics. Diagnostics contain exit status and output hashes, not private command text.
`outputs/` is the sole permitted source-local write area and is excluded from the public candidate.

A `PASS` means the configured candidate passed the engineering preflight. It does not authorize a
commit, tag, release, consumer update, data access, or scientific claim. Those remain separate
owner decisions. A `BLOCK` consumes the bounded verification attempt; repair or retry requires a
new authorized task.
