execute in minecraft:the_nether run function flusgrid_nether:pregen/release
data modify storage flusgrid_nether:job state set value "complete"
data modify storage flusgrid_nether:job reason set value ""
tellraw @a {text:"FlusGrid Nether: preparation complete! All selected chunks handled; owned force-load ticket released. Terrain beyond the prepared square remains normal.",color:"green"}
