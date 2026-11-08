execute if data storage flusgrid:realm platforms{overworld:1b} run return 0
fill -3 80 -3 3 80 3 minecraft:obsidian strict
fill -3 81 -3 3 84 3 minecraft:air strict
setworldspawn 0 81 0
gamerule minecraft:respawn_radius 0
data modify storage flusgrid:realm platforms.overworld set value 1b
