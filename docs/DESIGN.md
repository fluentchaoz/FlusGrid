# Design and validation

## Experience

Preserve the original terrain's spatial meaning: ore distribution, biome locations, and dimension identity. The objective is a sparse regular grid, not random SkyGrid blocks. Exact fidelity to RaysGrid is not established; do not invent its settings.

## Open decisions

- Final grid spacing and coordinate offsets (prototype uses spacing 4, offset 0). Keeping one position per n-by-n-by-n cube retains approximately 1/n^3 of eligible positions, not necessarily that fraction of actual terrain blocks. Four-block spacing retains 1/64 of positions; five retains 1/125. Neither is an approved default yet.
- Structure treatment: gridify, preserve selected progression blocks, or preserve entire structures.
- Fluids: retained sources can flow into cleared space. Waterlogged blocks also require testing.
- Falling blocks, unsupported vegetation, leaf decay, and block updates may alter the retained grid.
- Bedrock, Nether roof, spawn platform, portals, End entry and exit, and dragon fight behavior.
- Whether all three dimensions will share spacing and exceptions.

## Initial architecture and prototype

Version 0.1.0 validated a manually invoked single-cube converter. Version 0.2.0 adds a persistent 216-cube queue for a bounded 48x48 full-height area, one cube per tick, with pause/resume and reload pausing. Automatic exploration remains unimplemented. It would need a durable, dimension-aware region ledger, bounded work per tick, and a restart-safe processing state. A repeated clear-around-player loop is unsuitable: it can erase builds and duplicate work when players overlap.

Implemented first prototype: explicit administrator activation for one disposable test region, no automatic tick-driven terrain deletion on load. Align grid coordinates globally, including negative coordinates and chunk boundaries. Preserve retained blocks in place where possible so block state and block-entity data survive.

Investigate world-generation facilities before committing to post-processing. Do not assume datapacks provide a plugin-equivalent chunk generation callback or can filter every generation stage with one setting.

A completed-region ledger alone does not protect builds in queued or partially converted regions. The design must prevent entry/building during conversion or otherwise isolate preparation from play. Handle interruption deliberately rather than blindly restarting a partly converted region.

## Acceptance checks

1. Load the pack in an actual Java 26.3 runtime; inspect logs for syntax and registry errors.
2. Compare a converted region with untouched terrain from the same seed; verify retained coordinates, block states, and block-entity data.
3. Check grid continuity at positive and negative region boundaries.
4. Verify revisits, reloads, restarts, and overlapping players do not reconvert completed terrain.
5. Test interruption during conversion and recovery without deleting player work.
6. Check water, lava, waterlogging, sand, gravel, leaves, vegetation, containers, and structure progression.
7. Measure tick cost and exploration backlog; do not claim Realms suitability from static validation.
8. Run a real Realm trial after local checks, including players exploring in different directions.
9. Validate each dimension separately before claiming full survival progression.
10. Rehearse downloading and preserving the world. Terrain conversion must be disableable for archival import; any required worldgen definitions must be documented separately.

## Version reference

The official 26.3 release notes list datapack format 121.0. Verify against the target runtime when creating the pack; metadata alone does not prove command compatibility.

https://www.minecraft.net/en-us/article/minecraft-java-edition-26-3

## Completion standard

A downloadable ZIP, installation steps, exact tested game version, test results, and known limitations are required for a playable release. Documentation scaffolding is not a release.
