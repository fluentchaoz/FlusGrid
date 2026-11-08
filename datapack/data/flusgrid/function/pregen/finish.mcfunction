execute in minecraft:overworld run function flusgrid:pregen/release
data modify storage flusgrid:job state set value "complete"
data modify storage flusgrid:job reason set value ""
tellraw @a {text:"FlusGrid: preparation complete! All selected chunks handled; owned force-load ticket released. Terrain beyond the prepared square remains normal.",color:"green"}
