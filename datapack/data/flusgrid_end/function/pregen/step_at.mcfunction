$execute positioned $(x) 0 $(z) if predicate flusgrid_end:protected_center run return run function flusgrid_end:pregen/protect with storage flusgrid_end:job cursor
execute unless data storage flusgrid_end:job ticket run return run function flusgrid_end:pregen/acquire with storage flusgrid_end:job cursor
function flusgrid_end:pregen/process with storage flusgrid_end:job cursor
