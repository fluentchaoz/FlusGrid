data remove storage flusgrid:job pending[0]
execute store result score #done flusgrid run data get storage flusgrid:job done
scoreboard players add #done flusgrid 1
execute store result storage flusgrid:job done int 1 run scoreboard players get #done flusgrid
execute unless data storage flusgrid:job pending[0] run function flusgrid:area/finish
