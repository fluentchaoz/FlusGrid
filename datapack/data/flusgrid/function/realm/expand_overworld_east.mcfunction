execute if data storage flusgrid:job {state:"running"} run return 0
execute if data storage flusgrid:job {state:"paused"} run return 0
data modify storage flusgrid:realm plan set value {dimension:"overworld",direction:"east"}
data modify storage flusgrid:realm plan.bounds set from storage flusgrid:realm bounds.overworld
scoreboard players operation #rx flusgrid = #bmin_x flusgrid
scoreboard players operation #rz flusgrid = #bmin_z flusgrid
scoreboard players operation #ex flusgrid = #bmax_x flusgrid
scoreboard players operation #ez flusgrid = #bmax_z flusgrid
scoreboard players operation #rx flusgrid = #ex flusgrid
scoreboard players add #rx flusgrid 1
scoreboard players add #ex flusgrid 512
execute store result storage flusgrid:realm plan.bounds.max_x int 1 run scoreboard players get #ex flusgrid
function flusgrid:realm/rectangle_overworld
