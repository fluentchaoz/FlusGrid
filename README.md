# FlusGrid

A RaysGrid-inspired Minecraft Java survival project: keep naturally generated blocks at regular grid positions, preserving their relationship to the original terrain rather than randomizing block types.

## Confirmed target

- Minecraft Java Edition 26.3.
- A fresh, standalone world for Ryan and friends.
- Prefer a vanilla datapack playable on Java Realms, without client mods or server plugins.
- After the playthrough, download and import the world into Flunkstar for preservation.
- Independent implementation; not an official Rays Works release.

## Status

**0.3.0 experimental pre-generation:** `/function flusgrid:pregen_here` prepares a 512×512-block square through the full Overworld height. It generates distant chunks, converts one 16-cube per tick, tracks progress, and releases its temporary force-load ticket after each chunk. Pause, resume and reload/restart handling are included.

This is bounded local preparation, not infinite automatic exploration or a Realms-ready survival release. Physics and progression work remain.

- [Download the experimental datapack](https://github.com/fluentchaoz/FlusGrid/raw/refs/heads/main/dist/FlusGrid-0.3.0-experimental.zip)
- [Install and prepare 512×512](docs/PREGEN.md)
- [Earlier 48×48 test](docs/TESTING.md)
- [Test results](docs/TEST_RESULTS.md)
- [Design plan](docs/DESIGN.md)
- [Development handoff](docs/HANDOFF.md)

## Intended play workflow

1. Develop and validate locally on Java 26.3.
2. Prepare a fresh world with the validated datapack.
3. Upload to Java Realms and test with multiple players before starting the playthrough.
4. Download the completed world for eventual Flunkstar import.

If live conversion cannot meet correctness and performance requirements, evaluate locally preconverting a bounded world before upload. This fallback requires explicit world boundaries; it must not silently expose ordinary terrain beyond the prepared area.
