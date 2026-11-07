$execute if data storage flusgrid:ledger regions."$(x),$(y),$(z)" run return run tellraw @a {text:"FlusGrid: region already recorded; refusing another conversion. Inspect /data get storage flusgrid:ledger",color:"yellow"}
$execute positioned $(x) $(y) $(z) run function flusgrid:internal/run with storage flusgrid:work origin
