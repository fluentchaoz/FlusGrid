scoreboard players operation #rx flusgrid = #target_x flusgrid
scoreboard players operation #mod flusgrid = #rx flusgrid
scoreboard players operation #mod flusgrid %= #tile_size flusgrid
execute if score #mod flusgrid matches ..-1 run scoreboard players add #mod flusgrid 512
scoreboard players operation #rx flusgrid -= #mod flusgrid
execute unless score #rx flusgrid matches -29999984..29999472 run return 0
execute store result storage flusgrid:realm scratch.request.x int 1 run scoreboard players get #rx flusgrid
scoreboard players operation #rz flusgrid = #target_z flusgrid
scoreboard players operation #mod flusgrid = #rz flusgrid
scoreboard players operation #mod flusgrid %= #tile_size flusgrid
execute if score #mod flusgrid matches ..-1 run scoreboard players add #mod flusgrid 512
scoreboard players operation #rz flusgrid -= #mod flusgrid
execute unless score #rz flusgrid matches -29999984..29999472 run return 0
execute store result storage flusgrid:realm scratch.request.z int 1 run scoreboard players get #rz flusgrid
