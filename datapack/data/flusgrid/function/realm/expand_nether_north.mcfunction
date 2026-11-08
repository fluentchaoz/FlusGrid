execute if data storage flusgrid_nether:job {state:"running"} run return 0
execute if data storage flusgrid_nether:job {state:"paused"} run return 0
data modify storage flusgrid:realm plan set value {dimension:"nether",direction:"north"}
data modify storage flusgrid:realm plan.bounds set from storage flusgrid:realm bounds.nether
scoreboard players operation #rx flusgrid = #bmin_x flusgrid
scoreboard players operation #rz flusgrid = #bmin_z flusgrid
scoreboard players operation #ex flusgrid = #bmax_x flusgrid
scoreboard players operation #ez flusgrid = #bmax_z flusgrid
scoreboard players operation #ez flusgrid = #rz flusgrid
scoreboard players remove #ez flusgrid 1
scoreboard players remove #rz flusgrid 512
execute store result storage flusgrid:realm plan.bounds.min_z int 1 run scoreboard players get #rz flusgrid
function flusgrid:realm/rectangle_nether
