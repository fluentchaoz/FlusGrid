$execute positioned $(x) 0 $(z) unless loaded ~ ~ ~ run return run function flusgrid:pregen/wait
data modify storage flusgrid:job wait set value 0
$execute if data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:pregen/skip with storage flusgrid:job cursor
$execute if data storage flusgrid:ledger regions."$(x),$(y),$(z)" run return run function flusgrid:pregen/blocked
data modify storage flusgrid:work origin set from storage flusgrid:job cursor
scoreboard players set #quiet flusgrid 1
$execute positioned $(x) $(y) $(z) run function flusgrid:internal/run with storage flusgrid:work origin
scoreboard players set #quiet flusgrid 0
$execute unless data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:pregen/blocked
function flusgrid:pregen/advance
