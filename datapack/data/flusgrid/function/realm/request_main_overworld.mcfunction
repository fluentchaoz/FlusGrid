scoreboard players operation #threshold flusgrid = #bmin_x flusgrid
execute store result score #lead flusgrid run data get storage flusgrid:realm edge_lead
scoreboard players add #threshold flusgrid 0
scoreboard players operation #threshold flusgrid += #lead flusgrid
execute if score @s fg_x <= #threshold flusgrid run function flusgrid:realm/main_overworld_west
scoreboard players operation #threshold flusgrid = #bmax_x flusgrid
execute store result score #lead flusgrid run data get storage flusgrid:realm edge_lead
scoreboard players remove #threshold flusgrid 0
scoreboard players operation #threshold flusgrid -= #lead flusgrid
execute if score @s fg_x >= #threshold flusgrid run function flusgrid:realm/main_overworld_east
scoreboard players operation #threshold flusgrid = #bmin_z flusgrid
execute store result score #lead flusgrid run data get storage flusgrid:realm edge_lead
scoreboard players add #threshold flusgrid 0
scoreboard players operation #threshold flusgrid += #lead flusgrid
execute if score @s fg_z <= #threshold flusgrid run function flusgrid:realm/main_overworld_north
scoreboard players operation #threshold flusgrid = #bmax_z flusgrid
execute store result score #lead flusgrid run data get storage flusgrid:realm edge_lead
scoreboard players remove #threshold flusgrid 0
scoreboard players operation #threshold flusgrid -= #lead flusgrid
execute if score @s fg_z >= #threshold flusgrid run function flusgrid:realm/main_overworld_south
