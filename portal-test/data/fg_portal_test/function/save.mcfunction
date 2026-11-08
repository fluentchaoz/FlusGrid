execute store result score @s fpt_x run data get entity @s Pos[0] 16
execute store result score @s fpt_y run data get entity @s Pos[1] 16
execute store result score @s fpt_z run data get entity @s Pos[2] 16
execute store result score @s fpt_yaw run data get entity @s Rotation[0] 1000
execute store result score @s fpt_pitch run data get entity @s Rotation[1] 1000
scoreboard players operation @s fpt_sd = @s fpt_dim
scoreboard players set @s fpt_valid 1
