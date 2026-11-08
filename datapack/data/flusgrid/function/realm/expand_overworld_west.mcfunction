execute if data storage flusgrid:job {state:"running"} run return 0
execute if data storage flusgrid:job {state:"paused"} run return 0
data modify storage flusgrid:realm plan set value {dimension:"overworld",direction:"west"}
data modify storage flusgrid:realm plan.bounds set from storage flusgrid:realm bounds.overworld
scoreboard players operation #rx flusgrid = #bmin_x flusgrid
scoreboard players operation #rz flusgrid = #bmin_z flusgrid
scoreboard players operation #ex flusgrid = #bmax_x flusgrid
scoreboard players operation #ez flusgrid = #bmax_z flusgrid
scoreboard players operation #ex flusgrid = #rx flusgrid
scoreboard players remove #ex flusgrid 1
scoreboard players remove #rx flusgrid 512
execute store result storage flusgrid:realm plan.bounds.min_x int 1 run scoreboard players get #rx flusgrid
function flusgrid:realm/rectangle_overworld
