# FlusGrid

A RaysGrid-inspired Minecraft Java survival project: keep naturally generated blocks at regular grid positions, preserving their relationship to the original terrain rather than randomizing block types.

## Confirmed target

- Minecraft Java Edition 26.3.
- A fresh, standalone world for Ryan and friends.
- Prefer a vanilla datapack playable on Java Realms, without client mods or server plugins.
- After the playthrough, download and import the world into Flunkstar for preservation.
- Independent implementation; not an official Rays Works release.

## Status

Project initialized. No playable datapack or terrain converter exists yet. Realms performance and exact generation behavior remain unverified. Do not interpret the target as a compatibility guarantee.

## First milestone

Build and test a small, manually activated Overworld conversion prototype in a disposable local world. It must retain grid-position blocks, record completed regions, and avoid reprocessing player builds. Measure conversion cost before attempting automatic exploration or Realms deployment.

See [design and test plan](docs/DESIGN.md) and [development handoff](docs/HANDOFF.md).

## Intended play workflow

1. Develop and validate locally on Java 26.3.
2. Prepare a fresh world with the validated datapack.
3. Upload to Java Realms and test with multiple players before starting the playthrough.
4. Download the completed world for eventual Flunkstar import.

If live conversion cannot meet correctness and performance requirements, evaluate locally preconverting a bounded world before upload. This fallback requires explicit world boundaries; it must not silently expose ordinary terrain beyond the prepared area.
