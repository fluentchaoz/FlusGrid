# Development handoff

Updated: 2026-11-07

## Confirmed scope

FlusGrid is Ryan's independent RaysGrid-inspired project for Java 26.3. Start with a fresh world, aim for a vanilla datapack on Java Realms, and import into Flunkstar after the playthrough. Do not silently substitute a server plugin or client mod.

## Current implementation

0.1.0 experimental prototype is in `datapack/`, with a distributable ZIP in `dist/`. `tools/build.py` generates both using Python's standard library.

Public command: `/function flusgrid:convert {x:0,y:64,z:0}`. It converts exactly one aligned 16-cube in the Overworld. Origins must be multiples of 16, Y -64..304. Experimental spacing is 4 (64 retained positions / 4096). Off-grid positions are cleared with strict fills; retained blocks are not rewritten. There are 124 disjoint fill boxes, then 4,032 cleared-position checks.

Storage `flusgrid:ledger` has a `regions` compound keyed by canonical integer origins. Any existing entry blocks reprocessing. States: started, complete, failed. Reload never clears this storage. Interrupted or failed cubes have no automatic retry path. There is no tick function, automatic exploration, worldgen override, or dimension-wide conversion.

`flusgrid` scoreboard and `flusgrid:work` storage are scratch state. `internal/*` functions must not be called directly. Runtime commands execute synchronously; this is not a scalable queue yet.

## Validation

Actual vanilla 26.3 server, Java 25.0.5: cube geometry, negative origins, retained chest contents/state, natural sample comparisons, repeat protection, reload/restart persistence, and deliberate failed-conversion lock tested. See `docs/TEST_RESULTS.md` for limits and harness caveat. No Realms, graphical, multiplayer, physics stress, or complete survival tests.

## Next milestone

1. Let Ryan inspect the visible single-cube demonstration in `docs/TESTING.md`.
2. Test retained fluids, falling blocks, leaf decay, waterlogging, and existing scheduled ticks. Strict fill only suppresses immediate updates.
3. Decide spacing and structure/progression exceptions before scaling up.
4. Design and measure a bounded preparation queue, with protection against playing/building in unprepared regions. The current 4,032-check verifier per cube is deliberately conservative, not proven suitable for exploration.
5. Compare live conversion against local preconversion of a bounded world. Realms remains the target, not a verified claim.

Do not call this a playable full-world release. Preserve the ledger when importing or disabling the converter. It is not crash-atomic with world saves; backups remain necessary.
