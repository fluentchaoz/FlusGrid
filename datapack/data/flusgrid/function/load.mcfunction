scoreboard objectives add flusgrid dummy
scoreboard players set #quiet flusgrid 0
execute in minecraft:overworld run function flusgrid:pregen/release
execute if data storage flusgrid:job {state:"running"} run data modify storage flusgrid:job state set value "paused"
scoreboard players set #sixteen flusgrid 16
execute if data storage flusgrid:job {kind:"pregen"} unless data storage flusgrid:job chunk_total run data modify storage flusgrid:job chunk_total set value 1024
execute if data storage flusgrid:job {kind:"pregen"} unless data storage flusgrid:job size run data modify storage flusgrid:job size set value 512
execute unless data storage flusgrid:ledger regions run data modify storage flusgrid:ledger regions set value {}
