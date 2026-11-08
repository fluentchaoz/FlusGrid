# Validation history

## 0.5.0 Nether and End isolation (2026-11-08)

Tested on actual vanilla Java 26.3, Zulu Java 25.0.5.0.3, seed 887314, in a disposable headless server. Final pack loaded without function/predicate parsing errors. Initial development caught and fixed the 26.3 predicate `type` field requirement.

- Same-coordinate fixtures in all three dimensions: all 4,096 block positions per cube checked. Nether and End became their respective grids; the completed Overworld emerald cube remained wholly untouched. Separate ledger entries verified. Completion sentinel 1, failures 0. Read-only recheck after the bulk jobs also passed.
- End central gold sentinel survived direct conversion. Predicate boundaries -256 and 255 included, -257 and 256 excluded.
- Both 2048 entrypoints created correct 262,144-cube / 16,384-chunk jobs. Nether processed 938 cubes (58 whole chunks plus 10 cubes); End processed 1,376 cubes (86 chunks) before explicit pause. Reload preserved cursors/counts, paused both jobs and released owned tickets. Resume advanced both; manual pause released tickets again. Full 2048 runs were NOT performed.
- After pausing, only in the disposable test save, those partial 2048 jobs were marked complete to permit fresh 512 jobs. Their saved completed cubes remained and were skipped where overlapping.
- **Complete 512×512 jobs finished in both Nether and outer End** at X/Z 4096..4607, Y 0..255. Each reached 1,024 chunks, 16,384 cubes, 100%, state complete, with no owned ticket. After `save-all flush`, offline NBT audits checked every expected cube key in each dimension: all complete. Both workers ran simultaneously, exercising shared synchronous scoreboard scratch.
- Pre-existing force-load tickets remained: one Nether fixture ticket, two End fixture tickets. No job-owned tickets remained after completion.
- Central End pregen processed 20 protected cubes without acquiring any new ticket. A separately injected final cursor/count tested the last protected-cube completion branch; this was NOT a full central-square run.
- Twelve Python unit tests pass. ZIP contents match generated files exactly.

Bulk testing used target tick rate 200 and produced overload warnings; this is not a normal-speed benchmark. The pack never changes tick speed. No graphical player-wrapper test, full 2048 Nether/End completion, Realm test, dragon fight or survival-progression validation is claimed. The Overworld fixture demonstrates dimension isolation, not a complete real-world upgrade simulation. Ryan separately reports his 0.4.0 Overworld 2048 preparation completed in about six hours.

## 0.4.0 leaves and 2048 entrypoint (2026-11-07)

Tested against actual vanilla Java 26.3 / Java 25. The leaf list was extracted from the server's shipped block/leaves tag, not guessed.

- All 14 vanilla species converted with persistent=true and preserved species/distance/waterlogging in the immediate assertion fixture. A separate waterlogged oak at distance 3 also retained those values. Fixture completion sentinel 1, failures 0.
- After 100 stepped ticks with random_tick_speed=4096, all 14 dry persistent species survived and the untreated distance-7 oak control disappeared. Post-tick assertion failures 0. The test restored random_tick_speed=3; the datapack never changes it.
- Explicit 2048 start produced 16,384 chunks / 393,216 cubes and correct bounds (minimum 4096, maximum chunk origin 6128). 154 natural chunks / 3,696 cubes actually processed, including crossing the 128-chunk row boundary, before manual pause. Its owned ticket was released; three test-fixture force-load tickets remained untouched.
- Synthetic final-cube test: after explicitly injecting the final cursor/counts into the disposable test job, the worker completed the actual last cube, reached 16,384/393,216 and released its ticket. This tests the completion branch only, NOT full-area completion.
- Revisited an old completed cube: a newly placed nonpersistent grid leaf became persistent, while a newly placed off-grid gold block survived.
- Seven Python tests pass, including generated 2048 bounds/totals and all 196 leaf-state mappings (14 species × 7 distances × 2 waterlogged states).

The full 2048 job has NOT been run to completion. No end-to-end time, late-run memory profile, graphical-player wrapper test or Realms validation is claimed. Other physics are still active. Leaves are protected from natural decay, not fire/explosions/player breaking.

## 0.3.0 bounded pre-generation (2026-11-07)

**Full 512×512 run completed on vanilla Java 26.3 / Java 25.0.5.** Seed 887314, explicit minimum corner X/Z 4096, no players near the target. Bounds X/Z 4096..4607, Y -64..319. These are 100,663,296 potential block positions, with 1,572,864 grid positions retained where blocks originally existed.

- Actual generated terrain processed: 1,024 chunks, 24,576 cubes; job state complete, percent 100.
- After a clean stop, `tests/audit_pregen_save.py` independently checked all 24,576 expected keys in saved NBT. Every key was complete; no owned ticket remained.
- At sampled points while running, force-load query showed exactly the one pre-existing test ticket plus one FlusGrid-owned ticket. Pause/reload/completion left only the pre-existing ticket.
- Full restart with work in progress preserved done=367 and the cursor, set the job to paused, and removed the owned ticket. Resume completed the remainder.
- Retained test chest at (4096,304,4096) remained west-facing with seven diamonds after completion.
- Five Python tests pass, covering cube geometry, negative alignment, 48×48 queue coverage, 512×512 cursor contract and ownership-scoped release generation.
- No datapack/function parsing errors on the final build.

Initial conversion and pause/reload/restart checks ran at normal tick speed. The bulk completion run used `/tick rate 200` to accelerate developer testing, then restored 20. The pack itself never alters tick rate. This is not a normal-speed benchmark or a Realm throughput claim. An overload warning occurred during the accelerated test.

The saved-ledger audit establishes completed processing, not permanent freedom from subsequent fluid flow, falling blocks or decay. Player-only `pregen_here` has parsed in the server but was not exercised by a connected graphical player; its explicit coordinate backend was tested. Realms, multiplayer stress, timeout induction, abrupt process-crash recovery and full survival progression remain untested.

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
