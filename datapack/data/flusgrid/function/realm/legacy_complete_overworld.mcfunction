execute unless data storage flusgrid:fixtures overworld{ready:1b} in minecraft:overworld run return run function flusgrid:realm/fixture_tick_overworld
data modify storage flusgrid:realm bounds.overworld set value {min_x:-1024,max_x:1023,min_z:-1024,max_z:1023}
execute in minecraft:overworld run function flusgrid:realm/platform_overworld
execute in minecraft:overworld run function flusgrid:realm/portal
execute in minecraft:overworld run function flusgrid:realm/fixture_release_overworld
data merge storage flusgrid:realm {phase:"nether",owner:"nether"}
execute unless data storage flusgrid_nether:job {state:"complete",min_x:-1024,max_x:1008,min_z:-1024,max_z:1008,done:262144,chunks:16384} in minecraft:the_nether run function flusgrid_nether:pregen_2048_start {x:-1024,z:-1024}
