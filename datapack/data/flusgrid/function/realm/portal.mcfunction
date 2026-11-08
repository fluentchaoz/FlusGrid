execute if data storage flusgrid:realm {portal_built:1b} run return 0
fill -3 -33 -3 3 -33 3 minecraft:obsidian strict
fill -3 -32 -3 3 -29 3 minecraft:air strict
setblock -2 -32 -1 minecraft:end_portal_frame[facing=east,eye=false] strict
setblock 2 -32 -1 minecraft:end_portal_frame[facing=west,eye=false] strict
setblock -1 -32 -2 minecraft:end_portal_frame[facing=south,eye=false] strict
setblock -1 -32 2 minecraft:end_portal_frame[facing=north,eye=false] strict
setblock -2 -32 0 minecraft:end_portal_frame[facing=east,eye=false] strict
setblock 2 -32 0 minecraft:end_portal_frame[facing=west,eye=false] strict
setblock 0 -32 -2 minecraft:end_portal_frame[facing=south,eye=false] strict
setblock 0 -32 2 minecraft:end_portal_frame[facing=north,eye=false] strict
setblock -2 -32 1 minecraft:end_portal_frame[facing=east,eye=false] strict
setblock 2 -32 1 minecraft:end_portal_frame[facing=west,eye=false] strict
setblock 1 -32 -2 minecraft:end_portal_frame[facing=south,eye=false] strict
setblock 1 -32 2 minecraft:end_portal_frame[facing=north,eye=false] strict
data modify storage flusgrid:realm portal_built set value 1b
