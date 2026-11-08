function flusgrid:realm/tile_mark_nether with storage flusgrid:realm plan
data remove storage flusgrid:realm owner
data remove storage flusgrid:realm plan
tellraw @a {text:"FlusGrid: nether tile finished; that destination is now usable.",color:"green"}
