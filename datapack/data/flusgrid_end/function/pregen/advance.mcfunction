execute store result score #done flusgrid run data get storage flusgrid_end:job done
scoreboard players add #done flusgrid 1
execute store result storage flusgrid_end:job done int 1 run scoreboard players get #done flusgrid
execute store result score #py flusgrid run data get storage flusgrid_end:job cursor.y
scoreboard players remove #py flusgrid 16
execute store result storage flusgrid_end:job cursor.y int 1 run scoreboard players get #py flusgrid
execute if score #py flusgrid matches ..-16 run function flusgrid_end:pregen/next_chunk
