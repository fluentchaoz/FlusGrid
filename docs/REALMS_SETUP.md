# One-map setup — FlusGrid 0.6.0 experimental

This is one vanilla Java 26.3 datapack for local preparation followed by a Realms trial. It preserves natural blocks at four-block grid positions, prepares dimensions in order, then expands finished terrain in response to players. It is **not certified for production Realms**, and unlimited uninterrupted elytra exploration is not promised.

## Pick one world and install

1. Pick your seed/world. Keep a full backup. You can use the existing prepared FlusGrid world; keep its saved data/ledgers.
2. Exit Minecraft. Put only `FlusGrid-0.6.0-experimental.zip` in that world's `datapacks` folder, unextracted. Remove older FlusGrid ZIPs from that folder.
3. Reopen the world. Check `/datapack list enabled`. If needed:

```mcfunction
/datapack enable "file/FlusGrid-0.6.0-experimental.zip"
```

4. Use Creative or Spectator, before Survival/Adventure players join. Start once:

```mcfunction
/gamemode spectator
/function flusgrid:setup
```

The controller runs **Overworld → Nether → End** without additional start commands. Do not run the old independent start commands while the controller owns a job.

| Dimension | Initial finished square | Height |
|---|---|---|
| Overworld | X/Z -1024..1023 (2048×2048) | -64..319 |
| Nether | X/Z -1024..1023 (2048×2048) | 0..255 |
| End | X/Z -2048..2047 (4096×4096) | 0..255 |

The larger End includes outer-island territory inside the usable frontier. Terrain distribution still depends on the seed; specific cities/ships are not guaranteed.

A fresh setup has 1,703,936 ordinary cube steps, plus chunk acquisition, generation waits and extra steps for End protection. Its theoretical normal-speed lower bound is approximately 25 hours; actual time can be longer. Keep Minecraft running and unpaused. This is not a measured full-run ETA. A completed centered 2048 Overworld/Nether job with matching saved bounds/counts is adopted; other completed cubes are skipped as encountered. Existing unfinished jobs must finish before setup can take ownership.

## Controls

```mcfunction
/function flusgrid:realm_status
/function flusgrid:realm_pause
/function flusgrid:realm_resume
```

Use these controller commands, not the old dimension controls, for this workflow. A clean reload/restart automatically resumes the controller-owned job unless manually paused. Failed/interrupted cubes remain locked; never erase ledger entries to force a retry. Backups are necessary because world blocks and command storage are not crash-atomic.

When status becomes `ready`, inspect and back up the world, then upload the **whole save** to Realms. Keep the datapack and world data. Automatic expansion and the travel guard are already enabled. A real Realm trial with multiple players and elytra remains required before inviting everyone.

## Portals and safe arrival

After Overworld preparation, the pack creates an End portal frame centered at **0, -32, 0**, with all twelve frames empty and facing inward. Fill them with Eyes of Ender. Its 7×7 obsidian footing is at Y -33; the interior remains air until activation.

Small obsidian arrival platforms are created at Overworld/Nether (0,80,0), with standing height 81, and End (100,48,0), with standing height 49. The Overworld world spawn is set to (0,81,0) with respawn radius zero. These small platform/portal footprints are deliberately cleared once after preparation, so do not place builds there before setup completes. Players still need to create a Nether portal.

## End treatment

The old 512×512 untouched central square is removed. Terrain is gridded except:

- A central 17×17 column, X/Z -8..8, retains the natural podium foundation and exit-portal stage.
- Each actual vanilla pylon bedrock cap is located before editing. A small neighborhood around it preserves the top, crystal support and cage. The shafts below become grid terrain.
- The normal arrival-platform area is retained; the setup also creates its safe platform.

The cap scan uses all relevant central chunks, then journals protected cubes through small resumable steps. Those temporary chunk tickets are released on pause/reload/completion. Existing tickets from other systems are retained.

Old 0.5 `protected` entries explicitly meant untouched terrain and can now be converted; `complete`, `started` and `failed` entries are never silently reset. If players built in that previously exempt End square, use a backup/new world rather than converting those builds.

This preserves the initial arena geometry; it is not a completed dragon-fight/respawn playtest. Vanilla dragon respawning can regenerate full pillars later. Outer End cities, ships, and gateway structures are not generally exempt from gridding.

## Automatic expansion and its limits

Survival/Adventure players are checked against each dimension's finished rectangle. Creative/Spectator are exempt for administration.

- Approaching within 768 blocks of a finished edge requests a **512-block-wide strip spanning that entire edge**.
- Only one automatic strip runs globally, across all players/dimensions. Duplicated requests do not replace it. Regular scans rotate between dimensions and randomize player order; out-of-bounds arrivals can request work immediately.
- The strip opens only after every scheduled cube completes. Interrupted work does not move the finished boundary.
- A 512-block buffer stays between players and unfinished terrain. Crossing that inner boundary returns the player to their last recorded safe position in that dimension and briefly applies Slow Falling. A first arrival outside the usable region returns to its safe arrival platform.
- Pausing conversion leaves that travel guard active. A distant portal/gateway/teleport can therefore return a player to a safe platform until its destination area is prepared.

With initial bounds, the usable Overworld/Nether X/Z range is -512..511; the End is -1536..1535. Each completed strip opens another 512 blocks on that side. The buffer is intentional: players should not build where a future conversion will clear blocks.

A single initial-width Overworld strip involves 4096 chunks / 98,304 cubes: about 85 minutes minimum at normal tick rate, before generation waits. Elytra can outrun this. The guard prevents entering unfinished regions; it cannot make the worker as fast as flight or guarantee invisible transitions on every client/portal arrival. Heavy exploration in several directions will cause waits. Larger prepared regions before play are the way to reduce those waits.

The datapack does not change tick speed or install a server plugin. Its durable ledger and world size grow as more terrain is prepared. Keep backups and monitor actual Realm responsiveness. The current default deliberately favors bounded command work over maximum throughput.

## Physics and progression still need a playtest

Retained vanilla leaves are persistent. Fluids, falling blocks, unsupported plants, fire, mob behavior and dragon destruction still behave normally when updated. Most structures are thinned with the terrain; loot and progression availability depend on retained positions and seed. This update does not certify a fully balanced, deterioration-free survival experience.

## Archive to Flunkstar

Before disabling/removing the pack or importing as an archived world:

```mcfunction
/function flusgrid:archive
```

This pauses jobs, releases owned tickets, and disables automatic work and the travel guard. Download/preserve the complete save. Do not run conversion across existing Flunkstar builds.
