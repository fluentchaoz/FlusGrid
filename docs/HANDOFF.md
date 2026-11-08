# Development handoff

Updated: 2026-11-08

## Queued regions failing to start — fixed and runtime-confirmed (2026-11-08)

Ryan's screenshot showed controller {state:"ready",phase:"complete",live:1b,
model:10000,manual_pause:0b}, several queued Overworld tiles, and no
active owner. In Creative, tiles were indeed being REQUESTED, but never
started. Creative no-teleport behavior is intentional.

Two independent invalid vanilla command forms were fixed in tools/tenk.py:
- Tile dispatch used the invalid syntax "execute if data storage
  flusgrid:realm queue[0] {dimension:...}". Instead, copy queue[0] into
  the temporary dispatch compound and use a valid root NBT predicate
  against dispatch.dimension.
- Tile workers tried "data merge storage flusgrid:realm rectangle {...}".
  Vanilla data merge accepts an NBT compound for the full storage; the
  correct command is "data merge storage flusgrid:realm {rectangle:{...}}".

Python tests did not detect the second issue. A new
tests/run_10k_runtime.py launches actual vanilla Java 26.3 on GitHub
Actions (Java 25), loads the generated ZIP, enqueues an Overworld tile,
invokes the dispatch function, and asserts owner=overworld,
plan=(overworld,0,0), state=running, chunk_total=1024, and the queue head
consumed. **Vanilla runtime PASSED** on 2026-11-08 (Actions run
42513222035). This is not a real connected-player or full conversion
test, so the user must still validate Creative traversal and progress
in the actual world after replacing the ZIP and reloading. Do not
restart initial setup or erase queued tiles; this fix consumes them.

## 0.7 experimental feature branch — 10K and automatic remote tiles (2026-11-08)

Git branch: feature/10k-regions; draft PR #1. Built ZIP:
dist/FlusGrid-0.7.0-10k-experimental.zip. Main is still 0.6.
The new tools/tenk.py generator runs after tools/realms.py via tools/build.py.
The GitHub Actions workflow builds the ZIP, runs unittest and commits
generated datapack resources to the feature branch only.

Production setup is a centered 10,000×10,000 square per dimension:
X/Z -5008..4991, total 21,875,000 full-height cubes. At 20 TPS the
theoretical lower bound is about 12.66 active days. Small smoke test:
new world, /function flusgrid:setup_smoke, 256×256 each dimension
(-128..127), then the identical queued 512×512 remote-tile logic.

On-demand design: 64-entry deduplicated persistent queue, one global
rectangle job, ready-tile map per dimension, only commit usable status
after complete worker. Ordinary player ticks automatically queue a
tile for unsafe arrivals and nearby unconverted edges. The hold guard
sends the player to their last recorded safe approach, in its source
dimension when appropriate; it does not intentionally return them to
world spawn. Any grounded terrain can make a checkpoint provided 3×3
clearance, no nearby portal and no hazardous floor. Checkpoint/source
validation can still fail if source is unloaded or changed; in that case
a red diagnostic is shown and no fake fallback is attempted. This is
NOT yet a guarantee against entering ungridded terrain.

**Creative feedback change:** Players in Creative now enter the same
automatic tile-request scan as Survival/Adventure but return from the
handler before the teleport guard; they keep flying/walking into unprepared
areas while generation queues in the background. Spectator alone remains
excluded from the scan. Negative X/Z tile targeting also now uses
nonnegative modulo before alignment (Minecraft scoreboard remainder is
negative for negative inputs). Regression contracts check both behaviors.


**Remaining before promoting to main:** actual Java 26.3 player
test of setup_smoke; check the first unprepared Nether portal crossing,
message, accurate return point, automatic queued job, and accepting a
repeat crossing after tile completion. Test at least two players,
disconnect/reconnect, mounted transit and fast movement. A vanilla
headless/Realm run has NOT been done for 0.7. Read docs/TENK_MODEL.md
and do not tell players the pack is fully production ready.

## Scope and user feedback

Ryan wants a fresh RaysGrid-inspired Java 26.3 world, ultimately playable on Java Realms and archived in Flunkstar afterward. Vanilla datapack, no client mod/server plugin substitution without discussion.

He successfully tested 0.1.0's stone grid and 0.2.0's actual full-height terrain grid. He proposed preparing terrain hundreds of blocks ahead to hide conversion. We agreed to bounded local pregeneration before Realms rather than promising live exploration performance. The next delivered milestone is a 512×512 preparation job.

## Latest requested direction and isolated portal test

After0.6, Ryan discussed25k targets, then changed to10k initial preparation with on-demand regions beyond it. Far Nether-linked destinations need separate prepared regions, not a single enormous rectangle. Those scheduler/region changes are NOT implemented. Current0.6 still uses the documented initial2048/2048/4096 setup and strips.

Before implementing that larger change, Ryan authorized a small portal-return proof: return to the departure approach (not spawn), with an explanatory on-screen message. `tools/build_portal_test.py` builds standalone `portal-test/` and `dist/FlusGrid-portal-return-test-0.1.zip`. It does not mutate terrain, queue work, force-load or call the main pack. Main0.6 ZIP is unchanged. Run this only in a separate test world without an active FlusGrid guard.

