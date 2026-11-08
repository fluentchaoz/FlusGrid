# Small portal-return experiment — 0.1

This is a **separate datapack**, not a replacement for FlusGrid 0.6 and not the new radius scheduler. It never clears terrain, builds portals, force-loads chunks or queues generation. A rejection is deliberately simulated so we can test departure-point return and messages first.

## Install in a disposable world

Use a new Creative Java 26.3 world or a copy of your save. Install only `FlusGrid-portal-return-test-0.1.zip` for this experiment. Do not combine it with an active FlusGrid travel guard. Keep your actual preparation world unchanged.

If available but not enabled:

```mcfunction
/datapack enable "file/FlusGrid-portal-return-test-0.1.zip"
```

Build and light an ordinary Nether portal on a broad flat obsidian/stone floor, with clear standing room in front of it. Link/check both sides normally before arming if you want a predictable exit. Test on foot, initially in Creative. Do not start mounted or in a vehicle.

## Test 1 — reject and return

Stand at least 3 blocks outside the portal, with open air around your feet/head and a full obsidian/stone block underfoot. Run:

```mcfunction
/function fg_portal_test:arm
```

Walk into the portal. Expected:

1. The normal dimension transition may happen briefly.
2. You return to your recent clear approach point in the departure dimension, **not world spawn**.
3. A title says **Destination not ready**, with subtitle **TEST: Returned to your portal approach**. A yellow action-bar message remains briefly.
4. You stay outside the portal without an automatic teleport loop.

The checkpoint updates as you walk on suitable open ground, then stops updating near portal blocks. This is a conservative last-safe approach point, not a promise of the exact last pixel before transit.

Inspect diagnostics:

```mcfunction
/function fg_portal_test:status
```

Dimension IDs: 1 Overworld, 2 Nether, 3 End. Destination coordinates in status use fixed-point units: divide by 16. All player state is stored separately; the temporary command storage is reused synchronously.

## Test 2 — simulate a ready destination

While still armed, run:

```mcfunction
/function fg_portal_test:allow_next
```

Enter the portal again. This crossing should be allowed and the allowance consumed. Step away from the arrival portal onto an open solid floor before trying the reverse crossing. The return trip should now be rejected back to your **Nether approach point**.

This command does not grid anything or grant a permanent region exemption. It only lets one dimension change through for this test.

## Stop

```mcfunction
/function fg_portal_test:off
```

Disabling is per player. Reloading, reconnecting after a tick gap, or dying disarms the test; arm again on safe ground. Removing/disabling this standalone ZIP stops all its behavior.

## What to report

- Did it return you to the correct departure dimension and approach point?
- Did the title/action bar appear?
- Any suffocation, fall, portal loop, disconnect or failure message?
- Did `allow_next` permit exactly one crossing?
- Repeat with two players separately armed and taking different portals, then in Survival when comfortable.

## Scope and failure behavior

The detector observes **dimension changes after they happen**. It also catches administrator cross-dimension teleports while armed; it is not a cancellable pre-portal event. Same-dimension End gateways, player mounts/passengers and death/respawn routing are not part of this test.

The return checkpoint must still be loaded, on a supported full-block floor, have clear neighboring air, and be outside nearby portal blocks. If it cannot be validated, or the traveller is mounted, the test disables itself and displays a red failure message. It leaves the traveller at the destination rather than guessing another location or sending them to spawn. This is a diagnostic experiment, **not an access-control safeguard**.

Supported floors are deliberately limited to common full stone/dirt/obsidian/netherrack/end-stone blocks and vanilla planks. Air checks are conservative; foliage, slabs and cramped corridors may prevent recording. Precision is 1/16 block, allowing the coordinate scores to fit across vanilla world bounds. Portal cooldown/transition visuals and client movement still require actual player testing.
