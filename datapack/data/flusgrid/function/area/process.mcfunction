$execute if data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:area/skip with storage flusgrid:work origin
$execute if data storage flusgrid:ledger regions."$(x),$(y),$(z)" run return run function flusgrid:area/blocked
$execute positioned $(x) $(y) $(z) unless loaded ~ ~ ~ run return run function flusgrid:area/unloaded
scoreboard players set #quiet flusgrid 1
$execute positioned $(x) $(y) $(z) run function flusgrid:internal/run with storage flusgrid:work origin
scoreboard players set #quiet flusgrid 0
$execute unless data storage flusgrid:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid:area/blocked
function flusgrid:area/advance
