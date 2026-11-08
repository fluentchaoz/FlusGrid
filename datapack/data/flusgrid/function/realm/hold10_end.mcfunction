execute store result storage flusgrid:realm scratch.return.x double 0.0625 run scoreboard players get @s fg_sx
execute store result storage flusgrid:realm scratch.return.y double 0.0625 run scoreboard players get @s fg_sy
execute store result storage flusgrid:realm scratch.return.z double 0.0625 run scoreboard players get @s fg_sz
execute store result storage flusgrid:realm scratch.return.yaw double 0.001 run scoreboard players get @s fg_yaw
execute store result storage flusgrid:realm scratch.return.pitch double 0.001 run scoreboard players get @s fg_pitch
execute if score @s fg_sd matches 1 in minecraft:overworld run return run function flusgrid:realm/return10 with storage flusgrid:realm scratch.return
execute if score @s fg_sd matches 2 in minecraft:the_nether run return run function flusgrid:realm/return10 with storage flusgrid:realm scratch.return
execute if score @s fg_sd matches 3 in minecraft:the_end run return run function flusgrid:realm/return10 with storage flusgrid:realm scratch.return
title @s actionbar {text:"Region not ready. No saved portal approach; ask an operator for help.",color:"red"}
