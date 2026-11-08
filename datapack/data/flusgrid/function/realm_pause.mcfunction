data modify storage flusgrid:realm manual_pause set value 1b
execute in minecraft:overworld run function flusgrid:pause
execute in minecraft:the_nether run function flusgrid_nether:pause
execute in minecraft:the_end run function flusgrid_end:pause
execute in minecraft:overworld run function flusgrid:realm/fixture_release_overworld
execute in minecraft:the_nether run function flusgrid:realm/fixture_release_nether
execute in minecraft:the_end run function flusgrid:realm/fixture_release_end
tellraw @a {text:"FlusGrid preparation paused. Finished-area travel guard remains active.",color:"yellow"}
