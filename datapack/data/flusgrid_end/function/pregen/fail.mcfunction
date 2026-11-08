data modify storage flusgrid_end:job state set value "paused"
execute in minecraft:the_end run function flusgrid_end:pregen/release
function flusgrid_end:pregen/status
