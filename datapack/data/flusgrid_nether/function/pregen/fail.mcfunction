data modify storage flusgrid_nether:job state set value "paused"
execute in minecraft:the_nether run function flusgrid_nether:pregen/release
function flusgrid_nether:pregen/status
