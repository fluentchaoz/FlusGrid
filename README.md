# FlusGrid

A RaysGrid-inspired Minecraft Java survival project: keep naturally generated blocks at regular grid positions, preserving their relationship to the original terrain rather than randomizing block types.

## Confirmed target

- Minecraft Java Edition 26.3.
- A fresh, standalone world for Ryan and friends.
- Prefer a vanilla datapack playable on Java Realms, without client mods or server plugins.
- After the playthrough, download and import the world into Flunkstar for preservation.
- Independent implementation; not an official Rays Works release.

## Status

**0.5.0 experimental preparation:** separate Overworld, Nether and End jobs, with 512×512 and 2048×2048 options. Existing Overworld progress is preserved. The End's central 512×512 dragon arena is excluded from conversion by default. Retained vanilla leaves remain persistent.

Ryan completed his 2048×2048 Overworld on 0.4.0. Other block physics, survival progression and Realms validation remain unfinished. See test results for the exact developer validation scope.

- [Download the experimental datapack](https://github.com/fluentchaoz/FlusGrid/raw/refs/heads/main/dist/FlusGrid-0.5.0-experimental.zip)
- [Upgrade and prepare Nether / End](docs/DIMENSIONS.md)
- [Install and prepare 2,048×2,048](docs/PREP_2048.md)
- [Earlier 512×512 workflow](docs/PREGEN.md)
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
