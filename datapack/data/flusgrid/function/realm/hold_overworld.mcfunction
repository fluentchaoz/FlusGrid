execute unless score @s fg_sd matches 1 run tp @s 0 81 0
execute if score @s fg_sd matches 1 store result storage flusgrid:realm return.x double 0.001 run scoreboard players get @s fg_sx
execute if score @s fg_sd matches 1 store result storage flusgrid:realm return.y double 0.001 run scoreboard players get @s fg_sy
execute if score @s fg_sd matches 1 store result storage flusgrid:realm return.z double 0.001 run scoreboard players get @s fg_sz
execute if score @s fg_sd matches 1 run function flusgrid:realm/return with storage flusgrid:realm return
effect give @s minecraft:slow_falling 3 0 true
title @s actionbar {text:"Preparing the next region. Stay inside the finished frontier.",color:"yellow"}
