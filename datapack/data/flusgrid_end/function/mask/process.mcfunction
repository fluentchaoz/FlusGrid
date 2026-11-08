$execute if data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"complete"} run return run function flusgrid_end:pregen/skip with storage flusgrid_end:job cursor
execute unless data storage flusgrid_end:job mask run return run function flusgrid_end:mask/init with storage flusgrid_end:job cursor
$execute unless data storage flusgrid_end:job mask{x:$(x),y:$(y),z:$(z)} run return run function flusgrid_end:pregen/blocked
$execute unless data storage flusgrid_end:ledger regions{"$(x),$(y),$(z)":"started"} run return run function flusgrid_end:pregen/blocked
function flusgrid_end:mask/dispatch with storage flusgrid_end:job mask
