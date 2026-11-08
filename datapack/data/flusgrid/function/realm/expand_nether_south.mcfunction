execute if data storage flusgrid_nether:job {state:"running"} run return 0
execute if data storage flusgrid_nether:job {state:"paused"} run return 0
data modify storage flusgrid:realm plan set value {dimension:"nether",direction:"south"}
data modify storage flusgrid:realm plan.bounds set from storage flusgrid:realm bounds.nether
scoreboard players operation #rx flusgrid = #bmin_x flusgrid
scoreboard players operation #rz flusgrid = #bmin_z flusgrid
scoreboard players operation #ex flusgrid = #bmax_x flusgrid
scoreboard players operation #ez flusgrid = #bmax_z flusgrid
scoreboard players operation #rz flusgrid = #ez flusgrid
scoreboard players add #rz flusgrid 1
scoreboard players add #ez flusgrid 512
execute store result storage flusgrid:realm plan.bounds.max_z int 1 run scoreboard players get #ez flusgrid
function flusgrid:realm/rectangle_nether
