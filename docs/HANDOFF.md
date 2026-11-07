# Development handoff

Updated: 2026-11-07

## Scope and user feedback

Ryan wants a fresh RaysGrid-inspired Java 26.3 world, ultimately playable on Java Realms and archived in Flunkstar afterward. Vanilla datapack, no client mod/server plugin substitution without discussion.

He successfully tested 0.1.0's stone grid and 0.2.0's actual full-height terrain grid. He proposed preparing terrain hundreds of blocks ahead to hide conversion. We agreed to bounded local pregeneration before Realms rather than promising live exploration performance. The next delivered milestone is a 512×512 preparation job.

## Current build: 0.3.0 experimental pregen

`/function flusgrid:pregen_here` selects 32×32 chunks, from the caller's chunk minimum minus 256 on both axes, full height -64..319. Caller must be a Creative/Spectator player in the Overworld. Explicit minimum-corner API: `/function flusgrid:pregen_start {x:4096,z:4096}`.

A compact cursor processes 24 vertical cubes per chunk, X-fast then Z rows. The job acquires at most one force-load ticket, waits for readiness, converts one 16-cube per tick, releases its ticket, and moves on. No enormous cube queue is materialized. One extra acquisition tick per chunk plus generation waits makes the normal-speed theoretical minimum about 21m20s. The pack does not modify game speed/rules.

`flusgrid:job`: kind=pregen, state, cursor, min/max chunk origins, done/total=24576, chunks/1024, percent, wait, reason, optional ticket{x,z,owned}. Existing force-load tickets are recognized and never deliberately removed. Only tickets added by FlusGrid are released; external code should not modify the same target ticket concurrently.

Controls remain status/pause/resume. Pause and load/reload release the owned ticket. Load marks an active job paused. Resume explicitly reacquires the current chunk and continues. Chunk readiness timeout is 1200 ticks. Started/failed cube entries pause and refuse conversion; no cancel/reset is offered. Do not delete ledger entries to retry partial work.

The 48×48 area command still exists and shares the same one-job guard. Older area jobs without kind remain compatible with the area tick path. The area path never acquires tickets. Single-cube conversion is blocked while any job is running/paused.

## Converter and persistence

`flusgrid:ledger` regions has canonical x,y,z keys and started/complete/failed values. Spacing 4 is experimental. Each 16-cube retains 64 positions, clears via 124 strict fill boxes, then checks 4032 removed positions. Retained blocks are not rewritten. Completed entries are skipped even if builds or later physics changed that cube.

Scoreboard `flusgrid` and `flusgrid:work` are scratch state. Job and ledger are normally saved, not crash-atomic transactions across all world files. Backups still matter.

## Files and validation

- `tools/build.py`, `tools/area.py`, `tools/pregen.py`: standard-library generators.
- `datapack/`: generated files; `dist/FlusGrid-0.3.0-experimental.zip`: current build. Keep only this ZIP installed; older ZIPs are historical downloads.
- `docs/PREGEN.md`: current player instructions; `docs/TESTING.md`: earlier area demonstration.
- `docs/TEST_RESULTS.md`: runtime results and limits.
- `tests/audit_pregen_save.py`: optional offline audit of all 24,576 ledger entries; needs nbtlib. 26.3 storage path is world/data/flusgrid/command_storage.dat.

Review the recorded test results before making claims. Headless runtime tests use a separate disposable vanilla 26.3 server with Java 25. Accelerated tick rate is for development testing only; it is not normal-speed performance or a Realm test. The player wrapper is parsed but not tested through a graphical connected player here.

## Next work

Inspect Ryan's prepared square and address fluid flow, leaf decay, falling blocks, scheduled ticks and boundary inflow. Strict editing is not permanent physics suppression. Then decide progression exceptions, spawning, borders/expansion and dimensions before attempting Realms survival.

Beyond the square, ordinary terrain remains. No automatic exploration extension or world border is installed. This is not a full survival pack or certified Realms compatibility. Preserve the saved ledger when importing, and pause before removing/disabling the pack so its ticket is released.
