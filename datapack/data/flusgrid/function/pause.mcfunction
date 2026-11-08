execute if dimension minecraft:the_nether run return run function flusgrid_nether:pause
execute if dimension minecraft:the_end run return run function flusgrid_end:pause
execute in minecraft:overworld run function flusgrid:pregen/release
execute if data storage flusgrid:job {state:"running"} run data modify storage flusgrid:job state set value "paused"
function flusgrid:status
