data modify storage flusgrid:job state set value "paused"
tellraw @a {text:"FlusGrid paused: a cube is failed or interrupted. Inspect /function flusgrid:status. Restore a backup; do not erase the region ledger to retry.",color:"red"}
