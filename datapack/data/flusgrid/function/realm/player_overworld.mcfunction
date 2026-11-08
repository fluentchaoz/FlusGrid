execute store result score @s fg_x run data get entity @s Pos[0] 1
execute store result score @s fg_y run data get entity @s Pos[1] 1
execute store result score @s fg_z run data get entity @s Pos[2] 1
execute store result score #bmin_x flusgrid run data get storage flusgrid:realm bounds.overworld.min_x
execute store result score #bmax_x flusgrid run data get storage flusgrid:realm bounds.overworld.max_x
execute store result score #bmin_z flusgrid run data get storage flusgrid:realm bounds.overworld.min_z
execute store result score #bmax_z flusgrid run data get storage flusgrid:realm bounds.overworld.max_z
scoreboard players set #outside flusgrid 0
execute if score #scan_clock flusgrid matches 10.. if score #scan_dim flusgrid matches 0 unless data storage flusgrid:realm owner unless data storage flusgrid:realm {manual_pause:1b} run function flusgrid:realm/request_overworld
scoreboard players operation #smin_x flusgrid = #bmin_x flusgrid
scoreboard players operation #smax_x flusgrid = #bmax_x flusgrid
scoreboard players add #smin_x flusgrid 512
scoreboard players remove #smax_x flusgrid 512
execute if score @s fg_x < #smin_x flusgrid run scoreboard players set #outside flusgrid 1
execute if score @s fg_x > #smax_x flusgrid run scoreboard players set #outside flusgrid 1
scoreboard players operation #smin_z flusgrid = #bmin_z flusgrid
scoreboard players operation #smax_z flusgrid = #bmax_z flusgrid
scoreboard players add #smin_z flusgrid 512
scoreboard players remove #smax_z flusgrid 512
execute if score @s fg_z < #smin_z flusgrid run scoreboard players set #outside flusgrid 1
execute if score @s fg_z > #smax_z flusgrid run scoreboard players set #outside flusgrid 1
execute if score #outside flusgrid matches 1 unless data storage flusgrid:realm owner unless data storage flusgrid:realm {manual_pause:1b} run function flusgrid:realm/request_overworld
execute if score #outside flusgrid matches 1 run return run function flusgrid:realm/hold_overworld
execute store result score @s fg_sx run data get entity @s Pos[0] 1000
execute store result score @s fg_sy run data get entity @s Pos[1] 1000
execute store result score @s fg_sz run data get entity @s Pos[2] 1000
scoreboard players set @s fg_sd 1
