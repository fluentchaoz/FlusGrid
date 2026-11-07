execute if data storage flusgrid:job {kind:"pregen"} run return run function flusgrid:pregen/tick
execute unless data storage flusgrid:job {state:"running"} run return 0
execute in minecraft:overworld run function flusgrid:area/step
