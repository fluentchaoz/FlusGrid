# Explicit minimum corner. Exactly 32x32 chunks; fixed 512-block side.
execute unless dimension minecraft:the_nether run return 0
execute if data storage flusgrid_nether:job {state:"running"} run return run function flusgrid_nether:status
execute if data storage flusgrid_nether:job {state:"paused"} run return run function flusgrid_nether:status
$scoreboard players set #px flusgrid $(x)
$scoreboard players set #pz flusgrid $(z)
execute unless score #px flusgrid matches -29999984..29999472 run return 0
scoreboard players operation #mod flusgrid = #px flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid Nether: X and Z must be multiples of 16.",color:"red"}
execute unless score #pz flusgrid matches -29999984..29999472 run return 0
scoreboard players operation #mod flusgrid = #pz flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid Nether: X and Z must be multiples of 16.",color:"red"}
execute in minecraft:the_nether run function flusgrid_nether:pregen/release
data merge storage flusgrid_nether:job {kind:"pregen",state:"preparing",done:0,total:16384,chunks:0,chunk_total:1024,size:512,percent:0,wait:0,reason:"",cursor:{y:240}}
data remove storage flusgrid_nether:job pending
execute store result storage flusgrid_nether:job cursor.x int 1 run scoreboard players get #px flusgrid
execute store result storage flusgrid_nether:job min_x int 1 run scoreboard players get #px flusgrid
scoreboard players add #px flusgrid 496
execute store result storage flusgrid_nether:job max_x int 1 run scoreboard players get #px flusgrid
execute store result storage flusgrid_nether:job cursor.z int 1 run scoreboard players get #pz flusgrid
execute store result storage flusgrid_nether:job min_z int 1 run scoreboard players get #pz flusgrid
scoreboard players add #pz flusgrid 496
execute store result storage flusgrid_nether:job max_z int 1 run scoreboard players get #pz flusgrid
data modify storage flusgrid_nether:job state set value "running"
tellraw @a {text:"FlusGrid Nether: preparing 512x512 blocks, full Nether height. 1,024 chunks; at most one owned force-load ticket. Keep this local world running; do not play Survival yet. Controls: status, pause, resume.",color:"yellow"}
function flusgrid_nether:pregen/status
