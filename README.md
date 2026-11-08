# FlusGrid

A RaysGrid-inspired Minecraft Java survival project: keep naturally generated blocks at regular grid positions, preserving their relationship to the original terrain rather than randomizing block types.

## Confirmed target

- Minecraft Java Edition 26.3.
- A fresh, standalone world for Ryan and friends.
- Prefer a vanilla datapack playable on Java Realms, without client mods or server plugins.
- After the playthrough, download and import the world into Flunkstar for preservation.
- Independent implementation; not an official Rays Works release.

## Status

**0.6.0 experimental one-map setup:** `/function flusgrid:setup` prepares Overworld, Nether, then a larger End. It places the empty End portal at (0,-32,0), preserves pylon tops and the central podium, and grids the rest of the End island. Automatic 512-wide expansion strips and a finished-area travel guard support continued exploration.

**This is not an unlimited-flight or production-Realms guarantee.** Fast players can reach the guard before preparation finishes. Full-size end-to-end setup, Realm load and survival/dragon progression still require a playtest. Existing leaf persistence remains; other block physics are not frozen.

- [Download 0.6.0](https://github.com/fluentchaoz/FlusGrid/raw/refs/heads/main/dist/FlusGrid-0.6.0-experimental.zip)
- [One-map setup, exact commands and limits](docs/REALMS_SETUP.md)
- [Test results](docs/TEST_RESULTS.md)
- [Development handoff](docs/HANDOFF.md)
- [Earlier standalone dimension commands (0.5 history)](docs/DIMENSIONS.md)

## Portal-return experiment

A separate, opt-in test pack checks departure-point return after a dimension change. It does not grid terrain or implement the proposed 10k/on-demand region scheduler. [Download the test ZIP](https://github.com/fluentchaoz/FlusGrid/raw/refs/heads/main/dist/FlusGrid-portal-return-test-0.1.zip) · [Test instructions](docs/PORTAL_RETURN_TEST.md).

## Intended play workflow

1. Develop and validate locally on Java 26.3.
2. Prepare a fresh world with the validated datapack.
3. Upload to Java Realms and test with multiple players before starting the playthrough.
4. Download the completed world for eventual Flunkstar import.

If live conversion cannot meet correctness and performance requirements, evaluate locally preconverting a bounded world before upload. This fallback requires explicit world boundaries; it must not silently expose ordinary terrain beyond the prepared area.
