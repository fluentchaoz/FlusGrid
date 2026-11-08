$execute positioned $(x) $(y) $(z) unless loaded ~ ~ ~ run return run function fg_portal_test:failed
$execute positioned $(x) $(y) $(z) run function fg_portal_test:safe
execute unless score #safe fpt_tick matches 1 run return run function fg_portal_test:failed
$execute store success score #returned fpt_tick run tp @s $(x) $(y) $(z) $(yaw) $(pitch)
execute unless score #returned fpt_tick matches 1 run return run function fg_portal_test:failed
scoreboard players operation @s fpt_prev = @s fpt_sd
scoreboard players add @s fpt_blocks 1
scoreboard players set @s fpt_notice 100
title @s times 5 60 10
title @s title {text:"Destination not ready",color:"yellow"}
title @s subtitle {text:"TEST: Returned to your portal approach",color:"white"}
tellraw @s {text:"TEST RETURN: source checkpoint restored. The destination coordinates were recorded; no gridding was queued.",color:"yellow"}
