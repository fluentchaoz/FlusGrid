execute unless score @s fpt_epoch = #epoch fpt_tick run return run function fg_portal_test:stale
execute unless score @s fpt_last = #previous fpt_tick run return run function fg_portal_test:stale
scoreboard players operation @s fpt_last = #clock fpt_tick
execute if score @s fpt_deaths > @s fpt_seen run return run function fg_portal_test:stale
function fg_portal_test:dimension
execute unless score @s fpt_dim = @s fpt_prev run return run function fg_portal_test:transition
execute if score @s fpt_notice matches 1.. run title @s actionbar {text:"TEST: Destination not ready. Returned to your portal approach; no generation is running.",color:"yellow"}
execute if score @s fpt_notice matches 1.. run scoreboard players remove @s fpt_notice 1
execute store success score @s fpt_mount on vehicle if entity @s
execute if score @s fpt_mount matches 1 run return 0
function fg_portal_test:safe
execute if score #safe fpt_tick matches 1 run function fg_portal_test:save
