data modify storage flusgrid:realm bounds.overworld set from storage flusgrid:realm plan.bounds
data remove storage flusgrid:realm owner
data remove storage flusgrid:realm plan
tellraw @a {text:"FlusGrid: overworld frontier expanded. New terrain is ready.",color:"green"}
