function flusgrid_end:pregen/release
execute store result score #chunks flusgrid run data get storage flusgrid_end:job chunks
scoreboard players add #chunks flusgrid 1
execute store result storage flusgrid_end:job chunks int 1 run scoreboard players get #chunks flusgrid
scoreboard players operation #percent flusgrid = #chunks flusgrid
scoreboard players set #hundred flusgrid 100
execute store result score #chunk_total flusgrid run data get storage flusgrid_end:job chunk_total
scoreboard players operation #percent flusgrid *= #hundred flusgrid
scoreboard players operation #percent flusgrid /= #chunk_total flusgrid
execute store result storage flusgrid_end:job percent int 1 run scoreboard players get #percent flusgrid
title @a actionbar [{text:"FlusGrid End preparation: "},{nbt:"percent",storage:"flusgrid_end:job"},{text:"% | "},{nbt:"chunks",storage:"flusgrid_end:job"},{text:" / "},{nbt:"chunk_total",storage:"flusgrid_end:job"},{text:" chunks"}]
execute if score #chunks flusgrid >= #chunk_total flusgrid run return run function flusgrid_end:pregen/finish
data modify storage flusgrid_end:job cursor.y set value 240
execute store result score #px flusgrid run data get storage flusgrid_end:job cursor.x
execute store result score #max_x flusgrid run data get storage flusgrid_end:job max_x
scoreboard players add #px flusgrid 16
execute if score #px flusgrid > #max_x flusgrid run function flusgrid_end:pregen/next_row
execute store result storage flusgrid_end:job cursor.x int 1 run scoreboard players get #px flusgrid
