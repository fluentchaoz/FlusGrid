data modify storage flusgrid:realm bounds.nether set from storage flusgrid:realm plan.bounds
data remove storage flusgrid:realm owner
data remove storage flusgrid:realm plan
tellraw @a {text:"FlusGrid: nether frontier expanded. New terrain is ready.",color:"green"}
