execute unless score #rx flusgrid matches -29999984..29999968 run return 0
execute unless score #ex flusgrid matches -29999969..29999983 run return 0
scoreboard players operation #nx flusgrid = #ex flusgrid
scoreboard players operation #nx flusgrid -= #rx flusgrid
scoreboard players add #nx flusgrid 1
scoreboard players operation #nx flusgrid /= #sixteen flusgrid
scoreboard players remove #ex flusgrid 15
execute store result storage flusgrid:realm rectangle.x int 1 run scoreboard players get #rx flusgrid
execute store result storage flusgrid:realm rectangle.ex int 1 run scoreboard players get #ex flusgrid
execute unless score #rz flusgrid matches -29999984..29999968 run return 0
execute unless score #ez flusgrid matches -29999969..29999983 run return 0
scoreboard players operation #nz flusgrid = #ez flusgrid
scoreboard players operation #nz flusgrid -= #rz flusgrid
scoreboard players add #nz flusgrid 1
scoreboard players operation #nz flusgrid /= #sixteen flusgrid
scoreboard players remove #ez flusgrid 15
execute store result storage flusgrid:realm rectangle.z int 1 run scoreboard players get #rz flusgrid
execute store result storage flusgrid:realm rectangle.ez int 1 run scoreboard players get #ez flusgrid
scoreboard players operation #nx flusgrid *= #nz flusgrid
execute store result storage flusgrid:realm rectangle.chunks int 1 run scoreboard players get #nx flusgrid
scoreboard players set #sections flusgrid 16
scoreboard players operation #nx flusgrid *= #sections flusgrid
execute store result storage flusgrid:realm rectangle.total int 1 run scoreboard players get #nx flusgrid
execute in minecraft:the_nether run function flusgrid_nether:pregen/rectangle with storage flusgrid:realm rectangle
execute if data storage flusgrid_nether:job {state:"running"} run data modify storage flusgrid:realm owner set value "nether"
tellraw @a {text:"FlusGrid: preparing a new 512-block-wide nether strip. The frontier opens when it finishes.",color:"yellow"}
