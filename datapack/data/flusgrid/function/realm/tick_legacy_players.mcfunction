scoreboard players add #scan_clock flusgrid 1
execute as @a[sort=random,gamemode=!creative,gamemode=!spectator] at @s if dimension minecraft:overworld run function flusgrid:realm/player_overworld
execute as @a[sort=random,gamemode=!creative,gamemode=!spectator] at @s if dimension minecraft:the_nether run function flusgrid:realm/player_nether
execute as @a[sort=random,gamemode=!creative,gamemode=!spectator] at @s if dimension minecraft:the_end run function flusgrid:realm/player_end
execute if score #scan_clock flusgrid matches 10.. run function flusgrid:realm/scan_advance