Opt in with `fg_portal_test:arm`, test one allowed crossing with `allow_next`, inspect `status`, stop with `off`. Per-player scoreboard checkpoints update on conservative full-block/open-air positions outside portal proximity. Dimension changes are detected after arrival. Valid source return uses dimension plus fixed-point coordinates/rotation. Invalid/unloaded sources or mounted transit disarm and leave the traveller at the destination with a diagnostic; no spawn fallback. This is not yet an access-control guarantee. Reload/reconnect/death disarms and needs rearming.

Actual pig portal crossings passed both directions and simultaneous independent checkpoint tests. No connected-player/Realm client test yet; see TEST_RESULTS. Next step is Ryan's on-foot in-game test: return location, message visibility, no automatic loop, allow-next crossing, reverse direction. Do not claim player/vehicle/session behavior proven by pig fixtures. Only integrate a successful tested approach into the scheduler afterward.

## Current build: 0.6.0 — one-map controller and guarded frontier

User now wants one pack that prepares Overworld, Nether and End in order, then starts large remote swaths as players approach. End should be gridded except pylon tops and exit/dragon podium. Add empty End portal centered at Overworld (0,-32,0), keeping the previous requirement to fill twelve Eyes.

`tools/realms.py` generates controller, rectangular jobs, player frontier checks, stage decorations and End masks. `/function flusgrid:setup` starts 2048 Overworld, 2048 Nether, 4096 End centered at zero. Exact matching completed centered Overworld/Nether jobs are adopted without redoing them. Other completed cubes skip. Stage structures wait for their own chunks and release only owned tickets. Existing legacy jobs must not be running/paused at setup entry.

One automatic expansion globally: a player within768 blocks of a finished boundary requests a512-wide strip spanning the edge. Boundaries commit only after full completion. Survival/Adventure guard holds players512 blocks inside finished terrain, returning them to per-player/per-dimension-safe coordinates or a fallback platform. Creative/Spectator bypass. Guard remains active while preparation is paused. This DOES NOT guarantee seamless unlimited elytra flight; expansion can take hours. Do not conceal this limit.

Normal ticks keep one cube per tick. End central/arrival cubes use a durable mask cursor: init, four carve phases, four verify phases, finish. The original single-tick mask exceeded65536 commands in runtime; final split worker stays under the tested budget. Journal errors lock a cube. Load/pause releases arena tickets; resume reacquires and reconstructs marker caps before continuing the saved phase. End cap detection scans actual bedrock heights at vanilla spike centers with rounding tolerance, preserving13×11×13 neighborhoods (selector boundary details), a17×17 podium column and arrival area. First-fight geometry tested; actual fight/respawn not certified. Vanilla respawn can regenerate pillars. Outside these areas, End structures/gateways are gridded too.

Saved state: `flusgrid:realm` controller, per-dimension original jobs/ledgers, `flusgrid:fixtures` temporary owned stage tickets, `flusgrid_end:arena` owned central tickets/ready flag. New player scoreboards `fg_x/y/z`, `fg_sx/sy/sz`, `fg_sd`. `flusgrid_cap` markers identify caps. No random-tick shutdown, custom worldgen or plugin dependencies. Physics limitations remain.

Use `docs/REALMS_SETUP.md` as current player instructions. Current build: `dist/FlusGrid-0.6.0-experimental.zip`. Historical dimension instructions describe different End protection. Read TEST_RESULTS for exact runtime scope; never claim the entire25-hour setup or Realms session ran here. `/function flusgrid:archive` pauses/releases and disables the player guard for eventual Flunkstar import.

## Previous build: 0.5.0 — isolated dimension preparation

Ryan reports completing the 2048×2048 Overworld in about six hours on 0.4.0. Preserve that world and its original `flusgrid` storage. Nether and End use `flusgrid_nether` / `flusgrid_end` namespaces for jobs, work and ledgers. `tools/dimensions.py` generates these workers from the Overworld template before context-dispatch controls are appended. Shared scoreboard scratch is used only synchronously within a tick/function. All three dimension workers have tick handlers; recommend one job at a time.

Both new dimensions process Y 0–255 (16 cubes/chunk). Their 2048 jobs have 262,144 cubes, 16,384 chunks. The End excludes the central X/Z [-256,255] square before force-load acquisition, recording protected entries and advancing progress. Single-cube conversion also checks the guard. In 26.3 predicate JSON uses `type`, not the older `condition` field; the runtime caught this during development.

Public commands and upgrade steps are in `docs/DIMENSIONS.md`; current ZIP is 0.5.0. Dimension-specific status/pause/resume work from anywhere, while generic controls follow the caller's dimension. Explicit start APIs must execute in the intended dimension. No automatic conversion begins on installation. No changes to physics beyond existing leaf persistence, no portal safety system, no automatic border, and no End-city preservation. Central arena preservation is not a gameplay certification of the dragon fight.

