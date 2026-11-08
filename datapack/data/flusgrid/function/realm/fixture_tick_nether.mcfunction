execute unless data storage flusgrid:fixtures nether{acquired:1b} run return run function flusgrid:realm/fixture_acquire_nether
scoreboard players set #fixtures_loaded flusgrid 1
execute unless loaded -16 80 -16 run scoreboard players set #fixtures_loaded flusgrid 0
execute unless loaded -16 80 0 run scoreboard players set #fixtures_loaded flusgrid 0
execute unless loaded 0 80 -16 run scoreboard players set #fixtures_loaded flusgrid 0
execute unless loaded 0 80 0 run scoreboard players set #fixtures_loaded flusgrid 0
execute if score #fixtures_loaded flusgrid matches 1 run return run data modify storage flusgrid:fixtures nether.ready set value 1b
execute store result score #fixture_wait flusgrid run data get storage flusgrid:fixtures nether.wait
scoreboard players add #fixture_wait flusgrid 1
execute store result storage flusgrid:fixtures nether.wait int 1 run scoreboard players get #fixture_wait flusgrid
execute if score #fixture_wait flusgrid matches 1200.. run function flusgrid:realm_pause
