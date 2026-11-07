execute unless entity @s[type=minecraft:player] run return 0
execute unless dimension minecraft:overworld run return 0
execute unless entity @s[gamemode=creative] unless entity @s[gamemode=spectator] run return run tellraw @s {text:"Prepare a disposable world in Creative or Spectator first.",color:"red"}
execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status
execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status
execute store result score #px flusgrid run data get entity @s Pos[0] 1
scoreboard players operation #mod flusgrid = #px flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
scoreboard players operation #px flusgrid -= #mod flusgrid
scoreboard players remove #px flusgrid 256
execute store result storage flusgrid:work pregen.x int 1 run scoreboard players get #px flusgrid
execute store result score #pz flusgrid run data get entity @s Pos[2] 1
scoreboard players operation #mod flusgrid = #pz flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
scoreboard players operation #pz flusgrid -= #mod flusgrid
scoreboard players remove #pz flusgrid 256
execute store result storage flusgrid:work pregen.z int 1 run scoreboard players get #pz flusgrid
function flusgrid:pregen_start with storage flusgrid:work pregen
