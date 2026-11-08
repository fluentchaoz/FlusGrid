scoreboard players operation #tile_x flusgrid = @s fg_x
scoreboard players operation #mod flusgrid = #tile_x flusgrid
scoreboard players operation #mod flusgrid %= #tile_size flusgrid
scoreboard players operation #tile_x flusgrid -= #mod flusgrid
execute store result storage flusgrid:realm scratch.tile.x int 1 run scoreboard players get #tile_x flusgrid
scoreboard players operation #tile_z flusgrid = @s fg_z
scoreboard players operation #mod flusgrid = #tile_z flusgrid
scoreboard players operation #mod flusgrid %= #tile_size flusgrid
scoreboard players operation #tile_z flusgrid -= #mod flusgrid
execute store result storage flusgrid:realm scratch.tile.z int 1 run scoreboard players get #tile_z flusgrid
