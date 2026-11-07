scoreboard objectives add flusgrid dummy
scoreboard players set #quiet flusgrid 0
execute if data storage flusgrid:job {state:"running"} run data modify storage flusgrid:job state set value "paused"
scoreboard players set #sixteen flusgrid 16
execute unless data storage flusgrid:ledger regions run data modify storage flusgrid:ledger regions set value {}
