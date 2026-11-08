execute unless entity @s[tag=fpt_enabled] run return run tellraw @s {text:"Arm the test first.",color:"yellow"}
scoreboard players set @s fpt_allow 1
tellraw @s {text:"TEST: Your next dimension change is allowed. This simulates a ready destination; nothing has been gridded.",color:"green"}
