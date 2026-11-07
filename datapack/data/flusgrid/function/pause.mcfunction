execute in minecraft:overworld run function flusgrid:pregen/release
execute if data storage flusgrid:job {state:"running"} run data modify storage flusgrid:job state set value "paused"
function flusgrid:status
