function flusgrid:pregen/release
execute store result score #chunks flusgrid run data get storage flusgrid:job chunks
scoreboard players add #chunks flusgrid 1
execute store result storage flusgrid:job chunks int 1 run scoreboard players get #chunks flusgrid
scoreboard players operation #percent flusgrid = #chunks flusgrid
scoreboard players set #hundred flusgrid 100
scoreboard players set #chunk_total flusgrid 1024
scoreboard players operation #percent flusgrid *= #hundred flusgrid
scoreboard players operation #percent flusgrid /= #chunk_total flusgrid
execute store result storage flusgrid:job percent int 1 run scoreboard players get #percent flusgrid
title @a actionbar [{text:"FlusGrid preparation: "},{nbt:"percent",storage:"flusgrid:job"},{text:"% | "},{nbt:"chunks",storage:"flusgrid:job"},{text:" / 1024 chunks"}]
execute if score #chunks flusgrid matches 1024 run return run function flusgrid:pregen/finish
data modify storage flusgrid:job cursor.y set value 304
execute store result score #px flusgrid run data get storage flusgrid:job cursor.x
execute store result score #max_x flusgrid run data get storage flusgrid:job max_x
scoreboard players add #px flusgrid 16
execute if score #px flusgrid > #max_x flusgrid run function flusgrid:pregen/next_row
execute store result storage flusgrid:job cursor.x int 1 run scoreboard players get #px flusgrid
