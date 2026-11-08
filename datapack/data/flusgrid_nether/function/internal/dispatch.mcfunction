$execute if data storage flusgrid_nether:ledger regions."$(x),$(y),$(z)" run return run tellraw @a {text:"FlusGrid Nether: region already recorded; refusing another conversion. Inspect /data get storage flusgrid_nether:ledger",color:"yellow"}
$execute positioned $(x) $(y) $(z) run function flusgrid_nether:internal/run with storage flusgrid_nether:work origin
