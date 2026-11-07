execute unless data storage flusgrid:job {state:"paused"} run return run function flusgrid:status
data modify storage flusgrid:job state set value "running"
tellraw @a {text:"FlusGrid resumed. Stay nearby in Creative/Spectator.",color:"yellow"}
