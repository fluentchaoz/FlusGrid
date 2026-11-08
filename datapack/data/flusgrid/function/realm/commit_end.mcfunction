data modify storage flusgrid:realm bounds.end set from storage flusgrid:realm plan.bounds
data remove storage flusgrid:realm owner
data remove storage flusgrid:realm plan
tellraw @a {text:"FlusGrid: end frontier expanded. New terrain is ready.",color:"green"}
