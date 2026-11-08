execute unless data storage flusgrid:fixtures nether{ready:1b} in minecraft:the_nether run return run function flusgrid:realm/fixture_tick_nether
data modify storage flusgrid:realm bounds.nether set value {min_x:-5008,max_x:4991,min_z:-5008,max_z:4991}
execute in minecraft:the_nether run function flusgrid:realm/platform_nether
execute in minecraft:the_nether run function flusgrid:realm/fixture_release_nether
data merge storage flusgrid:realm {phase:"end",owner:"end"}
execute in minecraft:the_end run function flusgrid_end:pregen/rectangle {x:-5008,z:-5008,ex:4976,ez:4976,chunks:390625,total:6250000}
