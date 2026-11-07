# FlusGrid 0.2.0: full-height terrain test

Use your disposable Java 26.3 Creative test world. This build converts a real 48×48-block area, from Y -64 through 319. It is still a bounded experiment, not automatic world generation or a Realms release.

## Upgrade and run

1. Exit the test world.
2. Remove `FlusGrid-0.1.0-experimental.zip` from its `datapacks` folder. Install `FlusGrid-0.2.0-experimental.zip` instead. Do not install both versions.
3. Reopen the world. Run `/reload` if necessary.
4. Use Creative mode, fly above the part of the jungle you want to test, and wait for nearby terrain to load.
5. Run:

```mcfunction
/function flusgrid:area_here
```

Stay nearby while it works. It processes the chunk you are in plus its eight neighboring chunks, covering the full Overworld height. A completion message appears when all 216 small cubes have been handled. Expect roughly 11 seconds of conversion at 20 ticks per second, potentially longer with lag or pauses.

The converter removes off-grid blocks and leaves grid-position blocks as they were: dirt, ore, logs, leaves, containers, and so on. Air remains air. Spacing is four blocks along each axis. Surrounding terrain remains ordinary terrain, so expect a sharp boundary around the test area.

Previously recorded cubes are skipped. Your earlier floating stone test will therefore remain if it falls inside this area; it cannot be reconstructed into original terrain. Use a fresh location if you want only natural blocks.

## Controls

```mcfunction
/function flusgrid:status
/function flusgrid:pause
/function flusgrid:resume
```

Status shows the state, completed/skipped cube count, and next cube origin. Only one job can exist at a time. A second start request cannot replace a running or paused job.

If the next chunk is unloaded, the job pauses before changing it. Move closer, allow chunks to load, and resume. The pack does not force-load chunks. Reloading or restarting also pauses an active job, requiring an explicit resume.

If a cube is marked `started` or `failed`, the job will not retry its destructive work. Restore the disposable-world backup rather than deleting ledger entries. There is no reset or abandon command in this version.

## Important limits

- New, unprocessed cubes can contain your builds; off-grid blocks there WILL be removed. Only already-completed cubes are skipped.
- Keep everyone out of Survival mode during preparation. `area_here` requires its caller to be Creative or Spectator, but does not change other players' modes or protect them from falling.
- Strict edits suppress immediate neighbor/shape updates; they do not permanently freeze water, lava, sand, gravel, leaves, plants, redstone, or existing scheduled ticks. Waterfalls, falling blocks, and decay remain part of the next physics investigation.
- No structure, bedrock, portal, spawn, or progression exceptions. An off-grid chest and its contents are removed.
- Overworld only. No automatic conversion while exploring, multiplayer stress validation, or Realm testing yet.
- The ledger and job storage persist normally, but are not an atomic crash journal or a replacement for backups.

## Explicit development API

```mcfunction
/function flusgrid:area_start {x:128,z:128}
```

X/Z are the minimum corner of the 48×48 area, both multiples of 16. `area_here` instead computes that corner from your current chunk, minus one chunk on each axis. No relative coordinates in the explicit API. Single-cube `/function flusgrid:convert {x:0,y:64,z:0}` remains available only when no job is running or paused.

Do not call `internal/*` or `area/*` functions directly; they assume validated state.

## Build and tests

```sh
python tools/build.py
python -m unittest discover -s tests -v
```

A destructive full-height fixture can be installed in a NEW dedicated test world:

```sh
python tests/make_area_tests.py /path/to/test-world/datapacks/area-tests
```

Install the production ZIP as well. After server startup, `reload`, then `forceload add 112 112 175 175`, and wait until loaded. Run `function flusgrid_area_test:setup` exactly once on a fresh fixture. Wait for the production job to reach `complete`, then run `function flusgrid_area_test:check`. Require `#finished` = 1 and `#fail` = 0 in objective `fg_area`, plus job state complete/done 216. This tests a full-height stone fixture with retained ore, log, and chest samples. Do not run fixture setup on an already-processed area.

The earlier single-cube harness remains in `tests/make_runtime_tests.py`; it is also destructive and requires its own fresh world. See the 0.1.0 Git history for its detailed test procedure.