See TEST_RESULTS.md for runtime coverage. Do not describe any full 2048 Nether/End run as completed unless newly verified.

## Previous build: 0.4.0 — large prep and persistent leaves

Ryan requested 2048×2048 prep code so he could start preparing while further development proceeds, and specifically asked to prevent leaves/other normal deterioration. This build adds `pregen_2048_here` and explicit `pregen_2048_start {x,z}` minimum-corner API. Size-specific start functions share a worker using job.total/chunk_total rather than hardcoded 512 counts. Old 512 commands remain unchanged; load migrates missing size/chunk_total on old pregen jobs. 2048 means 16,384 chunks / 393,216 cubes, at least 5h41m20s at normal tick rate before lag/waits. No optimization, ETA, border or new survival setup in this build.

Leaf persistence is applied BEFORE removal, only to retained grid positions. `tools/leaves.py` enumerates all 14 species from the actual 26.3 vanilla leaves tag. Only persistent changes; distance, waterlogging and species remain. Previously completed cubes get leaf-only repair on skip, never re-clearing builds. Existing missing leaves cannot be recovered.

Do not say all physics are frozen: fluids, falling blocks, grass/farmland and unsupported plants remain unresolved. No global random-tick rule is changed by the pack. Persistent leaves can still be mined/burned/exploded. Custom species outside vanilla are unsupported.

The Overworld guide is `docs/PREP_2048.md`; 0.4.0 was the first large-prep ZIP. Test details belong in TEST_RESULTS.md. A complete 2048 run is NOT yet validated/timed. The user's requested extra stability work needs further investigation; don't imply it happens asynchronously after a response.

## Previous build: 0.3.0 experimental pregen

`/function flusgrid:pregen_here` selects 32×32 chunks, from the caller's chunk minimum minus 256 on both axes, full height -64..319. Caller must be a Creative/Spectator player in the Overworld. Explicit minimum-corner API: `/function flusgrid:pregen_start {x:4096,z:4096}`.

A compact cursor processes 24 vertical cubes per chunk, X-fast then Z rows. The job acquires at most one force-load ticket, waits for readiness, converts one 16-cube per tick, releases its ticket, and moves on. No enormous cube queue is materialized. One extra acquisition tick per chunk plus generation waits makes the normal-speed theoretical minimum about 21m20s. The pack does not modify game speed/rules.

`flusgrid:job`: kind=pregen, state, cursor, min/max chunk origins, done/total=24576, chunks/1024, percent, wait, reason, optional ticket{x,z,owned}. Existing force-load tickets are recognized and never deliberately removed. Only tickets added by FlusGrid are released; external code should not modify the same target ticket concurrently.

Controls remain status/pause/resume. Pause and load/reload release the owned ticket. Load marks an active job paused. Resume explicitly reacquires the current chunk and continues. Chunk readiness timeout is 1200 ticks. Started/failed cube entries pause and refuse conversion; no cancel/reset is offered. Do not delete ledger entries to retry partial work.

The 48×48 area command still exists and shares the same one-job guard. Older area jobs without kind remain compatible with the area tick path. The area path never acquires tickets. Single-cube conversion is blocked while any job is running/paused.

## Converter and persistence

`flusgrid:ledger` regions has canonical x,y,z keys and started/complete/failed values. Spacing 4 is experimental. Each 16-cube retains 64 positions, clears via 124 strict fill boxes, then checks 4032 removed positions. Retained blocks are not rewritten. Completed entries are skipped even if builds or later physics changed that cube.

Scoreboard `flusgrid` and `flusgrid:work` are scratch state. Job and ledger are normally saved, not crash-atomic transactions across all world files. Backups still matter.

## Files and validation

- `tools/build.py`, `tools/area.py`, `tools/pregen.py`: standard-library generators.
- `datapack/`: generated files; `dist/FlusGrid-0.5.0-experimental.zip`: current build. Keep only this ZIP installed; older ZIPs are historical downloads.
- `docs/PREGEN.md`: current player instructions; `docs/TESTING.md`: earlier area demonstration.
- `docs/TEST_RESULTS.md`: runtime results and limits.
- `tests/audit_pregen_save.py`: optional offline audit of all expected ledger entries for the selected dimension; needs nbtlib. 26.3 storage path is world/data/flusgrid/command_storage.dat.

Review the recorded test results before making claims. Headless runtime tests use a separate disposable vanilla 26.3 server with Java 25. Accelerated tick rate is for development testing only; it is not normal-speed performance or a Realm test. The player wrapper is parsed but not tested through a graphical connected player here.

## Next work

Inspect Ryan's prepared square and address fluid flow, leaf decay, falling blocks, scheduled ticks and boundary inflow. Strict editing is not permanent physics suppression. Then decide progression exceptions, spawning, borders/expansion and portal travel limits before attempting Realms survival.

Beyond the square, ordinary terrain remains. No automatic exploration extension or world border is installed. This is not a full survival pack or certified Realms compatibility. Preserve the saved ledger when importing, and pause before removing/disabling the pack so its ticket is released.
