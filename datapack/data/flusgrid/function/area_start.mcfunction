# Explicit lower X/Z corner API. 48x48 blocks, Y -64..319.
execute unless dimension minecraft:overworld run return 0
execute if data storage flusgrid:job {state:"running"} run return run function flusgrid:status
execute if data storage flusgrid:job {state:"paused"} run return run function flusgrid:status
$scoreboard players set #ax flusgrid $(x)
$scoreboard players set #az flusgrid $(z)
execute unless score #ax flusgrid matches -29999984..29999936 run return 0
scoreboard players operation #mod flusgrid = #ax flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return 0
execute unless score #az flusgrid matches -29999984..29999936 run return 0
scoreboard players operation #mod flusgrid = #az flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return 0
data merge storage flusgrid:job {kind:"area",state:"preparing",pending:[],done:0,total:216}
function flusgrid:area/enqueue
data modify storage flusgrid:job state set value "running"
tellraw @a {text:"FlusGrid: preparing 48x48 terrain, Y -64 through 319. Stay nearby in Creative/Spectator. /function flusgrid:pause stops between cubes.",color:"yellow"}
