execute unless data storage flusgrid:fixtures end{acquired:1b} run return run function flusgrid:realm/fixture_acquire_end
scoreboard players set #fixtures_loaded flusgrid 1
execute unless loaded 96 80 -16 run scoreboard players set #fixtures_loaded flusgrid 0
execute unless loaded 96 80 0 run scoreboard players set #fixtures_loaded flusgrid 0
execute if score #fixtures_loaded flusgrid matches 1 run return run data modify storage flusgrid:fixtures end.ready set value 1b
execute store result score #fixture_wait flusgrid run data get storage flusgrid:fixtures end.wait
scoreboard players add #fixture_wait flusgrid 1
execute store result storage flusgrid:fixtures end.wait int 1 run scoreboard players get #fixture_wait flusgrid
execute if score #fixture_wait flusgrid matches 1200.. run function flusgrid:realm_pause
