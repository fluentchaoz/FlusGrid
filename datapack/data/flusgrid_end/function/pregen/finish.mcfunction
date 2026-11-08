execute in minecraft:the_end run function flusgrid_end:pregen/release
data modify storage flusgrid_end:job state set value "complete"
data modify storage flusgrid_end:job reason set value ""
tellraw @a {text:"FlusGrid End: preparation complete! All selected chunks handled; owned force-load ticket released. Terrain beyond the prepared square remains normal.",color:"green"}
