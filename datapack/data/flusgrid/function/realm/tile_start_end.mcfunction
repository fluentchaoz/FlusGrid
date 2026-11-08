$scoreboard players set #rx flusgrid $(x)
$scoreboard players set #rz flusgrid $(z)
scoreboard players operation #ex flusgrid = #rx flusgrid
scoreboard players operation #ez flusgrid = #rz flusgrid
scoreboard players add #ex flusgrid 496
scoreboard players add #ez flusgrid 496
execute store result storage flusgrid:realm rectangle.x int 1 run scoreboard players get #rx flusgrid
execute store result storage flusgrid:realm rectangle.z int 1 run scoreboard players get #rz flusgrid
execute store result storage flusgrid:realm rectangle.ex int 1 run scoreboard players get #ex flusgrid
execute store result storage flusgrid:realm rectangle.ez int 1 run scoreboard players get #ez flusgrid
data merge storage flusgrid:realm {rectangle:{chunks:1024,total:16384}}
execute in minecraft:the_end run function flusgrid_end:pregen/rectangle with storage flusgrid:realm rectangle
execute if data storage flusgrid_end:job {state:"running"} run function flusgrid:realm/tile_claim_end
