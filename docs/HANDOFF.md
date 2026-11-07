# Development handoff

Updated: 2026-11-07

## Scope

Fresh RaysGrid-inspired Java 26.3 world, vanilla datapack targeting Java Realms; archive in Flunkstar after the playthrough. No plugin/client-mod substitution without discussion.

## Current build: 0.2.0 experimental

Ryan successfully tested the 0.1.0 floating stone cube. He confirmed that the goal is to remove terrain between grid positions while retaining the actual original blocks. He requested the next full-height terrain test.

`/function flusgrid:area_here` selects the player's current chunk and eight neighbors (48x48), full Overworld height -64..319. Creative/Spectator caller required. Explicit aligned-minimum-corner API: `/function flusgrid:area_start {x:128,z:128}`. It queues 216 cubes, top down within each chunk, one cube per tick. No automatic exploration yet.

Controls: `flusgrid:status`, `flusgrid:pause`, `flusgrid:resume`. Only one job may run/be paused at a time. Unloaded next chunks pause instead of force-loading. On load/reload a running job becomes paused. Completed ledger entries are skipped. Started/failed entries pause and refuse retry. No cancel/reset command yet.

The persistent job is in `flusgrid:job`: state, pending list, done, total. Shared temporary coordinates are in `flusgrid:work`; scoreboard `flusgrid` holds scratch values. Single-cube public conversion is blocked while an area job runs or is paused. No asynchronous work occurs inside one cube. This is normal saved state, not a crash-atomic transaction.

`flusgrid:ledger` regions uses canonical integer x,y,z keys and started/complete/failed values. Each cube is 16^3 with experimental four-block spacing: 64 untouched grid positions, 124 strict fill commands, 4,032 cleared-position checks. Previously processed cubes are never deliberately re-cleared, even if physics or builds have changed their contents.

## Files

- `tools/build.py`, `tools/area.py`: standard-library Python generators.
- `datapack/`: generated runtime files.
- `dist/FlusGrid-0.2.0-experimental.zip`: current test download; 0.1.0 ZIP retained for history only.
- `docs/TESTING.md`: user upgrade and single-command instructions.
- `docs/TEST_RESULTS.md`: measured checks and limits.
- `tests/make_area_tests.py`: destructive full-height runtime fixtures for a new test world.

## Next

Observe Ryan's natural-jungle test. Investigate fluid flow, leaf decay, falling blocks, waterlogging, and scheduled ticks; strict fill does not permanently disable physics. Consider test-area boundaries and outside fluids flowing in. Then resolve progression exceptions, spacing, and preparation versus live exploration before trying Realms.

Do not describe this as whole-world generation, a complete survival pack, or tested Realms compatibility. No multiplayer stress or complete progression test exists. Keep documentation and this handoff current.
