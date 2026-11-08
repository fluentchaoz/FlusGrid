execute unless data storage flusgrid:fixtures nether{ready:1b} in minecraft:the_nether run return run function flusgrid:realm/fixture_tick_nether
data modify storage flusgrid:realm bounds.nether set value {min_x:-1024,max_x:1023,min_z:-1024,max_z:1023}
execute in minecraft:the_nether run function flusgrid:realm/platform_nether
execute in minecraft:the_nether run function flusgrid:realm/fixture_release_nether
data merge storage flusgrid:realm {phase:"end",owner:"end"}
execute in minecraft:the_end run function flusgrid_end:pregen/rectangle {x:-2048,z:-2048,ex:2032,ez:2032,chunks:65536,total:1048576}
