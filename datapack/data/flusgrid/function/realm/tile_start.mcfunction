data modify storage flusgrid:realm dispatch set from storage flusgrid:realm queue[0]
execute if data storage flusgrid:realm {dispatch:{dimension:"overworld"}} run function flusgrid:realm/tile_start_overworld with storage flusgrid:realm dispatch
execute if data storage flusgrid:realm {dispatch:{dimension:"nether"}} run function flusgrid:realm/tile_start_nether with storage flusgrid:realm dispatch
execute if data storage flusgrid:realm {dispatch:{dimension:"end"}} run function flusgrid:realm/tile_start_end with storage flusgrid:realm dispatch
data remove storage flusgrid:realm dispatch
