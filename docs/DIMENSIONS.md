# Nether and End preparation — 0.5.0

Keep your completed Overworld. This update adds separate Nether and End jobs and ledgers; installing it does not start conversion or reset Overworld progress.

## Upgrade

1. Exit the world and back up the entire save, including its data folder.
2. Replace the old FlusGrid ZIP in that save's datapacks folder with `FlusGrid-0.5.0-experimental.zip`. Keep only one FlusGrid version installed.
3. Reopen the same world. Run `/datapack list enabled`. If the new ZIP is only available, enable it with `/datapack enable "file/FlusGrid-0.5.0-experimental.zip"`.
4. Run `/reload`. Any previously running job pauses on load; completed jobs stay complete.

## Nether: 2048 × 2048 centered at zero

Use Spectator while preparing:

```mcfunction
/gamemode spectator
/execute in minecraft:the_nether run tp @s 0 80 0
/function flusgrid:nether_pregen_2048_here
```

That selects X/Z -1024 through 1023 when standing at X/Z 0. Y 0–255 is processed, including bedrock floor and roof. It retains the existing blocks at four-block grid positions; fortresses and bastions are also thinned. No special progression protection has been added for Nether structures.

Exact equivalent from any dimension:

```mcfunction
/execute in minecraft:the_nether run function flusgrid:nether_pregen_2048_start {x:-1024,z:-1024}
```

Controls work from anywhere:

```mcfunction
/function flusgrid:nether_status
/function flusgrid:nether_pause
/function flusgrid:nether_resume
```

Run one preparation job at a time for predictable load. A 2048 square has 262,144 vertical cubes and 16,384 chunks. At one cube per tick plus acquisition ticks, the theoretical minimum is about 3h52m at 20 TPS; generation waits and lag add time. This is not a measured completion estimate.

## End: keep the dragon island, gridify outer terrain

The End worker always preserves the central 512 × 512 square: X/Z -256 through 255, at all heights. This leaves the central island, dragon arena and arrival platform untouched by FlusGrid. Protected cubes count toward processed progress but are recorded as `protected`, not converted. The pack does not claim a tested dragon fight or protect outer End cities/ships.

A 2048 square centered at zero spends much of its area on the central island and surrounding void. To prepare an eastern outer-island region instead, run:

```mcfunction
/execute in minecraft:the_end run function flusgrid:end_pregen_2048_start {x:1024,z:-1024}
```

This covers X 1024–3071, Z -1024–1023, Y 0–255. It is one outer region, not the whole End or every gateway destination. Additional regions need their own jobs. Wait for the current job to finish before starting another.

```mcfunction
/function flusgrid:end_status
/function flusgrid:end_pause
/function flusgrid:end_resume
```

Both dimensions also offer 512-square `nether_pregen_here` / `end_pregen_here` and explicit `nether_pregen_start {x:...,z:...}` / `end_pregen_start {x:...,z:...}`. Here commands require a Creative/Spectator player in the matching dimension. Explicit coordinates are minimum corners and must be multiples of 16.

## Boundaries and limitations

No automatic exploration expansion or world border is installed. Normal terrain remains outside prepared regions. Nether travel can link far beyond the prepared Overworld; a 2048-wide Nether is not automatically matched to a 2048-wide Overworld by portal scaling. Choose travel limits before opening the world to players.

Each dimension owns its job, ledger and force-load ticket. Existing third-party force-load tickets are retained. Reload pauses active jobs and releases tickets added by FlusGrid. Never delete saved ledgers to retry conversion: they prevent completed terrain and player builds from being carved again.

Retained vanilla leaves stay persistent. Strict editing does not freeze fluids, falling blocks, unsupported plants or future block updates. Realms multiplayer and survival progression remain unvalidated.
