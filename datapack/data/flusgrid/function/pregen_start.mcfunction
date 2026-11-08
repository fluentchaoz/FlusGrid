# Explicit minimum corner. Exactly 32x32 chunks; fixed 512-block side.
execute unless dimension minecraft:overworld run return 0
execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status
execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status
$scoreboard players set #px flusgrid $(x)
$scoreboard players set #pz flusgrid $(z)
execute unless score #px flusgrid matches -29999984..29999472 run return 0
scoreboard players operation #mod flusgrid = #px flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid: X and Z must be multiples of 16.",color:"red"}
execute unless score #pz flusgrid matches -29999984..29999472 run return 0
scoreboard players operation #mod flusgrid = #pz flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid: X and Z must be multiples of 16.",color:"red"}
execute in minecraft:overworld run function flusgrid:pregen/release
data merge storage flusgrid:job {kind:"pregen",state:"preparing",done:0,total:24576,chunks:0,chunk_total:1024,size:512,percent:0,wait:0,reason:"",cursor:{y:304}}
data remove storage flusgrid:job pending
execute store result storage flusgrid:job cursor.x int 1 run scoreboard players get #px flusgrid
execute store result storage flusgrid:job min_x int 1 run scoreboard players get #px flusgrid
scoreboard players add #px flusgrid 496
execute store result storage flusgrid:job max_x int 1 run scoreboard players get #px flusgrid
execute store result storage flusgrid:job cursor.z int 1 run scoreboard players get #pz flusgrid
execute store result storage flusgrid:job min_z int 1 run scoreboard players get #pz flusgrid
scoreboard players add #pz flusgrid 496
execute store result storage flusgrid:job max_z int 1 run scoreboard players get #pz flusgrid
data modify storage flusgrid:job state set value "running"
tellraw @a {text:"FlusGrid: preparing 512x512 blocks, full Overworld height. 1,024 chunks; at most one owned force-load ticket. Keep this local world running; do not play Survival yet. Controls: status, pause, resume.",color:"yellow"}
function flusgrid:pregen/status
