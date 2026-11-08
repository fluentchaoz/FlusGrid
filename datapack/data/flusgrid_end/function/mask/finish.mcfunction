$execute unless data storage flusgrid_end:job mask{errors:0} run data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "failed"
execute unless data storage flusgrid_end:job mask{errors:0} run return run function flusgrid_end:pregen/blocked
$data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "complete"
data remove storage flusgrid_end:job mask
function flusgrid_end:pregen/advance
