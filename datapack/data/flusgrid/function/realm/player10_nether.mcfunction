scoreboard players set #current flusgrid 2
execute store result score @s fg_x run data get entity @s Pos[0] 1
execute store result score @s fg_y run data get entity @s Pos[1] 1
execute store result score @s fg_z run data get entity @s Pos[2] 1
scoreboard players set #inside flusgrid 0
scoreboard players set #main flusgrid 0
execute store result score #bmin_x flusgrid run data get storage flusgrid:realm bounds.nether.min_x
execute store result score #bmax_x flusgrid run data get storage flusgrid:realm bounds.nether.max_x
execute store result score #bmin_z flusgrid run data get storage flusgrid:realm bounds.nether.min_z
execute store result score #bmax_z flusgrid run data get storage flusgrid:realm bounds.nether.max_z
execute if score @s fg_x >= #bmin_x flusgrid if score @s fg_x <= #bmax_x flusgrid if score @s fg_z >= #bmin_z flusgrid if score @s fg_z <= #bmax_z flusgrid run scoreboard players set #main flusgrid 1
execute if score #main flusgrid matches 1 run scoreboard players set #inside flusgrid 1
function flusgrid:realm/tile_coords
execute if score #inside flusgrid matches 0 run function flusgrid:realm/tile_lookup_nether with storage flusgrid:realm scratch.tile
execute if score #inside flusgrid matches 0 run function flusgrid:realm/request_here_nether
execute if score #inside flusgrid matches 1 if score #main flusgrid matches 1 run function flusgrid:realm/request_main_nether
execute if score #inside flusgrid matches 1 if score #main flusgrid matches 0 run function flusgrid:realm/request_neighbors_nether
execute if score #inside flusgrid matches 0 run return run function flusgrid:realm/hold10_nether
function flusgrid:realm/checkpoint_safe
execute if score #safe flusgrid matches 1 if entity @s[nbt={OnGround:1b}] run function flusgrid:realm/checkpoint
