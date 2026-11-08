$execute if data storage flusgrid_end:ledger regions."$(x),$(y),$(z)" run return run function flusgrid_end:pregen/blocked
$data modify storage flusgrid_end:ledger regions."$(x),$(y),$(z)" set value "started"
$data modify storage flusgrid_end:job mask set value {x:$(x),y:$(y),z:$(z),phase:0,errors:0}
