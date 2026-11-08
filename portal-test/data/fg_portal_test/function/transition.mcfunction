scoreboard players operation @s fpt_dd = @s fpt_dim
execute store result score @s fpt_dx run data get entity @s Pos[0] 16
execute store result score @s fpt_dy run data get entity @s Pos[1] 16
execute store result score @s fpt_dz run data get entity @s Pos[2] 16
execute if score @s fpt_allow matches 1 run return run function fg_portal_test:accept
execute unless score @s fpt_valid matches 1 run return run function fg_portal_test:failed
execute unless score @s fpt_sd = @s fpt_prev run return run function fg_portal_test:failed
execute store success score @s fpt_mount on vehicle if entity @s
execute if score @s fpt_mount matches 1 run return run function fg_portal_test:failed
execute store result storage fg_portal_test:work return.x double 0.0625 run scoreboard players get @s fpt_x
execute store result storage fg_portal_test:work return.y double 0.0625 run scoreboard players get @s fpt_y
execute store result storage fg_portal_test:work return.z double 0.0625 run scoreboard players get @s fpt_z
execute store result storage fg_portal_test:work return.yaw double 0.001 run scoreboard players get @s fpt_yaw
execute store result storage fg_portal_test:work return.pitch double 0.001 run scoreboard players get @s fpt_pitch
execute if score @s fpt_sd matches 1 in minecraft:overworld run return run function fg_portal_test:return with storage fg_portal_test:work return
execute if score @s fpt_sd matches 2 in minecraft:the_nether run return run function fg_portal_test:return with storage fg_portal_test:work return
execute if score @s fpt_sd matches 3 in minecraft:the_end run return run function fg_portal_test:return with storage fg_portal_test:work return
function fg_portal_test:failed
