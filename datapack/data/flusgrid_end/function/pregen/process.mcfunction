$execute positioned $(x) 0 $(z) unless loaded ~ ~ ~ run return run function flusgrid_end:pregen/wait
data modify storage flusgrid_end:job wait set value 0
$execute if data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid_end:pregen/skip with storage flusgrid_end:job cursor
$execute if data storage flusgrid_end:ledger regions."$(x),$(y),$(z)" run return run function flusgrid_end:pregen/blocked
data modify storage flusgrid_end:work origin set from storage flusgrid_end:job cursor
scoreboard players set #quiet flusgrid 1
$execute positioned $(x) $(y) $(z) run function flusgrid_end:internal/run with storage flusgrid_end:work origin
scoreboard players set #quiet flusgrid 0
$execute unless data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid_end:pregen/blocked
function flusgrid_end:pregen/advance
