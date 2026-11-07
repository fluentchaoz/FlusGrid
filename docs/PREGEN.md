# Prepare a 512×512 FlusGrid world — 0.3.0

This version prepares terrain before play. It generates and converts a fixed square even when you are far away, using at most one force-load ticket added by FlusGrid. It is still an experimental Overworld-only build, not automatic infinite-world generation.

## Install and start

1. Back up your test world. If an earlier job is running, use `/function flusgrid:pause` first.
2. Exit the world. Replace the old FlusGrid ZIP in its `datapacks` folder with `FlusGrid-0.3.0-experimental.zip`; keep only one version installed and leave it zipped.
3. Reopen the world in Creative or Spectator. If Minecraft lists the new pack as available rather than enabled, run:

```mcfunction
/datapack enable "file/FlusGrid-0.3.0-experimental.zip"
```

Wait for loading to finish before starting. Fly above the desired center and run:

```mcfunction
/function flusgrid:pregen_here
```

This selects a 32×32-chunk square: 512 blocks on each side, Y -64 through 319. The minimum corner is your current chunk's minimum X/Z minus 256. For example, starting in chunk X/Z 0 selects blocks X/Z -256 through 255.

**Keep the world running while it prepares.** You do not need to follow the converter. In single-player, the pause menu can stop progress. Do not begin Survival or build in unprepared terrain during this step.

At the normal 20 ticks/second, one cube per tick plus one acquisition tick per chunk has a theoretical minimum of about 21 minutes 20 seconds. Chunk generation, saving and lag add time. The pack never changes tick speed or your game rules.

An action-bar update shows completed chunks and percent. The completion message confirms all 1,024 chunks were handled and FlusGrid released its ticket. This is a preparation milestone, not a guarantee that fluids and survival progression are ready.

## Progress and interruption

```mcfunction
/function flusgrid:status
/function flusgrid:pause
/function flusgrid:resume
```

Pause retains progress and releases FlusGrid's ticket. Reload/reopening changes a running job to paused and releases any recorded owned ticket; resume explicitly when ready. Normal saves preserve the cursor and completed-cube ledger. Abrupt crashes are not transaction-safe across all world data, so keep backups.

A job will pause on a failed/interrupted cube or if a chunk stays unready for 1,200 ticks. A loading timeout can be retried with resume. A `started`/`failed` cube remains locked; restore the test backup rather than erase the ledger. Only one running/paused job is allowed. There is no cancel/reset command yet.

## What it does to terrain

The converter retains original blocks where X, Y and Z are all multiples of four, and removes the positions between them. It does not replace survivors with stone. Full height includes bedrock; no special structure/portal exceptions exist yet.

Previously completed cubes are skipped, preserving both earlier conversions and subsequent builds there. This means your artificial stone demonstration will remain if included. Fresh, unprocessed terrain may contain builds: their off-grid blocks WILL be removed.

The job loads one target chunk, waits until it is ready, works through its 24 vertical cubes, and releases its ticket before selecting the next chunk. Vanilla may load neighboring chunks as part of generation/ticket propagation; this is not a promise that only one chunk exists in memory. Recently released chunks may also remain loaded briefly.

If the target already had a force-load ticket, FlusGrid leaves that ticket alone. Do not manually add/remove tickets for its active target while it runs: Minecraft does not track independent ownership of identical administrative force-load requests.

## Boundaries and remaining limitations

- Beyond the square, terrain remains ordinary Minecraft. A 512-block square is not sufficient to conceal the boundary from every view distance or travel route.
- No automatic extension, world border, spawn platform, Nether/End conversion, or progression fixes are added.
- Strict editing suppresses immediate neighbor updates; retained fluids, sand/gravel, leaves, plants and scheduled ticks can still move or change later. Pregeneration does not solve those physics questions.
- Realms is the eventual destination. Prepare and inspect locally first; this release has no live Realm or multiplayer stress validation.
- Before removing/disabling the pack, pause it so its temporary ticket is released. Keep the world's saved ledger if you may resume conversion later.

## Explicit bounds for development

```mcfunction
/function flusgrid:pregen_start {x:4096,z:4096}
```

X/Z specify the aligned minimum corner, not the center. This example prepares X/Z 4096 through 4607. Both coordinates must be multiples of 16. The earlier 48×48 `area_here` command still exists, but shares the same one-job limit.

## Reproducible validation

Standard-library build and unit checks:

```sh
python tools/build.py
python -m unittest discover -s tests -v
```

The headless runtime test uses a fresh vanilla 26.3 server with Java 25 and no players near the target. A pre-existing `forceload add 4096 4096` tests ownership preservation; start the explicit job above, then inspect status and force-load tickets before/after pause, reload, restart and completion. Only the pre-existing ticket should remain when paused/complete.

The full-size test used an accelerated tick rate after initial normal-rate checks; this is a development test setting, not a player recommendation or normal-rate performance measurement.

Optional offline completion audit, after stopping that server (requires `pip install nbtlib`):

```sh
python tests/audit_pregen_save.py /path/to/world
```

The audit verifies every expected ledger key, completed counts, and absence of an owned ticket in the saved job. It does not assert that later physics left all converted blocks unchanged.
