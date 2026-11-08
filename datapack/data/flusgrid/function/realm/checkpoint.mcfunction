execute store result score @s fg_sx run data get entity @s Pos[0] 16
execute store result score @s fg_sy run data get entity @s Pos[1] 16
execute store result score @s fg_sz run data get entity @s Pos[2] 16
execute store result score @s fg_yaw run data get entity @s Rotation[0] 1000
execute store result score @s fg_pitch run data get entity @s Rotation[1] 1000
scoreboard players operation @s fg_sd = #current flusgrid
