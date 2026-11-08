execute store result score #done flusgrid run data get storage flusgrid_nether:job done
scoreboard players add #done flusgrid 1
execute store result storage flusgrid_nether:job done int 1 run scoreboard players get #done flusgrid
execute store result score #py flusgrid run data get storage flusgrid_nether:job cursor.y
scoreboard players remove #py flusgrid 16
execute store result storage flusgrid_nether:job cursor.y int 1 run scoreboard players get #py flusgrid
execute if score #py flusgrid matches ..-16 run function flusgrid_nether:pregen/next_chunk
