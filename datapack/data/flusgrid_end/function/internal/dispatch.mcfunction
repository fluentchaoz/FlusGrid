$execute if data storage flusgrid_end:ledger regions."$(x),$(y),$(z)" run return run tellraw @a {text:"FlusGrid End: region already recorded; refusing another conversion. Inspect /data get storage flusgrid_end:ledger",color:"yellow"}
$execute positioned $(x) $(y) $(z) run function flusgrid_end:internal/run with storage flusgrid_end:work origin
