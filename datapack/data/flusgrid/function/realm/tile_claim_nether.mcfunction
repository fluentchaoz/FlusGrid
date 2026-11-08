data modify storage flusgrid:realm plan set from storage flusgrid:realm queue[0]
data modify storage flusgrid:realm owner set value "nether"
data remove storage flusgrid:realm queue[0]
tellraw @a {text:"FlusGrid: queued 512x512 nether tile started; finished terrain remains guarded.",color:"yellow"}
