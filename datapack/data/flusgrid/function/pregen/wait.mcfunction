execute store result score #wait flusgrid run data get storage flusgrid:job wait
scoreboard players add #wait flusgrid 1
execute store result storage flusgrid:job wait int 1 run scoreboard players get #wait flusgrid
execute if score #wait flusgrid matches 1200.. run data modify storage flusgrid:job reason set value "Chunk generation wait exceeded 1,200 ticks. Resume to try loading again."
execute if score #wait flusgrid matches 1200.. run function flusgrid:pregen/fail
