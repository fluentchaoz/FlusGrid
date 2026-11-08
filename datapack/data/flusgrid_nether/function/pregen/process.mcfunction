$execute positioned $(x) 0 $(z) unless loaded ~ ~ ~ run return run function flusgrid_nether:pregen/wait
data modify storage flusgrid_nether:job wait set value 0
$execute if data storage flusgrid_nether:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid_nether:pregen/skip with storage flusgrid_nether:job cursor
$execute if data storage flusgrid_nether:ledger regions."$(x),$(y),$(z)" run return run function flusgrid_nether:pregen/blocked
data modify storage flusgrid_nether:work origin set from storage flusgrid_nether:job cursor
scoreboard players set #quiet flusgrid 1
$execute positioned $(x) $(y) $(z) run function flusgrid_nether:internal/run with storage flusgrid_nether:work origin
scoreboard players set #quiet flusgrid 0
$execute unless data storage flusgrid_nether:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid_nether:pregen/blocked
function flusgrid_nether:pregen/advance
