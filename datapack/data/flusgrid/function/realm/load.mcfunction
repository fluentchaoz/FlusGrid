scoreboard objectives add fg_x dummy
scoreboard objectives add fg_y dummy
scoreboard objectives add fg_z dummy
scoreboard objectives add fg_sx dummy
scoreboard objectives add fg_sy dummy
scoreboard objectives add fg_sz dummy
scoreboard objectives add fg_sd dummy
scoreboard players set #sixteen flusgrid 16
scoreboard players set #scan_clock flusgrid 0
scoreboard players set #scan_dim flusgrid 0
execute unless data storage flusgrid:realm initialized run data merge storage flusgrid:realm {initialized:1b,state:"idle",manual_pause:0b,live:0b}
execute in minecraft:overworld run function flusgrid:realm/fixture_release_overworld
execute in minecraft:the_nether run function flusgrid:realm/fixture_release_nether
execute in minecraft:the_end run function flusgrid:realm/fixture_release_end
execute unless data storage flusgrid:realm {manual_pause:1b} run function flusgrid:realm/resume_owned
