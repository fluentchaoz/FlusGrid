scoreboard players operation #trigger flusgrid = #bmin_x flusgrid
scoreboard players add #trigger flusgrid 768
execute if score @s fg_x <= #trigger flusgrid run return run function flusgrid:realm/expand_end_west
scoreboard players operation #trigger flusgrid = #bmax_x flusgrid
scoreboard players remove #trigger flusgrid 768
execute if score @s fg_x >= #trigger flusgrid run return run function flusgrid:realm/expand_end_east
scoreboard players operation #trigger flusgrid = #bmin_z flusgrid
scoreboard players add #trigger flusgrid 768
execute if score @s fg_z <= #trigger flusgrid run return run function flusgrid:realm/expand_end_north
scoreboard players operation #trigger flusgrid = #bmax_z flusgrid
scoreboard players remove #trigger flusgrid 768
execute if score @s fg_z >= #trigger flusgrid run return run function flusgrid:realm/expand_end_south
