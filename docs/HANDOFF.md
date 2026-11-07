# Development handoff

Updated: 2026-11-07

## User decisions

Ryan requested a RaysGrid-style project named FlusGrid for Minecraft Java 26.3. It will be a fresh world, preferably hosted on Java Realms using a datapack. Import into Flunkstar happens only after the playthrough. Do not switch the implementation to Paper/Purpur plugins or require client mods without discussing that change.

## Repository state

Documentation-only initialization. README.md and docs/DESIGN.md capture scope, unknowns, candidate implementation, and acceptance checks. No Minecraft runtime tests have been performed. No executable pack exists.

## Next work

1. Inspect current vanilla 26.3 datapack/worldgen capabilities and obtain a matching test runtime where available.
2. Choose the smallest viable conversion experiment; keep activation manual and bounded.
3. Implement pack scaffolding and a single-region grid conversion, with persistent completion tracking and explicit recovery behavior.
4. Test actual retained terrain, physics, region boundaries, and reload behavior before adding automatic processing.
5. Present evidence and a local test build. Record any inability to run Minecraft honestly.

Grid spacing, structure exceptions, fluid handling, and dimension rules are still unresolved. Prototype choices may be made as clearly documented experiments; do not turn them into claimed user requirements.

## Continuity

Read README.md, docs/DESIGN.md, and this file before continuing. Keep this handoff current with implemented features, actual test results, unresolved defects, and the next concrete task. Preserve existing user work and never describe untested compatibility as confirmed.
