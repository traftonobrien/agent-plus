# Control guarantees and repair coverage

Agent+ validates specific properties. No PASS certifies the entire system, a model, or a scientific claim.

| Guarantee | Enforcement | Falsifying regression |
| --- | --- | --- |
| Existing installation leaves survive collision | Initializer derives checks and copies from staged inventory | test_every_staged_leaf_collision_preserves_owner_content |
| Repeated closeout counts once | Anti-loop ledger records packet ID and content digest atomically | test_duplicate_conflicting_and_distinct_closeouts; test_concurrent_duplicate_block_records_count_once |
| R and analytical consumers cannot hide outside caller roots | Interface guard searches the supported source inventory | test_all_supported_analytical_consumers_outside_declared_roots_block |
| Required smoke evidence matches executed command, inputs, and output | Interface guard verifies fixed process-produced evidence | test_smoke_writer_binds_command_inputs_and_output |
| Malformed consumer fields return BLOCK | Type checks precede enum membership | test_bad_consumer_enums_and_encoding_are_typed |
| Startup has its binding procedures | Context validates required regular UTF-8 files before output | test_startup_requires_all_procedures_and_readiness_runs_hook |
| CURRENT compares actual source content | Lifecycle status compares managed hashes as well as labels | test_same_version_source_difference_is_not_current |
| Honest terminal failure can close at the limit | Chain closeout separates terminal recording from continuation | test_terminal_block_at_limit_is_valid_but_continuation_is_not |
| Public text checks include Python, JSON, YAML, and analytical files | Git publication inventory scan with redacted findings | test_public_scanner_checks_text_formats_without_echoing_secrets |

## Malformed JSON resource limits

JSON loaders return their existing typed failure when parsing exceeds recursion or integer limits.
This includes interface receipts, chain capsules, lifecycle manifests and registry, standalone doctor
routes, release configuration, and outcome records. Ordinary schema validation and successful input
behavior are unchanged. `tests/test_json_resource_failures.py` covers deep arrays, deep objects,
integer limits, below-limit documents, public CLI results, and bootstrap copies.
The lifecycle status command retains its existing kernel-lease file. Parser failure does not mutate
control or artifact bytes. This repair does not change locking or recovery semantics.

## Installation and readiness

Normal `doctor --target PROJECT` returns `AGENT_PLUS_STRUCTURE_PASS`. It does not execute an optional
project startup hook. `doctor --target PROJECT --readiness` explicitly runs the project context check.
Use readiness only when executing that project's hook is authorized. The legacy adoption route
retains its mandatory startup gate. Its PASS includes that legacy gate, not scientific readiness.
The optional consumer CI remains structural. Canonical CI runs the full public validator.

The normal initializer derives its shared script and test leaf inventory from staged files.
The manifest manager remains the managed-set authority. Tests exercise every managed leaf collision.
Keep historical managed-set identities for compatibility. New managed files require lifecycle coverage.

## Consumer closure and smoke evidence

Search roots are hints that must exist, not exclusions from coverage. The guard scans supported text
files across the repository. It excludes fixed generated or state directories: `.git`, `.agent-plus`,
`.planning`, `outputs`, caches, dependency directories, and virtual environments. Keep runtime source
outside these directories. Symlinked source directories fail closed. An explicit reviewed adapter is
required for unsupported binary or generated runtime consumers. Lexical discovery cannot prove dynamic
symbol resolution. Independent review still owns that limit.

The supported suffixes include R, R Markdown, Quarto, SQL, YAML, and notebooks, plus the existing
Python, JavaScript, shell, Markdown, and JSON formats. Exclusions are fixed in the guard, not a caller
field. Consumer acceptance check strings describe checks. They are not execution receipts.

A required smoke uses `.agent-plus/interface-smoke.json` and `.agent-plus/interface-smoke.log`.
Run its exact command explicitly. The tool never executes a command merely because it is in receipt data:

```sh
python3 scripts/interface_consumer_guard.py --root . --receipt RECEIPT.json --record-smoke -- python3 tests/operational_smoke.py
```

The receipt's command must equal the shell-quoted explicit argument list. Evidence binds the command,
zero exit status, current definition and consumer hashes, and captured output hash. Changed inputs,
missing evidence, or altered output block validation. Evidence is process-produced local evidence,
not a signature against an adversary with write access to the repository. A static public example
uses `NOT_REQUIRED` rather than pretending that an operational smoke occurred.

## Failure events and routing

An optional `recorded_blocks` map extends v2 failure states. Old ledgers remain readable without
rewriting historical counts. New closeouts atomically store their packet ID and canonical content digest.
A repeated identical packet returns `BLOCK_ALREADY_RECORDED` without writing. A reused ID with changed
content blocks. Historical events that predate this map cannot be retroactively deduplicated.

The capsule validates order and terminal routing only. It does not establish evidence quality,
reviewer independence, or authority. Promotion also needs the ledger-bound review, deterministic
acceptance evidence, and the human authority required by the task. Never substitute capsule PASS for
those checks. A terminal BLOCK or NULL does not authorize another attempt.

Keep the closed outcome catalog. `agent-plus-control-plane-capability` covers generic control work.
Research-specific IDs remain compatibility entries. A new product or scouting outcome requires a
named consumer and explicit authority review. Do not widen scientific claims through free text.

## Public inventory

The scanner uses tracked and nonignored Git files, including new files. It scans all UTF-8 text,
not just Markdown and shell. Findings identify the file and redact matched content. Known image and
PDF types remain outside textual scanning and require artifact review. Unknown binary formats block.
The scanner is a pattern check, not proof that no sensitive information exists. Review the exact
release inventory before publication. CI installation does not itself publish a release.
