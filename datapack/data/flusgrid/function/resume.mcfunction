execute unless data storage flusgrid:job {state:"paused"} run return run function flusgrid:status
data modify storage flusgrid:job wait set value 0
data modify storage flusgrid:job reason set value ""
data modify storage flusgrid:job state set value "running"
tellraw @a {text:"FlusGrid resumed. Keep this preparation world running.",color:"yellow"}
