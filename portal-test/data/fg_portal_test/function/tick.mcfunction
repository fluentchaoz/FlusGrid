scoreboard players add #clock fpt_tick 1
scoreboard players operation #previous fpt_tick = #clock fpt_tick
scoreboard players remove #previous fpt_tick 1
execute as @a[tag=fpt_enabled] at @s run function fg_portal_test:player
