function flusgrid:realm/tile_mark_overworld with storage flusgrid:realm plan
data remove storage flusgrid:realm owner
data remove storage flusgrid:realm plan
tellraw @a {text:"FlusGrid: overworld tile finished; that destination is now usable.",color:"green"}
