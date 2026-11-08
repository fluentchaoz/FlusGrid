scoreboard objectives add flusgrid dummy
scoreboard players set #quiet flusgrid 0
execute in minecraft:the_nether run function flusgrid_nether:pregen/release
execute if data storage flusgrid_nether:job {state:"running"} run data modify storage flusgrid_nether:job state set value "paused"
scoreboard players set #sixteen flusgrid 16
execute if data storage flusgrid_nether:job {kind:"pregen"} unless data storage flusgrid_nether:job chunk_total run data modify storage flusgrid_nether:job chunk_total set value 1024
execute if data storage flusgrid_nether:job {kind:"pregen"} unless data storage flusgrid_nether:job size run data modify storage flusgrid_nether:job size set value 512
execute unless data storage flusgrid_nether:ledger regions run data modify storage flusgrid_nether:ledger regions set value {}
