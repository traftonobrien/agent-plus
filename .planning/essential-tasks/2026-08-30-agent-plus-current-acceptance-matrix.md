# Agent+ current acceptance matrix

Date: 2026-08-30

Outcome: `PASS — DETACHED ENGINEERING PREFLIGHT AND INDEPENDENT REVIEW 003`.

This is engineering acceptance, not publication authority. The real source remains at VERSION
`0.3.0` and HEAD `ea147c0e2b2dac481238f96c37b56a31fe65033b`. Only the detached candidate
uses `0.4.0`. Publication, consumer synchronization, data access, and scientific decisions remain
separate owner boundaries.

## Current integrated evidence

- Exact candidate manifest: 81 paths, SHA-256
  `ed23a9aa8cbe52fd4924df675f056f90e970cbcfe5a4caac956b23061c507ddd`.
- Evaluator and independent reviewer each passed the closed preflight and matched candidate tree
  `af26236a8217aae7c0c3212ca47bf02fe1adb982` before administrative closeout.
- Complete public suite: 196 tests, including 32 focused verifier tests. Do not add these counts.
- Independent review: 26/26 attacks, 17/17 coverage areas, and 50/50 additional probes PASS.
- Current manager typing, helper rejection, lifecycle tests, and historical v1 fixture correction
  are covered by review 003, rather than inferred from older lifecycle acceptance.
- Strict mypy, Ruff, canonical/bootstrap bindings, privacy, links, whitespace, source integrity,
  detached integrity, exact public scope, and interface-consumer closure PASS.
- Evaluator receipt:
  `sha256:0a7061fe7e4b54ab13a50c25fa44d104718b59d31646d94bcd1a7e8f994deb1b`.
- Reviewer receipt:
  `sha256:4a84abfc6335bb68d37e938753b98ffd70eacbeedaee01943eae92996b45a71c`.
- Completed review packet:
  `.agent-plus/agent-plus-0-4-0-release-preflight-reset-review-003.json`.
- Review closeout:
  `sha256:bdb2fdeff215ba00c450f6acf3a0f8b472c8392d4de8f88d31a26baf3990d8a4`.
- Independent report SHA-256:
  `2c254f1783d3ff556e19e8c8cd54c0b5adb950c2be5dd1d65bb16edee2bb4f94`.

The reviewer permits only final review/state text and planned-to-complete packet changes within
the existing manifest, followed by one success-only final candidate refresh. Implementation,
configuration, tests, and manifest remain unchanged. The final candidate tree is intentionally
not embedded in these public records: doing so would change the tree again. A matching current
PASS in `outputs/release-candidate/receipt.json` is required before the owner publication decision.
The preserved evaluator and reviewer receipts identify the earlier, independently reviewed tree.

## Historical accepted baselines, rebound against the current ledger

Current normalized ledger SHA-256:
`a5b50f6a20ea27b43936ba7f1b1fedd7ef25bbaf7d9c3b7c0345d39f345d5efc`.

| Accepted boundary | Packet SHA-256 | Current administrative closeout receipt |
| --- | --- | --- |
| Active-chain routing and cost isolation | `e8b787f6dd993fdbeaa19e9fa00187fd09a45a1efaec30f7daf3cbb101923b4c` | `sha256:85ee38161ae830a11f23d04154956aba65a39d4ac53605f137384f08f34806aa` |
| Active-chain lifecycle delivery | `2b617e065ee81b980eb7960d8d70734e1123469a179b09a18827e55557c3935c` | `sha256:49f0208ddaeb6e46fe411c409abd94d2384f8d899323889657d24e4793a49aeb` |
| Unreleased policy refinement bundle | `0c112021bcf0c961f1febbe4f256c027c7b7d2bd04bffa99069f5219ee49e561` | `sha256:4bf25b14cb39c0dddb9d43a91c9e7e9ea28ead3921460bf5ace67b2992350e16` |

These rebindings validate historical packets against the current ledger; they do not certify
current file bytes. Later manager, lifecycle-test, legacy-fixture, README, and ledger changes were
explicitly assessed or bound in review 003. Ten policy content files still match their historical
review; the ledger changed. Historical receipts remain evidence for their original ledger states.

## Historical BLOCKs remain visible

The static-typing review completed its 8 attacks and 7 coverage areas but could not start the
required simulated-version validator because the archive failed. Its terminal BLOCK remains:
`sha256:ab87a2b1d035f1337a2686bffc9b3bf297386d8e7407912198327e4463a287e7`.
The recorded block event remains:
`sha256:d704c9223ebc44444dac3a39ce49dd0ab5cc33a349ad5a37846744d7a359e2fa`.

Attempt 002 subsequently blocked on object-store metadata mutation. The timestamp scan did not
prove new objects or a concurrent writer. Independent synthetic reproduction showed that existing
alternate objects can have timestamps refreshed without changed names or content. Attempt 003
removed the alternate relationship; it did not reinterpret attempt 002 as success.

The ledger retains `block_count=2`, `architecture_reset_required=true`, and the explicit
`attempt-03` authorization. Successful reset evidence does not erase historical failures or
authorize another local repair.

## Limits and next action

- No live version edit, real Git staging/object write, commit, push, tag, release, consumer
  synchronization, private project mutation, real data access, or scientific result is implied.
- The verifier supports regular local SHA-1 repositories on POSIX, not every Git layout.
- Installed executables and validation code remain trusted. Routing is not an OS sandbox.
- A final refresh failure stops the chain without retry.
- Local outputs, capsule, registry, lock, and editor/macOS metadata remain outside public scope.
- The separate public research coverage gate remains BLOCK.

Next action: inspect the final matching receipt and owner packet, then obtain one exact publication
decision. Consumer adoption or synchronization requires another project-owned decision.

Restart command:

```sh
./scripts/ai-context.sh
```
