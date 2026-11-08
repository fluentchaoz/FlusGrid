execute unless data storage flusgrid:fixtures overworld{ready:1b} in minecraft:overworld run return run function flusgrid:realm/fixture_tick_overworld
data modify storage flusgrid:realm bounds.overworld set value {min_x:-5008,max_x:4991,min_z:-5008,max_z:4991}
execute in minecraft:overworld run function flusgrid:realm/platform_overworld
execute in minecraft:overworld run function flusgrid:realm/portal
execute in minecraft:overworld run function flusgrid:realm/fixture_release_overworld
data merge storage flusgrid:realm {phase:"nether",owner:"nether"}
execute in minecraft:the_nether run function flusgrid_nether:pregen/rectangle {x:-5008,z:-5008,ex:4976,ez:4976,chunks:390625,total:6250000}
