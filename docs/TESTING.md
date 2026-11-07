# Try FlusGrid 0.1.0 locally

This is a manually activated, single-cube experiment, not a playable full-world generator. Use a disposable Java 26.3 Creative world with commands enabled. Do not upload this prototype to your active Realm.

## Install

1. Download `dist/FlusGrid-0.1.0-experimental.zip` from this repository (use the raw/download button).
2. Put the ZIP, without extracting it, in the test world's `datapacks` folder.
3. Open the world and run `/reload`.
4. Run `/datapack list enabled` and check that FlusGrid appears.

Nothing is converted automatically. There is no tick function, worldgen override, client mod, or resource pack.

## Visible stone-cube demonstration

In the disposable world, run these commands separately, waiting for the area to load after teleporting:

```mcfunction
/gamemode creative
/tp @s 8 110 24
/fill 0 96 0 15 111 15 minecraft:stone strict
/function flusgrid:convert {x:0,y:96,z:0}
```

The stone cube becomes 64 floating stones, spaced four blocks apart along each axis. The entire cube from `(0,96,0)` through `(15,111,15)` is affected. The other 4,032 positions become air. This is 98.4375% of positions removed, not an exact 99% rule.

For a natural terrain sample, fly near the location and call:

```mcfunction
/function flusgrid:convert {x:0,y:0,z:0}
```

That processes ONLY `(0,0,0)` through `(15,15,15)`. It does not clear the ground above it. Pick other explicit origins to inspect other cubes. Each coordinate must be an integer multiple of 16; Y must be between -64 and 304. Negative aligned origins work. Overworld only.

## Repeat protection and inspection

Place a block in a cleared position, then repeat the exact conversion command. It must refuse conversion and retain your new block. The same applies after `/reload` or reopening the world.

```mcfunction
/data get storage flusgrid:ledger
```

Entries are `started`, `complete`, or `failed`. Any existing entry blocks another conversion, including interrupted work. There is intentionally no retry/reset command. Restore the disposable world's backup after an interrupted or failed operation. Do not erase the ledger to continue playing on partially converted terrain.

## Limits

- Strict edits suppress immediate neighbor/shape updates. They do not permanently freeze water, lava, sand, gravel, leaves, vegetation, redstone, or scheduled ticks.
- No special structure, container, bedrock, portal, spawn, or progression exceptions. A retained chest survives in place; an off-grid chest and its contents are removed.
- Fresh cubes can contain player builds, which WILL be removed at off-grid positions. Repeat protection applies only to already recorded cubes.
- The public API validates origins. `internal/*` functions are implementation details and must not be invoked directly.
- Verification performs 4,032 block checks per cube. This is intentionally conservative for this small experiment, not a demonstrated scalable exploration architecture.
- No multiplayer, Realm, fluid stress, or complete survival playthrough tests yet.
- An abrupt server crash can lose unsaved world and storage data. The ledger is not a transaction journal or backup substitute.

## Rebuild and development tests

Python 3, standard library only:

```sh
python tools/build.py
python -m unittest discover -s tests -v
```

The build writes the unpacked pack to `datapack/` and its ZIP to `dist/`.

Optional destructive runtime tests: use a NEW disposable dedicated-server world with Java 26.3 and Java 25. Install the production ZIP, then generate the separate test pack:

```sh
python tests/make_runtime_tests.py /path/to/test-world/datapacks/flusgrid-tests
```

After the server has started, run `reload`, then `forceload add -16 -16 63 15`. Wait for the chunks to load before running `function flusgrid_test:run`. Check both `scoreboard players get #finished fg_test` (must be 1) and `scoreboard players get #fail fg_test` (must be 0), plus the three `complete` ledger entries. Unloaded block checks can fail as commands without incrementing a failure counter, so never use the counter alone as proof.

Run `function flusgrid_test:revisit` after reload and restart, and inspect `#fail` again. The test suite must not be rerun on an already-used test world: its fixture setup overwrites blocks while the conversion ledger intentionally prevents reprocessing.
