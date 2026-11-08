# FlusGrid 0.7 experimental — 10K initial preparation and remote regions

**Status: development branch, not certified for a live Realm.** Build with
python tools/build.py and take the output named
dist/FlusGrid-0.7.0-10k-experimental.zip. Install this ZIP alone in a
new/disposable Java 26.3 world. Do not stack it with 0.6 or the standalone
portal-return test ZIP.

## What 10K means

A **10,000 × 10,000-block square in each dimension**, *not* a 10,000-block
radius: X/Z -5008 through 4991 inclusive. The cube origins end at 4976.
The initial controller prepares **Overworld → Nether → End** with the existing
persistent, one-cube-per-tick backend, then enables automatic region requests.

| Dimension | Initial chunks | Full-height cubes |
| --- | ---: | ---: |
| Overworld (-64..319) | 390,625 | 9,375,000 |
| Nether (0..255) | 390,625 | 6,250,000 |
| End (0..255) | 390,625 | 6,250,000 |
| **Total** | **1,171,875** | **21,875,000** |

At 20 ticks/second and one cube per tick, the **theoretical minimum** is
12 days, 15 hours and 49 minutes of active simulation. Chunk generation,
ticket waits and special End protection increase that. This has *not* been
timed end to end; do not start a production Realm before preparing offline
and testing the entire save. At a Realm that suspends while nobody plays,
preparation may not advance.

## Start, pause and resume

Back up your save. Switch to Creative/Spectator and run once:

    /function flusgrid:setup
    /function flusgrid:realm_status

Control a running job with /function flusgrid:realm_pause and
/function flusgrid:realm_resume. Initial work is restart-resumable and
preserves previously completed journal entries. Existing unfinished
dimension jobs must finish before setup starts. The 0.6 legacy controller
remains supported if you never invoke this 0.7 setup on that save; this
version does **not** migrate a partially prepared 0.6 campaign to 10K.

## Automatic regions after setup

The new scheduler **does not convert one enormous edge strip**. When a
Survival/Adventure player nears a prepared boundary, it queues adjacent
**512 × 512-block tiles**. If a player arrives outside the completed area
(for example via a far-away Nether portal), the tile containing the arrival
is requested automatically; no player command is required. The queue and
in-flight jobs persist across clean reloads, with one conversion worker
active globally. It deduplicates queued destinations and caps the backlog
at 64 tiles. A paused controller still retains queued work.

Tiles are marked usable **only after conversion is complete**; old ledger
entries remain respected. A tile may overlap the original square at a
boundary, which safely skips already completed cubes. A tile uses
24,576 Overworld cubes or 16,384 Nether/End cubes. Minimum per tile at
20 TPS: about 20m29s Overworld, 13m39s Nether/End, before waiting.

## Travel handling

At each game tick, players are checked against the initial 10K square
and completed remote tiles. Players who enter unfinished terrain trigger
a tile request and are returned to their last *recorded safe approach*
instead of being sent to world spawn. The checkpoint is updated
automatically while they stand on an allowed full block, with a 3×3
clearance and no nearby portal. It retains dimension, position and
rotation. Rejected Nether cross-dimension arrivals can return to their
Overworld checkpoint, or the reverse, **after the vanilla portal transfer
has occurred**. A title explains that the destination is not ready.

The checkpoint is deliberately conservative. If it has never been
recorded, is blocked/unsafe or is no longer loaded, teleportation is
refused with a red diagnostic rather than silently using world spawn.
This exceptional case means the implementation is **not yet a hard
access-control guarantee**. A player could remain at the destination
until an operator assists. Mounted travel, player reconnects, portal
cooldowns and same-dimension End gateways have not been validated.

Elytra, high-speed movement and portal timing may expose unfinished
terrain for a tick before the datapack can react. The converter cannot
instantly generate far-away chunks. Multi-client portal and Realm tests
are mandatory before inviting players.

## End, physics and preservation

The previous 0.6 central End arena mask and created empty End portal remain.
The first dragon fight, dragon respawn, structure/loot availability and
plant/fluid/falling-block physics still require gameplay testing. Vanilla
leaves retained by the grid are made persistent; unsupported blocks can
otherwise deteriorate or move.

When finished, use /function flusgrid:archive and preserve the complete
world save before importing it into Flunkstar.

## Developer checks

python tools/build.py generates the pack and ZIP.
python -m unittest discover -s tests -v checks static contracts.
GitHub Actions also attempts this build on feature/10k-regions and
publishes the experimental ZIP as an artifact. These checks do **not**
establish a real client/Realms survival test.
