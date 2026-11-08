scoreboard players set @s fpt_allow 0
scoreboard players set @s fpt_notice 0
scoreboard players operation @s fpt_prev = @s fpt_dim
scoreboard players set @s fpt_valid 0
tellraw @s {text:"TEST: Destination accepted. Step away from the portal onto an open solid floor to record a new return point.",color:"green"}
