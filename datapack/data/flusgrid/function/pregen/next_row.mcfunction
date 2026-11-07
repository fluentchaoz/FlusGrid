execute store result score #px flusgrid run data get storage flusgrid:job min_x
execute store result score #pz flusgrid run data get storage flusgrid:job cursor.z
scoreboard players add #pz flusgrid 16
execute store result storage flusgrid:job cursor.z int 1 run scoreboard players get #pz flusgrid
