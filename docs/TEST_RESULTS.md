# Validation history

## 0.2.0 full-height area (2026-11-07)

Tested on the same vanilla Java 26.3 / Java 25.0.5 runtime, using the explicit `area_start` API in a headless server. No graphical client or Realm test.

- 48×48×384 fixture (884,736 positions) completed all 216 queued cubes.
- Verified all 13,824 retained grid positions and 13,824 off-grid air samples: zero failures, completion sentinel 1. Production also verifies all 4,032 removed positions within each cube during conversion.
- Retained diamond ore at Y -64, an X-axis oak log at Y 316, and a west-facing chest containing seven diamonds.
- A gold block immediately outside the selected area remained untouched.
- Paused at cube 116; a replacement start request was refused. Reload and clean stop/start retained the count and paused state. Resume completed the remaining work.
- Repeating the completed area skipped all cubes and preserved a newly placed off-grid gold block.
- An unloaded-area request paused with done=0, before conversion.
- Negative remainder arithmetic was checked in the actual scoreboard: -1 modulo 16 = 15, matching the player wrapper alignment calculation.
- Three Python tests pass: cube complement geometry, grid phase across negative origins, and queue coverage/order/uniqueness.

The player-only `area_here` wrapper loaded successfully but has not been exercised through a connected graphical player. The conversion backend was runtime-tested. Full natural-terrain physics and Realms throughput remain unverified.

## 0.1.0 single-cube validation

Date: 2026-11-07. Tested in a headless vanilla Java 26.3 dedicated server on Temurin Java 25.0.5. No graphical client or Realm was used.

Server download SHA-1: `33680f5f2ac32864d6d7cf5e56a705fdb3e05f4c` (Mojang version manifest).

## Passed

- Pack metadata and functions loaded in the actual 26.3 runtime without datapack parse errors.
- Python geometry checks: disjoint removal boxes cover exactly 4,032 positions and exclude all 64 retained positions; grid phase is consistent across positive and negative aligned origins.
- Runtime positive stone cube: all 4,096 positions checked against the expected result.
- Runtime negative-coordinate stone cube: all 4,096 positions checked against the expected result.
- Retained chest preserved east-facing state and seven diamonds.
- Natural terrain sample: every retained position compared with a pre-conversion clone; every removed position checked for air.
- A gold block placed off-grid after conversion survived a repeat request, datapack reload, and a full clean server stop/start.
- Misaligned, non-Overworld, and unloaded-region requests did not add ledger entries.
- Deliberately reducing the block-modification limit to 1 caused conversion verification to fail and record `failed`. After restoring the limit, a retry was refused; a sampled off-grid stone remained untouched.
- Ledger persisted three completed cubes and the deliberately failed cube after restart.

The runtime assertion counter reported zero failures. Completion was also checked via ledger entries and direct block checks, not merely the counter.

## Harness correction

An initial attempt ran before all requested chunks were loaded. Unloaded block checks can fail without incrementing the assertion counter, so that attempt was not considered a passing run. The suite was rerun after chunks loaded. The checked-in harness now includes loaded-area preconditions and a `#finished` completion sentinel to make this distinction explicit.

## Not established

Realms compatibility under load, multiplayer exploration, conversion throughput, later fluid/falling-block behavior, interrupted crash recovery, Nether/End progression, and whole-world generation remain untested. This build is for a local disposable-world demonstration only.

Authentication service discovery was unavailable in the test environment. The server still loaded and ran console-driven tests; this does not establish online client connectivity.
