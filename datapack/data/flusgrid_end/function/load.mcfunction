scoreboard objectives add flusgrid dummy
scoreboard players set #quiet flusgrid 0
execute in minecraft:the_end run function flusgrid_end:pregen/release
execute if data storage flusgrid_end:job {state:"running"} run data modify storage flusgrid_end:job state set value "paused"
scoreboard players set #sixteen flusgrid 16
execute if data storage flusgrid_end:job {kind:"pregen"} unless data storage flusgrid_end:job chunk_total run data modify storage flusgrid_end:job chunk_total set value 1024
execute if data storage flusgrid_end:job {kind:"pregen"} unless data storage flusgrid_end:job size run data modify storage flusgrid_end:job size set value 512
execute unless data storage flusgrid_end:ledger regions run data modify storage flusgrid_end:ledger regions set value {}
