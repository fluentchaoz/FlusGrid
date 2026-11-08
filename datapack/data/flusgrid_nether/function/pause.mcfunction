execute in minecraft:the_nether run function flusgrid_nether:pregen/release
execute if data storage flusgrid_nether:job {state:"running"} run data modify storage flusgrid_nether:job state set value "paused"
function flusgrid_nether:status
