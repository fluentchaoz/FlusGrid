function flusgrid:realm/tile_mark_end with storage flusgrid:realm plan
data remove storage flusgrid:realm owner
data remove storage flusgrid:realm plan
tellraw @a {text:"FlusGrid: end tile finished; that destination is now usable.",color:"green"}
