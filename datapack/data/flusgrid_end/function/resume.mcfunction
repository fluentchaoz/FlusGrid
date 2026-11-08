execute unless data storage flusgrid_end:job {state:"paused"} run return run function flusgrid_end:status
data modify storage flusgrid_end:job wait set value 0
data modify storage flusgrid_end:job reason set value ""
data modify storage flusgrid_end:job state set value "running"
tellraw @a {text:"FlusGrid resumed. Keep this preparation world running.",color:"yellow"}
