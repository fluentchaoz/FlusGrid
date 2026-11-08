execute unless data storage flusgrid:fixtures end{ready:1b} in minecraft:the_end run return run function flusgrid:realm/fixture_tick_end
data modify storage flusgrid:realm bounds.end set from storage flusgrid:realm start_bounds
execute in minecraft:the_end run function flusgrid:realm/platform_end
execute in minecraft:the_end run function flusgrid:realm/fixture_release_end
data merge storage flusgrid:realm {state:"ready",phase:"complete",live:1b}
data remove storage flusgrid:realm owner
tellraw @a {text:"FlusGrid 10K initial campaign completed. Inspect and back up the world before multiplayer.",color:"green"}
