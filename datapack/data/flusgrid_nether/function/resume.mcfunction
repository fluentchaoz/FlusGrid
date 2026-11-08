execute unless data storage flusgrid_nether:job {state:"paused"} run return run function flusgrid_nether:status
data modify storage flusgrid_nether:job wait set value 0
data modify storage flusgrid_nether:job reason set value ""
data modify storage flusgrid_nether:job state set value "running"
tellraw @a {text:"FlusGrid resumed. Keep this preparation world running.",color:"yellow"}
