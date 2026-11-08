# Operator API. Explicit integer origins; no relative coordinates.
execute if data storage flusgrid_nether:job {state:"running"} run return 0
execute if data storage flusgrid_nether:job {state:"paused"} run return 0
execute unless dimension minecraft:the_nether run return run tellraw @a {text:"FlusGrid Nether: Nether only.",color:"red"}
$scoreboard players set #x flusgrid $(x)
$scoreboard players set #y flusgrid $(y)
$scoreboard players set #z flusgrid $(z)
execute unless score #x flusgrid matches -29999984..29999968 run return 0
execute unless score #z flusgrid matches -29999984..29999968 run return 0
execute unless score #y flusgrid matches 0..240 run return 0
scoreboard players operation #mod flusgrid = #x flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid Nether: origins must be multiples of 16.",color:"red"}
scoreboard players operation #mod flusgrid = #y flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid Nether: origins must be multiples of 16.",color:"red"}
scoreboard players operation #mod flusgrid = #z flusgrid
scoreboard players operation #mod flusgrid %= #sixteen flusgrid
execute unless score #mod flusgrid matches 0 run return run tellraw @a {text:"FlusGrid Nether: origins must be multiples of 16.",color:"red"}
execute store result storage flusgrid_nether:work origin.x int 1 run scoreboard players get #x flusgrid
execute store result storage flusgrid_nether:work origin.y int 1 run scoreboard players get #y flusgrid
execute store result storage flusgrid_nether:work origin.z int 1 run scoreboard players get #z flusgrid
function flusgrid_nether:internal/dispatch with storage flusgrid_nether:work origin
