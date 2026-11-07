# FlusGrid

A RaysGrid-inspired Minecraft Java survival project: keep naturally generated blocks at regular grid positions, preserving their relationship to the original terrain rather than randomizing block types.

## Confirmed target

- Minecraft Java Edition 26.3.
- A fresh, standalone world for Ryan and friends.
- Prefer a vanilla datapack playable on Java Realms, without client mods or server plugins.
- After the playthrough, download and import the world into Flunkstar for preservation.
- Independent implementation; not an official Rays Works release.

## Status

**0.1.0 experimental prototype:** a manually invoked Overworld converter for one aligned 16×16×16 cube, with four-block grid spacing. It retains existing blocks at grid positions, uses strict removal, verifies cleared positions, and records processed cubes to refuse retries.

This is not a full-world generator or a Realms-ready survival release. Grid spacing is an experimental choice, not an established RaysGrid specification.

- [Download the experimental datapack](https://github.com/fluentchaoz/FlusGrid/raw/refs/heads/main/dist/FlusGrid-0.1.0-experimental.zip)
- [Installation and local demonstration](docs/TESTING.md)
- [Test results](docs/TEST_RESULTS.md)
- [Design plan](docs/DESIGN.md)
- [Development handoff](docs/HANDOFF.md)

## Intended play workflow

1. Develop and validate locally on Java 26.3.
2. Prepare a fresh world with the validated datapack.
3. Upload to Java Realms and test with multiple players before starting the playthrough.
4. Download the completed world for eventual Flunkstar import.

If live conversion cannot meet correctness and performance requirements, evaluate locally preconverting a bounded world before upload. This fallback requires explicit world boundaries; it must not silently expose ordinary terrain beyond the prepared area.
