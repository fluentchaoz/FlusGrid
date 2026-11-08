execute in minecraft:the_end run function flusgrid_end:arena/release
execute in minecraft:the_end run function flusgrid_end:pregen/release
execute if data storage flusgrid_end:job {state:"running"} run data modify storage flusgrid_end:job state set value "paused"
function flusgrid_end:status
