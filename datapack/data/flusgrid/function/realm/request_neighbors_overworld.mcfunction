scoreboard players operation #threshold flusgrid = #tile_x flusgrid
scoreboard players add #threshold flusgrid 192
execute if score @s fg_x < #threshold flusgrid run function flusgrid:realm/neighbor_overworld_west
scoreboard players operation #threshold flusgrid = #tile_x flusgrid
scoreboard players add #threshold flusgrid 319
execute if score @s fg_x > #threshold flusgrid run function flusgrid:realm/neighbor_overworld_east
scoreboard players operation #threshold flusgrid = #tile_z flusgrid
scoreboard players add #threshold flusgrid 192
execute if score @s fg_z < #threshold flusgrid run function flusgrid:realm/neighbor_overworld_north
scoreboard players operation #threshold flusgrid = #tile_z flusgrid
scoreboard players add #threshold flusgrid 319
execute if score @s fg_z > #threshold flusgrid run function flusgrid:realm/neighbor_overworld_south
