execute unless entity @s[type=minecraft:player] run return 0
execute unless dimension minecraft:overworld run return 0
execute unless entity @s[gamemode=creative] unless entity @s[gamemode=spectator] run return run tellraw @s {text:"Use Creative or Spectator in your disposable test world.",color:"red"}
execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status
execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status
execute store result score #ax flusgrid run data get entity @s Pos[0] 1
scoreboard players operation #mod flusgrid = #ax flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
scoreboard players operation #ax flusgrid -= #mod flusgrid
scoreboard players remove #ax flusgrid 16
execute store result storage flusgrid:work area.x int 1 run scoreboard players get #ax flusgrid
execute store result score #az flusgrid run data get entity @s Pos[2] 1
scoreboard players operation #mod flusgrid = #az flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
scoreboard players operation #az flusgrid -= #mod flusgrid
scoreboard players remove #az flusgrid 16
execute store result storage flusgrid:work area.z int 1 run scoreboard players get #az flusgrid
function flusgrid:area_start with storage flusgrid:work area
