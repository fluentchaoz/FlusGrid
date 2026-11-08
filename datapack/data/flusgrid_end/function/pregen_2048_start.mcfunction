# Explicit minimum corner. Exactly 128x128 chunks; fixed 2048-block side.
execute unless dimension minecraft:the_end run return 0
execute if data storage flusgrid_end:job {state:"running"} run return run function flusgrid_end:status
execute if data storage flusgrid_end:job {state:"paused"} run return run function flusgrid_end:status
$scoreboard players set #px flusgrid $(x)
$scoreboard players set #pz flusgrid $(z)
execute unless score #px flusgrid matches -29999984..29997936 run return 0
scoreboard players operation #mod flusgrid = #px flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid End: X and Z must be multiples of 16.",color:"red"}
execute unless score #pz flusgrid matches -29999984..29997936 run return 0
scoreboard players operation #mod flusgrid = #pz flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid End: X and Z must be multiples of 16.",color:"red"}
execute in minecraft:the_end run function flusgrid_end:pregen/release
data merge storage flusgrid_end:job {kind:"pregen",state:"preparing",done:0,total:262144,chunks:0,chunk_total:16384,size:2048,percent:0,wait:0,reason:"",cursor:{y:240}}
data remove storage flusgrid_end:job pending
execute store result storage flusgrid_end:job cursor.x int 1 run scoreboard players get #px flusgrid
execute store result storage flusgrid_end:job min_x int 1 run scoreboard players get #px flusgrid
scoreboard players add #px flusgrid 2032
execute store result storage flusgrid_end:job max_x int 1 run scoreboard players get #px flusgrid
execute store result storage flusgrid_end:job cursor.z int 1 run scoreboard players get #pz flusgrid
execute store result storage flusgrid_end:job min_z int 1 run scoreboard players get #pz flusgrid
scoreboard players add #pz flusgrid 2032
execute store result storage flusgrid_end:job max_z int 1 run scoreboard players get #pz flusgrid
data modify storage flusgrid_end:job state set value "running"
tellraw @a {text:"FlusGrid End: preparing 2048x2048 blocks, full End height. 16,384 chunks; at most one owned force-load ticket. Keep this local world running; do not play Survival yet. Controls: status, pause, resume.",color:"yellow"}
function flusgrid_end:pregen/status
